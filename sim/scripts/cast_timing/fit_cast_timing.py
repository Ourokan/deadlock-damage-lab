"""When real Phantom+ players cast each hero ability in a fight, against when the sim does, and the hold that makes the
sim's first casts follow the real ones (Mechanics.cast_timing).

The sim's duels start with every cooldown ready and cast each ability the moment its rule allows: the ultimate goes
out at t=0 in ~90% of duels (real: 10-40% of fights by 20 s), and its cast lock / channel then keeps the gun quiet
for the first seconds, so the gun and the item procs riding on it land seconds later than in real fights
(validation/opener_timing.md: 66 sources clearly later in the sim). The opener-timing hold (Mechanics.opener_timing)
only moved the booking; this moves the casts.

real: the fight-length replays (fight_length/fetch_fights.py: two enemy heroes trading, gaps < 5 s, >= 4 hits both
ways, the unit the sim's fight-length booking is fitted on) and their ability casts (fetch_ability_casts.py: cooldown
starts per owner pawn, real_casts: not the cooldown cuts). For each fighter of a fight and each ability it has (cast before in the match, or in the
fight): the first cast from PRE_S before the fight's first hit (the cast that opens it), seconds after the first hit
(0 for an opening cast), censored by the fight's end: a Kaplan-Meier P(cast by t | fight still going). A cast on
another enemy of a team fight counts too (the cooldown is spent all the same).
sim: the damage audit's duels (real builds both sides) with the holds off: the same curve of each ability's first
cast (a duel ends at a death or 20 s).

Hold: for abilities the sim casts on sight (CAST_ON_SIGHT of its casts by 20 s within the first second), QBINS
equal-probability values of the real first cast time (None = not cast by HORIZON), less the sim's own median cast
time. Abilities the sim already gates (a health or stack condition) keep their own timing.

usage: python3 -I fit_cast_timing.py real [--fights DIR] [--casts DIR] [--workers 4]     -> work/cast_timing_real.json
       python3 -I fit_cast_timing.py fit [n=3000] [workers] [--write]   (sim duels with the holds off, then on)
       python3 -I fit_cast_timing.py fit [n] [workers] --hero NAME [--write]   (one hero, all its players)
fit writes data/cast_timing.json and validation/cast_timing.md (--hero: only that hero's rows in both, the others and
the report's mean gap line stay). Static snapshot: refit after a patch that changes
cooldowns, and after a hero file changes when an ability is cast. After a refit rerun fight_length/length_factors.py.
"""
import bisect
import collections
import gzip
import json
import os
import random
import statistics
import sys
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "fight_length"))
import fit_length as FL  # noqa: E402
import opener_timing as OT  # noqa: E402

FIGHTS = "/mnt/project-files/analysis/work/fight_length/raw/"
CASTS = "/mnt/project-files/analysis/work/cast_timing/raw/"
SAMPLE = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
REAL = os.path.join(ROOT, "validation", "cast_timing_real.json")
OUT = os.path.join(ROOT, "data", "cast_timing.json")
REPORT = os.path.join(ROOT, "validation", "cast_timing.md")
T = 64
PRE_S = 1.0          # a cast this long before the fight's first hit opens it (counts as t = 0)
GRID = [0.5 * k for k in range(41)]   # 0..20 s
HORIZON = 20.0
MIN_FIGHTS = 60      # real fights for a row
MIN_DUELS = 30
CAST_ON_SIGHT = 0.7
PROBE_SIGHT_S = 2.0  # held_opens == "first_hit" abilities: on sight in the probe run by then
QBINS = 20
LAG_MAX = 8.0        # a hit this long after the cast belongs to it (charge-up, fuse, travel, a DoT's first tick)
MIN_OFFSET_ROWS = 30  # rows on one tick -> game time offset for it to be a stretch of the match (real_casts)
MAX_LATER_S = 20.0    # a cast's cooldown can start this long after it (the ability's duration)
MIN_LAGS = 30        # casts with a hit for an ability's median cast -> hit time
PRECAST = True       # damage abilities: hold on when the damage lands (due), not the cast (holds())
# a fighter's overlapping pair fights merged into one engagement (as fit_item_use.py)? No: the sim's duel timeline is
# the pair fight's (its length booking, data/fight_length.json, is fitted on pair fights), and merged engagements put
# a later-joining enemy's whole fight after t0 (the curve came out ~1 s later than the hits, opener_timing.md)
MERGE = False
BUILD_COLS = False   # real_rows rows also carry build_cols() of the fighter at the fight start (ability_lean.py)


