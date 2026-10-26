"""How fast real Phantom+ McGinnis players place Mini Turrets inside a fight, from replays: data/turret_gaps.json.

The sim casts every Mini Turret charge the moment it is ready: from tier 2 on (3 charges, 3 s between charges) it
drops three turrets in the first ~6 s of every duel. Real players place far fewer: own turrets placed from 1 s before
a pair fight's first hit, fights lasting 10 s, by 10 s into the fight: lane (< 15 min) 0.89, mid 1.11, late 1.13
against the sim's ~2.6 in every phase (real gaps to the next one: median ~9-11 s, 2-9% within 2 s); the sim put 65%
of her damage on the turret in the lane against real 45% (validation/README.md "McGinnis's Mini Turret").

Input: the summons replays (summons/fetch_summons.py: turret entities with their owner and create tick, and every
hero-vs-hero DamageEvent). Wall turrets (Spectral Wall tier 3) are created in a group within a few ticks and are dropped.
Fights: pair fights as fit_cast_timing.py (two enemy heroes trading, gaps < GAP_S s, >= MIN_HITS hits both ways).
For each own turret placed in a fight (from PRE_S before its first hit to its last), the time to the next one
placed in that fight, Kaplan-Meier with the fight's end censoring.

Output: per game phase (match time: lane < LANE_MIN, late >= LATE_MIN, McGinnis's median times to the net worth
bounds of mechanics.LENGTH_PHASES in the Phantom+ sample), QBINS equal-probability gaps (s) to the next placement
(None = no other turret in the fight by HORIZON). Read by deadsim/heroes/forge.py (MiniTurret, TURRET_PACING): after
each turret a fight holds the next one by a gap drawn from it, as well as for the charge to be ready.

usage: python3 -I turret_gaps.py [--raw DIR] [--write]
"""
import bisect
import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "summons"))
import summon_stats as SS  # noqa: E402

RAW = "/mnt/project-files/analysis/work/summons/raw/"
OUT = os.path.join(ROOT, "data", "turret_gaps.json")
MCGINNIS = 8
TICKS = SS.TICKS
GAP_S = 5.0          # as fit_length.GAP_S
MIN_HITS = 4         # as fit_length.MIN_HITS
PRE_S = 1.0          # as fit_cast_timing.PRE_S
LANE_MIN, LATE_MIN = 15.0, 30.0   # McGinnis's median minutes to 10k / 27k net worth (phantom_sample)
HORIZON = 20.0
GRID = [0.5 * k for k in range(int(HORIZON / 0.5) + 1)]
QBINS = 20
GROUP_S = 1.0       # turrets this close are one Spectral Wall's (a placed turret's next charge is >= 3 s away)


def km(rows):
    """rows (gap s or None, censor s): P(next placement by t) on GRID (Kaplan-Meier)."""
    ev = sorted((u if u is not None else d, u is not None) for u, d in rows)
    n, i, surv, out = len(ev), 0, 1.0, []
    for t in GRID:
        while i < n and ev[i][0] <= t:
            j, c = i, 0
            while j < n and ev[j][0] == ev[i][0]:
                c += ev[j][1]
                j += 1
            surv *= 1.0 - c / (n - i)
            i = j
        out.append(round(1.0 - surv, 4))
    return out


def quantile(curve, p):
    k = next((k for k in range(len(curve)) if curve[k] >= p), None)
    if k is None:
        return None
    if k == 0:
        return 0.0
    lo = curve[k - 1]
    return GRID[k] - 0.5 * (curve[k] - p) / max(1e-9, curve[k] - lo)


def phase(t_s):
    m = t_s / 60
    return "lane" if m < LANE_MIN else "mid" if m < LATE_MIN else "late"


