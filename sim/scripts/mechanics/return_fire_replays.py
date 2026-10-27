"""Return Fire (and Arctic Blast) per activation in the 260 Phantom+ replays (fight_length raw): reflected damage,
victims, the attackers' damage to the holder in the 6.5 s window, the holder's health at the start, death in the
window (validation/return_fire.md). An activation = the holder's Return Fire hits with gaps under 8 s.

usage: python3 -I scripts/mechanics/return_fire_replays.py OUT.json [raw dir]   (~1 min; prints the summary)
"""
import collections
import glob
import gzip
import json
import os
import statistics
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "sim"))
from deadsim import game
G = game()
RF = G.item("Return Fire").id
AB = G.item("Arctic Blast").id
weap = {w["id"] for w in json.load(open(os.path.join(ROOT, "data", "game", "weapons.json")))}
T = 64
RAW = "/mnt/project-files/analysis/work/fight_length/raw/"
acts = []
abacts = []
for fn in sorted(glob.glob(os.path.join(sys.argv[2] if len(sys.argv) > 2 else RAW, "*.ndjson.gz"))):
    hero, ev = {}, []
    for l in gzip.open(fn, "rt"):
        r = json.loads(l)
        if r["k"] == "ctl":
            hero[r["a"]] = int(r["s"])
        elif r["k"] == "dmg" and r.get("s"):
            ab, hp, hm = r["s"].split("|")
            ev.append((r["tick"] / T, r["a"] // 100000, r["a"] % 100000, int(ab), float(hp), float(hm), r["v"]))
    ev.sort()
    for SRC, out in ((RF, acts), (AB, abacts)):
        hits = [e for e in ev if e[3] == SRC]
        by = collections.defaultdict(list)
        for e in hits:
            by[e[1]].append(e)
        for h, hs in by.items():
            groups = []
            for e in hs:
                if not groups or e[0] - groups[-1][0][0] > 8.0:
                    groups.append([])
                groups[-1].append(e)
            for g in groups:
                t0 = g[0][0]
                w0, w1 = t0 - 0.5, t0 + 6.5
                inc = collections.defaultdict(lambda: [0.0, 0.0])
                hp0 = None
                died = False
                for e in ev:
                    if e[0] < w0 - 3 or e[0] > w1 + 3:
                        continue
                    if e[2] == h and e[1] != h:
                        if hp0 is None and e[0] >= w0 - 3:
                            hp0 = (e[4] + e[6]) / e[5]
                        if w0 <= e[0] <= w1:
                            inc[e[1]][0 if e[3] in weap else 1] += e[6]
                            if e[4] <= 0:
                                died = True
                refl = collections.Counter()
                for e in g:
                    refl[e[2]] += e[6]
                own = collections.Counter()   # holder's other damage on those victims in window
                for e in ev:
                    if w0 <= e[0] <= w1 and e[1] == h and e[3] != SRC and e[2] in refl:
                        own[e[2]] += e[6]
                out.append(dict(fn=os.path.basename(fn), h=h, hero=hero.get(h), t0=t0, refl=dict(refl),
                                inc={k: v for k, v in inc.items()}, hp0=hp0, died=died, own=dict(own)))
json.dump(dict(rf=acts, ab=abacts), open(sys.argv[1], "w"))
refl = sum(sum(x["refl"].values()) for x in acts)
num = den = 0.0
for x in acts:
    for v, r in x["refl"].items():
        b, s = x["inc"].get(v, x["inc"].get(str(v), [0, 0]))
        num += r
        den += 0.65 * b + 0.25 * s
print(f"Return Fire: {len(acts)} activations, reflected {refl / len(acts):.0f} each onto "
      f"{statistics.mean(len(x['refl']) for x in acts):.2f} heroes (top {sum(max(x['refl'].values()) for x in acts) / refl:.0%}), "
      f"attackers {statistics.mean(len(x['inc']) for x in acts):.2f}, incoming {sum(b + s for x in acts for b, s in x['inc'].values()) / len(acts):.0f}, "
      f"reflected / (65% bullet + 25% spirit of that attacker) {num / den:.2f}, holder died in window "
      f"{statistics.mean(x['died'] for x in acts):.0%}; Arctic Blast {len(abacts)} casts")
