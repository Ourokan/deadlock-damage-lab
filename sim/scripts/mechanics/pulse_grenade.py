"""Paradox's Pulse Grenade in real fights (Phantom+ replays; Mechanics.pulse_hits).

The sim kept the time-slowed target inside the grenade for every pulse (5, 7 at T3): each landed throw dealt every
pulse and stacked the damage amp 5-7 times. Per real throw (cast rows from cast_timing raw, the hero's Pulse Grenade
DamageEvents in the next PULSE_WIN s from fight_length raw), a victim's pulses are the events on the 0.8 s pulse grid
from its first hit (+-3 ticks, size within 0.75-1.35x of the first: the small events between are the amp, which the
game books under Pulse Grenade too). Per match-fraction bin: the share of throws that hit a hero, the heroes per
landed throw and the pulses on the throw's main victim (the one hit most); the amp booked under Pulse Grenade (events
on the tick of another of Paradox's hits on the same victim) and its size per hit (median ~0.08 = 2 stacks).

usage: python3 -I pulse_grenade.py [--write] [fight_length raw dir] [cast_timing raw dir]
--write: data/pulse_hits.json (each bin's survival P(main victim takes > i pulses | landed), i = 0..6, at Paradox's
median net worth at the bin's middle in phantom_sample).
"""
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
PARADOX = 10
PULSE = 58655583
INTERVAL = 0.8 * T
PULSE_WIN = 6.5
MAX_PULSES = 7
BINS = (0.0, 0.25, 0.5, 0.75, 1.01)


def victim_pulses(ev):
    """pulses on the 0.8 s grid from the best anchor among one victim's [(tick, dmg)] of a throw"""
    best = 0
    for a, xa in ev:
        if xa < 10:
            continue
        k = sum(1 for m in range(MAX_PULSES)
                if any(abs(t - (a + m * INTERVAL)) <= 3 and 0.75 * xa <= x <= 1.35 * xa for t, x in ev))
        best = max(best, k)
    return best


def throws(fl, ct):
    """per Paradox throw: (match fraction, [pulses per victim hit]); and the amp totals"""
    out, amp = [], collections.Counter()
    ratios = []
    for f in sorted(os.listdir(fl)):
        if not os.path.exists(os.path.join(ct, f)):
            continue
        rows = [r for r in (json.loads(x) for x in gzip.open(os.path.join(fl, f))) if r.get("s")]
        hero = {r["a"]: int(r["s"]) for r in rows if r["k"] == "ctl"}
        dmg = sorted((r for r in rows if r["k"] == "dmg"), key=lambda r: r["tick"])
        if not dmg:
            continue
        t0, t1 = dmg[0]["tick"], dmg[-1]["tick"]
        casts = [json.loads(x) for x in gzip.open(os.path.join(ct, f))]
        for p in (p for p, h in hero.items() if h == PARADOX):
            mine = [r for r in dmg if r["a"] // 100000 == p and r["a"] % 100000 in hero]
            other = collections.Counter()
            for r in mine:
                if int(r["s"].split("|")[0]) != PULSE:
                    other[r["tick"], r["a"]] += r["v"]
            ev = []
            for r in mine:
                if int(r["s"].split("|")[0]) == PULSE:
                    ev.append((r["tick"], r["a"] % 100000, r["v"]))
                    amp["pulse"] += r["v"]
                    if (r["tick"], r["a"]) in other:
                        amp["amp"] += r["v"]
                        ratios.append(r["v"] / other[r["tick"], r["a"]])
            for c in sorted(c["tick"] for c in casts if c["a"] == p and int(c["s"]) == PULSE):
                byv = collections.defaultdict(list)
                for t, v, x in ev:
                    if c <= t <= c + PULSE_WIN * T:
                        byv[v].append((t, x))
                hits = [k for k in (victim_pulses(e) for e in byv.values()) if k]
                out.append(((c - t0) / max(1, t1 - t0), hits))
    return out, amp, ratios


def main():
    args = [a for a in sys.argv[1:] if a != "--write"]
    fl = args[0] if args else "/mnt/project-files/analysis/work/fight_length/raw"
    ct = args[1] if len(args) > 1 else "/mnt/project-files/analysis/work/cast_timing/raw"
    out, amp, ratios = throws(fl, ct)
    print(f"{len(out)} throws; amp booked under Pulse Grenade {amp['amp'] / amp['pulse']:.3f} of its damage, "
          f"amp / hit median {statistics.median(r for r in ratios if r < 0.5):.3f}")
    nws = median_nw([(lo + hi) / 2 for lo, hi in zip(BINS, BINS[1:])], hero=PARADOX)
    points = []
    for lo, hi in zip(BINS, BINS[1:]):
        g = [h for fr, h in out if lo <= fr < hi]
        land = [h for h in g if h]
        main_k = [max(h) for h in land]
        surv = [round(sum(1 for k in main_k if k > i) / len(main_k), 4) for i in range(MAX_PULSES)]
        print(f"{lo:.2f}-{hi:.2f}: throws {len(g)}, landed {len(land) / len(g):.2f}, heroes per landed "
              f"{statistics.mean(len(h) for h in land):.2f}, main victim pulses {statistics.mean(main_k):.2f} "
              f"survival {surv}")
        points.append([nws[(lo + hi) / 2], surv])
    if "--write" in sys.argv:
        fn = os.path.join(HERE, "..", "..", "data", "pulse_hits.json")
        with open(fn, "w") as fh:
            json.dump({"source": f"{len(out)} Pulse Grenade throws in Phantom+ replays (scripts/mechanics/pulse_grenade.py)",
                       "note": "P(the throw's main victim takes more than i pulses | it hit a hero), i = 0..6, by "
                               "match fraction bin at Paradox's median net worth there (Mechanics.pulse_hits)",
                       "points": points}, fh, indent=1)
        print("wrote", fn)


if __name__ == "__main__":
    main()
