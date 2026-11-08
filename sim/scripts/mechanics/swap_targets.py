"""Whom real Lady Geists swap with: the hero they were fighting, or a fresh one (Mechanics.swap_fresh).

For each Soul Exchange hit on an enemy hero in the replays' hero-on-hero DamageEvents: did Geist damage that hero in
the 5 s before, was it the hero she damaged most then (her duel target), did anyone damage it, and its health share
before the swap.

Result (2026-11-08, 134 swaps in 260 Phantom+ replays, analysis/work/fight_length/raw): Geist had hit the victim in
the 5 s before on 51% of swaps, it was her main target on only 32%, and 26% of victims took no damage from anyone in
those 5 s. Victims she hadn't hit sat at 0.94 of their health (median), the ones she had at 0.85. The sim's duel only
had its own target (0.78 at swap), so a gap of real size (ghost.SWAP_GAPS, median 0.6) opened late and Soul Exchange
read 1.3x under on 303 post-hotfix Geists; ghost.FRESH_HP is the 0.94.

usage: python3 -I swap_targets.py <raw dir>
"""
import collections
import glob
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fight_length"))
from opener_timing import read  # noqa: E402

GEIST = 4
SE = 1307289689   # ability_health_swap (MurmurHash2 of the class name, seed 0x31415926)
WINDOW = 5.0


def main(raw):
    rows = []
    for fn in sorted(glob.glob(os.path.join(raw, "*.ndjson.gz"))):
        hero, ev = read(fn)
        me = {e for e, h in hero.items() if h == GEIST}
        if not me:
            continue
        for i, (t, a, v, hp, mx, d, ab) in enumerate(ev):
            if ab != SE or a not in me:
                continue
            prior = [x for x in ev[max(0, i - 3000):i] if t - WINDOW <= x[0] < t]
            mine = sum(x[5] for x in prior if x[1] == a and x[2] == v)
            others = sum(x[5] for x in prior if x[2] == v and x[1] != a)
            by_victim = collections.Counter()
            for x in prior:
                if x[1] == a:
                    by_victim[x[2]] += x[5]
            top = by_victim.most_common(1)[0][0] if by_victim else None
            rows.append((mine > 0, top == v, mine == 0 and others == 0, (hp + d) / mx))
    n = len(rows) or 1
    print(f"swaps {len(rows)}: Geist hit the victim in the {WINDOW:.0f} s before {sum(r[0] for r in rows) / n:.2f}, "
          f"her main target {sum(r[1] for r in rows) / n:.2f}, nobody hit it {sum(r[2] for r in rows) / n:.2f}")
    for name, sel in (("hit by Geist", lambda r: r[0]), ("not hit by Geist", lambda r: not r[0])):
        s = [r[3] for r in rows if sel(r)]
        if s:
            print(f"  {name:17s} n {len(s):3d}  victim health before (median) {statistics.median(s):.2f}")


if __name__ == "__main__":
    main(sys.argv[1])
