"""Fetch an out-of-sample Phantom+ sample for some heroes: every aim_sample match (badge >= 91) not in phantom_sample
that has one of the heroes, through fetch_validation.get + slim. For refitting heroes whose rows were fitted on the few
phantom_sample players they have (validation/README.md "Small-sample heroes refit"); damage_audit.py with AUDIT_HEROES
reads only the named heroes' players, so one file serves several heroes.

usage: python3 scripts/fetch_hero_sample.py OUT.jsonl.gz "Hero,Hero,..." [threads=12]
(12 threads: ~3,700 matches in ~6 min, ~70 MB)
"""
import concurrent.futures as cf
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from fetch_validation import get, slim  # noqa: E402
from deadsim import game  # noqa: E402

VALID = os.path.join(HERE, "..", "validation")


def main(argv):
    out, names = argv[0], {n.strip() for n in argv[1].split(",") if n.strip()}
    threads = int(argv[2]) if len(argv) > 2 else 12
    G = game()
    want = {G.hero(n).id for n in names}
    with gzip.open(os.path.join(VALID, "phantom_sample.jsonl.gz"), "rt") as fh:
        seen = {json.loads(line)["match_id"] for line in fh}
    ids = []
    with gzip.open(os.path.join(VALID, "aim_sample.jsonl.gz"), "rt") as fh:
        for line in fh:
            m = json.loads(line)
            if m["match_id"] not in seen and (m.get("badge") or 0) >= 91 \
                    and any(p["hero_id"] in want for p in m["players"]):
                ids.append(m["match_id"])
    ids.sort(reverse=True)
    print(len(ids), "matches to fetch", flush=True)
    k = 0
    with gzip.open(out, "wt") as f, cf.ThreadPoolExecutor(threads) as ex:
        for m in ex.map(get, ids):
            if m and m.get("damage_matrix"):
                f.write(json.dumps(slim(m), separators=(",", ":")) + "\n")
                k += 1
    print("wrote", k, "matches")


if __name__ == "__main__":
    main(sys.argv[1:])
