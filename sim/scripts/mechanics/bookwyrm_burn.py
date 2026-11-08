"""Paige's Bookwyrm burn per victim in real games, by the caster's net worth (2026-11-08).

The sim burned every Bookwyrm victim for TRAIL_UPTIME (0.5) of GroundFlameDuration plus the DebuffDuration linger:
3 s (10 ticks) at T0-T1, 4 s at T2+, at every phase of the match. The damage audit had Bookwyrm 1.5x its real share
in the lane fifth of the match (Captivating Read 2x) while matching later on.

Replays (the cast_timing + fight_length replays, Phantom+, 54 matches with a Paige): for each Bookwyrm cast, the enemy
heroes its DamageEvents hit within 10 s (before her next cast); per victim the events after the first are trail ticks.
Uptime = ticks x TickRate / GroundFlameDuration at the cast's tier (from the player's ability events). Real victims
stand in the fire 0.20 of the flame in the lane and 0.27-0.30 later (lane fights are 1v1 with room to step out; later
fights add teammates' crowd control). The sim keeps the formula's tier terms (T2 flame +2 s, T3 DPS) and burns each
victim for flame x uptime(net worth) with no linger (Mechanics.bookwyrm_burn, bookworm.burn_uptime).

usage: python3 -I scripts/mechanics/bookwyrm_burn.py [--half 0|1] [--write]   (writes data/bookwyrm_burn.json)
"""
import bisect
import collections
import gzip
import json
import math
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (ROOT, os.path.join(ROOT, "scripts"), os.path.join(ROOT, "scripts", "cast_timing"),
          os.path.join(ROOT, "scripts", "fight_length")):
    sys.path.insert(0, p)
import fit_cast_timing as CT  # noqa: E402
import fit_length as FL  # noqa: E402
import opener_timing as OT  # noqa: E402
from deadsim import game  # noqa: E402

CLS = "ability_bookworm_dragonfire"
WINDOW = 10.0   # s after the cast its hits are counted (or to the next cast)
BINS = (0, 5000, 10000, 15000, 22000, 30000, 10 ** 9)   # caster net worth
OUT = os.path.join(ROOT, "data", "bookwyrm_burn.json")


def victims(half=None):
    """[(net worth, tier, ticks)] per (Bookwyrm cast, enemy hero it hit)."""
    G = game()
    H = G.hero("Paige")
    ab = next(a for a in H.abilities if a.class_name == CLS)
    mids = {f.split(".")[0] for f in os.listdir(CT.CASTS) if f.endswith(".ndjson.gz")}
    mids &= {f.split(".")[0] for f in os.listdir(CT.FIGHTS) if f.endswith(".ndjson.gz")}
    if half is not None:
        mids = {x for x in mids if int(x) % 2 == half}
    sample = FL.load_sample(CT.SAMPLE, mids)
    out = []
    for mid in sorted(mids):
        m = sample.get(mid)
        by_hero = {p["hero_id"]: p for p in m["players"]} if m else {}
        if H.id not in by_hero:
            continue
        p = by_hero[H.id]
        hero, ev = OT.read(os.path.join(CT.FIGHTS, f"{mid}.ndjson.gz"))
        pawn = next((k for k, v in hero.items() if v == H.id), None)
        cr = CT.real_casts([json.loads(x) for x in gzip.open(os.path.join(CT.CASTS, f"{mid}.ndjson.gz"), "rt")])
        off = statistics.median(r["tick"] / CT.T - r["v"] for r in cr) if cr else 0.0
        cs = sorted(r["tick"] / CT.T for r in cr if r["a"] == pawn and int(r["s"]) == ab.id)
        hs = []
        for e in ev:
            pv = by_hero.get(hero.get(e[2]))
            if e[1] == pawn and e[6] == ab.id and pv is not None and pv["team"] != p["team"]:
                hs.append((e[0], e[2]))
        ups = sorted(bt for i, bt, _, _ in p["items"] if i == ab.id)   # first = unlock, later = upgrades
        cache = {}
        for k, c in enumerate(cs):
            end = min(c + WINDOW, cs[k + 1] if k + 1 < len(cs) else 1e18)
            per = collections.Counter(v for _, v in hs[bisect.bisect_left(hs, (c,)):bisect.bisect_left(hs, (end,))])
            if not per:
                continue
            nw = CT.build_cols(p, c - off, m, cache)[1]
            tier = max(0, min(3, bisect.bisect_right(ups, c - off) - 1))
            out += [(nw, tier, n - 1) for n in per.values()]
    return out


def flame(tier):
    """GroundFlameDuration at the tier (T2 +2 s)."""
    ab = next(a for a in game().hero("Paige").abilities if a.class_name == CLS)
    d = ab.props["GroundFlameDuration"]
    for t, up in enumerate(ab.upgrades[:tier]):
        d += up.get("GroundFlameDuration", 0.0)
    return d


def bins(rows):
    tick = next(a for a in game().hero("Paige").abilities if a.class_name == CLS).props["TickRate"]
    out = []
    for lo, hi in zip(BINS, BINS[1:]):
        r = [x for x in rows if lo <= x[0] < hi]
        if r:
            out.append({"net_worth": round(statistics.mean(x[0] for x in r)),
                        "uptime": round(statistics.mean(x[2] * tick / flame(x[1]) for x in r), 4),
                        "ticks": round(statistics.mean(x[2] for x in r), 2), "victims": len(r)})
    return out


def main():
    args = sys.argv[1:]
    half = int(args[args.index("--half") + 1]) if "--half" in args else None
    rows = victims(half)
    b = bins(rows)
    for x in b:
        print(x)
    if "--write" in args:
        json.dump({"source": "scripts/mechanics/bookwyrm_burn.py (cast_timing + fight_length replays, Phantom+)",
                   "note": "Bookwyrm trail ticks per victim x TickRate / GroundFlameDuration at the cast's tier, by "
                           "caster net worth (linear in ln net worth between bins, flat outside)",
                   "sim_before": "TRAIL_UPTIME 0.5 x flame + DebuffDuration 1.5 s (1.0 of the flame at T0-T1, 0.8 at T2+)",
                   "bins": b}, open(OUT, "w"), indent=1)
        print("->", OUT)


if __name__ == "__main__":
    main()
