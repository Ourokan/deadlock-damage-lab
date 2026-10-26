"""Fetch the aim sample behind data/skill_defaults.json: final hero-aim stats of recent Phantom+ ranked matches.

Reads the bulk metadata endpoint (match store, no SQL rate limit), six 4-hour windows per day so every
day and every region's prime time counts, and keeps per player only the hero-only gun stats (Enemy Hero Accuracy Shots/Hits/Headshots) and the
outgoing bullet distance histogram (no account ids: the file is committed). Output lines match validation/matches_sample.jsonl.gz enough for
build_skill_defaults.py (match_id, badge, players[hero_id, custom]).

usage: python3 scripts/fetch_aim_sample.py [--badge 91] [--days 10] [--per-day 420] [--out validation/aim_sample.jsonl.gz]
"""
import argparse
import gzip
import json
import os
import time
import urllib.request

UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}
ROOT = os.path.join(os.path.dirname(__file__), "..")
KEEP = ("Enemy Hero Accuracy##", "Outgoing Bullet Dist##")


def window(t0, t1, badge, limit):
    url = (f"https://api.deadlock-api.com/v1/matches/metadata?min_unix_timestamp={t0}&max_unix_timestamp={t1}"
           f"&min_average_badge={badge}&min_duration_s=1500&limit={limit}&include_info=true&include_player_info=true"
           f"&include_player_final_stats=true&order_by=match_id&order_direction=desc")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001 - network hiccups: retry with backoff
            print("retry", attempt, e)
            time.sleep(2 ** (attempt + 1))
    raise SystemExit("fetch failed")


def slim(m):
    players = []
    for p in m.get("players") or []:
        c = (p.get("final_stats") or {}).get("custom_user_stats") or {}
        players.append({"hero_id": p["hero_id"], "custom": {k: v for k, v in c.items() if k.startswith(KEEP)}})
    return {"match_id": m["match_id"], "start_time": m.get("start_time"), "duration_s": m.get("duration_s"),
            "badge": m.get("average_badge"), "players": players}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--badge", type=int, default=91)
    ap.add_argument("--days", type=int, default=10)
    ap.add_argument("--per-day", type=int, default=420)
    ap.add_argument("--out", default=os.path.join(ROOT, "validation", "aim_sample.jsonl.gz"))
    a = ap.parse_args()
    now = int(time.time()) - 3 * 3600
    seen, n = set(), 0
    with gzip.open(a.out, "wt") as f:
        for d in range(a.days):
            ms = []
            for h in range(6):  # six 4-hour slices per day, so every region's prime time is in
                t1 = now - d * 86400 - h * 4 * 3600
                ms += window(t1 - 4 * 3600, t1, a.badge, a.per_day // 6)
            for m in ms:
                if m.get("match_mode") not in ("Ranked", 4) or m["match_id"] in seen:
                    continue
                seen.add(m["match_id"])
                f.write(json.dumps(slim(m)) + "\n")
                n += 1
            print(f"day -{d}: {len(ms)} matches, total {n}")


if __name__ == "__main__":
    main()
