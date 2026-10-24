"""What each counter item is worth in the current sim, per buyer hero and per enemy hero.

Scored with the overall test (damage/scripts/overall_search.py, standard bracket build_pool.PRIMARY, Phantom and up):
net damage dealt before dying against the typical real build of every hero at the same net worth, enemy at x2
damage, counterplay, sustain (real fight entry health, gap healing, heal trips), movement value, mechanics on
(parry, Counterspell, Ricochet...), range spread and targetable summons. Whatever the sim knows about a fight, a
counter item gets credit for.

For each buyer hero and net worth, the hero's most popular real build is scored as is and once per counter item
added on top of it (a free extra, its held components consumed, like damage/scripts/item_probe.py). Per item:
- gain: overall score change (1.0 = the popular build), so 0.05 = 5% more damage before dying over all enemies;
- per_1000: gain per 1,000 souls the item adds (its cost minus held components);
- vs: per enemy hero, the change in that matchup's net damage before dying (x the movement and time-on-map
  ratios), as a share of the popular build's mean over all matchups, so the enemy-weighted mean of vs is gain and a
  matchup the hero barely scores in can't blow up into a huge ratio. Raw matchup damage is kept too (matchups).
Items the popular build already holds are left out (null).

usage: python3 counters/scripts/sim_counters.py [--workers 4] [--heroes Haze,7] [--budgets 27000]
Writes counters/work/jobs/<hero_id>_<budget>.json (resumes); counters/scripts/export_sim.py builds counters/out/sim.json.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "damage", "scripts"))

import game_path as GP  # noqa: E402
import overall_search as O  # noqa: E402

S = O.S
JOBS = os.path.join(ROOT, "counters", "work", "jobs")
# the five counters of the real analysis (counters/README.md), the nine defensive items it compares them with, and
# Healbane (the counter to enemy healing)
OPTIONS = ["Dispel Magic", "Counterspell", "Metal Skin", "Return Fire", "Plated Armor", "Debuff Reducer",
           "Bullet Resilience", "Spirit Resilience", "Unstoppable", "Spellbreaker", "Witchmail", "Reactive Barrier",
           "Indomitable", "Divine Barrier", "Healbane"]
BUDGETS = [18000, 27000, 37000, 50000]   # counters are bought from ~17 min (Return Fire) to ~32 min (Plated Armor)


def matchup_gain(d, base, enemy):
    """Change in one matchup, in overall-score units: (net damage before dying x movement x map time with the item -
    without) / the popular build's mean net damage before dying."""
    mult = (d["movement_value"] / base["movement_value"]) * (d["map_time"] / base["map_time"])
    m, m0 = d["matchups"][enemy][0], base["matchups"][enemy][0]
    return (m * mult - m0) / max(1.0, base["damage_before_death"])


def job(args):
    hero, b = args
    path = os.path.join(JOBS, f"{hero}_{b}.json")
    if os.path.exists(path):
        return path, "skip"
    t0 = time.time()
    O._phases()
    g = S.G()
    pools = S.load_pools(b)
    ev = GP.make_evaluator(hero, b, pools)
    pop = list(S.popular_build(hero, GP.item_budget(b), pools))
    base = ev.run(pop, detail=True)
    items = {}
    for name in OPTIONS:
        it = g.item(name)
        if it.id in pop:
            items[name] = None
            continue
        build = GP.with_item(pop, it.id)
        added = it.cost - sum(g.items[i].cost for i in pop if i not in build)
        d = ev.run(build, detail=True)
        gain = d["score"] - base["score"]
        items[name] = {"gain": round(gain, 4), "added_souls": added,
                       "per_1000": round(gain / max(500, added) * 1000, 4),
                       "time_alive_s": d["time_alive_s"], "entry_hp": d["entry_hp"],
                       "vs": {e: round(matchup_gain(d, base, e), 4) for e in base["matchups"]},
                       "matchups": {e: m[0] for e, m in d["matchups"].items()}}
    res = {"hero": hero, "budget": b, "bracket": S.BRACKET, "popular": pop,
           "base": {k: base[k] for k in ("score", "damage_before_death", "time_alive_s", "entry_hp")},
           "base_matchups": {e: m[0] for e, m in base["matchups"].items()},
           "weights": {str(h): w for h, _, w in pools["F"]}, "items": items, "fights": ev.fights,
           "seconds": round(time.time() - t0, 1)}
    with open(path + ".tmp", "w") as f:
        json.dump(res, f)
    os.replace(path + ".tmp", path)
    best = max(((n, v["gain"]) for n, v in items.items() if v), key=lambda x: x[1], default=("-", 0))
    return path, f"{g.heroes[hero].name} {b}: best {best[0]} {best[1]:+.3f} ({res['fights']} fights, {res['seconds']} s)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--heroes", default="")
    ap.add_argument("--budgets", default="")
    a = ap.parse_args()
    g = S.G()
    heroes = [g.hero(int(h) if h.isdigit() else h).id for h in a.heroes.split(",") if h] or sorted(g.heroes)
    budgets = [int(b) for b in a.budgets.split(",") if b] or BUDGETS
    budgets = [b for b in budgets if b in BUDGETS]   # run_shard passes its own budgets; counters skip the lane ones
    os.makedirs(JOBS, exist_ok=True)
    jobs = [(h, b) for b in budgets for h in heroes]
    with Pool(a.workers) as p:
        for path, msg in p.imap_unordered(job, jobs):
            print(time.strftime("%H:%M:%S"), msg, flush=True)


if __name__ == "__main__":
    main()
