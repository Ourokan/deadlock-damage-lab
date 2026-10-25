"""When real Phantom+ players use their damage abilities and items inside a fight, against when the sim does.

The sim's duels start with every cooldown ready and each opener goes out as soon as its cast rule allows. Real
fights often follow another one (the cooldown is still running) and players hold some casts. This measures, per
hero and damage source (ability or item, by the game's ability id), in the fights of fit_length.py (two enemy
heroes trading, gaps < 5 s, >= 4 hits both ways):

- held: fights where the attacker has the source (an item bought before the fight and not sold, from the sample's
  item times and the replay clock offset; an ability once the attacker has hit with it earlier in the match),
- ready: no hit of the source by the attacker on any hero in the cooldown before the fight started (base cooldown
  from the game data; a DoT's late ticks make this a little strict),
- first use: the first hit of the source on the fight's enemy, seconds after the fight's first hit. The fight's end
  censors it, so the curve is a Kaplan-Meier P(used by t | fight still going), as the sim books damage x P(fight
  still going).

The sim side runs the damage audit's duels (real builds both sides, the searches' skills) and takes the same
Kaplan-Meier curve of each held source's first hit (a duel ends at a death or 20 s).

usage: python3 -I opener_timing.py real <raw dir> <out.json> [--sample PATH]
       python3 -I opener_timing.py compare <real.json> [max_players=3000] [workers] [--sim CACHE] [--out PATH] [--no-hold]
       python3 -I opener_timing.py fit <real.json> [max_players=3000] [workers] [--sim CACHE] [--write]
The real output is kept as validation/opener_timing_real.json.gz (real.json may be gzipped). fit writes
data/opener_timing.json from the sim run with the holds off.
Raw dir: fetch_fights.py output (project folder analysis/work/fight_length/raw).
"""
import collections
import glob
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import fit_length as FL  # noqa: E402

GRID = [0.5 * k for k in range(41)]   # 0..20 s
MIN_FIGHTS = 60                       # held fights for a source row


