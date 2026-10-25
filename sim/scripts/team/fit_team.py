"""How many teammates and other enemies are close by in real Phantom+ fights, from match_paths (1 s positions), for
the team value of auras, ally heals and area items in the overall score.

Fight second: player A alive and flagged in hero combat (combat_type & 1), nearest living enemy B within NEAR m and
also in hero combat (same definition as fit_range.py). For each fight second and radius R:
- allies(R): living teammates of A within R m of A (who an aura or an area heal around A reaches);
- any_ally(R): share of fight seconds with at least one teammate within R m (a single-target ally cast can land);
- extra(R): other living enemies within R m of B (who an area hit centred on A's target also hits);
- extra_self(R): living enemies other than B within R m of A (area around A: Scourge, Torment Pulse, Cold Front);
- attackers: living enemies other than B within NEAR m of A and in hero combat (who else shoots A).
Means are split by A's net worth at that second, binned to the search budgets.
Writes sim/data/team_value.json (the fitted part; team_value.py adds the item values).

usage: python3 -I fit_team.py <sim dir> <paths dir>
"""
import bisect, glob, gzip, json, math, os, sys
from collections import defaultdict

NEAR = 40.0
RADII = (5, 8, 10, 12, 15, 16, 20, 25, 30, 35, 40)
BUDGETS = (10000, 18000, 27000, 37000, 50000)


def worth_at(nw, t):
    """Net worth at second t, linear between the API's samples."""
    ts = [p[0] for p in nw]
    i = bisect.bisect_left(ts, t)
    if i == 0:
        return nw[0][1] * t / max(1, nw[0][0])
    if i >= len(nw):
        return nw[-1][1]
    (t0, v0), (t1, v1) = nw[i - 1], nw[i]
    return v0 + (v1 - v0) * (t - t0) / max(1, t1 - t0)


def budget_bin(w):
    return min(BUDGETS, key=lambda b: abs(math.log(max(w, 1000) / b)))


def scan(m, acc):
    P = {p["slot"]: p for p in m["players"]}
    paths = {int(k): v for k, v in m["paths"].items() if int(k) in P}
    if len(paths) < 12:
        return
    n = min(len(v["x"]) for v in paths.values())
    step = m.get("interval_s", 1)
    for t in range(n):
        alive = [s for s in paths if paths[s]["hp"][t] > 0]
        pos = {s: (paths[s]["x"][t], paths[s]["y"][t]) for s in alive}

        def d(a, b):
            return math.hypot(pos[a][0] - pos[b][0], pos[a][1] - pos[b][1])

        for a in alive:
            if not paths[a]["combat"][t] & 1:
                continue
            foes = sorted((d(a, q), q) for q in alive if P[q]["team"] != P[a]["team"])
            if not foes or foes[0][0] > NEAR or not paths[foes[0][1]]["combat"][t] & 1:
                continue
            b = foes[0][1]
            mates = [d(a, q) for q in alive if q != a and P[q]["team"] == P[a]["team"]]
            others = [q for _, q in foes[1:]]
            near_b = [d(b, q) for q in others]
            near_a = [dd for dd, q in foes[1:]]
            row = acc[budget_bin(worth_at(P[a]["net_worth"], t * step))]
            row["n"] += 1
            row["attackers"] += sum(1 for dd, q in foes[1:] if dd <= NEAR and paths[q]["combat"][t] & 1)
            row["solo"] += 1 if not [x for x in mates if x <= NEAR] and not [x for x in near_a if x <= NEAR] else 0
            for r in RADII:
                row[f"allies_{r}"] += sum(1 for x in mates if x <= r)
                row[f"any_ally_{r}"] += 1 if any(x <= r for x in mates) else 0
                row[f"extra_{r}"] += sum(1 for x in near_b if x <= r)
                row[f"extra_self_{r}"] += sum(1 for x in near_a if x <= r)


def main():
    files = sorted(glob.glob(os.path.join(sys.argv[2], "*.json.gz")))
    acc = defaultdict(lambda: defaultdict(float))
    for fn in files:
        scan(json.load(gzip.open(fn, "rt")), acc)
    out = {"source": f"{len(files)} Phantom+ matches, match_paths 1 s (fit_team.py)", "near_m": NEAR,
           "radii_m": list(RADII), "budgets": {}}
    tot = defaultdict(float)
    for b in BUDGETS:
        row = acc[b]
        for k, v in row.items():
            tot[k] += v
    for b, row in list(((b, acc[b]) for b in BUDGETS)) + [("all", tot)]:
        n = max(1.0, row["n"])
        out["budgets"][str(b)] = {
            "fight_seconds": int(row["n"]), "solo_share": round(row["solo"] / n, 3),
            "attackers": round(row["attackers"] / n, 3),
            "allies": {str(r): round(row[f"allies_{r}"] / n, 3) for r in RADII},
            "any_ally": {str(r): round(row[f"any_ally_{r}"] / n, 3) for r in RADII},
            "extra": {str(r): round(row[f"extra_{r}"] / n, 3) for r in RADII},
            "extra_self": {str(r): round(row[f"extra_self_{r}"] / n, 3) for r in RADII},
        }
        print(b, out["budgets"][str(b)])
    dst = os.path.join(sys.argv[1], "data", "team_value.json")
    old = {}
    if os.path.exists(dst):
        old = json.load(open(dst))
    old["positions"] = out
    json.dump(old, open(dst, "w"), indent=1)


if __name__ == "__main__":
    main()
