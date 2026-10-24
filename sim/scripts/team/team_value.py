"""What ally items give teammates, per teammate in reach, for the overall score's team value. Run from sim/:

    python3 scripts/team/team_value.py [--workers 4]

The overall score (damage/scripts/overall_search.py) is a 1v1: Heroic Aura's fire rate, Healing Nova's heal and a
Divine Barrier on a teammate do nothing there. Here each ally item is put on one hero of a 3v3 and the fight is run
twice more with everything that reaches teammates turned off (team_fight(allies=False): duel item handlers, no ally
abilities). The item's team-only value is

    team_only = (swing with item - swing without), allies on  -  the same with allies off

with swing = health the enemy team lost - health our team lost over a 20 s fight (heals and barriers count, see
deadsim/team.py). It is divided by the holder's share of the damage in the allies-off fight without the item (enemy
health lost / 3, ratio of the means over all fights), so value 0.10 = the item gives teammates a tenth of what the
holder deals in a fight. Every ally in the 3v3 is in reach (huddle 1, one distance), so the value is per `reach_sim` allies; overall_search scales it by
how many teammates are really in reach in Phantom+ fights (positions in data/team_value.json, fit_team.py):
mean teammates within the radius for auras and area heals, the share of fight seconds with one in cast range for
single-target casts.

Lineups: LINEUPS random 3v3s (fixed seed) of the heroes' most popular real builds at each budget (damage/out), each
A hero carrying the item in turn, focus and spread targeting, 12 and 20 m. Skills: the overall search's (Phantom+
aim and badge, counterplay on). Writes the "items" part of data/team_value.json.
"""
import argparse
import dataclasses
import json
import os
import random
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, SIM)
sys.path.insert(0, os.path.join(SIM, "scripts"))
sys.path.insert(0, os.path.join(SIM, "..", "search", "scripts"))

from deadsim import Loadout  # noqa: E402
from deadsim.accuracy import hero_default_skill  # noqa: E402
from deadsim.data import game  # noqa: E402
from deadsim.team import team_fight  # noqa: E402
from team_fight import popular_items  # noqa: E402
from build_pool import BRACKETS, PRIMARY  # noqa: E402

OUT = os.path.join(SIM, "data", "team_value.json")
BUDGETS = (10000, 18000, 27000, 37000, 50000)
LINEUPS = 40
MAX_TIME = 20.0
SEED = 7
# item -> (reach kind, radius m, allies the 3v3 reaches). "allies": mean teammates within the radius;
# "any": share of fight seconds with a teammate in cast range (one target); "enemies": other enemies within the
# radius of the holder (Hunter's Aura shreds every enemy around it, which teammates then shoot; in the 3v3 the aura
# reaches both other enemies at 12 m and none at 20 m, so 1 on average).
ALLY_ITEMS = {
    "Heroic Aura": ("allies", 35, 2.0),
    "Healing Nova": ("allies", 18, 2.0),
    "Rescue Beam": ("any", 35, 1.0),
    "Divine Barrier": ("any", 40, 1.0),
    "Guardian Ward": ("any", 40, 1.0),
    "Restorative Locket": ("any", 32, 1.0),
    "Hunter's Aura": ("enemies", 15, 1.0),
}


def skill(hero):
    lo, _, aim, _ = BRACKETS[PRIMARY]
    return hero_default_skill(hero, aim, badge=lo if lo > 0 else None, counterplay=True)


def lineups():
    g = game()
    heroes = sorted(h.name for h in (g.heroes.values() if isinstance(g.heroes, dict) else g.heroes)
                    if popular_items(h.name, 27000))
    rng = random.Random(SEED)
    return [tuple(rng.sample(heroes, 6)) for _ in range(LINEUPS)]


def swing(r):
    return r.hp_lost("B") - r.hp_lost("A")


def job(args):
    item, souls = args
    tot = {"team_only": 0.0, "on": 0.0, "off": 0.0, "share": 0.0}
    vals = []
    n = 0
    for six in lineups():
        a = [Loadout(h, popular_items(h, souls), souls=souls, skill=skill(h)) for h in six[:3]]
        b = [Loadout(h, popular_items(h, souls), souls=souls, skill=skill(h)) for h in six[3:]]
        for k in range(3):
            base = [dataclasses.replace(x, items=[i for i in x.items if i != item]) for x in a]
            with_ = list(base)
            with_[k] = dataclasses.replace(base[k], items=base[k].items + [item])
            for focus in ("focus", "spread"):
                for dist in (12.0, 20.0):
                    kw = dict(focus=focus, distance=dist, max_time=MAX_TIME, huddle=1.0, aoe_share=0.0)
                    r0_off = team_fight(base, b, allies=False, **kw)
                    d_on = swing(team_fight(with_, b, **kw)) - swing(team_fight(base, b, **kw))
                    d_off = swing(team_fight(with_, b, allies=False, **kw)) - swing(r0_off)
                    share = max(1.0, r0_off.hp_lost("B") / len(a))
                    tot["team_only"] += d_on - d_off
                    vals.append(d_on - d_off)
                    tot["on"] += d_on
                    tot["off"] += d_off
                    tot["share"] += share
                    n += 1
    out = {k: v / n for k, v in tot.items()}
    m = out["team_only"]
    se = (sum((x - m) ** 2 for x in vals) / max(1, n - 1) / n) ** 0.5
    out["team_only"], out["se"] = m / out["share"], se / out["share"]   # ratio of means: small fights don't blow up
    return item, souls, out, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--items", default="", help="comma list: refit only these, keep the others' values")
    q = ap.parse_args()
    todo = [i for i in q.items.split(",") if i] or list(ALLY_ITEMS)
    jobs = [(i, b) for i in todo for b in BUDGETS]
    res = {}
    with Pool(q.workers) as p:
        for item, souls, v, n in p.imap_unordered(job, jobs):
            res.setdefault(item, {})[str(souls)] = {"value": round(v["team_only"], 4), "se": round(v["se"], 4),
                                                    "swing_on": round(v["on"], 1), "swing_off": round(v["off"], 1),
                                                    "holder_damage": round(v["share"], 1), "fights": n}
            print(f"{item:<20} {souls:>6}: team-only {v['team_only']:+.3f} of the holder's damage (se {v['se']:.3f}) "
                  f"(swing +{v['on']:.0f} with allies, +{v['off']:.0f} without)", flush=True)
    d = json.load(open(OUT)) if os.path.exists(OUT) else {}
    old = d.get("items", {}).get("values", {})
    d["items"] = {
        "source": f"team_value.py: {LINEUPS} random 3v3 lineups x 3 holders x focus/spread x 12/20 m, "
                  f"{MAX_TIME:.0f} s, popular builds, Phantom+ skills",
        "values": {i: {"reach": ALLY_ITEMS[i][0], "radius_m": ALLY_ITEMS[i][1], "reach_sim": ALLY_ITEMS[i][2],
                       "budgets": dict(sorted(res[i].items(), key=lambda x: int(x[0])))} if i in res else old[i]
                   for i in ALLY_ITEMS if i in res or i in old},
    }
    json.dump(d, open(OUT, "w"), indent=1)


if __name__ == "__main__":
    main()
