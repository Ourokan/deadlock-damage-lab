"""Per-hero holders vs non-holders of every item (holder_rates.py split by hero): hero damage dealt, deaths and kills
+ assists per minute, at the 27k and 37k search bands, all matches and each half by match id parity. Each metric
is [ratio, z, base per minute]; heroes x items with fewer than MIN_N held intervals are left out.

usage: python3 -I holder_rates_hero.py SRC_DIR OUT.json
"""
import glob
import gzip
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import real_rates as R  # noqa: E402

M = {"dealt": 2, "taken": 3, "deaths": 5}
R.METRICS = tuple(M) + ("ka",)
MIN_N = 60
items = R.shop_items()
BANDS = {27000: (20250, 36450), 37000: (27750, 49950)}
st = {(b, h): R.Strata() for b in BANDS for h in (0, 1, 2)}
for p in sorted(glob.glob(os.path.join(sys.argv[1], "*.jsonl.gz"))):
    with gzip.open(p, "rt") as f:
        for line in f:
            m = json.loads(line)
            if m.get("mode") not in (None, "Normal", 1):
                continue
            half = m["match_id"] % 2
            for pl in m["players"]:
                ab = pl.get("abandon_s") or 0
                buys = [b for b in pl["items"] if b[0] in items]
                s = pl["stats"]
                for a, b in zip(s, s[1:]):
                    mins = (b[0] - a[0]) / 60
                    if mins < R.MIN_MIN or (ab and ab < b[0]):
                        continue
                    for bb, (lo, hi) in BANDS.items():
                        if lo <= a[1] < hi:
                            held, part = R.held_sets(buys, items, a[0], b[0])
                            v = {k: (b[j] - a[j]) / mins for k, j in M.items()}
                            v["ka"] = (b[4] + b[6] - a[4] - a[6]) / mins
                            r = (pl["hero_id"], a[1], a[0], mins, v, held, part)
                            st[(bb, 2)].add(r)
                            st[(bb, half)].add(r)
out = {}
for (bb, h), s in st.items():
    t = defaultdict(dict)
    heroes = {k[0] for k in s.tot}
    for i, c in s.count.items():
        if c < MIN_N:
            continue
        for hero in heroes:
            e = s.compare(i, hero=hero)
            if e and e["n"] >= MIN_N:
                t[str(hero)][items[i]["name"]] = {"n": e["n"], **{k: [e[k]["ratio"], e[k]["z"], e[k]["base"]]
                                                                for k in R.METRICS}}
    out[f"{bb}_{h}"] = t
json.dump(out, open(sys.argv[2], "w"))
print("done", sum(s.n for (b, h), s in st.items() if h == 2))
