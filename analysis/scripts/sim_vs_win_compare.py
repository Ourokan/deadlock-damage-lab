"""Is a sim_vs_win change real? Two row files (sim_vs_win.py --out, base and variant) against the shipped edges and
against edges rebuilt from each half of the window's days (independent matches: hero halves share each item's
all-hero edge, so an item-wide change moves both hero halves alike whatever the noise). Prints, per budget and edge
set, within slot and tier Pearson base -> variant, its hero halves, a noise sd of the delta (edges redrawn by their
se), all pairs, and Spearman (the score ranks items; Pearson over the raw gains follows the few largest gains).
sim/validation/heal_survival.md.

    python3 analysis/scripts/sim_vs_win_compare.py BASE.json VAR.json [--halves PARTIALS_DIR [--work DIR]]
    # PARTIALS_DIR: item_win_edge per-day partials (pipeline/refresh_win_edge.partials), e.g. win_edge_week/
"""
import argparse
import glob
import json
import os
import random
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sim_vs_win as V  # noqa: E402
import build_win_check as B  # noqa: E402


def day_half_edges(partials, work):
    """edges_A / edges_B.json in work from alternate days of the partials; returns their paths."""
    days = sorted(glob.glob(os.path.join(partials, "*.json.gz")))
    out = []
    for k, ps in (("A", days[0::2]), ("B", days[1::2])):
        p = os.path.join(work, f"edges_{k}.json")
        if not os.path.exists(p):
            heroes, fit = B.hero_edges(B.load(ps))
            B.write_edges(heroes, p, fit=fit, days=[os.path.basename(x)[:10] for x in ps], note="day half " + k)
        out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("var")
    ap.add_argument("--halves", default="")
    ap.add_argument("--work", default=os.path.join(V.ROOT, "analysis", "work", "edge_halves"))
    a = ap.parse_args()
    g = V.S.G()
    slot = {it.name: (it.slot, it.tier) for it in g.items.values()}
    by_name = {it.name: i for i, it in g.items.items()}
    base, var = json.load(open(a.base)), json.load(open(a.var))
    edges = {"shipped": None}
    if a.halves:
        os.makedirs(a.work, exist_ok=True)
        for p in day_half_edges(a.halves, a.work):
            edges[os.path.basename(p)] = json.load(open(p))["heroes"]

    def cen(rows):
        grp = {}
        for r in rows:
            grp.setdefault((r[0], r[1], *slot[r[2]]), []).append(r)
        return {(r[0], r[1], r[2]): r[3] - statistics.mean(q[3] for q in rs)
                for rs in grp.values() if len(rs) > 1 for r in rs}

    for b in sorted({r[1] for r in base}):
        xb, xv = cen([r for r in base if r[1] == b]), cen([r for r in var if r[1] == b])
        ab = {(r[0], r[1], r[2]): r[3] for r in base if r[1] == b}
        av = {(r[0], r[1], r[2]): r[3] for r in var if r[1] == b}
        for en, ed in edges.items():
            e, se = {}, {}
            for r in base:
                if r[1] != b:
                    continue
                v = (r[4], r[5]) if ed is None else ed.get(str(r[0]), {}).get(str(by_name[r[2]]))
                if v is not None:
                    e[(r[0], r[1], r[2])], se[(r[0], r[1], r[2])] = v[0], v[1]
            keys = sorted(k for k in xb if k in xv and k in e)
            hs = sorted({k[0] for k in keys})
            halves = [[k for k in keys if k[0] in set(hs[h::2])] for h in (0, 1)]

            def r_(f, ks, x):
                return f([x[k] for k in ks], [e[k] for k in ks])
            w = [r_(V.pearson, keys, x) for x in (xb, xv)]
            wh = [r_(V.pearson, ks, xv) - r_(V.pearson, ks, xb) for ks in halves]
            sp = [r_(V.spearman, keys, x) for x in (xb, xv)]
            sph = [r_(V.spearman, ks, xv) - r_(V.spearman, ks, xb) for ks in halves]
            ak = sorted(k for k in ab if k in av and k in e)
            al = [r_(V.pearson, ak, x) for x in (ab, av)]
            rnd, ds, items = random.Random(1), [], sorted({k[2] for k in keys})
            for _ in range(200):   # each edge redrawn by its se: 0.6 shared by the item's heroes, 0.8 its own
                sh = {i: rnd.gauss(0, 1) for i in items}
                ee = {k: e[k] + se[k] * (0.6 * sh[k[2]] + 0.8 * rnd.gauss(0, 1)) for k in keys}
                ds.append(V.pearson([xv[k] for k in keys], [ee[k] for k in keys])
                          - V.pearson([xb[k] for k in keys], [ee[k] for k in keys]))
            print(f"{b} {en:13s} within {w[0]:.4f} -> {w[1]:.4f} ({w[1] - w[0]:+.4f} +-{statistics.pstdev(ds):.4f}, "
                  f"halves {wh[0]:+.4f}/{wh[1]:+.4f})  all {al[0]:.4f} -> {al[1]:.4f}  Spearman within {sp[0]:.4f} -> "
                  f"{sp[1]:.4f} ({sp[1] - sp[0]:+.4f}, halves {sph[0]:+.4f}/{sph[1]:+.4f})  n {len(keys)}", flush=True)


if __name__ == "__main__":
    main()
