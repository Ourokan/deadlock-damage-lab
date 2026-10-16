"""Real-match numbers for parry / multi-target items from the slim matches (fetch_mech.py)."""
import glob, gzip, json, random, sys
N_T = [0]
def at(s, k):
    """Damage-matrix arrays are cumulative per sample time but right-aligned: shorter arrays start later."""
    i = k - (N_T[0] - len(s))
    return s[i] if 0 <= i < len(s) else (0 if i < 0 else s[-1])
sys.path.insert(0, sys.argv[1])
from deadsim.data import game
G = game()
ID = {n: G.item(n).id for n in ("Counterspell", "Ricochet", "Split Shot", "Rebuttal", "Metal Skin", "Spirit Resilience", "Debuff Reducer", "Unstoppable")}
files = sorted(glob.glob(sys.argv[2] + "/*.json.gz"))

def held(items, iid, t0, t1):
    return any(i == iid and b <= t0 and (not s or s >= t1) for i, b, s in items)

def ever(items, iid, t1):
    return any(i == iid and b <= t1 for i, b, s in items)


def is_ability(name):
    return name.startswith(("ability_", "citadel_ability")) or "_ability" in name

cs = {n: {"with": [], "without": []} for n in ("Counterspell", "Metal Skin", "Spirit Resilience", "Unstoppable")}
ric = {"Ricochet": [0, 0, 0], "Split Shot": [0, 0, 0]}
par = {"reb": [0, 0], "other": [0, 0]}  # parry successes, player-windows
reb_dmg = [0, 0]
for fn in files:
    m = json.load(gzip.open(fn, "rt"))
    T = m["times"]; N_T[0] = len(T)
    P = {p["slot"]: p for p in m["players"]}
    def maxhp(p, t):
        for ts, hp, nw in p["stats"]:
            if ts >= t and hp:
                return hp
        return p["stats"][-1][1] if p["stats"] else None
    for k in range(1, len(T)):
        t0, t1 = T[k - 1], T[k]
        # A: ability damage taken, holders vs non-holders of item X, same dealer + window
        for dslot, srcs in m["dmg"].items():
            me = P.get(int(dslot))
            if not me: continue
            per_t = {}
            for nm, tg in srcs.items():
                if not is_ability(nm): continue
                for ts, ser in tg.items():
                    d = at(ser, k) - at(ser, k - 1)
                    per_t[int(ts)] = per_t.get(int(ts), 0) + d
            enemies = [p for p in m["players"] if p["team"] != me["team"]]
            for name, acc in cs.items():
                iid = ID[name]
                w, wo = [], []
                for p in enemies:
                    hp = maxhp(p, t1)
                    if not hp: continue
                    v = per_t.get(p["slot"], 0) / hp
                    if held(p["items"], iid, t0, t1): w.append(v)
                    elif not ever(p["items"], iid, t1): wo.append(v)
                if w and wo and (sum(w) + sum(wo)) > 0:
                    acc["with"].append(sum(w) / len(w)); acc["without"].append(sum(wo) / len(wo))
        # B/C: multi-target item damage / gun damage of holders
        for dslot, srcs in m["dmg"].items():
            me = P.get(int(dslot))
            if not me: continue
            gun = sum(at(s, k) - at(s, k - 1) for nm, tg in srcs.items() if nm.startswith("citadel_weapon") for s in tg.values())
            for name in ric:
                if held(me["items"], ID[name], t0, t1):
                    v = sum(at(s, k) - at(s, k - 1) for s in srcs.get("upgrade_" + {"Ricochet": "ricochet", "Split Shot": "split_shot"}[name], {}).values())
                    ric[name][0] += v; ric[name][1] += gun; ric[name][2] += 1
            if held(me["items"], ID["Rebuttal"], t0, t1):
                reb_dmg[0] += sum(at(s, k) - at(s, k - 1) for s in srcs.get("upgrade_melee_rebuttal", {}).values()); reb_dmg[1] += 1
        # D: parry successes per window, Rebuttal holders vs others
        for p in m["players"]:
            ser = dict(p["custom"].get("Parry Success", []))
            if t0 not in ser or t1 not in ser: continue
            key = "reb" if held(p["items"], ID["Rebuttal"], t0, t1) else "other"
            par[key][0] += ser[t1] - ser[t0]; par[key][1] += 1

out = {"matches": len(files)}
random.seed(3)
for name, acc in cs.items():
    pairs = list(zip(acc["with"], acc["without"]))
    if not pairs: continue
    r = sum(a for a, _ in pairs) / sum(b for _, b in pairs)
    bs = []
    for _ in range(500):
        s = [random.choice(pairs) for _ in pairs]
        bs.append(sum(a for a, _ in s) / max(1e-12, sum(b for _, b in s)))
    bs.sort()
    out["ability_dmg_taken_ratio_" + name] = {"ratio": round(r, 3), "ci90": [round(bs[25], 3), round(bs[474], 3)], "windows": len(pairs)}
for name, (v, g, n) in ric.items():
    out[name] = {"item_dmg_over_gun_dmg": round(v / g, 4) if g else None, "holder_windows": n}
out["Rebuttal"] = {"dmg_per_180s_window": round(reb_dmg[0] / max(1, reb_dmg[1]), 1), "holder_windows": reb_dmg[1]}
out["parry_success_per_180s"] = {k: round(a / max(1, b), 3) for k, (a, b) in par.items()}
out["parry_windows"] = {k: b for k, (a, b) in par.items()}
print(json.dumps(out, indent=1))
