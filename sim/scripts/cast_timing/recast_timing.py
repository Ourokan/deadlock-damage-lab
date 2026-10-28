"""When real Phantom+ players recast an ability inside a fight once its cooldown is ready, against the sim, which
recasts the moment the cooldown is up (its rule allowing).

real: the fight-length replays' pair fights (as fit_cast_timing.py real) and their ability casts (real_casts: no
cooldown cuts). For each fighter of a fight, each cast of an ability from PRE_S before the fight's first hit on whose
cooldown runs out before the fight's last hit is a recast chance: ready = cast + the player's cooldown for it at that
moment (the sim's AbilityState.cooldown() of the player's real build at that game time: items, net worth -> ability
tiers by the popular order), delay = the next cast of the ability - ready, censored at the fight's end. Kaplan-Meier
P(recast by t s after ready | fight still going) on GRID. Charged abilities (2+ charges) and ultimates are left out
(charges recast between charges; an ult's cooldown outlasts the fight). Silver's wolf abilities count as their own rows (their
class ids in replays; the slot's cooldown reduction). fit: rows for abilities with MIN_ROW chances, shrunk toward the
pooled curve (n / (n + SHRINK)); split-half 0.110 / 0.096 (MIN_FIT 100 rows only) -> 0.101 / 0.089.
sim: the damage audit's duels (real builds both sides, the model as the searches fight): the same curve from the
duels' cast times (engine.PROFILE_SOURCES keeps every cast, Fighter.casts_at).

usage: python3 -I recast_timing.py real [--workers 4]    -> validation/recast_timing_real.json
       python3 -I recast_timing.py fit [n=1500] [workers]  -> data/recast_timing.json (sim run with recasts on ready)
       python3 -I recast_timing.py sim [n=1500] [workers] [--on]  -> real vs sim per ability (validation/recast_timing.md)
Split-half: real --half 0|1 --real PATH; fit --real PATH --report PATH with RECAST_OUT=PATH; sim --on --data PATH
--real PATH --report PATH (the waits fitted on one half against the other half's real curves).
"""
import bisect
import collections
import gzip
import json
import os
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

REAL = os.path.join(ROOT, "validation", "recast_timing_real.json")
REPORT = os.path.join(ROOT, "validation", "recast_timing.md")
GRID = [0.5 * k for k in range(49)]   # 0..24 s after ready
MIN_CHANCES = 40
CD_BUCKET_S = 60.0   # the player's cooldowns are taken from the build at the start of each minute


