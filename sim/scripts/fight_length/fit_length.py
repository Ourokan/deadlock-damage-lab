"""Real Phantom+ fight lengths from replays, for the sim's fight-length expectation (data/fight_length.json,
mechanics.length_weight).

Input: fetch_fights.py extracts (every hero-vs-hero DamageEvent with the victim's health after the hit, pawn ->
hero) and the validation sample they come from (net worth over time, death times to line the replay clock up with
the game clock).

A fight is a run of damage between two enemy heroes, either way, with no gap over GAP_S s: what a 1v1 duel in the
sim stands for (the sim duel is the hero and its main target trading until one dies). It ends either with one of
the two dying (a hit leaves the victim at 0 health) or with a disengage (no more damage between them: someone ran,
backed, turned to another target or the fight moved). The sim already ends a duel at a death, so what it misses is
the disengage: S(t) = P(the two are still trading t s in | nobody died yet), the Kaplan-Meier survival of the
disengage time with the death-ended fights censored at their death. The sim's expected damage over real fight
lengths is then each hit x S(its time) (Engine.length_w), which is exact when the disengage does not depend on the
sim's path (an assumption: real players back off more when losing).

Fights counted: runs with at least MIN_HITS hits and damage both ways (a single poke is not a duel; runs shorter than
that are mostly trooper-wave pokes the sim does not stand for). The share of real hero damage they hold is printed.

By game phase: the fight's net worth is the two fighters' mean net worth at its start (sample stats snapshots);
phases as the overall search's game_phase (lane < 10k, late > 27k).

Also printed: the real damage profile by time into the fight (share of fight damage in each 2 s slice), to compare
with the sim's (scripts/damage_audit.py --length).

usage: python3 -I fit_length.py <raw dir> [--sample validation/phantom_sample.jsonl.gz] [--write]
"""
import bisect
import collections
import glob
import gzip
import json
import math
import os
import random
import statistics
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
T = 64            # ticks per second
GAP_S = 5.0       # no damage between the two for this long = the fight is over
MIN_HITS = 4      # damage events in the run (both ways together)
STEP = 0.5        # s, grid of the survival curve
T_MAX = 30.0      # s, the curve's end (the overall search's fight cap)
PHASES = (("lane", 0, 10000), ("mid", 10000, 27000), ("late", 27000, math.inf))
BOOT = 200


def load_sample(path, mids):
    out = {}
    for line in gzip.open(path):
        m = json.loads(line)
        if str(m["match_id"]) in mids:
            out[str(m["match_id"])] = m
    return out


def nw_at(stats, t):
    """Net worth at game time t from the player's stats snapshots (linear, from 0 before the first)."""
    if not stats:
        return None
    ts = [s["time_stamp_s"] for s in stats]
    i = bisect.bisect_left(ts, t)
    if i == 0:
        return stats[0]["net_worth"] * max(0.0, t) / max(1, ts[0])
    if i >= len(ts):
        return stats[-1]["net_worth"]
    a, b = stats[i - 1], stats[i]
    return a["net_worth"] + (b["net_worth"] - a["net_worth"]) * (t - ts[i - 1]) / max(1, ts[i] - ts[i - 1])


