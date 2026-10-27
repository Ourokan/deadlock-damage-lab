"""Soul Exchange swaps in Phantom+ replays: how much of the target's max health a real swap takes, and how many casts
land, for Mechanics.swap_full (ghost.SWAP_LAND).

The sim booked the swap through Soul Exchange's fitted landing factor x length_corr (1.42 x 0.41 = 0.58), so the
target lost ~0.20 of its max health per swap where real swaps take ~0.50, and the damage audit had Soul Exchange at
about half its real share (0.07 vs 0.14, on 37 and on ~270 Geist players). The swap is a health swap, not a hit that
lands part of the time: Mechanics.swap_full books it whole on the real share of casts that hit a hero.

Per Geist (fight_length/raw damage events, cast_timing/raw casts as fit_cast_timing.real_casts; matches with both):
casts, Soul Exchange hits on enemy heroes, each hit's loss / target max health, the target's health before, Geist's
last seen health; rows "all" / "even" / "odd" match ids.

usage: python3 -I swap_real.py   (~1 min on 4 cores)
"""
import collections
import gzip
import json
import os
import statistics
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fight_length"))
sys.path.insert(0, os.path.join(HERE, "..", "cast_timing"))
import fit_cast_timing as CT  # noqa: E402
import opener_timing as OT  # noqa: E402

GEIST = 4
SE = 1307289689


def match_rows(fn):
    """(match id, casts, [(loss / max health, target health before, Geist health)], SE damage, all hero damage)"""
    mid = int(os.path.basename(fn).split(".")[0])
    cfn = os.path.join(CT.CASTS, os.path.basename(fn))
    if not os.path.exists(cfn):
        return None
    hero, ev = OT.read(fn)
    gs = {a for a, h in hero.items() if h == GEIST}
    if not gs:
        return None
    casts = sum(1 for r in CT.real_casts([json.loads(line) for line in gzip.open(cfn, "rt")])
                if int(r["s"]) == SE and r["a"] in gs)
    hits, se, tot, last = [], 0.0, 0.0, {}
    for t, a, v, hp, hmax, d, ab in ev:
        if a in gs and v not in gs and v in hero and hero[v] != GEIST:
            tot += d
            if ab == SE:
                se += d
                hits.append((d / hmax, (hp + d) / hmax, last.get(a, 1.0)))
        if hmax:
            last[v] = hp / hmax
    return mid, casts, hits, se, tot


def main():
    files = sorted(os.path.join(CT.FIGHTS, f) for f in os.listdir(CT.FIGHTS) if f.endswith(".ndjson.gz"))
    by = collections.defaultdict(lambda: [0, [], 0.0, 0.0])
    with Pool(4) as p:
        for r in p.imap_unordered(match_rows, files):
            if r is None:
                continue
            for row in ("all", "even" if r[0] % 2 == 0 else "odd"):
                b = by[row]
                b[0] += r[1]
                b[1] += r[2]
                b[2] += r[3]
                b[3] += r[4]
    for row in ("all", "even", "odd"):
        casts, hits, se, tot = by[row]
        print(f"{row:4s} casts {casts:4d}  hits {len(hits):4d}  hits/cast {len(hits) / max(1, casts):.3f}  "
              f"loss/max hp median {statistics.median(h[0] for h in hits):.3f} mean {statistics.mean(h[0] for h in hits):.3f}  "
              f"target before {statistics.median(h[1] for h in hits):.3f}  Geist {statistics.median(h[2] for h in hits):.3f}  "
              f"SE share of hero dmg {se / tot:.3f}")


if __name__ == "__main__":
    main()
