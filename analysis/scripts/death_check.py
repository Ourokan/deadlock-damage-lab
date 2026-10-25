"""Does the sim's death chance move with items like real deaths do? For the overall score's death cost
(damage/scripts/overall_search.py death_value, which takes a build's deaths as the hero's real rate x the build's sim
death chance / the popular build's).

Real: per (hero, item), deaths per 10 min of Phantom+ players holding the item at the end vs not, matched like
kill_participation.py (hero, final net worth // 2500, duration // 300 s), final net worth in [NW_LO, NW_HI), as a
ratio holders / others. Sim: the popular build + the item vs the popular build, ratio of overall_search.death_chance
(+ DEATH_EPS), from sim_vs_win.py --out rows. Prints the correlation over (hero, item) pairs with enough holders
and per item (mean over heroes), and the elasticity (least squares slope of log real ratio on log sim ratio). These
are associations at equal net worth, not a controlled effect: players who die a lot may buy defensive items.

usage: python3 analysis/scripts/death_check.py SIM_ROWS.json [--min-holders 150]
"""
import argparse
import collections
import glob
import gzip
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kill_participation as KP  # noqa: E402

NW_LO, NW_HI = 20000, 37000
EPS = 0.01


def real_rows():
    kda = KP.load_kda()
    teams = collections.defaultdict(list)
    for r in kda.values():
        teams[(r["match_id"], r["team"])].append(r)
    keys = {k for k, r in kda.items() if NW_LO <= r["net_worth"] < NW_HI and r["duration_s"] >= 600
            and len(teams[(r["match_id"], r["team"])]) == 6}
    out = []
    for p in sorted(glob.glob(f"{KP.BUILDS}/*.jsonl.gz")):
        with gzip.open(p, "rt") as f:
            for line in f:
                b = json.loads(line)
                k = (b["match_id"], b["account_id"])
                if k in keys:
                    r = kda[k]
                    out.append({"hero": r["hero_id"], "nw": r["net_worth"], "dur": r["duration_s"],
                                "d10": r["deaths"] / r["duration_s"] * 600, "items": set(b["final_items"])})
                    keys.discard(k)
    return out


def pearson(x, y, w=None):
    w = w or [1.0] * len(x)
    tw = sum(w)
    mx, my = sum(a * c for a, c in zip(x, w)) / tw, sum(b * c for b, c in zip(y, w)) / tw
    sxy = sum(c * (a - mx) * (b - my) for a, b, c in zip(x, y, w))
    sxx = sum(c * (a - mx) ** 2 for a, c in zip(x, w))
    syy = sum(c * (b - my) ** 2 for b, c in zip(y, w))
    return sxy / math.sqrt(sxx * syy), sxy / sxx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sim")
    ap.add_argument("--min-holders", type=int, default=150)
    a = ap.parse_args()
    sim = json.load(open(a.sim))
    names = {x["name"]: i for i, x in KP.ITEMS.items()}
    rows = real_rows()
    by_hero = collections.defaultdict(list)
    for r in rows:
        by_hero[r["hero"]].append(r)
    pairs = []
    for hero, b, name, gain, edge, se, pd_pop, pd, *_ in sim:
        i = names.get(name)
        rs = by_hero.get(hero)
        if i is None or not rs:
            continue
        m = KP.matched(rs, lambda r: i in r["items"], "d10")
        if m is None or m["n"] < a.min_holders or m["base"] <= 0:
            continue
        real = (m["base"] + m["diff"]) / m["base"]
        pairs.append((hero, name, math.log((pd + EPS) / (pd_pop + EPS)), math.log(real), m["n"], m["diff"] / m["se"]))
    x, y, w = [p[2] for p in pairs], [p[3] for p in pairs], [p[4] for p in pairs]
    r, slope = pearson(x, y, w)
    print(f"{len(rows)} real players at {NW_LO // 1000}-{NW_HI // 1000}k; {len(pairs)} (hero, item) pairs with >= "
          f"{a.min_holders} holders: holder-weighted Pearson log sim vs log real death ratio {r:+.3f}, slope {slope:+.3f}")
    by = collections.defaultdict(list)
    for p in pairs:
        by[p[1]].append(p)
    items = [(n, sum(p[2] * p[4] for p in ps) / sum(p[4] for p in ps), sum(p[3] * p[4] for p in ps) / sum(p[4] for p in ps),
              sum(p[4] for p in ps)) for n, ps in by.items() if len(ps) >= 3]
    r2, s2 = pearson([i[1] for i in items], [i[2] for i in items], [i[3] for i in items])
    print(f"per item (>= 3 heroes, {len(items)} items): Pearson {r2:+.3f}, slope {s2:+.3f}")
    print("items the sim says cut deaths most | real deaths ratio (holders / others):")
    for n, s, e, k in sorted(items, key=lambda i: i[1])[:15]:
        print(f"  {n:24s} sim {math.exp(s):.2f}  real {math.exp(e):.2f}  ({k} holders)")
    print("items real holders die least with | sim:")
    for n, s, e, k in sorted(items, key=lambda i: i[2])[:12]:
        print(f"  {n:24s} real {math.exp(e):.2f}  sim {math.exp(s):.2f}  ({k} holders)")


if __name__ == "__main__":
    main()