def read(fn):
    hero, ev = {}, []
    for line in gzip.open(fn, "rt"):
        r = json.loads(line)
        if r["k"] == "ctl":
            hero[r["a"]] = int(r["s"])
        elif r["k"] == "dmg" and r.get("s"):
            ab, hp, hmax = r["s"].split("|")
            ev.append((r["tick"] / T, r["a"] // 100000, r["a"] % 100000, float(hp), float(hmax), r["v"]))
    ev.sort()
    return hero, ev


def clock_offset(ev, hero, m):
    """Replay seconds -> game seconds. Pauses add replay time, so the offset is a step function: each replay death
    (a hit to 0 health) is matched to the sample's nearest death of the same hero, a match counts when at least
    two other deaths share its gap (+-1.5 s), and a time t uses the gap of the last counted death before it (the
    first one before any). None when fewer than 3 deaths count."""
    slot = {p["hero_id"]: p for p in m["players"]}
    pts, dead = [], set()
    for t, a, v, hp, _, _ in ev:
        if hp > 0:
            dead.discard(v)
            continue
        if v in dead:
            continue
        dead.add(v)
        p = slot.get(hero.get(v))
        if p and p.get("deaths"):
            pts.append((t, min((t - d["t"] for d in p["deaths"]), key=abs)))
    good = [(t, g) for t, g in pts if sum(abs(g - h) < 1.5 for _, h in pts) >= 3]
    if len(good) < 3:
        return None
    ts = [t for t, _ in good]

    def off(t):
        return good[max(0, bisect.bisect_right(ts, t) - 1)][1]
    return off


def fights(fn, sample):
    """[(phase, net worth, duration s, ended by a death, hero ids (a, b), damage profile {slice: dmg}, damage)]."""
    mid = os.path.basename(fn).split(".")[0]
    m = sample.get(mid)
    hero, ev = read(fn)
    if m is None:
        return [], 0.0
    off = clock_offset(ev, hero, m)
    by_hero = {p["hero_id"]: p for p in m["players"]}
    pairs = collections.defaultdict(list)
    total = 0.0
    for e in ev:
        _, a, v = e[:3]
        pa, pv = by_hero.get(hero.get(a)), by_hero.get(hero.get(v))
        if pa is None or pv is None or pa["team"] == pv["team"]:
            continue
        total += e[5]
        pairs[min(a, v), max(a, v)].append(e)
    out = []
    for (x, y), es in pairs.items():
        runs = []
        for e in es:
            if not runs or e[0] - runs[-1][-1][0] > GAP_S:
                runs.append([])
            runs[-1].append(e)
        for f in runs:
            death = next((k for k, e in enumerate(f) if e[3] <= 0), None)
            if death is not None:
                f = f[:death + 1]
            dirs = {(e[1], e[2]) for e in f}
            if len(f) < MIN_HITS or len(dirs) < 2:
                continue
            t0 = f[0][0]
            dur = f[-1][0] - t0
            prof = collections.Counter()
            for e in f:
                prof[int((e[0] - t0) // 2)] += e[5]
            nw = None
            if off is not None:
                g = t0 - off(t0)
                v = [nw_at(by_hero[hero[z]]["stats"], g) for z in (x, y)]
                if None not in v:
                    nw = sum(v) / 2
            ph = None if nw is None else next(n for n, lo, hi in PHASES if lo <= nw < hi)
            out.append((ph, nw, dur, death is not None, (hero[x], hero[y]), prof, sum(e[5] for e in f)))
    return out, total


def km(rows, grid):
    """Kaplan-Meier survival of the disengage time at the grid times: rows (duration, died); a death censors."""
    rows = sorted(rows)
    n, i, s, out = len(rows), 0, 1.0, []
    at_risk = n
    for t in grid:
        while i < n and rows[i][0] < t:
            d, died = rows[i]
            j = i
            ends = cens = 0
            while j < n and rows[j][0] == d:
                cens += rows[j][1]
                ends += not rows[j][1]
                j += 1
            if at_risk > 0 and ends:
                s *= 1.0 - ends / at_risk
            at_risk -= ends + cens
            i = j
        out.append(s)
    return out


def quantile(curve, grid, q):
    """First grid time where the survival curve drops to q or below (None if it never does)."""
    return next((t for t, s in zip(grid, curve) if s <= q), None)


def main():
    args = sys.argv[1:]
    sample_path = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
    if "--sample" in args:
        sample_path = args[args.index("--sample") + 1]
        args.remove("--sample")
        args.remove(sample_path)
    raw = [a for a in args if not a.startswith("--")][0]
    files = sorted(glob.glob(os.path.join(raw, "*.ndjson.gz")))
    sample = load_sample(sample_path, {os.path.basename(f).split(".")[0] for f in files})
    rows, total, by_match = [], 0.0, collections.defaultdict(list)
    for fn in files:
        r, tot = fights(fn, sample)
        rows += r
        total += tot
        by_match[fn] = r
    grid = [k * STEP for k in range(int(T_MAX / STEP) + 1)]
    kept = sum(r[6] for r in rows)
    print(f"{len(files)} replays, {len(rows)} fights (>= {MIN_HITS} hits both ways, gaps < {GAP_S:.0f} s), "
          f"{kept / max(1, total):.0%} of hero damage; {sum(r[0] is None for r in rows)} without net worth")
    durs = [r[2] for r in rows]
    died = [r for r in rows if r[3]]
    print(f"length median {statistics.median(durs):.1f} s, mean {statistics.mean(durs):.1f} s, "
          f"{len(died) / len(rows):.0%} end in a death (median {statistics.median([r[2] for r in died]):.1f} s)")

    def curve(rs):
        return km([(r[2], r[3]) for r in rs], grid)

    out = {"source": f"{len(files)} Phantom+ replays, hero-vs-hero DamageEvent with victim health "
                     f"(scripts/fight_length/fit_length.py)",
           "gap_s": GAP_S, "min_hits": MIN_HITS, "step_s": STEP,
           "note": "survival[k] = P(the two are still trading at k*step_s s | nobody died): Kaplan-Meier of the "
                   "disengage time, deaths censored; the sim weighs each hit by it (mechanics.length_weight)",
           "phases": {}}
    mids = sorted(by_match)
    rng = random.Random(1)
    for name, lo, hi in (("all", -1, math.inf),) + PHASES:
        rs = [r for r in rows if (name == "all" or (r[1] is not None and lo <= r[1] < hi))]
        if len(rs) < 50:
            continue
        c = curve(rs)
        draws = []
        for _ in range(BOOT):
            pick = [r for f in rng.choices(mids, k=len(mids)) for r in by_match[f]
                    if name == "all" or (r[1] is not None and lo <= r[1] < hi)]
            draws.append(curve(pick))
        band = [(sorted(d[k] for d in draws)[int(0.025 * BOOT)], sorted(d[k] for d in draws)[int(0.975 * BOOT) - 1])
                for k in range(len(grid))]
        mean_len = sum(c) * STEP
        prof = collections.Counter()
        for r in rs:
            prof.update(r[5])
        ptot = sum(prof.values())
        row = {"fights": len(rs), "death_share": round(sum(r[3] for r in rs) / len(rs), 3),
               "median_s": round(statistics.median([r[2] for r in rs]), 2),
               "disengage_median_s": quantile(c, grid, 0.5), "disengage_mean_s": round(mean_len, 2),
               "survival": [round(v, 4) for v in c],
               "survival_95": [[round(a, 4), round(b, 4)] for a, b in band],
               "damage_by_2s": [round(prof.get(k, 0) / ptot, 4) for k in range(int(T_MAX // 2))],
               # damage per fight still going at the slice's start, relative to the first slice: the fight's damage
               # rate over time apart from fights ending (an opener burst shows as a high first slice)
               "rate_by_2s": [round(prof.get(k, 0) / max(1, sum(r[2] >= 2 * k for r in rs))
                                    / (prof.get(0, 0) / len(rs)), 3) for k in range(int(T_MAX // 2))]}
        out["phases"][name] = row
        print(f"{name:5s} {len(rs):6d} fights, deaths {row['death_share']:.0%}, length median {row['median_s']:.1f} s, "
              f"disengage median {row['disengage_median_s']} s, mean (to {T_MAX:.0f} s) {mean_len:.1f} s; "
              f"S(5) {c[10]:.2f} S(10) {c[20]:.2f} S(20) {c[40]:.2f}")
        print("      damage by 2 s into the fight: " + " ".join(f"{v:.2f}" for v in row["damage_by_2s"][:10]))
        print("      rate per going fight (first 2 s = 1): " + " ".join(f"{v:.2f}" for v in row["rate_by_2s"][:10]))
    # per hero: the hero's fights (either side), as a ratio of the mean disengage length to the phase pool's
    heroes = collections.defaultdict(list)
    for r in rows:
        for h in set(r[4]):
            heroes[h].append(r)
    base = sum(out["phases"]["all"]["survival"]) * STEP
    out["hero_mean_ratio"] = {}
    for h, rs in sorted(heroes.items()):
        if len(rs) >= 150:
            out["hero_mean_ratio"][str(h)] = round(sum(curve(rs)) * STEP / base, 3)
    print("per hero mean disengage length / all:", sorted(out["hero_mean_ratio"].values()))
    if "--write" in sys.argv:
        with open(os.path.join(ROOT, "data", "fight_length.json"), "w") as fh:
            json.dump(out, fh, indent=1)
            fh.write("\n")


if __name__ == "__main__":
    main()