def cls_key(hid, cls):
    return f"{hid}:{cls}"


def km(rows):
    """rows (first cast s or None, fight length s): P(cast by t | still going) on GRID (Kaplan-Meier)."""
    ev = sorted((u if u is not None else d, u is not None) for u, d in rows)
    n, i, surv, out = len(ev), 0, 1.0, []
    for t in GRID:
        while i < n and ev[i][0] <= t:
            j, c = i, 0
            while j < n and ev[j][0] == ev[i][0]:
                c += ev[j][1]
                j += 1
            surv *= 1.0 - c / (n - i)
            i = j
        out.append(round(1.0 - surv, 4))
    return out


def real_casts(rows):
    """The rows that are casts. A cast sets the cooldown start to the current game time, a fixed offset from tick / T
    within a stretch of the match (a pause moves the offset: 1-10 stretches a replay, each hundreds of rows), or to a
    later time for an ability whose cooldown runs after its duration (Rem's Helping Hands, ~5 s). Cooldown cuts move
    the start back to an earlier time, which is no cast: Violet's Living Ink hits cut her other cooldowns 1.5 s (63% of
    her rows were cuts, so all four of her abilities followed the Living Ink hits: cast in 97-99% of fights by 20 s),
    Rem 63%, Deadman Danny 76%, most heroes 3-20% (Witchmail, cooldown items)."""
    rows = sorted((r for r in rows if r.get("k", "cast") == "cast"), key=lambda r: r["tick"])
    n = collections.Counter(round(r["tick"] / T - r["v"], 1) for r in rows)
    span = {}
    for r in rows:
        o = round(r["tick"] / T - r["v"], 1)
        if n[o] >= MIN_OFFSET_ROWS:
            span[o] = (span.get(o, (r["tick"],))[0], r["tick"])
    out, last = [], {}
    for r in rows:
        t = r["tick"] / T
        offs = [o for o, (t0, t1) in span.items() if t0 <= r["tick"] <= t1] or list(span)
        now = any(abs(t - r["v"] - o) < 0.1 for o in offs)
        later = 0 < r["v"] - (t - min(offs)) <= MAX_LATER_S if offs else False
        key = r["a"], r["s"]
        if now or (later and r["v"] > last.get(key, -1e9)):
            out.append(r)
        last[key] = max(last.get(key, -1e9), r["v"])
    return out


