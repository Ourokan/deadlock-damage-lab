"""Stat timelines + item timelines of current-patch Phantom+ matches, for the fight rate fit (fit_fight_rate.py).

The bulk metadata endpoint (reads the API's store, no SQL rate limit, ~5 s per 200 matches) returns each player's
stats every ~180-300 s (net worth, hero damage dealt / taken, kills, deaths, assists, max health) and item buys with
sell times. Writes one gzipped JSONL per hour window, one line per match, skipped if present (resumes).

usage: python3 -I fetch_rates.py [--start 2026-09-30] [--end 2026-10-25] [--out DIR] [--min-badge 91]
"""
import argparse
import datetime
import gzip
import json
import os
import time
import urllib.request

UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}
STAT_KEYS = ("time_stamp_s", "net_worth", "player_damage", "player_damage_taken", "kills", "deaths", "assists",
             "max_health", "self_healing")
URL = ("https://api.deadlock-api.com/v1/matches/metadata?min_unix_timestamp={a}&max_unix_timestamp={b}"
       "&min_average_badge={badge}&min_duration_s=900&limit=1000&include_info=true&include_player_info=true"
       "&include_player_stats=true&include_player_items=true&order_by=match_id&order_direction=desc")


def get(url):
    for i in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001 - retry anything transient
            print("retry", i, e, flush=True)
            time.sleep(10 * (i + 1))
    raise RuntimeError(url)


def slim(m):
    return {"match_id": m["match_id"], "duration_s": m["duration_s"], "winning_team": m.get("winning_team"),
            "badge": m.get("average_badge"), "mode": m.get("game_mode"),
            "players": [{"account_id": p.get("account_id"), "team": p["team"], "hero_id": p["hero_id"],
                         "net_worth": p.get("net_worth"), "abandon_s": p.get("abandon_match_time_s") or 0,
                         "stats": [[s.get(k) or 0 for k in STAT_KEYS] for s in p.get("stats") or []],
                         "items": [[it["item_id"], it["game_time_s"], it.get("sold_time_s") or 0]
                                   for it in p.get("items") or [] if not it.get("imbued_ability_id")]}
                        for p in m["players"]]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-09-30")
    ap.add_argument("--end", default="2026-10-25")
    ap.add_argument("--out", default="/mnt/project-files/analysis/work/fight_rate")
    ap.add_argument("--min-badge", type=int, default=91)
    ap.add_argument("--hours", type=int, default=3)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t = datetime.datetime.fromisoformat(a.start).replace(tzinfo=datetime.timezone.utc)
    end = datetime.datetime.fromisoformat(a.end).replace(tzinfo=datetime.timezone.utc)
    step = datetime.timedelta(hours=a.hours)
    while t < end:
        path = os.path.join(a.out, t.strftime("%Y-%m-%dT%H") + ".jsonl.gz")
        if not os.path.exists(path):
            ms = get(URL.format(a=int(t.timestamp()), b=int((t + step).timestamp()), badge=a.min_badge))
            with gzip.open(path + ".tmp", "wt") as f:
                for m in ms:
                    if m.get("players") and len(m["players"]) == 12:
                        f.write(json.dumps(slim(m), separators=(",", ":")) + "\n")
            os.replace(path + ".tmp", path)
            print(time.strftime("%H:%M:%S"), path, len(ms), "(CAP!)" if len(ms) >= 1000 else "", flush=True)
        t += step


if __name__ == "__main__":
    main()
