"""Do ability range items (Mystic Expansion, Greater Expansion) make real abilities hit more heroes, or the same heroes
more often, per cast? The sim gives range only a shorter walk-in (engine reach, CastCtx.within), so if they did the
sim would under-value them.

casts_by_build.py had range item holders' damage per cast 1.18x non-holders' in real vs 1.07x in the sim (same hero
ability and net-worth bin). Holders also have ~1.66x the spirit item souls, so two checks:

- area: Phantom+ replay fights as ability_area_phase.py (runs of one attacker's hero damage, main target = most gun
  damage), each fight tagged with the attacker's build at its minute. Per hero ability and net-worth bin, hits on
  heroes other than the main target per main-target damage relative to the gun's in the same fights
  ((1 + other / main) / (1 + gun other / main)), holders over non-holders of neither item, geometric mean weighted by
  the smaller side's fights; "area" = abilities whose pooled extra over the gun is at least ability_area_phase.MIN_EXTRA.
  A bigger radius catching more heroes would lift area abilities above single-target ones.
- casts: casts_by_build.py's real and sim rows (run its real and sim steps first, same CASTS_WORK), holders of the
  item vs non-holders of either range item whose spirit item souls are at least MATCH x the holders' median (so the
  spirit investment matches), damage and hits per cast, real and sim.

usage: python3 -I range_hits.py area [--half 0|1]
       python3 -I range_hits.py casts [--half 0|1]
Results: validation/README.md "Range items and hits per cast".
"""
import bisect
import collections
import gzip
import json
import math
import os
import pickle
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "fight_length"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "cast_timing"))
sys.path.insert(0, HERE)
import ability_area_phase as AP  # noqa: E402
import fit_length as FL  # noqa: E402

RANGE = ("Greater Expansion", "Mystic Expansion")
EDGES = [0] + AP.NW_EDGES + [math.inf]
MIN_ROW = 8      # fights of one side in a hero ability x bin cell
MIN_ABIL = 100   # fights of an ability in all
MATCH = 0.7      # casts: non-holders' spirit item souls at least this x the holders' median


