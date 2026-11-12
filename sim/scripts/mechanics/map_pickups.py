"""Permanent map pickups by net worth, from a Phantom+ validation sample (2026-11-11).

Breakables and the Sinners' Sacrifice / urn drops leave permanent pickups (match players' "power_ups": type, values,
pickup times): weapon damage %, fire rate %, spirit power, max health, cooldown reduction %, bullet and spirit resist %,
plus ammo, range and move speed the sim does not use. validate_stats.py shows the real stat sheet is the build plus
these. The sim's fights had none, while a real player carries ~+10% weapon damage, +5% fire rate, +7 spirit power and
+100 health by 90% of the match. This averages each stat over every player's stats snapshots (pickups collected by the
snapshot's time) in net-worth bins; Mechanics.map_pickups adds the bin curve (linear in ln net worth) to both fighters.

usage: python3 -I map_pickups.py <sample.jsonl.gz> [--half 0|1] [--write]   (~1 min on a 4,000-match sample)
"""
import bisect
import collections
import gzip
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "data", "map_pickups.json")
KINDS = {"wp": "weapon_pct", "firerate": "fire_rate_pct", "spirit": "spirit", "hp": "health", "cd": "cdr_pct",
         "bulletresist": "bullet_resist_pct", "spiritresist": "spirit_resist_pct"}
BINS = (0, 3000, 6000, 10000, 15000, 20000, 26000, 33000, 42000, 55000, 10 ** 9)


def kind(t):
    base = (t or "").split("_permanent_pickup")[0]
    return KINDS.get(base)


def fit(sample, half=None):
    acc = collections.defaultdict(lambda: collections.Counter())   # bin -> stat -> summed value ("n", "nw" too)
    for line in gzip.open(sample):
        m = json.loads(line)
        if half is not None and m["match_id"] % 2 != half:
            continue
        for p in m["players"]:
            got = []   # (time, stat, value)
            for b in p.get("power_ups") or []:
                k = kind(b.get("type"))
                if k:
                    got += [(t, k, v) for v, t in zip(b.get("values") or [], b.get("times") or [])]
            got.sort()
            times = [g[0] for g in got]
            for s in p.get("stats") or []:
                nw = s.get("net_worth") or 0
                if nw <= 0:
                    continue
                bi = bisect.bisect_right(BINS, nw) - 1
                c = acc[bi]
                c["n"] += 1
                c["nw"] += nw
                for _, k, v in got[:bisect.bisect_right(times, s["time_stamp_s"])]:
                    c[k] += v
    bins = []
    for bi in sorted(acc):
        c = acc[bi]
        if c["n"] < 200:
            continue
        bins.append({"net_worth": round(c["nw"] / c["n"]), "n": c["n"],
                     **{k: round(c[k] / c["n"], 3) for k in KINDS.values()}})
    return bins


def main():
    args = sys.argv[1:]
    half = int(args[args.index("--half") + 1]) if "--half" in args else None
    sample = args[0]
    bins = fit(sample, half)
    for b in bins:
        print(b)
    if "--write" in args:
        json.dump({"source": f"scripts/mechanics/map_pickups.py ({os.path.basename(sample)})",
                   "note": "mean permanent pickups collected by a stats snapshot, by its net-worth bin; percent stats "
                           "in points (4.0 = +4%); Mechanics.map_pickups, linear in ln net worth, flat outside",
                   "bins": bins}, open(OUT, "w"), indent=1)
        print("->", OUT)


if __name__ == "__main__":
    main()
