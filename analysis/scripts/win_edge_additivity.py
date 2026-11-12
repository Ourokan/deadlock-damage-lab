"""Do summed item win edges add up in real games? (the check behind overall_search.WIN_REALIZED)

overall_search.win_value multiplies a build's score by exp(WIN_K x the sum of its items' real per-hero win edges), as
if a player holding items whose edges sum to S points won S points more often. This takes later real games, finds
each Ritualist+ player at the moment their held item souls first reach a checkpoint (9k / 15k / 24k), sums the
edges of what they hold exactly as win_value does (clear of noise, capped, movement items left out) and regresses
the win on that sum WITHIN strata of the edge script (hero, 5-min bin, team item-souls lead, own souls vs team), so
team lead and farm don't count. A slope of 1.0 would mean the edges add up as the blend assumes.

Edges come from the item_win_edge cache (default: its days, 2026-09-30..10-14), games from data/builds/player_builds
(default: 2026-10-31..11-05), so the test is out of sample. Teams: the six players of a match with the same result.

    python3 analysis/scripts/win_edge_additivity.py [--days 2026-10-31,...] [--min-badge 7]

Result 2026-11-12 (edges 09-30..10-14, games 10-31..11-05, Ritualist+): slope 0.40 / 0.38 / 0.35 win points per
point of summed edge at 9k / 15k / 24k item souls (+-0.03), linear over -8..+8; every split of the games into day
halves x account halves gives 0.32-0.43; Phantom+ only 0.38 / 0.39 / 0.30. Real 24k builds sum -1.4 points median,
+5 at the 95th percentile, while the overall search's best builds summed 2.5-22 (median 11): the blend extrapolated
far past any real build. Haze 0.23-0.55 per half (+-0.12..0.19).
"""
from __future__ import annotations

import argparse
import collections
import gzip
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [HERE, os.path.join(REPO, "damage", "scripts")]
import build_win_check as B  # noqa: E402
import overall_search as O  # noqa: E402

BUILDS = "/mnt/project-files/data/builds/player_builds"
COST = {i: x["cost"] for i, x in B.ITEMS.items()}
TIER = {i: x["tier"] for i, x in B.ITEMS.items()}
DAYS = "2026-10-31,2026-11-01,2026-11-02,2026-11-03,2026-11-04,2026-11-05"
CHECKS = (9000, 15000, 24000)


def edges():
    """hero -> item -> edge in points, filtered and capped as overall_search.win_value does."""
    heroes, _ = B.hero_edges(B.load())
    O.movement_value((), None)
    moving = O._move[2] | {i for row in O._move[3].values() for i in row}
    return {int(h): {int(i): max(-O.WIN_CAP, min(O.WIN_CAP, 100 * v["edge"])) for i, v in row.items()
                     if int(i) not in moving and (v["edge"] > 1.96 * v["se"] or v["edge"] < -O.WIN_NEG_Z * v["se"])}
            for h, row in heroes.items()}


def held(p, t):
    return [it for it, b, sold in p["purchases"] if b <= t and (sold == 0 or sold > t) and it in COST]


def souls(items):
    return sum(COST[i] for i in items)


def reach(p, c):
    for _, b, _ in sorted(p["purchases"], key=lambda x: x[1]):
        if souls(held(p, b)) >= c:
            return b
    return None


def rows(E, days, min_badge):
    """(check, day, hero, stratum, S, won, account) for every Ritualist+ player at each checkpoint."""
    out = []
    for day in days:
        by = collections.defaultdict(list)
        with gzip.open(f"{BUILDS}/{day}.jsonl.gz", "rt") as f:
            for line in f:
                p = json.loads(line)
                by[p["match_id"]].append(p)
        for ps in by.values():
            if len(ps) != 12:
                continue
            for p in ps:
                if p["badge"] // 10 < min_badge:
                    continue
                for c in CHECKS:
                    t = reach(p, c)
                    if t is None:
                        continue
                    own = held(p, t)
                    team = sum(souls(held(q, t)) for q in ps if q["won"] == p["won"])
                    enemy = sum(souls(held(q, t)) for q in ps if q["won"] != p["won"])
                    lead = max(-6, min(6, round((team - enemy) / 2500)))
                    rel = max(-4, min(4, round((souls(own) - team / 6) / 1500)))
                    eh = E.get(p["hero_id"], {})
                    s = sum(eh.get(i, 0.0) for i in set(own) if 1 <= TIER.get(i, 0) <= 4)
                    out.append((c, day, p["hero_id"], (p["hero_id"], t // 300, lead, rel), s, int(p["won"]), p["account_id"]))
    return out


def slope(rs):
    """within-stratum slope of the win (points) on the summed edge (points), with its binomial se."""
    g = collections.defaultdict(list)
    for r in rs:
        g[r[3]].append((r[4], r[5]))
    sxy = sxx = 0.0
    for v in g.values():
        if len(v) < 2:
            continue
        ms = sum(x for x, _ in v) / len(v)
        mw = sum(y for _, y in v) / len(v)
        for x, y in v:
            sxy += (x - ms) * (y - mw)
            sxx += (x - ms) ** 2
    return (100 * sxy / sxx, 100 * math.sqrt(0.25 / sxx)) if sxx else (float("nan"), float("nan"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", default=DAYS)
    ap.add_argument("--min-badge", type=int, default=7, help="badge // 10, as item_win_edge.bracket (7 = Ritualist+)")
    a = ap.parse_args()
    days = a.days.split(",")
    rs = rows(edges(), days, a.min_badge)
    half = days[: len(days) // 2]
    for c in CHECKS:
        rc = [r for r in rs if r[0] == c]
        b, se = slope(rc)
        hz = slope([r for r in rc if r[2] == 13])
        ss = sorted(r[4] for r in rc)
        splits = []
        for d in (True, False):
            for acc in (0, 1):
                splits.append(slope([r for r in rc if (r[1] in half) == d and r[6] % 2 == acc])[0])
        print(f"{c // 1000}k item souls: slope {b:.2f} +- {se:.2f} win points per summed edge point (n {len(rc)}), "
              f"day x account splits {' '.join(f'{x:.2f}' for x in splits)}, Haze {hz[0]:.2f} +- {hz[1]:.2f}; "
              f"summed edge p50 {ss[len(ss) // 2]:.1f} p95 {ss[int(0.95 * (len(ss) - 1))]:.1f} max {ss[-1]:.1f}")


if __name__ == "__main__":
    main()
