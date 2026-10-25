"""Fetch every hero ability cast (ability cooldown start) with its owner pawn from Phantom+ replays (Deadlock API demo
queries), for the real cast timing in fights (fit_cast_timing.py).

The matches are the fight-length replays (/mnt/project-files/analysis/work/fight_length/raw: hero damage events and
pawn -> hero), so fights and casts come from the same matches. One demo query per match, ~10-30 s each, 200
queries/h per IP; cached files are skipped, so a cut-off run resumes. Same tables as fight_patterns/fetch_replays.py
(ability entity tables, not Upgrade ones: item casts are item_use/fetch_item_casts.py).

usage: python3 -I fetch_ability_casts.py <work dir> [n_matches=260] [workers=4] [--ids DIR]
Writes <work>/raw/<match_id>.ndjson.gz. Rows: k "cast": a = owner pawn entindex, s = ability id, v = cooldown start
(replay s), tick.
"""
import concurrent.futures as cf
import gzip
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fight_patterns"))
sys.path.insert(0, os.path.join(HERE, "..", "item_use"))
from demo_query import run  # noqa: E402
from fetch_item_casts import item_id  # noqa: E402

API = "https://api.deadlock-api.com/v1"
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}


def query():
    """Hero ability tables: one row per (owner, ability, cooldown start). m_nSubclassID (little-endian hex) = ability
    id; owner handle % 16384 = pawn entindex."""
    schema = json.load(urllib.request.urlopen(urllib.request.Request(f"{API}/matches/demo/schema", headers=UA),
                                              timeout=120))
    need = {"m_flCooldownStart", "m_hOwnerEntity", "m_eAbilitySlot", "m_nSubclassID"}
    tabs = sorted(t["name"] for t in schema["tables"]
                  if need <= {c["name"] for c in t["columns"]} and "Upgrade" not in t["name"]
                  and "Item" not in t["name"])
    return "\nUNION ALL\n".join(
        f"""SELECT 'cast' AS k, CAST("m_hOwnerEntity" AS BIGINT) % 16384 AS a, encode("m_nSubclassID", 'hex') AS s, CAST("m_flCooldownStart" AS DOUBLE) AS v, min(tick) AS tick FROM {t} WHERE "m_flCooldownStart" > 0 GROUP BY "m_hOwnerEntity", "m_nSubclassID", "m_flCooldownStart\""""
        for t in tabs)


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
    sql = query()

    def one(mid):
        out = os.path.join(work, "raw", f"{mid}.ndjson.gz")
        if os.path.exists(out):
            return "cached"
        tmp = os.path.join(work, f"{mid}.tmp")
        try:
            run(mid, sql, tmp)
            with open(tmp) as f, gzip.open(out + ".tmp", "wt") as g:
                for line in f:
                    r = json.loads(line)
                    r["s"] = str(item_id(r["s"]))
                    g.write(json.dumps(r) + "\n")
            os.replace(out + ".tmp", out)
            os.remove(tmp)
            return "ok"
        except BaseException as e:  # noqa: BLE001
            return f"err {str(e)[:120]}"
    with cf.ThreadPoolExecutor(workers) as ex:
        for mid, r in zip(ids, ex.map(one, ids)):
            print(mid, r, flush=True)


if __name__ == "__main__":
    main()
