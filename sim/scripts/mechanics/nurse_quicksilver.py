"""Nurse Harrow's Leech Therapy in Phantom+ replays: is its landing factor above 1 bigger leeches or more casts?

The sim's Leech Therapy factor (landing x length_corr, data/landing_rates_mech.json) is ~2.26, while the audit read
Quicksilver Reload (imbued on Leech Therapy: in these replays 481 of 483 Nurse Quicksilver procs land in the same
tick as a Leech Therapy hit) 2.2x under per gun on 226 Nurse holders. Quicksilver spends one charge per cast, so if
the factor stood for bigger leeches the item would read right; it reads ~1 / factor, as if real Nurses cast ~2x as
often. This prints, from the replays' hero-on-hero DamageEvents:

- leech streams (one victim's Leech Therapy ticks, gaps < 1.2 s): damage and length per stream (formula-sized:
  DPS x AbilityDuration = 115 + spirit scaling, 5 s);
- victims per cast (streams starting within 3 s of each other);
- Quicksilver procs: which of the Nurse's own sources hit in the same tick, victims per proc.

Result (2026-11-08, 235 replays with a Nurse in analysis/work/fight_length/raw): streams median 136 dmg over 4.6 s
(mean 165), 1.16 victims per cast, Quicksilver 1.12 victims per proc: real casts are formula-sized, so the factor is
more casts than the sim's cadence lands, and items_fx.LANDING_PROCS scales Quicksilver's charge damage by it.

usage: python3 -I nurse_quicksilver.py <raw dir>   (fetch_fights.py extracts)
"""
import collections
import glob
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fight_length"))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from opener_timing import read, sources  # noqa: E402
from deadsim.data import game  # noqa: E402

NURSE = 87
LEECH = 267712790        # ability_nurse_leech_therapy (MurmurHash2 of the class name, seed 0x31415926)
QSR = 84321454           # upgrade_quick_silver


def main(raw):
    names = sources(game())
    streams, lengths, per_cast, with_src, victims = [], [], [], collections.Counter(), []
    procs = casts = 0
    for fn in sorted(glob.glob(os.path.join(raw, "*.ndjson.gz"))):
        hero, ev = read(fn)
        for me in (e for e, h in hero.items() if h == NURSE):
            by_victim = collections.defaultdict(list)
            q = []
            for i, (t, a, v, hp, mx, d, ab) in enumerate(ev):
                if a != me:
                    continue
                if ab == LEECH:
                    by_victim[v].append((t, d))
                elif ab == QSR:
                    q.append((t, v))
                    near = {names.get(e[6], ("?", "other"))[1] for e in ev[max(0, i - 30):i + 30]
                            if e[1] == me and abs(e[0] - t) < 0.05 and e[6] != QSR}
                    with_src["Leech Therapy" if any("Leech" in n for n in near) else "other"] += 1
            st = []
            for v, hits in by_victim.items():
                cur = None
                for t, d in hits:
                    if cur and t - cur[1] < 1.2:
                        cur[1], cur[2] = t, cur[2] + d
                    else:
                        cur = [t, t, d]
                        st.append(cur)
            st.sort()
            for s in st:
                streams.append(s[2])
                lengths.append(s[1] - s[0])
            cs = []
            for s in st:
                if cs and s[0] - cs[-1][0] < 3:
                    cs[-1][1] += 1
                else:
                    cs.append([s[0], 1])
            per_cast += [n for _, n in cs]
            if q:
                procs += len(q)
                casts += len(cs)
                groups = []
                for t, v in q:
                    if groups and t - groups[-1][0] < 3:
                        groups[-1][1].add(v)
                    else:
                        groups.append([t, {v}])
                victims += [len(g[1]) for g in groups]
    print(f"leech streams {len(streams)}: damage median {statistics.median(streams):.0f} mean {statistics.mean(streams):.0f},"
          f" length median {statistics.median(lengths):.2f} s; victims per cast {statistics.mean(per_cast):.2f}")
    print(f"Quicksilver procs {procs} (same tick as: {dict(with_src)}), victims per proc {statistics.mean(victims):.2f},"
          f" procs per Leech cast over the whole match (holders) {procs / max(1, casts):.2f}")


if __name__ == "__main__":
    main(sys.argv[1])
