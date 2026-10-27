"""Each hero's typical ability order from real Phantom+ players (data/ability_order.json, fight.ORDER_HEROES).

Without an ability order a loadout follows the hero's most played full order (fight.popular_ability_order, the
build aggregates' single top row), cut to the median number of ability events at its net worth. One order is not the
typical player: real Celeste players have Shining Wonder at tier 1.6 on average at 60% of the match, the popular
order 0.4 (the top row saves every point for Dazzling Trick first), and the same shows for Ivy's Kudzu Connection
(2.1 vs 0.0), Pocket's Affliction (1.4 vs 0.1), Baba's Feed The Birds (1.2 vs 0.0) and others.

Here the order is the hero's ability events (unlock = the ability's first, then each upgrade) sorted by the median
net worth real players had when they bought it, over every player-match of the hero in the sample (a player who
never bought it counts as above every net worth, so an event fewer than half the players reach sorts after the
others, by how many reach it). An ability's own events stay in their order. The loadout still takes the first
ability_events_for_souls(souls) events of it, as with the popular order.

usage: python3 -I scripts/ability_order.py [--sample PATH] [--check] [--write]
  --check: real mean tier per ability at 30 / 60 / 90% of the match beside the popular and the median order's
"""
import collections
import gzip
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
from deadsim import game  # noqa: E402
from deadsim import fight as F  # noqa: E402
import landing_rates as L  # noqa: E402

SAMPLE = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
OUT = os.path.join(ROOT, "data", "ability_order.json")


def nw_at(p, t):
    snaps = [s for s in p["stats"] if s["time_stamp_s"] <= t] or p["stats"][:1]
    return snaps[-1]["net_worth"]


def events(p, ids):
    """[(ability id, occurrence, buy time)] in buy order."""
    seen = collections.Counter()
    out = []
    for i, bt, _, _ in sorted(p["items"], key=lambda x: x[1]):
        if i in ids:
            out.append((i, seen[i], bt))
            seen[i] += 1
    return out


def median(xs, n):
    """Median of xs padded to n values with +inf."""
    xs = sorted(xs) + [math.inf] * (n - len(xs))
    return xs[(n - 1) // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def tiers_of(ids, evs):
    tiers, un = [0] * len(ids), [False] * len(ids)
    for aid in evs:
        k = ids.index(aid)
        if un[k]:
            tiers[k] = min(3, tiers[k] + 1)
        else:
            un[k] = True
    return tiers


def main():
    args = sys.argv[1:]
    sample = args[args.index("--sample") + 1] if "--sample" in args else SAMPLE
    G = game()
    buys = collections.defaultdict(lambda: collections.defaultdict(list))   # hero -> (aid, occ) -> [nw]
    players = collections.Counter()
    rows = []
    for line in gzip.open(sample, "rt"):
        m = json.loads(line)
        for p in m["players"]:
            ids = [a.id for a in G.hero(p["hero_id"]).abilities]
            players[p["hero_id"]] += 1
            evs = events(p, set(ids))
            for aid, occ, bt in evs:
                buys[p["hero_id"]][(aid, occ)].append(nw_at(p, bt))
            rows.append((m, p, ids, evs))
    out = {}
    for hid, b in buys.items():
        n = players[hid]
        keys = sorted(b, key=lambda k: (median(b[k], n), -len(b[k]), k[1]))
        # an ability's own events keep their order (occurrence k after k - 1)
        order, done = [], collections.Counter()
        pending = list(keys)
        while pending:
            for k in pending:
                if k[1] == done[k[0]]:
                    order.append(k[0])
                    done[k[0]] += 1
                    pending.remove(k)
                    break
        out[str(hid)] = {"name": G.hero(hid).name, "players": n, "order": order}
    if "--check" in args:
        acc = collections.defaultdict(lambda: [0.0, 0.0, 0.0, 0])
        for m, p, ids, evs in rows:
            h = G.hero(p["hero_id"])
            pop = F.popular_ability_order(h.id)
            med = out[str(h.id)]["order"]
            for frac in L.FRACS:
                t = m["duration_s"] * frac
                souls = nw_at(p, t)
                ne = F.ability_events_for_souls(souls)
                real = tiers_of(ids, [a for a, _, bt in evs if bt <= t])
                tp = tiers_of(ids, [a for a in pop[:ne] if a in ids]) if pop else [0] * 4
                tm = tiers_of(ids, med[:ne])
                for k in range(len(ids)):
                    x = acc[(h.name, frac, k)]
                    x[0] += real[k]
                    x[1] += tp[k]
                    x[2] += tm[k]
                    x[3] += 1
        err = collections.defaultdict(lambda: [0.0, 0.0, 0])
        for (hn, frac, k), (r, a, b, n) in sorted(acc.items()):
            e = err[hn]
            e[0] += abs(r - a) / n
            e[1] += abs(r - b) / n
            e[2] += 1
        print("hero: mean |real - popular| / |real - median order| tier gap over abilities x 30/60/90%")
        for hn, (a, b, n) in sorted(err.items(), key=lambda x: -x[1][0]):
            print(f"  {hn:15s} {a / n:.2f} -> {b / n:.2f}")
        tot = [sum(e[i] for e in err.values()) / sum(e[2] for e in err.values()) for i in (0, 1)]
        print(f"all heroes {tot[0]:.3f} -> {tot[1]:.3f}")
        for hn in args[args.index("--check") + 1:] if len(args) > args.index("--check") + 1 else []:
            if hn.startswith("--"):
                break
            for (h2, frac, k), (r, a, b, n) in sorted(acc.items()):
                if h2 == hn:
                    print(f"  {hn} {frac:.0%} {G.hero(hn).abilities[k].name:24s} real {r / n:.2f}  popular {a / n:.2f}"
                          f"  median order {b / n:.2f}")
    if "--write" in args:
        json.dump({"source": f"{os.path.basename(sample)}: ability events by real players' median net worth at "
                             "the buy (scripts/ability_order.py)",
                   "heroes": out}, open(OUT, "w"), indent=1)
        print("wrote", OUT)


if __name__ == "__main__":
    main()
