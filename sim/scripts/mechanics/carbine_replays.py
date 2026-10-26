"""Paradox's Kinetic Carbine in Phantom+ replays: hit size against his gun hits, hits per gun damage, the gap from his
last gun hit, and which of his hits release Tankbuster / Mystic Burst.

Reads the fight-length replays (fetch_fights.py output, project folder analysis/work/fight_length/raw: hero-vs-hero
DamageEvents and each pawn's hero). No queries. Compare with the sim's own numbers from the damage audit's duels
(validation/README.md "Paradox's Carbine count").

usage: python3 -I carbine_replays.py [raw dir]
"""
import bisect
import collections
import gzip
import json
import os
import statistics as st
import sys

RAW = "/mnt/project-files/analysis/work/fight_length/raw/"
T = 64
PARADOX = 10
CARBINE, GUN, PULSE, SWAP = 1128670012, 2390964381, 58655583, 2917891787
TANKBUSTER, MYSTIC_BURST = 2121044373, 1998374645
NAMES = {CARBINE: "Kinetic Carbine", GUN: "gun", PULSE: "Pulse Grenade", SWAP: "Paradoxical Swap"}
FRACS = (0.3, 0.6, 0.9)   # the audit's duel points (share of the match), +-0.05


def matches(raw):
    for f in sorted(os.listdir(raw)):
        rows = [r for r in (json.loads(x) for x in gzip.open(os.path.join(raw, f))) if r.get("s")]
        hero = {r["a"]: int(r["s"]) for r in rows if r["k"] == "ctl"}
        for p in (p for p, h in hero.items() if h == PARADOX):
            dmg = sorted((r for r in rows if r["k"] == "dmg"), key=lambda r: r["tick"])
            mine = [(r["tick"], r["a"] % 100000, int(r["s"].split("|")[0]), r["v"]) for r in dmg
                    if r["a"] // 100000 == p and r["a"] % 100000 in hero]
            if mine:
                yield dmg[0]["tick"], dmg[-1]["tick"], mine


def main():
    raw = sys.argv[1] if len(sys.argv) > 1 else RAW
    tot = collections.Counter()
    size = collections.defaultdict(lambda: ([], []))   # frac -> (Carbine hits, gun hits)
    by_gap = collections.defaultdict(list)             # 0.5 s gap bucket -> Carbine hit / median of the last 30 gun hits
    gaps = []
    release = {TANKBUSTER: collections.Counter(), MYSTIC_BURST: collections.Counter()}
    n = 0
    for t0, t1, ev in matches(raw):
        n += 1
        gt = [t for t, _, a, _ in ev if a == GUN]
        gv = [v for _, _, a, v in ev if a == GUN]
        tick = collections.defaultdict(list)
        for t, vic, a, v in ev:
            tot[a] += v
            tot["n", a] += 1
            tick[t, vic].append(a)
            fr = (t - t0) / max(1, t1 - t0)
            for c in FRACS:
                if abs(fr - c) <= 0.05 and a in (CARBINE, GUN):
                    size[c][a == GUN].append(v)
            if a != CARBINE:
                continue
            i = bisect.bisect_left(gt, t)
            if i < 10:   # gap and ratio need his earlier gun hits (sizes and counts above take every hit)
                continue
            g = (t - gt[i - 1]) / T
            if g <= 10:
                gaps.append(g)
                by_gap[min(8.0, int(g * 2) / 2)].append(v / st.median(gv[max(0, i - 30):i]))
        for ids in tick.values():
            for item, c in release.items():
                if item in ids:
                    other = [NAMES.get(a, str(a)) for a in ids if a != item]
                    c[other[0] if other else "none"] += 1
    g = tot[GUN]
    print(f"{n} Paradox players; Carbine / gun damage {tot[CARBINE] / g:.2f}, Carbine hits per 1000 gun damage "
          f"{1000 * tot['n', CARBINE] / g:.2f}, mean hit {tot[CARBINE] / tot['n', CARBINE]:.0f}")
    for c in FRACS:
        cs, gs = size[c]
        print(f"at {c:.0%} of the match: Carbine median {st.median(cs):.0f}, gun hit median {st.median(gs):.0f}, "
              f"ratio {st.median(cs) / st.median(gs):.1f} ({len(cs)} Carbine hits)")
    mid = [x for x in gaps if x <= 5]
    print("gap from his last gun hit (<= 5 s, mid-fight) quartiles", [round(x, 2) for x in st.quantiles(mid, n=4)])
    print("Carbine hit / median gun hit by that gap:",
          ", ".join(f"{k:.1f}s {st.median(v):.1f}" for k, v in sorted(by_gap.items())))
    for item, c in release.items():
        print(("Tankbuster" if item == TANKBUSTER else "Mystic Burst"), "released with:", c.most_common(5))


if __name__ == "__main__":
    main()
