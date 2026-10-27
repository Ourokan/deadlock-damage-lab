"""How an area ability's hits on heroes other than the fight's main target grow with the game phase, from Phantom+
replay damage events (data/ability_area_phase.json, Mechanics.ability_area_phase).

A duel has one target, so an ability's landing factor (landing_rates_mech.json) absorbs its pooled hits on the other
enemies of a real fight: Nurse's Lurking Terrors hits 2.3 heroes per cast in fights before 45% of the match, 3.1
after 75% (team fights), and its real share of her damage goes 0.15 / 0.36 / 0.45 at 30 / 60 / 90% of the match
while the sim's stayed 0.28 / 0.35 / 0.35. Area items already have a phase curve (area_hits.py,
mechanics.area_extra); abilities had none.

Fights as area_hits.py: a run of one attacker's hero damage with gaps under GAP_S, main target = the hero who took
the most of the attacker's gun damage. Per hero ability and attacker net worth bin (the attacker's own net worth at
the fight's start, from the sample's stats snapshots, the duel's souls): main = damage on the main target, other =
on every other hero. Gun damage is the baseline (target switches inside a fight): extra(bin) = other / main -
gun other / main in that bin. The gun switches to more heroes late too (other / main 0.21 in lane, 0.40 late) and
the sim's gun has no phase term (its calibration counts hits on every hero), so what moves an ability against the
gun is rel(bin) = (1 + other / main) / (1 + gun other / main). One ability's bins are few fights, so the curve is
shrunk to the ability's pooled rel with SHRINK fights of weight (n / (n + SHRINK)) and made non-decreasing (pool
adjacent violators).

The sim multiplies the ability's damage at net worth nw by rel(nw) / pooled rel (the fitted curve's mean weighted
by main-target damage, so the real fights' mean multiplier is 1), linear in
ln net worth between bin means, flat outside: the pooled level stays where the landing factor put it, only the phase
shape moves. Rows only for HEROES (split-half) and abilities with MIN_EXTRA pooled extra hits over the gun's and MIN_FIGHTS fights.

usage: python3 -I ability_area_phase.py [--raw DIR] [--all] [--write]   (--all: every hero's rows, to judge more heroes)
"""
import bisect
import collections
import gzip
import json
import math
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT)
RAW = "/mnt/project-files/analysis/work/fight_length/raw/"
SAMPLE = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
OUT = os.path.join(ROOT, "data", "ability_area_phase.json")
T = 64
GAP_S = 8
NW_EDGES = [8000, 14000, 20000, 27000, 35000]
MIN_FIGHTS = 150
MIN_EXTRA = 0.15
SHRINK = 60
# heroes it is on for (2026-10-27 split-half: level corrections refit on one half of the audit sample with and without
# the phase term, per-phase source distance at 30 / 60 / 90% of the match on the other half lower both ways and mix
# distance not worse by more than 0.002). Haze, Infernus and Deadman Danny got clearly worse (their sim ability share
# already followed the real one by phase: something else in their model leans the other way), the rest flat.
HEROES = ["Baba", "Bebop", "Dynamo", "Grey Talon", "Kelvin", "Mina", "Mo & Krill", "Nurse Harrow", "Paige", "Paradox",
          "Pocket", "Rat King", "Violet", "Viscous"]


def nw_at(curve, t):
    xs = [x for x, _ in curve]
    i = bisect.bisect_left(xs, t)
    if i == 0:
        return curve[0][1] * max(0.0, t) / max(1, curve[0][0])
    if i >= len(curve):
        return curve[-1][1]
    (t0, a), (t1, b) = curve[i - 1], curve[i]
    return a + (b - a) * (t - t0) / max(1, t1 - t0)


