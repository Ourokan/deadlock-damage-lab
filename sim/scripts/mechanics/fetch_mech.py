"""Fetch full metadata for ranked matches with Counterspell / Ricochet / Split Shot / Rebuttal holders and keep a
slim copy: players (items, max_health timeline, parry stats), damage matrix per dealer x source x enemy target
(cumulative per 180 s sample), and match_paths (1 s positions in meters, health %, combat/move type).

usage: python3 -I fetch_mech.py <sim dir> <out dir> [n_matches]
"""
import concurrent.futures as cf, glob, gzip, json, os, random, sys, time, urllib.request
sys.path.insert(0, sys.argv[1])
from deadsim.data import game, UNITS_PER_METER
OUT = sys.argv[2]; N = int(sys.argv[3]) if len(sys.argv) > 3 else 600
G = game()
WANT = {G.item(n).id for n in ("Counterspell", "Ricochet", "Split Shot", "Rebuttal")}
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}

def get(mid):
    url = f"https://api.deadlock-api.com/v1/matches/{mid}/metadata"
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return json.load(r)["match_info"]
        except Exception:
            time.sleep(3 * (i + 1))
    return None

def slim(m):
    dm = m.get("damage_matrix") or {}
    names = dm.get("source_details", {}).get("source_name", [])
    stypes = dm.get("source_details", {}).get("stat_type", [])
    team = {p["player_slot"]: p["team"] for p in m["players"]}
    dmg = {}
    for d in dm.get("damage_dealers", []):
        me = d["dealer_player_slot"]
        out = dmg.setdefault(str(me), {})
        for s in d["damage_sources"]:
            i = s["source_details_index"]
            if i >= len(names) or stypes[i] != 0:
                continue
            for tp in s["damage_to_players"]:
                t = tp["target_player_slot"]
                if t in team and team[t] != team.get(me) and tp["damage"] and tp["damage"][-1]:
                    out.setdefault(names[i], {})[str(t)] = tp["damage"]
    cus = {c["id"]: c["name"] for c in m.get("custom_user_stats") or []}
    players = []
    for p in m["players"]:
        custom = {}
        for s in p.get("stats") or []:
            for c in s.get("custom_user_stats") or []:
                nm = cus.get(c["id"], str(c["id"]))
                if "Parry" in nm:
                    custom.setdefault(nm, []).append((s["time_stamp_s"], c["value"]))
        players.append({"slot": p["player_slot"], "team": p["team"], "hero_id": p["hero_id"],
                        "items": [(x["item_id"], x["game_time_s"], x.get("sold_time_s") or 0) for x in p["items"]],
                        "stats": [(s["time_stamp_s"], s.get("max_health"), s.get("net_worth")) for s in p.get("stats") or []],
                        "deaths": [(d["game_time_s"], d.get("time_to_kill_s"), d.get("killer_player_slot")) for d in p.get("death_details") or []],
                        "custom": custom})
    mp = m.get("match_paths") or {}
    paths = {}
    P = mp.get("paths")
    if isinstance(P, str):
        import ast
        P = ast.literal_eval(P)
    for pp in P or []:
        def arr(k):
            v = pp.get(k)
            return json.loads(v) if isinstance(v, str) else (v or [])
        xs, ys = arr("x_pos"), arr("y_pos")
        sx = (pp["x_max"] - pp["x_min"]) / mp.get("x_resolution", 16383) / UNITS_PER_METER
        sy = (pp["y_max"] - pp["y_min"]) / mp.get("y_resolution", 16383) / UNITS_PER_METER
        x0, y0 = pp["x_min"] / UNITS_PER_METER, pp["y_min"] / UNITS_PER_METER
        paths[str(pp["player_slot"])] = {"x": [round(x0 + v * sx, 1) for v in xs], "y": [round(y0 + v * sy, 1) for v in ys],
                                         "hp": arr("health"), "combat": arr("combat_type"), "move": arr("move_type")}
    return {"match_id": m["match_id"], "duration_s": m["duration_s"], "badge": m.get("average_badge_team0"),
            "times": dm.get("sample_time_s") or [], "players": players, "dmg": dmg, "paths": paths}

def main():
    files = sorted(glob.glob("/mnt/project-files/data/builds/player_builds/*.jsonl.gz"))[-5:-1]
    hits, allm = {}, set()
    for fn in files:
        for line in gzip.open(fn, "rt"):
            r = json.loads(line)
            if (r["badge"] or 0) < 60 or r["duration_s"] < 1200:
                continue
            allm.add(r["match_id"])
            k = len(WANT & set(r["final_items"]))
            if k:
                hits[r["match_id"]] = hits.get(r["match_id"], 0) + k
    ids = sorted(hits, key=lambda x: -hits[x])
    random.seed(5)
    top = ids[: N * 3]
    ids = random.sample(top, min(N, len(top)))
    ids = [i for i in ids if not os.path.exists(os.path.join(OUT, f"{i}.json.gz"))]
    print(len(allm), "ranked matches,", len(hits), "with a wanted item; fetching", len(ids), flush=True)
    done = 0
    with cf.ThreadPoolExecutor(6) as ex:
        for mid, m in zip(ids, ex.map(get, ids)):
            if not m:
                continue
            try:
                s = slim(m)
            except Exception as e:
                print("slim fail", mid, e, flush=True); continue
            with gzip.open(os.path.join(OUT, f"{mid}.json.gz"), "wt") as f:
                json.dump(s, f)
            done += 1
            if done % 50 == 0:
                print(done, flush=True)
    print("done", done)

if __name__ == "__main__":
    main()
