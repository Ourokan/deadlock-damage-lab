"""Dummy damage search: the item builds that deal the most damage per hero and souls budget against a target dummy.

Separate from the duel search (/mnt/project-files/search): nothing shoots back, nobody wins. The question is only
"which items turn these souls into the most damage on this hero".

Dummy: never acts, has no resists and no items, cannot die (lethal damage refills it, like a training dummy), and
has the weighted median max HP of the real typical builds at that budget (items like Tankbuster or Spirit Burn
scale off target HP, so a realistic pool matters). Damage is counted before it hits HP, so overkill counts.

Attacker: hero_default_skill (ranked median hero accuracy and headshot rate, real ability landing and melee rates),
abilities on cooldown, actives used, same item budget as the duel search (the share of net worth real players hold
in items). Distance: the hero's real median engagement distance.

Three objectives from the same 30 s run: damage dealt by 5 s (burst), 15 s (fight) and 30 s (sustained).
Search per objective: start from the most popular real build, then repeat up to ROUNDS times: value every candidate
item added and every owned item removed, propose 1-for-1, 2-for-1, 1-for-2 and add moves by predicted gain, and move
to the best real improvement. All evaluations are cached, so the three searches share fights.

usage: python3 scripts/dummy_search.py [--workers 4] [--heroes Haze] [--budgets 27000] [--aim p50]
Writes work/jobs/<hero_id>_<budget>.json (resumes), then scripts/export.py builds out/.
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SEARCH = os.path.join(ROOT, "..", "search", "scripts")
sys.path.insert(0, os.path.join(ROOT, "..", "sim"))
sys.path.insert(0, SEARCH)

from deadsim import compute_stats  # noqa: E402
from build_pool import BUDGETS, item_budget  # noqa: E402
import search as S  # noqa: E402
sys.path.insert(0, ROOT)
from dummy import Dummy, damage_test  # noqa: E402

T_MAX = 30.0
WINDOWS = {"burst_5s": 5.0, "fight_15s": 15.0, "sustained_30s": 30.0}
ROUNDS = 8
MIN_GAIN = 0.002          # relative gain below which a search stops
TOP_OUT = 10
AIM = "p50"
DUMMY_HERO = "Haze"       # only its base hitbox is used: no abilities, items or resists


def run_dummy(hero, items, souls, dummy_hp):
    """Damage dealt at each window, and the damage split by source over 30 s (dummy.damage_test)."""
    r = damage_test(hero, items, souls=souls, dummy=Dummy(hp=dummy_hp, bullet_resist=0, spirit_resist=0,
                                                          melee_resist=0, hero=DUMMY_HERO),
                    aim=AIM, marks=tuple(WINDOWS.values()))
    return {k: r["damage"][f"{t:g}s"] for k, t in WINDOWS.items()}, r["sources"]


class Evaluator:
    def __init__(self, hero, souls, dummy_hp):
        self.hero, self.souls, self.hp = hero, souls, dummy_hp
        self.cache = {}
        self.fights = 0

    def run(self, items):
        k = tuple(sorted(items))
        if k not in self.cache:
            self.cache[k] = run_dummy(self.hero, k, self.souls, self.hp)
            self.fights += 1
        return self.cache[k]

    def val(self, items, obj):
        return self.run(items)[0][obj]


def dummy_hp_for(pools, souls):
    """Weighted median max HP of the typical real builds at this budget."""
    hp = sorted((compute_stats(h, list(it), souls=souls).max_health, w) for h, it, w in pools["F"])
    tot, acc = sum(w for _, w in hp), 0.0
    for v, w in hp:
        acc += w
        if acc >= tot / 2:
            return round(v)
    return round(statistics.median(v for v, _ in hp))


def local_search(ev, start, obj, limit, cand, log):
    g = S.G()
    cur = list(start)
    cur_v = ev.val(cur, obj)
    for rnd in range(ROUNDS):
        add_v = {}
        for j in cand:
            if j in cur:
                continue
            trial = [i for i in cur if j not in S.component_ids(g.items[i]) and i not in S.component_ids(g.items[j])]
            add_v[j] = ev.val(trial + [j], obj) - cur_v
        rem_v = {i: cur_v - ev.val([x for x in cur if x != i], obj) for i in cur}
        adds = sorted(add_v, key=lambda j: -add_v[j])[:25]
        props = set()

        def propose(remove, add):
            new = [i for i in cur if i not in remove]
            for j in add:
                new = [i for i in new if i not in S.component_ids(g.items[j])]
                new.append(j)
            if S.valid(new, limit):
                props.add(tuple(sorted(new)))

        for j in adds:
            propose([], [j])
            for i in cur:
                propose([i], [j])
        cheap = sorted(cur, key=lambda i: rem_v[i] / g.items[i].cost)[:6]
        for x in range(len(cheap)):
            for y in range(x + 1, len(cheap)):
                for j in adds[:12]:
                    propose([cheap[x], cheap[y]], [j])
        for i in cheap[:4] + [None]:
            for x in range(min(10, len(adds))):
                for y in range(x + 1, min(10, len(adds))):
                    propose([i] if i else [], [adds[x], adds[y]])
        best = max(props, key=lambda p: ev.val(p, obj), default=None)
        if best is None:
            break
        bv = ev.val(best, obj)
        log(f"  {obj} round {rnd + 1}: {cur_v:.0f} -> {bv:.0f} ({len(props)} proposals, {ev.fights} fights)")
        if bv <= cur_v:
            break
        gain = (bv - cur_v) / max(1.0, cur_v)
        cur, cur_v = list(best), bv
        if gain < MIN_GAIN:
            break
    return cur


def item_table(ev, base, obj, cand):
    """Damage gained per 1000 souls when each candidate item is added to `base` (component swaps handled)."""
    g = S.G()
    b = ev.val(base, obj)
    out = {}
    for j in cand:
        if j in base:
            continue
        trial = [i for i in base if j not in S.component_ids(g.items[i]) and i not in S.component_ids(g.items[j])]
        extra = g.items[j].cost - sum(g.items[i].cost for i in base if i not in trial)
        gain = ev.val(trial + [j], obj) - b
        out[str(j)] = {"gain": round(gain, 1), "per_1000_souls": round(gain / max(1, extra) * 1000, 1)}
    return out


def dummy_job(args):
    hero, budget = args
    path = os.path.join(ROOT, "work", "jobs", f"{hero}_{budget}.json")
    if os.path.exists(path):
        return path, "skip"
    g = S.G()
    t0 = time.time()
    pools = S.load_pools(budget)
    limit = item_budget(budget)
    hp = dummy_hp_for(pools, budget)
    ev = Evaluator(hero, budget, hp)
    cand = S.candidates(limit, pools["usage"])
    popular = S.popular_build(hero, limit, pools)
    lines = []
    bests = {obj: local_search(ev, popular, obj, limit, cand, lines.append) for obj in WINDOWS}

    def describe(items):
        marks, src = ev.run(items)
        return {"items": sorted(items), "cost": S.cost(items),
                "damage": {k: round(v, 1) for k, v in marks.items()},
                "dps": {k: round(v / WINDOWS[k], 1) for k, v in marks.items()},
                "sources_30s": {k: round(v, 1) for k, v in sorted(src.items(), key=lambda x: -x[1])}}

    res = {"hero_id": hero, "hero": g.hero(hero).name, "budget": budget, "item_budget": limit, "dummy_hp": hp,
           "aim": AIM, "popular": describe(popular), "objectives": {}}
    for obj in WINDOWS:
        ranked = sorted((k for k in ev.cache if S.valid(list(k), limit)), key=lambda k: -ev.cache[k][0][obj])[:TOP_OUT]
        best = list(ranked[0])
        base = ev.val(best, obj)
        res["objectives"][obj] = {
            "builds": [describe(k) for k in ranked],
            "best_item_removal_loss": {str(i): round(base - ev.val([x for x in best if x != i], obj), 1) for i in best},
            "item_value_on_popular": item_table(ev, popular, obj, cand),
        }
    res.update({"fights": ev.fights, "seconds": round(time.time() - t0, 1), "candidates": len(cand), "log": lines})
    json.dump(res, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    b = res["objectives"]["fight_15s"]["builds"][0]["damage"]["fight_15s"]
    return path, f"{res['hero']} {budget}: 15s damage best {b:.0f} vs popular {res['popular']['damage']['fight_15s']:.0f}" \
                 f" ({ev.fights} fights, {res['seconds']}s)"


def main():
    global AIM
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--heroes", default="")
    ap.add_argument("--budgets", default="")
    ap.add_argument("--aim", default="p50")
    a = ap.parse_args()
    AIM = a.aim
    g = S.G()
    heroes = [g.hero(h).id for h in a.heroes.split(",") if h] or sorted(g.heroes)
    budgets = [int(b) for b in a.budgets.split(",") if b] or BUDGETS
    os.makedirs(os.path.join(ROOT, "work", "jobs"), exist_ok=True)
    jobs = [(h, b) for b in budgets for h in heroes]
    with Pool(a.workers) as p:
        for path, msg in p.imap_unordered(dummy_job, jobs):
            print(time.strftime("%H:%M:%S"), msg, flush=True)


if __name__ == "__main__":
    main()
