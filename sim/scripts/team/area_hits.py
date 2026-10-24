"""How much more of an area item's damage lands on heroes other than the fight's main target, from Phantom+ replay
damage events, for the team value of area items (data/area_hits.json, used by overall_search.area_damage and the
damage audit).

Input: replay extracts with every hero-vs-hero DamageEvent (scripts/mechanics/split_shot_replays.py fetch writes
them; the 2026-10-24 fit's 110 matches are kept gzipped in the project folder analysis/work/replay_damage). A fight is a run of one attacker's hero damage with gaps under 8 s; its main target is the hero who took the
most of the attacker's gun damage. Per item: other / main = damage on every other hero / damage on the main target.
Single-target gun procs (BASELINE: Toxic Bullets, Mystic Shot) also land on others when the attacker switches
targets, so an area item's extra hits per main hit = its other / main - the baseline's. That is what a 1v1 duel
misses: the duel's damage of the item on its one target x extra_per_main.

The position-based count (team_value.json "positions": other enemies within the radius at 1 s samples) gives
0.05-0.4 here, far below what the replays show, because most fight seconds in the position data are approach and
poke at 15-20 m, while area items fire in the brawl.

usage: python3 -I area_hits.py <raw dir>... [--write]
"""
import collections
import glob
import gzip
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
T = 64
GAP_S = 8
AREA = ["Mystic Reverb", "Alchemical Fire", "Tesla Bullets", "Capacitor", "Scourge", "Torment Pulse", "Cold Front",
        "Arctic Blast"]
BASELINE = ["Toxic Bullets", "Mystic Shot"]
MIN_DMG = 20000      # real damage an item needs for a fit


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    weap = {w["id"] for w in json.load(open(os.path.join(ROOT, "..", "data", "game", "weapons.json")))}
    items = {i["id"]: i["name"] for i in json.load(open(os.path.join(ROOT, "..", "data", "game", "shop_items.json")))
             if i.get("name") in AREA + BASELINE}
    acc = collections.defaultdict(lambda: [0.0, 0.0])    # item -> [main, other]
    seen, n_matches = set(), 0
    for d in args:
        for fn in glob.glob(os.path.join(d, "*.ndjson")) + glob.glob(os.path.join(d, "*.ndjson.gz")):
            mid = os.path.basename(fn).split(".")[0]
            if mid in seen:
                continue
            seen.add(mid)
            n_matches += 1
            ev = collections.defaultdict(list)
            for line in (gzip.open(fn, "rt") if fn.endswith(".gz") else open(fn)):
                r = json.loads(line)
                if r.get("k") == "dmg" and r.get("s"):
                    ev[r["a"] // 100000].append((r["tick"], r["a"] % 100000, int(r["s"]), r["v"]))
            for es in ev.values():
                es.sort()
                fights, last = [], -1e18
                for e in es:
                    if e[0] - last > GAP_S * T:
                        fights.append([])
                    last = e[0]
                    fights[-1].append(e)
                for f in fights:
                    gun = collections.Counter()
                    for _, v, i, d in f:
                        if i in weap:
                            gun[v] += d
                    if not gun:
                        continue
                    main = gun.most_common(1)[0][0]
                    for _, v, i, d in f:
                        if i in items:
                            acc[items[i]][0 if v == main else 1] += d
    base_m = sum(acc[b][0] for b in BASELINE)
    base = sum(acc[b][1] for b in BASELINE) / max(1.0, base_m)
    out = {"source": f"{n_matches} Phantom+ replays, hero-vs-hero DamageEvent (scripts/team/area_hits.py)",
           "baseline_other_per_main": round(base, 3), "items": {}}
    print(f"baseline (single-target procs) other / main {base:.2f}")
    for name in AREA:
        m, o = acc[name]
        if m + o < MIN_DMG:
            print(f"  {name:16s} too little damage ({m + o:.0f})")
            continue
        row = {"other_per_main": round(o / m, 3), "extra_per_main": round(max(0.0, o / m - base), 3),
               "damage": int(m + o)}
        out["items"][name] = row
        print(f"  {name:16s} other / main {row['other_per_main']:.2f}  extra hits per main hit {row['extra_per_main']:.2f}")
    if "--write" in sys.argv:
        with open(os.path.join(ROOT, "data", "area_hits.json"), "w") as fh:
            json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
