"""Viscous' ability hits and the items riding them in Phantom+ replays (validation/README.md "Viscous: procs per
hit", items_fx.LANDING_PROCS, Mechanics.charge_gaps, viscous.REAL_HITS).

Per Viscous holding the item (from 3 s before its first proc): Mystic Burst / Tankbuster damage by the hit that
set it off (same victim, within 2 ticks), per damage of that ability, and the size of the Splatter hits that set
them off; Goo Ball hits per hero per cast (hits within 12 s of the cast's first) and the gap between re-hits;
Spirit Snatch procs per landed Puddle Punch cast (hits more than 0.5 s apart) by the gap since the one before.

usage: python3 -I viscous_procs.py [raw dir ...]   (default: project folder analysis/work/fight_length/raw and
analysis/work/viscous_replays/raw, DamageEvent rows from scripts/fight_length/fetch_fights.py)
"""
import collections
import glob
import gzip
import json
import os
import sys

T = 64
VISCOUS = 35
SPLATTER, GOO_BALL, PUNCH = 3247040238, 4206531918, 1020817390
EXPRESS, GUN, ALT = 690458959, 3413773852, 3819944797
MYSTIC_BURST, TANKBUSTER, SNATCH = 1998374645, 2121044373, 3190916303
NAMES = {SPLATTER: "Splatter", GOO_BALL: "Goo Ball", PUNCH: "Puddle Punch", EXPRESS: "Express Shot", GUN: "gun",
         ALT: "alt fire"}
ITEMS = {MYSTIC_BURST: "Mystic Burst", TANKBUSTER: "Tankbuster"}


def read(fn):
    hero, ev = {}, collections.defaultdict(list)
    for line in gzip.open(fn, "rt"):
        r = json.loads(line)
        if r["k"] == "ctl":
            hero[r["a"]] = int(r["s"])
        elif r["k"] == "dmg" and r.get("s"):
            ev[r["a"] // 100000].append((r["tick"], r["a"] % 100000, int(r["s"].split("|")[0]), r["v"]))
    return hero, ev


def pct(x, qs=(0.1, 0.25, 0.5, 0.75)):
    x = sorted(x)
    return [round(x[int(q * len(x))]) for q in qs] if x else None


def main():
    dirs = sys.argv[1:] or ["/mnt/project-files/analysis/work/fight_length/raw/",
                            "/mnt/project-files/analysis/work/viscous_replays/raw/"]
    item, own, size = collections.Counter(), collections.Counter(), collections.defaultdict(list)
    ball_hits, ball_victims, rehit = collections.Counter(), [], []
    punch = collections.Counter()
    seen, players = set(), 0
    for d in dirs:
        for fn in sorted(glob.glob(os.path.join(d, "*.ndjson.gz"))):
            mid = os.path.basename(fn).split(".")[0]
            if mid in seen:
                continue
            seen.add(mid)
            hero, ev = read(fn)
            for pawn, es in ev.items():
                if hero.get(pawn) != VISCOUS:
                    continue
                players += 1
                es = sorted(e for e in es if e[1] in hero and hero[e[1]] != VISCOUS)
                for iid, it in ITEMS.items():
                    procs = [i for i, e in enumerate(es) if e[2] == iid]
                    if not procs:
                        continue
                    t0 = es[procs[0]][0] - 3 * T
                    for e in es:
                        if e[0] >= t0 and e[2] not in ITEMS:
                            own[it, NAMES.get(e[2], "other")] += e[3]
                    for i in procs:
                        e = es[i]
                        cand = [f for f in es[max(0, i - 40):i + 40]
                                if f[1] == e[1] and abs(f[0] - e[0]) <= 2 and f[2] not in ITEMS]
                        cand.sort(key=lambda f: (abs(f[0] - e[0]), -f[3]))
                        src = NAMES.get(cand[0][2], "other") if cand else "none"
                        item[it, src] += e[3]
                        if src == "Splatter":
                            size[it].append(cand[0][3])
                hits = [e for e in es if e[2] == GOO_BALL]
                i = 0
                while i < len(hits):
                    j = i
                    while j < len(hits) and hits[j][0] - hits[i][0] < 12 * T:
                        j += 1
                    by = collections.defaultdict(list)
                    for e in hits[i:j]:
                        by[e[1]].append(e[0])
                    ball_victims.append(len(by))
                    for ts in by.values():
                        ball_hits[len(ts)] += 1
                        rehit += [(b - a) / T for a, b in zip(ts, ts[1:])]
                    i = j
                snatch = [e[0] for e in es if e[2] == SNATCH]
                if snatch:
                    casts = []
                    for t in sorted(e[0] for e in es if e[2] == PUNCH and e[0] >= snatch[0] - 10 * T):
                        if not casts or t - casts[-1] >= 0.5 * T:
                            casts.append(t)
                    prev = None
                    for t in casts:
                        b = "under 6 s" if prev is not None and t - prev < 6 * T else "6 s+"
                        punch[b, "casts"] += 1
                        punch[b, "snatch"] += sum(1 for s in snatch if 0 <= s - t <= 0.3 * T)
                        prev = t
    print(f"{len(seen)} replays, {players} Viscous")
    for it in ITEMS.values():
        tot = sum(v for (i, _), v in item.items() if i == it) or 1.0
        print(f"{it}: {tot:.0f} damage by the hit that set it off (share, per damage of that source):")
        for (i, s), v in sorted(item.items(), key=lambda x: -x[1]):
            if i == it and v / tot >= 0.01:
                print(f"   {s:14s} {v / tot:.3f}  {v / max(1.0, own[it, s]):.3f}")
        print(f"   Splatter hits that set it off, dealt 10/25/50/75th pct: {pct(size[it])}")
    n = sum(ball_hits.values()) or 1
    print(f"Goo Ball: {len(ball_victims)} casts, {sum(ball_victims) / max(1, len(ball_victims)):.2f} heroes per cast, "
          f"{sum(k * v for k, v in ball_hits.items()) / n:.2f} hits per hero {sorted(ball_hits.items())}, "
          f"re-hit gap 25/50/75th pct {[round(x, 2) for x in (sorted(rehit)[int(q * len(rehit))] for q in (0.25, 0.5, 0.75))] if rehit else None}")
    for b in ("6 s+", "under 6 s"):
        c = punch[b, "casts"]
        print(f"Puddle Punch {b} after the last: {c} landed casts, {punch[b, 'snatch'] / max(1, c):.2f} Spirit Snatch each")


if __name__ == "__main__":
    main()
