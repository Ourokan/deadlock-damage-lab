"""Rem's Tag Along in real fights (Phantom+ replays; Mechanics.tag_along).

Rem napping on an ally (Tag Along) is the pawn state bit ATTACH_BIT (on for every cast: in 122538863 it turns on
within 0.6 s of all 40 casts' cast delay, and never otherwise). Combat time is every second within PAD s of hero
damage dealt or taken by Rem. Per match-fraction bin: the share of Rem's combat seconds he is attached; overall: his
damage per combat second by source and the damage he takes, attached vs not, and the attach lengths.

usage: python3 -I rem_tag_along.py [--write] [cc_time raw dir] [fight_length raw dir]
--write: data/tag_along.json (each bin's share at Rem's median net worth at the bin's middle in phantom_sample, and
the attach length quantiles). Pawn states: scripts/fight_length/fetch_cc.py (default the project folder
analysis/work/cc_time/raw).
"""
import bisect
import collections
import gzip
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from krill_burrow import median_nw  # noqa: E402

T = 64.0
REM = 79
ATTACH_BIT = 261
PAD = 2
BINS = (0.0, 0.25, 0.5, 0.75, 1.01)
QBINS = 20
SRC = {1961336982: "gun", 3692321247: "Pillow Toss", 2396527575: "Naptime", 536278136: "Lil Helpers"}
MELEE = {2247993425, 2573821048}   # light / heavy melee ability ids


def attached(states_fn, pawn):
    """[(start s, end s)] with ATTACH_BIT on, and the last state tick (s)"""
    iv, start, last = [], None, 0.0
    w, b = divmod(ATTACH_BIT, 64)
    for line in gzip.open(states_fn, "rt"):
        r = json.loads(line)
        if r["k"] != "st" or r["a"] != pawn:
            continue
        m = [int(x) for x in r["s"].split("#")[0].split(",") if x]
        on = len(m) > w and (m[w] >> b) & 1
        t = r["tick"] / T
        last = max(last, t)
        if on and start is None:
            start = t
        elif not on and start is not None:
            iv.append((start, t))
            start = None
    return iv, last


def main():
    args = [a for a in sys.argv[1:] if a != "--write"]
    sd = args[0] if args else "/mnt/project-files/analysis/work/cc_time/raw"
    dd = args[1] if len(args) > 1 else "/mnt/project-files/analysis/work/fight_length/raw"
    secs = [collections.Counter() for _ in BINS[:-1]]
    dealt, taken, lens, n = collections.defaultdict(collections.Counter), collections.Counter(), [], 0
    for fn in sorted(os.listdir(dd)):
        sfn = os.path.join(sd, fn)
        if not os.path.exists(sfn):
            continue
        rows = [json.loads(x) for x in gzip.open(os.path.join(dd, fn), "rt")]
        rem = [r["a"] for r in rows if r["k"] == "ctl" and r["s"] == str(REM)]
        if not rem:
            continue
        rem = rem[0]
        iv, last = attached(sfn, rem)
        if not last:
            continue
        n += 1
        starts = [a for a, _ in iv]

        def on(t):
            i = bisect.bisect_right(starts, t) - 1
            return i >= 0 and iv[i][0] <= t < iv[i][1]
        dm = [(r["tick"] / T, r["a"] // 100000, r["a"] % 100000, int(r["s"].split("|")[0]), r["v"])
              for r in rows if r["k"] == "dmg" and "s" in r]
        combat = set()
        for t, a, v, _, _ in dm:
            if rem in (a, v):
                combat.update(range(int(t) - PAD, int(t) + PAD + 1))
        for s in combat:
            b = next(i for i in range(len(BINS) - 1) if BINS[i] <= min(1.0, s / last) < BINS[i + 1])
            secs[b]["att" if on(s + 0.5) else "free"] += 1
        for t, a, v, ab, x in dm:
            st = "att" if on(t) else "free"
            if a == rem:
                dealt[st][SRC.get(ab, "melee" if ab in MELEE else "items/other")] += x
            elif v == rem:
                taken[st] += x
        lens += [e - s for s, e in iv if any(int(s) <= c <= int(e) for c in combat)]
    tot = collections.Counter()
    for c in secs:
        tot.update(c)
    share = [c["att"] / max(1, sum(c.values())) for c in secs]
    print(f"{n} matches with Rem, {sum(tot.values())} combat s, attached {tot['att'] / sum(tot.values()):.3f}")
    print("attached share of combat s by match fraction:",
          " ".join(f"{BINS[i]:.2f}-{min(1, BINS[i + 1]):.2f} {x:.3f}" for i, x in enumerate(share)))
    for st in ("free", "att"):
        print(f"{st:5s} dealt/s " + ", ".join(f"{k} {v / tot[st]:.1f}" for k, v in dealt[st].most_common())
              + f"; taken/s {taken[st] / tot[st]:.1f}")
    lens.sort()
    q = [round(lens[min(len(lens) - 1, int((i + 0.5) / QBINS * len(lens)))], 2) for i in range(QBINS)]
    print(f"{len(lens)} attaches in fights, median {statistics.median(lens):.1f} s, quantiles {q}")
    if "--write" in sys.argv:
        mids = [(BINS[b] + min(1.0, BINS[b + 1])) / 2 for b in range(len(BINS) - 1)]
        nw = median_nw(mids, REM)
        out = {"source": f"{n} Phantom+ replays with Rem, {sum(tot.values())} combat s (scripts/mechanics/rem_tag_along.py)",
               "note": "share of Rem's combat seconds he is attached to an ally (Tag Along), by match fraction bin at "
                       "Rem's median net worth there; attach lengths (s) as QBINS quantiles (Mechanics.tag_along)",
               "points": [[nw[mids[b]], round(share[b], 4)] for b in range(len(mids))],
               "lengths": q}
        json.dump(out, open(os.path.join(HERE, "..", "..", "data", "tag_along.json"), "w"), indent=1)
        print("wrote data/tag_along.json")


if __name__ == "__main__":
    main()
