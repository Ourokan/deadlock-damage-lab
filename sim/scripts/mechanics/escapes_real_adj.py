"""Escape share (escaped / (escaped + died)) for runners holding item X vs not, adjusted for game time (5-min bins)
and runner hero (Mantel-Haenszel risk difference). Same episodes as escapes_real.py."""
import glob, gzip, json, math, sys, collections
sys.path.insert(0, sys.argv[1])
from deadsim.data import game
G = game()
LOW, NEAR, HORIZON, ESC = 25, 25.0, 10, 35.0
ITEMS = ["Majestic Leap", "Warp Stone", "Ethereal Shift", "Fleetfoot", "Enduring Speed", "Magic Carpet", "Extra Stamina",
         "Stamina Mastery", "Kinetic Dash", "Dispel Magic", "Sprint Boots", "Extra Health", "Spirit Resilience"]
ENEMY = ["Slowing Hex", "Mystic Slow", "Slowing Bullets", "Cold Front", "Arctic Blast", "Phantom Strike", "Lifestrike", "Knockdown"]
ID = {G.item(n).id: n for n in ITEMS + ENEMY}
eps = []
for fn in sorted(glob.glob(sys.argv[2] + "/*.json.gz")):
    m = json.load(gzip.open(fn, "rt"))
    P = {p["slot"]: p for p in m["players"]}
    paths = {int(k): v for k, v in m["paths"].items() if int(k) in P}
    if len(paths) < 12: continue
    n = min(len(v["x"]) for v in paths.values())
    def dist(a, b, t):
        return math.hypot(paths[a]["x"][t] - paths[b]["x"][t], paths[a]["y"][t] - paths[b]["y"][t])
    for s, pa in paths.items():
        me = P[s]; hp = pa["hp"]; last = -99
        for t in range(1, n - HORIZON):
            if not (hp[t - 1] >= LOW > hp[t] > 0) or t - last < 15: continue
            en = [q for q in paths if P[q]["team"] != me["team"] and paths[q]["hp"][t] > 0 and dist(s, q, t) <= NEAR]
            ma = [q for q in paths if q != s and P[q]["team"] == me["team"] and paths[q]["hp"][t] > 0 and dist(s, q, t) <= NEAR]
            if len(en) != 1 or ma: continue
            last = t; q = en[0]; res = None
            for u in range(t, t + HORIZON + 1):
                if hp[u] == 0: res = 0; break
                if paths[q]["hp"][u] == 0: res = None; break
            else:
                res = 1 if dist(s, q, t + HORIZON) > ESC else None
            if res is None: continue
            mine = {ID[i] for i, b, so in me["items"] if i in ID and b <= t and (not so or so > t)}
            theirs = {ID[i] for i, b, so in P[q]["items"] if i in ID and b <= t and (not so or so > t)}
            eps.append((res, t // 300, me["hero_id"], mine, theirs))
print("episodes", len(eps), "escape share", round(sum(e[0] for e in eps) / len(eps), 3))
def mh(has):
    strata = collections.defaultdict(lambda: [0, 0, 0, 0])
    for r, tb, h, mi, th in eps:
        k = strata[(tb, h)]
        if has(mi, th): k[0] += r; k[1] += 1
        else: k[2] += r; k[3] += 1
    num = den = 0.0; n1 = 0
    for a, n_a, b, n_b in strata.values():
        if n_a and n_b:
            w = n_a * n_b / (n_a + n_b); num += w * (a / n_a - b / n_b); den += w; n1 += n_a
    return (num / den if den else float("nan")), n1
for it in ITEMS:
    d, n1 = mh(lambda mi, th, it=it: it in mi)
    print(f"runner holds {it:18s} escape share {d:+.3f}  (n={n1})")
for it in ENEMY:
    d, n1 = mh(lambda mi, th, it=it: it in th)
    print(f"enemy holds  {it:18s} escape share {d:+.3f}  (n={n1})")
d, n1 = mh(lambda mi, th: bool(set(ENEMY) & th)); print(f"enemy holds any slow item escape share {d:+.3f} (n={n1})")
