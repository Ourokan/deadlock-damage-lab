"""Step 3: search the item build space per hero and souls budget against real opponent builds.

For every hero and souls budget (net worth), find the item sets that win 1v1 duels most often and fastest against
the builds real ranked players actually have at that net worth.

Opponents (per budget, from scripts/build_pool.py snapshots of current-patch ranked games):
  F  "typical" pool: one real build per hero (the snapshot whose items are most common for that hero), all 41
     heroes, weighted by how often the hero reaches that budget. All ranking happens on F.
  F2 "random" pool: one random real snapshot per hero, same weights. Only used to re-check the final builds
     (robustness against less typical builds).
  S  screening pool: the 16 most-played heroes of F. Used to estimate item values cheaply.

Fight: deadsim.duel, 30 s cap, both sides at ranked median aim with real ability landing and melee rates
(hero_default_skill), distance = mean of the two heroes' real median engagement distances. Both sides have the same
net worth; the candidate may spend ITEM_SHARE of it on items, the share real players hold in items at that worth.

Per fight score = win (1 / timeout 0.5 / 0) + 0.3 * HP margin (my HP% - enemy HP%) + 0.2 * speed (1 - t/30 on a
win). Build score = weighted mean over the pool. Ranking is by score; win rate and time are reported separately.

Search (deterministic, the sim has no randomness):
  seed = the hero's most popular real build at that budget (topped up with the best affordable items)
  repeat up to ROUNDS: on S, measure each candidate item's value when added to the current build and each owned
  item's value when removed; propose swaps (1-for-1, 2-for-1, 1-for-2, add) ranked by predicted gain per the
  measured values; evaluate the best proposals on S, the best few on F; move to the best F improvement.
  Everything evaluated on F goes to an archive; the top builds are re-checked on F2.

Constraints: <= 12 items, total cost <= item budget, no duplicates, never an item together with its own component.

usage: python3 scripts/search.py [--bracket all|low|phantom|ascendant|eternus|eternus5] [--workers 4] [--heroes "Haze,Abrams"] [--budgets 18000,37000]
Results: work/jobs/<hero_id>_<budget>.json (one per job; existing ones are skipped, so it resumes).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "..", "sim"))
sys.path.insert(0, HERE)

from deadsim import Loadout, duel, game, compute_stats  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
from deadsim.accuracy import default_distance, hero_default_skill  # noqa: E402
from deadsim.items_fx import MODELED  # noqa: E402
from build_pool import BUDGETS, BRACKETS, item_budget, suffix  # noqa: E402

MAX_TIME = 30.0
MAX_ITEMS = 12
S_SIZE = 16
ROUNDS = 8
MIN_GAIN = 0.004        # stop when a round improves the F score by less than this
FULL_SCAN_ROUNDS = 1      # rounds that scan every candidate item; later rounds scan the TOP_SCAN best + owned
TOP_SCAN = 45
PROPOSALS_S = 14          # proposals evaluated on S per round
PROPOSALS_F = 4           # best S proposals evaluated on F per round
TOP_OUT = 10
# no effect in a 1v1 at fixed distance (multi-target) or no modeled effect at all
EXCLUDE = {"upgrade_ricochet", "upgrade_split_shot"}

_G = None
BRACKET = "all"   # rank bracket (build_pool.BRACKETS): opponent builds and aim percentile
_ctx = {}


def G():
    global _G
    if _G is None:
        _G = game()
        load_heroes()
    return _G


# ---------------------------------------------------------------------------------------------------------------
# pools
# ---------------------------------------------------------------------------------------------------------------
def load_pools(budget):
    """Returns dict with F, F2, S (lists of (hero_id, items, weight)), usage per hero, real snapshots."""
    snaps = json.load(open(os.path.join(ROOT, "work", f"snapshots_{budget}{suffix(BRACKET)}.json")))
    usage = json.load(open(os.path.join(ROOT, "work", f"item_usage{suffix(BRACKET)}.json")))[str(budget)]
    g = G()
    n = {h: usage[h]["_n"] for h in usage if int(h) in g.heroes}
    tot = sum(n.values())
    F, F2 = [], []
    for h, rows in sorted(snaps.items(), key=lambda x: int(x[0])):
        if int(h) not in g.heroes or not rows:
            continue
        u = usage[h]
        freq = {int(i): c / u["_n"] for i, c in u.items() if i != "_n"}

        def typical(items):
            return sum(freq.get(i, 0) for i in items) / max(1, len(items)) * min(1.0, len(items) / 4)

        best = max(rows, key=lambda r: typical(r[0]))
        w = n[h] / tot
        F.append((int(h), tuple(best[0]), w))
        F2.append((int(h), tuple(rows[(int(h) * 7919) % len(rows)][0]), w))
    S = sorted(F, key=lambda x: -x[2])[:S_SIZE]
    return {"F": F, "F2": F2, "S": S, "usage": usage, "snaps": snaps}


# ---------------------------------------------------------------------------------------------------------------
# evaluation
# ---------------------------------------------------------------------------------------------------------------
_skill_cache, _dist_cache, _maxhp_cache = {}, {}, {}


def skill(h):
    if h not in _skill_cache:
        lo = BRACKETS[BRACKET][0]   # rank-dependent behaviour (Dispel Magic timing) uses the bracket's lowest badge
        _skill_cache[h] = hero_default_skill(G().hero(h).name, BRACKETS[BRACKET][2], badge=lo if lo > 0 else None)
    return _skill_cache[h]


def dist(h):
    if h not in _dist_cache:
        _dist_cache[h] = default_distance(G().hero(h).name)
    return _dist_cache[h]


def max_hp(h, items, souls):
    k = (h, items, souls)
    if k not in _maxhp_cache:
        _maxhp_cache[k] = compute_stats(h, list(items), souls=souls).max_health
    return _maxhp_cache[k]


def fight(h, items, oh, oitems, souls):
    """One duel; returns (win, margin, time) from the candidate's side."""
    a = Loadout(h, list(items), souls=souls, skill=skill(h))
    b = Loadout(oh, list(oitems), souls=souls, skill=skill(oh))
    r = duel(a, b, distance=(dist(h) + dist(oh)) / 2, max_time=MAX_TIME)
    if r.winner is None:
        win = 0.5
    else:
        win = 1.0 if r.winner.endswith("(A)") else 0.0
    m = max(0.0, r.a_hp) / max_hp(h, items, souls) - max(0.0, r.b_hp) / max_hp(oh, oitems, souls)
    return win, m, r.time


