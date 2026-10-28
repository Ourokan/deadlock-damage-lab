"""How many Ballistic Enchantment stacks a holder carries when they shoot, per imbued ability, from Phantom+ replay
damage events (data/ballistic_stacks.json, Mechanics.ballistic_stacks).

Ballistic Enchantment gives +WeaponPowerPerStack weapon damage per unique enemy hero the imbued ability damaged in
the last AbilityDuration (20 s). A duel has one enemy, so the sim's holder had at most one stack, while an area
ability in a real fight tags several heroes (Malice, Aura of Suffering, Fixation's bullets ...). Real holders deal
1.15x the hero damage per minute of non-holders at 27k (same hero, net worth, game time; holder_rates.py), the
biggest gap to the sim's damage gain (1.055) of any item.

For every attacker's gun hit on a hero (DamageEvent with a weapon source), and every ability that attacker has
damaged a hero with: the distinct heroes that ability damaged in the last 20 s. Kept per ability: the gun-damage
weighted mean of that count over the gun hits where it is at least 1 (the sim's holder has its one stack exactly
then; how often the ability is on a hero stays the sim's own timing), and the share of gun damage with at least one
(P >= 1, for reference). Every player who used the ability counts, not only Ballistic Enchantment holders (too few
in 260 replays; the imbue's +22% radius would only add hits). Halves by match id parity for the split-half check.
Non-hero stacks (+5% per creep, at most 8) are not counted: the extracts hold hero-vs-hero damage only.

usage: python3 -I ballistic_stacks.py [RAW_DIR] [--write]
"""
import collections
import glob
import gzip
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GAME = os.path.join(ROOT, "..", "data", "game")
RAW = "/mnt/project-files/analysis/work/replay_damage"
OUT = os.path.join(ROOT, "data", "ballistic_stacks.json")
T = 64
WINDOW_S = 20.0      # Ballistic Enchantment AbilityDuration
MIN_GUN = 5000       # gun damage with >= 1 stack an ability needs for a row


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    raw = args[0] if args else RAW
    ab = {int(a["id"]): a for a in json.load(open(os.path.join(GAME, "abilities.json")))}
    weap = {int(w["id"]) for w in json.load(open(os.path.join(GAME, "weapons.json")))}
    # ability id -> [half 0, half 1] x [gun dmg x stacks, gun dmg with >= 1 stack, all gun dmg of its users]
    acc = collections.defaultdict(lambda: [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
    files = sorted(glob.glob(os.path.join(raw, "*.ndjson.gz")))
    for fn in files:
        half = int(os.path.basename(fn).split(".")[0]) % 2
        ev = collections.defaultdict(list)
        for line in gzip.open(fn, "rt"):
            r = json.loads(line)
            if r.get("k") == "dmg" and r.get("s"):
                ev[r["a"] // 100000].append((r["tick"], r["a"] % 100000, int(r["s"]), r["v"]))
        for es in ev.values():
            es.sort()
            last = collections.defaultdict(dict)   # ability id -> victim -> tick of its last hit
            for t, v, s, d in es:
                if s in ab:
                    last[s][v] = t
                elif s in weap:
                    for a, vs in last.items():
                        c = sum(1 for tt in vs.values() if t - tt <= WINDOW_S * T)
                        x = acc[a][half]
                        x[2] += d
                        if c:
                            x[0] += d * c
                            x[1] += d
    out = {"source": f"{len(files)} Phantom+ replays, hero-vs-hero DamageEvent (scripts/team/ballistic_stacks.py)",
           "window_s": WINDOW_S, "abilities": {}}
    rows = []
    for a, (h0, h1) in acc.items():
        w = h0[1] + h1[1]
        if w < MIN_GUN:
            continue
        m = (h0[0] + h1[0]) / w
        row = {"hero": ab[a]["hero"], "name": ab[a]["name"], "stacks": round(m, 3),
               "halves": [round(h[0] / h[1], 3) if h[1] else None for h in (h0, h1)],
               "p_any": round(w / (h0[2] + h1[2]), 3), "gun_damage": int(w)}
        out["abilities"][ab[a]["class_name"]] = row
        rows.append(row)
    for r in sorted(rows, key=lambda r: -r["stacks"]):
        print(f"{r['hero']:14s} {r['name']:24s} stacks {r['stacks']:.2f} (halves {r['halves'][0]} / {r['halves'][1]})"
              f"  P>=1 {r['p_any']:.2f}")
    if "--write" in sys.argv:
        with open(OUT, "w") as f:
            json.dump(out, f, indent=1)
        print("wrote", OUT)


if __name__ == "__main__":
    main()
