"""Does range drift fit real damage better or worse? Replays real builds as landing_rates.py --iterate does (current
landing factors applied) with drift off and on, and reports per hero how far each ability's and melee's damage
relative to gun damage is from the real damage matrix: mean |ln(real ratio / sim ratio)|, weighted by real share.

usage: python3 drift_check.py [max_players] [workers]
"""
import collections, gzip, json, math, os, random, sys
from concurrent.futures import ProcessPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..")); sys.path.insert(0, os.path.join(HERE, ".."))
import deadsim.mechanics as M  # noqa: E402
import landing_rates as L  # noqa: E402
from deadsim import game  # noqa: E402

L.ITERATE = True


def run(drift, jobs, workers):
    M.DEFAULT = M.Mechanics(range_drift=drift)
    sim = collections.defaultdict(collections.Counter)
    with ProcessPoolExecutor(workers) as ex:
        for hid, d, n, _ in ex.map(L.sim_player, jobs, chunksize=8):
            for k, v in d.items():
                if not k.startswith("_"):
                    sim[hid][k] += v
    return sim


def main():
    maxp = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
    G = game()
    real = collections.defaultdict(collections.Counter)
    jobs = []
    for line in gzip.open(os.path.join(L.ROOT, "validation", "matches_sample.jsonl.gz")):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] not in G.heroes or p["custom"].get(L.HITS, 0) < L.MIN_HITS:
                continue
            classes = [ab.class_name for ab in G.hero(p["hero_id"]).abilities]
            for k, v in p["damage_sources"].items():
                if k not in L.CATEGORY:
                    real[p["hero_id"]][L.real_key(k, classes)] += v
            jobs.append((m, p["slot"]))
    random.Random(1).shuffle(jobs)
    jobs = jobs[:maxp]
    res = {mode: run(mode == "on", jobs, workers) for mode in ("off", "on")}
    tot = collections.Counter()
    rows = []
    for hid in sorted(res["off"]):
        h = G.hero(hid)
        r = real[hid]
        keys = [ab.class_name for ab in h.abilities] + ["MELEE"]
        err = {}
        for mode in ("off", "on"):
            s = res[mode][hid]
            e = w = 0.0
            for k in keys:
                if r.get(k, 0) <= 0 or s.get(k, 0) <= 0 or r["GUN"] <= 0 or s["GUN"] <= 0:
                    continue
                share = r[k] / sum(r.values())
                e += share * abs(math.log((r[k] / r["GUN"]) / (s[k] / s["GUN"])))
                w += share
            err[mode] = e / w if w else 0.0
            tot[mode] += err[mode]
        rows.append((h.name, err["off"], err["on"]))
    for n, a, b in sorted(rows, key=lambda x: x[2] - x[1]):
        print(f"{n:15s} off {a:.3f} on {b:.3f} {'better' if b < a - 0.02 else 'worse' if b > a + 0.02 else ''}")
    print("mean", {k: round(v / len(rows), 4) for k, v in tot.items()})


if __name__ == "__main__":
    main()
