"""Ability upgrade order: the order to spend ability points in that makes a hero's best damage builds hit hardest.

The sim normally levels abilities the way real players do (the most played order, deadsim.fight
popular_ability_order). This script searches the upgrade order instead, per hero and objective, on the dummy damage
search's best build at each net worth:

- Ability points and unlocks come from the hero's levels (deadsim.fight.ability_budget): unlocks at levels 1, 3, 5
  and 8 (all four abilities by ~3.8k souls), one point at every other level, 32 in all. Upgrades cost 1, 2 and 5
  points for tiers 1, 2 and 3. The four unlocks keep the popular order's sequence (they come at fixed levels and
  every ability is unlocked before the first milestone, so the choice doesn't change any number here).
- Milestones 10k/18k/27k/37k/50k have 12/20/24/28/32 points. At each, an order leaves the hero with some tiers. A
  candidate is every tier spread the points pay for, scored with that milestone's best build against the damage
  search's dummy: damage / the popular order's damage there. Points can sit unspent: an order buys strictly in
  sequence, so it waits when its next upgrade costs more than the points left (saving for a tier 3).
- One order has to pass through all milestones, so the tiers at one milestone must be contained in the next one's,
  and the order must be able to stop there (its next upgrade unaffordable). The order picked maximizes the summed
  score over the milestones under those rules (dynamic programming over tier spreads); the popular order is one of
  the chains, so the sum never falls below it, though one milestone can drop a little to gain more at others.
  Between milestones, upgrades go in the order of most extra damage per point, measured with the next milestone's
  build.
- An upgrade never counts as making things worse: each spread scores as the best spread it contains. Where the sim
  deals less with more upgrades it's the hero's cast logic (a channel that pauses the gun, say), not the upgrade, so
  skipping upgrades is never what wins. Such rows are flagged (below_fewer_upgrades).
- It also records the best spread at each milestone with no consistency rule, to show what a single order gives up.

Same dummy, aim and windows as dummy_search.py. Duels, the overall score and team fights still use the popular order.

usage: python3 scripts/skill_order.py [--workers 4] [--heroes Haze] [--use-published]
Reads work/jobs/<hero>_<budget>.json from dummy_search.py (out/heroes/<id>.json with --use-published). Writes
work/jobs_skill/<hero_id>.json (resumes); scripts/export.py copies them to out/skill/.
"""
from __future__ import annotations

import argparse
import itertools
import json
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

from build_pool import BUDGETS  # noqa: E402
from deadsim.fight import NET_WORTH_OFFSET, UPGRADE_AP, abilities_for_order, ability_budget, popular_ability_order  # noqa: E402
from dummy import Dummy, damage_test  # noqa: E402
import buy_order as BO  # noqa: E402
import dummy_search as D  # noqa: E402
import search as S  # noqa: E402

JOBS = os.path.join(ROOT, "work", "jobs_skill")
TIER_COST = (0, 1, 3, 8)   # points to reach tier 0..3 (cumulative UPGRADE_AP)


def cost(t):
    return sum(TIER_COST[x] for x in t)


def spreads(n, points):
    """Tier spreads that cost at most `points`."""
    return [t for t in itertools.product(range(4), repeat=n) if cost(t) <= points]


def stops_at(t, points, toward=None):
    """Can an order hold exactly `t` with `points` earned? Its next upgrade (one toward `toward`, or any) must cost
    more than the points left, since the order buys strictly in sequence."""
    left = points - cost(t)
    nxt = [i for i in range(len(t)) if t[i] < 3 and (toward is None or toward[i] > t[i])]
    return (not nxt and toward is None) or any(UPGRADE_AP[t[i]] > left for i in nxt)


class Scorer:
    def __init__(self, hero, res):
        self.hero, self.res = hero, res
        self.cache = {}
        self.fights = 0

    def dmg(self, budget, obj, tiers):
        items = tuple(sorted(self.res[budget]["objectives"][obj]["builds"][0]["items"]))
        k = (items, budget, tuple(tiers))
        if k not in self.cache:
            r = damage_test(self.hero, items, souls=budget, aim=D.AIM, marks=tuple(D.WINDOWS.values()), tiers=list(tiers),
                            dummy=Dummy(hp=self.res[budget]["dummy_hp"], bullet_resist=0, spirit_resist=0,
                                        melee_resist=0, hero=D.DUMMY_HERO, zone_exit_s=D.DUMMY_ZONE_EXIT))
            self.cache[k] = {o: r["damage"][f"{t:g}s"] for o, t in D.WINDOWS.items()}
            self.fights += 1
        return self.cache[k][obj]