def fight_score(win, m, t):
    speed = (1 - t / MAX_TIME) if win == 1.0 else 0.0
    return win + 0.3 * m + 0.2 * speed


class Evaluator:
    def __init__(self, hero, budget, pools):
        self.h, self.souls, self.pools = hero, budget, pools
        self.cache = {}
        self.fights = 0

    def run(self, items, pool="F", detail=False):
        key = (tuple(sorted(items)), pool)
        if key not in self.cache:
            rows = []
            for oh, oitems, w in self.pools[pool]:
                win, m, t = fight(self.h, key[0], oh, oitems, self.souls)
                rows.append((oh, w, win, m, t))
                self.fights += 1
            self.cache[key] = rows
        rows = self.cache[key]
        tw = sum(r[1] for r in rows)
        score = sum(r[1] * fight_score(*r[2:]) for r in rows) / tw
        if not detail:
            return score
        wins = [r for r in rows if r[2] == 1.0]
        return {
            "score": round(score, 4),
            "win_rate": round(sum(r[1] * r[2] for r in rows) / tw, 4),
            "loss_rate": round(sum(r[1] for r in rows if r[2] == 0.0) / tw, 4),
            "hp_margin": round(sum(r[1] * r[3] for r in rows) / tw, 4),
            "avg_win_time_s": round(sum(r[1] * r[4] for r in wins) / sum(r[1] for r in wins), 2) if wins else None,
            "matchups": {str(r[0]): [r[2], round(r[3], 3), round(r[4], 2)] for r in rows},
        }


