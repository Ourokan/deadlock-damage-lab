"""Pull deadlock-api aggregate build stats for the current patch, per hero."""
import json, sys, time, os, urllib.request, urllib.parse
OUT = sys.argv[1]; HEROES = sys.argv[2]
PATCH_TS = 1790726400  # 2026-09-30 00:00 UTC, first full day of the 09-29-2026 patch
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
    return None
RANKS = {"all": {}, "oracle_plus": {"min_average_badge": 81}}
def save(name, data):
    os.makedirs(os.path.dirname(os.path.join(OUT, name)), exist_ok=True)
    json.dump(data, open(os.path.join(OUT, name), "w"))
save("hero_stats.json", {k: get("/v1/analytics/hero-stats", min_unix_timestamp=PATCH_TS, **v) for k, v in RANKS.items()})
for h in heroes:
    hid = h["id"]; d = {}
    for k, v in RANKS.items():
        d[k] = {
            "item_stats": get("/v1/analytics/item-stats", hero_id=hid, min_unix_timestamp=PATCH_TS, **v),
            "item_stats_by_networth": get("/v1/analytics/item-stats", hero_id=hid, min_unix_timestamp=PATCH_TS, bucket="net_worth_by_1000", **v),
            "ability_order_stats": get("/v1/analytics/ability-order-stats", hero_id=hid, min_unix_timestamp=PATCH_TS, min_matches=50, **v),
        }
    d["published_builds"] = get("/v1/builds", hero_id=hid, only_latest="true", sort_by="favorites", sort_direction="desc", limit=50)
    save(f"per_hero/{hid}_{h['class_name']}.json", d); print(hid, h["name"], flush=True)
