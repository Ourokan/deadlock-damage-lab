"""Every gun hit on an enemy hero with its resist / falloff / crit terms, from Phantom+ replays (demo queries), for
gun damage per hit by game phase (gun_phase.py --replays).

The matches are analysis/work/replay_damage's (validation sample replays, ~10 s per query, 200 queries/h per IP);
cached files are skipped. usage: python3 -I fetch_gun_hits.py <work dir> [n_matches=150] [workers=4]
Rows: k "dmg": a = attacker entindex * 100000 + victim entindex, s = "ability_id|pre_damage|effectiveness|crit_damage|
hits|victim_health_new|victim_health_max|damage_absorbed|victim_shield_max", v = damage
(health lost: barrier-absorbed damage is not in it, nor in the API damage matrix), tick (damage >= 0, main weapons only); k "ctl": pawn -> hero id.
"""
import concurrent.futures as cf
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fight_patterns"))
from demo_query import run  # noqa: E402


def weapon_ids():
    raw = json.load(open(os.path.join(HERE, "..", "..", "..", "data", "game", "raw", "items.json")))
    return sorted(x["id"] for x in raw if x.get("type") == "weapon" and x.get("hero"))


def sql():
    ids = ",".join(str(i) for i in weapon_ids())
    return "\nUNION ALL\n".join([
        f"""SELECT 'dmg' AS k, CAST(entindex_attacker AS BIGINT) * 100000 + CAST(entindex_victim AS BIGINT) AS a, CAST(ability_id AS VARCHAR) || '|' || COALESCE(CAST(pre_damage AS VARCHAR), '') || '|' || COALESCE(CAST(effectiveness AS VARCHAR), '') || '|' || COALESCE(CAST(crit_damage AS VARCHAR), '') || '|' || COALESCE(CAST(hits AS VARCHAR), '') || '|' || CAST(victim_health_new AS VARCHAR) || '|' || CAST(victim_health_max AS VARCHAR) || '|' || COALESCE(CAST(damage_absorbed AS VARCHAR), '') || '|' || COALESCE(CAST(victim_shield_max AS VARCHAR), '') AS s, CAST(damage AS DOUBLE) AS v, tick FROM DamageEvent WHERE attacker_class = 1 AND victim_class = 1 AND ability_id IN ({ids})""",
        """SELECT 'ctl' AS k, CAST(max("m_hHeroPawn") AS BIGINT) % 16384 AS a, CAST(max("m_PlayerDataGlobal__m_nHeroID") AS VARCHAR) AS s, 0.0 AS v, min(tick) AS tick FROM CCitadelPlayerController GROUP BY entity_index""",
    ])


def main():
    work = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 150
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    ids_dir = "/mnt/project-files/analysis/work/replay_damage/"
    os.makedirs(os.path.join(work, "raw"), exist_ok=True)
    ids = sorted({f.split(".")[0] for f in os.listdir(ids_dir) if f.endswith((".ndjson", ".ndjson.gz"))})[:n]
    q = sql()

    def one(mid):
        out = os.path.join(work, "raw", f"{mid}.ndjson.gz")
        if os.path.exists(out):
            return "cached"
        tmp = os.path.join(work, "raw", f"{mid}.tmp")
        try:
            run(mid, q, tmp)
            with open(tmp, "rb") as src, gzip.open(out + ".part", "wb") as dst:
                dst.write(src.read())
            os.rename(out + ".part", out)
            os.remove(tmp)
            return "ok"
        except BaseException as e:  # noqa: BLE001
            return f"err {str(e)[:100]}"
    with cf.ThreadPoolExecutor(workers) as ex:
        for mid, r in zip(ids, ex.map(one, ids)):
            print(mid, r, flush=True)


if __name__ == "__main__":
    main()
