"""Pull real player builds (ranked) from deadlock-api SQL, one gzipped JSONL file per UTC day.

usage: python3 fetch_builds.py OUT_DIR SHOP_ITEMS_RAW_JSON END_DAY [--start DAY] [--max-days N]
                               [--interval SECONDS] [--deadline-min MINUTES]

Days run from --start (default: patch_start in data/patch.json) to END_DAY, keeping only the newest --max-days.
Days already in OUT_DIR are skipped, so it resumes. /v1/sql allows about 20 requests an hour per IP, so queries
are spaced --interval seconds apart (default 185) and a 429 waits 10 minutes. Each day is queried in 6-hour
windows, split further when a window hits the endpoint's 100k row cap. With --deadline-min the script stops
before starting a query it can't finish in time and exits with code 3 (finished days are kept).
Duplicate (match, player) rows, which match_player has, are dropped.
"""
import argparse, datetime, gzip, json, os, sys, time, urllib.error, urllib.parse, urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import patch_state  # noqa: E402

ROW_CAP = 100000
Q = ("SELECT match_id, account_id, hero_id, won, net_worth, average_badge, duration_s, player_level, "
     "\"items.item_id\" iid, \"items.game_time_s\" t, \"items.sold_time_s\" s, \"items.upgrade_id\" u "
     "FROM match_player WHERE start_time >= TIMESTAMP '{a}+00' AND start_time < TIMESTAMP '{b}+00' "
     "AND game_mode='Normal' AND average_badge IS NOT NULL")


class OutOfTime(Exception):
    pass


class Sql:
    def __init__(self, interval, deadline):
        self.interval, self.deadline, self.last = interval, deadline, 0.0

    def wait(self, seconds):
        if self.deadline and time.time() + seconds + 300 > self.deadline:  # 300 s: room for the query itself
            raise OutOfTime
        time.sleep(seconds)

    def get(self, q):
        url = "https://api.deadlock-api.com/v1/sql?" + urllib.parse.urlencode({"query": q})
        for i in range(8):
            self.wait(max(0.0, self.last + self.interval - time.time()))
            self.last = time.time()
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "deadlock-build-sim/0.1 (research)"})
                with urllib.request.urlopen(req, timeout=300) as r:
                    return json.load(r)
            except urllib.error.HTTPError as e:
                print("retry", i, e, flush=True)
                if e.code == 429:
                    self.wait(600)
            except Exception as e:
                print("retry", i, e, flush=True)
                self.wait(30 * (i + 1))
        raise RuntimeError(q)


def window(sql, a, b):
    rows = sql.get(Q.format(a=a.strftime("%Y-%m-%d %H:%M:%S"), b=b.strftime("%Y-%m-%d %H:%M:%S")))
    if len(rows) < ROW_CAP:
        return rows
    if b - a <= datetime.timedelta(hours=1):
        raise RuntimeError(f"row cap hit in one hour from {a}")
    mid = a + (b - a) / 2
    return window(sql, a, mid) + window(sql, mid, b)


def fetch_day(sql, out, d, upg, abil):
    fn = os.path.join(out, f"{d}.jsonl.gz")
    if os.path.exists(fn):
        return -1
    start = datetime.datetime.combine(d, datetime.time())
    rows = []
    for h in range(0, 24, 6):
        rows += window(sql, start + datetime.timedelta(hours=h), start + datetime.timedelta(hours=h + 6))
    tmp = fn + ".tmp"
    seen = set()   # match_player holds some rows more than once
    with gzip.open(tmp, "wt") as f:
        for r in rows:
            if (r["match_id"], r["account_id"]) in seen:
                continue
            seen.add((r["match_id"], r["account_id"]))
            buys = [(i, t, s) for i, t, s in zip(r["iid"], r["t"], r["s"]) if i in upg]
            ab = [(i, t) for i, t in zip(r["iid"], r["t"]) if i in abil]
            f.write(json.dumps({"match_id": r["match_id"], "account_id": r["account_id"], "hero_id": r["hero_id"],
                "won": r["won"], "net_worth": r["net_worth"], "badge": r["average_badge"], "duration_s": r["duration_s"],
                "level": r["player_level"], "final_items": [i for i, t, s in buys if not s],
                "purchases": buys, "ability_points": ab}, separators=(",", ":")) + "\n")
    os.replace(tmp, fn)
    return len(seen)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("items", help="raw items dump (data/game/raw/items.json)")
    ap.add_argument("end", help="last UTC day to fetch, YYYY-MM-DD")
    ap.add_argument("--start", default=None)
    ap.add_argument("--max-days", type=int, default=0)
    ap.add_argument("--interval", type=float, default=185.0)
    ap.add_argument("--deadline-min", type=float, default=0)
    a = ap.parse_args()
    items = json.load(open(a.items))
    upg = {x["id"] for x in items if x.get("type") == "upgrade"}
    abil = {x["id"] for x in items if x.get("type") == "ability"}
    start = patch_state.day(a.start or patch_state.load()["patch_start"])
    end = patch_state.day(a.end)
    days = [start + datetime.timedelta(days=i) for i in range((end - start).days + 1)]
    if a.max_days:
        days = days[-a.max_days:]
    os.makedirs(a.out, exist_ok=True)
    sql = Sql(a.interval, time.time() + 60 * a.deadline_min if a.deadline_min else 0)
    try:
        for d in days:
            print(d, fetch_day(sql, a.out, d, upg, abil), flush=True)
    except OutOfTime:
        print("out of time; finished days are kept, run again to continue", flush=True)
        sys.exit(3)


if __name__ == "__main__":
    main()
