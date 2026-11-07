"""sim_vs_win against RAW per-hero edges from half of the days (no shrinkage, so nothing in the edges uses buy shares).

The shipped edges' rare-pick prior (build_win_check.rarity_fit) lowers an item's edge by its buy share, so any change
to the score that uses buy shares (overall_search.buy_value) lifts the usual check mechanically. This check compares
the sim gain (centred within hero, budget, slot and tier) with each item's raw edge from alternate days of the
item_win_edge partials (day halves A / B), inverse-variance weighted (binomial se + TAU^2), base vs variant row files
(sim_vs_win.py --out), with the two hero halves. sim/validation/buy_rate.md.

    python3 analysis/scripts/sim_vs_win_raw.py BASE.json VAR.json --halves PARTIALS_DIR
"""
import argparse
import glob
import math
import os
import statistics
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sim_vs_win as V  # noqa: E402
import build_win_check as B  # noqa: E402

TAU2 = 1.2e-4   # spread of true per-hero edges (rarity_fit tau2 on 10-31..11-05)


def wpearson(x, y, w):
    W = sum(w)
    mx, my = sum(a * c for a, c in zip(x, w)) / W, sum(b * c for b, c in zip(y, w)) / W
    sxy = sum(c * (a - mx) * (b - my) for a, b, c in zip(x, y, w))
    sxx = sum(c * (a - mx) ** 2 for a, c in zip(x, w))
    syy = sum(c * (b - my) ** 2 for b, c in zip(y, w))
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0


def raw_halves(partials):
    days = sorted(glob.glob(os.path.join(partials, "*.json.gz")))
    out = {}
    for k, ps in (("A", days[0::2]), ("B", days[1::2])):
        heroes, _ = B.hero_edges(B.load(ps))
        out[k] = {h: {i: (c["raw"], c["raw_se"]) for i, c in row.items()} for h, row in heroes.items()}
    return out


def check(rows, gains, edges, b, slot, by_name, heroes=None):
    grp = {}
    for r, x in zip(rows, gains):
        if r[1] != b or (heroes is not None and r[0] not in heroes):
            continue
        v = edges.get(r[0], {}).get(by_name[r[2]])
        if v is not None:
            grp.setdefault((r[0], *slot[r[2]]), []).append((x, v))
    xs, ys, ws = [], [], []
    for q in grp.values():
        if len(q) < 2:
            continue
        m = statistics.mean(x for x, _ in q)
        for x, (raw, se) in q:
            xs.append(x - m)
            ys.append(raw)
            ws.append(1 / (se ** 2 + TAU2))
    return wpearson(xs, ys, ws)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("var")
    ap.add_argument("--halves", required=True)
    a = ap.parse_args()
    g = V.S.G()
    slot = {it.name: (it.slot, it.tier) for it in g.items.values()}
    by_name = {it.name: i for i, it in g.items.items()}
    base = json.load(open(a.base))
    vm = {(r[0], r[1], r[2]): r[3] for r in json.load(open(a.var))}
    rows = [r for r in base if (r[0], r[1], r[2]) in vm]
    xb, xv = [r[3] for r in rows], [vm[(r[0], r[1], r[2])] for r in rows]
    hs = sorted({r[0] for r in rows})
    hh = [set(hs[0::2]), set(hs[1::2])]
    for k, ed in raw_halves(a.halves).items():
        for b in sorted({r[1] for r in rows}):
            r0, r1 = (check(rows, x, ed, b, slot, by_name) for x in (xb, xv))
            d = [check(rows, xv, ed, b, slot, by_name, h) - check(rows, xb, ed, b, slot, by_name, h) for h in hh]
            print(f"{b} day half {k}: raw within {r0:.4f} -> {r1:.4f} ({r1 - r0:+.4f}, hero halves {d[0]:+.4f}/{d[1]:+.4f})")


if __name__ == "__main__":
    main()
