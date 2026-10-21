"""Real bullet-hit distance histogram ("Outgoing Bullet Dist", creeps included) vs the sim's distance spread:
fixed distance (every hit in one bucket) and range drift (lognormal around the hero's distance with
data/fight_range.json log_sd). Shares per bucket, all sampled players pooled.

usage: python3 bullet_dist_check.py
"""
import gzip, json, math, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from deadsim.accuracy import DIST_EDGES, DIST_PREFIX, default_distance  # noqa: E402
from deadsim.mechanics import drift_params, DRIFT_MIN, DRIFT_MAX  # noqa: E402
from deadsim.data import game  # noqa: E402

EDGES = [0, 10, 20, 30, 40, 50, 75, 100, 150]


def ncdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def main():
    G = game()
    sd, _ = drift_params()
    real, fixed, drift = Counter(), Counter(), Counter()
    for line in gzip.open(os.path.join(HERE, "..", "..", "validation", "matches_sample.jsonl.gz")):
        m = json.loads(line)
        for p in m["players"]:
            c = p.get("custom") or {}
            b = {DIST_EDGES[k[len(DIST_PREFIX):]]: v for k, v in c.items()
                 if k.startswith(DIST_PREFIX) and k[len(DIST_PREFIX):] in DIST_EDGES}
            n = sum(b.values())
            if n < 300 or p["hero_id"] not in G.heroes:
                continue
            for e, v in b.items():
                real[e] += v / n
            d = default_distance(G.hero(p["hero_id"]).name)
            fixed[next(e for e in EDGES[1:] if d <= e)] += 1
            for lo, hi in zip(EDGES, EDGES[1:]):
                f = lambda x: 0.0 if x <= DRIFT_MIN else 1.0 if x >= DRIFT_MAX else ncdf(math.log(x / d) / sd)  # noqa: E731
                drift[hi] += f(hi) - f(lo)
    tot = sum(real.values())
    print(f"{'bucket':>8s} {'real':>6s} {'fixed':>6s} {'drift':>6s}")
    for lo, hi in zip(EDGES, EDGES[1:]):
        print(f"{lo:3d}-{hi:<4d} {real[hi] / tot:6.3f} {fixed[hi] / tot:6.3f} {drift[hi] / tot:6.3f}")


if __name__ == "__main__":
    main()
