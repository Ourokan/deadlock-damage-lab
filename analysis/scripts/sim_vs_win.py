"""Does the overall score rank items like real wins do? Sim marginal item value vs real per-hero win edge.

For each hero at a budget: the popular Phantom+ build + one item (components consumed) vs the popular build, in the
overall score with the real win-edge blend OFF (overall_search.WIN_K = 0, so the check is independent of the edges
it is compared with), as score gain per 1000 souls of the item. Compared with the item's per-hero real edge
(analysis/out/hero_item_edge.json, Ritualist+, same-slot same-tier, shrunk). Items the popular build holds and
movement items (their real value is in movement_value already) are skipped.

Prints Pearson / Spearman over every (hero, item) pair, over items that deal damage (kill_weight.json rows) and
per-item mean sim gain vs mean edge, over (hero, item) pairs with the sim gain centred on the hero's other items of
the same slot and tier (as the edge is), with the overall score's KILL_WEIGHT and DEATH_COST as set (--no-kill to turn the
kill weight off, --elasticity for DAMAGE_ELASTICITY, --focus-gamma for FOCUS_GAMMA, --farm-gamma for FARM_GAMMA, --deaths-per-minute for death ratios per minute, --death to turn the opt-in death cost on, --bounty for DEATH_BOUNTY, --no-death-rate to
turn the real death rate value off, --fight-rate for the opt-in fight rate). Rows in --out also carry the popular build's and the
item build's sim death chance (overall_search.death_chance), for analysis/scripts/death_check.py, then health lost
per fight and max health of both builds and both scores (for offline fight-rate variants), the item cost and both builds' damage before death.
Earlier ad hoc check: Pearson 0.05 over 16 heroes x 27k/37k (build_win_check.md). This script, all heroes at 27k
(2026-10-24): all pairs 0.10 without the kill weight, 0.14 with it.

usage: python3 analysis/scripts/sim_vs_win.py [--budgets 27000] [--heroes all] [--workers 4] [--no-kill] [--death]
       [--bounty 1] [--out FILE]
"""
import argparse
import json
import os
import statistics
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "damage", "scripts"))
import game_path as GP  # noqa: E402
import overall_search as O  # noqa: E402

S = O.S
EDGE = os.path.join(ROOT, "analysis", "out", "hero_item_edge.json")
KILL = os.path.join(ROOT, "sim", "data", "kill_weight.json")


def setup(kill, death=False, bounty=None, death_rate=True, fight_rate=False, elasticity=None, focus=None, farm=None,
          per_ka=True):
    O.WIN_K = 0.0
    O.DEATH_PER_KA = per_ka
    if farm is not None:
        O.FARM_GAMMA = farm
    if focus is not None:
        O.FOCUS_GAMMA = focus
    if elasticity is not None:
        O.DAMAGE_ELASTICITY = elasticity
    O.KILL_WEIGHT = kill
    O.DEATH_COST = death
    O.DEATH_RATE = death_rate
    O.FIGHT_RATE = fight_rate
    if bounty is not None:
        O.DEATH_BOUNTY = bounty
    O._phases()


def job(args):
    hero, b, kill, death, bounty, death_rate, fight_rate, elasticity, focus, farm, per_ka = args
    setup(kill, death, bounty, death_rate, fight_rate, elasticity, focus, farm, per_ka)
    with open(EDGE) as f:
        edges = json.load(f)["heroes"].get(str(hero), {})
    O.movement_value(())
    moving = O._move[2]
    pools = S.load_pools(b)
    ev = GP.make_evaluator(hero, b, pools)
    pop = S.popular_build(hero, GP.item_budget(b), pools)
    base = ev.run(pop)
    dmg_pop = ev.run(pop, detail=True)["damage_before_death"]
    pd_pop = ev.pd_pop["F"]
    fe = ev.fight if isinstance(ev, O.MixEvaluator) else ev   # MixEvaluator: its fight part
    loss_pop, hp_pop = getattr(fe, "loss_pop", {}).get("F", 0.0), O.build_stats(hero, pop, b)["max_hp"]
    g = S.G()
    out = []
    for i, e in edges.items():
        i = int(i)
        if i not in g.items or i in pop or i in moving:
            continue
        it = g.items[i]
        if it.cost > GP.item_budget(b):
            continue
        d = ev.run(GP.with_item(pop, i), detail=True)
        sc = d["score"]
        out.append((hero, b, it.name, (sc - base) / it.cost * 1000, e[0], e[1], pd_pop, d["death_chance"],
                    loss_pop, d.get("hp_lost_per_fight", 0.0), hp_pop, O.build_stats(hero, GP.with_item(pop, i), b)["max_hp"],
                    base, sc, it.cost, dmg_pop, d["damage_before_death"]))
    return out


def pearson(x, y):
    mx, my = statistics.mean(x), statistics.mean(y)
    sx = sum((a - mx) ** 2 for a in x) ** 0.5
    sy = sum((b - my) ** 2 for b in y) ** 0.5
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else 0.0


