"""How much of the sim's survival gain shows up in real holders' deaths (overall_search.HEAL_SURVIVAL).

Per item: sim log ratios (item build / popular build, mean over heroes; sim_vs_win.py --out rows: damage before death
idx 15-16, time alive idx 17-18) of time alive and of damage while alive, against real holders' / non-holders' log
ratios of hero damage per minute and of deaths / (kills + assists) (holder_rates.py output, matched by hero, net worth
and game time). Least squares slopes over items with 5+ heroes, healing items (overall_search.HEAL_ITEMS) apart from
the rest, all matches and each match-id half, with a bootstrap sd over items. sim/validation/heal_survival.md.

usage: python3 sim/scripts/fight_rate/survival_slope.py SIM_VS_WIN_ROWS.json HOLDER_RATES.json   # repo root
"""
import json
import math
import os
import random
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "damage", "scripts"))
import overall_search as O  # noqa: E402


def slope(P, xi, yi):
    xs, ys = [p[xi] for p in P], [p[yi] for p in P]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


def main():
    rows, holder = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
    for b in sorted({str(r[1]) for r in rows}):
        sim = {}
        for r in rows:
            if str(r[1]) == b and len(r) > 18 and min(r[15], r[16], r[17], r[18]) > 0:
                lt = math.log(r[18] / r[17])
                sim.setdefault(r[2], []).append((math.log(r[16] / r[15]) - lt, lt))
        for half, label in (("2", "all matches"), ("0", "even match ids"), ("1", "odd match ids")):
            real = holder.get(f"{b}_{half}")
            if not real:
                continue
            pts = [(statistics.mean(a for a, _ in v), statistics.mean(t for _, t in v), math.log(real[n]["dealt"][0]),
                    math.log(real[n]["deaths"][0] / real[n]["ka"][0]), n in O.HEAL_ITEMS)
                   for n, v in sim.items() if n in real and len(v) >= 5]
            out = []
            for lab, P in (("healing", [p for p in pts if p[4]]), ("other", [p for p in pts if not p[4]])):
                rnd = random.Random(0)
                bs = [slope([rnd.choice(P) for _ in P], 1, 3) for _ in range(300)]
                out.append(f"{lab} {len(P)} items: dealt ~ dps {slope(P, 0, 2):.2f}, deaths/ka ~ time alive "
                           f"{slope(P, 1, 3):+.2f} (sd {statistics.pstdev(bs):.2f})")
            print(f"{b} {label:15s} " + " | ".join(out))


if __name__ == "__main__":
    main()
