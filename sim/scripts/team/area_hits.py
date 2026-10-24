"""How much more of an area item's damage lands on heroes other than the fight's main target, from Phantom+ replay
damage events, for the team value of area items (data/area_hits.json, used by overall_search.area_damage and the
damage audit).

Input: replay extracts with every hero-vs-hero DamageEvent (scripts/mechanics/split_shot_replays.py fetch writes
them; the fit's matches are kept gzipped in the project folder analysis/work/replay_damage) and the validation
sample those matches come from (validation/phantom_sample.jsonl.gz, for net worth over time). A fight is a run of
one attacker's hero damage with gaps under 8 s; its main target is the hero who took the most of the attacker's gun
damage. Per item: other / main = damage on every other hero / damage on the main target. Single-target gun procs
(BASELINE: Toxic Bullets, Mystic Shot) also land on others when the attacker switches targets, so an area item's
extra hits per main hit = its other / main - the baseline's. That is what a 1v1 duel misses: the duel's damage of
the item on its one target x extra_per_main.

By game phase: a fight's net worth is the match's mean player net worth at its start (the sample's per-player stats
snapshots). Early fights are lane trades and small ganks, late ones team fights, so the extra hits grow with net
worth. Few area items are bought early, so one phase curve for every area item: per net worth bin (each with its
own baseline), every area item's extra damage there / what the item's pooled extra_per_main predicts for its
main-target damage in that bin, made non-decreasing (pool adjacent violators, weight = the predicted damage; a dip
between bins is noise, fights do not get smaller later). Between the bins' mean net worths linear in ln net worth,
flat outside. An item's extra hits at net worth nw = its pooled extra_per_main x phase(nw)
(mechanics.area_extra(name, souls)). A straight line in ln net worth fits worse: the extra hits are low in lane,
rise to ~1.1x the pooled value by ~22k and stay there.

The position-based count (team_value.json "positions": other enemies within the radius at 1 s samples) gives
0.05-0.4 here, far below what the replays show, because most fight seconds in the position data are approach and
poke at 15-20 m, while area items fire in the brawl.

usage: python3 -I area_hits.py <raw dir>... [--sample validation/phantom_sample.jsonl.gz] [--write]
"""
import ast
import bisect
import collections
import glob
import gzip
import json
import math
import os
import random
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
T = 64
GAP_S = 8
AREA = ["Mystic Reverb", "Alchemical Fire", "Tesla Bullets", "Capacitor", "Scourge", "Torment Pulse", "Cold Front",
        "Arctic Blast"]
BASELINE = ["Toxic Bullets", "Mystic Shot"]
MIN_DMG = 20000      # real damage an item needs for a fit
NW_EDGES = [10000, 15000, 20000, 25000, 32000, 40000]   # fight net worth bins for the phase curve
BOOT = 200           # match bootstrap draws for the curve's 95% band


def nw_curves(sample, matches):
    """match id -> (duration s, [per player [(time s, net worth)]])."""
    out = {}
    for line in gzip.open(sample):
        m = json.loads(line)
        if str(m["match_id"]) not in matches:
            continue
        curves = []
        for p in m["players"]:
            st = ast.literal_eval(p["stats"]) if isinstance(p["stats"], str) else p["stats"]
            if st:
                curves.append([(s["time_stamp_s"], s["net_worth"]) for s in st])
        out[str(m["match_id"])] = (m["duration_s"], curves)
    return out


def mean_nw(curves, t):
    """The match's mean player net worth at t s (linear between snapshots, from 0 before the first)."""
    v = []
    for c in curves:
        i = bisect.bisect_left([x[0] for x in c], t)
        if i == 0:
            v.append(c[0][1] * max(0.0, t) / max(1, c[0][0]))
        elif i >= len(c):
            v.append(c[-1][1])
        else:
            (t0, a), (t1, b) = c[i - 1], c[i]
            v.append(a + (b - a) * (t - t0) / max(1, t1 - t0))
    return sum(v) / len(v)


