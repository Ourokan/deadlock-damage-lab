"""Does spirit power reach abilities and items in Phantom+ replays the way their tooltip formulas say? (validation/
README.md "Spirit power reaching abilities and items").

Every hero-on-hero damage event of a spirit-scaled ability or item, its attacker's spirit power at that moment
(compute_stats on the real build + permanent spirit pickups, which validate_stats.py shows matches the in-game
snapshots) and ability tier (sample ability events), divided by the victim's spirit resist (its build + pickups):
the real per-hit damage over the formula Base(tier) + scale(tier) x spirit power, using for each source the
spirit-scaled property whose ratio varies least (DoT props are per tick, so only the ratio's change matters).

Prints, within source x net-worth bin (6k), the per-hit real/formula of fighters above vs at or below the median
spirit item souls (abilities, items; without and with spirit-amp holders; even / odd match ids), the same as a
slope against the formula's spirit share, per-item fitted base and spirit slope next to the formula's, and the enemy
heroes each ability hit cluster (1.5 s) reaches by spirit item souls and by range items.

usage: python3 spirit_reach.py [fight_length raw dir]   (default: project folder analysis/work/fight_length/raw)
"""
import collections
import glob
import gzip
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import landing_rates as L  # noqa: E402
from deadsim.build import combine_resist, compute_stats  # noqa: E402
from deadsim.data import game  # noqa: E402

T = 64.0
SAMPLE = os.path.join(HERE, "..", "..", "validation", "phantom_sample.jsonl.gz")
G = game()
AB = {a.id: a for h in G.heroes.values() for a in h.abilities}
AMP = ("Spirit Strike", "Mystic Vulnerability", "Spirit Snatch", "Escalating Exposure", "Spirit Shredder", "Spirit Rend")
RANGE = ("Mystic Expansion", "Greater Expansion", "Knockdown", "Spirit Burn", "Vortex Web", "Mystic Conduit")


def pickups(p, t, prefix):
    return sum(v for b in p["power_ups"] if (b["type"] or "").startswith(prefix)
               for v, tt in zip(b["values"] or [], b["times"] or []) if tt <= t)


def tiers(p, t):
    ids = [ab.id for ab in G.hero(p["hero_id"]).abilities]
    tr, un = [0] * len(ids), [False] * len(ids)
    for i, bt, _, _ in sorted(p["items"], key=lambda x: x[1]):
        if i in ids and bt <= t:
            k = ids.index(i)
            if un[k]:
                tr[k] = min(3, tr[k] + 1)
            else:
                un[k] = True
    return tr