def read(fn):
    hero, ev = {}, []
    for line in gzip.open(fn, "rt"):
        r = json.loads(line)
        if r["k"] == "ctl":
            hero[r["a"]] = int(r["s"])
        elif r["k"] == "dmg" and r.get("s"):
            ab, hp, hmax = r["s"].split("|")
            ev.append((r["tick"] / FL.T, r["a"] // 100000, r["a"] % 100000, float(hp), float(hmax), r["v"], int(ab)))
    ev.sort()
    return hero, ev


def sources(G):
    """ability id -> (kind, name, class, base cooldown s) for hero abilities and active / proc items."""
    out = {}
    for h in G.heroes.values():
        for ab in h.abilities:
            cd = ab.props.get("AbilityCooldown") or 0.0
            out[ab.id] = ("ability", f"{h.name}: {ab.name}", ab.class_name, float(cd))
    for it in G.items.values():
        cd = it.props.get("AbilityCooldown") or 0.0
        out[it.id] = ("item", it.name, it.class_name, float(cd))
    return out


def load(path):
    return json.load(gzip.open(path, "rt") if path.endswith(".gz") else open(path))


def km_used(rows):
    """rows (first use s or None, fight length s): P(used by t | the fight still going at t), on GRID (Kaplan-Meier
    of the first use, the fight's end censors)."""
    ev = sorted((u if u is not None else d, u is not None) for u, d in rows)
    n, i, surv, out = len(ev), 0, 1.0, []
    for t in GRID:
        while i < n and ev[i][0] <= t:
            j, uses = i, 0
            while j < n and ev[j][0] == ev[i][0]:
                uses += ev[j][1]
                j += 1
            surv *= 1.0 - uses / (n - i)
            i = j
        out.append(round(1.0 - surv, 4))
    return out


def real(raw, out_path, sample_path):
    from deadsim import game
    G = game()
    src = sources(G)
    weap = {w["id"] for w in json.load(open(os.path.join(ROOT, "..", "data", "game", "weapons.json")))}
    files = sorted(glob.glob(os.path.join(raw, "*.ndjson.gz")))
    sample = FL.load_sample(sample_path, {os.path.basename(f).split(".")[0] for f in files})
    rows = collections.defaultdict(list)    # (hero id, source id) -> [(ready, first use or None, length, window gun share)]
    prof = collections.defaultdict(collections.Counter)   # (hero id, source id or "GUN") -> 2 s slice -> damage
    for fn in files:
        mid = os.path.basename(fn).split(".")[0]
        m = sample.get(mid)
        if m is None:
            continue
        hero, ev = read(fn)
        off = FL.clock_offset([e[:6] for e in ev], hero, m)
        by_hero = {p["hero_id"]: p for p in m["players"]}
        uses = collections.defaultdict(list)   # (attacker, source) -> hit times on any enemy hero
        pairs = collections.defaultdict(list)
        for e in ev:
            t, a, v = e[:3]
            pa, pv = by_hero.get(hero.get(a)), by_hero.get(hero.get(v))
            if pa is None or pv is None or pa["team"] == pv["team"]:
                continue
            if e[6] in src:
                uses[a, e[6]].append(t)
            pairs[min(a, v), max(a, v)].append(e)
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
                t0, t1 = f[0][0], f[-1][0]
                for e in f:
                    if e[6] in src or e[6] in weap:
                        prof[hero[e[1]], e[6] if e[6] in src else "GUN"][int((e[0] - t0) // 2)] += e[5]
                for a in (x, y):
                    p = by_hero[hero[a]]
                    g = None if off is None else t0 - off(t0)
                    owned = set()
                    if g is not None:
                        owned = {i[0] for i in p["items"] if i[1] <= g and (not i[2] or i[2] > g)}
                    first = {}
                    for e in f:
                        if e[1] == a and e[6] in src and e[6] not in first:
                            first[e[6]] = e[0] - t0
                    cand = {s for s in owned if s in src and src[s][3] > 0}
                    cand |= {s for (aa, s), ts in uses.items() if aa == a and src[s][0] == "ability" and ts[0] < t0}
                    cand |= {s for s in first if src[s][0] == "ability"}
                    for s in cand:
                        if src[s][0] == "item" and s not in owned:
                            continue
                        ts = uses.get((a, s), [])
                        cd = src[s][3]
                        ready = not any(t0 - cd <= t < t0 for t in ts)
                        win = None
                        if s in first:
                            w0 = t0 + first[s]
                            gun = [e for e in f if e[1] == a and e[6] in weap]
                            gtot = sum(e[5] for e in gun if e[0] >= w0)
                            if gtot > 0:
                                win = sum(e[5] for e in gun if w0 <= e[0] < w0 + 5) / gtot
                        rows[hero[a], s].append((ready, first.get(s), t1 - t0, win))
    res = {"source": f"{len(files)} Phantom+ replays (scripts/fight_length/opener_timing.py real)",
           "grid_s": GRID, "rows": {}}
    for (h, s), rs in sorted(rows.items()):
        if len(rs) < MIN_FIGHTS:
            continue
        kind, name, cls, cd = src[s]
        ready = [r for r in rs if r[0]]
        used = [r[1] for r in rs if r[1] is not None]
        used_r = sorted(r[1] for r in ready if r[1] is not None)
        row = {"hero": h, "kind": kind, "name": name, "class": cls, "cooldown": cd, "fights": len(rs),
               "ready_share": round(len(ready) / len(rs), 3),
               "used_share": round(len(used) / len(rs), 3),
               "used_if_ready": round(len(used_r) / max(1, len(ready)), 3),
               "first_use_median_if_ready": used_r[len(used_r) // 2] if used_r else None,
               "used_by": km_used([(r[1], r[2]) for r in rs]),
               "used_by_if_ready": km_used([(r[1], r[2]) for r in ready])}
        wins = [r[3] for r in rs if r[3] is not None]
        if wins:
            row["gun_share_5s_after_first_use"] = round(sum(wins) / len(wins), 3)
        pr = prof.get((h, s), {})
        tot = sum(pr.values())
        if tot:
            row["damage_by_2s"] = [round(pr.get(k, 0) / tot, 4) for k in range(10)]
        res["rows"][f"{h}:{cls}"] = row
    for (h, s), pr in prof.items():
        if s == "GUN" and sum(pr.values()):
            res["rows"][f"{h}:GUN"] = {"hero": h, "kind": "gun", "name": "gun", "class": "GUN",
                                       "damage_by_2s": [round(pr.get(k, 0) / sum(pr.values()), 4) for k in range(10)]}
    with open(out_path, "w") as fh:
        json.dump(res, fh, indent=1)
    print(len(res["rows"]), "rows")


HORIZON = 20.0       # s: the opener's first-use curve is normalised to its use by then (the level stays the factors')
CAST_ON_SIGHT = 0.7  # a sim source whose first hits are this much in the first second gets the real timing
QBINS = 20           # equal-probability bins of the hold


def hold_quantiles(used_by, sim_used_by):
    """The hold (s) before a source's first use that makes the sim's first use follow the real one: QBINS quantiles
    of the real first use given a use by HORIZON, less the sim's own median first hit (its cast and travel time)."""
    h = int(HORIZON / 0.5)
    top = used_by[h]
    sim_top = sim_used_by[h] or 1.0
    s_med = next((GRID[k] for k in range(h + 1) if sim_used_by[k] >= 0.5 * sim_top), 0.0)
    out = []
    for b in range(QBINS):
        p = (b + 0.5) / QBINS * top
        k = next((k for k in range(h + 1) if used_by[k] >= p), h)
        # linear inside the 0.5 s step
        lo = used_by[k - 1] if k else 0.0
        t = GRID[k] - 0.5 * (used_by[k] - p) / max(1e-9, used_by[k] - lo) if k else 0.0
        out.append(round(max(0.0, t - s_med), 3))
    return out


def fit(real_path, sim, write=False):
    """data/opener_timing.json: per hero source that the sim casts on sight, the real hold before its first use
    (hold_quantiles); items also pooled over heroes (by real fights) for heroes without a row."""
    real_rows = load(real_path)["rows"]
    out, pooled = {}, collections.defaultdict(list)
    for key, r in sorted(real_rows.items()):
        sm = sim.get(key)
        if r.get("kind") not in ("ability", "item") or not sm or sm["duels"] < 30:
            continue
        h = int(HORIZON / 0.5)
        if r["used_by"][h] < 0.05 or sm["used_by"][h] < 0.05:
            continue
        if sm["used_by"][2] < CAST_ON_SIGHT * sm["used_by"][h]:
            continue   # the sim already waits for something (a health gate, a proc): its timing is its own
        q = hold_quantiles(r["used_by"], sm["used_by"])
        out[key] = q
        if r["kind"] == "item":
            pooled[r["class"]].append((r["fights"], q))
    items = {}
    for cls, rs in pooled.items():
        n = sum(w for w, _ in rs)
        items[cls] = [round(sum(w * q[b] for w, q in rs) / n, 3) for b in range(QBINS)]
    res = {"source": load(real_path)["source"] + "; sim: damage audit duels",
           "note": "hold (s) before a source's first use in a fight, QBINS equal-probability values: the real first "
                   "use (Kaplan-Meier, fight end censors) given a use by HORIZON s, less the sim's own median first "
                   "hit; only sources the sim casts on sight. Engine books their hits x mean over the values of "
                   "P(fight going at t + hold) (Mechanics.opener_timing, with fight_length)",
           "horizon_s": HORIZON, "sources": out, "items_pooled": items}
    import statistics
    print(f"{len(out)} hero sources, {len(items)} pooled items; median hold "
          f"{statistics.median(statistics.median(q) for q in out.values()):.2f} s")
    if write:
        with open(os.path.join(ROOT, "data", "opener_timing.json"), "w") as fh:
            json.dump(res, fh, indent=1)
            fh.write("\n")
    return res


def sim_job(j):
    import damage_audit as A
    from deadsim import engine
    A.PROFILE = True
    engine.PROFILE_SOURCES = True
    hid, d, _ = A.sim_player(j)
    return hid, {k: v for k, v in d.items() if k.startswith(("_fu:", "_fc:", "_s2:"))}


def sim_curves(n, workers, sample=None):
    """{"hero id:source class": {"duels", "used_by" on GRID, "full_by_2s"}} from the audit's duels."""
    import random
    from concurrent.futures import ProcessPoolExecutor
    from deadsim import game
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import landing_rates as L
    G = game()
    jobs = []
    for line in gzip.open(sample or os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")):
        m = json.loads(line)
        jobs += [(m, p["slot"]) for p in m["players"] if p["hero_id"] in G.heroes and L.gun_known(p)]
    random.Random(1).shuffle(jobs)
    tot = collections.defaultdict(collections.Counter)
    with ProcessPoolExecutor(workers) as ex:
        for hid, d in ex.map(sim_job, jobs[:n], chunksize=8):
            for k, v in d.items():
                kind, key, b = k.split(":")
                tot[f"{hid}:{key}"][kind, int(b)] += v
    out = {}
    for key, c in tot.items():
        n_all = sum(v for (k, _), v in c.items() if k != "_s2")
        risk, surv, curve = n_all, 1.0, []
        for b in range(len(GRID)):
            u = c.get(("_fu", b), 0)
            if risk:
                surv *= 1.0 - u / risk
            risk -= u + c.get(("_fc", b), 0)
            curve.append(round(1.0 - surv, 4))
        out[key] = {"duels": n_all, "used_by": curve, "full_by_2s": [c.get(("_s2", b), 0.0) for b in range(10)]}
    return out


def expected_share(full, hold=None):
    """Damage by 2 s slice in full -> share expected over real fight lengths: each slice's damage x P(fight going)
    at its middle; with opener hold values, moved h s later and x P(going) there (what the engine books)."""
    from deadsim.mechanics import LENGTH_STEP, real_length
    S = real_length()
    e = [0.0] * len(full)
    for h in hold or (0.0,):
        for k, v in enumerate(full):
            t = 2 * k + 1 + h
            j = int(t // 2)
            if j < len(e):
                e[j] += v * S[min(len(S) - 1, int(t / LENGTH_STEP))]
    tot = sum(e) or 1.0
    return [v / tot for v in e]


def mean_t(share):
    return sum((2 * k + 1) * v for k, v in enumerate(share))


def compare(real_path, n, workers, out_path=None, sim=None, hold_on=True):
    """Per hero source: share of its fight damage in the first 2 s and its mean time into the fight, real vs sim
    (expected over real fight lengths), plus P(first hit by 1 / 3 / 6 s | fight going). Sorted by how much earlier
    the sim puts the damage (real mean time - sim mean time)."""
    from deadsim import game
    G = game()
    real_rows = load(real_path)["rows"]
    sim = sim or sim_curves(n, workers)
    holds = {}
    if hold_on:
        ot = json.load(open(os.path.join(ROOT, "data", "opener_timing.json")))
        holds = dict(ot["sources"])
        for key in real_rows:
            cls = key.split(":", 1)[1]
            if key not in holds and cls in ot["items_pooled"]:
                holds[key] = ot["items_pooled"][cls]
    rows = []
    for key, r in real_rows.items():
        if key not in sim or "damage_by_2s" not in r or sum(sim[key]["full_by_2s"]) <= 0:
            continue
        if r.get("kind") != "gun" and (r["used_share"] < 0.03 or sim[key]["duels"] < 30):
            continue
        es = expected_share(sim[key]["full_by_2s"], holds.get(key))
        rows.append((mean_t(r["damage_by_2s"]) - mean_t(es), key, r, sim[key], es))
    rows.sort(key=lambda x: -x[0])
    name = {h.id: h.name for h in G.heroes.values()}
    lines = ["| hero | source | real fights | ready at start | first 2 s real / sim | mean time real / sim (s) |"
             " used by 1 / 3 / 6 s real | sim |", "|---|---|---|---|---|---|---|---|"]
    for d, key, r, sm, es in rows:
        ub = r.get("used_by")
        lines.append(f"| {name.get(r['hero'], r['hero'])} | {r['name'].split(': ')[-1]} | {r.get('fights', '')} | "
                     f"{r.get('ready_share', '')} | {r['damage_by_2s'][0]:.2f} / {es[0]:.2f} | "
                     f"{mean_t(r['damage_by_2s']):.1f} / {mean_t(es):.1f} | "
                     + (f"{ub[2]:.2f} / {ub[6]:.2f} / {ub[12]:.2f} | " if ub else "| ")
                     + (f"{sm['used_by'][2]:.2f} / {sm['used_by'][6]:.2f} / {sm['used_by'][12]:.2f} |"
                        if ub else " |"))
    print("\n".join(lines))
    if out_path:
        with open(out_path, "w") as fh:
            json.dump({k: {"real_by_2s": r["damage_by_2s"], "sim_by_2s": [round(v, 4) for v in es],
                           "shift_s": round(d, 3), "sim_duels": sm["duels"]}
                       for d, k, r, sm, es in rows}, fh, indent=1)
    return rows


if __name__ == "__main__":
    args = sys.argv[1:]
    sp = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
    if "--sample" in args:
        sp = args[args.index("--sample") + 1]
    if args[0] == "real":
        real(args[1], args[2], sp)
    else:
        out = args[args.index("--out") + 1] if "--out" in args else None
        cache = args[args.index("--sim") + 1] if "--sim" in args else None
        pos = [a for a in args[2:] if not a.startswith("--") and a not in (out, cache)]
        n, w = int(pos[0]) if pos else 3000, int(pos[1]) if len(pos) > 1 else os.cpu_count()
        sim = None
        if cache and os.path.exists(cache):
            sim = json.load(open(cache))
        else:
            sim = sim_curves(n, w)
            if cache:
                json.dump(sim, open(cache, "w"))
        if args[0] == "compare":
            rows = compare(args[1], n, w, out, sim, "--no-hold" not in args)
            import statistics
            sh = [abs(d) for d, *_ in rows]
            print(f"mean time real - sim: median |shift| {statistics.median(sh):.2f} s over {len(sh)} sources")
        else:
            fit(args[1], sim, "--write" in args)
