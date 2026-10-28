"""Teammates of item holders vs teammates of non-holders: the other four players' (summed) per-minute deaths, kills +
assists, hero damage dealt and damage taken, and the enemy team's deaths, over the holder's stat interval. Matched
like holder_rates.py (the holder's hero, net worth // 2500, start time // 300 s) at the 27k and 37k search bands,
all matches and each half by match id parity. Written for the team items check (sim/validation/team_items.md): the
3v3 team value (team_value.json) says what an ally item gives teammates; this is what real teammates of holders get.

usage: python3 -I teammate_rates.py SRC_DIR OUT.json   (~10 min on the 74k matches)
"""
import glob
import gzip
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import real_rates as R  # noqa: E402

R.METRICS = ("mate_deaths", "mate_ka", "mate_dealt", "mate_taken", "foe_deaths")
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
            snap = [{s[0]: s for s in pl["stats"]} for pl in m["players"]]
            if any(pl.get("abandon_s") for pl in m["players"]):
                continue   # a leaver changes every teammate's rates
            for k, pl in enumerate(m["players"]):
                buys = [b for b in pl["items"] if b[0] in items]
                s = pl["stats"]
                for a, b in zip(s, s[1:]):
                    mins = (b[0] - a[0]) / 60
                    if mins < R.MIN_MIN:
                        continue
                    v = dict.fromkeys(R.METRICS, 0.0)
                    ok = True
                    for j, q in enumerate(m["players"]):
                        if j == k:
                            continue
                        qa, qb = snap[j].get(a[0]), snap[j].get(b[0])
                        if qa is None or qb is None:
                            ok = False
                            break
                        if q["team"] == pl["team"]:
                            v["mate_deaths"] += (qb[5] - qa[5]) / mins
                            v["mate_ka"] += (qb[4] + qb[6] - qa[4] - qa[6]) / mins
                            v["mate_dealt"] += (qb[2] - qa[2]) / mins
                            v["mate_taken"] += (qb[3] - qa[3]) / mins
                        else:
                            v["foe_deaths"] += (qb[5] - qa[5]) / mins
                    if not ok:
                        continue
                    for bb, (lo, hi) in BANDS.items():
                        if lo <= a[1] < hi:
                            held, part = R.held_sets(buys, items, a[0], b[0])
                            r = (pl["hero_id"], a[1], a[0], mins, v, held, part)
                            st[(bb, 2)].add(r)
                            st[(bb, half)].add(r)
out = {}
for (bb, h), s in st.items():
    t = {}
    for i, c in s.count.items():
        if c < 200:
            continue
        e = s.compare(i)
        if e:
            t[items[i]["name"]] = {"n": e["n"], **{k: [e[k]["ratio"], e[k]["z"], e[k]["base"]] for k in R.METRICS}}
    out[f"{bb}_{h}"] = t
json.dump(out, open(sys.argv[2], "w"))
print("done", sum(s.n for (b, h), s in st.items() if h == 2))
