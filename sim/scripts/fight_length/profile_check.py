"""Damage over time into the fight, sim vs real: the check that the fight-length expectation puts the damage where
real fights have it.

Real (data/fight_length.json, fit_length.py): share of fight damage in each 2 s slice, and the damage rate per fight
still going at the slice's start relative to the first slice (the opener). Sim: the damage audit's duels (real
builds both sides, the searches' skills), damage per duel still going by slice (in full), and the expected
profile = that x P(a real fight is still going) at the slice's middle, normalised.

usage: python3 profile_check.py [max_players=2000] [workers]
"""
import collections
import gzip
import json
import os
import random
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from deadsim import game  # noqa: E402
from deadsim.mechanics import LENGTH_STEP, real_length  # noqa: E402
import damage_audit as A  # noqa: E402
import landing_rates as L  # noqa: E402

A.PROFILE = True
K = 10


def job(j):
    return A.sim_player(j)[1]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
    G = game()
    jobs = []
    for line in gzip.open(os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")):
        m = json.loads(line)
        jobs += [(m, p["slot"]) for p in m["players"] if p["hero_id"] in G.heroes and L.gun_known(p)]
    random.Random(1).shuffle(jobs)
    tot = collections.Counter()
    with ProcessPoolExecutor(workers) as ex:
        for d in ex.map(job, jobs[:n], chunksize=8):
            tot.update({k: v for k, v in d.items() if k.startswith(("_by2s", "_alive"))})
    real = json.load(open(os.path.join(ROOT, "data", "fight_length.json")))["phases"]["all"]
    S = real_length()
    rate = [tot[f"_by2s:{k}"] / max(1, tot[f"_alive:{k}"]) for k in range(K)]
    s_mid = [S[min(len(S) - 1, int((2 * k + 1) / LENGTH_STEP))] for k in range(K)]
    exp = [rate[k] * tot[f"_alive:{k}"] / tot["_alive:0"] * s_mid[k] for k in range(K)]
    full = [tot[f"_by2s:{k}"] for k in range(K)]
    print("slice (s)          " + " ".join(f"{2 * k:>2d}-{2 * k + 2:<3d}" for k in range(K)))
    print("real share         " + " ".join(f"{v:6.2f}" for v in real["damage_by_2s"][:K]))
    print("sim share expected " + " ".join(f"{v / sum(exp):6.2f}" for v in exp))
    print("sim share in full  " + " ".join(f"{v / sum(full):6.2f}" for v in full))
    print("real rate          " + " ".join(f"{v:6.2f}" for v in real["rate_by_2s"][:K]))
    print("sim rate           " + " ".join(f"{v / rate[0]:6.2f}" for v in rate))
    print("sim duels going    " + " ".join(f"{tot[f'_alive:{k}'] / tot['_alive:0']:6.2f}" for k in range(K)))


if __name__ == "__main__":
    main()
