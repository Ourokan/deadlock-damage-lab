"""What each counter item is worth in the step 2 sim, per attacking hero.

Every hero's typical real build at a budget (search/out/opponents.json) duels every other hero's typical build, once
as is and once per counter item added to it (same souls, so the item is a free extra). Fight settings match the
build search: deadsim.duel, 30 s cap, ranked median aim and landing rates, mean real engagement distance.

Per (counter, attacker) the gain is the defender's mean score change over all defenders that don't already own the
item. Score = win (1 / 0.5 timeout / 0) + 0.3 x HP margin, the build search's score without its speed bonus.

    python3 scripts/sim_counters.py --budget 27000 --workers 4
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from multiprocessing import Pool

ROOT = "/mnt/project-files"
sys.path.insert(0, f"{ROOT}/sim")

from deadsim import Loadout, compute_stats, duel  # noqa: E402
from deadsim.accuracy import default_distance, hero_default_skill  # noqa: E402
from deadsim.data import game  # noqa: E402

OPTIONS = ["Metal Skin", "Return Fire", "Plated Armor", "Dispel Magic", "Counterspell",
           "Debuff Reducer", "Bullet Resilience", "Spirit Resilience", "Fortitude", "Unstoppable"]
ITEMS = {x["name"]: x["id"] for x in json.load(open(f"{ROOT}/data/game/shop_items.json"))}
_sk, _dist = {}, {}


def skill(h):
    if h not in _sk:
        _sk[h] = hero_default_skill(game().hero(h).name, "p50")
    return _sk[h]


def dist(h):
    if h not in _dist:
        _dist[h] = default_distance(game().hero(h).name)
    return _dist[h]


def score(d_hero, d_items, a_hero, a_items, souls):
    d = Loadout(d_hero, list(d_items), souls=souls, skill=skill(d_hero))
    a = Loadout(a_hero, list(a_items), souls=souls, skill=skill(a_hero))
    r = duel(d, a, distance=(dist(d_hero) + dist(a_hero)) / 2, max_time=30.0)
    win = 0.5 if r.winner is None else (1.0 if r.winner.endswith("(A)") else 0.0)
    m = max(0.0, r.a_hp) / compute_stats(d_hero, list(d_items), souls=souls).max_health \
        - max(0.0, r.b_hp) / compute_stats(a_hero, list(a_items), souls=souls).max_health
    dmg_taken = sum(r.b_dmg.values())
    return win + 0.3 * m, win, r.time, dmg_taken, r.a_dmg


def job(args):
    d, pool, souls = args
    out = {}
    for a in pool:
        if a["hero_id"] == d["hero_id"]:
            continue
        row = {}
        base = score(d["hero_id"], d["items"], a["hero_id"], a["items"], souls)
        row["none"] = base[:4]
        for name in OPTIONS:
            iid = ITEMS[name]
            if iid in d["items"]:
                continue
            s = score(d["hero_id"], d["items"] + [iid], a["hero_id"], a["items"], souls)
            row[name] = s[:4] + (round(s[4].get(name, 0.0), 1),)
        out[a["hero_id"]] = row
    return d["hero_id"], out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", default="27000")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    pool = json.load(open(f"{ROOT}/search/out/opponents.json"))["all"][a.budget]["typical"]
    defenders = pool[:a.limit] if a.limit else pool
    res = {}
    with Pool(a.workers) as p:
        for h, out in p.imap_unordered(job, [(d, pool, int(a.budget)) for d in defenders]):
            res[h] = out
            print("defender", h, "done", file=sys.stderr, flush=True)
    os.makedirs(f"{ROOT}/counters/out", exist_ok=True)
    json.dump({"budget": int(a.budget), "options": OPTIONS, "weights": {d["hero_id"]: d["weight"] for d in pool},
               "defender_items": {d["hero_id"]: d["items"] for d in pool}, "duels": res},
              open(f"{ROOT}/counters/out/sim_{a.budget}.json", "w"))


if __name__ == "__main__":
    main()
