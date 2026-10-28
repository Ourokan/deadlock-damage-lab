"""sim_vs_win without rerunning the sim: rows from sim_vs_win.py --out, with other target edges (hero_item_edge.json
form, e.g. edge_lead_check.py edges) and/or other fight_rate tables (fit_fight_rate.py --out). The death rate, focus
and farm values are pure item multipliers, so rescaling each row's item-build score by their new / old ratio is
exact. Prints all pairs, within slot and tier (hero halves: every other hero id) and per item, per budget.

    python3 analysis/scripts/sim_vs_win_offline.py ROWS_27k.json ROWS_37k.json [--edges a.json,b.json]
        [--rates fight_rate_x.json,...] [--clear]   # seconds
"""
import argparse
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim_vs_win as V  # noqa: E402
O, S, GP = V.O, V.S, V.GP
ap = argparse.ArgumentParser()
ap.add_argument("rows", nargs="+")
ap.add_argument("--edges", default="")
ap.add_argument("--rates", default="")
ap.add_argument("--clear", action="store_true", help="only edges clear of 95%% band")
a = ap.parse_args()
V.setup(True)
g = S.G()
by_name = {it.name: i for i, it in g.items.items()}
slot = {it.name: (it.slot, it.tier) for it in g.items.values()}
rows = [r for p in a.rows for r in json.load(open(p))]
pops = {}
for b in sorted({r[1] for r in rows}):
    pools = S.load_pools(b)
    for h in sorted({r[0] for r in rows if r[1] == b}):
        pops[(h, b)] = S.popular_build(h, GP.item_budget(b), pools)

def F(items, hero, souls):
    return O.death_rate_value(items, hero, souls) * O.focus_value(items, souls) * O.farm_value(items, souls)

def load_rates(p):
    O._rate = json.load(open(p)) if p != "shipped" else None
    O._drate.clear(); O._taken.clear(); O._jungle.clear()
    O.fight_rate_data()

load_rates("shipped")
old = {}
for r in rows:
    pop = pops[(r[0], r[1])]
    old[id(r)] = F(GP.with_item(pop, by_name[r[2]]), r[0], r[1]) / F(pop, r[0], r[1])

def metrics(rs):
    out = {}
    x, y = [r[3] for r in rs], [r[4] for r in rs]
    out["all"] = V.pearson(x, y)
    grp = {}
    for r in rs:
        grp.setdefault((r[0], *slot[r[2]]), []).append(r)
    cen = [(r[3] - statistics.mean(q[3] for q in g_), r[4], r[0]) for g_ in grp.values() if len(g_) > 1 for r in g_]
    out["within"] = V.pearson([c[0] for c in cen], [c[1] for c in cen])
    hs = sorted({r[0] for r in rs})
    for k in (0, 1):
        half = set(hs[k::2])
        cc = [c for c in cen if c[2] in half]
        out[f"w{k}"] = V.pearson([c[0] for c in cc], [c[1] for c in cc])
    by = {}
    for r in rs:
        by.setdefault(r[2], []).append(r)
    its = [(statistics.mean(q[3] for q in v), statistics.mean(q[4] for q in v)) for v in by.values() if len(v) >= 5]
    out["item"] = V.pearson(*zip(*its))
    out["n"] = len(rs)
    return out

edges = {"shipped": None}
for p in a.edges.split(","):
    if p:
        edges[os.path.basename(p)] = json.load(open(p))["heroes"]
rates = ["shipped"] + [p for p in a.rates.split(",") if p]
for rp in rates:
    load_rates(rp)
    for en, ed in edges.items():
        for b in sorted({r[1] for r in rows}):
            rs = []
            for r in rows:
                if r[1] != b:
                    continue
                pop = pops[(r[0], r[1])]
                new = F(GP.with_item(pop, by_name[r[2]]), r[0], r[1]) / F(pop, r[0], r[1])
                sc = r[13] * new / old[id(r)]
                gain = (sc - r[12]) / r[14] * 1000
                if ed is None:
                    e, se = r[4], r[5]
                else:
                    v = ed.get(str(r[0]), {}).get(str(by_name[r[2]]))
                    if v is None:
                        continue
                    e, se = v[0], v[1]
                if a.clear and abs(e) <= 1.96 * se:
                    continue
                rs.append([r[0], r[1], r[2], gain, e, se])
            m = metrics(rs)
            print(f"rates {os.path.basename(rp):14s} edges {en:20s} {b}: all {m['all']:.4f} within {m['within']:.4f} "
                  f"({m['w0']:.4f} / {m['w1']:.4f}) item {m['item']:.4f} n {m['n']}", flush=True)
