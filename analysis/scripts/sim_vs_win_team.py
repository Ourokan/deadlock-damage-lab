"""sim_vs_win rows (sim_vs_win.py --out) rescored offline for ally heal team value variants: team value is a pure item
multiplier, so score x new / old is exact. Prints within slot and tier (hero halves) and all pairs per budget.
sim/validation/nova_heal.md.

    python3 analysis/scripts/sim_vs_win_team.py ROWS_27k.json[,ROWS_37k.json] "Healing Nova=2.4" ["Healing Nova=0.5,Rescue Beam=0.5" ...]
    # repo root, search/work pools built
"""
import json
import statistics
import sys
sys.path.insert(0, "analysis/scripts")
import sim_vs_win as V  # noqa: E402
O, S, GP = V.O, V.S, V.GP
V.setup(True)
g = S.G()
by = {it.name: i for i, it in g.items.items()}
slot = {it.name: (it.slot, it.tier) for it in g.items.values()}
rows = [r for p in sys.argv[1].split(",") for r in json.load(open(p))]
pops = {}
for b in sorted({r[1] for r in rows}):
    pools = S.load_pools(b)
    for h in sorted({r[0] for r in rows if r[1] == b}):
        pops[(h, b)] = tuple(sorted(S.popular_build(h, GP.item_budget(b), pools)))


def metrics(rs):
    grp = {}
    for r in rs:
        grp.setdefault((r[0], *slot[r[2]]), []).append(r)
    cen = [(r[3] - statistics.mean(q[3] for q in g_), r[4], r[0]) for g_ in grp.values() if len(g_) > 1 for r in g_]
    hs = sorted({r[0] for r in rs})
    out = {"within": V.pearson([c[0] for c in cen], [c[1] for c in cen])}
    for k in (0, 1):
        half = set(hs[k::2])
        cc = [c for c in cen if c[2] in half]
        out[f"w{k}"] = V.pearson([c[0] for c in cc], [c[1] for c in cc])
    out["all"] = V.pearson([r[3] for r in rs], [r[4] for r in rs])
    return out


O.ally_heal()
AH0 = dict(O._ally_heal)


def rescore(changes):
    out = []
    for r in rows:
        pop = pops[(r[0], r[1])]
        wi = tuple(sorted(GP.with_item(list(pop), by[r[2]])))
        O._ally_heal = AH0
        old = O.team_value(wi, r[1]) / O.team_value(pop, r[1])
        O._ally_heal = {**AH0, **changes}
        new = O.team_value(wi, r[1]) / O.team_value(pop, r[1])
        O._ally_heal = AH0
        rr = list(r)
        rr[3] = (r[13] * new / old - r[12]) / r[14] * 1000
        out.append(rr)
    return out


def parse(s):
    return {k.strip(): float(v) for k, v in (x.split("=") for x in s.split(",") if x.strip())}


for label in ["shipped"] + sys.argv[2:]:
    rs = rescore({} if label == "shipped" else parse(label))
    for b in sorted({r[1] for r in rs}):
        sub = [r for r in rs if r[1] == b]
        m = metrics(sub)
        gains = sorted(((r[3], r[2]) for r in sub if r[2] == "Healing Nova"), reverse=True)
        print(f"{label:34s} {b} within {m['within']:.4f} halves {m['w0']:.4f}/{m['w1']:.4f} all {m['all']:.4f} "
              f"Nova mean gain {statistics.mean(x for x, _ in gains) if gains else float('nan'):.2f}", flush=True)
