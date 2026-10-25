"""Collect counters/work/jobs (sim_counters.py) into counters/out/sim.json (for the site) and counters/out/sim.md.

sim.json, per net worth:
- items: per counter item, mean overall gain over buyer heroes (weighted by how often each hero reaches that net
  worth), gain per 1,000 souls, and how many buyer heroes already hold it in their popular build;
- enemy: per enemy hero, per item, the weighted mean matchup change over buyer heroes ("vs this enemy"), and the
  lift over the item's mean matchup change over all enemies (how much more it helps against this one);
- hero: per buyer hero, per item, its overall gain and per-enemy matchup changes (enemy ids in `enemies` order).

usage: python3 counters/scripts/export_sim.py
"""
from __future__ import annotations

import datetime
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sim"))

from sim_counters import BUDGETS, JOBS, OPTIONS  # noqa: E402
from deadsim.data import game  # noqa: E402

OUT = os.path.join(ROOT, "counters", "out")


def wmean(pairs):
    tw = sum(w for _, w in pairs)
    return sum(v * w for v, w in pairs) / tw if tw else None


def r4(x):
    return None if x is None else round(x, 4)


def main():
    g = game()
    jobs = {}
    for fn in glob.glob(os.path.join(JOBS, "*.json")):
        with open(fn) as f:
            d = json.load(f)
        jobs.setdefault(d["budget"], {})[d["hero"]] = d
    if not jobs:
        sys.exit("no counter jobs in " + JOBS)
    bracket = next(iter(next(iter(jobs.values())).values()))["bracket"]
    res = {"bracket": bracket, "built": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "items": [{"name": n, "id": g.item(n).id, "cost": g.item(n).cost} for n in OPTIONS],
           "heroes": {str(h): g.heroes[h].name for h in sorted(g.heroes)}, "budgets": {}}
    for b in sorted(jobs):
        rows = jobs[b]
        weights = next(iter(rows.values()))["weights"]
        enemies = sorted({e for d in rows.values() for v in d["items"].values() if v for e in v["vs"]}, key=int)
        items, enemy, hero = {}, {e: {} for e in enemies}, {}
        for n in OPTIONS:
            have = [(d["items"][n], weights.get(str(h), 0.0)) for h, d in rows.items() if d["items"].get(n)]
            held = sum(1 for d in rows.values() if d["items"].get(n) is None)
            mean_vs = wmean([(v["vs"][e], w * weights.get(e, 0.0)) for v, w in have for e in v["vs"]])
            items[n] = {"gain": r4(wmean([(v["gain"], w) for v, w in have])),
                        "per_1000": r4(wmean([(v["per_1000"], w) for v, w in have])),
                        "mean_vs": r4(mean_vs), "buyers": len(have), "held": held}
            for e in enemies:
                m = wmean([(v["vs"][e], w) for v, w in have if e in v["vs"]])
                enemy[e][n] = None if m is None else [r4(m), r4(m - mean_vs)]
        for h, d in sorted(rows.items()):
            hero[str(h)] = {"base": d["base"],
                            "items": {n: None if v is None else
                                      {"gain": v["gain"], "per_1000": v["per_1000"], "added": v["added_souls"],
                                       "vs": [v["vs"].get(e) for e in enemies]}
                                      for n, v in d["items"].items()}}
        res["budgets"][str(b)] = {"enemies": enemies, "weights": weights, "items": items, "enemy": enemy,
                                  "hero": hero}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "sim.json"), "w") as f:
        json.dump(res, f, separators=(",", ":"))
    write_md(res)
    print(f"counters: {sum(len(v) for v in jobs.values())} jobs, budgets {sorted(jobs)} -> {OUT}/sim.json")


def write_md(res):
    H = res["heroes"]
    L = [f"# Counter items in the sim ({res['bracket']} and up)\n",
         f"Built {res['built']} by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item "
         "added on top and is scored with the overall test (net damage dealt before dying against every hero's "
         "typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall "
         "score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in "
         "the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on "
         "Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular "
         "build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's "
         "mean over all enemies.\n"]
    for b, d in res["budgets"].items():
        L.append(f"## {int(b):,} souls\n\n| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |"
                 "\n|---|---|---|---|---|---|---|")
        cost = {x["name"]: x["cost"] for x in res["items"]}
        for n, v in sorted(d["items"].items(), key=lambda x: -(x[1]["per_1000"] or -9)):
            if v["gain"] is None:
                continue
            best = sorted(((e, row[n]) for e, row in d["enemy"].items() if row.get(n)), key=lambda x: -x[1][1])[:3]
            L.append(f"| {n} | {cost[n]:,} | {v['gain']:+.3f} | {v['per_1000']:+.3f} | {v['mean_vs']:+.3f} | "
                     + ", ".join(f"{H[e]} {m[1]:+.2f}" for e, m in best) + f" | {v['held']} heroes |")
        L.append("\nBest counter per enemy hero (highest lift; matchup change in brackets):\n")
        for e in d["enemies"]:
            row = [(n, m) for n, m in d["enemy"][e].items() if m]
            top = sorted(row, key=lambda x: -x[1][1])[:3]
            L.append(f"- **{H[e]}**: " + ", ".join(f"{n} {m[1]:+.2f} ({m[0]:+.2f})" for n, m in top))
        L.append("")
    with open(os.path.join(OUT, "sim.md"), "w") as f:
        f.write("\n".join(L))


if __name__ == "__main__":
    main()
