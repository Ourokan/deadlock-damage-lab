"""Graves in Phantom+ replays by game phase: Jar of Dead charges at a fight's start and throws per fight, Grasping
Hands casts per fight, and each one's hero damage per fight and per cast (validation/README.md "Mo & Krill and Graves").

A fight is a run of hero-vs-hero damage to or from Graves with gaps under GAP s and at least MIN_DMG damage (as
fight_patterns/replay_openers.py); casts from PRE s before its first hit to its end count. The phase is the fight
start's share of the replay's last damage tick.

--write: data/graves_phase.json (Mechanics.graves_phase) in PHASES match-fraction bins at Graves' median net worth
there (phantom_sample): the share of fights with 0 / 1 / 2 / 3+ Jar of Dead throws, and the share with a Grasping
Hands cast over the whole match's.

usage: python3 -I graves_jars.py [--write] [states dir] [fight_length raw dir]
(states: scripts/fight_patterns/fetch_states.py graves; default the project folder analysis/work/krill_graves/graves)
"""
import collections
import glob
import gzip
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cast_timing"))
from krill_burrow import fights, BINS, T, median_nw  # noqa: E402
from fit_cast_timing import real_casts  # noqa: E402  pauses move the tick -> game time offset

GRAVES = 76
PRE = 4.0
JAR, WALL, STONE = 3214055642, 2001589780, 4110547059
TABS = {"cast:CCitadel_Ability_Necro_HauntingSkull": "jar", "cast:CCitadel_Ability_Necro_ZombieWall": "wall",
        "cast:CCitadel_Ability_Necro_GraveStone": "stone"}
ABIL = {JAR: "jar", WALL: "wall", STONE: "stone"}


PHASES = (0.0, 0.3, 0.6, 1.01)
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    args = [a for a in sys.argv[1:] if a != "--write"]
    sd = args[0] if args else "/mnt/project-files/analysis/work/krill_graves/graves"
    dd = args[1] if len(args) > 1 else "/mnt/project-files/analysis/work/fight_length/raw"
    throws = collections.defaultdict(collections.Counter)   # phase bin -> Counter(min(throws, 3))
    walled = collections.Counter()
    n = collections.Counter()
    casts = collections.defaultdict(collections.Counter)
    dmg = collections.defaultdict(collections.Counter)
    charges = collections.defaultdict(list)
    gun = collections.Counter()
    for fn in sorted(glob.glob(os.path.join(sd, "*.ndjson"))):
        mid = os.path.basename(fn).split(".")[0]
        dfn = os.path.join(dd, f"{mid}.ndjson.gz")
        if not os.path.exists(dfn):
            continue
        ch, cs, rows = collections.defaultdict(list), collections.defaultdict(list), []
        for line in open(fn):
            r = json.loads(line)
            if r["k"] == "charges":
                ch[r["a"] & 0x3FFF].append((r["tick"] / T, int(r["s"])))
            elif r["k"] in TABS:
                rows.append({"k": "cast", "a": r["a"], "s": TABS[r["k"]], "v": r["v"], "tick": r["tick"]})
        for r in real_casts(rows):
            cs[r["a"] & 0x3FFF].append((r["tick"] / T, r["s"]))
        hero, ev, last = {}, collections.defaultdict(list), 0
        for line in gzip.open(dfn, "rt"):
            r = json.loads(line)
            if r["k"] == "ctl":
                hero[r["a"]] = int(r["s"])
            elif r["k"] == "dmg":
                ev[r["a"] // 100000, r["a"] % 100000].append((r["tick"] / T, r["v"], int(r["s"].split("|")[0]) if r.get("s") else 0))
                last = max(last, r["tick"] / T)
        for g in [p for p, h in hero.items() if h == GRAVES]:
            mine = sorted((t, v) for (a, b), es in ev.items() if (a == g or b == g) and a in hero and b in hero
                          and a != b for t, v, _ in es)
            out = [(t, v, s) for (a, b), es in ev.items() if a == g and b in hero and b != g for t, v, s in es]
            st = sorted(ch.get(g, []))
            for s, e, d in fights(mine):
                b = next(i for i in range(len(BINS) - 1) if BINS[i] <= s / last < BINS[i + 1])
                n[b] += 1
                before = [c for t, c in st if t <= s - PRE]
                charges[b].append(before[-1] if before else 0)
                for t, k in cs.get(g, []):
                    if s - PRE <= t <= e:
                        casts[b][k] += 1
                pb = next(i for i in range(len(PHASES) - 1) if PHASES[i] <= s / last < PHASES[i + 1])
                throws[pb][min(3, sum(1 for t, k in cs.get(g, []) if k == "jar" and s - PRE <= t <= e))] += 1
                walled[pb, any(k == "wall" and s - PRE <= t <= e for t, k in cs.get(g, []))] += 1
                for t, v, src in out:
                    if s - PRE <= t <= e + 2:
                        dmg[b][ABIL.get(src, "other")] += v
                        gun[b] += v
    print("phase      fights  jars@start  jar/f  wall/f  stone/f   dmg share jar wall stone (of all Graves hero dmg in fights)")
    for b in range(len(BINS) - 1):
        f = max(1, n[b])
        tot = max(1, gun[b])
        print(f"{BINS[b]:.2f}-{min(1, BINS[b + 1]):.2f}  {n[b]:6d}  {statistics.mean(charges[b]) if charges[b] else 0:.2f}"
              f"  {casts[b]['jar'] / f:.2f}  {casts[b]['wall'] / f:.2f}  {casts[b]['stone'] / f:.2f}"
              f"   {dmg[b]['jar'] / tot:.3f} {dmg[b]['wall'] / tot:.3f} {dmg[b]['stone'] / tot:.3f}"
              f"   per cast jar {dmg[b]['jar'] / max(1, casts[b]['jar']):.0f} wall {dmg[b]['wall'] / max(1, casts[b]['wall']):.0f}")
    nb = len(PHASES) - 1
    wall_all = sum(walled[b, True] for b in range(nb)) / max(1, sum(walled.values()))
    pts_t, pts_w = [], []
    nw = median_nw([(PHASES[b] + min(1.0, PHASES[b + 1])) / 2 for b in range(nb)], GRAVES)
    for b in range(nb):
        tot = sum(throws[b].values())
        share = [round(throws[b][k] / tot, 3) for k in range(4)]
        w = walled[b, True] / max(1, walled[b, True] + walled[b, False])
        x = nw[(PHASES[b] + min(1.0, PHASES[b + 1])) / 2]
        pts_t.append([x, share])
        pts_w.append([x, round(w / wall_all, 3)])
        print(f"phase {PHASES[b]:.1f}-{min(1, PHASES[b + 1]):.1f} nw {x}: jar throws 0/1/2/3+ {share}, "
              f"Grasping Hands cast {w:.2f} (x{w / wall_all:.2f} of the match's {wall_all:.2f})")
    if "--write" in sys.argv:
        out = {"source": f"{sum(n.values())} Graves fights in Phantom+ replays (scripts/mechanics/graves_jars.py)",
               "note": "jar_throws: share of fights with 0 / 1 / 2 / 3+ Jar of Dead throws; wall_mult: share of fights "
                       "with a Grasping Hands cast over the whole match's; at Graves' median net worth in each "
                       "match-fraction bin, linear in ln net worth between points (Mechanics.graves_phase)",
               "jar_throws": pts_t, "wall_mult": pts_w}
        json.dump(out, open(os.path.join(HERE, "..", "..", "data", "graves_phase.json"), "w"), indent=1)
        print("wrote data/graves_phase.json")


if __name__ == "__main__":
    main()
