"""How much cooldown reduction items raise an ability's readiness at the start of real Phantom+ fights.

The sim opens each fight with every ability ready and holds its first cast to the real cast timing (data/
cast_timing.json), which already has real players' share of fights started with an ability still on cooldown from
the fight before. That share came from real cooldowns, so a build with cooldown items (Compress / Superior /
Transcendent Cooldown, ult cooldown items) got no more fights started ready than one without: cooldown items were
worth only the recasts inside a fight.

real: the fight-length replays' pair fights and ability casts (as recast_timing.py real). For each fighter, each
single-charge ability (ults included) at each fight start: tau = time since its last cast, cd = the player's
cooldown for it then (the sim's AbilityState.cooldown() of the real build at that minute) and cd0 = the same
without the build's item cooldown reduction. Ready at the start = tau >= cd.
fit: per ability (>= MIN_FIGHTS fights; else pooled ult / non-ult) the share of fights with tau >= k x cd on K_GRID
for players without cooldown items, and the use ratio rho: the share of the gain that real holders of cooldown items
get (holders' ready share vs matched non-holders', against non-holders' tau at the holders' cooldown ratio). Holders
cast more often between fights too, so their tau is shorter and only part of the cooldown cut shows at the fight
start. -> data/cdr_ready.json (Mechanics.cdr_ready, mechanics.hold_first_casts).

usage: python3 -I cdr_ready.py real [workers]   -> /mnt/project-files/analysis/work/cdr_ready/rows.pkl (20 MB)
       python3 -I cdr_ready.py fit [--half 0|1]  -> data/cdr_ready.json (prints rho per half of the heroes)
"""
import bisect
import collections
import gzip
import json
import os
import pickle
import statistics
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "fight_length"))
sys.path.insert(0, HERE)
import fit_cast_timing as CT  # noqa: E402
import fit_length as FL  # noqa: E402
import opener_timing as OT  # noqa: E402
import recast_timing as RT  # noqa: E402

ROWS = "/mnt/project-files/analysis/work/cdr_ready/rows.pkl"
OUT = os.path.join(ROOT, "data", "cdr_ready.json")
K_GRID = [round(0.3 + 0.05 * k, 2) for k in range(15)]   # cooldown ratio 0.3 .. 1.0
MIN_FIGHTS = 300
MIN_COOLDOWN_CUT = 0.05   # s: a holder's items cut this ability's cooldown at least this much


