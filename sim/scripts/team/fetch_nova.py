"""Healing Nova casts in Phantom+ replays (Deadlock API demo queries), for nova_heal.py: every cast (owner pawn, tick),
pawns (team, hero), pawn health / max health / life state changes and hero damage taken from 3 s before to 15 s after
each cast, pawn positions at the cast, and every hero kill. One demo query per match (~20-60 s, 200 queries/h per IP).

usage: python3 -I sim/scripts/team/fetch_nova.py <out dir> <match ids json> [workers=4]
Match ids: Phantom+ matches with a Nova buy that have a replay (salts endpoint replay_salt). Writes <out>/<id>.ndjson.gz;
cached files are skipped.
"""
import concurrent.futures as cf
import gzip
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fight_patterns"))
from demo_query import run  # noqa: E402

SQL = """WITH c AS (SELECT CAST("m_hOwnerEntity" AS BIGINT) % 16384 AS o, min(tick) AS t FROM CCitadel_UtilityUpgrade_HealthNova WHERE "m_flCooldownStart" > 0 GROUP BY "m_hOwnerEntity", "m_flCooldownStart"),
w AS (SELECT t - 192 AS t0, t + 960 AS t1, t FROM c),
pw AS (SELECT entity_index, tick, "m_iHealth" AS h, "m_iMaxHealth" AS mh, "m_lifeState" AS ls, LAG("m_iHealth") OVER (PARTITION BY entity_index ORDER BY tick) AS ph, LAG("m_iMaxHealth") OVER (PARTITION BY entity_index ORDER BY tick) AS pmh, LAG("m_lifeState") OVER (PARTITION BY entity_index ORDER BY tick) AS pls FROM CCitadelPlayerPawn WHERE "m_iHealth" IS NOT NULL)
SELECT 'nova' AS k, o AS a, '' AS s, 0.0 AS v, t AS tick FROM c
UNION ALL
SELECT 'pawn' AS k, entity_index AS a, CAST(max("m_iTeamNum") AS VARCHAR) AS s, CAST(max("m_nHeroID") AS DOUBLE) AS v, min(tick) AS tick FROM CCitadelPlayerPawn GROUP BY entity_index
UNION ALL
SELECT DISTINCT 'mod' AS k, CAST(m.entindex_caster AS BIGINT) * 100000 + CAST(m.entindex_parent AS BIGINT) AS a, '' AS s, 0.0 AS v, m.tick FROM ModifierAppliedEvent m JOIN c ON m.entindex_caster = c.o AND m.tick BETWEEN c.t - 8 AND c.t + 64
UNION ALL
SELECT DISTINCT 'hp' AS k, entity_index AS a, CAST(mh AS VARCHAR) || '|' || CAST(ls AS VARCHAR) AS s, CAST(h AS DOUBLE) AS v, pw.tick FROM pw JOIN w ON pw.tick BETWEEN w.t0 AND w.t1 WHERE ph IS NULL OR ph <> h OR pmh <> mh OR pls <> ls
UNION ALL
SELECT DISTINCT 'pos' AS k, p.entity_index AS a, CAST(p."CBodyComponent__m_cellX" AS VARCHAR) || '|' || CAST(p."CBodyComponent__m_cellY" AS VARCHAR) || '|' || CAST(p."CBodyComponent__m_vecX" AS VARCHAR) || '|' || CAST(p."CBodyComponent__m_vecY" AS VARCHAR) || '|' || CAST(p."CBodyComponent__m_cellZ" AS VARCHAR) || '|' || CAST(p."CBodyComponent__m_vecZ" AS VARCHAR) AS s, 0.0 AS v, p.tick FROM CCitadelPlayerPawn p JOIN c ON p.tick BETWEEN c.t - 4 AND c.t + 16 AND p.tick % 4 = 0
UNION ALL
SELECT DISTINCT 'dmg' AS k, CAST(d.entindex_attacker AS BIGINT) * 100000 + CAST(d.entindex_victim AS BIGINT) AS a, CAST(d.health_lost AS VARCHAR) || '|' || CAST(d.victim_health_new AS VARCHAR) || '|' || CAST(d.attacker_class AS VARCHAR) AS s, CAST(d.damage AS DOUBLE) AS v, d.tick FROM DamageEvent d JOIN w ON d.tick BETWEEN w.t0 AND w.t1 WHERE d.victim_class = 1
UNION ALL
SELECT 'kill' AS k, CAST(entindex_attacker AS BIGINT) * 100000 + CAST(entindex_victim AS BIGINT) AS a, CAST(victim_team_number AS VARCHAR) AS s, 0.0 AS v, tick FROM HeroKilledEvent"""


def main():
    out, ids = sys.argv[1], json.load(open(sys.argv[2]))
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    os.makedirs(out, exist_ok=True)

    def one(mid):
        fn = os.path.join(out, f"{mid}.ndjson.gz")
        if os.path.exists(fn) or os.path.exists(fn + ".none"):
            return "cached"
        try:
            run(mid, SQL, fn + ".tmp")
            with open(fn + ".tmp", "rb") as f, gzip.open(fn, "wb") as g:
                g.write(f.read())
            os.remove(fn + ".tmp")
            return "ok"
        except BaseException as e:  # noqa: BLE001
            return f"err {str(e)[:100]}"
    with cf.ThreadPoolExecutor(workers) as ex:
        for mid, r in zip(ids, ex.map(one, ids)):
            print(mid, r, flush=True)


if __name__ == "__main__":
    main()
