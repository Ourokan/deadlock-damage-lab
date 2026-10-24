"""Hero summons in Phantom+ replays (Deadlock API demo queries): spawn/despawn, health, damage taken from heroes.

usage: python3 -I fetch_summons.py <work dir> [n_matches=150] [workers=4] [min_badge=91] [days=4]
Writes <work>/raw/<match_id>.ndjson. Matches are picked from recent Phantom+ games that have a replay and a hero with
a summon (Graves, Sinclair, McGinnis first). Same API limits as fight_patterns/fetch_replays.py.
"""
import concurrent.futures as cf
import json
import os
import random
import sys
import time
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fight_patterns"))
from demo_query import run  # noqa: E402

API = "https://api.deadlock-api.com/v1"
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}

# entity table -> label (owner hero)
TABLES = {
    "CNPC_NecroSkele": "graves_zombie", "CNecro_HauntingSkullEntity": "graves_skull",
    "CCitadel_GraveStone_Blocker": "graves_stone", "CCitadel_MagicianTurret": "sinclair_assistant",
    "CNPC_ShieldedSentry": "mcginnis_turret", "CCitadel_MobileResupply": "mcginnis_specter",
    "CCitadel_GuidedArrow_OwlModel": "talon_owl", "CNPC_FamiliarHelper": "rem_helper",
    "CCitadel_Nano_Predatory_Statue": "calico_statue", "CCitadel_CatAnimating": "calico_cat",
    "CNPC_ChessPiece": "solomon_piece", "CNPC_Ratking_Rat": "ratking_rat", "CCitadel_Ratking_Standard": "ratking_standard",
    "CCitadel_RestorativeGooCube": "viscous_cube", "CCitadelViscousBall": "viscous_ball", "CNPC_NurseLeech": "nurse_leech",
}
SUMMON_HEROES = {76, 60, 8}
HEROES_WITH_SUMMONS = {76, 60, 8, 17, 79, 16, 85, 84, 35, 87}


def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300))


def query():
    parts = []
    for t, lab in TABLES.items():
        parts.append(f"""SELECT 'ent' AS k, entity_index AS a, '{lab}|' || CAST(delta_type AS VARCHAR) || '|' || COALESCE(CAST("m_hOwnerEntity" AS VARCHAR), '') || '|' || COALESCE(CAST("m_iTeamNum" AS VARCHAR), '') || '|' || COALESCE(CAST("m_iHealth" AS VARCHAR), '') AS s, CAST("m_iMaxHealth" AS DOUBLE) AS v, tick FROM {t} WHERE delta_type IN ('create', 'delete')""")
    victims = " UNION ".join(f"SELECT entity_index FROM {t}" for t in TABLES)
    parts.append(f"""SELECT 'sdmg' AS k, CAST(entindex_attacker AS BIGINT) * 100000 + CAST(entindex_victim AS BIGINT) AS a, COALESCE(CAST(ability_id AS VARCHAR), '') || '|' || COALESCE(CAST(victim_health_new AS VARCHAR), '') || '|' || COALESCE(CAST(attacker_class AS VARCHAR), '') AS s, CAST(damage AS DOUBLE) AS v, tick FROM DamageEvent WHERE victim_class <> 1 AND damage > 0 AND entindex_victim IN ({victims})""")
    parts.append("""SELECT 'dmg' AS k, CAST(entindex_attacker AS BIGINT) * 100000 + CAST(entindex_victim AS BIGINT) AS a, CAST(ability_id AS VARCHAR) AS s, CAST(damage AS DOUBLE) AS v, tick FROM DamageEvent WHERE attacker_class = 1 AND victim_class = 1 AND damage > 0""")
    parts.append("""SELECT 'pawn' AS k, entity_index AS a, CAST(max("m_iTeamNum") AS VARCHAR) AS s, CAST(max("m_nHeroID") AS DOUBLE) AS v, min(tick) AS tick FROM CCitadelPlayerPawn GROUP BY entity_index""")
    parts.append("""SELECT 'ctl' AS k, CAST(max("m_hHeroPawn") AS BIGINT) % 16384 AS a, CAST(max("m_PlayerDataGlobal__m_nHeroID") AS VARCHAR) AS s, 0.0 AS v, min(tick) AS tick FROM CCitadelPlayerController GROUP BY entity_index""")
    return "\nUNION ALL\n".join(parts)


def candidates(work, min_badge, days):
    fn = os.path.join(work, "with_demo.json")
    if os.path.exists(fn):
        return json.load(open(fn))
    now = int(time.time())
    ms = get(f"{API}/matches/metadata?min_unix_timestamp={now - days * 86400}&max_unix_timestamp={now - 3 * 3600}"
             f"&min_average_badge={min_badge}&limit=3000&include_info=true&include_player_info=true"
             f"&order_by=match_id&order_direction=desc")
    ms = [m for m in ms if HEROES_WITH_SUMMONS & {p["hero_id"] for p in m.get("players", [])}]
    ms.sort(key=lambda m: -len(SUMMON_HEROES & {p["hero_id"] for p in m["players"]}))

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
    n, workers = (int(sys.argv[2]) if len(sys.argv) > 2 else 150), (int(sys.argv[3]) if len(sys.argv) > 3 else 4)
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
