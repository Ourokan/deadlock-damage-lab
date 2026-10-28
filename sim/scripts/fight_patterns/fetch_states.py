"""Ability state changes for one hero's replays (Deadlock API demo queries): Mo & Krill's Burrow underground flag
(m_bInGround) and Graves' Jar of Dead charges (m_iRemainingCharges), one row per change (LAG), plus cast times.

usage: python3 -I fetch_states.py <krill|graves> <out dir> <match id> ...   (writes <out dir>/<match id>.ndjson)
"""
import concurrent.futures as cf
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from demo_query import run  # noqa: E402

COLS = {"krill": [("ground", "CCitadel_Ability_Burrow", "m_bInGround")],
        "graves": [("charges", "CCitadel_Ability_Necro_HauntingSkull", "m_iRemainingCharges")]}
CASTS = {"krill": ["CCitadel_Ability_Burrow"],
         "graves": ["CCitadel_Ability_Necro_HauntingSkull", "CCitadel_Ability_Necro_ZombieWall",
                    "CCitadel_Ability_Necro_GraveStone"]}


def query(hero):
    parts = []
    for k, tab, col in COLS[hero]:
        parts.append(f"""SELECT '{k}' AS k, o AS a, CAST(x AS VARCHAR) AS s, 0.0 AS v, tick FROM (SELECT "m_hOwnerEntity" AS o, "{col}" AS x, tick, LAG("{col}") OVER (PARTITION BY "m_hOwnerEntity" ORDER BY tick) AS p FROM {tab} WHERE "{col}" IS NOT NULL) WHERE p IS NULL OR p <> x""")
    for tab in CASTS[hero]:
        parts.append(f"""SELECT 'cast:{tab}' AS k, "m_hOwnerEntity" AS a, '' AS s, CAST("m_flCooldownStart" AS DOUBLE) AS v, min(tick) AS tick FROM {tab} WHERE "m_flCooldownStart" > 0 GROUP BY "m_hOwnerEntity", "m_flCooldownStart\"""")
    return "\nUNION ALL\n".join(parts)


def main():
    hero, out, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
    os.makedirs(out, exist_ok=True)
    sql = query(hero)

    def one(mid):
        fn = os.path.join(out, f"{mid}.ndjson")
        if os.path.exists(fn):
            return "cached"
        try:
            run(mid, sql, fn + ".tmp")
            os.rename(fn + ".tmp", fn)
            return "ok"
        except BaseException as e:  # noqa: BLE001
            return f"err {str(e)[:100]}"
    with cf.ThreadPoolExecutor(4) as ex:
        for mid, r in zip(ids, ex.map(one, ids)):
            print(mid, r, flush=True)


if __name__ == "__main__":
    main()
