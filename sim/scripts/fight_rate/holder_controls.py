"""Why late holders of cheap items get more kills + assists (validation/tier1_death_rate.md): holders vs non-holders of
every item at the 27k / 37k search bands, matched like real_rates.py (hero, net worth // 2500, start time // 300 s)
plus one extra stratum each: previous interval's kills + assists per minute (prevka), souls gained per minute over
the previous interval (prevgain), the team's net worth lead (lead, 8000 bins clamped to +-4), the number of items
held (nheld), lead and items held (lead_nheld). Each match-id half separately (keys BAND_VAR_HALF).

usage: python3 -I holder_controls.py [SRC_DIR] [OUT.json]   (~30 min on the 74k matches)
"""
import glob, gzip, json, os, sys, math, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import real_rates as R
items = R.shop_items()
tier = {i: x.get("tier") for i, x in items.items()}
BANDS = {27000: (20250, 36450), 37000: (27750, 49950)}
VARS = ("base", "prevka", "prevgain", "lead", "nheld", "lead_nheld")
st = {(b, v, h): R.Strata() for b in BANDS for v in VARS for h in (0, 1)}
SRC = sys.argv[1] if len(sys.argv) > 1 else R.SRC
OUT = sys.argv[2] if len(sys.argv) > 2 else "holder_controls.json"
files = sorted(glob.glob(os.path.join(SRC, "*.jsonl.gz")))
def nw_at(stats, t):
    ts = [s[0] for s in stats]
    k = bisect.bisect_right(ts, t) - 1
    return stats[max(0, k)][1]
for p in files:
    with gzip.open(p, "rt") as f:
        for line in f:
            m = json.loads(line)
            if m.get("mode") not in (None, "Normal", 1):
                continue
            half = m["match_id"] % 2
            pls = m["players"]
            for pl in pls:
                ab = pl.get("abandon_s") or 0
                buys = [b for b in pl["items"] if b[0] in items]
                s = pl["stats"]
                for j in range(1, len(s) - 1):
                    a, b, pr = s[j], s[j + 1], s[j - 1]
                    mins = (b[0] - a[0]) / 60
                    if mins < R.MIN_MIN or (ab and ab < b[0]):
                        continue
                    for bb, (lo, hi) in BANDS.items():
                        if not lo <= a[1] < hi:
                            continue
                        held, part = R.held_sets(buys, items, a[0], b[0])
                        v = {"dealt": (b[2] - a[2]) / mins, "taken": (b[3] - a[3]) / mins,
                             "deaths": (b[5] - a[5]) / mins, "ka": (b[4] + b[6] - a[4] - a[6]) / mins}
                        pm = max(0.5, (a[0] - pr[0]) / 60)
                        pka = (a[4] + a[6] - pr[4] - pr[6]) / pm
                        gain = (a[1] - pr[1]) / pm
                        tl = sum((1 if q["team"] == pl["team"] else -1) * nw_at(q["stats"], a[0]) for q in pls)
                        nh = len(held)
                        keys = {"base": pl["hero_id"], "prevka": (pl["hero_id"], min(6, int(pka / 0.25))),
                                "lead": (pl["hero_id"], max(-4, min(4, int(tl // 8000)))),
                                "nheld": (pl["hero_id"], nh),
                                "lead_nheld": (pl["hero_id"], max(-4, min(4, int(tl // 8000))), nh),
                                "prevgain": (pl["hero_id"], min(8, int(gain // 300)))}
                        for var, k in keys.items():
                            st[(bb, var, half)].add((k, a[1], a[0], mins, v, held, part))
out = {}
for (bb, var, h), s in st.items():
    t = {}
    for i, c in s.count.items():
        if c < 200:
            continue
        e = s.compare(i)
        if e:
            t[items[i]["name"]] = {"tier": tier[i], "n": e["n"], **{k: [e[k]["ratio"], e[k]["z"]] for k in R.METRICS}}
    out[f"{bb}_{var}_{h}"] = t
json.dump(out, open(OUT, "w"))
print("done")
