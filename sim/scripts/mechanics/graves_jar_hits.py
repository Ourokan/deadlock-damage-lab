"""Graves' Jar of Dead per throw in Phantom+ replays by game phase and Jar tier (validation/README.md "Graves' Jar of
Dead by phase"): hero hits per throw, damage per throw, real damage per hit over the formula Damage + 0.25 x spirit
power (the throw's build from phantom_sample), throws per fight, and the hits after a throw in 2 s buckets.

A throw's hits are its Deadheads' damage events on enemy heroes up to 16 s later or the next throw. Fights as
graves_jars.py. The tier and build are the player's at the throw (sample items, damage_audit.real_tiers).

usage: python3 graves_jar_hits.py [states dir] [fight_length raw dir]
(states: scripts/fight_patterns/fetch_states.py graves; default the project folder analysis/work/krill_graves/graves)
"""
import collections
import glob
import gzip
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "cast_timing"))
from krill_burrow import T, fights  # noqa: E402
from fit_cast_timing import real_casts  # noqa: E402
import landing_rates as L  # noqa: E402
import damage_audit as D  # noqa: E402
from deadsim.build import compute_stats  # noqa: E402

GRAVES = 76
JAR = 3214055642
CAST = "cast:CCitadel_Ability_Necro_HauntingSkull"
PHASES = (0.0, 0.3, 0.6, 1.01)
SAMPLE = os.path.join(HERE, "..", "..", "validation", "phantom_sample.jsonl.gz")


def phase(x):
    return next((i for i in range(len(PHASES) - 1) if PHASES[i] <= x < PHASES[i + 1]), len(PHASES) - 2)


def main():
    sd = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project-files/analysis/work/krill_graves/graves"
    dd = sys.argv[2] if len(sys.argv) > 2 else "/mnt/project-files/analysis/work/fight_length/raw"
    D.ORDER_HEROES = set(D.ORDER_HEROES) | {"Graves"}   # real_tiers for Graves
    sample = {}
    for line in gzip.open(SAMPLE):
        m = json.loads(line)
        sample[str(m["match_id"])] = m
    throws, buckets = collections.defaultdict(list), collections.defaultdict(collections.Counter)
    per_fight = collections.defaultdict(collections.Counter)
    for fn in sorted(glob.glob(os.path.join(sd, "*.ndjson"))):
        mid = os.path.basename(fn).split(".")[0]
        dfn = os.path.join(dd, f"{mid}.ndjson.gz")
        m = sample.get(mid)
        if m is None or not os.path.exists(dfn):
            continue
        p = next((x for x in m["players"] if x["hero_id"] == GRAVES), None)
        if p is None:
            continue
        rows = [json.loads(line) for line in open(fn)]
        rows = [{"k": "cast", "a": r["a"], "s": "jar", "v": r["v"], "tick": r["tick"]} for r in rows if r["k"] == CAST]
        casts = collections.defaultdict(list)
        for r in real_casts(rows):
            casts[r["a"] & 0x3FFF].append(r["tick"] / T)
        hero, ev = {}, collections.defaultdict(list)
        for line in gzip.open(dfn, "rt"):
            r = json.loads(line)
            if r["k"] == "ctl":
                hero[r["a"]] = int(r["s"])
            elif r["k"] == "dmg":
                ev[r["a"] // 100000, r["a"] % 100000].append((r["tick"] / T, r["v"], int(r["s"].split("|")[0]) if r.get("s") else 0))
        for g in [x for x, h in hero.items() if h == GRAVES]:
            ct = sorted(casts.get(g, []))
            out = [(t, b, v, s) for (a, b), es in ev.items() if a == g and b in hero and hero[b] != GRAVES for t, v, s in es]
            for i, t in enumerate(ct):
                end = min(t + 16, ct[i + 1] if i + 1 < len(ct) else 1e9)
                hs = [(tt, v) for tt, b, v, s in out if s == JAR and t <= tt < end]
                t3 = D.real_tiers(p, t)["tiers"][0] == 3
                items, souls = L.build_at(p, t)
                k = (phase(t / m["duration_s"]), t3)
                throws[k].append((len(hs), sum(v for _, v in hs), 16 + 0.25 * compute_stats("Graves", items, souls).spirit_power))
                for tt, _ in hs:
                    buckets[k][int(tt - t) // 2] += 1
            mine = sorted((t, v) for (a, b), es in ev.items() if (a == g or b == g) and a in hero and b in hero and a != b
                          for t, v, _ in es)
            for s, e, _ in fights(mine):
                k = (phase(s / m["duration_s"]), D.real_tiers(p, s)["tiers"][0] == 3)
                per_fight[k]["fights"] += 1
                per_fight[k]["throws"] += sum(1 for t in ct if s - 4 <= t <= e)
    print("phase    Jar T3  throws  hits/throw  dmg/throw  real/formula per hit  throws/fight   hits per 2 s after the throw")
    for k in sorted(throws):
        r, n = throws[k], len(throws[k])
        f = per_fight[k]
        print(f"{PHASES[k[0]]:.1f}-{min(1, PHASES[k[0] + 1]):.1f}  {'yes' if k[1] else 'no ':3s}  {n:6d}  "
              f"{statistics.mean(x[0] for x in r):10.2f}  {statistics.mean(x[1] for x in r):9.0f}  "
              f"{sum(x[1] for x in r) / max(1.0, sum(x[0] * x[2] for x in r)):20.2f}  "
              f"{f['throws'] / max(1, f['fights']):12.2f}   " + " ".join(f"{buckets[k][b] / n:.2f}" for b in range(8)))


if __name__ == "__main__":
    main()
