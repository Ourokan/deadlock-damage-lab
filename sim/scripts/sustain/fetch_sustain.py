"""Fetch full metadata for Phantom+ ranked matches and keep what the sustain fit needs: each player's items (buy and
sell times), stats every 180 s (max health, net worth, self healing, heal prevented, damage taken), the healing part
of the damage matrix (stat_type 1 = heals, 5 = regen, 2 = heal prevented) per source, cumulative per sample, and
match_paths health % + hero-combat flag every second.

usage: python3 -I fetch_sustain.py <sim dir> <out dir> [n_matches] [min_badge]
"""
import concurrent.futures as cf, glob, gzip, json, os, random, sys, time, urllib.request
sys.path.insert(0, sys.argv[1])
OUT = sys.argv[2]; N = int(sys.argv[3]) if len(sys.argv) > 3 else 300
MIN_BADGE = int(sys.argv[4]) if len(sys.argv) > 4 else 91
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}
HEAL_TYPES = (1, 2, 5)
STATS = ("max_health", "net_worth", "self_healing", "heal_prevented", "heal_lost", "player_damage_taken",
         "player_damage", "creep_damage", "deaths")


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
    heal = {}
    for d in dm.get("damage_dealers", []):
        me = str(d["dealer_player_slot"])
        for s in d["damage_sources"]:
            i = s["source_details_index"]
            if i >= len(names) or stypes[i] not in HEAL_TYPES:
                continue
            for tp in s["damage_to_players"]:
                if tp["damage"] and tp["damage"][-1]:
                    heal.setdefault(me, []).append([stypes[i], names[i], tp["target_player_slot"], tp["damage"]])
    cus = {c["id"]: c["name"] for c in m.get("custom_user_stats") or []}
    players = []
    for p in m["players"]:
        parry = {}
        for s in p.get("stats") or []:
            for c in s.get("custom_user_stats") or []:
                nm = cus.get(c["id"], str(c["id"]))
                if "Parry" in nm:
                    parry.setdefault(nm, []).append((s["time_stamp_s"], c["value"]))
        players.append({"slot": p["player_slot"], "team": p["team"], "hero_id": p["hero_id"],
                        "items": [(x["item_id"], x["game_time_s"], x.get("sold_time_s") or 0) for x in p["items"]],
                        "stats": [[s["time_stamp_s"]] + [s.get(k) for k in STATS] for s in p.get("stats") or []],
                        "parry": parry})
    mp = m.get("match_paths") or {}
    P = mp.get("paths")
    if isinstance(P, str):
        import ast
        P = ast.literal_eval(P)
    paths = {}
    for pp in P or []:
        def arr(k):
            v = pp.get(k)
            return json.loads(v) if isinstance(v, str) else (v or [])
        paths[str(pp["player_slot"])] = {"hp": arr("health"), "combat": arr("combat_type")}
    return {"match_id": m["match_id"], "duration_s": m["duration_s"], "badge": m.get("average_badge_team0"),
            "times": dm.get("sample_time_s") or [], "stat_keys": ["t", *STATS], "players": players, "heal": heal,
            "paths": paths}


def main():
    os.makedirs(OUT, exist_ok=True)
    files = sorted(glob.glob("/mnt/project-files/data/builds/player_builds/*.jsonl.gz"))[-4:]
    ids = set()
    for fn in files:
        for line in gzip.open(fn, "rt"):
            r = json.loads(line)
            if (r["badge"] or 0) >= MIN_BADGE and r["duration_s"] >= 1200:
                ids.add(r["match_id"])
    random.seed(7)
    ids = random.sample(sorted(ids), min(N, len(ids)))
    ids = [i for i in ids if not os.path.exists(os.path.join(OUT, f"{i}.json.gz"))]
    print("fetching", len(ids), flush=True)
    done = 0
    with cf.ThreadPoolExecutor(6) as ex:
        for mid, m in zip(ids, ex.map(get, ids)):
            if not m:
                continue
            try:
                s = slim(m)
            except Exception as e:
                print("slim fail", mid, e, flush=True)
                continue
            with gzip.open(os.path.join(OUT, f"{mid}.json.gz"), "wt") as f:
                json.dump(s, f)
            done += 1
            if done % 50 == 0:
                print(done, flush=True)
    print("done", done)


if __name__ == "__main__":
    main()
