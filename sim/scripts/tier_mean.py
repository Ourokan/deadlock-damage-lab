"""Real players' mean ability tiers by net worth (data/tier_mean.json, fight.TIER_MEAN_HEROES).

The default order (popular or median) gives every sim fighter one tier set per net worth, but real players level
some abilities at very different times: real Hazes have Bullet Dance at tier 0.25 / 0.6 / 1.1 on average in the
2nd / 3rd / 4th fifth of the match, while every order (popular and median) keeps it at 0 until 18k. A hero in
fight.TIER_MEAN_HEROES fights below its net worth limit with these mean tiers instead (fractional: an upgrade's
flat values count x the fraction, deadsim.abilities CastCtx.raw), the probability-weighted tier over real players.

Per hero: every stats snapshot of every player (net worth then) with the player's tiers from their ability events
up to that time (sample items: an ability id's first buy unlocks it, each later one is an upgrade), binned by net
worth (BINS), the mean tier per ability over the bin's snapshots at the bin's median net worth.

usage: python3 tier_mean.py <sample.jsonl.gz>... [--parity even|odd] [--out PATH] [--heroes name,name]
"""
import collections
import gzip
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, ROOT)
from deadsim import game  # noqa: E402

OUT = os.path.join(ROOT, "data", "tier_mean.json")
BINS = [0, 3000, 5000, 7500, 10000, 13000, 16500, 20000, 25000, 30000, 36000, 45000, 10 ** 9]
MIN_N = 50


def tiers_at(p, t, ids):
    tiers = [0] * len(ids)
    seen = [False] * len(ids)
    for i, bt, _, _ in sorted(p["items"], key=lambda x: x[1]):
        if i in ids and bt <= t:
            k = ids.index(i)
            if seen[k]:
                tiers[k] = min(3, tiers[k] + 1)
            else:
                seen[k] = True
    return tiers


def main():
    a = sys.argv[1:]
    out, parity, names = OUT, None, None
    if "--out" in a:
        i = a.index("--out")
        out = a[i + 1]
        a = a[:i] + a[i + 2:]
    if "--parity" in a:
        i = a.index("--parity")
        parity = 0 if a[i + 1] == "even" else 1
        a = a[:i] + a[i + 2:]
    if "--heroes" in a:
        i = a.index("--heroes")
        names = set(a[i + 1].split(","))
        a = a[:i] + a[i + 2:]
    G = game()
    rows = collections.defaultdict(lambda: collections.defaultdict(list))   # hero id -> bin -> [(nw, tiers)]
    for fn in a:
        for line in gzip.open(fn, "rt"):
            m = json.loads(line)
            if parity is not None and m["match_id"] % 2 != parity:
                continue
            for p in m["players"]:
                h = G.heroes.get(p["hero_id"])
                if h is None or (names and h.name not in names):
                    continue
                ids = [ab.id for ab in h.abilities]
                for s in p["stats"]:
                    nw = s["net_worth"]
                    b = next(k for k in range(len(BINS) - 1) if BINS[k] <= nw < BINS[k + 1])
                    rows[h.id][b].append((nw, tiers_at(p, s["time_stamp_s"], ids)))
    res = {}
    for hid, bins in rows.items():
        pts = []
        for b in sorted(bins):
            v = bins[b]
            if len(v) < MIN_N:
                continue
            pts.append({"nw": round(statistics.median(x[0] for x in v)), "n": len(v),
                        "tiers": [round(sum(x[1][k] for x in v) / len(v), 3) for k in range(len(v[0][1]))]})
        res[str(hid)] = {"name": G.heroes[hid].name, "points": pts}
        print(G.heroes[hid].name, [(q["nw"], q["tiers"]) for q in pts[:9]])
    with open(out, "w") as fh:
        json.dump({"source": "real ability events by net worth, " + ", ".join(os.path.basename(x) for x in a)
                             + (f" ({['even', 'odd'][parity]} match ids)" if parity is not None else ""),
                   "note": "mean tier per ability (hero ability order) at each bin's median net worth; linear "
                           "between points (fight.TIER_MEAN_HEROES)", "heroes": res}, fh, indent=1)
        fh.write("\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