def plan(sc, hero, obj, budgets, popular):
    n = len(hero.abilities)
    pts = {b: ability_budget(hero, b)[1] for b in budgets}
    pop = {b: tuple(abilities_for_order(hero, popular, b)[0]) for b in budgets}
    base = {b: max(1e-9, sc.dmg(b, obj, pop[b])) for b in budgets}
    cand = {b: spreads(n, pts[b]) for b in budgets}
    # an upgrade never makes a spread worse: score each spread by the best spread it contains, so the order can't
    # win by skipping an upgrade the sim's cast logic happens to play worse with (e.g. a channel that pauses the gun)
    score = {}
    for b in budgets:
        env = {}
        for t in sorted(cand[b], key=cost):
            env[t] = max([sc.dmg(b, obj, t)] + [env[t[:i] + (t[i] - 1,) + t[i + 1:]] for i in range(n) if t[i]])
        score[b] = {t: v / base[b] for t, v in env.items()}
    # DP: best summed score of a chain of spreads ending in t, each contained in the next, where the order can stop
    # at each one (popular's own chain is one of them, so the result never sums below it)
    back = [{t: (score[budgets[0]][t], None) for t in cand[budgets[0]]}]
    for k, b in enumerate(budgets[1:], start=1):
        prev, cur, pb = back[-1], {}, pts[budgets[k - 1]]
        for t in cand[b]:
            opts = [(v, p) for p, (v, _) in prev.items()
                    if all(x <= y for x, y in zip(p, t)) and (p == t or stops_at(p, pb, t))]
            if opts:
                v, p = max(opts)
                cur[t] = (v + score[b][t], p)
        back.append(cur)
    last = {t: v for t, v in back[-1].items() if stops_at(t, pts[budgets[-1]])}
    t = max(last, key=lambda k: last[k][0])
    chain = [t]
    for layer in reversed(back[1:]):
        t = layer[t][1]
        chain.append(t)
    chain.reverse()

    # upgrades between milestones: most extra damage per point first, with the next milestone's build
    seq, cur, hold = [], (0,) * n, None   # hold: points earned at the last milestone that ended at `cur`
    for b, goal in zip(budgets, chain):
        first = True
        while cur != goal:
            opts = []
            for i in range(n):
                if cur[i] < goal[i] and not (first and hold is not None and UPGRADE_AP[cur[i]] <= hold - cost(cur)):
                    nxt = cur[:i] + (cur[i] + 1,) + cur[i + 1:]
                    gain = score[b][nxt] - score[b][cur]   # every spread up to the goal costs no more than it
                    opts.append((gain / UPGRADE_AP[cur[i]], -UPGRADE_AP[cur[i]], -i, i, nxt))
            *_, i, cur = max(opts)
            seq.append(i)
            first = False
        hold = pts[b]
    # after the last milestone: the rest, most expensive first, so the last milestone's stop holds too
    while any(x < 3 for x in cur):
        i = max(range(n), key=lambda j: (UPGRADE_AP[cur[j]] if cur[j] < 3 else -1, -j))
        cur = cur[:i] + (cur[i] + 1,) + cur[i + 1:]
        seq.append(i)
    order, steps = full_order(hero, popular, seq)
    for b, goal in zip(budgets, chain):
        got = tuple(abilities_for_order(hero, order, b)[0])
        assert got == goal, (hero.name, obj, b, got, goal)
    rows = {}
    for b, goal in zip(budgets, chain):
        top = max((k for k in cand[b] if stops_at(k, pts[b])), key=lambda k: sc.dmg(b, obj, k))
        rows[str(b)] = {
            "items": sorted(sc.res[b]["objectives"][obj]["builds"][0]["items"]),
            "points": pts[b], "tiers": list(goal), "popular_tiers": list(pop[b]),
            "damage": round(sc.dmg(b, obj, goal), 1), "popular_damage": round(base[b], 1),
            "best_tiers": list(top), "best_damage": round(sc.dmg(b, obj, top), 1),
            # the sim deals less with these tiers than with fewer upgrades (its cast logic, not the upgrades)
            "below_fewer_upgrades": score[b][goal] * base[b] > sc.dmg(b, obj, goal) * 1.01,
        }
    return {"order": order, "steps": steps, "budgets": rows}


