"""Pull real player builds (ranked, current patch) from deadlock-api SQL, one UTC day per query."""
import json, gzip, sys, time, urllib.request, urllib.parse, datetime, os, concurrent.futures as cf
OUT = sys.argv[1]; ITEMS = sys.argv[2]
START = datetime.date(2026, 9, 30); END = datetime.date.fromisoformat(sys.argv[3])
items = json.load(open(ITEMS))
upg = {x['id'] for x in items if x.get('type') == 'upgrade'}
abil = {x['id'] for x in items if x.get('type') == 'ability'}
Q = ("SELECT match_id, account_id, hero_id, won, net_worth, average_badge, duration_s, player_level, "
     "\"items.item_id\" iid, \"items.game_time_s\" t, \"items.sold_time_s\" s, \"items.upgrade_id\" u "
     "FROM match_player WHERE start_time >= TIMESTAMP '{a} {h1}:00:00+00' AND start_time < TIMESTAMP '{b} {h2}:00:00+00' "
     "AND game_mode='Normal' AND average_badge IS NOT NULL")
def get(q):
    url = "https://api.deadlock-api.com/v1/sql?" + urllib.parse.urlencode({"query": q})
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "deadlock-build-sim/0.1 (research)"}), timeout=300) as r: return json.load(r)
        except Exception as e:
            print("retry", i, e, flush=True); time.sleep(5 * (i + 1))
    raise RuntimeError(q)
def day(d):
    fn = os.path.join(OUT, f"{d}.jsonl.gz")
    if os.path.exists(fn): return d, -1
    rows = []
    for h in range(0, 24, 3):  # the SQL endpoint caps results at 100k rows, so query 3h windows
        b = d + datetime.timedelta(days=(h + 3) // 24)
        part = get(Q.format(a=d, b=b, h1=f"{h:02d}", h2=f"{(h + 3) % 24:02d}"))
        if len(part) >= 100000: raise RuntimeError(f"row cap hit {d} {h}")
        rows += part
    tmp = fn + ".tmp"
    with gzip.open(tmp, "wt") as f:
        for r in rows:
            buys = [(i, t, s) for i, t, s in zip(r["iid"], r["t"], r["s"]) if i in upg]
            ab = [(i, t) for i, t in zip(r["iid"], r["t"]) if i in abil]
            f.write(json.dumps({"match_id": r["match_id"], "account_id": r["account_id"], "hero_id": r["hero_id"],
                "won": r["won"], "net_worth": r["net_worth"], "badge": r["average_badge"], "duration_s": r["duration_s"],
                "level": r["player_level"], "final_items": [i for i, t, s in buys if not s],
                "purchases": buys, "ability_points": ab}, separators=(",", ":")) + "\n")
    os.replace(tmp, fn); return d, len(rows)
days = [START + datetime.timedelta(days=i) for i in range((END - START).days + 1)]
with cf.ThreadPoolExecutor(3) as ex:
    for d, n in ex.map(day, days): print(d, n, flush=True)
