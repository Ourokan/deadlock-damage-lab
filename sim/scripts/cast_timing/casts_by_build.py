"""Ability casts per fight by build: do real players with more souls in spirit items cast their abilities more often in
a fight, use more of their cooldowns, or land more of their casts, than the sim's duels of the same builds?

The damage audit had abilities ~4% under and items ~8% over on spirit builds (same hero, same fifth of the match);
per-hit damage over the tooltip formula and heroes hit per cast match real (spirit_reach.py), and the casts' timing
(ability_lean.py) explains about a quarter. This counts the casts.

real: the fight-length replays' pair fights (recast_timing.pair_spans), each fighter's abilities it has cast before or
in the fight (unlocked): casts from PRE_S before the first hit to the last hit, landed casts (a hit of that ability on an
enemy hero within LAG_MAX s and before its next cast), the fight's length, the ability's cooldown in the player's real
build at that minute (recast_timing.cooldowns; charged abilities and ults have none) and the build (spirit item souls,
net worth, cooldown reduction: fit_cast_timing.build_cols).
sim: the damage audit's duels (real builds both sides, the model as the searches fight), each cast of the audited
fighter's abilities weighted by P(a real fight still goes on then) (Engine.length_w), so a duel's count is the expected
casts over real fight lengths; its expected length is the same weight integrated over the duel.

Compare: within hero ability x net-worth bin (NW_BIN souls), builds split at the bin's median spirit item souls; the
hi / lo ratio of casts per fight, fight length, casts per fight second, cooldown use (casts / (1 + length / cooldown),
plain abilities) and landed share (real only: the sim books landing as a damage factor), pooled over bins weighted by
the smaller half's fights. A ratio real / sim above 1 is spirit builds casting more in real than in the sim.

usage: python3 -I casts_by_build.py real [--half 0|1] [--workers 4]   -> scratch pickle (REAL_OUT)
       python3 -I casts_by_build.py sim [n=1500] [--workers 4] [--on MECH_FIELD]...  -> scratch pickle (SIM_OUT)
       python3 -I casts_by_build.py mix [--workers 4]   -> real damage by kind inside / outside pair fights (compare reads it)
       python3 -I casts_by_build.py compare [--half 0|1]
       python3 -I casts_by_build.py imbues [ITEM] [--half 0|1]   (default Duration Extender)
Results: validation/README.md "Ability casts per fight by build".
"""
import bisect
import collections
import dataclasses
import gzip
import json
import math
import os
import pickle
import random
import statistics
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "fight_length"))
sys.path.insert(0, HERE)
import fit_cast_timing as CT  # noqa: E402
import fit_length as FL  # noqa: E402
import opener_timing as OT  # noqa: E402
import recast_timing as RT  # noqa: E402

WORK = os.environ.get("CASTS_WORK", "/tmp/casts_by_build")   # scratch pickles
REAL_OUT = os.path.join(WORK, "real.pkl")
SIM_OUT = os.path.join(WORK, "sim.pkl")
NW_BIN = 8000
MIN_SIDE = 10   # fights on each side of a bin's split
LAG_MAX = CT.LAG_MAX
# item groups whose holders split the compare (flags in each row): ability duration, ability range / radius, spirit amp
GROUPS = {"duration": ("Arcane Surge", "Duration Extender", "Superior Duration", "Magic Carpet", "Diviner's Kevlar",
                       "Spiritual Overflow"),
          "range": ("Mystic Expansion", "Greater Expansion", "Knockdown", "Spirit Burn", "Vortex Web", "Mystic Conduit"),
          "amp": ("Spirit Strike", "Mystic Vulnerability", "Spirit Snatch", "Escalating Exposure", "Spirit Shredder",
                  "Spirit Rend")}


ITEMS = [n for g in GROUPS.values() for n in g]


def flags(names):
    """(holds any item of each group, ...) + (holds each item of ITEMS, ...)."""
    return tuple(any(n in names for n in g) for g in GROUPS.values()) + tuple(n in names for n in ITEMS)


