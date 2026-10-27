"""Do real holders' fewer deaths go with real wins for healing items? (overall_search.HEAL_ITEMS)

Per item: x = log(real holders' / non-holders' deaths per minute) (holder_rates.py output, matched by hero, net worth
and game time), y = the item's mean real win edge over heroes (analysis/out/hero_item_edge.json, same-slot same-tier).
Least squares slope and Pearson r of y on x, healing items vs the rest, for all matches and each match-id half.
Across the other items holders who die less win more (27k: -11.6 points per log death ratio, r -0.39), the basis of
the score's death rate factor (death_rate_value). Across healing items it goes the other way (+7.8, r +0.35, both
halves, 37k alike): their holders die less without winning more, so the score leaves their death ratios out.

usage: python3 -I heal_deaths.py HOLDER_RATES.json [BUDGET]   (run from the repo root)
"""
import json
import math
import os
import statistics
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "damage", "scripts"))
import overall_search as O  # noqa: E402

holder = json.load(open(sys.argv[1]))
budget = sys.argv[2] if len(sys.argv) > 2 else "27000"
with open(O.WIN_EDGE) as f:
    heroes = json.load(f)["heroes"]
g = O.S.G()
edges = {}
for row in heroes.values():
    for i, e in row.items():
        if int(i) in g.items:
            edges.setdefault(g.items[int(i)].name, []).append(e[0])


def fit(pts):
    xs, ys = zip(*pts)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx, syy = sum((x - mx) ** 2 for x in xs), sum((y - my) ** 2 for y in ys)
    return sxy / sxx, sxy / (sxx * syy) ** 0.5


for half, label in (("2", "all matches"), ("0", "even match ids"), ("1", "odd match ids")):
    real = holder[f"{budget}_{half}"]
    pts = {True: [], False: []}
    for n, v in edges.items():
        if n in real and len(v) >= 5:
            pts[n in O.HEAL_ITEMS].append((math.log(real[n]["deaths"][0]), statistics.mean(v)))
    out = []
    for heal in (False, True):
        b, r = fit(pts[heal])
        out.append(f"{'healing' if heal else 'other'} {len(pts[heal])} items: {b:+.1f} pt per log death ratio, r {r:+.2f}")
    print(f"{label:15s} " + " | ".join(out))
