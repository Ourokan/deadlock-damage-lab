"""Does the overall score rank items like real wins do? Sim marginal item value vs real per-hero win edge.

For each hero at a budget: the popular Phantom+ build + one item (components consumed) vs the popular build, in the
overall score with the real win-edge blend OFF (overall_search.WIN_K = 0, so the check is independent of the edges
it is compared with), as score gain per 1000 souls of the item. Compared with the item's per-hero real edge
(analysis/out/hero_item_edge.json, Ritualist+, same-slot same-tier, shrunk). Items the popular build holds and
movement items (their real value is in movement_value already) are skipped.

Prints Pearson / Spearman over every (hero, item) pair, over items that deal damage (kill_weight.json rows) and
per-item mean sim gain vs mean edge, with the overall score's KILL_WEIGHT as set (--no-kill to turn it off).
Before the kill weight (2026-10-24): Pearson 0.05 over 16 heroes x 27k/37k (build_win_check.md).

usage: python3 analysis/scripts/sim_vs_win.py [--budgets 27000] [--heroes all] [--workers 4] [--no-kill] [--out FILE]
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


def setup(kill):
    O.WIN_K = 0.0
    O.KILL_WEIGHT = kill
    O._phases()


def job(args):
    hero, b, kill = args
    setup(kill)
    with open(EDGE) as f:
        edges = json.load(f)["heroes"].get(str(hero), {})
    O.movement_value(())
    moving = O._move[2]
    pools = S.load_pools(b)
    ev = GP.make_evaluator(hero, b, pools)
    pop = S.popular_build(hero, GP.item_budget(b), pools)
    base = ev.run(pop)
    g = S.G()
    out = []
    for i, e in edges.items():
        i = int(i)
        if i not in g.items or i in pop or i in moving:
            continue
        it = g.items[i]
        if it.cost > GP.item_budget(b):
            continue
        sc = ev.run(GP.with_item(pop, i))
        out.append((hero, b, it.name, (sc - base) / it.cost * 1000, e[0], e[1]))
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
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    g = S.G()
    heroes = [g.hero(int(h) if h.isdigit() else h).id for h in a.heroes.split(",") if h] or sorted(g.heroes)
    jobs = [(h, int(b), not a.no_kill) for b in a.budgets.split(",") for h in heroes]
    rows = []
    with Pool(a.workers) as p:
        for r in p.imap_unordered(job, jobs):
            rows += r
    with open(KILL) as f:
        dmg_items = set(json.load(f)["items"])
    print(f"kill weight {'off' if a.no_kill else 'on'}; {len(rows)} (hero, item) pairs")
    for label, rs in (("all items", rows), ("damage items", [r for r in rows if r[2] in dmg_items]),
                      ("edges clear of noise", [r for r in rows if abs(r[4]) > 1.96 * r[5]])):
        x, y = [r[3] for r in rs], [r[4] for r in rs]
        print(f"  {label:22s} n {len(rs):5d}  Pearson {pearson(x, y):+.3f}  Spearman {spearman(x, y):+.3f}")
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
