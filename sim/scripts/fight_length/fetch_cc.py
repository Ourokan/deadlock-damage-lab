"""Fetch each pawn's crowd-control state from Phantom+ replays (Deadlock API demo queries), for the real CC time per
fight (cc_time.py).

Same matches as fetch_fights.py (fight_length/raw). One demo query per match, ~15 s each, 200 queries/h per IP; cached
files are skipped, so a cut-off run resumes.

usage: python3 -I fetch_cc.py <work dir> [n_matches=260] [workers=4] [--ids DIR]
Writes <work>/raw/<match_id>.ndjson.gz. Rows: k "st": a = pawn entindex, s = "<modifier state mask words>#<slow
starts>;<slow ends>;<slow speeds>" whenever the pawn's enabled-state mask or its slow ring changes (the first row of
each pawn too); k "nt": AbilityNotifyEvent, a = attacker entindex * 100000 + victim entindex, s = "ability_id|status
impact bits", v = 1 for a refresh.
"""
import concurrent.futures as cf
import gzip
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fight_patterns"))
from demo_query import run  # noqa: E402

SQL = """WITH p AS (SELECT tick, entity_index AS e, array_to_string("m_pModifierProp__m_bvEnabledStateMask", ',') AS m, array_to_string("m_flTimeSlowedStart", ',') || ';' || array_to_string("m_flTimeSlowedEnd", ',') || ';' || array_to_string("m_flSlowSpeed", ',') AS sl FROM CCitadelPlayerPawn),
q AS (SELECT tick, e, m, sl, LAG(m) OVER (PARTITION BY e ORDER BY tick) AS pm, LAG(sl) OVER (PARTITION BY e ORDER BY tick) AS psl FROM p)
SELECT 'st' AS k, CAST(e AS BIGINT) AS a, m || '#' || sl AS s, 0.0 AS v, tick FROM q WHERE pm IS NULL OR m <> pm OR sl <> psl
UNION ALL
SELECT 'nt' AS k, CAST(attacker AS BIGINT) % 16384 * 100000 + CAST(victim AS BIGINT) % 16384 AS a, CAST(ability_id AS VARCHAR) || '|' || COALESCE(CAST(status_impact AS VARCHAR), '') AS s, CASE WHEN is_refresh THEN 1.0 ELSE 0.0 END AS v, tick FROM AbilityNotifyEvent
"""


def main():
    args = sys.argv[1:]
    ids_dir = "/mnt/project-files/analysis/work/fight_length/raw/"
    if "--ids" in args:
        i = args.index("--ids")
        ids_dir = args[i + 1]
        args = args[:i] + args[i + 2:]
    work = args[0]
    n = int(args[1]) if len(args) > 1 else 260
    workers = int(args[2]) if len(args) > 2 else 4
    os.makedirs(os.path.join(work, "raw"), exist_ok=True)
    ids = sorted({f.split(".")[0] for f in os.listdir(ids_dir) if f.endswith((".ndjson", ".ndjson.gz"))})[:n]

    def one(mid):
        out = os.path.join(work, "raw", f"{mid}.ndjson.gz")
        if os.path.exists(out):
            return "cached"
        tmp = os.path.join(work, "raw", f"{mid}.tmp")
        try:
            run(mid, SQL, tmp)
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
