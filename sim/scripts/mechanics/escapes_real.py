"""Real 1v1 low-health episodes from match_paths (1 s positions + health %).
Episode: player P's health drops below LOW % while exactly one enemy hero is within NEAR m and no teammate within
NEAR m. Outcome over the next HORIZON s: died (health 0), won (the enemy died), escaped (alive, gap > ESC m), or other.
Also splits by whether P holds a mobility item and whether the enemy holds a slow item, and the gap growth while
escaping."""
import glob, gzip, json, math, sys, collections
sys.path.insert(0, sys.argv[1])
from deadsim.data import game
G = game()
LOW, NEAR, HORIZON, ESC = 25, 25.0, 10, 35.0
MOB = {G.item(n).id: n for n in ("Majestic Leap", "Warp Stone", "Ethereal Shift", "Fleetfoot", "Enduring Speed",
                                  "Magic Carpet", "Extra Stamina", "Stamina Mastery", "Kinetic Dash", "Dispel Magic")}
SLOW = {G.item(n).id: n for n in ("Slowing Hex", "Mystic Slow", "Slowing Bullets", "Cold Front", "Arctic Blast",
                                   "Phantom Strike", "Lifestrike", "Knockdown")}
def holds(items, t):
    return {i for i, b, s in items if b <= t and (not s or s > t)}
out = collections.Counter(); by_mob = collections.defaultdict(collections.Counter); by_item = collections.defaultdict(collections.Counter)
by_slow = collections.defaultdict(collections.Counter); gaps = []
for fn in sorted(glob.glob(sys.argv[2] + "/*.json.gz")):
    m = json.load(gzip.open(fn, "rt"))
    P = {p["slot"]: p for p in m["players"]}
    paths = {int(k): v for k, v in m["paths"].items() if int(k) in P}
    if len(paths) < 12: continue
    n = min(len(v["x"]) for v in paths.values())
    def pos(s, t): return paths[s]["x"][t], paths[s]["y"][t]
    def dist(a, b, t):
        (x1, y1), (x2, y2) = pos(a, t), pos(b, t); return math.hypot(x1 - x2, y1 - y2)
    for s, pa in paths.items():
        me = P[s]; hp = pa["hp"]
        last = -99
        for t in range(1, n - HORIZON):
            if not (hp[t - 1] >= LOW > hp[t] > 0) or t - last < 15: continue
            enemies = [q for q in paths if P[q]["team"] != me["team"] and paths[q]["hp"][t] > 0 and dist(s, q, t) <= NEAR]
            mates = [q for q in paths if q != s and P[q]["team"] == me["team"] and paths[q]["hp"][t] > 0 and dist(s, q, t) <= NEAR]
            if len(enemies) != 1 or mates: continue
            last = t
            q = enemies[0]
            res = "other"
            for u in range(t, t + HORIZON + 1):
                if hp[u] == 0: res = "died"; break
                if paths[q]["hp"][u] == 0: res = "won"; break
            if res == "other":
                res = "escaped" if dist(s, q, t + HORIZON) > ESC else "still_fighting"
            mob = holds(me["items"], m["times"][0] and t) & set(MOB)
            slow = holds(P[q]["items"], t) & set(SLOW)
            out[res] += 1
            by_mob[bool(mob)][res] += 1
            by_slow[bool(slow)][res] += 1
            for i in mob: by_item[MOB[i]][res] += 1
            d0 = dist(s, q, t)
            gaps.append((res, d0, [round(dist(s, q, t + k), 1) for k in range(0, HORIZON + 1, 2)]))
def show(c):
    tot = sum(c.values()); return {k: f"{v} ({v / tot:.0%})" for k, v in sorted(c.items())} | {"n": tot}
print("all", show(out))
print("runner has mobility item", show(by_mob[True])); print("no mobility item", show(by_mob[False]))
print("enemy has slow item", show(by_slow[True])); print("no slow item", show(by_slow[False]))
for k, c in sorted(by_item.items()): print("  ", k, show(c))
med = sorted(g[1] for g in gaps); print("gap at low-hp moment, median", med[len(med) // 2])
esc = [g[2] for g in gaps if g[0] == "escaped"]
if esc:
    print("escaped: median gap every 2 s", [sorted(x[k] for x in esc)[len(esc) // 2] for k in range(len(esc[0]))])
dd = [g[2] for g in gaps if g[0] == "died"]
print("died: median gap every 2 s", [sorted(x[k] for x in dd)[len(dd) // 2] for k in range(len(dd[0]))])