def cooldowns(p, t, cache):
    """({ability class: (cooldown s, ult)}, {class: cooldown without item cdr}, holds cooldown items) of player p's real
    build at game time t (per minute); charged abilities left out."""
    b = int(t // 60)
    key = (p["slot"], b)
    if key not in cache:
        import landing_rates as L
        from deadsim import Loadout, game
        from deadsim.engine import Engine
        from deadsim.fight import make_fighter
        from deadsim.mechanics import item_cd_keep
        G = game()
        items, souls = L.build_at(p, max(0.0, b * 60))
        f = make_fighter(Engine(mech=None), Loadout(G.hero(p["hero_id"]).name, items, souls=souls))
        cds, cd0 = {}, {}
        for ab in f.abilities:
            if ab.max_charges() > 1 or not ab.unlocked:
                continue
            c = ab.cooldown()
            cds[ab.ab.class_name] = (c, bool(ab.ab.ultimate))
            cd0[ab.ab.class_name] = c / item_cd_keep(f, ab)
        cache[key] = (cds, cd0)
    return cache[key]


def real_rows(args):
    """[(hero id, class, ult, cd, cd without item cdr, game time s, tau s, first cast after the start s or None)]."""
    fn, cast_fn, m, abil = args
    hero, ev = OT.read(fn)
    by_hero = {p["hero_id"]: p for p in m["players"]}
    rows = CT.real_casts([json.loads(line) for line in gzip.open(cast_fn, "rt")])
    off = statistics.median([r["tick"] / CT.T - r["v"] for r in rows]) if rows else 0.0
    casts = collections.defaultdict(list)
    for r in rows:
        casts[(r["a"], int(r["s"]))].append(r["tick"] / CT.T)
    for v in casts.values():
        v.sort()
    out, cache = [], {}
    for pawn, sp in RT.pair_spans(hero, ev, by_hero).items():
        hid = hero.get(pawn)
        if hid not in abil or hid not in by_hero:
            continue
        p = by_hero[hid]
        for t0, t1 in sorted(sp):
            cds, cd0 = cooldowns(p, t0 - off, cache)
            for aid, cls in abil[hid].items():
                if cls not in cds:
                    continue
                cd, ult = cds[cls]
                cs = casts.get((pawn, aid), [])
                k = bisect.bisect_left(cs, t0 - CT.PRE_S)
                tau = t0 - CT.PRE_S - cs[k - 1] if k else 1e9
                first = cs[k] - t0 if k < len(cs) and cs[k] <= t1 else None
                out.append((hid, cls, ult, cd, cd0[cls], t0 - off, tau, first))
    return out


def real(workers):
    from deadsim import game
    G = game()
    abil = {h.id: {ab.id: ab.class_name for ab in h.abilities} for h in G.heroes.values()}
    mids = {f.split(".")[0] for f in os.listdir(CT.CASTS) if f.endswith(".ndjson.gz")}
    mids &= {f.split(".")[0] for f in os.listdir(CT.FIGHTS) if f.endswith(".ndjson.gz")}
    sample = FL.load_sample(CT.SAMPLE, mids)
    jobs = [(os.path.join(CT.FIGHTS, f"{mid}.ndjson.gz"), os.path.join(CT.CASTS, f"{mid}.ndjson.gz"), sample[mid], abil)
            for mid in sorted(mids) if mid in sample]
    rows = []
    with Pool(workers) as p:
        for rs in p.imap_unordered(real_rows, jobs):
            rows += rs
    with open(ROWS, "wb") as fh:
        pickle.dump(rows, fh)
    print(len(rows), "fight starts x abilities from", len(jobs), "matches")


def holder(r):
    return r[4] - r[3] > MIN_COOLDOWN_CUT


def use_ratio(rows):
    """rho: holders' ready gain over matched non-holders (same hero, ability, 10-min bin) / the gain non-holders'
    tau gives at the holders' mean cooldown ratio; with the parts."""
    key = lambda r: (r[0], r[1], int(r[5] // 600))   # noqa: E731
    hold = [r for r in rows if holder(r)]
    non = [r for r in rows if not holder(r)]
    hs, ns = collections.Counter(map(key, hold)), collections.Counter(map(key, non))
    hold = [r for r in hold if ns[key(r)]]
    non = [r for r in non if hs[key(r)]]
    if not hold:
        return None
    w = {k: hs[k] / ns[k] for k in ns}
    W = sum(w[key(r)] for r in non)
    k = statistics.mean(r[3] / r[4] for r in hold)
    got = sum(r[6] >= r[3] for r in hold) / len(hold)
    base = sum(w[key(r)] * (r[6] >= r[3]) for r in non) / W
    pred = sum(w[key(r)] * (r[6] >= r[3] * k) for r in non) / W
    return {"rho": round((got - base) / (pred - base), 3), "holders": len(hold), "k": round(k, 3),
            "ready_holders": round(got, 3), "ready_matched": round(base, 3), "ready_predicted": round(pred, 3)}


def curve(rows):
    return [round(sum(r[6] >= k * r[3] for r in rows) / len(rows), 4) for k in K_GRID]


def fit(half=None):
    with open(ROWS, "rb") as fh:
        rows = [r for r in pickle.load(fh) if r[5] > 0]
    if half is not None:
        rows = [r for r in rows if r[0] % 2 == half]
    res = {"source": "Phantom+ fight-length replays, pair fight starts (scripts/cast_timing/cdr_ready.py)",
           "k_grid": K_GRID, "rho": {}, "pooled": {}, "sources": {}}
    for ult in (False, True):
        part = [r for r in rows if r[2] == ult]
        tag = "ult" if ult else "ability"
        res["rho"][tag] = use_ratio(part)
        res["pooled"][tag] = curve([r for r in part if not holder(r)])
        print(tag, res["rho"][tag])
    by = collections.defaultdict(list)
    for r in rows:
        if not holder(r):
            by[f"{r[0]}:{r[1]}"].append(r)
    for key, rs in sorted(by.items()):
        if len(rs) >= MIN_FIGHTS:
            res["sources"][key] = curve(rs)
    if half is None:
        with open(OUT, "w") as fh:
            json.dump(res, fh, indent=1)
            fh.write("\n")
        print(len(res["sources"]), "abilities with own curves ->", OUT)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "real":
        real(int(a[1]) if len(a) > 1 else 4)
    elif a and a[0] == "fit":
        fit(int(a[a.index("--half") + 1]) if "--half" in a else None)
    else:
        print(__doc__)
