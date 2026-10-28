"""Express Shot on Shiv's and Yamato's alt fire in Phantom+ replays (validation/README.md "Shiv and Yamato: Express
Shot on the alt fire", items_fx.EXPRESS_ALT). The same check as viscous_alt_fire.py for the two other heroes with a
secondary weapon (raw heroes.json items.weapon_secondary).

Per hero: the alt fire's share of gun damage with and without Express Shot; median Express Shot event, alt-fire hit
and primary hit after the first proc; Express Shot damage per proc (events within PROC_S) by match fifth.

usage: python3 -I express_alt_fire.py [raw dir]     (default: project folder analysis/work/fight_length/raw)
"""
import collections
import glob
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from viscous_alt_fire import PROC_S, T, med, read  # noqa: E402

EXPRESS = 690458959
HEROES = {19: ("Shiv", 3121968594, 225271804), 27: ("Yamato", 440716503, 2725537392)}   # id: name, primary, alt


def main():
    raw = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project-files/analysis/work/fight_length/raw/"
    files = [read(fn) for fn in sorted(glob.glob(os.path.join(raw, "*.ndjson.gz")))]
    for hid, (name, prim, alt) in HEROES.items():
        alt_share = {True: [], False: []}
        sizes = collections.defaultdict(list)
        per_proc = collections.defaultdict(list)
        for hero, ev, last in files:
            for pawn, es in ev.items():
                if hero.get(pawn) != hid:
                    continue
                es = sorted(e for e in es if e[1] in hero and hero[e[1]] != hid)
                by = collections.defaultdict(list)
                for e in es:
                    by[e[2]].append(e)
                gun = sum(e[3] for e in by[prim] + by[alt])
                if gun:
                    alt_share[bool(by[EXPRESS])].append(sum(e[3] for e in by[alt]) / gun)
                if not by[EXPRESS]:
                    continue
                t0 = by[EXPRESS][0][0]
                for k in (EXPRESS, alt, prim):
                    sizes[k] += [e[3] for e in by[k] if e[0] >= t0]
                procs = []
                for e in by[EXPRESS]:
                    if procs and e[0] - procs[-1][0] < PROC_S * T:
                        procs[-1][1] += e[3]
                    else:
                        procs.append([e[0], e[3]])
                for t, v in procs:
                    per_proc[min(4, int(5 * t / last))].append(v)
        print(name)
        for k, v in alt_share.items():
            if v:
                print(f"  alt fire share of gun damage, {'with' if k else 'without'} Express Shot: {len(v)} players, "
                      f"median {statistics.median(v):.2f}")
        print(f"  after the first proc, median Express Shot event {med(sizes[EXPRESS])}, alt hit {med(sizes[alt])}, "
              f"primary hit {med(sizes[prim])}")
        print("  Express Shot damage per proc by fifth:", {b: (len(v), med(v)) for b, v in sorted(per_proc.items())})


if __name__ == "__main__":
    main()
