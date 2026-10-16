"""Pull deadlock-api aggregate build stats for the current patch, per hero.

usage: python3 fetch_analytics.py OUT_DIR RAW_HEROES_JSON [--slim]

The patch start comes from data/patch.json. --slim fetches only what the sim reads (oracle_plus ability orders)
and keeps the most played full order per hero, the form committed to the repo; without it every table is kept.
"""
import datetime, json, sys, time, os, urllib.request, urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import patch_state  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT, HEROES = args[0], args[1]
SLIM = "--slim" in sys.argv
start = patch_state.day(patch_state.load()["patch_start"])
PATCH_TS = int(datetime.datetime.combine(start, datetime.time(), datetime.timezone.utc).timestamp())
A = "https://api.deadlock-api.com"
heroes = [h for h in json.load(open(HEROES)) if h["player_selectable"] and not h["disabled"] and not h["in_development"]]
def get(path, **q):
    url = A + path + ("?" + urllib.parse.urlencode(q) if q else "")
    for i in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "deadlock-build-sim/0.1 (research)"}), timeout=300) as r:
                time.sleep(0.35); return json.load(r)
        except Exception as e:
            print("retry", path, i, e, flush=True); time.sleep(10 * (i + 1))
    raise RuntimeError(url)
RANKS = {"all": {}, "oracle_plus": {"min_average_badge": 81}}
def save(name, data):
    os.makedirs(os.path.dirname(os.path.join(OUT, name)), exist_ok=True)
    json.dump(data, open(os.path.join(OUT, name), "w"))
def slim_orders(rows):
    """The row fight.popular_ability_order() picks: most matches among full (16 point) orders."""
    rows = rows or []
    full = [r for r in rows if len(r["abilities"]) >= 16] or rows
    return [max(full, key=lambda r: r["matches"])] if full else []
save("hero_stats.json", {k: get("/v1/analytics/hero-stats", min_unix_timestamp=PATCH_TS, **v) for k, v in RANKS.items()})
for h in heroes:
    hid = h["id"]; d = {}
    if SLIM:
        rows = get("/v1/analytics/ability-order-stats", hero_id=hid, min_unix_timestamp=PATCH_TS, min_matches=50, **RANKS["oracle_plus"])
        if not rows and os.path.exists(os.path.join(OUT, f"per_hero/{hid}_{h['class_name']}.json")):
            print(hid, h["name"], "no orders yet on this patch, keeping the old file", flush=True); continue
        d = {"oracle_plus": {"ability_order_stats": slim_orders(rows)}}
    else:
        for k, v in RANKS.items():
            d[k] = {
                "item_stats": get("/v1/analytics/item-stats", hero_id=hid, min_unix_timestamp=PATCH_TS, **v),
                "item_stats_by_networth": get("/v1/analytics/item-stats", hero_id=hid, min_unix_timestamp=PATCH_TS, bucket="net_worth_by_1000", **v),
                "ability_order_stats": get("/v1/analytics/ability-order-stats", hero_id=hid, min_unix_timestamp=PATCH_TS, min_matches=50, **v),
            }
        d["published_builds"] = get("/v1/builds", hero_id=hid, only_latest="true", sort_by="favorites", sort_direction="desc", limit=50)
    save(f"per_hero/{hid}_{h['class_name']}.json", d); print(hid, h["name"], flush=True)