def real_rows(args):
    """[(hero id, ability class, ult, casts, landed, fight s, cooldown s or None, spirit souls, net worth, cdr, match)]."""
    fn, cast_fn, m, abil = args
    hero, ev = OT.read(fn)
    by_hero = {p["hero_id"]: p for p in m["players"]}
    rows = CT.real_casts([json.loads(line) for line in gzip.open(cast_fn, "rt")])
    off = statistics.median(r["tick"] / CT.T - r["v"] for r in rows) if rows else 0.0
    casts = collections.defaultdict(list)
    for r in rows:
        casts[(r["a"], int(r["s"]))].append(r["tick"] / CT.T)
    for v in casts.values():
        v.sort()
    hits, dmg = collections.defaultdict(list), collections.defaultdict(list)
    for e in ev:
        pa, pv = by_hero.get(hero.get(e[1])), by_hero.get(hero.get(e[2]))
        if pa is not None and pv is not None and pa["team"] != pv["team"]:
            hits[e[1], e[6]].append(e[0])
            dmg[e[1], e[6]].append((e[0], e[5]))
    out, cache, bcache, fcache = [], {}, {}, {}
    for pawn, sp in RT.pair_spans(hero, ev, by_hero).items():
        hid = hero.get(pawn)
        if hid not in abil or hid not in by_hero:
            continue
        p = by_hero[hid]
        for t0, t1 in sorted(sp):
            b = CT.build_cols(p, t0 - off, m, bcache)
            cds = RT.cooldowns(p, t0 - off, cache)
            fk = (p["slot"], int((t0 - off) // 60))
            if fk not in fcache:
                import landing_rates as L
                from deadsim import game
                fcache[fk] = flags({game().items[i].name for i in L.build_at(p, max(0.0, fk[1] * 60.0))[0]})
            for aid, (cls, ult) in abil[hid].items():
                cs = casts.get((pawn, aid), [])
                k0 = bisect.bisect_left(cs, t0 - CT.PRE_S)
                k1 = bisect.bisect_right(cs, t1)
                if k1 == 0:
                    continue   # never cast by the fight's end: not unlocked (or never used) yet
                hs = hits.get((pawn, aid), [])
                hd = dmg.get((pawn, aid), [])
                i0, i1 = bisect.bisect_left(hd, (t0 - CT.PRE_S,)), bisect.bisect_right(hd, (t1 + LAG_MAX, 1e18))
                d, nh = sum(x for _, x in hd[i0:i1]), i1 - i0
                landed = 0
                for k in range(k0, k1):
                    c = cs[k]
                    end = min(c + LAG_MAX, cs[k + 1] if k + 1 < len(cs) else 1e9)
                    j = bisect.bisect_left(hs, c)
                    landed += j < len(hs) and hs[j] <= end
                out.append((hid, cls, ult, k1 - k0, landed, t1 - t0, cds.get(cls)) + b + (d, nh, k1 - k0, d, fcache[fk]))
    return out


def real(half, workers):
    from deadsim import game
    G = game()
    abil = {h.id: {ab.id: (ab.class_name, bool(ab.ultimate)) for ab in h.abilities} for h in G.heroes.values()}
    mids = {f.split(".")[0] for f in os.listdir(CT.CASTS) if f.endswith(".ndjson.gz")}
    mids &= {f.split(".")[0] for f in os.listdir(CT.FIGHTS) if f.endswith(".ndjson.gz")}
    if half is not None:
        mids = {x for x in mids if int(x) % 2 == half}
    sample = FL.load_sample(CT.SAMPLE, mids)
    jobs = [(os.path.join(CT.FIGHTS, f"{mid}.ndjson.gz"), os.path.join(CT.CASTS, f"{mid}.ndjson.gz"), sample[mid], abil)
            for mid in sorted(mids) if mid in sample]
    rows = []
    with Pool(workers) as p:
        for rs in p.imap_unordered(real_rows, jobs):
            rows += rs
    os.makedirs(WORK, exist_ok=True)
    pickle.dump(rows, open(REAL_OUT, "wb"))
    print(len(rows), "rows from", len(jobs), "matches ->", REAL_OUT)


_REC = None


def _sim_job(job):
    """The audit duels of one player: [(hero id, cls, ult, exp casts, 0, exp length, cooldown, spirit, nw, cdr, mid)]."""
    global _REC
    import damage_audit as A
    from deadsim import abilities, engine, game
    from deadsim.build import compute_stats
    G = game()
    if _REC is None:
        _REC = {"casts": collections.defaultdict(list), "eng": {}, "mix": {}, "hits": {}, "cur": None}
        cast0, run0, duel0 = abilities.AbilityState.cast, engine.Engine.run, A.duel
        book0 = engine.Engine.booking

        def booking(src, dst, amt, kind, name, pure):
            if src.name.endswith("(A)") and amt > 0:
                v = _REC["hits"].setdefault(id(src.e), collections.defaultdict(lambda: [0, 0.0]))[name]
                v[0] += 1
                v[1] += amt
            return book0(src, dst, amt, kind, name, pure)
        engine.Engine.booking = staticmethod(booking)

        def cast(self):
            if self.f.name.endswith("(A)") and not self.scratch.get("prefight"):
                cd = None if self.ab.ultimate or self.max_charges() > 1 else self.cooldown()
                _REC["casts"][id(self.f.e)].append((self.ab.class_name, self.f.e.length_w(), cd))
            return cast0(self)

        def run(self, *a, **k):
            # expected fight length: integral of length_w over the duel (0.25 s steps), recorded after the run
            f = a[0]
            live = {s.ab.class_name: None if s.ab.ultimate or s.max_charges() > 1 else s.cooldown()
                    for s in f.abilities if s.unlocked and s.impl.kind != "passive"}
            r = run0(self, *a, **k)
            _REC["mix"][id(self)] = dict(f.dmg_exp)
            _REC["eng"][id(self)] = (sum(self.length_w(0.25 * (i + 0.5)) for i in range(int(self.t / 0.25) + 1)) * 0.25,
                                     _REC["cur"], live)
            return r

        def duel(a, b, *x, **k):
            hero, items = a.resolve()
            st = compute_stats(hero, items, a.souls, a.level)
            _REC["cur"] = (sum(i.cost for i in items if i.slot == "spirit"), a.souls, st.cdr,
                           {ab.class_name: bool(ab.ultimate) for ab in hero.abilities}, flags({i.name for i in items}))
            return duel0(a, b, *x, **k)
        abilities.AbilityState.cast, engine.Engine.run, A.duel = cast, run, duel
    _REC["casts"].clear()
    _REC["eng"].clear()
    _REC["mix"].clear()
    _REC["hits"].clear()
    m, slot = job
    hid, _, _ = A.sim_player(job)
    import landing_rates as L
    h = G.hero(hid)
    names = {ab.name: ab.class_name for ab in h.abilities}
    acls = set(names.values())
    icls = {it.class_name for it in G.items.values()}
    out, mix, dcls = [], [], {}
    for eid, d in _REC["mix"].items():
        cur = _REC["eng"][eid][1]
        if cur is None:
            continue
        v = [0.0, 0.0, 0.0]
        for src, x in d.items():
            c = L.sim_key(src, names, G)
            dcls.setdefault(eid, collections.Counter())[c] += x
            v[0 if c in acls else 1 if c in icls else 2] += x
        mix.append((hid, cur[1], cur[0], m["match_id"], v, [0.0, 0.0, 0.0]))
    for eid, (length, cur, live) in _REC["eng"].items():
        if cur is None:
            continue
        ss, nw, cdr, abil, fl = cur
        by = collections.defaultdict(list)
        for cls, w, cd in _REC["casts"].get(eid, []):
            by[cls].append((w, cd))
        hraw = collections.defaultdict(lambda: [0, 0.0])
        for src, (nh, amt) in _REC["hits"].get(eid, {}).items():
            c = L.sim_key(src, names, G)
            hraw[c][0] += nh
            hraw[c][1] += amt
        for cls, ult in abil.items():
            if cls not in live:
                continue   # locked (the real side counts abilities cast by the fight's end)
            cs = by.get(cls, [])
            out.append((hid, cls, ult, sum(w for w, _ in cs), 0, length, live[cls],
                        ss, nw, cdr, m["match_id"], dcls.get(eid, {}).get(cls, 0.0),
                        hraw[cls][0], len(cs), hraw[cls][1], fl))
    return out, mix


def sim(n, workers, on=()):
    import damage_audit as A
    import landing_rates as L
    from deadsim import game
    if on:
        A.MECH = dataclasses.replace(A.MECH, **{k: (float(v) if v.replace(".", "").isdigit() else v == "1") if "=" in kv
                                                 else True for kv in on for k, v in [(kv.split("=") + ["1"])[:2]]})
    G = game()
    jobs = []
    for line in gzip.open(CT.SAMPLE):
        m = json.loads(line)
        jobs += [(m, p["slot"]) for p in m["players"] if p["hero_id"] in G.heroes and L.gun_known(p)]
    random.Random(1).shuffle(jobs)
    rows, mix = [], []
    with Pool(workers) as p:
        for rs, mx in p.imap_unordered(_sim_job, jobs[:n], chunksize=8):
            rows += rs
            mix += mx
    os.makedirs(WORK, exist_ok=True)
    pickle.dump(rows, open(SIM_OUT, "wb"))
    pickle.dump(mix, open(SIM_OUT.replace(".pkl", "_mix.pkl"), "wb"))
    print(len(rows), "rows from", n, "players ->", SIM_OUT)


def ratios(rows, key=lambda r: True):
    """Pooled hi / lo ratios within hero ability x net-worth bin, split at the bin's median spirit souls."""
    by = collections.defaultdict(list)
    for r in rows:
        if key(r):
            by[r[0], r[1], int(r[8] // NW_BIN)].append(r)
    acc = collections.defaultdict(lambda: [0.0, 0.0])
    for rs in by.values():
        med = statistics.median(r[7] for r in rs)
        hi, lo = [r for r in rs if r[7] > med], [r for r in rs if r[7] <= med]
        if len(hi) < MIN_SIDE or len(lo) < MIN_SIDE:
            continue
        w = min(len(hi), len(lo))

        def mean(rs, f):
            v = [f(r) for r in rs]
            v = [x for x in v if x is not None]
            return sum(v) / len(v) if v else None
        stats = {
            "casts/fight": lambda r: r[3],
            "length": lambda r: r[5],
            "casts/s": None,
            "cd use": lambda r: r[3] / (1 + r[5] / r[6]) if r[6] else None,
            "landed/cast": None,
            "dmg/fight": lambda r: r[11],
            "dmg/cast": None,
            "hits/cast": None,
            "dmg/hit": None,
            "spirit souls": lambda r: r[7],
        }
        for name, f in stats.items():
            if name == "casts/s":
                a = sum(r[3] for r in hi) / sum(r[5] for r in hi)
                b = sum(r[3] for r in lo) / sum(r[5] for r in lo)
            elif name == "hits/cast":
                a = sum(r[12] for r in hi) / max(1e-9, sum(r[13] for r in hi))
                b = sum(r[12] for r in lo) / max(1e-9, sum(r[13] for r in lo))
            elif name == "dmg/hit":
                a = sum(r[14] for r in hi) / max(1e-9, sum(r[12] for r in hi))
                b = sum(r[14] for r in lo) / max(1e-9, sum(r[12] for r in lo))
            elif name == "dmg/cast":
                a = sum(r[11] for r in hi) / max(1e-9, sum(r[3] for r in hi))
                b = sum(r[11] for r in lo) / max(1e-9, sum(r[3] for r in lo))
            elif name == "landed/cast":
                a = sum(r[4] for r in hi) / max(1e-9, sum(r[3] for r in hi))
                b = sum(r[4] for r in lo) / max(1e-9, sum(r[3] for r in lo))
            else:
                a, b = mean(hi, f), mean(lo, f)
            if a is None or b is None or (name != "spirit souls" and (a <= 0 or b <= 0)):
                continue
            acc[name][0] += w * (math.log(a / b) if name != "spirit souls" else a - b)
            acc[name][1] += w
    return {k: v[0] / v[1] if k == "spirit souls" else math.exp(v[0] / v[1]) for k, v in acc.items() if v[1]}


def mix_rows(args):
    """Real hero damage by kind inside / outside the attacker's pair fights, per player minute:
    [(hero id, net worth, spirit souls, match, [ability, item, other] inside, [same] outside)]."""
    fn, cast_fn, m, kinds = args
    hero, ev = OT.read(fn)
    by_hero = {p["hero_id"]: p for p in m["players"]}
    rows = CT.real_casts([json.loads(line) for line in gzip.open(cast_fn, "rt")])
    off = statistics.median(r["tick"] / CT.T - r["v"] for r in rows) if rows else 0.0
    spans = RT.pair_spans(hero, ev, by_hero)
    for v in spans.values():
        v.sort()
    acc = collections.defaultdict(lambda: [0.0] * 6)
    for e in ev:
        pa, pv = by_hero.get(hero.get(e[1])), by_hero.get(hero.get(e[2]))
        if pa is None or pv is None or pa["team"] == pv["team"]:
            continue
        sp = spans.get(e[1], [])
        j = bisect.bisect_right(sp, (e[0] + CT.PRE_S, 1e18)) - 1
        inside = any(t0 - CT.PRE_S <= e[0] <= t1 + LAG_MAX for t0, t1 in sp[max(0, j - 3):j + 1])
        k = {"ability": 0, "item": 1}.get(kinds.get(e[6]), 2)
        acc[pa["hero_id"], int((e[0] - off) // 60)][k + (0 if inside else 3)] += e[5]
    out, bcache = [], {}
    for (hid, mn), v in acc.items():
        ss, nw, _, mid = CT.build_cols(by_hero[hid], mn * 60.0, m, bcache)
        out.append((hid, nw, ss, mid, v[:3], v[3:]))
    return out


def mix_real(workers):
    from deadsim import game
    G = game()
    kinds = {k: v[0] for k, v in OT.sources(G).items()}
    mids = {f.split(".")[0] for f in os.listdir(CT.CASTS) if f.endswith(".ndjson.gz")}
    mids &= {f.split(".")[0] for f in os.listdir(CT.FIGHTS) if f.endswith(".ndjson.gz")}
    sample = FL.load_sample(CT.SAMPLE, mids)
    jobs = [(os.path.join(CT.FIGHTS, f"{mid}.ndjson.gz"), os.path.join(CT.CASTS, f"{mid}.ndjson.gz"), sample[mid], kinds)
            for mid in sorted(mids) if mid in sample]
    rows = []
    with Pool(workers) as p:
        for rs in p.imap_unordered(mix_rows, jobs):
            rows += rs
    os.makedirs(WORK, exist_ok=True)
    pickle.dump(rows, open(os.path.join(WORK, "mix_real.pkl"), "wb"))
    print(len(rows), "player minutes from", len(jobs), "matches")


def shares(rows, half=None):
    """hi / lo (spirit souls within hero x net-worth bin, damage-weighted) of each kind's share of damage."""
    by = collections.defaultdict(list)
    for r in rows:
        if half is None or int(r[3]) % 2 == half:
            by[r[0], int(r[1] // NW_BIN)].append(r)
    acc = collections.defaultdict(lambda: [0.0, 0.0])
    for rs in by.values():
        med = statistics.median(r[2] for r in rs)
        hi, lo = [r for r in rs if r[2] > med], [r for r in rs if r[2] <= med]
        if len(hi) < MIN_SIDE or len(lo) < MIN_SIDE:
            continue
        w = min(len(hi), len(lo))
        for name, f in (("ability in", lambda v: v[4][0]), ("item in", lambda v: v[4][1]), ("other in", lambda v: v[4][2]),
                        ("ability all", lambda v: v[4][0] + v[5][0]), ("item all", lambda v: v[4][1] + v[5][1]),
                        ("other all", lambda v: v[4][2] + v[5][2]),
                        ("ability out/all", None)):
            if f is None:
                a = sum(r[5][0] for r in hi) / max(1e-9, sum(r[4][0] + r[5][0] for r in hi))
                b = sum(r[5][0] for r in lo) / max(1e-9, sum(r[4][0] + r[5][0] for r in lo))
            else:
                tot = (lambda r: sum(r[4]) + sum(r[5])) if "all" in name else (lambda r: sum(r[4]))
                a = sum(f(r) for r in hi) / max(1e-9, sum(tot(r) for r in hi))
                b = sum(f(r) for r in lo) / max(1e-9, sum(tot(r) for r in lo))
            if a and b:
                acc[name][0] += w * math.log(a / b)
                acc[name][1] += w
    return {k: math.exp(v[0] / v[1]) for k, v in acc.items()}


def imbues(item, half, src="real"):
    """Per hero, each ability's damage per cast of holders of item (an imbue) over non-holders (same ability and
    net-worth bin), real rows (or the sim's with --sim): the imbued ability is the one that rises."""
    from deadsim import game
    G = game()
    gi = len(GROUPS) + ITEMS.index(item)
    rows = pickle.load(open(REAL_OUT if src == "real" else SIM_OUT, "rb"))
    by = collections.defaultdict(list)
    for r in rows:
        if half is None or int(r[10]) % 2 == half:
            by[r[0], r[1], int(r[8] // NW_BIN)].append(r)
    acc = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for (h, c, _), rs in by.items():
        hi, lo = [r for r in rs if r[15][gi]], [r for r in rs if not r[15][gi]]
        a, b = (sum(r[14] for r in x) / max(1e-9, sum(r[13] for r in x)) for x in (hi, lo))
        if len(hi) < 5 or len(lo) < 5 or a <= 0 or b <= 0 or min(sum(r[13] for r in x) for x in (hi, lo)) < 3:
            continue
        w = min(len(hi), len(lo))
        acc[h, c][0] += w * math.log(a / b)
        acc[h, c][1] += w
        acc[h, c][2] += len(hi)
    heroes = collections.defaultdict(list)
    for (h, c), v in acc.items():
        heroes[h].append((math.exp(v[0] / v[1]), c, v[2]))
    for h, vs in sorted(heroes.items(), key=lambda x: -sum(v[2] for v in x[1])):
        nm = {a.class_name: a.name + ("*" if a.ultimate else "") for a in G.heroes[h].abilities}
        print(f"{G.heroes[h].name:14s} " + "  ".join(f"{nm[c][:16]} {r:.2f} ({n})" for r, c, n in sorted(vs, reverse=True)))


def compare(half):
    mr, ms = os.path.join(WORK, "mix_real.pkl"), SIM_OUT.replace(".pkl", "_mix.pkl")
    if os.path.exists(mr) and os.path.exists(ms):
        a, b = shares(pickle.load(open(mr, "rb")), half), shares(pickle.load(open(ms, "rb")), half)
        print("damage shares hi / lo spirit souls (real pair fights 'in', whole match 'all'; sim duels)")
        for k in a:
            s = b.get(k.replace("all", "in"))
            print(f"   {k:16s} real {a[k]:6.3f}" + (f"   sim {s:6.3f}   real/sim {a[k] / s:6.3f}" if s and "out" not in k else ""))
    real = pickle.load(open(REAL_OUT, "rb"))
    sim = pickle.load(open(SIM_OUT, "rb"))
    if half is not None:
        real = [r for r in real if int(r[10]) % 2 == half]
        sim = [r for r in sim if int(r[10]) % 2 == half]
    sel = [("all", lambda r: True), ("plain", lambda r: not r[2] and r[6]), ("ult", lambda r: r[2])]
    for i, g in enumerate(GROUPS):
        sel += [(f"no {g}", lambda r, i=i: not r[15][i]), (f"{g} held", lambda r, i=i: r[15][i])]
    for name, key in sel:
        a, b = ratios(real, key), ratios(sim, key)
        print(f"{name:13s} real {len([r for r in real if key(r)]):6d} sim {len([r for r in sim if key(r)]):6d}")
        for k in a:
            s = b.get(k)
            print(f"   {k:13s} real hi/lo {a[k]:7.3f}   sim {s if s is None else round(s, 3)!s:>7s}"
                  + (f"   real/sim {a[k] / s:6.3f}" if s and k != "spirit souls" else ""))


if __name__ == "__main__":
    args = sys.argv[1:]
    half = int(args[args.index("--half") + 1]) if "--half" in args else None
    w = int(args[args.index("--workers") + 1]) if "--workers" in args else 4
    on = [args[i + 1] for i, a in enumerate(args) if a == "--on"]
    pos = [a for i, a in enumerate(args[1:], 1) if not a.startswith("--") and args[i - 1] not in ("--half", "--workers", "--on")]
    if args[0] == "real":
        real(half, w)
    elif args[0] == "mix":
        mix_real(w)
    elif args[0] == "imbues":
        imbues(" ".join(pos) or "Duration Extender", half, "sim" if "--sim" in args else "real")
    elif args[0] == "sim":
        sim(int(pos[0]) if pos else 1500, w, on)
    else:
        compare(half)
