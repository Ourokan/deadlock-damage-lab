"""What does a death cost in real wins, next to damage dealt? (overall_search.DEATH_RATE_GAMMA)

Per item: the real holders' / non-holders' rates (holder_rates.py output, matched by hero, net worth and game time):
log damage dealt per minute, log deaths per kills + assists (the death_rate_value ratio), log kills + assists and log
damage taken per minute; y = the item's mean real win edge over heroes (analysis/out/hero_item_edge.json, same-slot
same-tier). All centred within slot and tier (as the edge is), least squares of y on the four. Healing items
(overall_search.HEAL_ITEMS) are left out, as the score leaves their death ratios out.

The score moves ~1x a log change of real damage dealt (DAMAGE_ELASTICITY 0.5 on the sim gain, which real holders
show 0.51x of) and, with DEATH_RATE_GAMMA 1, ~0.33x a log change of the death ratio (the share of game time a
death takes, death_rate_value's slope at the mid-game rates). Printed: the coefficients, the real death : dealt price
ratio and the score's at DEATH_RATE_GAMMA 1. 2026-10-29: 27k dealt +6.9, deaths/ka -14.2 (ratio 2.1), 37k +7.4 /
-12.4 (1.7); both match-id halves alike (2.0 / 2.0, 1.5 / 1.6); the score's ratio 0.33.

usage: python3 -I death_price.py HOLDER_RATES.json [BUDGETS=27000,37000]   (run from the repo root)
"""
import json
import math
import os
import statistics
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "damage", "scripts"))
import overall_search as O  # noqa: E402

holder = json.load(open(sys.argv[1]))
budgets = (sys.argv[2] if len(sys.argv) > 2 else "27000,37000").split(",")
with open(O.WIN_EDGE) as f:
    heroes = json.load(f)["heroes"]
g = O.S.G()
edges = {}
for row in heroes.values():
    for i, e in row.items():
        if int(i) in g.items:
            edges.setdefault(g.items[int(i)].name, []).append(e[0])
slot = {it.name: (it.slot, it.tier) for it in g.items.values()}


def score_slope(souls):
    """d log death_rate_value / d log death ratio at ratio 1 (DEATH_RATE_GAMMA 1), hero ratio 1."""
    dd = O.death_data()
    row = dd["phases"][O.game_phase(souls)]
    dL = row["deaths_per_engagement"] * O.death_seconds(souls)
    return dL / (row["alive_s_per_engagement"] + dL)


for b in budgets:
    for half, label in (("2", "all"), ("0", "even ids"), ("1", "odd ids")):
        rates = holder[f"{b}_{half}"]
        pts = []
        for n, v in edges.items():
            t = rates.get(n)
            if t is None or len(v) < 5 or n in O.HEAL_ITEMS or not all(k in t for k in ("dealt", "deaths", "ka", "taken")):
                continue
            pts.append((slot[n], statistics.mean(v), [math.log(t["dealt"][0]), math.log(t["deaths"][0] / t["ka"][0]),
                                                      math.log(t["ka"][0]), math.log(t["taken"][0])]))
        grp = {}
        for p in pts:
            grp.setdefault(p[0], []).append(p)
        X, Y = [], []
        for v in grp.values():
            if len(v) < 2:
                continue
            x = np.array([p[2] for p in v])
            y = np.array([p[1] for p in v])
            X += list(x - x.mean(0))
            Y += list(y - y.mean())
        c, *_ = np.linalg.lstsq(np.array(X), np.array(Y), rcond=None)
        print(f"{b} {label:8s} n {len(Y)}: win points per log dealt {c[0]:+.1f}, deaths/ka {c[1]:+.1f}, ka {c[2]:+.1f}, "
              f"taken {c[3]:+.1f}; death : dealt price real {-c[1] / c[0]:.2f}, score at gamma 1 "
              f"{score_slope(int(b)) / (O.DAMAGE_ELASTICITY / 0.51):.2f}")