def fights(fn, weap, items, nw):
    """(match, fight net worth or None, item, damage on the main target, damage on other heroes) per item and fight."""
    mid = os.path.basename(fn).split(".")[0]
    ev, last_tick = collections.defaultdict(list), 0
    for line in (gzip.open(fn, "rt") if fn.endswith(".gz") else open(fn)):
        r = json.loads(line)
        last_tick = max(last_tick, r["tick"])
        if r.get("k") == "dmg" and r.get("s"):
            ev[r["a"] // 100000].append((r["tick"], r["a"] % 100000, int(r["s"]), r["v"]))
    dur, curves = nw.get(mid, (None, None))
    off = max(0.0, last_tick / T - dur) if curves else 0.0   # ticks run from before the game clock starts
    rows = []
    for es in ev.values():
        es.sort()
        runs, last = [], -1e18
        for e in es:
            if e[0] - last > GAP_S * T:
                runs.append([])
            last = e[0]
            runs[-1].append(e)
        for f in runs:
            gun = collections.Counter()
            for _, v, i, d in f:
                if i in weap:
                    gun[v] += d
            if not gun:
                continue
            main = gun.most_common(1)[0][0]
            fnw = mean_nw(curves, f[0][0] / T - off) if curves else None
            acc = collections.defaultdict(lambda: [0.0, 0.0])
            for _, v, i, d in f:
                if i in items:
                    acc[items[i]][0 if v == main else 1] += d
            rows += [(mid, fnw, k, m, o) for k, (m, o) in acc.items()]
    return rows


def pooled(rows):
    acc = collections.defaultdict(lambda: [0.0, 0.0])
    for _, _, k, m, o in rows:
        acc[k][0] += m
        acc[k][1] += o
    base_m = sum(acc[b][0] for b in BASELINE)
    base = sum(acc[b][1] for b in BASELINE) / max(1.0, base_m)
    return acc, base_m, base


def phase_fit(rows, extra):
    """Net worth bins of every area item's extra damage: mean net worth, baseline, observed / predicted extra,
    predicted extra damage, and the non-decreasing fit."""
    edges = [0] + NW_EDGES + [math.inf]
    acc = collections.defaultdict(lambda: [0.0, 0.0])
    nws = collections.defaultdict(lambda: [0.0, 0.0])
    for _, nw, k, m, o in rows:
        if nw is None:
            continue
        b = bisect.bisect_right(edges, nw) - 1
        acc[(k, b)][0] += m
        acc[(k, b)][1] += o
        if k in extra:
            nws[b][0] += math.log(max(nw, 1.0)) * (m + o)
            nws[b][1] += m + o
    bins = []
    for b in range(len(edges) - 1):
        bm = sum(acc[(x, b)][0] for x in BASELINE)
        if not nws[b][1] or not bm:
            continue
        base = sum(acc[(x, b)][1] for x in BASELINE) / bm
        obs = sum(acc[(n, b)][1] - base * acc[(n, b)][0] for n in extra)
        pred = sum(extra[n] * acc[(n, b)][0] for n in extra)
        if pred > 0:
            bins.append({"net_worth": math.exp(nws[b][0] / nws[b][1]), "baseline": base, "phase": obs / pred,
                         "predicted": pred})
    # pool adjacent violators: non-decreasing, weighted by the predicted extra damage
    blocks = [[x["phase"], x["predicted"], 1] for x in bins]
    i = 0
    while i < len(blocks) - 1:
        if blocks[i][0] > blocks[i + 1][0]:
            (a, wa, na), (b, wb, nb) = blocks[i], blocks.pop(i + 1)
            blocks[i] = [(a * wa + b * wb) / (wa + wb), wa + wb, na + nb]
            i = max(0, i - 1)
        else:
            i += 1
    fit = [v for v, _, n in blocks for _ in range(n)]
    for x, v in zip(bins, fit):
        x["fit"] = v
    return bins

def main():
    args = sys.argv[1:]
    sample = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
    if "--sample" in args:
        sample = args[args.index("--sample") + 1]
        args.remove("--sample")
        args.remove(sample)
    dirs = [a for a in args if not a.startswith("--")]
    weap = {w["id"] for w in json.load(open(os.path.join(ROOT, "..", "data", "game", "weapons.json")))}
    items = {i["id"]: i["name"] for i in json.load(open(os.path.join(ROOT, "..", "data", "game", "shop_items.json")))
             if i.get("name") in AREA + BASELINE}
    files = {}
    for d in dirs:
        for fn in glob.glob(os.path.join(d, "*.ndjson")) + glob.glob(os.path.join(d, "*.ndjson.gz")):
            files.setdefault(os.path.basename(fn).split(".")[0], fn)
    nw = nw_curves(sample, set(files))
    print(f"{len(files)} replays, {len(nw)} with net worth in {sample}")
    rows = [r for fn in files.values() for r in fights(fn, weap, items, nw)]
    acc, base_m, base = pooled(rows)
    if base_m < MIN_DMG:
        # without the baseline every extra would be overstated by the target-switch share (~0.44)
        sys.exit(f"too little baseline damage ({', '.join(BASELINE)}: {base_m:.0f}); add replays that have them")
    out = {"source": f"{len(files)} Phantom+ replays, hero-vs-hero DamageEvent (scripts/team/area_hits.py)",
           "baseline_other_per_main": round(base, 3), "items": {}}
    print(f"baseline (single-target procs) other / main {base:.2f}")
    extra = {}
    for name in AREA:
        m, o = acc[name]
        if m + o < MIN_DMG:
            print(f"  {name:16s} too little damage ({m + o:.0f})")
            continue
        row = {"other_per_main": round(o / m, 3), "extra_per_main": round(max(0.0, o / m - base), 3),
               "damage": int(m + o)}
        out["items"][name] = row
        extra[name] = row["extra_per_main"]
        print(f"  {name:16s} other / main {row['other_per_main']:.2f}  extra hits per main hit {row['extra_per_main']:.2f}")

    bins = phase_fit(rows, extra)
    by = collections.defaultdict(list)
    for r in rows:
        by[r[0]].append(r)
    mids, rng, draws = sorted(by), random.Random(1), collections.defaultdict(list)
    for _ in range(BOOT):
        rs = [r for m in rng.choices(mids, k=len(mids)) for r in by[m]]
        a, _, b = pooled(rs)
        ex = {n: max(0.0, a[n][1] / a[n][0] - b) for n in extra if a[n][0]}
        for x in phase_fit(rs, ex):
            draws[min(range(len(bins)), key=lambda k: abs(math.log(bins[k]["net_worth"] / x["net_worth"])))].append(x["fit"])
    print("phase by fight net worth (all area items, observed extra / pooled prediction, non-decreasing fit, 95% band)")
    for k, x in enumerate(bins):
        d = sorted(draws[k]) or [x["fit"]]     # a bin no draw reached (small replay sets) gets no band
        x["band"] = [d[int(0.025 * len(d))], d[max(0, int(0.975 * len(d)) - 1)]]
        print(f"  nw {x['net_worth']:6.0f}  baseline {x['baseline']:.2f}  observed {x['phase']:.2f}  "
              f"fit {x['fit']:.2f} [{x['band'][0]:.2f}, {x['band'][1]:.2f}]")
    out["phase"] = {
        "note": "extra hits at fight net worth nw = items[name].extra_per_main x the bins' fit, linear in ln net worth "
                "between bins, flat outside; one curve for every area item",
        "bins": [{"net_worth": round(x["net_worth"]), "baseline": round(x["baseline"], 3),
                  "observed": round(x["phase"], 3), "fit": round(x["fit"], 3),
                  "fit_95": [round(v, 3) for v in x["band"]], "predicted_extra_damage": round(x["predicted"])}
                 for x in bins]}
    if "--write" in sys.argv:
        with open(os.path.join(ROOT, "data", "area_hits.json"), "w") as fh:
            json.dump(out, fh, indent=1)
            fh.write("\n")


if __name__ == "__main__":
    main()
