"""Download the raw game asset dumps normalize_game.py reads: python3 fetch_game.py RAW_DIR

Writes assets_<name>.json (heroes, items, generic-data, modifiers, ranks, client-versions), patches.json and
info.json from api.deadlock-api.com. These are plain REST endpoints, not the rate-limited SQL one.
"""
import json, os, sys, time, urllib.request

A = "https://api.deadlock-api.com"
FILES = {
    "assets_heroes.json": "/v1/assets/heroes",
    "assets_items.json": "/v1/assets/items",
    "assets_generic-data.json": "/v1/assets/generic-data",
    "assets_modifiers.json": "/v1/assets/modifiers",
    "assets_ranks.json": "/v1/assets/ranks",
    "assets_client-versions.json": "/v1/assets/client-versions",
    "patches.json": "/v1/patches",
    "info.json": "/v1/info",
}


def get(path):
    for i in range(5):
        try:
            req = urllib.request.Request(A + path, headers={"User-Agent": "deadlock-build-sim/0.1 (research)"})
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.load(r)
        except Exception as e:
            print("retry", path, i, e, flush=True)
            time.sleep(10 * (i + 1))
    raise RuntimeError(path)


def fetch(raw_dir):
    os.makedirs(raw_dir, exist_ok=True)
    for name, path in FILES.items():
        with open(os.path.join(raw_dir, name), "w") as f:
            json.dump(get(path), f)


if __name__ == "__main__":
    fetch(sys.argv[1])
