"""Phantom+ match sample for the Improvements tab's benchmarks (web/improve.js, analysis/scripts/improve_benchmarks.cjs).

Recent ranked normal matches at or above an average badge, from the bulk metadata endpoint (no SQL, so no 20/h limit),
with every player's stat timeline, items and deaths. Only the stat keys the tab reads are kept.

    python3 analysis/scripts/fetch_improve_sample.py [--badge 91] [--days 7] [--n 2000] [--out analysis/work/improve/sample.jsonl.gz]
    python3 analysis/scripts/fetch_improve_sample.py --winners   # winning team of each sim/validation/phantom_sample match

The per-match stats the bulk endpoint lacks (hero accuracy, unspent souls, parries, damage per source) come from
sim/validation/phantom_sample.jsonl.gz, which has no match result: --winners adds it (analysis/work/improve/winners.json).
"""
import argparse
import gzip
import json
import time
import urllib.request

API = "https://api.deadlock-api.com/v1/matches/metadata"
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}
STAT_KEYS = ("time_stamp_s", "net_worth", "player_damage", "player_damage_taken", "kills", "deaths", "assists",
             "creep_kills", "denies", "gold_lane_creep", "gold_neutral_creep", "gold_death_loss", "level")


def fetch(url):
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001 - retry anything transient
            print("retry", i, e, flush=True)
            time.sleep(5 * (i + 1))
    raise SystemExit("API did not answer")


def slim(m):
    keep = ("account_id", "hero_id", "player_slot", "team", "kills", "deaths", "assists", "net_worth", "last_hits",
            "denies", "assigned_lane")
    return {"match_id": m["match_id"], "start_time": m["start_time"], "duration_s": m["duration_s"],
            "winning_team": m["winning_team"], "badge": m.get("average_badge"),
            "players": [{**{k: p.get(k) for k in keep},
                         "items": [[x["item_id"], x["game_time_s"], x.get("sold_time_s") or 0] for x in p.get("items") or []],
                         "stats": [{k: s.get(k) for k in STAT_KEYS} for s in p.get("stats") or []],
                         "death_details": [{"game_time_s": d.get("game_time_s"), "time_to_kill_s": d.get("time_to_kill_s")}
                                           for d in p.get("death_details") or []]}
                        for p in m["players"]]}


def winners(out="analysis/work/improve/winners.json"):
    ids = [json.loads(l)["match_id"] for l in gzip.open("sim/validation/phantom_sample.jsonl.gz")]
    won = {}
    for i in range(0, len(ids), 100):
        for m in fetch(f"{API}?match_ids={','.join(map(str, ids[i:i + 100]))}&include_info=true&limit=100"):
            won[m["match_id"]] = m["winning_team"]
    with open(out, "w") as f:
        json.dump(won, f)
    print(len(won), "of", len(ids))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--winners", action="store_true")
    ap.add_argument("--badge", type=int, default=91)   # 91 = Phantom 1
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--out", default="analysis/work/improve/sample.jsonl.gz")
    a = ap.parse_args()
    if a.winners:
        return winners()
    now = int(time.time())
    base = (f"{API}?min_unix_timestamp={now - a.days * 86400}&max_unix_timestamp={now - 3 * 3600}&min_average_badge={a.badge}"
            "&game_mode=normal&match_mode=ranked&min_duration_s=900&include_info=true&include_player_info=true"
            "&include_player_stats=true&include_player_items=true&include_player_death_details=true"
            "&order_by=match_id&order_direction=desc&limit=100")
    n, below = 0, None
    with gzip.open(a.out, "wt") as f:
        while n < a.n:
            ms = fetch(base + (f"&max_match_id={below - 1}" if below else ""))
            if not ms:
                break
            for m in ms:
                if len(m.get("players") or []) == 12:
                    f.write(json.dumps(slim(m), separators=(",", ":")) + "\n")
                    n += 1
            below = min(m["match_id"] for m in ms)
            print(n, below, flush=True)


if __name__ == "__main__":
    main()
