"""Extract hero ability casts and hero-vs-hero damage from Phantom+ replays (Deadlock API demo queries).

usage: python3 -I fetch_replays.py <work dir> [n_matches=160] [workers=4] [min_badge=91] [days=4]
Writes <work>/raw/<match_id>.ndjson (one demo query per match, ~1 min each, 200 queries/h per IP). Result files are
served from demo-extracts.deadlock-api.com, which the cloud environment must allow.
"""
import concurrent.futures as cf
import json
import os
import random
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from demo_query import run  # noqa: E402

API = "https://api.deadlock-api.com/v1"
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}


def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120))


def query():
    """Every hero ability table's cast times (cooldown start changes), hero-vs-hero damage, pawns, Burrow state."""
    need = {"m_flCooldownStart", "m_hOwnerEntity", "m_eAbilitySlot", "m_nSubclassID", "m_iRemainingCharges"}
    tabs = [t["name"] for t in get(f"{API}/matches/demo/schema")["tables"]
            if need <= {c["name"] for c in t["columns"]} and "Upgrade" not in t["name"]]
    parts = [f"""SELECT 'cast' AS k, "m_hOwnerEntity" AS a, encode("m_nSubclassID", 'hex') AS s, CAST("m_flCooldownStart" AS DOUBLE) AS v, min(tick) AS tick FROM {t} WHERE "m_flCooldownStart" > 0 GROUP BY "m_hOwnerEntity", "m_nSubclassID", "m_flCooldownStart\"""" for t in tabs]
    parts.append("""SELECT 'dmg' AS k, CAST(entindex_attacker AS BIGINT) * 100000 + CAST(entindex_victim AS BIGINT) AS a, CAST(ability_id AS VARCHAR) AS s, CAST(damage AS DOUBLE) AS v, tick FROM DamageEvent WHERE attacker_class = 1 AND victim_class = 1 AND damage > 0""")
    parts.append("""SELECT 'pawn' AS k, entity_index AS a, CAST(max("m_iTeamNum") AS VARCHAR) AS s, CAST(max("m_nHeroID") AS DOUBLE) AS v, min(tick) AS tick FROM CCitadelPlayerPawn GROUP BY entity_index""")
    parts.append("""SELECT 'ground' AS k, "m_hOwnerEntity" AS a, CAST("m_bInGround" AS VARCHAR) AS s, 0.0 AS v, tick FROM CCitadel_Ability_Burrow WHERE "m_bInGround" IS NOT NULL""")
    return "\nUNION ALL\n".join(parts)


def candidates(work, min_badge, days):
    fn = os.path.join(work, "with_demo.json")
    if os.path.exists(fn):
        return json.load(open(fn))
    now = int(time.time())
    ms = get(f"{API}/matches/metadata?min_unix_timestamp={now - days * 86400}&max_unix_timestamp={now - 3 * 3600}"
             f"&min_average_badge={min_badge}&limit=3000&include_info=true&order_by=match_id&order_direction=desc")

    def salt(m):
        try:
            return m["match_id"] if get(f"{API}/matches/{m['match_id']}/salts").get("replay_salt") else None
        except Exception:  # noqa: BLE001
            return None
    with cf.ThreadPoolExecutor(8) as ex:
        ok = [i for i in ex.map(salt, ms) if i]
    json.dump(ok, open(fn, "w"))
    return ok


def main():
    work = sys.argv[1]
    n, workers = (int(sys.argv[2]) if len(sys.argv) > 2 else 160), (int(sys.argv[3]) if len(sys.argv) > 3 else 4)
    min_badge, days = (int(sys.argv[4]) if len(sys.argv) > 4 else 91), (int(sys.argv[5]) if len(sys.argv) > 5 else 4)
    os.makedirs(os.path.join(work, "raw"), exist_ok=True)
    ids = candidates(work, min_badge, days)
    random.Random(7).shuffle(ids)
    sql = query()

    def one(mid):
        out = os.path.join(work, "raw", f"{mid}.ndjson")
        if os.path.exists(out):
            return "cached"
        try:
            run(mid, sql, out + ".tmp")
            os.rename(out + ".tmp", out)
            return "ok"
        except BaseException as e:  # noqa: BLE001
            return f"err {str(e)[:100]}"
    with cf.ThreadPoolExecutor(workers) as ex:
        for mid, r in zip(ids[:n], ex.map(one, ids[:n])):
            print(mid, r, flush=True)


if __name__ == "__main__":
    main()