# ---------------------------------------------------------------------------------------------------------------
# build space
# ---------------------------------------------------------------------------------------------------------------
def component_ids(item):
    """All component ids below an item (recursive)."""
    g = G()
    out = set()
    stack = list(item.components)
    while stack:
        c = stack.pop()
        it = g.items_by_class.get(c)
        if it and it.id not in out and it.id != item.id:
            out.add(it.id)
            stack += list(it.components)
    return out


def valid(items, limit):
    g = G()
    if len(items) > MAX_ITEMS or len(set(items)) != len(items):
        return False
    if sum(g.items[i].cost for i in items) > limit:
        return False
    s = set(items)
    for i in items:
        if component_ids(g.items[i]) & s:
            return False
    return True


def candidates(limit, usage):
    """Items the search may use: tiers 1-4 with a modeled effect or always-on stats; tier 5 only if real players
    buy them at this budget."""
    g = G()
    out = []
    for it in g.items.values():
        if it.cost <= 0 or it.cost > limit or it.class_name in EXCLUDE:
            continue
        if not (it.class_name in MODELED or it.innate):
            continue
        if it.tier == 5 and sum(c.get(str(it.id), 0) for c in usage.values()) < 50:
            continue
        out.append(it.id)
    return out


def cost(items):
    g = G()
    return sum(g.items[i].cost for i in items)


def popular_build(hero, limit, pools):
    """Most popular real build: the hero's snapshots' item frequencies, greedy by frequency under the limit."""
    u = pools["usage"].get(str(hero))
    if not u:
        return []
    freq = sorted(((c / u["_n"], int(i)) for i, c in u.items() if i != "_n"), reverse=True)
    build = []
    for f, i in freq:
        if f < 0.15:
            break
        if i in G().items and valid(build + [i], limit):
            build.append(i)
    return build


