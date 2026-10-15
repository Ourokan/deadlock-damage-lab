"""Survival search: for tank heroes, the item builds that stay alive longest against real enemy builds while
keeping the hero's core items and most of its damage.

Survival: survival.survive() against every typical real build at the same net worth (search/ "F" pool, one per hero,
weighted by how often the hero reaches that worth). Both sides fight normally at ranked median aim; the enemy never
dies and its damage is multiplied by FOCUS (2 = focused by two enemies of that build; at 1 most tanks outlive a 60 s
cap, so builds can't be told apart). Score per fight = seconds alive (cap 60) + 5 x HP fraction left if alive.
Build score = weighted mean over the pool.

Core items: items at least CORE_RATE of real players of that hero own at that budget. They stay in every build
(or are upgraded into an item that contains them).

Damage: dummy damage by 15 s (damage/ tool, same dummy as the damage search) must stay within MARGIN of the most
popular real build's. Searched for several margins; one search per margin, shared cache.

Search per margin: start from the most popular real build. Each round, value every candidate item added and every
non-core item removed on the 16 most played opponents, propose add / 1-for-1 / 2-for-1 / 1-for-2 moves by predicted
gain, check the best 6 that pass the damage rule on the full pool, move to the best. Up to ROUNDS rounds.

usage: python3 scripts/survival_search.py [--workers 4] [--heroes Abrams,Bebop] [--budgets 27000] [--focus 2]
Writes work/jobs/<hero_id>_<budget>.json (resumes); scripts/export.py builds out/.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "..", "sim"))
sys.path.insert(0, os.path.join(ROOT, "..", "search", "scripts"))
sys.path.insert(0, os.path.join(ROOT, "..", "damage", "scripts"))
sys.path.insert(0, ROOT)

import search as S  # noqa: E402
from build_pool import BUDGETS, item_budget  # noqa: E402
import dummy_search as D  # noqa: E402
from survival import survive  # noqa: E402

MAX_TIME = 60.0
FOCUS = 2.0
REPORT_FOCUS = (1.0, 2.0, 3.0)
CORE_RATE = 0.5
MARGINS = (0.0, 0.10, 0.25)
DMG_OBJ = "fight_15s"
ROUNDS = 6
PROPOSALS_S = 30
PROPOSALS_F = 6
MIN_GAIN = 0.1           # seconds
TOP_OUT = 10
N_TANKS = 10


def tank_heroes(usage):
    """Heroes whose real players put the largest share of item souls into vitality items (18k-37k budgets)."""
    g = S.G()
    share = {}
    for b in ("18000", "27000", "37000"):
        for h, d in usage[b].items():
            if int(h) not in g.heroes:
                continue
            tot = vit = 0.0
            for i, c in d.items():
                if i == "_n" or int(i) not in g.items:
                    continue
                it = g.items[int(i)]
                tot += c * it.cost
                vit += c * it.cost * (it.slot == "vitality")
            share.setdefault(int(h), []).append(vit / tot if tot else 0)
    share = {h: sum(v) / len(v) for h, v in share.items()}
    return sorted(share, key=lambda h: -share[h]), share


class Evaluator:
    def __init__(self, hero, budget, pools, dummy_hp, focus):
        self.h, self.souls, self.pools, self.hp, self.focus = hero, budget, pools, dummy_hp, focus
        self.cache, self.dcache = {}, {}
        self.fights = 0

    def rows(self, items, pool="F", focus=None):
        focus = focus or self.focus
        key = (tuple(sorted(items)), pool, focus)
        if key not in self.cache:
            out = []
            for oh, oit, w in self.pools[pool]:
                r = survive(self.h, key[0], self.souls, oh, oit, max_time=MAX_TIME, focus=focus)
                out.append((oh, w, r))
                self.fights += 1
            self.cache[key] = out
        return self.cache[key]

    def score(self, items, pool="F", focus=None):
        rows = self.rows(items, pool, focus)
        tw = sum(w for _, w, _ in rows)
        return sum(w * fight_score(r) for _, w, r in rows) / tw

    def damage(self, items):
        k = tuple(sorted(items))
        if k not in self.dcache:
            self.dcache[k] = D.run_dummy(self.h, k, self.souls, self.hp)
        return self.dcache[k]


def fight_score(r):
    left = 0.0 if not r["survived"] else max(0.0, r["final_hp"]) / r["max_hp"]
    return r["time_alive"] + 5.0 * left


def keeps_core(items, core):
    g = S.G()
    have = set(items)
    for i in items:
        have |= S.component_ids(g.items[i])
    return core <= have


def local_search(ev, start, core, min_dmg, limit, cand, log, tag):
    g = S.G()
    ok = lambda b: S.valid(list(b), limit) and keeps_core(b, core) and ev.damage(b)[0][DMG_OBJ] >= min_dmg
    cur = list(start)
    cur_v = ev.score(cur)
    for rnd in range(ROUNDS):
        base_s = ev.score(cur, "S")
        add_v = {}
        for j in cand:
            if j in cur:
                continue
            trial = [i for i in cur if j not in S.component_ids(g.items[i]) and i not in S.component_ids(g.items[j])]
            add_v[j] = ev.score(trial + [j], "S") - base_s
        removable = [i for i in cur if keeps_core([x for x in cur if x != i], core)]
        rem_v = {i: base_s - ev.score([x for x in cur if x != i], "S") for i in removable}
        adds = sorted(add_v, key=lambda j: -add_v[j])[:20]
        adds += [j for j in sorted(add_v, key=lambda j: -add_v[j] / g.items[j].cost)[:20] if j not in adds]
        props = {}

        def propose(remove, add):
            new = [i for i in cur if i not in remove]
            for j in add:
                new = [i for i in new if i not in S.component_ids(g.items[j])]
                new.append(j)
            k = tuple(sorted(new))
            if k not in props and S.valid(new, limit) and keeps_core(new, core):
                props[k] = sum(add_v.get(j, 0) for j in add) - sum(rem_v.get(i, 0) for i in remove)

        for j in adds:
            propose([], [j])
            for i in removable:
                propose([i], [j])
        cheap = sorted(removable, key=lambda i: rem_v[i] / g.items[i].cost)[:6]
        for x in range(len(cheap)):
            for y in range(x + 1, len(cheap)):
                for j in adds[:20]:
                    propose([cheap[x], cheap[y]], [j])
        for i in cheap[:4] + [None]:
            for x in range(min(10, len(adds))):
                for y in range(x + 1, min(10, len(adds))):
                    propose([i] if i else [], [adds[x], adds[y]])
        ranked = sorted(props, key=lambda k: -props[k])[:PROPOSALS_S * 3]
        ranked = [k for k in ranked if ev.damage(k)[0][DMG_OBJ] >= min_dmg][:PROPOSALS_S]
        ranked = sorted(ranked, key=lambda k: -ev.score(k, "S"))[:PROPOSALS_F]
        best = max(ranked, key=lambda k: ev.score(k), default=None)
        if best is None:
            break
        bv = ev.score(best)
        log(f"  {tag} round {rnd + 1}: {cur_v:.2f} -> {bv:.2f} s ({len(props)} proposals, {ev.fights} fights)")
        if bv <= cur_v:
            break
        gain = bv - cur_v
        cur, cur_v = list(best), bv
        if gain < MIN_GAIN:
            break
    return cur


def job(args):
    hero, budget, focus = args
    path = os.path.join(ROOT, "work", "jobs", f"{hero}_{budget}.json")
    if os.path.exists(path):
        return path, "skip"
    g = S.G()
    t0 = time.time()
    pools = S.load_pools(budget)
    limit = item_budget(budget)
    hp = D.dummy_hp_for(pools, budget)
    ev = Evaluator(hero, budget, pools, hp, focus)
    cand = S.candidates(limit, pools["usage"])
    popular = S.popular_build(hero, limit, pools)
    u = pools["usage"][str(hero)]
    rate = {int(i): c / u["_n"] for i, c in u.items() if i != "_n"}
    core = {i for i in popular if rate.get(i, 0) >= CORE_RATE}
    base_dmg = ev.damage(popular)[0][DMG_OBJ]
    lines = []
    bests = {}
    for m in MARGINS:
        bests[m] = local_search(ev, popular, core, base_dmg * (1 - m), limit, cand, lines.append, f"margin {m:.0%}")

    def describe(items):
        items = tuple(sorted(items))
        dmg, src = ev.damage(items)
        out = {"items": list(items), "cost": S.cost(items), "score": round(ev.score(items), 2),
               "damage": {k: round(v, 1) for k, v in dmg.items()},
               "damage_vs_popular": round(dmg[DMG_OBJ] / base_dmg - 1, 4)}
        for f in REPORT_FOCUS:
            rows = ev.rows(items, "F", f)
            tw = sum(w for _, w, _ in rows)
            out[f"focus_{f:g}"] = {
                "time_alive": round(sum(w * r["time_alive"] for _, w, r in rows) / tw, 2),
                "survived_60s": round(sum(w * r["survived"] for _, w, r in rows) / tw, 4),
                "damage_taken": round(sum(w * r["damage_taken"] for _, w, r in rows) / tw, 1),
                "healing": round(sum(w * r["healing"] for _, w, r in rows) / tw, 1)}
        return out

    res = {"hero_id": hero, "hero": g.hero(hero).name, "budget": budget, "item_budget": limit, "focus": focus,
           "max_time": MAX_TIME, "dummy_hp": hp, "core_rate": CORE_RATE, "core": sorted(core),
           "popular": describe(popular), "popular_damage_15s": base_dmg, "margins": {}}
    for m in MARGINS:
        floor = base_dmg * (1 - m)
        pool = [k for (k, p, f) in ev.cache if p == "F" and f == focus and S.valid(list(k), limit)
                and keeps_core(k, core) and ev.damage(k)[0][DMG_OBJ] >= floor]
        ranked = sorted(pool, key=lambda k: -ev.score(k))[:TOP_OUT]
        best = list(ranked[0])
        bv = ev.score(best)
        rem = {}
        for i in best:
            if i not in core:
                rem[str(i)] = round(bv - ev.score([x for x in best if x != i]), 2)
        matchups = {str(oh): {"time_alive": r["time_alive"], "survived": r["survived"]}
                    for oh, _, r in ev.rows(best, "F")}
        res["margins"][f"{m:g}"] = {"min_damage_15s": round(floor, 1), "builds": [describe(k) for k in ranked],
                                    "best_item_removal_loss_s": rem, "best_matchups": matchups,
                                    "popular_matchups": {str(oh): {"time_alive": r["time_alive"],
                                                                   "survived": r["survived"]}
                                                         for oh, _, r in ev.rows(popular, "F")}}
    res.update({"fights": ev.fights, "seconds": round(time.time() - t0, 1), "candidates": len(cand), "log": lines})
    json.dump(res, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    b = res["margins"]["0.1"]["builds"][0]
    return path, (f"{res['hero']} {budget}: alive {res['popular']['score']:.1f}s -> {b['score']:.1f}s at "
                  f"{b['damage_vs_popular']:+.0%} damage ({ev.fights} fights, {res['seconds']}s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--heroes", default="")
    ap.add_argument("--budgets", default="")
    ap.add_argument("--focus", type=float, default=FOCUS)
    a = ap.parse_args()
    g = S.G()
    usage = json.load(open(os.path.join(ROOT, "..", "search", "work", "item_usage.json")))
    order, share = tank_heroes(usage)
    heroes = [g.hero(h).id for h in a.heroes.split(",") if h] or order[:N_TANKS]
    print("heroes:", ", ".join(f"{g.hero(h).name} ({share[h]:.0%} vitality)" for h in heroes), flush=True)
    budgets = [int(b) for b in a.budgets.split(",") if b] or BUDGETS
    os.makedirs(os.path.join(ROOT, "work", "jobs"), exist_ok=True)
    jobs = [(h, b, a.focus) for b in budgets for h in heroes]
    with Pool(a.workers) as p:
        for path, msg in p.imap_unordered(job, jobs):
            print(time.strftime("%H:%M:%S"), msg, flush=True)


if __name__ == "__main__":
    main()
