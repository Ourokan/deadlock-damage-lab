"""Fetch match_paths (and heroes, deaths) for matches. usage: python3 -I fetch_paths.py <matches.json from /v1/matches/metadata> <out dir>"""
import json, sys, os, time, urllib.request, concurrent.futures as cf, gzip
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}
ids = [m["match_id"] for m in json.load(open(sys.argv[1]))]
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
def get(mid):
    fn = f"{out}/{mid}.json.gz"
    if os.path.exists(fn): return 1
    for i in range(3):
        try:
            m = json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.deadlock-api.com/v1/matches/{mid}/metadata", headers=UA), timeout=90))["match_info"]
            break
        except Exception as e:
            if "503" in str(e): return 0
            time.sleep(3)
    else: return 0
    slim = {"match_id": mid, "badge": m.get("average_badge_team0"), "players": [{"slot": p["player_slot"], "team": p["team"], "hero_id": p["hero_id"],
            "deaths": [d["game_time_s"] for d in p.get("death_details") or []]} for p in m["players"]], "paths": m.get("match_paths")}
    json.dump(slim, gzip.open(fn, "wt")); return 1
with cf.ThreadPoolExecutor(6) as ex: r = list(ex.map(get, ids))
print(sum(r), len(r))
