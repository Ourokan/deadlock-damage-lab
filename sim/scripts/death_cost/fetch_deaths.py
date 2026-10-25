"""Death details of the validation sample's Phantom+ matches, for the death cost fit (fit_death_cost.py).

The sample (validation/phantom_sample.jsonl.gz) keeps each death's time and killer but not its respawn time; the
match metadata has it (death_details[].death_duration_s). Writes one line per match: per player slot its hero, team,
net worth / kills / deaths snapshots and deaths (game time, respawn s, killer slot).

usage: python3 -I fetch_deaths.py [--sample validation/phantom_sample.jsonl.gz] [--out DIR] [--workers 4]
"""
import argparse
import concurrent.futures as cf
import gzip
import json
import os
import time
import urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}


def get(mid):
    url = f"https://api.deadlock-api.com/v1/matches/{mid}/metadata"
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return json.load(r)["match_info"]
        except Exception:  # noqa: BLE001 - retry anything transient
            time.sleep(3 * (i + 1))
    return None


def slim(m):
    return {"match_id": m["match_id"], "duration_s": m["duration_s"], "winning_team": m.get("winning_team"),
            "players": [{"slot": p["player_slot"], "team": p["team"], "hero_id": p["hero_id"],
                         "stats": [{k: s.get(k) for k in ("time_stamp_s", "net_worth", "kills", "deaths")}
                                   for s in p.get("stats") or []],
                         "deaths": [{"t": d.get("game_time_s"), "respawn_s": d.get("death_duration_s"),
                                     "killer": d.get("killer_player_slot")} for d in p.get("death_details") or []]}
                        for p in m["players"]]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", default=os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz"))
    ap.add_argument("--out", default="/mnt/project-files/analysis/work/death_cost")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    ids = [json.loads(line)["match_id"] for line in gzip.open(a.sample)]
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, "deaths.jsonl.gz")
    done = set()
    if os.path.exists(path):
        done = {json.loads(line)["match_id"] for line in gzip.open(path)}
    todo = [i for i in ids if i not in done]
    with gzip.open(path, "at") as out, cf.ThreadPoolExecutor(a.workers) as ex:
        for k, m in enumerate(ex.map(get, todo)):
            if m:
                out.write(json.dumps(slim(m)) + "\n")
            if k % 50 == 0:
                print(k, len(todo), flush=True)


if __name__ == "__main__":
    main()