def full_order(hero, popular, seq):
    """Interleave the popular unlock sequence with the upgrade sequence, level by level, in the API's id format.
    Returns (ability ids, steps with the level and net worth each happens at)."""
    ids = [a.id for a in hero.abilities]
    unlocks = []
    for aid in popular:
        if aid in ids and aid not in unlocks:
            unlocks.append(aid)
    unlocks += [a for a in ids if a not in unlocks]
    tiers, unlocked = [0] * len(ids), set()
    order, steps, points, q = [], [], 0, list(seq)
    for lvl, (g, bonus) in enumerate(zip(hero.level_gold, hero.level_bonus), start=1):
        nw = g + NET_WORTH_OFFSET if g else 0
        if bonus == "unlock" and unlocks:
            aid = unlocks.pop(0)
            unlocked.add(aid)
            order.append(aid)
            steps.append({"ability": aid, "tier": 0, "level": lvl, "net_worth": nw})
        elif bonus == "point":
            points += 1
        while q and ids[q[0]] in unlocked and points >= UPGRADE_AP[tiers[q[0]]]:
            i = q.pop(0)
            points -= UPGRADE_AP[tiers[i]]
            tiers[i] += 1
            order.append(ids[i])
            steps.append({"ability": ids[i], "tier": tiers[i], "level": lvl, "net_worth": nw})
    if q:
        raise RuntimeError(f"{hero.name}: {len(q)} upgrades left after the last level")
    return order, steps


def skill_job(args):
    hero_id, use_published = args
    BO.USE_PUBLISHED = use_published
    path = os.path.join(JOBS, f"{hero_id}.json")
    if os.path.exists(path):
        return path, "skip"
    t0 = time.time()
    hero = S.G().hero(hero_id)
    res = BO.search_results(hero_id)
    budgets = sorted(res)
    popular = list(popular_ability_order(hero_id))
    if not budgets or not popular or len(hero.abilities) != 4:
        return path, f"{hero.name}: no damage search results or popular order, skipped"
    sc = Scorer(hero_id, res)
    out = {"hero_id": hero_id, "hero": hero.name,
           "abilities": [{"id": a.id, "name": a.name, "ultimate": bool(a.ultimate)} for a in hero.abilities],
           "popular_order": popular, "objectives": {}}
    for obj in D.WINDOWS:
        out["objectives"][obj] = plan(sc, hero, obj, budgets, popular)
    out.update({"fights": sc.fights, "seconds": round(time.time() - t0, 1)})
    os.makedirs(JOBS, exist_ok=True)
    json.dump(out, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    o = out["objectives"]["fight_15s"]["budgets"]
    gains = " ".join(f"{int(b) // 1000}k {r['damage'] / r['popular_damage'] - 1:+.1%}" for b, r in o.items())
    return path, f"{hero.name}: 15 s damage vs popular order {gains} ({sc.fights} fights, {out['seconds']}s)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--heroes", default="")
    ap.add_argument("--budgets", default="", help="ignored (every budget the damage search has); for run_shard.py")
    ap.add_argument("--use-published", action="store_true", help="read out/heroes when work/jobs is missing")
    a = ap.parse_args()
    g = S.G()
    heroes = [g.hero(int(h) if h.isdigit() else h).id for h in a.heroes.split(",") if h] or sorted(g.heroes)
    os.makedirs(JOBS, exist_ok=True)
    with Pool(a.workers) as p:
        for path, msg in p.imap_unordered(skill_job, [(h, a.use_published) for h in heroes]):
            print(time.strftime("%H:%M:%S"), msg, flush=True)


if __name__ == "__main__":
    main()