def search(hero, budget, log=print):
    g = G()
    pools = load_pools(budget)
    limit = item_budget(budget)
    ev = Evaluator(hero, budget, pools)
    cand = candidates(limit, pools["usage"])
    t0 = time.time()

    popular = popular_build(hero, limit, pools)
    archive = {}

    def full(items):
        items = tuple(sorted(items))
        if items not in archive:
            archive[items] = ev.run(items, "F")
        return archive[items]

    cur = list(popular)
    cur_f = full(cur)
    log(f"  seed popular {len(cur)} items cost {cost(cur)} F={cur_f:.3f}")
    scan_set = list(cand)
    for rnd in range(ROUNDS):
        base_s = ev.run(cur, "S")
        add_v = {}
        for j in scan_set:
            if j in cur or not valid(cur + [j], 10 ** 9) and len(cur) < MAX_ITEMS:
                continue
            trial = [i for i in cur if j not in component_ids(g.items[i]) and i not in component_ids(g.items[j])]
            add_v[j] = ev.run(trial + [j], "S") - base_s
        rem_v = {i: base_s - ev.run([x for x in cur if x != i], "S") for i in cur}
        if rnd < FULL_SCAN_ROUNDS:
            scan_set = sorted(add_v, key=lambda j: -add_v[j] / g.items[j].cost)[:TOP_SCAN] + \
                sorted(add_v, key=lambda j: -add_v[j])[:15]
            scan_set = list(dict.fromkeys(scan_set))
        # proposals
        props = []
        slack = limit - cost(cur)
        adds = sorted(add_v, key=lambda j: -add_v[j])[:30]

        def propose(remove, add):
            new = [i for i in cur if i not in remove]
            for j in add:
                new = [i for i in new if i not in component_ids(g.items[j])]
                new.append(j)
            if valid(new, limit) and tuple(sorted(new)) not in archive:
                pred = sum(add_v.get(j, 0) for j in add) - sum(rem_v.get(i, 0) for i in remove if i in cur)
                props.append((pred, tuple(sorted(new))))

        for j in adds:
            propose([], [j])
            for i in cur:
                propose([i], [j])
        cheap = sorted(cur, key=lambda i: rem_v[i] / g.items[i].cost)[:6]
        for a in range(len(cheap)):
            for b in range(a + 1, len(cheap)):
                for j in adds[:15]:
                    propose([cheap[a], cheap[b]], [j])
        for i in cheap[:4]:
            for a in range(min(10, len(adds))):
                for b in range(a + 1, min(10, len(adds))):
                    propose([i], [adds[a], adds[b]])
        if slack > 0:
            for a in range(min(10, len(adds))):
                for b in range(a + 1, min(10, len(adds))):
                    propose([], [adds[a], adds[b]])
        props = sorted(set(props), key=lambda p: -p[0])[:PROPOSALS_S]
        if not props:
            break
        scored = sorted(((ev.run(p, "S"), p) for _, p in props), key=lambda x: -x[0])
        best_f, best_p = cur_f, None
        for s_val, p in scored[:PROPOSALS_F]:
            f = full(p)
            if f > best_f:
                best_f, best_p = f, p
        log(f"  round {rnd + 1}: {len(add_v)} items scanned, best F {best_f:.3f} "
            f"({'moved' if best_p else 'no gain'}), fights {ev.fights}, {time.time() - t0:.0f}s")
        if best_p is None:
            break
        gain = best_f - cur_f
        cur, cur_f = list(best_p), best_f
        if gain < MIN_GAIN:
            break

    # rank everything evaluated on F
    ranked = sorted(archive.items(), key=lambda x: -x[1])[:TOP_OUT]
    out_builds = []
    for items, f in ranked:
        d = ev.run(items, "F", detail=True)
        d2 = ev.run(items, "F2", detail=True)
        out_builds.append({"items": list(items), "cost": cost(items), "F": d, "F2": {k: d2[k] for k in d2 if k != "matchups"}})
    pop_items = tuple(sorted(popular))
    pop = {"items": list(pop_items), "cost": cost(pop_items), "F": ev.run(pop_items, "F", detail=True)}
    d2 = ev.run(pop_items, "F2", detail=True)
    pop["F2"] = {k: d2[k] for k in d2 if k != "matchups"}
    # item value at the best build: gain when added / loss when removed, on F
    best = list(ranked[0][0])
    base = ev.run(best, "F")
    item_values = {str(i): round(base - ev.run([x for x in best if x != i], "F"), 4) for i in best}
    return {
        "hero_id": hero, "hero": g.hero(hero).name, "budget": budget, "item_budget": limit,
        "builds": out_builds, "popular": pop, "best_item_removal_loss": item_values,
        "fights": ev.fights, "seconds": round(time.time() - t0, 1), "candidates": len(cand),
    }


def job(args):
    hero, budget = args
    path = os.path.join(ROOT, "work", "jobs" + suffix(BRACKET), f"{hero}_{budget}.json")
    if os.path.exists(path):
        return path, "skip"
    lines = []
    res = search(hero, budget, log=lines.append)
    res["log"] = lines
    tmp = path + ".tmp"
    json.dump(res, open(tmp, "w"))
    os.replace(tmp, path)
    return path, f"{res['hero']} {budget}: best {res['builds'][0]['F']['score']} vs popular {res['popular']['F']['score']}" \
                 f" ({res['fights']} fights, {res['seconds']}s)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--heroes", default="")
    ap.add_argument("--budgets", default="")
    ap.add_argument("--bracket", default="all", choices=list(BRACKETS))
    a = ap.parse_args()
    global BRACKET
    BRACKET = a.bracket
    g = G()
    heroes = [g.hero(h).id for h in a.heroes.split(",") if h] or sorted(g.heroes)
    budgets = [int(b) for b in a.budgets.split(",") if b] or BUDGETS
    os.makedirs(os.path.join(ROOT, "work", "jobs" + suffix(BRACKET)), exist_ok=True)
    order = [27000, 18000, 37000, 10000, 50000]
    budgets = sorted(budgets, key=lambda b: order.index(b) if b in order else 99)
    jobs = [(h, b) for b in budgets for h in heroes]
    with Pool(a.workers) as p:
        for path, msg in p.imap_unordered(job, jobs):
            print(time.strftime("%H:%M:%S"), msg, flush=True)


if __name__ == "__main__":
    main()
