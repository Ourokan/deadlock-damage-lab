"""When real Phantom+ players open with a melee item proc in a fight, for Mechanics.melee_timing.

The sim's melee is a steady rate (Skill.melee_rate, a fraction of a hit every 1 / MELEE_MIN_RATE s from t = 2.5 s),
so a melee item (Spirit Strike, Spirit Snatch, Melee Charge...) first procs seconds into a duel and only once the
weights add up to a hit. Real holders open with it: 5-10% of fights by the first hit, ~20% by 2 s
(validation/opener_timing.md, damage in the first 2 s 0.3-0.7 real vs ~0 sim).

Real: the opener timing rows (opener_timing.py real, validation/opener_timing_real.json.gz): per hero and item,
P(first hit of the item on the fight's enemy by t | fight still going), Kaplan-Meier over the fights where the hero
held it. Pooled over heroes (fights-weighted; most hero x item rows are thin) into QBINS equal-probability values of
the first proc time (None past the share used by HORIZON: no opening proc in that fight). The proc lands with the
melee hit, so there is no cast -> hit time to take off.

usage: python3 -I melee_timing.py [real.json] [--write]   -> data/melee_timing.json
"""
import collections
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts", "cast_timing"))
from fit_cast_timing import GRID, HORIZON, QBINS, quantile  # noqa: E402

REAL = os.path.join(ROOT, "validation", "opener_timing_real.json.gz")
OUT = os.path.join(ROOT, "data", "melee_timing.json")
MIN_FIGHTS = 200    # pooled holder fights for an item row


def load(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt") as fh:
        return json.load(fh)


def fit(real_path=REAL):
    from deadsim import game
    from deadsim.engine import MELEE_ITEMS
    G = game()
    rows = load(real_path)["rows"]
    pool = collections.defaultdict(lambda: [0, [0.0] * len(GRID)])
    for r in rows.values():
        if r.get("kind") != "item" or r.get("class") not in MELEE_ITEMS or not r.get("used_by"):
            continue
        p = pool[r["class"]]
        p[0] += r["fights"]
        for k, v in enumerate(r["used_by"]):
            p[1][k] += v * r["fights"]
    h = int(HORIZON / 0.5)
    out = {}
    for cls, (n, c) in sorted(pool.items()):
        curve = [v / n for v in c]
        if n < MIN_FIGHTS or curve[h] <= 0:
            continue   # Lifestrike, Boxing Glove: no damage of their own in the replays
        q = []
        for b in range(QBINS):
            p = (b + 0.5) / QBINS
            q.append(None if p > curve[h] else round(quantile(curve, p), 3))
        out[cls] = {"name": G.items_by_class[cls].name, "fights": n,
                    "used_by_1_3_6_20s": [round(curve[k], 3) for k in (2, 6, 12, h)], "holds": q}
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    pos = [a for a in args if not a.startswith("--")]
    res = fit(pos[0] if pos else REAL)
    for cls, r in res.items():
        print(cls, r["fights"], r["used_by_1_3_6_20s"], r["holds"][:8])
    if "--write" in args:
        with open(OUT, "w") as fh:
            json.dump({"source": "validation/opener_timing_real.json.gz (260 Phantom+ replays), melee item holders' "
                                 "first proc on the fight's enemy, pooled over heroes "
                                 "(scripts/fight_length/melee_timing.py)",
                       "note": "QBINS equal-probability times (s) of a holder's opening melee proc (None: no opening "
                               "proc in that fight); Mechanics.melee_timing", "horizon_s": HORIZON, "items": res},
                      fh, indent=1)
            fh.write("\n")
