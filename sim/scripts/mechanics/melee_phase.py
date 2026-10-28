"""Melee by game phase: each hero's real melee share over the sim's at 30 / 60 / 90% of the match
(data/melee_phase.json, Mechanics.melee_phase).

The melee rate (data/melee_rates.json) is one number per hero, fitted to the whole match. Real players melee most in
the lane and less later: the real melee share of a hero's damage around 30% of the match is 1.20x the sim's at its
30% duels (all heroes, players weighted), 0.91x at 60%, 0.74x at 90%. Ranged heroes drop the most (Ivy 1.47 / 0.72 /
0.51, Nurse 1.10 / 0.59 / 0.44), melee heroes stay flat (Abrams 0.92 / 1.01 / 1.05). Calico, the hero furthest from
real damage after the 2026-10-27 fixes: 1.27 / 1.15 / 1.03, her items matching real at every phase (her whole-match
"items over" was the late duels' weight). Per hit sizes match the formula at every phase (melee_scaling.py), so it
is the rate.

Real: the sample's damage_series (cumulative per source at damage_times), each source's damage in the window
frac +- WINDOW of the match. Sim: the damage audit with only duels at that frac (AUDIT_SEEDS draws). Per hero and
frac: r = real melee share / sim melee share, times the multiplier already in use (the mechanic on), shrunk in ln to
the pooled curve (heroes weighted by real melee damage) with SHRINK players of weight. Net worth of a point: the median of the hero's players at that frac.
Rows for heroes with MIN_PLAYERS players and a real melee share >= MIN_SHARE at 30%.

usage: python3 melee_phase.py [--sample PATH] [--parity even|odd] [--hero NAME] [--write]
(--parity: fit on that half of the sample's matches by match_id, for split-half checks; --hero: refit only that hero's
row from a hero sample (e.g. validation/mirage_sample.jsonl.gz), shrunk to the file's pooled curve, other rows kept)
"""
import collections
import bisect
import gzip
import json
import math
import os
import statistics
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(HERE, ".."))
from deadsim import game  # noqa: E402
from deadsim.mechanics import melee_phase_mult  # noqa: E402
import landing_rates as L  # noqa: E402

SAMPLE = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
OUT = os.path.join(ROOT, "data", "melee_phase.json")
FRACS = (0.3, 0.6, 0.9)
WINDOW = 0.15
AUDIT_SEEDS = (0, 1)
SHRINK = 30      # players
MIN_PLAYERS = 20
MIN_SHARE = 0.01
CLAMP = (0.25, 3.0)


def cum(times, ser, t):
    xs, ys = [0] + times, [0] + ser
    i = bisect.bisect_right(xs, t) - 1
    if i >= len(xs) - 1:
        return ys[-1]
    return ys[i] + (ys[i + 1] - ys[i]) * (t - xs[i]) / (xs[i + 1] - xs[i])


def real_phase(sample, G, kind):
    """{hero id: {frac: Counter(kind -> real damage in the window)}}, {hero id: {frac: [net worths]}}"""
    acc = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    nw = collections.defaultdict(lambda: collections.defaultdict(list))
    for line in gzip.open(sample):
        m = json.loads(line)
        T, tm = m["duration_s"], m["damage_times"]
        for p in m["players"]:
            hid = p["hero_id"]
            if hid not in G.heroes or not L.gun_known(p):
                continue
            classes = {ab.class_name for ab in G.hero(hid).abilities}
            for fr in FRACS:
                nw[hid][fr].append(L.build_at(p, fr * T)[1])
            for k, ser in p["damage_series"].items():
                if k in L.CATEGORY:
                    continue
                kk = kind(L.real_key(k, list(classes)), G, classes)
                for fr in FRACS:
                    lo, hi = max(0.0, fr - WINDOW) * T, min(1.0, fr + WINDOW) * T
                    acc[hid][fr][kk] += cum(tm, ser, hi) - cum(tm, ser, lo)
    return acc, nw


def sim_phase(sample):
    """{hero name: {frac: (mean sim melee share, players)}} from the damage audit's duels at one frac."""
    import damage_audit as D
    out = collections.defaultdict(dict)
    for fr in FRACS:
        L.FRACS = (fr,)
        shares = collections.defaultdict(list)
        for seed in AUDIT_SEEDS:
            path = os.path.join(tempfile.gettempdir(), f"melee_phase_{os.getpid()}_{fr}_{seed}")
            os.environ["AUDIT_SEED"], os.environ["AUDIT_OUT"] = str(seed), path
            D.SEED = seed
            sys.argv = ["damage_audit.py", sample]
            D.main()
            for h, row in json.load(open(path + ".json"))["heroes"].items():
                shares[h].append((row["sim_mix"]["melee"], row["players"]))
        for h, v in shares.items():
            out[h][fr] = (statistics.mean(x for x, _ in v), v[0][1])
    L.FRACS = FRACS
    return out