def fights(args):
    """[(hero id, source id (-1 gun), net worth, main dmg, other dmg, holds GE, holds ME, match)] per fight and source."""
    import landing_rates as L
    from deadsim import game
    G = game()
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
    clock = FL.clock_offset(FL.read(fn)[1], hero, m)
    off = max(0.0, last / AP.T - m["duration_s"])
    out, held = [], {}
    for pawn, es in ev.items():
        p = by_hero.get(hero.get(pawn))
        if p is None:
            continue
        team = {pw for pw, h in hero.items() if h in by_hero and by_hero[h]["team"] == p["team"]}
        es = sorted(e for e in es if e[1] not in team)
        curve = [(s["time_stamp_s"], s["net_worth"]) for s in p["stats"]]
        runs, lt = [], -1e18
        for e in es:
            if e[0] - lt > AP.GAP_S * AP.T:
                runs.append([])
            lt = e[0]
            runs[-1].append(e)
        mine = abil.get(p["hero_id"], set())
        for f in runs:
            gun = collections.Counter()
            for _, v, s, d in f:
                if s in weap:
                    gun[v] += d
            if not gun:
                continue
            main = gun.most_common(1)[0][0]
            t = f[0][0] / AP.T - (clock(f[0][0] / AP.T) if clock else off)
            key = (p["slot"], int(max(0.0, t) // 60))
            if key not in held:
                names = {G.items[i].name for i in L.build_at(p, key[1] * 60.0)[0]}
                held[key] = tuple(n in names for n in RANGE)
            acc = collections.defaultdict(lambda: [0.0, 0.0])
            for _, v, s, d in f:
                k = -1 if s in weap else s if s in mine else None
                if k is not None:
                    acc[k][0 if v == main else 1] += d
            out += [(p["hero_id"], k, AP.nw_at(curve, t), a, b) + held[key] + (m["match_id"],) for k, (a, b) in acc.items()]
    return out


def area(half):
    from multiprocessing import Pool
    from deadsim import game
    G = game()
    weap = {w["id"] for w in json.load(open(os.path.join(ROOT, "..", "data", "game", "weapons.json")))}
    abil = {h.id: {ab.id for ab in h.abilities} for h in G.heroes.values()}
    files = {f.split(".")[0]: os.path.join(AP.RAW, f) for f in os.listdir(AP.RAW) if f.endswith(".ndjson.gz")}
    jobs = [(files[str(m["match_id"])], m, weap, abil) for m in map(json.loads, gzip.open(AP.SAMPLE, "rt"))
            if str(m["match_id"]) in files and (half is None or m["match_id"] % 2 == half)]
    rows = []
    with Pool(4) as pl:
        for r in pl.imap_unordered(fights, jobs):
            rows += r
    acc = collections.defaultdict(lambda: [0.0, 0.0, 0])   # (hero, source, bin, group) -> main, other, fights
    pool = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for hid, k, nw, a, b, ge, me, _ in rows:
        g = "Greater Expansion" if ge else "Mystic Expansion" if me else None
        for x in (acc[hid, k, bisect.bisect_right(EDGES, nw) - 1, g], pool[hid, k]):
            x[0] += a
            x[1] += b
            x[2] += 1
    gun = [sum(v[i] for (_, k), v in pool.items() if k == -1) for i in (0, 1)]
    base = gun[1] / gun[0]

    def rel(hid, k, b, g):
        x, y = acc.get((hid, k, b, g)), acc.get((hid, -1, b, g))
        if not x or not y or x[0] <= 0 or y[0] <= 0 or x[2] < MIN_ROW:
            return None
        return (1 + x[1] / x[0]) / (1 + y[1] / y[0])
    out = collections.defaultdict(lambda: [0.0, 0.0])
    for (hid, k), p in pool.items():
        if k == -1 or p[0] <= 0 or p[2] < MIN_ABIL:
            continue
        kind = "area" if (1 + p[1] / p[0]) / (1 + base) - 1 >= AP.MIN_EXTRA else "single"
        for b in range(len(EDGES) - 1):
            rn = rel(hid, k, b, None)
            for g in RANGE:
                rh = rel(hid, k, b, g)
                if rn is None or rh is None:
                    continue
                w = min(acc[hid, k, b, None][2], acc[hid, k, b, g][2])
                out[g, kind][0] += w * math.log(rh / rn)
                out[g, kind][1] += w
    print(f"{len(jobs)} replays: holders / non-holders, other heroes hit per main-target damage over the gun's")
    for (g, kind), (s, w) in sorted(out.items()):
        print(f"   {g:18s} {kind:6s} {math.exp(s / w):6.3f}  (weight {w:.0f})")


def casts(half):
    import casts_by_build as CB
    flag = {n: len(CB.GROUPS) + CB.ITEMS.index(n) for n in RANGE + ("Duration Extender",)}
    for src, fn in (("real", CB.REAL_OUT), ("sim", CB.SIM_OUT)):
        by = collections.defaultdict(list)
        for r in pickle.load(open(fn, "rb")):
            if half is None or int(r[10]) % 2 == half:
                by[r[0], r[1], int(r[8] // CB.NW_BIN)].append(r)
        for item, i in flag.items():
            acc = collections.defaultdict(lambda: [0.0, 0.0])
            for rs in by.values():
                hi = [r for r in rs if r[15][i]]
                lo = [r for r in rs if not any(r[15][j] for j in flag.values())]
                if len(hi) < 5:
                    continue
                med = statistics.median(r[7] for r in hi)
                lo = [r for r in lo if r[7] >= MATCH * med]
                if len(lo) < 5:
                    continue
                for name, num, den in (("dmg/cast", 14, 13), ("hits/cast", 12, 13)):
                    a = sum(r[num] for r in hi) / max(1e-9, sum(r[den] for r in hi))
                    b = sum(r[num] for r in lo) / max(1e-9, sum(r[den] for r in lo))
                    if a > 0 and b > 0:
                        w = min(len(hi), len(lo))
                        acc[name][0] += w * math.log(a / b)
                        acc[name][1] += w
                a, b = (sum(r[7] for r in x) / len(x) for x in (hi, lo))
                acc["spirit souls"][0] += min(len(hi), len(lo)) * math.log(max(1.0, a) / max(1.0, b))
                acc["spirit souls"][1] += min(len(hi), len(lo))
            print(f"{src:4s} {item:18s} holders / matched non-holders: "
                  + "  ".join(f"{k} {math.exp(s / w):.3f}" for k, (s, w) in acc.items() if w))


if __name__ == "__main__":
    a = sys.argv[1:]
    h = int(a[a.index("--half") + 1]) if "--half" in a else None
    {"area": area, "casts": casts}[a[0]](h)
