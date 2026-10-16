"""Real-build snapshots at each souls budget, for opponents and for seeding the search.

For every ranked current-patch player row (data/builds/player_builds/*.jsonl.gz) and every budget B, take the
items the player held at the last purchase moment where the held item cost was still <= ITEM_SHARE(B) * B
(players hold ~80-89% of net worth in items; calibrated on validation/matches_sample.jsonl.gz, which has real
net worth over time). Rows whose final net worth never reached B are skipped for that budget.

Writes work/snapshots_<B>.json: {hero_id: [[item_ids, won, badge], ...]} (reservoir sample, up to CAP per hero)
and work/item_usage.json (how often each item appears per hero per budget).

usage: python3 scripts/build_pool.py [bracket]   (see BRACKETS)
"""
import glob
import gzip
import json
import os
import random
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "..", "sim"))
sys.path.insert(0, os.path.join(ROOT, "..", "data"))
from deadsim import game  # noqa: E402
import patch_state  # noqa: E402

BUDGETS = [10000, 18000, 27000, 37000, 50000]
CAP = 600
# rank brackets: name -> (min badge, max badge, aim percentile used in fights, days of games). badge = match
# average rank, tier*10 + subrank (5 Ritualist, 9 Phantom, 10 Ascendant, 11 Eternus). "all" writes the unsuffixed
# files. No match in the data averages Eternus 6 (116), so "eternus5" (115) is the top bracket available.
BRACKETS = {
    "all": (0, 999, "p50", 7),
    "low": (0, 59, "p25", 7),
    "phantom": (91, 999, "p75", 14),
    "ascendant": (101, 999, "p90", 14),
    "eternus": (111, 999, "p90", 14),
    "eternus5": (115, 999, "p90", 14),
}


# Phantom and up is the standard (Tyler, 2026-10-16): the dummy damage, buy order, survival and overall searches use
# its builds and aim, and the site opens on it. Patch reruns go tier by tier in pipeline/tiers.json order.
PRIMARY = "phantom"


def suffix(bracket):
    return "" if bracket in (None, "all") else "_" + bracket


def item_share(b):
    """Median held-item cost / net worth by net worth (validation/matches_sample.jsonl.gz)."""
    pts = [(6500, 0.80), (10000, 0.836), (15000, 0.858), (21500, 0.879), (30000, 0.894), (42000, 0.895), (60000, 0.885)]
    if b <= pts[0][0]:
        return pts[0][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if b <= x1:
            return y0 + (y1 - y0) * (b - x0) / (x1 - x0)
    return pts[-1][1]


def item_budget(b):
    return int(round(item_share(b) * b / 50) * 50)


def timeline(purchases, cost):
    """[(time, held cost after all events at that time)] in time order."""
    ev = defaultdict(int)
    for i, bt, st in purchases:
        c = cost.get(i)
        if not c:
            continue
        ev[bt] += c
        if st:
            ev[st] -= c
    out, c = [], 0
    for t in sorted(ev):
        c += ev[t]
        out.append((t, c))
    return out


def snapshot(purchases, tl, limit):
    """Items held at the last event before held cost first exceeds limit (None if never bought anything)."""
    t_snap, c_snap = None, 0
    for t, c in tl:
        if c > limit:
            break
        t_snap, c_snap = t, c
    if t_snap is None:
        return None
    return [i for i, bt, st in purchases if bt <= t_snap and (st == 0 or st > t_snap)], c_snap


def main():
    bracket = sys.argv[1] if len(sys.argv) > 1 else "all"
    lo_b, hi_b, _, days = BRACKETS[bracket]
    sfx = suffix(bracket)
    G = game()
    cost = {i: it.cost for i, it in G.items.items() if it.cost > 0}
    # the patch's full days only (data/patch.json), newest `days` of them
    patch_days = {f"{d}.jsonl.gz" for d in patch_state.build_days()}
    files = sorted(glob.glob(os.path.join(ROOT, "..", "data", "builds", "player_builds", "*.jsonl.gz")))
    files = [f for f in files if os.path.basename(f) in patch_days][-days:]
    rnd = random.Random(7)
    res = {b: defaultdict(list) for b in BUDGETS}
    seen = {b: Counter() for b in BUDGETS}
    usage = {b: defaultdict(Counter) for b in BUDGETS}
    for fn in files:
        print("reading", os.path.basename(fn), flush=True)
        for line in gzip.open(fn, "rt"):
            r = json.loads(line)
            if not lo_b <= r["badge"] <= hi_b:
                continue
            h = r["hero_id"]
            tl = timeline(r["purchases"], cost)
            for b in BUDGETS:
                if r["net_worth"] < b:
                    break
                lim = item_budget(b)
                s = snapshot(r["purchases"], tl, lim)
                if not s or s[1] < 0.85 * lim:
                    continue
                items = [i for i in s[0] if i in cost]
                usage[b][h].update(set(items))
                usage[b][h]["_n"] += 1
                seen[b][h] += 1
                row = [items, int(r["won"]), r["badge"]]
                lst = res[b][h]
                if len(lst) < CAP:
                    lst.append(row)
                else:
                    j = rnd.randrange(seen[b][h])
                    if j < CAP:
                        lst[j] = row
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
    for b in BUDGETS:
        json.dump({str(h): v for h, v in res[b].items()}, open(os.path.join(ROOT, "work", f"snapshots_{b}{sfx}.json"), "w"))
        print(b, "item budget", item_budget(b), "rows", sum(seen[b].values()))
    json.dump({str(b): {str(h): dict(c) for h, c in usage[b].items()} for b in BUDGETS},
              open(os.path.join(ROOT, "work", f"item_usage{sfx}.json"), "w"))


if __name__ == "__main__":
    main()
