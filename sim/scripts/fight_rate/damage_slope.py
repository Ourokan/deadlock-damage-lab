"""How much of the sim's damage gain shows up in real holders' damage per minute (overall_search.DAMAGE_ELASTICITY).

Per item: x = mean over heroes of log(sim damage before death with the item / the popular build's)
(analysis/scripts/sim_vs_win.py --out rows, idx 15-16), y = log(real holders' / non-holders' hero damage per minute)
(holder_rates.py output, matched by hero, net worth and game time). Least squares slope y on x over items with 5+
heroes, for all matches and each match-id half.

usage: python3 -I damage_slope.py SIM_VS_WIN_ROWS.json HOLDER_RATES.json [BUDGET]
"""
import json
import math
import statistics
import sys

rows, holder = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
budget = sys.argv[3] if len(sys.argv) > 3 else "27000"
sim = {}
for r in rows:
    if r[15] > 0 and r[16] > 0:
        sim.setdefault(r[2], []).append(math.log(r[16] / r[15]))
for half, label in (("2", "all matches"), ("0", "even match ids"), ("1", "odd match ids")):
    real = holder[f"{budget}_{half}"]
    xs, ys = zip(*[(statistics.mean(v), math.log(real[n]["dealt"][0])) for n, v in sim.items()
                   if n in real and len(v) >= 5])
    mx, my = statistics.mean(xs), statistics.mean(ys)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    print(f"{label:15s} {len(xs)} items  slope {b:.3f}  intercept {my - b * mx:+.3f}")
