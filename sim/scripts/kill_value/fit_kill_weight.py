"""How often each item's damage turns into a kill in real Phantom+ fights, against the holder's own other damage.

The overall score counts every point of damage the same, but real damage is worth what it does to kills. Decay is
the clearest case (the build win check found it in ~120 of ~200 best builds while losing 2-5 win points on every
hero): its ticks are % of current health and non-lethal, so they land mostly on healthy targets that walk away. In
260 Phantom+ replays (sim/scripts/fight_length/fetch_fights.py) a point of Decay damage is followed by the victim's
death within WINDOW s about half as often as the same holder's gun and ability damage.

Method, per item with >= MIN_HOLDERS holders (player-matches dealing its damage):
- every hit counts, also DoT ticks after the two stopped trading: the sim's item damage is fitted to real TOTAL item
  damage (item_landing.py), and length_factors.py keeps that pooled ratio when the overall score books damage over
  real fight lengths, so the score already holds Decay's after-fight ticks (58% of real Decay damage lands while its
  holder hits the victim with nothing else within 3 s) and their low kill share belongs in the weight. --in-fight S
  keeps only hits with another source from the same attacker on the same victim within S s (Decay 0.60 at 3 s);
- converted = the victim dies (a hit to 0 health, any attacker) within WINDOW s after the hit;
- raw weight = item's converted share / the share expected from the same holder's other damage in the same match (sum over holders), so hero, rank and game state cancel;
- shrunk toward 1 by its holder-bootstrap variance (method-of-moments spread between items).

Writes sim/data/kill_weight.json {"items": {name: {"weight", "raw", "se", "holders", "damage"}}};
damage/scripts/overall_search.py multiplies each item's own damage by its weight (kill_weight).

usage: python3 sim/scripts/kill_value/fit_kill_weight.py [raw dir] [--window 10] [--in-fight 3]
"""
import argparse
import bisect
import collections
import gzip
import json
import os
import random
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
RAW = "/mnt/project-files/analysis/work/fight_length/raw/"
OUT = os.path.join(ROOT, "sim", "data", "kill_weight.json")
T = 64              # ticks per second
WINDOW = 10.0       # s after the hit the victim must die in (median real fight 7.5 s, mean 9 s)
IN_FIGHT = 0.0      # s; > 0: only hits with another source from the same attacker on the same victim within it
MIN_HOLDERS = 15
BOOT = 300


def read(fn):
    ev = []
    for line in gzip.open(fn, "rt"):
        r = json.loads(line)
        if r["k"] == "dmg" and r.get("s"):
            ab, hp, _ = r["s"].split("|")
            ev.append((r["tick"] / T, r["a"] // 100000, r["a"] % 100000, ab, float(hp), r["v"]))
    ev.sort()
    return ev


def holders(fn, window, in_fight):
    """{(match, attacker): {source id: [damage, converted damage]}} of one match's hero-on-hero hits."""
    ev = read(fn)
    deaths, pairs = collections.defaultdict(list), collections.defaultdict(list)
    for t, a, v, ab, hp, d in ev:
        if hp <= 0:
            deaths[v].append(t)
        pairs[(a, v)].append((t, ab))
    per = collections.defaultdict(lambda: collections.defaultdict(lambda: [0.0, 0.0]))
    for t, a, v, ab, hp, d in ev:
        if a == v:
            continue
        if in_fight > 0:
            pl = pairs[(a, v)]
            lo, hi = bisect.bisect_left(pl, (t - in_fight,)), bisect.bisect_right(pl, (t + in_fight, "~"))
            if not any(x[1] != ab for x in pl[lo:hi]):
                continue
        dl = deaths[v]
        k = bisect.bisect_left(dl, t - 1e-9)
        row = per[(fn, a)][ab]
        row[0] += d
        if k < len(dl) and dl[k] - t <= window:
            row[1] += d
    return per


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw", nargs="?", default=RAW)
    ap.add_argument("--window", type=float, default=WINDOW)
    ap.add_argument("--in-fight", type=float, default=IN_FIGHT)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    with open(os.path.join(ROOT, "data", "game", "shop_items.json")) as f:
        items = json.load(f)
    items = items if isinstance(items, list) else items.get("items", list(items.values()))
    name = {str(i["id"]): i["name"] for i in items}

    # per item: list of holder rows (item dmg, item converted, expected converted from the holder's other damage)
    rows = collections.defaultdict(list)
    files = sorted(f for f in os.listdir(a.raw) if f.endswith(".ndjson.gz"))
    for fn in files:
        for _, srcs in holders(os.path.join(a.raw, fn), a.window, a.in_fight).items():
            tot = sum(r[0] for r in srcs.values())
            totk = sum(r[1] for r in srcs.values())
            for ab, (d, k) in srcs.items():
                other = tot - d
                if ab in name and d > 0 and other > 0:
                    rows[name[ab]].append((d, k, d * (totk - k) / other))

    rng = random.Random(1)
    est = {}
    for n, rs in rows.items():
        if len(rs) < MIN_HOLDERS:
            continue
        exp = sum(r[2] for r in rs)
        if exp <= 0:
            continue
        raw = sum(r[1] for r in rs) / exp
        boots = []
        for _ in range(BOOT):
            s = [rs[rng.randrange(len(rs))] for _ in rs]
            e = sum(r[2] for r in s)
            if e > 0:
                boots.append(sum(r[1] for r in s) / e)
        est[n] = (raw, statistics.pstdev(boots), len(rs), sum(r[0] for r in rs))
    # method of moments: spread of the true weights around 1 = observed spread - mean sampling variance
    tau2 = max(0.0, statistics.mean((r - 1) ** 2 for r, *_ in est.values())
               - statistics.mean(se ** 2 for _, se, *_ in est.values()))
    out = {}
    for n, (raw, se, h, d) in sorted(est.items(), key=lambda kv: kv[1][0]):
        w = 1 + (raw - 1) * tau2 / (tau2 + se ** 2) if tau2 > 0 else 1.0
        out[n] = {"weight": round(w, 3), "raw": round(raw, 3), "se": round(se, 3), "holders": h, "damage": round(d)}
        print(f"{n:24s} {w:5.2f}  (raw {raw:.2f} +- {se:.2f}, {h} holders)")
    meta = {"source": f"{len(files)} Phantom+ replays (sim/scripts/fight_length/fetch_fights.py)",
            "window_s": a.window, "in_fight_s": a.in_fight, "tau": round(tau2 ** 0.5, 3),
            "formula": "share of the item's damage followed by the victim's death within window_s / the same share "
                       "of the holder's other damage in the same match; shrunk toward 1 (in_fight_s > 0: only hits "
                       "with another source from the same attacker on the victim within it)",
            "use": "damage/scripts/overall_search.py: each item's own damage x weight in the overall score"}
    with open(a.out, "w") as f:
        json.dump({"meta": meta, "items": out}, f, indent=1)
    print(f"tau {tau2 ** 0.5:.3f}; wrote {a.out}")


if __name__ == "__main__":
    main()
