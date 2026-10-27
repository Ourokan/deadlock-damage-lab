"""Real Phantom+ fight rates while holding an item: hero damage dealt, damage taken, deaths and kills + assists per
minute, holders vs non-holders at the same hero, net worth and game time.

Unit = one player's stat interval (the API's ~180-300 s snapshots, fetch_rates.py). An item is held in an interval
when it was bought by the interval's start and not sold before its end; intervals where it was bought or sold inside
are left out of that item's comparison. Matched like analysis/scripts/kill_participation.py: stratum = (hero, net
worth at the interval start // NW_BIN, start time // T_BIN); per stratum holders' mean - non-holders' mean, holder-
weighted; SE from the stratum variances. Reported as holders / non-holders ratios. These are associations, not a
controlled effect: who buys an item, and when, rides along.

usage: python3 -I real_rates.py [--src DIR] [--nw 20000 37000] [--out FILE.json]
"""
import argparse
import glob
import gzip
import json
import math
import os
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
SRC = "/mnt/project-files/analysis/work/fight_rate_ext"   # with imbued buys (fight_rate/ dropped them)
NW_BIN, T_BIN = 2500, 300
METRICS = ("dealt", "taken", "deaths", "ka")
MIN_MIN = 2.0     # minutes: shorter intervals (the last one) are noisy


def shop_items():
    with open(os.path.join(ROOT, "data", "game", "shop_items.json")) as f:
        return {x["id"]: x for x in json.load(f)}


def intervals(src=SRC, nw=(0, 10 ** 9), items=None):
    """Yield (hero, nw0, t0, minutes, metrics dict, held set, partial set) per player stat interval."""
    items = items or shop_items()
    for p in sorted(glob.glob(os.path.join(src, "*.jsonl.gz"))):
        with gzip.open(p, "rt") as f:
            for line in f:
                m = json.loads(line)
                if m.get("mode") not in (None, "Normal", 1):
                    continue
                for pl in m["players"]:
                    ab = pl.get("abandon_s") or 0
                    buys = [b for b in pl["items"] if b[0] in items]
                    st = pl["stats"]
                    for a, b in zip(st, st[1:]):
                        t0, t1 = a[0], b[0]
                        mins = (t1 - t0) / 60
                        if mins < MIN_MIN or (ab and ab < t1) or not (nw[0] <= a[1] < nw[1]):
                            continue
                        held, part = held_sets(buys, items, t0, t1)
                        yield (pl["hero_id"], a[1], t0, mins,
                               {"dealt": (b[2] - a[2]) / mins, "taken": (b[3] - a[3]) / mins,
                                "deaths": (b[5] - a[5]) / mins, "ka": (b[4] + b[6] - a[4] - a[6]) / mins},
                               held, part)


def held_sets(buys, items, t0, t1):
    """Shop items held through [t0, t1] (bought by t0, not sold before t1), and the ones held only part of it."""
    held, part = set(), set()
    for i, t, s in buys:
        if i not in items:
            continue
        if t <= t0 and (not s or s >= t1):
            held.add(i)
        elif t < t1 and (not s or s > t0):
            part.add(i)
    return held, part - held


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def var(xs):
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / max(1, len(xs) - 1)


class Strata:
    """Per-stratum sums of every metric for all rows, each item's holders and each item's partial holders, so all
    items compare in one pass over the rows."""

    def __init__(self, rows=()):
        z = lambda: [0, [0.0] * len(METRICS), [0.0] * len(METRICS)]   # noqa: E731 - n, sum, sum of squares
        self.tot = defaultdict(z)
        self.held = defaultdict(lambda: defaultdict(z))
        self.part = defaultdict(lambda: defaultdict(z))
        self.count = defaultdict(int)   # intervals each item is held in
        self.n = 0
        for r in rows:
            self.add(r)

    def add(self, r):
        self.n += 1
        k = (r[0], r[1] // NW_BIN, r[2] // T_BIN)
        v = [r[4][m] for m in METRICS]
        for i in r[5]:
            self.count[i] += 1
        for acc in [self.tot[k]] + [self.held[i][k] for i in r[5]] + [self.part[i][k] for i in r[6]]:
            acc[0] += 1
            for q, x in enumerate(v):
                acc[1][q] += x
                acc[2][q] += x * x

    def compare(self, item, hero=None, min_h=2, min_o=5):
        acc = [[0.0, 0.0, 0.0] for _ in METRICS]   # sum n*diff, sum n*base, var
        n = 0
        part = self.part.get(item, {})
        for k, h in self.held.get(item, {}).items():
            if hero is not None and k[0] != hero:
                continue
            t, p = self.tot[k], part.get(k)
            no = t[0] - h[0] - (p[0] if p else 0)
            if h[0] < min_h or no < min_o:
                continue
            n += h[0]
            for q in range(len(METRICS)):
                so = t[1][q] - h[1][q] - (p[1][q] if p else 0)
                qo = t[2][q] - h[2][q] - (p[2][q] if p else 0)
                mh, mo = h[1][q] / h[0], so / no
                vh = max(0.0, (h[2][q] - h[0] * mh * mh) / max(1, h[0] - 1))
                vo = max(0.0, (qo - no * mo * mo) / max(1, no - 1))
                a = acc[q]
                a[0] += h[0] * (mh - mo)
                a[1] += h[0] * mo
                a[2] += h[0] ** 2 * (vh / h[0] + vo / no)
        if not n:
            return None
        out = {"n": n}
        for q, m in enumerate(METRICS):
            d, base, v = acc[q][0] / n, acc[q][1] / n, math.sqrt(acc[q][2]) / n
            out[m] = {"ratio": (base + d) / base if base > 0 else 1.0, "z": d / v if v > 0 else 0.0, "base": base}
        return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=SRC)
    ap.add_argument("--nw", nargs=2, type=int, default=[20000, 37000])
    ap.add_argument("--out", default="")
    ap.add_argument("--min-holders", type=int, default=300)
    a = ap.parse_args()
    items = shop_items()
    st = Strata(intervals(a.src, tuple(a.nw), items))
    print(f"{st.n} intervals at {a.nw[0] // 1000}-{a.nw[1] // 1000}k")
    res = {}
    for i, c in sorted(st.count.items(), key=lambda x: -x[1]):
        if c < a.min_holders or items[i].get("slot") is None:
            continue
        e = st.compare(i)
        if e and e["n"] >= a.min_holders:
            res[items[i]["name"]] = e
    print(f"{'item':24s} {'slot':9s} {'n':>6s}  " + "  ".join(f"{m:>12s}" for m in METRICS))
    for nme, e in sorted(res.items(), key=lambda x: -x[1]["taken"]["ratio"]):
        slot = next(x["slot"] for x in items.values() if x["name"] == nme)
        print(f"{nme:24s} {slot:9s} {e['n']:6d}  " + "  ".join(
            f"{e[m]['ratio']:6.3f} ({e[m]['z']:+5.1f})" for m in METRICS))
    if a.out:
        json.dump({"nw": a.nw, "items": res}, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
