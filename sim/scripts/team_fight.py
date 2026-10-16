"""Run a team fight (2v2, 3v3) from the command line. Run from sim/:

    python3 scripts/team_fight.py --a "Haze: Rapid Rounds, Toxic Bullets" --a "Dynamo: Healing Nova, Rescue Beam" \
        --b "Abrams: Extra Health" --b "Infernus: Extra Spirit" --souls 20000
    python3 scripts/team_fight.py ... --value 2 "Healing Nova"           # what A's 2nd hero's item is worth to A
    python3 scripts/team_fight.py ... --value 2 "Healing Nova" --replace "Extra Health"
    python3 scripts/team_fight.py --support 27000                         # support items ranked in standard 3v3s

A hero with no ":" gets the most popular real build at that net worth (damage/out). --json prints the full result.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from deadsim import Loadout  # noqa: E402
from deadsim.accuracy import hero_default_skill  # noqa: E402
from deadsim.data import game  # noqa: E402
from deadsim.team import team_fight, team_item_value  # noqa: E402

POPULAR = os.path.join(HERE, "..", "..", "damage", "out", "heroes")


def popular_items(hero, souls):
    G = game()
    h = G.hero(hero)
    try:
        d = json.load(open(os.path.join(POPULAR, f"{h.id}.json")))
    except OSError:
        return []
    budgets = sorted(d["budgets"], key=lambda b: abs(int(b) - souls))
    return [G.item(i).name for i in d["budgets"][budgets[0]]["popular"]["items"]] if budgets else []


def parse(spec, souls, aim):
    hero, _, rest = spec.partition(":")
    hero = game().hero(hero.strip()).name
    items = [x.strip() for x in rest.split(",") if x.strip()] if _ else popular_items(hero, souls)
    return Loadout(hero, items, souls=souls, skill=hero_default_skill(hero, aim))


# Support items scored by --support
SUPPORT_ITEMS = ["Healing Nova", "Rescue Beam", "Divine Barrier", "Guardian Ward", "Restorative Locket", "Heroic Aura",
                 "Hunter's Aura", "Healing Booster"]
LINEUPS = [  # (team A, team B); A's last hero carries the item
    (["Haze", "Abrams", "Dynamo"], ["Infernus", "Seven", "Lash"]),
    (["Wraith", "McGinnis", "Kelvin"], ["Haze", "Abrams", "Ivy"]),
    (["Vindicta", "Mo & Krill", "Ivy"], ["Wraith", "Warden", "Dynamo"]),
]


def support_table(souls, aim):
    """Each support item on the last hero of team A vs an empty slot, averaged over LINEUPS x both focus modes x
    two distances, 20 s fights. swing = health the enemy team lost - health team A lost (heals count)."""
    G = game()
    rows = []
    for item in SUPPORT_ITEMS:
        tot, n = {}, 0
        for ta, tb in LINEUPS:
            a = [parse(h, souls, aim) for h in ta]
            b = [parse(h, souls, aim) for h in tb]
            a[-1].items = [i for i in a[-1].items if i not in SUPPORT_ITEMS]
            for focus in ("focus", "spread"):
                for dist in (12.0, 20.0):
                    v = team_item_value(a, b, len(a) - 1, item, focus=focus, distance=dist, max_time=20.0)["delta"]
                    for k, x in v.items():
                        tot[k] = tot.get(k, 0) + x
                    n += 1
        rows.append((item, {k: x / n for k, x in tot.items()}))
    rows.sort(key=lambda r: r[1]["swing"], reverse=True)
    print(f"Support items on the 3rd hero vs an empty slot, {souls:.0f} souls, mean of {n} 3v3 fights")
    print(f"{'item':<20}{'cost':>6}{'swing':>9}{'team dmg':>10}{'dmg taken':>11}{'heal/shield given':>19}{'win':>7}")
    for item, t in rows:
        print(f"{item:<20}{G.item(item).cost:>6}{t['swing']:>+9.0f}{t['damage']:>+10.0f}{t['damage_taken']:>+11.0f}"
              f"{t['healing_given']:>+19.0f}{t['win']:>+7.2f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a", action="append", default=[], help='"Hero: item, item" (repeat per hero)')
    ap.add_argument("--b", action="append", default=[])
    ap.add_argument("--souls", type=float, default=27000)
    ap.add_argument("--aim", default="p50", help="ranked percentile for every hero (p25, p50, p75, p90)")
    ap.add_argument("--focus", default="focus", choices=["focus", "spread"])
    ap.add_argument("--distance", type=float, default=15.0)
    ap.add_argument("--max-time", type=float, default=40.0)
    ap.add_argument("--value", nargs=2, metavar=("N", "ITEM"), help="value of ITEM on team A's Nth hero (1-based)")
    ap.add_argument("--replace", help="with --value: the item that takes its slot (default: empty slot)")
    ap.add_argument("--support", type=float, metavar="SOULS", help="rank support items in standard 3v3 lineups")
    ap.add_argument("--json", action="store_true")
    q = ap.parse_args()
    if q.support:
        support_table(q.support, q.aim)
        return
    if not q.a or not q.b:
        ap.error("give at least one --a and one --b hero")
    a = [parse(s, q.souls, q.aim) for s in q.a]
    b = [parse(s, q.souls, q.aim) for s in q.b]
    kw = dict(distance=q.distance, max_time=q.max_time, focus=q.focus)
    if q.value:
        v = team_item_value(a, b, int(q.value[0]) - 1, q.value[1], replace=q.replace, **kw)
        print(json.dumps(v, indent=1, default=round))
        return
    r = team_fight(a, b, **kw)
    if q.json:
        print(json.dumps(r.to_dict(), indent=1))
        return
    for side, team in (("A", a), ("B", b)):
        for x in team:
            print(f"[{side}] {x.hero}: {', '.join(x.items) or '(no items)'}")
    print(r.summary())


if __name__ == "__main__":
    main()
