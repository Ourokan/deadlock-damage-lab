"""Does Arctic Beam lock Kelvin's gun as long in Phantom+ replays as in the sim? (validation/README.md "Kelvin, Billy,
Celeste: item factors on the fresh sample")

The sim channels the beam for its whole AbilityDuration with the gun locked (kelvin.ArcticBeam). Per beam cast (cast
rows) that hit a hero: when its last damage tick came, and Kelvin's gun hits from that tick to the end of the
duration vs his gun rate in the 5 s after. If real Kelvins cut the channel short to shoot, gun hits would show up in
the rest of the window. 2026-10-28 (259 matches, 1,463 beams): last tick median 4.0 s (25% by 2.2 s), but after an
early end only 0.05 gun hits/s vs 0.19 in the next 5 s, 7% of early ends with any gun hit: the channel runs on
(the target walked out of the beam), as the sim has it.

usage: python3 -I kelvin_beam.py [cast raw dir] [damage raw dir]   (default: project folder analysis/work/cast_timing/raw
and analysis/work/fight_length/raw)
"""
import glob
import gzip
import json
import os
import sys

T = 64
KELVIN = 12
BEAM, GUN = 2351041382, 3576988085


def q(x, qs=(0.1, 0.25, 0.5, 0.75, 0.9)):
    x = sorted(x)
    return [round(x[int(p * len(x))], 2) for p in qs] if x else None


def main():
    ct = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project-files/analysis/work/cast_timing/raw/"
    fl = sys.argv[2] if len(sys.argv) > 2 else "/mnt/project-files/analysis/work/fight_length/raw/"
    ids = lambda d: {os.path.basename(f).split(".")[0] for f in glob.glob(os.path.join(d, "*.ndjson.gz"))}  # noqa: E731
    last, rows = [], []
    for mid in sorted(ids(ct) & ids(fl)):
        hero, es = {}, []
        for line in gzip.open(os.path.join(fl, mid + ".ndjson.gz"), "rt"):
            r = json.loads(line)
            if r["k"] == "ctl":
                hero[r["a"]] = int(r["s"])
            elif r["k"] == "dmg" and r.get("s"):
                es.append((r["tick"], r["a"] // 100000, r["a"] % 100000, int(r["s"].split("|")[0])))
        pawns = [p for p, h in hero.items() if h == KELVIN]
        if len(pawns) != 1:
            continue
        pawn = pawns[0]
        es = sorted((t, src) for t, a, v, src in es if a == pawn and v in hero and hero[v] != KELVIN)
        casts = [r["tick"] for r in map(json.loads, gzip.open(os.path.join(ct, mid + ".ndjson.gz"), "rt"))
                 if r["k"] == "cast" and r["a"] == pawn and int(r["s"]) == BEAM]
        for c in casts:
            ticks = [t for t, s in es if s == BEAM and c <= t <= c + 6 * T]
            if not ticks:
                continue
            lb = max(ticks)
            last.append((lb - c) / T)
            rows.append((lb - c, sum(1 for t, s in es if s == GUN and lb < t <= c + 5 * T),
                         sum(1 for t, s in es if s == GUN and c + 5 * T < t <= c + 10 * T)))
    print(f"beam casts that hit a hero: {len(rows)}")
    print("last beam tick after the cast (s), 10/25/50/75/90%:", q(last))
    early = [x for x in rows if x[0] < 4 * T]
    rest = sum(5 * T - x[0] for x in early) / T
    print(f"beam ended before 4 s: {len(early)}; gun hits/s until 5 s {sum(x[1] for x in early) / max(1e-9, rest):.3f}, "
          f"in the next 5 s {sum(x[2] for x in rows) / (5 * len(rows)):.3f}; "
          f"share with a gun hit before 5 s {sum(1 for x in early if x[1]) / max(1, len(early)):.3f}")


if __name__ == "__main__":
    main()
