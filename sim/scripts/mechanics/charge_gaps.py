"""Gaps between a charged ability's landed casts in Phantom+ replays (Mechanics.charge_gaps, data/charge_gaps.json).

The sim casts a charged ability's next charge as soon as AbilityCooldownBetweenCharge allows (recast timing skips
charged abilities), so Viscous fired Puddle Punch's second charge 1.7 s after the first, inside Spirit Snatch's 6 s
cooldown: 54% of the sim's Punches met a Snatch on cooldown, 24% of real ones. Real players space them: of the gaps
between one Viscous' landed Punches (casts = hits more than 0.5 s apart) past 30% of the match (charges bought),
22% are under 6 s, 9% under 3 s, 54% over 20 s (the next fight). The gaps under 20 s are written as QBINS
quantiles; the sim draws the wait from the cast to the next one from them (the fight's end already stands for the
longer ones, as recast_timing's finite draws).

usage: python3 -I charge_gaps.py [raw dir ...]   (default: project folder analysis/work/fight_length/raw and
analysis/work/viscous_replays/raw, DamageEvent rows from scripts/fight_length/fetch_fights.py)
"""
import collections
import glob
import gzip
import json
import os
import sys

T = 64
QBINS = 20
MERGE_S = 0.5     # hits of one cast (several heroes, same tick or so)
FROM_FRAC = 0.3   # past this share of the match (the extra charge bought)
MAX_GAP = 20.0
ABILITIES = {35: ("viscous_telepunch", 1020817390)}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "charge_gaps.json")


def read(fn):
    hero, ev, last = {}, collections.defaultdict(list), 0
    for line in gzip.open(fn, "rt"):
        r = json.loads(line)
        last = max(last, r["tick"])
        if r["k"] == "ctl":
            hero[r["a"]] = int(r["s"])
        elif r["k"] == "dmg" and r.get("s"):
            ev[r["a"] // 100000].append((r["tick"], r["a"] % 100000, int(r["s"].split("|")[0])))
    return hero, ev, last


def main():
    dirs = sys.argv[1:] or ["/mnt/project-files/analysis/work/fight_length/raw/",
                            "/mnt/project-files/analysis/work/viscous_replays/raw/"]
    gaps = collections.defaultdict(list)
    seen = set()
    for d in dirs:
        for fn in sorted(glob.glob(os.path.join(d, "*.ndjson.gz"))):
            mid = os.path.basename(fn).split(".")[0]
            if mid in seen:
                continue
            seen.add(mid)
            hero, ev, last = read(fn)
            for pawn, es in ev.items():
                h = hero.get(pawn)
                if h not in ABILITIES:
                    continue
                cls, aid = ABILITIES[h]
                casts = []
                for t in sorted(e[0] for e in es if e[2] == aid and e[1] in hero and hero[e[1]] != h):
                    if not casts or t - casts[-1] >= MERGE_S * T:
                        casts.append(t)
                gaps[f"{h}:{cls}"] += [(b - a) / T for a, b in zip(casts, casts[1:]) if a > FROM_FRAC * last]
    out = {"source": f"{len(seen)} Phantom+ replays, hero-vs-hero DamageEvent (scripts/mechanics/charge_gaps.py)",
           "note": f"gaps (s) between landed casts past {FROM_FRAC:.0%} of the match, those under {MAX_GAP:.0f} s as "
                   f"{QBINS} quantiles; Mechanics.charge_gaps draws the wait from a cast to the next charge's",
           "sources": {}}
    for k, g in sorted(gaps.items()):
        g.sort()
        fin = [x for x in g if x < MAX_GAP]
        out["sources"][k] = {"gaps": len(g), "under_6s": round(sum(x < 6 for x in g) / len(g), 3),
                             "under_20s": round(len(fin) / len(g), 3),
                             "q": [round(fin[int((i + 0.5) / QBINS * len(fin))], 2) for i in range(QBINS)]}
        print(k, out["sources"][k])
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