def fights(args):
    """[(hero id, source id, attacker net worth, main dmg, other dmg)] per fight and source (source -1 = gun)."""
    fn, m, weap, abil = args
    hero, ev, last = {}, collections.defaultdict(list), 0
    for line in gzip.open(fn, "rt"):
        r = json.loads(line)
        last = max(last, r["tick"])
        if r["k"] == "ctl":
            hero[r["a"]] = int(r["s"])
        elif r["k"] == "dmg" and r.get("s"):
            ev[r["a"] // 100000].append((r["tick"], r["a"] % 100000, int(r["s"].split("|")[0]), r["v"]))
    by_hero = {p["hero_id"]: p for p in m["players"]}
    off = max(0.0, last / T - m["duration_s"])
    out = []
    for pawn, es in ev.items():
        p = by_hero.get(hero.get(pawn))
        if p is None:
            continue
        team = {pw for pw, h in hero.items() if h in by_hero and by_hero[h]["team"] == p["team"]}
        es = [e for e in es if e[1] not in team]
        curve = [(s["time_stamp_s"], s["net_worth"]) for s in p["stats"]]
        es.sort()
        runs, lt = [], -1e18
        for e in es:
            if e[0] - lt > GAP_S * T:
                runs.append([])
            lt = e[0]
            runs[-1].append(e)
        mine = abil.get(p["hero_id"], {})
        for f in runs:
            gun = collections.Counter()
            for _, v, s, d in f:
                if s in weap:
                    gun[v] += d
            if not gun:
                continue
            main = gun.most_common(1)[0][0]
            nw = nw_at(curve, f[0][0] / T - off)
            acc = collections.defaultdict(lambda: [0.0, 0.0])
            for _, v, s, d in f:
                k = -1 if s in weap else s if s in mine else None
                if k is not None:
                    acc[k][0 if v == main else 1] += d
            out += [(p["hero_id"], k, nw, a, b) for k, (a, b) in acc.items()]
    return out


def isotonic(vals, w):
    blocks = [[v, x, 1] for v, x in zip(vals, w)]
    i = 0
    while i < len(blocks) - 1:
        if blocks[i][0] > blocks[i + 1][0]:
            (a, wa, na), (b, wb, nb) = blocks[i], blocks.pop(i + 1)
            blocks[i] = [(a * wa + b * wb) / max(1e-9, wa + wb), wa + wb, na + nb]
            i = max(0, i - 1)
        else:
            i += 1
    return [v for v, _, n in blocks for _ in range(n)]


def main():
    from multiprocessing import Pool
    from deadsim import game
    G = game()
    args = sys.argv[1:]
    raw = args[args.index("--raw") + 1] if "--raw" in args else RAW
    weap = {w["id"] for w in json.load(open(os.path.join(ROOT, "..", "data", "game", "weapons.json")))}
    abil = {h.id: {ab.id: ab for ab in h.abilities} for h in G.heroes.values()}
    files = {f.split(".")[0]: os.path.join(raw, f) for f in os.listdir(raw) if f.endswith(".ndjson.gz")}
    jobs = []
    for line in gzip.open(SAMPLE, "rt"):
        m = json.loads(line)
        if str(m["match_id"]) in files:
            jobs.append((files[str(m["match_id"])], m, weap, {k: set(v) for k, v in abil.items()}))
    rows = []
    with Pool(4) as pl:
        for r in pl.imap_unordered(fights, jobs):
            rows += r
    edges = [0] + NW_EDGES + [math.inf]
    nb = len(edges) - 1
    acc = collections.defaultdict(lambda: [[0.0, 0.0, 0, 0.0] for _ in range(nb)])   # main, other, fights, sum ln nw*dmg
    for hid, k, nw, a, b in rows:
        x = acc[(hid, k)][bisect.bisect_right(edges, nw) - 1]
        x[0] += a
        x[1] += b
        x[2] += 1
        x[3] += math.log(max(nw, 1.0)) * (a + b)
    gun = [[0.0, 0.0] for _ in range(nb)]
    for (hid, k), bs in acc.items():
        if k == -1:
            for i, x in enumerate(bs):
                gun[i][0] += x[0]
                gun[i][1] += x[1]
    base = [o / max(1.0, m_) for m_, o in gun]
    base_all = sum(o for _, o in gun) / sum(m_ for m_, _ in gun)
    print(f"{len(jobs)} replays; gun other/main by bin", [round(b, 2) for b in base], "pooled", round(base_all, 2))
    res = {"source": f"{len(jobs)} Phantom+ replays, hero-vs-hero DamageEvent (scripts/team/ability_area_phase.py)",
           "note": "ability damage x rel(nw) / pooled at the duel's net worth nw, linear in ln nw "
                   "between bin means, flat outside (Mechanics.ability_area_phase)",
           "gun_other_per_main": [round(b, 3) for b in base], "abilities": {}}
    for (hid, k), bs in sorted(acc.items()):
        if k == -1:
            continue
        ab = abil[hid][k]
        M, O, N = sum(x[0] for x in bs), sum(x[1] for x in bs), sum(x[2] for x in bs)
        if N < MIN_FIGHTS or M <= 0:
            continue
        # hits per main hit relative to the gun's (which also switches to more heroes late): r = (1 + o/m) / (1 + b)
        rb = [(1.0 + x[1] / x[0]) / (1.0 + base[i]) if x[0] > 0 else None for i, x in enumerate(bs)]
        pooled = sum(r * x[0] for r, x in zip(rb, bs) if r is not None) / M
        if (1.0 + O / M) / (1.0 + base_all) - 1.0 < MIN_EXTRA:
            continue
        ex, w, nws = [], [], []
        for i, x in enumerate(bs):
            if x[0] <= 0:
                continue
            s = x[2] / (x[2] + SHRINK)
            ex.append(s * rb[i] + (1 - s) * pooled)
            w.append(x[0])
            nws.append(math.exp(x[3] / max(1e-9, x[0] + x[1])))
        fit = isotonic(ex, w)
        pooled = sum(f * x for f, x in zip(fit, w)) / sum(w)   # the fitted curve's main-damage-weighted mean
        name = f"{G.heroes[hid].name}: {ab.name}"
        if G.heroes[hid].name not in HEROES and "--all" not in args:
            continue
        res["abilities"][ab.class_name] = {
            "name": name, "fights": N, "pooled": round(pooled, 4),
            "bins": [{"net_worth": round(n), "rel": round(f, 4), "observed": round(e, 4)} for n, f, e in zip(nws, fit, ex)]}
        print(f"  {name[:40]:40s} n {N:5d} pooled {pooled:.2f}  " +
              "  ".join(f"{n / 1000:.0f}k {f / pooled:.2f}" for n, f in zip(nws, fit)))
    if "--write" in args:
        with open(OUT, "w") as fh:
            json.dump(res, fh, indent=1)
            fh.write("\n")


if __name__ == "__main__":
    main()