def match_rows(fn):
    """{phase: [(gap to the next own turret or None, time left in the fight)]}, {phase: [turrets by 10 s]}."""
    rows = SS.load(fn)
    hero_of = {r["a"]: int(r["s"]) for r in rows["ctl"] if r.get("s") and r["s"] != "0"}
    team_of = {r["a"]: int(r["s"]) for r in rows["pawn"] if r.get("s")}
    mcg = [pw for pw, h in hero_of.items() if h == MCGINNIS]
    gaps, by10 = collections.defaultdict(list), collections.defaultdict(list)
    if not mcg:
        return gaps, by10
    ins = [x for x in SS.instances(rows, hero_of, team_of) if x["label"] == "mcginnis_turret"]
    for pw in mcg:
        mine = [x for x in ins if x["owner"] == pw]
        ts = sorted(x["t0"] / TICKS for x in mine)
        # wall turrets come in groups a few ticks apart; a placed one is at least the charge gap from the next
        own = [t for i, t in enumerate(ts) if (i == 0 or t - ts[i - 1] > GROUP_S)
               and (i + 1 == len(ts) or ts[i + 1] - t > GROUP_S)]
        pairs = collections.defaultdict(list)
        for r in rows["dmg"]:
            a, v = divmod(r["a"], 100000)
            if team_of.get(a) == team_of.get(v):
                continue
            if a == pw:
                pairs[v].append((r["tick"] / TICKS, 0))
            elif v == pw:
                pairs[a].append((r["tick"] / TICKS, 1))
        for es in pairs.values():
            es.sort()
            runs = []
            for e in es:
                if not runs or e[0] - runs[-1][-1][0] > GAP_S:
                    runs.append([])
                runs[-1].append(e)
            for f in runs:
                if len(f) < MIN_HITS or len({e[1] for e in f}) < 2:
                    continue
                t0, t1 = f[0][0], f[-1][0]
                ph = phase(t0)
                cs = [c for c in own[bisect.bisect_left(own, t0 - PRE_S):] if c <= t1]
                for i, c in enumerate(cs):
                    gaps[ph].append((cs[i + 1] - c if i + 1 < len(cs) else None, t1 - c))
                if t1 - t0 >= 10:
                    by10[ph].append(sum(1 for c in cs if c <= t0 + 10))
    return gaps, by10


def main():
    args = sys.argv[1:]
    raw = args[args.index("--raw") + 1] if "--raw" in args else RAW
    gaps, by10 = collections.defaultdict(list), collections.defaultdict(list)
    n = 0
    for fn in sorted(glob.glob(os.path.join(raw, "*.ndjson"))):
        g, b = match_rows(fn)
        n += bool(g)
        for k, v in g.items():
            gaps[k] += v
        for k, v in b.items():
            by10[k] += v
    out = {"source": f"{n} Phantom+ replays with McGinnis (summons/fetch_summons.py), pair fights "
                     "(sim/scripts/mechanics/turret_gaps.py)",
           "note": "per game phase (match time lane < 15 min, late >= 30 min): equal-probability gaps (s) from one own "
                   "Mini Turret placed in a fight to the next (null = none by 20 s), Kaplan-Meier with the fight's end "
                   "censoring; wall turrets dropped",
           "phases": {}}
    for ph in ("lane", "mid", "late"):
        curve = km(gaps[ph])
        q = [None if (b + 0.5) / QBINS > curve[-1] else round(quantile(curve, (b + 0.5) / QBINS), 2)
             for b in range(QBINS)]
        out["phases"][ph] = {"turrets": len(gaps[ph]), "by10_mean": round(sum(by10[ph]) / max(1, len(by10[ph])), 2),
                             "next_by": {str(t): curve[GRID.index(t)] for t in (2.0, 4.0, 6.0, 10.0, 20.0)},
                             "gaps": q}
        print(ph, json.dumps(out["phases"][ph]))
    if "--write" in args:
        with open(OUT, "w") as fh:
            json.dump(out, fh, indent=1)
        print("wrote", OUT)


if __name__ == "__main__":
    main()
