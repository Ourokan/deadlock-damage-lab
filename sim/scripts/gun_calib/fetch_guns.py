"""Shots fired and gun hits on heroes from Phantom+ replays (Deadlock API demo queries), for heroes whose gun records
no hero accuracy in the match stats (Graves, Deadman Danny) plus every other hero in the same matches as a reference.

usage: python3 -I fetch_guns.py <work dir> [n_matches=60] [workers=4]
Reads the replay match list <work>/with_demo.json (or ../summons' format: a JSON list of match ids that have a replay)
and writes <work>/raw/<match_id>.ndjson and <work>/meta/<match_id>.json (API final stats: hero accuracy).
One row per shot: the weapon entity's m_nShotNumber changes once per trigger pull (any weapon table that has it).
"""
import concurrent.futures as cf
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fight_patterns"))
from demo_query import run  # noqa: E402

API = "https://api.deadlock-api.com/v1"
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}
TARGET = {76, 78}


def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300))


def query():
    parts = []
    for tab in get(f"{API}/matches/demo/schema")["tables"]:
        t, cols = tab["name"], {c["name"] for c in tab["columns"]}
        if not {"m_nShotNumber", "m_hOwnerEntity"} <= cols:
            continue
        tether = 'max(CAST("m_bHasTetherTarget" AS INT))' if "m_bHasTetherTarget" in cols else "0"
        parts.append(f"""SELECT 'shot' AS k, CAST(max("m_hOwnerEntity") AS BIGINT) % 16384 AS a, '{t}' AS s, CAST({tether} AS DOUBLE) AS v, min(tick) AS tick FROM {t} WHERE "m_nShotNumber" > 0 GROUP BY entity_index, "m_nShotNumber\"""")
    parts.append("""SELECT 'dmg' AS k, CAST(entindex_attacker AS BIGINT) * 100000 + CAST(entindex_victim AS BIGINT) AS a, CAST(ability_id AS VARCHAR) || '|' || COALESCE(CAST(hits AS VARCHAR), '') || '|' || COALESCE(CAST(crit_damage AS VARCHAR), '') AS s, CAST(damage AS DOUBLE) AS v, tick FROM DamageEvent WHERE attacker_class = 1 AND victim_class = 1 AND damage > 0""")
    parts.append("""SELECT 'pawn' AS k, entity_index AS a, CAST(max("m_iTeamNum") AS VARCHAR) AS s, 0.0 AS v, min(tick) AS tick FROM CCitadelPlayerPawn GROUP BY entity_index""")
    parts.append("""SELECT 'ctl' AS k, CAST(max("m_hHeroPawn") AS BIGINT) % 16384 AS a, CAST(max("m_PlayerDataGlobal__m_nHeroID") AS VARCHAR) AS s, 0.0 AS v, min(tick) AS tick FROM CCitadelPlayerController GROUP BY entity_index""")
    return "\nUNION ALL\n".join(parts)


def meta(ids):
    out = {}
    for i in range(0, len(ids), 20):
        chunk = ids[i:i + 20]
        ms = get(f"{API}/matches/metadata?match_ids={','.join(map(str, chunk))}&include_info=true"
                 f"&include_player_info=true&include_player_final_stats=true&include_player_stats=true")
        for m in ms:
            out[m["match_id"]] = m
    return out


def main():
    work = sys.argv[1]
    n, workers = (int(sys.argv[2]) if len(sys.argv) > 2 else 60), (int(sys.argv[3]) if len(sys.argv) > 3 else 4)
    for d in ("raw", "meta"):
        os.makedirs(os.path.join(work, d), exist_ok=True)
    ids = json.load(open(os.path.join(work, "with_demo.json")))
    ms = meta(ids)
    pick = [i for i in ids if i in ms and TARGET & {p["hero_id"] for p in ms[i]["players"]}][:n]
    print(len(ids), "replays,", len(pick), "with Graves or Danny", flush=True)
    for i in pick:
        json.dump(ms[i], open(os.path.join(work, "meta", f"{i}.json"), "w"))
    sql = query()

    def one(mid):
        out = os.path.join(work, "raw", f"{mid}.ndjson")
        if os.path.exists(out):
            return mid, "cached"
        try:
            run(mid, sql, out + ".tmp")
            os.replace(out + ".tmp", out)
            return mid, "ok"
        except BaseException as e:  # noqa: BLE001 (demo_query raises SystemExit on 400/404)
            return mid, f"fail {e}"[:200]
    with cf.ThreadPoolExecutor(workers) as ex:
        for mid, st in ex.map(one, pick):
            print(mid, st, flush=True)


if __name__ == "__main__":
    main()
