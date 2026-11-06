"""sim_vs_win rows (made without the trip gate, sim_vs_win.py --no-trip-gate --out) rescored offline for map time (TRIP_S,
heal items off, TRIP_JUNGLE_GATE via the gate variant) and heal items' team value variants: both are pure item multipliers, so score x new / old is exact.
Prints within slot and tier (hero halves) and all pairs per budget. sim/validation/map_time.md.

    python3 analysis/scripts/sim_vs_win_map.py ROWS_27k.json[,ROWS_37k.json]   # repo root, search/work pools built
"""
import json
import statistics
import sys
sys.path.insert(0, "analysis/scripts")
import sim_vs_win as V
O, S, GP = V.O, V.S, V.GP
V.setup(True)
O.TRIP_JUNGLE_GATE = False   # variants are relative to the ungated map time the rows were made with
g = S.G(); by = {it.name: i for i, it in g.items.items()}
slot = {it.name: (it.slot, it.tier) for it in g.items.values()}
rows = [r for p in sys.argv[1].split(",") for r in json.load(open(p))]
pops = {}
for b in sorted({r[1] for r in rows}):
    pools = S.load_pools(b)
    for h in sorted({r[0] for r in rows if r[1] == b}):
        pops[(h, b)] = tuple(sorted(S.popular_build(h, GP.item_budget(b), pools)))

def mt(h, items, b, pop):
    return O.map_time(h, items, b, pop) / O.map_time(h, pop, b, pop)

def metrics(rs):
    grp = {}
    for r in rs: grp.setdefault((r[0], *slot[r[2]]), []).append(r)
    cen = [(r[3] - statistics.mean(q[3] for q in g_), r[4], r[0]) for g_ in grp.values() if len(g_) > 1 for r in g_]
    hs = sorted({r[0] for r in rs}); out = {"within": V.pearson([c[0] for c in cen], [c[1] for c in cen])}
    for k in (0, 1):
        half = set(hs[k::2]); cc = [c for c in cen if c[2] in half]
        out[f"w{k}"] = V.pearson([c[0] for c in cc], [c[1] for c in cc])
    out["all"] = V.pearson([r[3] for r in rs], [r[4] for r in rs])
    return out

def rescore(factor):
    out = []
    for r in rows:
        pop = pops[(r[0], r[1])]; wi = tuple(sorted(GP.with_item(list(pop), by[r[2]])))
        f = factor(r[0], r[1], pop, wi, r[2])
        sc = r[13] * f
        rr = list(r); rr[3] = (sc - r[12]) / r[14] * 1000; out.append(rr)
    return out

base_mt = {}
def variant(trip=None, items_off=()):
    def f(h, b, pop, wi, name):
        k = (h, b, wi)
        if k not in base_mt: base_mt[k] = mt(h, wi, b, pop)
        old = base_mt[k]
        if name in items_off: return 1.0 / old
        if trip is None: return 1.0
        saved = O.TRIP_S; O.TRIP_S = trip
        new = mt(h, wi, b, pop); O.TRIP_S = saved
        return new / old
    return f

def gate_variant():
    def f(h, b, pop, wi, name):
        k = (h, b, wi)
        if k not in base_mt: base_mt[k] = mt(h, wi, b, pop)
        O.TRIP_JUNGLE_GATE = True
        new = mt(h, wi, b, pop)
        O.TRIP_JUNGLE_GATE = False
        return new / base_mt[k]
    return f


O.ally_heal()
AH0 = dict(O._ally_heal)
def team_variant(changes):
    def f(h, b, pop, wi, name):
        O._ally_heal = AH0
        old = O.team_value(wi, b) / O.team_value(pop, b)
        O._ally_heal = {**AH0, **changes}
        new = O.team_value(wi, b) / O.team_value(pop, b)
        O._ally_heal = AH0
        return new / old
    return f
EXTRA = [(f"Nova team x{k}", team_variant({"Healing Nova": k})) for k in (0.0, 0.25, 0.5, 0.75)] + \
        [(f"Nova+RB team x{k}", team_variant({"Healing Nova": k, "Rescue Beam": k})) for k in (0.25, 0.5)]
for label, fac in EXTRA + [("shipped", variant()), ("TRIP 0", variant(trip=0.0)), ("TRIP 20", variant(trip=20.0)),
                   ("TRIP 60", variant(trip=60.0)),
                   ("heal items map off", variant(items_off=O.HEAL_ITEMS)), ("jungle gate", gate_variant())]:
    rs = rescore(fac)
    for b in sorted({r[1] for r in rs}):
        m = metrics([r for r in rs if r[1] == b])
        print(f"{label:22s} {b} within {m['within']:.4f} halves {m['w0']:.4f}/{m['w1']:.4f} all {m['all']:.4f}", flush=True)