def build_cols(p, t, m, cache):
    """(spirit item souls, net worth, global ability cooldown reduction, match id) of player p's real build at game time
    t (per minute; ability_lean.py)."""
    key = (p["slot"], int(t // 60))
    if key not in cache:
        import landing_rates as L
        from deadsim import game
        from deadsim.build import compute_stats
        G = game()
        items, souls = L.build_at(p, max(0.0, key[1] * 60.0))
        st = compute_stats(G.hero(p["hero_id"]), [G.items[i] for i in items], souls=souls)
        cache[key] = (sum(G.items[i].cost for i in items if G.items[i].slot == "spirit"), souls, st.cdr, m["match_id"])
    return cache[key]


def real_rows(args):
    """[(hero id, ability class, first cast s or None, fight length s, its hit s after the cast or None, first due s
    or None)] for one match. Due: when the first cast's damage lands (its own hit, else the cast + the ability's
    median cast -> hit time from lags), counted from the fight's first hit; a cast before the fight whose damage
    lands from PRE_S before the first hit on opens it (a charged Kinetic Carbine fired 2 s before it lands)."""
    fn, cast_fn, m, abil, lags = args
    hero, ev = OT.read(fn)   # FL.read's rows + the hit's ability id
    by_hero = {p["hero_id"]: p for p in m["players"]}
    casts = collections.defaultdict(list)
    rc = real_casts([json.loads(line) for line in gzip.open(cast_fn, "rt")])
    off = statistics.median(r["tick"] / T - r["v"] for r in rc) if BUILD_COLS and rc else 0.0   # tick / T -> game time
    cache = {}
    for r in rc:
        casts[(r["a"], int(r["s"]))].append(r["tick"] / T)
    for v in casts.values():
        v.sort()
    pairs = collections.defaultdict(list)
    hits = collections.defaultdict(list)
    for e in ev:
        _, a, v = e[:3]
        pa, pv = by_hero.get(hero.get(a)), by_hero.get(hero.get(v))
        if pa is None or pv is None or pa["team"] == pv["team"]:
            continue
        pairs[min(a, v), max(a, v)].append(e)
        hits[a, e[6]].append(e[0])
    spans = collections.defaultdict(list)
    for (x, y), es in pairs.items():
        runs = []
        for e in es:
            if not runs or e[0] - runs[-1][-1][0] > FL.GAP_S:
                runs.append([])
            runs[-1].append(e)
        for f in runs:
            death = next((k for k, e in enumerate(f) if e[3] <= 0), None)
            if death is not None:
                f = f[:death + 1]
            if len(f) < FL.MIN_HITS or len({(e[1], e[2]) for e in f}) < 2:
                continue
            for pawn in (x, y):
                spans[pawn].append((f[0][0], f[-1][0]))
    out = []
    for pawn, sp in spans.items():
        hid = hero.get(pawn)
        if hid not in abil:
            continue
        sp.sort()
        merged = []
        for t0, t1 in sp:
            if MERGE and merged and t0 <= merged[-1][1] + FL.GAP_S:
                merged[-1][1] = max(merged[-1][1], t1)
            else:
                merged.append([t0, t1])
        for t0, t1 in merged:
            for aid, cls in abil[hid].items():
                cs = casts.get((pawn, aid), [])
                k = bisect.bisect_left(cs, t0 - PRE_S)
                first = cs[k] if k < len(cs) and cs[k] <= t1 else None
                if first is None and not (k > 0):
                    continue   # never cast before in the match: not unlocked (or never used) yet
                lag = None
                if first is not None:
                    hs = hits.get((pawn, aid), [])
                    j = bisect.bisect_left(hs, first)
                    if j < len(hs) and hs[j] - first <= LAG_MAX:
                        lag = hs[j] - first
                hs = hits.get((pawn, aid), [])
                due = None
                for c in cs[bisect.bisect_left(cs, t0 - LAG_MAX):]:
                    if c > t1:
                        break
                    j = bisect.bisect_left(hs, c)
                    d = hs[j] if j < len(hs) and hs[j] - c <= LAG_MAX else c + lags.get(cls_key(hid, cls), 0.0)
                    if d >= t0 - PRE_S:
                        due = max(0.0, d - t0)
                        break
                row = (hid, cls, None if first is None else max(0.0, first - t0), t1 - t0, lag, due)
                if BUILD_COLS and hid in by_hero:
                    row += build_cols(by_hero[hid], t0 - off, m, cache)
                out.append(row)
    return out


def real(fights_dir, casts_dir, workers):
    from deadsim import game
    G = game()
    abil = {h.id: {ab.id: ab.class_name for ab in h.abilities} for h in G.heroes.values()}
    mids = {f.split(".")[0] for f in os.listdir(casts_dir) if f.endswith(".ndjson.gz")}
    mids &= {f.split(".")[0] for f in os.listdir(fights_dir) if f.endswith(".ndjson.gz")}
    sample = FL.load_sample(SAMPLE, mids)
    jobs = [(os.path.join(fights_dir, f"{mid}.ndjson.gz"), os.path.join(casts_dir, f"{mid}.ndjson.gz"), sample[mid],
             abil) for mid in sorted(mids) if mid in sample]
    # two passes: the median cast -> hit time of each ability, then each fight's due time with it (a missed cast)
    med = {}
    for _ in range(2):
        rows = collections.defaultdict(list)
        dues = collections.defaultdict(list)
        lags = collections.defaultdict(list)
        with Pool(workers) as p:
            for rs in p.imap_unordered(real_rows, [j + (med,) for j in jobs]):
                for hid, cls, u, d, lag, due in rs:
                    rows[cls_key(hid, cls)].append((u, d))
                    dues[cls_key(hid, cls)].append((due, d))
                    if lag is not None:
                        lags[cls_key(hid, cls)].append(lag)
        med = {k: statistics.median(v) for k, v in lags.items() if len(v) >= MIN_LAGS}
    res = {"source": f"{len(jobs)} Phantom+ replays, pair fights (scripts/cast_timing/fit_cast_timing.py real)",
           "grid_s": GRID, "rows": {}}
    for key, rs in sorted(rows.items()):
        if len(rs) < MIN_FIGHTS:
            continue
        res["rows"][key] = {"fights": len(rs), "cast_share": round(sum(u is not None for u, _ in rs) / len(rs), 3),
                            "cast_by": km(rs)}
        if key in med:
            res["rows"][key]["hit_lag_s"] = round(med[key], 3)
            res["rows"][key]["due_by"] = km(dues[key])
    with open(REAL, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(len(res["rows"]), "rows from", len(jobs), "matches")


# ---- sim side ------------------------------------------------------------------------------------------------
def sim_job(args):
    j, timing, probe = args
    import damage_audit as A
    from deadsim import abilities, engine
    import dataclasses
    A.PROFILE = True
    engine.PROFILE_SOURCES = True
    A.MECH = dataclasses.replace(A.MECH, cast_timing=timing)
    abilities.PROBE_HELD = probe
    hid, d, _ = A.sim_player(j)
    return hid, {k: v for k, v in d.items() if k.startswith(("_cu:", "_cn:", "_fu:", "_fc:", "_lg:"))}


def sim_curves(n, workers, timing, probe=False, hero=None):
    """{"hero id:ability class": {"duels", "cast_by", "hit_by" on GRID (first cast / first hit)}} from the audit's
    duels (hero: that hero id's players only, all of them)."""
    from deadsim import game
    import landing_rates as L
    G = game()
    jobs = []
    for line in gzip.open(SAMPLE):
        m = json.loads(line)
        jobs += [(m, p["slot"]) for p in m["players"] if p["hero_id"] in G.heroes and L.gun_known(p)]
    random.Random(1).shuffle(jobs)
    if hero is not None:
        jobs = [j for j in jobs if next(p for p in j[0]["players"] if p["slot"] == j[1])["hero_id"] == hero]
        n = len(jobs)
    tot = collections.defaultdict(collections.Counter)
    with ProcessPoolExecutor(workers) as ex:
        for hid, d in ex.map(sim_job, [(j, timing, probe) for j in jobs[:n]], chunksize=8):
            for k, v in d.items():
                kind, cls, b = k.split(":")
                tot[f"{hid}:{cls}"][kind, int(b)] += v
    def curve(c, use, none):
        risk = sum(v for (k, _), v in c.items() if k in (use, none))
        n_all, surv, out = risk, 1.0, []
        for b in range(len(GRID)):
            u = c.get((use, b), 0)
            if risk:
                surv *= 1.0 - u / risk
            risk -= u + c.get((none, b), 0)
            out.append(round(1.0 - surv, 4))
        return n_all, out
    out = {}
    for key, c in tot.items():
        n_all, cast = curve(c, "_cu", "_cn")
        if not n_all:
            continue
        out[key] = {"duels": n_all, "cast_by": cast, "hit_by": curve(c, "_fu", "_fc")[1]}
        lg = sorted((b, v) for (k, b), v in c.items() if k == "_lg")
        n_lg = sum(v for _, v in lg)
        if n_lg >= MIN_LAGS:
            acc = 0
            for b, v in lg:
                acc += v
                if acc >= n_lg / 2:
                    out[key]["hit_lag_s"] = 0.25 * b + 0.125
                    break
    return out


def quantile(curve, p):
    """Smallest t on GRID (linear inside a step) with curve(t) >= p."""
    k = next((k for k in range(len(curve)) if curve[k] >= p), None)
    if k is None:
        return None
    if k == 0:
        return 0.0
    lo = curve[k - 1]
    return GRID[k] - 0.5 * (curve[k] - p) / max(1e-9, curve[k] - lo)


def holds(real, sim):
    """QBINS hold values: equal-probability points of the real first cast curve (None past its share cast by
    HORIZON: not cast in that fight), less the sim's own median first cast. For an ability that deals damage (a real
    and a sim cast -> hit time): points of the real due curve (when the first cast's damage lands) less the sim's
    median cast and cast -> hit time, so the sim's hits land when the real ones do. That can be negative, down to
    -(the sim's cast -> hit time): the cast went out before the fight and its hit opens it (a charged Kinetic Carbine,
    a fused Sticky Bomb; mechanics.precast)."""
    h = int(HORIZON / 0.5)
    sim_cast = sim["cast_by"]
    s_top = sim_cast[h] or 1.0
    s_med = quantile([v / s_top for v in sim_cast], 0.5) or 0.0
    curve, shift, floor = real["cast_by"], s_med, 0.0
    if PRECAST and "due_by" in real and sim.get("hit_lag_s") is not None:
        curve, shift, floor = real["due_by"], s_med + sim["hit_lag_s"], -sim["hit_lag_s"]
    out = []
    for b in range(QBINS):
        p = (b + 0.5) / QBINS
        if p > curve[h]:
            out.append(None)
            continue
        out.append(round(max(floor, quantile(curve, p) - shift), 3))
    return out


NOTE = ("QBINS equal-probability holds (s) before an ability's first cast in a fight (None: not cast in that fight), "
        "only for abilities the sim casts on sight (Mechanics.cast_timing). Damage abilities: the real due time (when "
        "the first cast's damage lands, Kaplan-Meier, fight end censors) less the sim's median cast and cast -> hit "
        "time; a negative value is a precast, cast that long before t = 0 (mechanics.precast). Others: the real first "
        "cast less the sim's median cast time.")


def fit(n, workers, write, hero=None):
    from deadsim import game
    G = game()
    hid = G.hero(hero).id if hero else None
    real_rows = json.load(open(REAL))["rows"]
    if hid is not None:
        real_rows = {k: v for k, v in real_rows.items() if k.startswith(f"{hid}:")}
    sim0 = sim_curves(n, workers, False, hero=hid)
    # abilities whose gate a held first cast skips (an ultimate's setup wait, patterns.Plan; Slam Fire's last shell):
    # their timing with every first cast acting as held (abilities.PROBE_HELD), only for them (an early ult would
    # move the other abilities' timing)
    from deadsim.abilities import REGISTRY, load_heroes
    load_heroes()
    ults = {f"{hh.id}:{a.class_name}" for hh in G.heroes.values() for i, a in enumerate(hh.abilities)
            if i == 3 or getattr(REGISTRY.get(a.class_name), "held_opens", False)}
    # held openers that wait for a first gun hit (Djinn's Mark's first mark) come after the other openers' gun locks
    # with the holds off: their probe counts as on sight by PROBE_SIGHT_S
    late_ok = {f"{hh.id}:{a.class_name}" for hh in G.heroes.values() for a in hh.abilities
               if getattr(REGISTRY.get(a.class_name), "held_opens", False) == "first_hit"}
    sim0u = sim_curves(n, workers, False, probe=True, hero=hid)
    h = int(HORIZON / 0.5)

    def on_sight(sm, by=2):
        return sm and sm["duels"] >= MIN_DUELS and sm["cast_by"][h] >= 0.05 and \
            sm["cast_by"][by] >= CAST_ON_SIGHT * sm["cast_by"][h]
    out = {}
    for key, r in sorted(real_rows.items()):
        sm = sim0.get(key)
        if getattr(REGISTRY.get(key.split(":", 1)[1]), "draw_plan", None) is not None:
            continue   # its own real plan (Mechanics.execute_timing): Victor's aura is timed from its hits
        if on_sight(sm):
            pass
        elif key in ults and on_sight(sim0u.get(key), int(PROBE_SIGHT_S / 0.5) if key in late_ok else 2):
            sm = sim0u[key]
        else:
            continue   # the sim already waits for something (a health gate, stacks, range): its timing is its own
        out[key] = holds(r, sm)
    res = {"source": json.load(open(REAL))["source"] + "; sim: damage audit duels, holds off",
           "note": NOTE,
           "horizon_s": HORIZON, "sources": out}
    print(f"{len(out)} abilities held")
    if hid is not None:   # keep the other heroes' rows
        old = json.load(open(OUT))
        old["sources"] = {k: v for k, v in old["sources"].items() if not k.startswith(f"{hid}:")}
        old["sources"].update(out)
        old["sources"] = dict(sorted(old["sources"].items()))
        res = old
    if not write:
        for k, v in out.items():
            print(k, v)
        return
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    sim1 = sim_curves(n, workers, True, hero=hid)
    name = {}
    for hh in G.heroes.values():
        for i, ab in enumerate(hh.abilities):
            name[f"{hh.id}:{ab.class_name}"] = f"{hh.name}: {ab.name}" + (" (ult)" if i == 3 else "")
    lines = ["# Ability cast timing: sim vs real Phantom+ (scripts/cast_timing/fit_cast_timing.py)", "",
             "P(first cast by 1 / 3 / 6 / 20 s | fight still going). Real: " + res["source"] + ". Sim: damage audit "
             f"duels ({n} players x 3), before = holds off (cast on sight), after = Mechanics.cast_timing. "
             "Held: the ability gets a real hold; others keep the sim's own timing.", "",
             "| ability | real fights | real | sim before | sim after | held |", "|---|---|---|---|---|---|"]

    def f4(c):
        return f"{c[2]:.2f} / {c[6]:.2f} / {c[12]:.2f} / {c[40]:.2f}"
    gaps0, gaps1 = [], []
    for key, r in sorted(real_rows.items(), key=lambda x: name.get(x[0], x[0])):
        if key not in sim0 or key not in sim1 or sim0[key]["duels"] < MIN_DUELS:
            continue
        g0 = statistics.mean(abs(a - b) for a, b in zip(r["cast_by"][:41:2], sim0[key]["cast_by"][:41:2]))
        g1 = statistics.mean(abs(a - b) for a, b in zip(r["cast_by"][:41:2], sim1[key]["cast_by"][:41:2]))
        gaps0.append(g0)
        gaps1.append(g1)
        lines.append(f"| {name.get(key, key)} | {r['fights']} | {f4(r['cast_by'])} | {f4(sim0[key]['cast_by'])} | "
                     f"{f4(sim1[key]['cast_by'])} | {'yes' if key in out else ''} |")
    gap = (f"Mean |real - sim| of the curve (0-20 s): before {statistics.mean(gaps0):.3f}, after "
           f"{statistics.mean(gaps1):.3f} over {len(gaps0)} abilities.")
    if hid is not None:   # swap this hero's table rows into the report
        prefix = f"| {G.hero(hero).name}: "
        old = open(REPORT).read().rstrip("\n").split("\n")
        head = [x for x in old if not x.startswith("| ") or x.startswith(("| ability", "|---"))]
        rows = [x for x in old if x.startswith("| ") and not x.startswith(("| ability", "|---", prefix))]
        lines = head + sorted(rows + lines[6:])
        print(hero, gap)
    else:
        lines[3:3] = [gap, ""]
    with open(REPORT, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(lines[3])


if __name__ == "__main__":
    args = sys.argv[1:]

    def opt(k, d):
        if k in args:
            i = args.index(k)
            v = args[i + 1]
            del args[i:i + 2]
            return v
        return d
    if args[0] == "real":
        fd, cd, w = opt("--fights", FIGHTS), opt("--casts", CASTS), int(opt("--workers", 4))
        real(fd, cd, w)
    else:
        write = "--write" in args
        hero = opt("--hero", None)
        pos = [a for a in args[1:] if not a.startswith("--")]
        fit(int(pos[0]) if pos else 3000, int(pos[1]) if len(pos) > 1 else os.cpu_count(), write, hero)
