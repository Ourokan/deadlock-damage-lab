"""Viscous' Express Shot and Puddle Punch procs in Phantom+ replays (validation/README.md "Viscous: Express Shot on the
alt fire", items_fx.EXPRESS_ALT / FULL_MELEE_PROC).

Per Viscous in the replays: his alt fire's share of his gun damage (citadel_weapon_viscous_set_2, a slow 42-damage
goo shot) with and without Express Shot; median Express Shot event, alt-fire hit and primary hit after the first
proc; Express Shot damage per proc (events within PROC_S) by match fifth; Spirit Snatch procs per landed Puddle Punch
cast after the first Snatch, and what landed on the same target in the 3 s before each Snatch.

usage: python3 -I viscous_alt_fire.py [raw dir]     (default: project folder analysis/work/fight_length/raw)
"""
import collections
import glob
import gzip
import json
import os
import statistics
import sys

T = 64
PROC_S = 0.6
VISCOUS = 35
PRIMARY, ALT = 3413773852, 3819944797
EXPRESS, SNATCH, PUNCH = 690458959, 3190916303, 1020817390


def read(fn):
    hero, ev, last = {}, collections.defaultdict(list), 0
    for line in gzip.open(fn, "rt"):
        r = json.loads(line)
        last = max(last, r["tick"])
        if r["k"] == "ctl":
            hero[r["a"]] = int(r["s"])
        elif r["k"] == "dmg" and r.get("s"):
            ev[r["a"] // 100000].append((r["tick"], r["a"] % 100000, int(r["s"].split("|")[0]), r["v"]))
    return hero, ev, last


def med(x):
    return round(statistics.median(x)) if x else None


def main():
    raw = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project-files/analysis/work/fight_length/raw/"
    alt_share = {True: [], False: []}
    sizes = collections.defaultdict(list)
    per_proc = collections.defaultdict(list)
    punches = snatches = 0
    before = collections.Counter()
    for fn in sorted(glob.glob(os.path.join(raw, "*.ndjson.gz"))):
        hero, ev, last = read(fn)
        for pawn, es in ev.items():
            if hero.get(pawn) != VISCOUS:
                continue
            es = sorted(e for e in es if e[1] in hero and hero[e[1]] != VISCOUS)
            by = collections.defaultdict(list)
            for e in es:
                by[e[2]].append(e)
            gun = sum(e[3] for e in by[PRIMARY] + by[ALT])
            if gun:
                alt_share[bool(by[EXPRESS])].append(sum(e[3] for e in by[ALT]) / gun)
            if by[EXPRESS]:
                t0 = by[EXPRESS][0][0]
                for k in (EXPRESS, ALT, PRIMARY):
                    sizes[k] += [e[3] for e in by[k] if e[0] >= t0]
                procs = []
                for e in by[EXPRESS]:
                    if procs and e[0] - procs[-1][0] < PROC_S * T:
                        procs[-1][1] += e[3]
                    else:
                        procs.append([e[0], e[3]])
                for t, v in procs:
                    per_proc[min(4, int(5 * t / last))].append(v)
            if by[SNATCH]:
                t0, lt = by[SNATCH][0][0], -1e18
                for e in by[PUNCH]:
                    if e[0] >= t0 and e[0] - lt > 0.5 * T:
                        punches += 1
                    lt = e[0]
                snatches += len(by[SNATCH])
                for e in by[SNATCH]:
                    prev = [x for x in es if x[1] == e[1] and x[2] != SNATCH and 0 <= e[0] - x[0] <= 3 * T]
                    before["Puddle Punch" if prev and prev[-1][2] == PUNCH else "other" if prev else "none"] += 1
    for k, v in alt_share.items():
        print(f"alt fire share of gun damage, {'with' if k else 'without'} Express Shot: {len(v)} players, "
              f"median {statistics.median(v):.2f}" if v else "")
    print(f"after the first proc, median Express Shot event {med(sizes[EXPRESS])}, alt hit {med(sizes[ALT])}, "
          f"primary hit {med(sizes[PRIMARY])}")
    print("Express Shot damage per proc by fifth:", {b: (len(v), med(v)) for b, v in sorted(per_proc.items())})
    print(f"Spirit Snatch: {snatches} procs after {punches} landed Puddle Punch casts ({snatches / max(1, punches):.2f} "
          f"per cast); hit before it: {dict(before)}")


if __name__ == "__main__":
    main()
