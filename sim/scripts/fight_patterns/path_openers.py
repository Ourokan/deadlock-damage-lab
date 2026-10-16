"""Fight starts from match_paths (1 s samples): share of starts during each movement type and distance to the
nearest enemy. Movement types: 1 = ability movement, 2 = ability debuff, 3 = ground dash, 4 = slide, 6 = zipline,
7 = in air, 8 = air dash (by observation).

usage: python3 -I path_openers.py <paths dir from fetch_paths.py> <out.json>
"""
import json, gzip, glob, os, sys, math, statistics as st, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from deadsim.data import game, UNITS_PER_METER
G = game()
agg = collections.defaultdict(lambda: collections.defaultdict(list))
for fn in glob.glob(os.path.join(sys.argv[1], "*.json.gz")):
    m = json.load(gzip.open(fn, "rt"))
    mp = m["paths"]; 
    if not mp: continue
    team = {p["slot"]: p["team"] for p in m["players"]}; hero = {p["slot"]: p["hero_id"] for p in m["players"]}
    P = {}
    for pp in mp["paths"]:
        sx = (pp["x_max"] - pp["x_min"]) / mp["x_resolution"] / UNITS_PER_METER
        sy = (pp["y_max"] - pp["y_min"]) / mp["y_resolution"] / UNITS_PER_METER
        P[pp["player_slot"]] = dict(x=[pp["x_min"]/UNITS_PER_METER + v*sx for v in pp["x_pos"]], y=[pp["y_min"]/UNITS_PER_METER + v*sy for v in pp["y_pos"]],
                                    hp=pp["health"], c=pp["combat_type"], mv=pp["move_type"])
    for s, p in P.items():
        if s not in hero: continue
        h = hero[s]; n = len(p["c"])
        foes = [o for o in P if o in team and team[o] != team[s]]
        def near(t):
            best = 1e9
            for o in foes:
                q = P[o]
                if t < len(q["hp"]) and q["hp"][t] > 0:
                    best = min(best, math.hypot(q["x"][t]-p["x"][t], q["y"][t]-p["y"][t]))
            return best
        last = -99
        for t in range(n):
            if p["c"][t] != 1: continue
            if t - last > 6 and t > 120 and p["hp"][t] > 0:
                win = p["mv"][max(0, t-4):t+1]
                a = agg[h]
                a["starts"].append(1)
                for k in (2, 1, 3, 8, 7, 4, 6):
                    a[f"mv{k}"].append(1 if k in win else 0)
                d = near(t); 
                if d < 1e8: a["d0"].append(d)
                # first 6 s of the fight: distance trace
                for u in range(t, min(n, t+8)):
                    if p["c"][u] == 1:
                        d = near(u)
                        if d < 1e8: a["dfight"].append(d)
            last = t
out = {}
for h, a in sorted(((h, a) for h, a in agg.items() if h in G.heroes), key=lambda kv: G.hero(kv[0]).name):
    r = {"name": G.hero(h).name, "fights": len(a["starts"])}
    for k in (2, 1, 3, 8, 7, 4, 6): r[f"mv{k}"] = round(sum(a[f"mv{k}"]) / len(a["starts"]), 2)
    r["start_dist_med"] = round(st.median(a["d0"]), 1) if a["d0"] else None
    r["fight_dist_med"] = round(st.median(a["dfight"]), 1) if a["dfight"] else None
    out[h] = r
json.dump(out, open(sys.argv[2], "w"), indent=1)
print(f"{'hero':16}{'n':>5} " + " ".join(f"{k:>5}" for k in ("abil","dbf","dash","adash","air","slide","zip","d0","dfit")))
for h, r in out.items():
    print(f"{r['name']:16}{r['fights']:>5} " + " ".join(f"{r[k]:>5}" for k in ("mv2","mv1","mv3","mv8","mv7","mv4","mv6","start_dist_med","fight_dist_med")))
