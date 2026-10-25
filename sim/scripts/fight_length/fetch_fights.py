"""Fetch every hero-vs-hero DamageEvent with the victim's health after the hit, plus each pawn's hero, from Phantom+
replays (Deadlock API demo queries), for the real fight lengths (fit_length.py).

The matches are the validation sample's replays that analysis/work/replay_damage already has (they have replay salts
and net worth curves in validation/phantom_sample.jsonl.gz). One demo query per match, ~10 s each, 200 queries/h per
IP; cached files are skipped, so a cut-off run resumes.

usage: python3 -I fetch_fights.py <work dir> [n_matches=260] [workers=4] [--ids DIR]
Writes <work>/raw/<match_id>.ndjson.gz. Rows: k "dmg": a = attacker entindex * 100000 + victim entindex,
s = "ability_id|victim_health_new|victim_health_max", v = damage, tick; k "ctl": a = pawn entindex, s = hero id.
"""
import concurrent.futures as cf
import gzip
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fight_patterns"))
from demo_query import run  # noqa: E402

SQL = "\nUNION ALL\n".join([
    """SELECT 'dmg' AS k, CAST(entindex_attacker AS BIGINT) * 100000 + CAST(entindex_victim AS BIGINT) AS a, CAST(ability_id AS VARCHAR) || '|' || CAST(victim_health_new AS VARCHAR) || '|' || CAST(victim_health_max AS VARCHAR) AS s, CAST(damage AS DOUBLE) AS v, tick FROM DamageEvent WHERE attacker_class = 1 AND victim_class = 1 AND damage > 0""",
    """SELECT 'ctl' AS k, CAST(max("m_hHeroPawn") AS BIGINT) % 16384 AS a, CAST(max("m_PlayerDataGlobal__m_nHeroID") AS VARCHAR) AS s, 0.0 AS v, min(tick) AS tick FROM CCitadelPlayerController GROUP BY entity_index""",
])


def main():
    args = sys.argv[1:]
    ids_dir = "/mnt/project-files/analysis/work/replay_damage/"
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