def cooldowns(p, t, cache):
    """{ability class: cooldown s} of player p's real build at game time t (per CD_BUCKET_S), charged abilities None."""
    b = int(t // CD_BUCKET_S)
    key = (p["slot"], b)
    if key not in cache:
        import landing_rates as L
        from deadsim import Loadout, game
        from deadsim.engine import Engine
        from deadsim.fight import make_fighter
        items, souls = L.build_at(p, max(0.0, b * CD_BUCKET_S))
        f = make_fighter(Engine(mech=None), Loadout(game().hero(p["hero_id"]).name, items, souls=souls))
        cds = {}
        for ab in f.abilities:
            cds[ab.ab.class_name] = None if ab.max_charges() > 1 or ab.ab.ultimate or not ab.unlocked else ab.cooldown()
            if cds[ab.ab.class_name] and getattr(ab.impl, "WOLF", ""):   # Silver's wolf ability on the slot
                cds[ab.impl.WOLF] = ab.impl.wolf_cooldown(ab.ctx)
        cache[key] = cds
    return cache[key]


def slot_classes(h):
    """{ability id in replays: class} of hero h: its abilities and the wolf abilities cast from Silver's slots."""
    from deadsim.abilities import REGISTRY, load_heroes
    load_heroes()
    out = {ab.id: ab.class_name for ab in h.abilities}
    for ab in h.abilities:
        w = getattr(REGISTRY.get(ab.class_name), "WOLF", "")
        if w:
            from deadsim.heroes.werewolf import raw_ability
            out[raw_ability(w).id] = w
    return out


def pair_spans(hero, ev, by_hero):
    """{pawn: [(t0, t1)]} pair fights (fit_cast_timing.real_rows)."""
    pairs = collections.defaultdict(list)
    for e in ev:
        _, a, v = e[:3]
        pa, pv = by_hero.get(hero.get(a)), by_hero.get(hero.get(v))
        if pa is None or pv is None or pa["team"] == pv["team"]:
            continue
        pairs[min(a, v), max(a, v)].append(e)
    spans = collections.defaultdict(list)
    for (x, y), es in pairs.items():
        runs = []
        for e in es:
            if not runs or e[0] - runs[-1][-1][0] > FL.GAP_S:
                runs.append([])
            runs[-1].append(e)
        for f in runs:
            death = next((k for k, e in enumerate(f) if e[3] <= 0), None)
            if death is not None:
                f = f[:death + 1]
            if len(f) < FL.MIN_HITS or len({(e[1], e[2]) for e in f}) < 2:
                continue
            for pawn in (x, y):
                spans[pawn].append((f[0][0], f[-1][0]))
    return spans


def real_rows(args):
    """[(hero id, ability class, delay s after ready or None, time left in the fight at ready s, cooldown s)]."""
    fn, cast_fn, m, abil = args
    hero, ev = OT.read(fn)
    by_hero = {p["hero_id"]: p for p in m["players"]}
    rows = CT.real_casts([json.loads(line) for line in gzip.open(cast_fn, "rt")])
    offs = [r["tick"] / CT.T - r["v"] for r in rows]
    off = statistics.median(offs) if offs else 0.0   # tick / T -> game time
    casts = collections.defaultdict(list)
    for r in rows:
        casts[(r["a"], int(r["s"]))].append(r["tick"] / CT.T)
    for v in casts.values():
        v.sort()
    out, cache, bcache = [], {}, {}
    for pawn, sp in pair_spans(hero, ev, by_hero).items():
        hid = hero.get(pawn)
        if hid not in abil or hid not in by_hero:
            continue
        p = by_hero[hid]
        for t0, t1 in sorted(sp):
            for aid, cls in abil[hid].items():
                cs = casts.get((pawn, aid), [])
                for k in range(bisect.bisect_left(cs, t0 - CT.PRE_S), len(cs)):
                    c = cs[k]
                    if c > t1:
                        break
                    cd = cooldowns(p, c - off, cache).get(cls)
                    if not cd:
                        continue
                    ready = c + cd
                    if ready >= t1:
                        continue
                    nxt = cs[k + 1] if k + 1 < len(cs) else None
                    d = nxt - ready if nxt is not None and nxt <= t1 else None
                    row = (hid, cls, d, t1 - ready, cd)
                    out.append(row + CT.build_cols(p, c - off, m, bcache) if CT.BUILD_COLS else row)
    return out


def km_grid(rows):
    ev = sorted((u if u is not None else d, u is not None) for u, d in rows)
    n, i, surv, out = len(ev), 0, 1.0, []
    for t in GRID:
        while i < n and ev[i][0] <= t:
            j, c = i, 0
            while j < n and ev[j][0] == ev[i][0]:
                c += ev[j][1]
                j += 1
            surv *= 1.0 - c / (n - i)
            i = j
        out.append(round(1.0 - surv, 4))
    return out


def real(workers):
    from deadsim import game
    G = game()
    abil = {h.id: slot_classes(h) for h in G.heroes.values()}
    mids = {f.split(".")[0] for f in os.listdir(CT.CASTS) if f.endswith(".ndjson.gz")}
    mids &= {f.split(".")[0] for f in os.listdir(CT.FIGHTS) if f.endswith(".ndjson.gz")}
    if HALF is not None:   # split-half: even (0) or odd (1) match ids only
        mids = {m for m in mids if int(m) % 2 == HALF}
    sample = FL.load_sample(CT.SAMPLE, mids)
    jobs = [(os.path.join(CT.FIGHTS, f"{mid}.ndjson.gz"), os.path.join(CT.CASTS, f"{mid}.ndjson.gz"), sample[mid], abil)
            for mid in sorted(mids) if mid in sample]
    rows = collections.defaultdict(list)
    with Pool(workers) as p:
        for rs in p.imap_unordered(real_rows, jobs):
            for hid, cls, d, left, cd in rs:
                rows[f"{hid}:{cls}"].append((d, left, cd))
    res = {"source": f"{len(jobs)} Phantom+ replays, pair fights (scripts/cast_timing/recast_timing.py real)",
           "grid_s": GRID, "rows": {}}
    allr = []
    for key, rs in sorted(rows.items()):
        allr += rs
        if len(rs) < MIN_CHANCES:
            continue
        ds = [d for d, _, _ in rs if d is not None]
        res["rows"][key] = {"chances": len(rs), "recast": len(ds), "cooldown_s": round(statistics.median(c for *_, c in rs), 2),
                            "early": round(sum(d < -0.5 for d in ds) / max(1, len(ds)), 3),
                            "recast_by": km_grid([(None if d is None else max(0.0, d), left) for d, left, _ in rs])}
    res["pooled"] = {"chances": len(allr), "recast_by": km_grid([(None if d is None else max(0.0, d), left) for d, left, _ in allr])}
    with open(REAL, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(len(res["rows"]), "rows from", len(jobs), "matches;", len(allr), "chances")
    c = res["pooled"]["recast_by"]
    print("pooled P(recast by 0.5/1/2/4/8/16 s after ready):", [c[k] for k in (1, 2, 4, 8, 16, 32)])


_REC = None


def _sim_job(job):
    """The audit duels of one player: [(ability class, delay after ready or None, time left at ready)]."""
    global _REC
    import damage_audit as A
    from deadsim import abilities, engine
    from deadsim.heroes import werewolf
    if _REC is None:
        _REC = {"casts": [], "ends": {}}
        cast0, run0 = abilities.AbilityState.cast, engine.Engine.run

        def cast(self):
            if self.f.name.endswith("(A)") and not self.ab.ultimate and self.max_charges() == 1 and not self.scratch.get("prefight"):
                cls, cd = self.ab.class_name, self.cooldown()
                if getattr(self.impl, "WOLF", "") and werewolf.wolf(self.ctx):   # Silver's slot casts its wolf ability
                    cls, cd = self.impl.WOLF, self.impl.wolf_cooldown(self.ctx)
                _REC["casts"].append((id(self.f.e), cls, self.f.e.t, cd))
            return cast0(self)

        def run(self, *a, **k):
            r = run0(self, *a, **k)
            _REC["ends"][id(self)] = self.t
            return r
        abilities.AbilityState.cast, engine.Engine.run = cast, run
    _REC["casts"].clear()
    _REC["ends"].clear()
    hid, _, _ = A.sim_player(job)
    by = collections.defaultdict(list)
    for eid, cls, t, cd in _REC["casts"]:
        by[eid, cls].append((t, cd))
    out = []
    for (eid, cls), cs in by.items():
        end = _REC["ends"].get(eid)
        if end is None:
            continue
        for k, (t, cd) in enumerate(cs):
            ready = t + cd
            if ready >= end:
                continue
            d = cs[k + 1][0] - ready if k + 1 < len(cs) else None
            out.append((cls, d, end - ready))
    return hid, out


def sim(n, workers, on=False, fit_out=None):
    """Real vs sim recast curves (on: with Mechanics.recast_timing); fit_out: write data/recast_timing.json from the
    real rows and this (holds off) sim run."""
    import dataclasses
    import random
    import damage_audit as A
    A.MECH = dataclasses.replace(A.MECH, recast_timing=on)
    import landing_rates as L
    from deadsim import game
    G = game()
    jobs = []
    for line in gzip.open(CT.SAMPLE):
        m = json.loads(line)
        jobs += [(m, p["slot"]) for p in m["players"] if p["hero_id"] in G.heroes and L.gun_known(p)]
    random.Random(1).shuffle(jobs)
    real_rows = json.load(open(REAL))["rows"]
    rows = collections.defaultdict(list)
    with Pool(workers) as p:
        for hid, rs in p.imap_unordered(_sim_job, jobs[:n], chunksize=8):
            for cls, d, left in rs:
                rows[f"{hid}:{cls}"].append((None if d is None else max(0.0, d), left))
    nm = {f"{h.id}:{a.class_name}": f"{h.name}: {a.name}" for h in G.heroes.values() for a in h.abilities}
    from deadsim.heroes.werewolf import raw_ability
    nm.update({f"{h.id}:{c}": f"{h.name}: {raw_ability(c).name} (wolf)" for h in G.heroes.values()
               for c in slot_classes(h).values() if f"{h.id}:{c}" not in nm})
    lines = ["# Ability recasts after the cooldown is ready: sim vs real Phantom+ (scripts/cast_timing/recast_timing.py)",
             "", "P(recast by 0.5 / 1 / 2 / 4 / 8 s after the cooldown is ready | fight still going). Real: "
             + json.load(open(REAL))["source"] + f". Sim: damage audit duels ({n} players x 3).", "",
             "| ability | real chances | real | sim chances | sim |", "|---|---|---|---|---|"]
    pr, ps = [], []
    for key, r in sorted(real_rows.items(), key=lambda x: nm.get(x[0], x[0])):
        s = rows.get(key)
        if not s or len(s) < 20:
            continue
        c = km_grid(s)
        pr.append(r["recast_by"])
        ps.append(c)
        f5 = lambda c: " / ".join(f"{c[k]:.2f}" for k in (1, 2, 4, 8, 16))  # noqa: E731
        lines.append(f"| {nm.get(key, key)} | {r['chances']} | {f5(r['recast_by'])} | {len(s)} | {f5(c)} |")
    gap = statistics.mean(abs(a - b) for x, y in zip(pr, ps) for a, b in zip(x[:17], y[:17]))
    lines[3:3] = [f"Mean |real - sim| of the curve (0-8 s): {gap:.3f} over {len(pr)} abilities "
                  f"(Mechanics.recast_timing {'on' if on else 'off'}).", ""]
    print("\n".join(lines))
    with open(REPORT, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    if fit_out:
        fit(real_rows, {k: (len(v), km_grid(v)) for k, v in rows.items()}, fit_out)


def waits(curve):
    """QBINS equal-probability waits (s) of a recast curve on GRID (None past its share by the last GRID point)."""
    out = []
    for b in range(QBINS):
        p = (b + 0.5) / QBINS
        if p > curve[-1]:
            out.append(None)
            continue
        k = next(k for k in range(len(curve)) if curve[k] >= p)
        if k == 0:
            out.append(0.0)
            continue
        lo = curve[k - 1]
        out.append(round(GRID[k] - 0.5 * (curve[k] - p) / max(1e-9, curve[k] - lo), 3))
    return out


def fit(real_rows, sim_rows, path):
    """Rows: real abilities with MIN_FIT chances the sim recasts on ready (P(by 0.5 s) >= ON_READY or over SKIP_MARGIN
    above real, or too few sim chances to tell); skip: abilities the sim gates itself to about real timing; pooled: the rows' curves weighted by
    chances, for abilities without a row."""
    src, skip, pool, w = {}, [], [0.0] * len(GRID), 0
    for key, r in sorted(real_rows.items()):
        n, c = sim_rows.get(key, (0, None))
        if n >= MIN_SIM and c[1] < min(ON_READY, r["recast_by"][1] + SKIP_MARGIN):
            skip.append(key)
            continue
        if r["chances"] < MIN_FIT:
            continue
        pool = [a + r["chances"] * b for a, b in zip(pool, r["recast_by"])]
        w += r["chances"]
    pooled = [round(v / w, 4) for v in pool]
    for key, r in sorted(real_rows.items()):
        if key in skip or r["chances"] < MIN_ROW:
            continue
        k = r["chances"] / (r["chances"] + SHRINK)   # few chances: shrunk toward the pooled curve
        src[key] = waits([k * a + (1 - k) * b for a, b in zip(r["recast_by"], pooled)])
    res = {"source": json.load(open(REAL))["source"] + "; sim: damage audit duels, recast timing off",
           "note": NOTE, "grid_s": GRID, "pooled_by": pooled, "pooled": waits(pooled), "skip": skip, "sources": src}
    with open(path, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(f"{len(src)} rows, {len(skip)} skipped; pooled waits {res['pooled']}")


NOTE = ("QBINS equal-probability waits (s) past an ability's cooldown before its next cast in a fight (None: not again "
        "in that fight), from the real Kaplan-Meier P(recast by t s after ready | fight still going) "
        "(Mechanics.recast_timing). sources: per ability; pooled: abilities without a row; skip: abilities the sim "
        "gates itself (a toggle, stacks), which keep their own timing.")
QBINS = 20
MIN_FIT = 100   # chances for an ability's curve to count in the pooled one
MIN_ROW = int(os.environ.get("RECAST_MIN_ROW", 40))   # chances for its own row
SHRINK = float(os.environ.get("RECAST_SHRINK", 50))   # its curve x n / (n + SHRINK) + pooled x the rest
MIN_SIM = 20
ON_READY = 0.5
SKIP_MARGIN = 0.1   # a self-gated ability recasting this much more often by 0.5 s than real still gets the waits


HALF = None

if __name__ == "__main__":
    args = sys.argv[1:]
    for k in ("--half", "--real", "--data", "--report"):
        if k in args:
            i = args.index(k)
            v = args[i + 1]
            del args[i:i + 2]
            if k == "--half":
                HALF = int(v)
            elif k == "--real":
                REAL = v
            elif k == "--report":
                REPORT = v
            else:   # sim with this recast_timing.json (forked workers inherit it)
                from deadsim import mechanics as M
                M._RECAST = json.load(open(v))
                M._RECAST["skip"] = set(M._RECAST.get("skip", ()))
    w = int(args[args.index("--workers") + 1]) if "--workers" in args else 4
    if args[0] == "real":
        real(w)
    elif args[0] in ("sim", "fit"):
        pos = [a for a in args[1:] if not a.startswith("--") and not (args.index(a) > 0 and args[args.index(a) - 1] == "--workers")]
        sim(int(pos[0]) if pos else 1500, int(pos[1]) if len(pos) > 1 else os.cpu_count(), on="--on" in args,
            fit_out=(os.environ.get("RECAST_OUT") or os.path.join(ROOT, "data", "recast_timing.json")) if args[0] == "fit" else None)
