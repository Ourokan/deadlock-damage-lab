"""Real fight range per hero from match_paths (1 s positions), for the sim's drifting fight distance.

Fight second: player A alive and flagged in hero combat (combat_type & 1), nearest living enemy B within NEAR m and
also in hero combat. Duel second: additionally no other enemy and no teammate of A within CROWD m of A (the sim
models 1v1s). Segments are runs of consecutive fight seconds against the same B.

Per A's hero: distance percentiles, and how far and fast the distance drifts: a log-distance variogram over segments
of LONG+ s fitted as an Ornstein-Uhlenbeck process (stationary log_sd, time constant tau_s). Demeaning short segments
biases autocorrelation negative, which is why the variogram is used.
Writes sim/data/fight_range.json.

usage: python3 -I fit_range.py <sim dir> <paths dir>
"""
import glob, gzip, json, math, os, statistics, sys
from collections import defaultdict
sys.path.insert(0, sys.argv[1])
from deadsim.data import game  # noqa: E402

NEAR, CROWD, MIN_SEG, LONG, LAGS = 40.0, 25.0, 4, 10, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
G = game()
NAMES = {h.id: h.name for h in (G.heroes.values() if isinstance(G.heroes, dict) else G.heroes)}


def pct(xs, q):
    xs = sorted(xs)
    i = (len(xs) - 1) * q
    lo = int(i)
    return xs[lo] + (xs[min(lo + 1, len(xs) - 1)] - xs[lo]) * (i - lo)


def segments(m, duel_only):
    P = {p["slot"]: p for p in m["players"]}
    paths = {int(k): v for k, v in m["paths"].items() if int(k) in P}
    if len(paths) < 12:
        return
    n = min(len(v["x"]) for v in paths.values())

    def d(a, b, t):
        return math.hypot(paths[a]["x"][t] - paths[b]["x"][t], paths[a]["y"][t] - paths[b]["y"][t])

    def fighting(s, t):
        return paths[s]["hp"][t] > 0 and paths[s]["combat"][t] & 1

    for a in paths:
        seg, foe = [], None
        for t in range(n):
            b = None
            if fighting(a, t):
                en = sorted((d(a, q, t), q) for q in paths if P[q]["team"] != P[a]["team"] and paths[q]["hp"][t] > 0)
                if en and en[0][0] <= NEAR and fighting(en[0][1], t):
                    b = en[0][1]
                    if duel_only:
                        crowd = sum(1 for dd, q in en[1:] if dd <= CROWD) + sum(
                            1 for q in paths if q != a and P[q]["team"] == P[a]["team"] and paths[q]["hp"][t] > 0
                            and d(a, q, t) <= CROWD)
                        if crowd:
                            b = None
            if b is not None and b == foe:
                seg.append(d(a, b, t))
                continue
            if len(seg) >= MIN_SEG:
                yield P[a]["hero_id"], P[foe]["hero_id"], seg
            seg, foe = ([d(a, b, t)], b) if b is not None else ([], None)
        if len(seg) >= MIN_SEG:
            yield P[a]["hero_id"], P[foe]["hero_id"], seg


def summarize(segs):
    """Percentiles of all fight seconds; drift from segments of LONG+ s: log-distance variogram
    g(k) = mean((ln d(t+k) - ln d(t))^2) / 2, fitted as an Ornstein-Uhlenbeck process sd^2 (1 - exp(-k / tau))."""
    ds = [x for s in segs for x in s]
    if len(ds) < 200:
        return None
    g, c = defaultdict(float), defaultdict(int)
    for s in segs:
        if len(s) < LONG:
            continue
        L = [math.log(max(1.0, x)) for x in s]
        for k in LAGS:
            for i in range(len(L) - k):
                g[k] += (L[i + k] - L[i]) ** 2 / 2
                c[k] += 1
    if c[LAGS[-1]] < 100:
        return None
    vg = {k: g[k] / c[k] for k in LAGS}
    sill = statistics.fmean(vg[k] for k in LAGS[-3:])
    taus = [-k / math.log(1 - vg[k] / sill) for k in LAGS[:4] if vg[k] < sill]
    return {"seconds": len(ds), "segments": len(segs), "long_segments": sum(1 for s in segs if len(s) >= LONG),
            "median_m": round(statistics.median(ds), 1), "p10_m": round(pct(ds, .1), 1), "p25_m": round(pct(ds, .25), 1),
            "p75_m": round(pct(ds, .75), 1), "p90_m": round(pct(ds, .9), 1),
            "log_sd": round(math.sqrt(sill), 3), "tau_s": round(statistics.median(taus), 2) if taus else None,
            "variogram_sqrt": {str(k): round(math.sqrt(v), 3) for k, v in vg.items()}}


def main():
    files = sorted(glob.glob(os.path.join(sys.argv[2], "*.json.gz")))
    out = {"source": f"{len(files)} Phantom+ matches, match_paths 1 s", "near_m": NEAR, "crowd_m": CROWD}
    for mode in ("duel", "all"):
        by_hero, pairs, allsegs = defaultdict(list), [], []
        for fn in files:
            m = json.load(gzip.open(fn, "rt"))
            for ha, hb, seg in segments(m, mode == "duel"):
                by_hero[ha].append(seg)
                allsegs.append(seg)
                pairs.append((ha, hb, statistics.fmean(seg), len(seg)))
        heroes = {}
        for h, segs in sorted(by_hero.items()):
            s = summarize(segs)
            if s:
                heroes[str(h)] = dict(name=NAMES.get(h, str(h)), **s)
        out[mode] = {"all": summarize(allsegs), "heroes": heroes}
        # who sets the range: segment mean vs both heroes' own medians (least squares, d = c + wa * A + wb * B)
        med = {int(k): v["median_m"] for k, v in heroes.items()}
        rows = [(med[a], med[b], dm, n) for a, b, dm, n in pairs if a in med and b in med]
        if rows:
            sw = sum(r[3] for r in rows)
            mean = [sum(r[i] * r[3] for r in rows) / sw for i in range(3)]
            saa = sum(r[3] * (r[0] - mean[0]) ** 2 for r in rows)
            sbb = sum(r[3] * (r[1] - mean[1]) ** 2 for r in rows)
            sab = sum(r[3] * (r[0] - mean[0]) * (r[1] - mean[1]) for r in rows)
            say = sum(r[3] * (r[0] - mean[0]) * (r[2] - mean[2]) for r in rows)
            sby = sum(r[3] * (r[1] - mean[1]) * (r[2] - mean[2]) for r in rows)
            det = saa * sbb - sab * sab
            out[mode]["pair_fit"] = {"w_own": round((say * sbb - sby * sab) / det, 3),
                                     "w_enemy": round((sby * saa - say * sab) / det, 3), "segments": len(rows)}
        a = out[mode]["all"]
        print(mode, {k: a[k] for k in ("seconds", "segments", "long_segments", "median_m", "p25_m", "p75_m", "log_sd",
                                        "tau_s")}, a["variogram_sqrt"], out[mode].get("pair_fit"))
    dst = os.path.join(sys.argv[1], "data", "fight_range.json")
    json.dump(out, open(dst, "w"), indent=1)
    for k, v in sorted(out["duel"]["heroes"].items(), key=lambda x: x[1]["median_m"]):
        print(f"{v['name']:15s} n={v['seconds']:5d} med {v['median_m']:5.1f} p25 {v['p25_m']:5.1f} p75 {v['p75_m']:5.1f} "
              f"log_sd {v['log_sd']:.3f} tau {v['tau_s']}")


if __name__ == "__main__":
    main()
