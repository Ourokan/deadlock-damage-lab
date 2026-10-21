"""Fetch match_paths (1 s positions in meters, health %, combat type) for Phantom+ ranked matches and keep a slim copy
with the players' heroes and teams, for the fight-range fit (fit_range.py).

usage: python3 -I fetch_paths.py <sim dir> <player_builds dir> <out dir> [n_matches] [min_badge]
"""
import concurrent.futures as cf, glob, gzip, json, os, random, sys, time, urllib.request
sys.path.insert(0, sys.argv[1])
from deadsim.data import UNITS_PER_METER  # noqa: E402
BUILDS, OUT = sys.argv[2], sys.argv[3]
N = int(sys.argv[4]) if len(sys.argv) > 4 else 300
MIN_BADGE = int(sys.argv[5]) if len(sys.argv) > 5 else 91
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}


def get(mid):
    url = f"https://api.deadlock-api.com/v1/matches/{mid}/metadata"
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return json.load(r)["match_info"]
        except Exception:
            time.sleep(3 * (i + 1))
    return None


def slim(m):
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
        xs, ys = arr("x_pos"), arr("y_pos")
        sx = (pp["x_max"] - pp["x_min"]) / mp.get("x_resolution", 16383) / UNITS_PER_METER
        sy = (pp["y_max"] - pp["y_min"]) / mp.get("y_resolution", 16383) / UNITS_PER_METER
        x0, y0 = pp["x_min"] / UNITS_PER_METER, pp["y_min"] / UNITS_PER_METER
        paths[str(pp["player_slot"])] = {"x": [round(x0 + v * sx, 1) for v in xs], "y": [round(y0 + v * sy, 1) for v in ys],
                                         "hp": arr("health"), "combat": arr("combat_type"), "move": arr("move_type")}
    return {"match_id": m["match_id"], "duration_s": m["duration_s"], "badge": m.get("average_badge_team0"),
            "interval_s": mp.get("interval_s", 1.0),
            "players": [{"slot": p["player_slot"], "team": p["team"], "hero_id": p["hero_id"],
                         "net_worth": [(s["time_stamp_s"], s.get("net_worth")) for s in p.get("stats") or []]}
                        for p in m["players"]],
            "paths": paths}


def main():
    ids = set()
    for fn in sorted(glob.glob(os.path.join(BUILDS, "*.jsonl.gz")))[-4:]:
        for line in gzip.open(fn, "rt"):
            r = json.loads(line)
            if (r["badge"] or 0) >= MIN_BADGE and r["duration_s"] >= 1200:
                ids.add(r["match_id"])
    random.seed(11)
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