def read(raw):
    sample = {}
    for line in gzip.open(SAMPLE):
        m = json.loads(line)
        sample[str(m["match_id"])] = m
    cache, hits = {}, []

    def state(mid, p, t):
        key = (mid, p["slot"], int(t // 20))
        if key not in cache:
            items, nw = L.build_at(p, t)
            st = compute_stats(p["hero_id"], items, nw)
            cache[key] = dict(sp=st.spirit_power + pickups(p, t, "spirit_"), nw=nw, tiers=tiers(p, t), items=set(items),
                              res=combine_resist(st.spirit_resist + [pickups(p, t, "spiritresist_") / 100]),
                              ss=sum(G.items[i].cost for i in items if G.items[i].slot == "spirit"))
        return cache[key]

    for fn in sorted(glob.glob(os.path.join(raw, "*.ndjson.gz"))):
        mid = os.path.basename(fn).split(".")[0]
        m = sample.get(mid)
        if m is None:
            continue
        by_hero = {p["hero_id"]: p for p in m["players"]}
        rows = [json.loads(line) for line in gzip.open(fn, "rt")]
        hero = {r["a"]: int(r["s"]) for r in rows if r["k"] == "ctl"}   # ctl rows come after the damage rows
        for r in rows:
            if r["k"] != "dmg" or not r.get("s") or r["v"] <= 0:
                continue
            a, b = r["a"] // 100000, r["a"] % 100000
            pa, pb = by_hero.get(hero.get(a)), by_hero.get(hero.get(b))
            if pa is None or pb is None or pa["team"] == pb["team"]:
                continue
            src = int(r["s"].split("|")[0])
            if src not in AB and src not in G.items:
                continue
            t = r["tick"] / T
            sa = state(mid, pa, t)
            hits.append(dict(mid=int(mid), a=a, b=b, t=t, src=src, v=r["v"] / max(0.05, 1 - state(mid, pb, t)["res"]),
                             **{k: sa[k] for k in ("sp", "nw", "ss", "tiers", "items")}))
    return hits


def spirit_props(obj):
    return [(p, sc[2]) for p, sc in obj.scale.items()
            if (sc[0] == "scale_function_tech_damage" or sc[1] == "ETechPower") and sc[2] and obj.props.get(p)]


def formula(obj, prop, k, tier, sp):
    b = obj.props.get(prop, 0.0)
    if obj.id in AB:
        for i in range(tier):
            b += obj.upgrades[i].get(prop, 0.0) if i < len(obj.upgrades) else 0.0
            for typ, _, bonus in (obj.scale_upgrades[i].get(prop, []) if i < len(obj.scale_upgrades) else []):
                if typ == "EAddToScale":
                    k += bonus
    return b + k * sp


def tier_of(obj, h):
    return h["tiers"][[a.id for a in G.heroes[obj.hero_id].abilities].index(obj.id)] if obj.id in AB else 0


def per_hit(hits):
    """Per source: the best-fitting spirit-scaled prop; keeps sources whose median real/formula is 0.7-1.5 (the prop is
    the hit) with 500+ hits. Returns {name: [(is_ability, amp holder, spirit share, log ratio, nw, ss, mid, sp, v)]}."""
    amp = {G.item(n).id for n in AMP}
    by = collections.defaultdict(list)
    for h in hits:
        by[h["src"]].append(h)
    out = {}
    for src, hs in by.items():
        obj = AB.get(src) or G.items[src]
        if len(hs) < 500:
            continue
        best = None
        for prop, k in spirit_props(obj):
            lr = [math.log(h["v"] / f) for h in hs for f in [formula(obj, prop, k, tier_of(obj, h), h["sp"])] if f > 0]
            if len(lr) >= 100:
                mu = sum(lr) / len(lr)
                sd = (sum((x - mu) ** 2 for x in lr) / len(lr)) ** 0.5
                if best is None or sd < best[0]:
                    best = (sd, prop, k, math.exp(sorted(lr)[len(lr) // 2]))
        if best is None or not 0.7 <= best[3] <= 1.5:
            continue
        _, prop, k, _ = best
        pts = []
        for h in hs:
            f = formula(obj, prop, k, tier_of(obj, h), h["sp"])
            if f > 0:
                pts.append((src in AB, bool(amp & h["items"]), k * h["sp"] / f, math.log(h["v"] / f), h["nw"], h["ss"],
                            h["mid"], h["sp"], h["v"]))
        out[obj.name] = (prop, k, pts)
    return out


def hi_lo(srcs, sel):
    """exp(mean log ratio of fighters above the median spirit item souls - at or below), within source x nw bin."""
    num = den = 0.0
    for name, (_, _, pts) in srcs.items():
        g = collections.defaultdict(list)
        for p in pts:
            if sel(p):
                g[min(p[4] // 6000, 7)].append(p)
        for ps in g.values():
            if len(ps) < 40:
                continue
            med = sorted(p[5] for p in ps)[len(ps) // 2]
            hi, lo = [p[3] for p in ps if p[5] > med], [p[3] for p in ps if p[5] <= med]
            if len(hi) >= 10 and len(lo) >= 10:
                w = min(len(hi), len(lo))
                num += w * (sum(hi) / len(hi) - sum(lo) / len(lo))
                den += w
    return math.exp(num / max(den, 1e-9))


def slope(groups, xi, yi):
    sxx = sxy = 0.0
    for ps in groups:
        if len(ps) < 20:
            continue
        mx, my = sum(p[xi] for p in ps) / len(ps), sum(p[yi] for p in ps) / len(ps)
        sxx += sum((p[xi] - mx) ** 2 for p in ps)
        sxy += sum((p[xi] - mx) * (p[yi] - my) for p in ps)
    return sxy / max(sxx, 1e-9)


def area(hits):
    """Enemy heroes per ability hit cluster (same attacker and ability, 1.5 s from its first hit)."""
    rng = {G.item(n).id for n in RANGE}
    ev = collections.defaultdict(list)
    for h in hits:
        if h["src"] in AB:
            ev[(h["mid"], h["a"], h["src"])].append(h)
    cl = collections.defaultdict(list)
    for (mid, _, src), hs in ev.items():
        hs.sort(key=lambda h: h["t"])
        i = 0
        while i < len(hs):
            j, vs = i, set()
            while j < len(hs) and hs[j]["t"] < hs[i]["t"] + 1.5:
                vs.add(hs[j]["b"])
                j += 1
            cl[(src, min(hs[i]["nw"] // 6000, 7))].append((hs[i]["ss"] / 10000, float(bool(hs[i]["items"] & rng)),
                                                          len(vs), mid % 2))
            i = j
    return cl


def main():
    raw = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project-files/analysis/work/fight_length/raw"
    hits = read(raw)
    srcs = per_hit(hits)
    print(f"{len(hits)} hits, {len(srcs)} sources with a fitting spirit-scaled prop")
    print("\nper-hit real/formula, fighters above / at or below the median spirit item souls (same source, nw bin);"
          " slope = log ratio per unit spirit share of the formula")
    for lab, s in [("abilities", lambda p: p[0]), ("abilities, no spirit-amp items", lambda p: p[0] and not p[1]),
                   ("abilities, even ids", lambda p: p[0] and p[6] % 2 == 0),
                   ("abilities, odd ids", lambda p: p[0] and p[6] % 2 == 1),
                   ("items", lambda p: not p[0]), ("items, no spirit-amp items", lambda p: not p[0] and not p[1])]:
        sl = slope([[p for p in pts if s(p)] for _, _, pts in srcs.values()], 2, 3)
        print(f"  {lab:32s} hi/lo {hi_lo(srcs, s):.3f}   slope {sl:+.3f}")
    print("\nitems (no spirit-amp holders): formula base, scale | real fit base, per spirit power | even / odd")
    for name, (prop, k, pts) in sorted(srcs.items(), key=lambda x: -len(x[1][2])):
        ps = [p for p in pts if not p[0] and not p[1]]
        if len(ps) < 200:
            continue

        def fit(q):
            n = len(q)
            mx, my = sum(p[7] for p in q) / n, sum(p[8] for p in q) / n
            b = sum((p[7] - mx) * (p[8] - my) for p in q) / max(1e-9, sum((p[7] - mx) ** 2 for p in q))
            return my - b * mx, b
        a, b = fit(ps)
        e, o = fit([p for p in ps if p[6] % 2 == 0]), fit([p for p in ps if p[6] % 2 == 1])
        print(f"  {name:20s} {len(ps):6d}  {G.item(name).p(prop):6.1f} {k:5.3f} | {a:6.1f} {b:6.3f} | {e[1]:6.3f} {o[1]:6.3f}")
    cl = area(hits)
    n = sum(len(v) for v in cl.values())
    mean = sum(c[2] for v in cl.values() for c in v) / n
    print(f"\nability hit clusters {n}, enemy heroes per cluster {mean:.3f}; within ability x nw bin:")
    print(f"  per 10k spirit item souls {slope(cl.values(), 0, 2):+.4f} (even {slope([[c for c in v if c[3] == 0] for v in cl.values()], 0, 2):+.4f},"
          f" odd {slope([[c for c in v if c[3] == 1] for v in cl.values()], 0, 2):+.4f});"
          f" holding a range item {slope(cl.values(), 1, 2):+.4f}")


if __name__ == "__main__":
    main()