def main():
    args = sys.argv[1:]
    sample = args[args.index("--sample") + 1] if "--sample" in args else SAMPLE
    if "--parity" in args:
        par = 0 if args[args.index("--parity") + 1] == "even" else 1
        fd, half = tempfile.mkstemp(suffix=".jsonl.gz")
        os.close(fd)
        with gzip.open(half, "wt") as fh:
            for line in gzip.open(sample, "rt"):
                if json.loads(line)["match_id"] % 2 == par:
                    fh.write(line)
        sample = half
    write = "--write" in args
    only = args[args.index("--hero") + 1] if "--hero" in args else None
    if only:
        os.environ["AUDIT_HEROES"] = only
    G = game()
    import damage_audit as D
    real, nws = real_phase(sample, G, D.kind)
    sim = sim_phase(sample)
    rows = {}
    for hid in real:
        h = G.hero(hid)
        if h.name not in sim:
            continue
        pts = []
        for fr in FRACS:
            r = real[hid][fr]
            tot = sum(r.values())
            s, n = sim[h.name].get(fr, (0.0, 0))
            nw = statistics.median(nws[hid][fr])
            if tot <= 0 or s <= 0:
                pts = None
                break
            # the sim share was measured with the mechanic as it is: its multiplier there is part of the sim rate
            pts.append((fr, nw, r["melee"] / tot, s, n, melee_phase_mult(hid, nw)))
        if pts and pts[0][2] >= MIN_SHARE and pts[0][4] >= MIN_PLAYERS:
            rows[hid] = pts
    pooled = {}
    for i, fr in enumerate(FRACS):
        # weighted by real melee damage (players x share): heroes that barely melee have noisy ratios
        w = sum(p[i][4] * p[i][2] for p in rows.values())
        pooled[fr] = sum(p[i][4] * p[i][2] * math.log(p[i][2] / p[i][3] * p[i][5]) for p in rows.values()) / w
    if only:   # one hero's sample: its own ratios would be the "pooled" curve, so shrink to the file's
        old = json.load(open(OUT))
        pooled = {fr: math.log(old["pooled"][str(fr)]) for fr in FRACS}
        rows = {hid: p for hid, p in rows.items() if G.hero(hid).name == G.hero(only).name}
    out = {}
    for hid, pts in sorted(rows.items(), key=lambda x: G.hero(x[0]).name):
        n = pts[0][4]
        mults = []
        for fr, nw, rs, ss, _, cur in pts:
            lr = (n * math.log(rs / ss * cur) + SHRINK * pooled[fr]) / (n + SHRINK)
            mults.append([round(nw), round(min(CLAMP[1], max(CLAMP[0], math.exp(lr))), 4)])
        out[str(hid)] = {"name": G.hero(hid).name, "players": n,
                         "real_melee": [round(p[2], 4) for p in pts], "sim_melee": [round(p[3], 4) for p in pts],
                         "points": mults}
        print(f"{G.hero(hid).name:14s} n{n:4d} real {' '.join(f'{p[2]:.3f}' for p in pts)}  sim "
              f"{' '.join(f'{p[3]:.3f}' for p in pts)}  mult {' '.join(f'{m:.2f}@{nw}' for nw, m in mults)}")
    print("pooled", {fr: round(math.exp(v), 3) for fr, v in pooled.items()})
    if write and only:
        old["heroes"].update(out)
        json.dump(old, open(OUT, "w"), indent=1)
        print("wrote", OUT, "row", only)
    elif write:
        json.dump({"source": f"{os.path.basename(sample)} damage_series vs damage audit duels at {FRACS} "
                             "(scripts/mechanics/melee_phase.py)",
                   "note": "melee rate x mult at the duel's net worth, linear in ln net worth between points, flat "
                           "outside (Mechanics.melee_phase)",
                   "pooled": {str(fr): round(math.exp(v), 4) for fr, v in pooled.items()},
                   "heroes": out}, open(OUT, "w"), indent=1)
        print("wrote", OUT)


if __name__ == "__main__":
    main()
