"""Pull Phantom+ (average_badge >= 91) ranked player rows with team, kills, deaths and assists for the current patch,
two UTC days per /v1/sql query (about 70k rows; the endpoint caps a query at 100k and allows ~20 queries an hour).
Items come from data/builds/player_builds (same match_id/account_id); asking SQL for the item arrays timed out. One gzipped JSONL per window in analysis/work/kill_participation/, skipped if present (resumes).

    python3 scripts/fetch_kda.py START_DAY END_DAY   (END_DAY exclusive, e.g. 2026-09-30 2026-10-21)
"""
import datetime, gzip, json, os, sys, time, urllib.error, urllib.parse, urllib.request

OUT = "/mnt/project-files/analysis/work/kill_participation"
Q = ("SELECT match_id, account_id, hero_id, team, won, kills, deaths, assists, net_worth, duration_s, average_badge "
     "FROM match_player WHERE start_time >= TIMESTAMP '{a} 00:00:00+00' AND start_time < TIMESTAMP '{b} 00:00:00+00' "
     "AND game_mode='Normal' AND average_badge >= 91")


def get(q):
    url = "https://api.deadlock-api.com/v1/sql?" + urllib.parse.urlencode({"query": q})
    for i in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "deadlock-build-sim/0.1 (research)"})
            with urllib.request.urlopen(req, timeout=600) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            print("retry", i, e, flush=True)
            time.sleep(600 if e.code == 429 else 60)
        except Exception as e:
            print("retry", i, e, flush=True)
            time.sleep(60)
    raise RuntimeError(q)


def main():
    d = datetime.date.fromisoformat(sys.argv[1])
    end = datetime.date.fromisoformat(sys.argv[2])
    os.makedirs(OUT, exist_ok=True)
    while d < end:
        b = min(end, d + datetime.timedelta(days=2))
        path = os.path.join(OUT, f"{d}_{b}.jsonl.gz")
        if not os.path.exists(path):
            rows = get(Q.format(a=d, b=b))
            seen = set()
            with gzip.open(path + ".tmp", "wt") as f:
                for r in rows:
                    k = (r["match_id"], r["account_id"])
                    if k in seen:
                        continue
                    seen.add(k)
                    f.write(json.dumps(r, separators=(",", ":")) + "\n")
            os.replace(path + ".tmp", path)
            print(time.strftime("%H:%M:%S"), path, len(rows), "rows", "(CAP!)" if len(rows) >= 100000 else "", flush=True)
            time.sleep(200)
        d = b


if __name__ == "__main__":
    main()