def ranks(v):
    order = sorted(range(len(v)), key=lambda k: v[k])
    r = [0.0] * len(v)
    for pos, k in enumerate(order):
        r[k] = pos
    return r


def spearman(x, y):
    return pearson(ranks(x), ranks(y))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budgets", default="27000")
    ap.add_argument("--heroes", default="")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--no-kill", action="store_true")
    ap.add_argument("--death", action="store_true", help="turn the opt-in death cost on")
    ap.add_argument("--bounty", type=float, default=None, help="overall_search.DEATH_BOUNTY")
    ap.add_argument("--no-death-rate", action="store_true", help="turn the real death rate value off")
    ap.add_argument("--fight-rate", action="store_true", help="turn the opt-in fight rate (HP budget) on")
    ap.add_argument("--elasticity", type=float, default=None, help="overall_search.DAMAGE_ELASTICITY (1 = old score)")
    ap.add_argument("--focus-gamma", type=float, default=None, help="overall_search.FOCUS_GAMMA (0 = no focus cost)")
    ap.add_argument("--farm-gamma", type=float, default=None, help="overall_search.FARM_GAMMA (0 = no farm value)")
    ap.add_argument("--deaths-per-minute", action="store_true",
                    help="real death ratios per minute, not per kills + assists (DEATH_PER_KA off)")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    g = S.G()
    heroes = [g.hero(int(h) if h.isdigit() else h).id for h in a.heroes.split(",") if h] or sorted(g.heroes)
    jobs = [(h, int(b), not a.no_kill, a.death, a.bounty, not a.no_death_rate, a.fight_rate, a.elasticity,
             a.focus_gamma, a.farm_gamma, not a.deaths_per_minute)
            for b in a.budgets.split(",") for h in heroes]
    rows = []
    with Pool(a.workers) as p:
        for r in p.imap_unordered(job, jobs):
            rows += r
    with open(KILL) as f:
        dmg_items = set(json.load(f)["items"])
    print(f"kill weight {'off' if a.no_kill else 'on'}, death cost {'on' if a.death else 'off'}, death rate "
          f"{'off' if a.no_death_rate else ('per minute' if a.deaths_per_minute else 'per kills + assists')}, fight rate {'on' if a.fight_rate else 'off'}"
          f"{'' if a.bounty is None else f' (bounty {a.bounty:g})'}, damage elasticity "
          f"{O.DAMAGE_ELASTICITY if a.elasticity is None else a.elasticity:g}, focus cost "
          f"{O.FOCUS_GAMMA if a.focus_gamma is None else a.focus_gamma:g}, farm value "
          f"{O.FARM_GAMMA if a.farm_gamma is None else a.farm_gamma:g}; {len(rows)} (hero, item) pairs")
    for label, rs in (("all items", rows), ("damage items", [r for r in rows if r[2] in dmg_items]),
                      ("edges clear of noise", [r for r in rows if abs(r[4]) > 1.96 * r[5]])):
        x, y = [r[3] for r in rs], [r[4] for r in rs]
        print(f"  {label:22s} n {len(rs):5d}  Pearson {pearson(x, y):+.3f}  Spearman {spearman(x, y):+.3f}")
    # the real edge is against same-slot same-tier items, so also compare the sim gain against the hero's other
    # items of that slot and tier (a tier whose sim favourites lose real games drags its other items down otherwise)
    slot = {it.name: (it.slot, it.tier) for it in g.items.values()}
    grp = {}
    for r in rows:
        grp.setdefault((r[0], *slot[r[2]]), []).append(r)
    cen = [(r[3] - statistics.mean(q[3] for q in rs), r[4]) for rs in grp.values() if len(rs) > 1 for r in rs]
    print(f"  {'within slot and tier':22s} n {len(cen):5d}  Pearson {pearson(*zip(*cen)):+.3f}  Spearman "
          f"{spearman(*zip(*cen)):+.3f}")
    by = {}
    for r in rows:
        by.setdefault(r[2], []).append(r)
    items = [(n, statistics.mean(r[3] for r in rs), statistics.mean(r[4] for r in rs), len(rs))
             for n, rs in by.items() if len(rs) >= 5]
    print(f"  per item (mean over heroes) n {len(items)}  Pearson "
          f"{pearson([i[1] for i in items], [i[2] for i in items]):+.3f}  Spearman "
          f"{spearman([i[1] for i in items], [i[2] for i in items]):+.3f}")
    print("  top sim gain per 1000 souls (mean over heroes) | real edge:")
    for n, s, e, k in sorted(items, key=lambda i: -i[1])[:15]:
        print(f"    {n:24s} {s:+.4f}  {e:+.2f} pt  ({k} heroes)")
    if a.out:
        with open(a.out, "w") as f:
            json.dump(rows, f)


if __name__ == "__main__":
    main()
