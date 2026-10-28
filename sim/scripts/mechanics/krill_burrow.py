"""Mo & Krill: is Mo underground when a fight starts, by game phase (Phantom+ replays; Mechanics.burrow_prefight).

A fight is a run of hero-vs-hero damage to or from Mo with gaps under GAP s and at least MIN_DMG damage (as
fight_patterns/replay_openers.py). Mo starts it burrowed when he is underground at any moment from PRE s before its
first hit to POST s after. Also: when his first Burrow emerges after a fight's start that did not open burrowed.
The phase is the fight start's share of the replay's last damage tick.

usage: python3 -I krill_burrow.py [--write] [states dir] [fight_length raw dir]
--write: data/burrow_prefight.json, each bin's share at Mo's median net worth at the bin's middle (phantom_sample)
(states: scripts/fight_patterns/fetch_states.py krill; default the project folder analysis/work/krill_graves/krill)
"""
import collections
import glob
import gzip
import json
import os
import sys

T = 64.0
MO = 18
GAP, MIN_DMG, PRE, POST = 8.0, 300, 3.0, 0.5
BINS = (0.0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.01)


def fights(ev):
    """ev: [(s, dmg)] sorted -> [(start, end, dmg)]"""
    out, cur = [], None
    for t, v in ev:
        if cur and t - cur[1] <= GAP:
            cur[1], cur[2] = t, cur[2] + v
        else:
            if cur and cur[2] >= MIN_DMG:
                out.append(tuple(cur))
            cur = [t, t, v]
    if cur and cur[2] >= MIN_DMG:
        out.append(tuple(cur))
    return out


def ground_at(st, lo, hi):
    cur = False
    for t, g in st:
        if t > hi:
            break
        if t >= lo and g:
            return True
        cur = g
    return cur


def read(states_fn, dmg_fn):
    ground = collections.defaultdict(list)
    for line in open(states_fn):
        r = json.loads(line)
        if r["k"] == "ground":
            ground[r["a"] & 0x3FFF].append((r["tick"] / T, r["s"] == "true"))
    hero, ev, last = {}, collections.defaultdict(list), 0
    for line in gzip.open(dmg_fn, "rt"):
        r = json.loads(line)
        if r["k"] == "ctl":
            hero[r["a"]] = int(r["s"])
        elif r["k"] == "dmg":
            att, vic = r["a"] // 100000, r["a"] % 100000
            ev[att, vic].append((r["tick"] / T, r["v"]))
            last = max(last, r["tick"] / T)
    return ground, hero, ev, last


HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, "..", "..", "validation", "phantom_sample.jsonl.gz")


def median_nw(fracs, hero=MO):
    """Mo's median net worth at each match fraction in the audit sample."""
    vals = {f: [] for f in fracs}
    for line in gzip.open(SAMPLE, "rt"):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] != hero or not p["stats"]:
                continue
            for f in fracs:
                t = f * m["duration_s"]
                vals[f].append(min(p["stats"], key=lambda s: abs((s["time_stamp_s"] or 0) - t))["net_worth"])
    return {f: sorted(v)[len(v) // 2] for f, v in vals.items()}


def main():
    args = [a for a in sys.argv[1:] if a != "--write"]
    sd = args[0] if args else "/mnt/project-files/analysis/work/krill_graves/krill"
    dd = args[1] if len(args) > 1 else "/mnt/project-files/analysis/work/fight_length/raw"
    n, g, emerge = collections.Counter(), collections.Counter(), collections.defaultdict(list)
    for fn in sorted(glob.glob(os.path.join(sd, "*.ndjson"))):
        mid = os.path.basename(fn).split(".")[0]
        dfn = os.path.join(dd, f"{mid}.ndjson.gz")
        if not os.path.exists(dfn):
            continue
        ground, hero, ev, last = read(fn, dfn)
        for mo, st in ground.items():
            if hero.get(mo) != MO:
                continue
            st.sort()
            mine = sorted(x for (a, v), es in ev.items() if (a == mo or v == mo) and a in hero and v in hero
                          and hero[a] != hero[v] for x in es)
            # damage between heroes on different teams only: ctl has no team, so rely on a != v (ally damage is rare)
            for s, e, d in fights(mine):
                b = next(i for i in range(len(BINS) - 1) if BINS[i] <= s / last < BINS[i + 1])
                n[b] += 1
                if ground_at(st, s - PRE, s + POST):
                    g[b] += 1
                else:
                    ups = [t for (t, x), (t2, x2) in zip(st, st[1:]) if x and not x2 and s < t2 <= e + 1]
                    emerge[b].append(next((t2 - s for (t, x), (t2, x2) in zip(st, st[1:])
                                           if x and not x2 and s < t2 <= e + 1), None))
    print("phase      fights  burrowed at start  first emerge later (median s, share in fight)")
    for b in range(len(BINS) - 1):
        em = [x for x in emerge[b] if x is not None]
        em.sort()
        print(f"{BINS[b]:.2f}-{min(1, BINS[b + 1]):.2f}  {n[b]:6d}  {g[b] / max(1, n[b]):.3f}"
              f"   {em[len(em) // 2] if em else 0:.1f}  {len(em) / max(1, len(emerge[b])):.2f}")
    print("all", sum(n.values()), round(sum(g.values()) / max(1, sum(n.values())), 3))
    if "--write" in sys.argv:
        mids = [(BINS[b] + min(1.0, BINS[b + 1])) / 2 for b in range(len(BINS) - 1)]
        nw = median_nw(mids)
        out = {"source": f"{sum(n.values())} Mo & Krill fights in Phantom+ replays (scripts/mechanics/krill_burrow.py)",
               "note": "share of fights Mo opens underground (PRE s before the first hit to POST s after), by match "
                       "fraction bin at Mo's median net worth there (Mechanics.burrow_prefight)",
               "heroes": {str(MO): {"name": "Mo & Krill", "fights": sum(n.values()),
                                    "points": [[nw[mids[b]], round(g[b] / max(1, n[b]), 3)] for b in range(len(mids))]}}}
        json.dump(out, open(os.path.join(HERE, "..", "..", "data", "burrow_prefight.json"), "w"), indent=1)
        print("wrote data/burrow_prefight.json")


if __name__ == "__main__":
    main()
