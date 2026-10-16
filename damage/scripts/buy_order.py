"""Item buy order: the order to buy a hero's best 50k damage build in, with the net worth milestones on the way.

The dummy damage search (dummy_search.py) finds the best finished build at each net worth, but those builds don't
line up: you can't hold the 18k best build, then the 27k one, without selling. This script takes the best 50k build
for each objective as the target and works out the order to buy it in:

- Pieces: the target's items plus their components. Buying an upgrade while holding its component costs only the
  difference (the game credits the component), so a component can be a cheap early step toward its upgrade.
- Greedy by damage per soul: from an empty build, try every piece not yet owned, and buy the one with the most
  extra damage per soul it costs, measured at the net worth you'd have when you can afford it (hero level and
  boons included). Repeat until the target is complete. No selling.
- Net worth for an item spend: the lowest net worth whose item budget (share of net worth real players hold in
  items, build_pool.item_budget) covers it, rounded up to 500.
- Milestones (10k/18k/27k/37k/50k): what the path holds at each, its damage there, and how close that is to the
  best build the dummy search found for that exact net worth (which is free to pick items you'd later sell).

Same dummy as the damage search: no resists, refills instead of dying, HP interpolated from the median real build
HP at each budget.

usage: python3 scripts/buy_order.py [--workers 4] [--heroes Haze] [--use-published]
Reads work/jobs/<hero>_<budget>.json from dummy_search.py (out/heroes/<id>.json with --use-published). Writes
work/jobs_order/<hero_id>.json (resumes); scripts/export.py copies them to out/order/.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "..", "sim"))
sys.path.insert(0, os.path.join(ROOT, "..", "search", "scripts"))
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)

from build_pool import BUDGETS, item_budget  # noqa: E402
import search as S  # noqa: E402
import dummy_search as D  # noqa: E402

JOBS = os.path.join(ROOT, "work", "jobs_order")
NW_STEP = 500


def net_worth_for(spend):
    """Lowest net worth (multiple of NW_STEP) whose item budget covers this item spend."""
    nw = max(NW_STEP, int(math.ceil(spend / 0.9 / NW_STEP)) * NW_STEP)
    while nw > NW_STEP and item_budget(nw - NW_STEP) >= spend:
        nw -= NW_STEP
    while item_budget(nw) < spend:
        nw += NW_STEP
    return nw


USE_PUBLISHED = False   # --use-published: read out/heroes (local runs without work/jobs); never in the reruns


def search_results(hero):
    """{budget: {"dummy_hp", "objectives": {obj: {"best_items", "best"}}, "popular"}} from the damage search."""
    out = {}
    for b in BUDGETS:
        fn = os.path.join(ROOT, "work", "jobs", f"{hero}_{b}.json")
        if os.path.exists(fn):
            with open(fn) as f:
                out[b] = json.load(f)
    # published results only on request, so a rerun never mixes in the previous patch's out/heroes
    if USE_PUBLISHED and not out:
        fn = os.path.join(ROOT, "out", "heroes", f"{hero}.json")
        if os.path.exists(fn):
            with open(fn) as f:
                for b, r in json.load(f)["budgets"].items():
                    out.setdefault(int(b), r)
    return out


class Path:
    def __init__(self, hero, res):
        self.hero = hero
        self.hp_pts = sorted((b, r["dummy_hp"]) for b, r in res.items())
        self.cache = {}

    def hp(self, nw):
        pts = self.hp_pts
        if nw <= pts[0][0]:
            return pts[0][1]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if nw <= x1:
                return round(y0 + (y1 - y0) * (nw - x0) / (x1 - x0))
        return pts[-1][1]

    def dmg(self, items, nw):
        k = (tuple(sorted(items)), nw)
        if k not in self.cache:
            self.cache[k] = D.run_dummy(self.hero, k[0], nw, self.hp(nw))[0]
        return self.cache[k]


def after_buy(owned, piece):
    """Build after buying `piece`: owned components of it are consumed. Returns (new build, souls paid)."""
    g = S.G()
    comps = S.component_ids(g.items[piece])
    used = [i for i in owned if i in comps]
    new = [i for i in owned if i not in used] + [piece]
    return new, g.items[piece].cost - sum(g.items[i].cost for i in used)


def plan(path, target, obj):
    g = S.G()
    target = list(target)
    pieces = set(target)
    for i in target:
        pieces |= S.component_ids(g.items[i]) & set(g.items)
    owned, spent, steps = [], 0, []
    while set(target) - set(owned):
        best = None
        for p in pieces:
            if p in owned:
                continue
            # skip a component once its upgrade (or anything above it) is owned
            if any(p in S.component_ids(g.items[o]) for o in owned):
                continue
            new, paid = after_buy(owned, p)
            if len(new) > S.MAX_ITEMS:
                continue
            nw = net_worth_for(spent + paid)
            gain = path.dmg(new, nw)[obj] - path.dmg(owned, nw)[obj]
            score = gain / max(1, paid)
            if best is None or score > best[0] + 1e-12 or (abs(score - best[0]) <= 1e-12 and paid < best[3]):
                best = (score, p, new, paid, nw, gain)
        if best is None:   # every remaining piece is blocked (item cap): don't save a partial order as finished
            raise RuntimeError(f"no buyable piece left toward {sorted(set(target) - set(owned))}")
        _, p, new, paid, nw, gain = best
        replaced = [i for i in owned if i not in new]
        owned, spent = new, spent + paid
        steps.append({"item": p, "replaces": replaced, "paid": paid, "spent": spent, "net_worth": nw,
                      "gain": round(gain, 1), "damage": round(path.dmg(owned, nw)[obj], 1)})
    return steps


def milestones(path, res, steps, obj):
    out = {}
    for b in BUDGETS:
        limit = item_budget(b)
        held = []
        for s in steps:
            if s["spent"] > limit:
                break
            held = [i for i in held if i not in s["replaces"]] + [s["item"]]
        r = res.get(b)
        # re-run the search's builds on the current sim, so the comparison holds even if the sim changed since
        best = round(path.dmg(r["objectives"][obj]["builds"][0]["items"], b)[obj], 1) if r else None
        pop = round(path.dmg(r["popular"]["items"], b)[obj], 1) if r else None
        d = path.dmg(held, b)[obj] if held else 0.0
        out[str(b)] = {"items": sorted(held), "cost": S.cost(held), "item_budget": limit, "damage": round(d, 1),
                       "best_damage": best, "popular_damage": pop,
                       "share_of_best": round(d / best, 3) if best else None}
    return out


def order_job(args):
    hero, use_published = args
    global USE_PUBLISHED
    USE_PUBLISHED = use_published
    path_fn = os.path.join(JOBS, f"{hero}.json")
    if os.path.exists(path_fn):
        return path_fn, "skip"
    g = S.G()
    t0 = time.time()
    res = search_results(hero)
    missing = [b for b in BUDGETS if b not in res]
    if missing:
        raise RuntimeError(f"hero {hero}: no damage search result at {missing}")
    path = Path(hero, res)
    out = {"hero_id": hero, "hero": g.hero(hero).name, "target_budget": 50000, "objectives": {}}
    for obj in D.WINDOWS:
        target = res[50000]["objectives"][obj]["builds"][0]["items"]
        steps = plan(path, target, obj)
        out["objectives"][obj] = {"target": sorted(target), "steps": steps,
                                  "milestones": milestones(path, res, steps, obj)}
    out.update({"fights": len(path.cache), "seconds": round(time.time() - t0, 1)})
    os.makedirs(JOBS, exist_ok=True)
    with open(path_fn + ".tmp", "w") as f:
        json.dump(out, f)
    os.replace(path_fn + ".tmp", path_fn)
    m = out["objectives"]["fight_15s"]["milestones"]
    shares = " ".join(f"{int(b) // 1000}k {v['share_of_best']:.0%}" for b, v in m.items() if v["share_of_best"])
    return path_fn, f"{out['hero']}: 15 s path vs best build at each milestone {shares} " \
                    f"({out['fights']} fights, {out['seconds']}s)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--heroes", default="")
    ap.add_argument("--use-published", action="store_true",
                    help="read out/heroes when work/jobs has nothing for a hero (local runs only)")
    ap.add_argument("--budgets", default="", help="the order needs every budget; a run limited to some skips it")
    a = ap.parse_args()
    if a.budgets and {int(b) for b in a.budgets.split(",")} != set(BUDGETS):
        print("buy order skipped: it needs the damage search at every budget")
        return
    g = S.G()
    heroes = [g.hero(int(h) if h.isdigit() else h).id for h in a.heroes.split(",") if h] or sorted(g.heroes)
    with Pool(a.workers) as p:
        for path_fn, msg in p.imap_unordered(order_job, [(h, a.use_published) for h in heroes]):
            print(time.strftime("%H:%M:%S"), msg, flush=True)


if __name__ == "__main__":
    main()
