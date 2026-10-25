"""Marginal value of single items in the overall / lane score: popular real build + item vs popular build.

usage: python3 scripts/item_probe.py --heroes Haze,Infernus --budgets 6000,18000 --items "Healbane,Healing Booster"
Prints score gain per 1000 souls of the item (cost of the item's own tier, components not consumed).
"""
import argparse
import os
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import game_path as GP  # noqa: E402
import overall_search as O  # noqa: E402

S = O.S


def probe(args):
    hero, b, names = args
    O._phases()
    pools = S.load_pools(b)
    ev = GP.make_evaluator(S.G().hero(hero).id, b, pools)
    pop = S.popular_build(S.G().hero(hero).id, GP.item_budget(b), pools)
    base = ev.run(pop)
    out = []
    for n in names:
        it = S.G().item(n)
        if it.id in pop:
            out.append((n, None, None))
            continue
        sc = ev.run(GP.with_item(pop, it.id))
        out.append((n, sc - base, (sc - base) / it.cost * 1000))
    return hero, b, base, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--heroes", default="Haze,Infernus,Abrams,Seven")
    ap.add_argument("--budgets", default="6000,18000,37000")
    ap.add_argument("--items", default="Healing Booster,Radiant Regeneration,Restorative Shot,Counterspell,Healbane,"
                                       "Tankbuster,Rebuttal,Dispel Magic,Opening Rounds,Monster Rounds,Extra Regen,"
                                       "Extra Health,Extra Spirit,Headshot Booster")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    names = a.items.split(",")
    jobs = [(h, int(b), names) for h in a.heroes.split(",") for b in a.budgets.split(",")]
    with Pool(a.workers) as p:
        for hero, b, base, out in p.imap(probe, jobs):
            print(f"== {hero} {b}")
            for n, d, per in out:
                print(f"   {n:22s} " + ("held by popular" if d is None else f"{d:+.3f}  ({per:+.4f} per 1000 souls)"))


if __name__ == "__main__":
    main()
