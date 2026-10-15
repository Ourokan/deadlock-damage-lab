"""Stat model vs in-game snapshots: max health, spirit power and weapon damage % predicted by compute_stats from
the items a player owned at each stat snapshot (souls = net worth), compared with the recorded values.
Permanent pickups (power_up_buffs) are added on top: hp -> flat health, spirit -> spirit power, weapon damage ->
weapon %. usage: python3 scripts/validate_stats.py [sample.jsonl.gz]"""
import gzip
import json
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from deadsim import compute_stats, game  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "validation", "matches_sample.jsonl.gz")
G = game()
PICK = {"hp_": "hp", "spirit_": "spirit", "wp_": "weapon"}

OWN = []
res = {"max_health": [], "spirit_power": [], "weapon_pct": []}
for line in gzip.open(src):
    m = json.loads(line)
    for p in m["players"]:
        if p["hero_id"] not in G.heroes:
            continue
        for s in p["stats"][1:]:
            t = s["time_stamp_s"]
            own = [i for i, bt, st, _ in p["items"] if i in G.items and bt <= t and (st == 0 or st > t)
                   and G.items[i].cost > 0]
            try:
                st = compute_stats(p["hero_id"], own, souls=s["net_worth"])
            except Exception as e:  # noqa: BLE001
                print("skip", p["hero_id"], e)
                continue
            pk = {"hp": 0.0, "spirit": 0.0, "weapon": 0.0}
            for b in p["power_ups"]:
                kind = next((v for k, v in PICK.items() if (b["type"] or "").startswith(k)), None)
                if kind:
                    pk[kind] += sum(v for v, tt in zip(b["values"] or [], b["times"] or []) if tt <= t)
            OWN.append(own)
            res["max_health"].append((st.max_health + pk["hp"], s["max_health"]))
            res["spirit_power"].append((math.floor(st.spirit_power + pk["spirit"] + 1e-6), s["tech_power"]))   # shown floored
            res["weapon_pct"].append((st.weapon_pct * 100 + pk["weapon"], s["weapon_power"]))

print(f"{'stat':14s} {'n':>6s} {'within 1':>9s} {'within 2%':>9s} {'median err':>10s} {'median |err|':>12s}")
for k, rows in res.items():
    err = [a - b for a, b in rows]
    w1 = sum(abs(e) <= 1.0 for e in err) / len(err)
    w2 = sum(abs(a - b) <= max(1.0, 0.02 * abs(b)) for a, b in rows) / len(rows)
    print(f"{k:14s} {len(rows):6d} {w1:9.1%} {w2:9.1%} {statistics.median(err):10.2f} {statistics.median(map(abs, err)):12.2f}")

# Which owned items are most over-represented among misses (points at item stats the model gets wrong).
import collections  # noqa: E402
for k, rows in res.items():
    miss, alln = collections.Counter(), collections.Counter()
    nmiss = 0
    for (a, b), own in zip(rows, OWN):
        bad = abs(a - b) > max(1.0, 0.02 * abs(b))
        nmiss += bad
        for i in set(own):
            alln[i] += 1
            miss[i] += bad
    base = nmiss / len(rows)
    worst = sorted((i for i in alln if alln[i] >= 100), key=lambda i: -miss[i] / alln[i])[:8]
    print(f"\n{k}: items most often owned when off by >2% (overall miss rate {base:.1%})")
    for i in worst:
        errs = sorted(a - b for (a, b), own in zip(rows, OWN) if i in own)
        print(f"   {G.items[i].name:28s} miss {miss[i] / alln[i]:6.1%} of {alln[i]:5d}  median err {errs[len(errs) // 2]:+.1f}")
