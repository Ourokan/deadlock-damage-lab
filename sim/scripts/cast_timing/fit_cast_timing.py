"""When real Phantom+ players cast each hero ability in a fight, against when the sim does, and the hold that makes the
sim's first casts follow the real ones (Mechanics.cast_timing).

The sim's duels start with every cooldown ready and cast each ability the moment its rule allows: the ultimate goes
out at t=0 in ~90% of duels (real: 10-40% of fights by 20 s), and its cast lock / channel then keeps the gun quiet
for the first seconds, so the gun and the item procs riding on it land seconds later than in real fights
(validation/opener_timing.md: 66 sources clearly later in the sim). The opener-timing hold (Mechanics.opener_timing)
only moved the booking; this moves the casts.

real: the fight-length replays (fight_length/fetch_fights.py: two enemy heroes trading, gaps < 5 s, >= 4 hits both
ways, the unit the sim's fight-length booking is fitted on) and their ability casts (fetch_ability_casts.py: cooldown
starts per owner pawn). For each fighter of a fight and each ability it has (cast before in the match, or in the
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
fit writes data/cast_timing.json and validation/cast_timing.md. Static snapshot: refit after a patch that changes
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
QBINS = 20
# a fighter's overlapping pair fights merged into one engagement (as fit_item_use.py)? No: the sim's duel timeline is
# the pair fight's (its length booking, data/fight_length.json, is fitted on pair fights), and merged engagements put
# a later-joining enemy's whole fight after t0 (the curve came out ~1 s later than the hits, opener_timing.md)
MERGE = False


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


def real_rows(args):
    """[(hero id, ability class, first cast s or None, fight length s)] for one match."""
    fn, cast_fn, m, abil = args
    hero, ev = FL.read(fn)
    by_hero = {p["hero_id"]: p for p in m["players"]}
    casts = collections.defaultdict(list)
    for line in gzip.open(cast_fn, "rt"):
        r = json.loads(line)
        casts[(r["a"], int(r["s"]))].append(r["tick"] / T)
    for v in casts.values():
        v.sort()
    pairs = collections.defaultdict(list)
    for e in ev:
        _, a, v = e[:3]
        pa, pv = by_hero.get(hero.get(a)), by_hero.get(hero.get(v))
        if pa is None or pv is None or pa["team"] == pv["team"]:
            continue
        pairs[min(a, v), max(a, v)].append(e)
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
                out.append((hid, cls, None if first is None else max(0.0, first - t0), t1 - t0))
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
    rows = collections.defaultdict(list)
    with Pool(workers) as p:
        for rs in p.imap_unordered(real_rows, jobs):
            for hid, cls, u, d in rs:
                rows[f"{hid}:{cls}"].append((u, d))
    res = {"source": f"{len(jobs)} Phantom+ replays, pair fights (scripts/cast_timing/fit_cast_timing.py real)",
           "grid_s": GRID, "rows": {}}
    for key, rs in sorted(rows.items()):
        if len(rs) < MIN_FIGHTS:
            continue
        res["rows"][key] = {"fights": len(rs), "cast_share": round(sum(u is not None for u, _ in rs) / len(rs), 3),
                            "cast_by": km(rs)}
    with open(REAL, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(len(res["rows"]), "rows from", len(jobs), "matches")


# ---- sim side ------------------------------------------------------------------------------------------------
def sim_job(args):
    j, timing = args
    import damage_audit as A
    from deadsim import engine
    import dataclasses
    A.PROFILE = True
    engine.PROFILE_SOURCES = True
    A.MECH = dataclasses.replace(A.MECH, cast_timing=timing)
    hid, d, _ = A.sim_player(j)
    return hid, {k: v for k, v in d.items() if k.startswith(("_cu:", "_cn:", "_fu:", "_fc:"))}


def sim_curves(n, workers, timing):
    """{"hero id:ability class": {"duels", "cast_by", "hit_by" on GRID (first cast / first hit)}} from the audit's
    duels."""
    from deadsim import game
    import landing_rates as L
    G = game()
    jobs = []
    for line in gzip.open(SAMPLE):
        m = json.loads(line)
        jobs += [(m, p["slot"]) for p in m["players"] if p["hero_id"] in G.heroes and L.gun_known(p)]
    random.Random(1).shuffle(jobs)
    tot = collections.defaultdict(collections.Counter)
    with ProcessPoolExecutor(workers) as ex:
        for hid, d in ex.map(sim_job, [(j, timing) for j in jobs[:n]], chunksize=8):
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


def holds(real_cast, sim_cast):
    """QBINS hold values: equal-probability points of the real first cast curve (None past its share cast by
    HORIZON: not cast in that fight), less the sim's own median first cast."""
    h = int(HORIZON / 0.5)
    s_top = sim_cast[h] or 1.0
    s_med = quantile([v / s_top for v in sim_cast], 0.5) or 0.0
    out = []
    for b in range(QBINS):
        p = (b + 0.5) / QBINS
        if p > real_cast[h]:
            out.append(None)
            continue
        out.append(round(max(0.0, quantile(real_cast, p) - s_med), 3))
    return out


def fit(n, workers, write):
    from deadsim import game
    G = game()
    real_rows = json.load(open(REAL))["rows"]
    sim0 = sim_curves(n, workers, False)
    out = {}
    for key, r in sorted(real_rows.items()):
        sm = sim0.get(key)
        if not sm or sm["duels"] < MIN_DUELS:
            continue
        h = int(HORIZON / 0.5)
        if sm["cast_by"][h] < 0.05:
            continue
        if sm["cast_by"][2] < CAST_ON_SIGHT * sm["cast_by"][h]:
            continue   # the sim already waits for something (a health gate, stacks, range): its timing is its own
        out[key] = holds(r["cast_by"], sm["cast_by"])
    res = {"source": json.load(open(REAL))["source"] + "; sim: damage audit duels, holds off",
           "note": "QBINS equal-probability holds (s) before an ability's first cast in a fight (None: not cast in "
                   "that fight): the real first cast (Kaplan-Meier, fight end censors) less the sim's own median "
                   "cast time; only abilities the sim casts on sight (Mechanics.cast_timing)",
           "horizon_s": HORIZON, "sources": out}
    print(f"{len(out)} abilities held")
    if not write:
        return
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    sim1 = sim_curves(n, workers, True)
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
    lines[3:3] = [f"Mean |real - sim| of the curve (0-20 s): before {statistics.mean(gaps0):.3f}, after "
                  f"{statistics.mean(gaps1):.3f} over {len(gaps0)} abilities.", ""]
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
        pos = [a for a in args[1:] if not a.startswith("--")]
        fit(int(pos[0]) if pos else 3000, int(pos[1]) if len(pos) > 1 else os.cpu_count(), write)
