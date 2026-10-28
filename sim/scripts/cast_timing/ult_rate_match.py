"""Match a hero's ult casts per fight by net worth to real games: rewrite its Mechanics.ult_phase points from the sim's
own response (data/ult_phase.json, the hero's source row gets "matched").

ult_phase.py fits the ult hold's cast share by match fraction from real KM P(cast by 20 s), pooled bins over the whole
lane / mid / late, and the sim's duels then cast the ult with that share. For Nurse Harrow that left the lane far off:
real Nurses cast Lurking Terrors in 16% of their pair fights with the ult unlocked below 8k souls and 25-28% later,
while the audit's duels cast it (P(cast) x P(the real fight still going at the cast)) in 29-30% below 8k and 32-36%
later: the lane ult 1.8x real against the late one at 1.2x, its share of her damage 0.22 at 30% of the match vs real
0.15 (scripts/phase_mix.py). Real rate per net worth bin: the share of the hero's pair fights with the ult unlocked
in which it was cast (ult_phase.py real rows); sim rate: the damage audit's duels of the hero's players (AUDIT_SEED draws),
first ult cast weighted by Engine.length_w at the cast, duels with the ult unlocked. New mult per bin = old mult x
real / sim, scaled so the sim-duel weighted mean ratio is 1 (the level stays with the hold and the ult's corr; refit
the corr after: scripts/ability_corr_heroes.py --hero). ROUNDS rounds, each from the last.

Matched so far: Nurse Harrow, Dynamo (--rows), Violet, Sinclair (--sample validation/sinclair_sample.jsonl.gz);
McGinnis and Pocket were tried and left out (validation/README.md "Ult casts per fight for four more heroes"). After a
patch rerun this by hand for them (ult_phase.py fit keeps matched rows, CI doesn't redo them).

usage: python3 ult_rate_match.py --hero "Nurse Harrow" [--parity even|odd] [--sample PATH] [--rows PATH] [--write]
       (--parity: real rows of that half of the matches by id; --sample: the audit sample for the sim side;
       --rows: real rows from more replays of the hero, ult_phase.py real_rows format, e.g. Dynamo:
       /mnt/project-files/analysis/work/dynamo_replays/ult_rows.pkl from scripts/cast_timing/hero_ult_rows.py)
"""
import collections
import gzip
import json
import math
import os
import pickle
import random
import statistics
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, HERE)
os.environ.pop("AUDIT_COVER", None)   # duels at 30 / 60 / 90% (L.FRACS): the souls spread over the match
import damage_audit as D  # noqa: E402
import landing_rates as L  # noqa: E402
import ult_phase as UP  # noqa: E402
from deadsim import abilities as A  # noqa: E402
from deadsim import game, mechanics  # noqa: E402

NW_BINS = (0, 6000, 8000, 11000, 14000, 20000, 27000, 10 ** 9)
SEEDS = (0, 1, 2, 3)
ROUNDS = 2
MIN_REAL = 60     # real unlocked fights for a bin's own ratio (fewer: merged into the next bin)
CLAMP = (0.1, 3.0)

_states = []
_rec = []


def _init(orig):
    def f(self, *a, **k):
        orig(self, *a, **k)
        if self.ab.ultimate:
            _states.append(self)
    return f


def _cast(orig):
    def f(self):
        if self.ab.ultimate and not self.casts:
            self.scratch["_rate_w"] = self.f.e.length_w()
        return orig(self)
    return f


def _duel(orig):
    def f(a, b, **kw):
        _states.clear()
        r = orig(a, b, **kw)
        me = next((s for s in _states if s.f.name.endswith("(A)")), None)
        if me is not None:
            _rec.append((a.souls, me.unlocked, me.scratch.get("_rate_w", 0.0)))
        return r
    return f


def _setup(seed, ult_phase):
    global _patched
    if not globals().get("_patched"):
        A.AbilityState.__init__ = _init(A.AbilityState.__init__)
        A.AbilityState.cast = _cast(A.AbilityState.cast)
        D.duel = _duel(D.duel)
        _patched = True
    D.SEED = seed
    mechanics._ULT_PHASE = None
    if ult_phase is not None:   # this round's points (workers don't see the parent's file edits otherwise)
        mechanics._ULT_PHASE = {k: [(math.log(nw), m) for nw, m in v["points"]] for k, v in ult_phase["sources"].items()}


def _job(args):
    job, seed, ult_phase = args
    _setup(seed, ult_phase)
    _rec.clear()
    D.sim_player(job)
    return list(_rec)


def bin_of(nw):
    return next(i for i in range(len(NW_BINS) - 1) if nw < NW_BINS[i + 1])


def real_rate(hid, cls, parity=None, path=None):
    with open(path or UP.ROWS, "rb") as fh:
        rows = [r for r in pickle.load(fh) if r[1] == hid and r[2] == cls and r[6] is not None]
    if parity is not None:
        rows = [r for r in rows if r[0] % 2 == parity]
    out = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        k = bin_of(r[6])
        out[k][0] += 1
        out[k][1] += r[3] is not None
    return out


def sim_rate(jobs, ult_phase, workers):
    out = collections.defaultdict(lambda: [0, 0.0, []])
    with ProcessPoolExecutor(workers) as ex:
        for recs in ex.map(_job, [(j, s, ult_phase) for s in SEEDS for j in jobs], chunksize=4):
            for souls, unlocked, w in recs:
                if unlocked and souls:
                    k = bin_of(souls)
                    out[k][0] += 1
                    out[k][1] += w
                    out[k][2].append(souls)
    return out


def merged(real, sim):
    """Bins with fewer than MIN_REAL real fights merged into the next (the last into the one before)."""
    groups, cur = [], []
    for k in range(len(NW_BINS) - 1):
        cur.append(k)
        if sum(real[x][0] for x in cur) >= MIN_REAL and sum(sim[x][0] for x in cur):
            groups.append(cur)
            cur = []
    if cur and groups:
        groups[-1] += cur
    return groups


def main():
    a = sys.argv[1:]
    hero = a[a.index("--hero") + 1]
    parity = None
    if "--parity" in a:
        parity = 0 if a[a.index("--parity") + 1] == "even" else 1
    sample = a[a.index("--sample") + 1] if "--sample" in a else os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
    workers = os.cpu_count()
    G = game()
    h = G.hero(hero)
    ult = next(ab for ab in h.abilities if ab.ultimate)
    key = f"{h.id}:{ult.class_name}"
    with open(UP.OUT) as fh:
        data = json.load(fh)
    src = data["sources"][key]
    jobs = []
    for line in gzip.open(sample, "rt"):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] == h.id and L.gun_known(p):
                jobs.append((m, p["slot"]))
    real = real_rate(h.id, ult.class_name, parity, a[a.index("--rows") + 1] if "--rows" in a else None)
    for rnd in range(ROUNDS + 1):
        sim = sim_rate(jobs, data, workers)
        groups = merged(real, sim)
        rows, tot_w, tot_r = [], 0.0, 0.0
        for g in groups:
            rn, rc = sum(real[k][0] for k in g), sum(real[k][1] for k in g)
            sn, sw = sum(sim[k][0] for k in g), sum(sim[k][1] for k in g)
            souls = statistics.median(s for k in g for s in sim[k][2])
            ratio = (rc / rn) / max(1e-9, sw / sn)
            rows.append((g, souls, rc / rn, sw / sn, ratio, sn))
            tot_w += sn
            tot_r += sn * ratio
        norm = tot_r / tot_w
        print(f"round {rnd}: " + "  ".join(f"{NW_BINS[g[0]]}+ real {pr:.3f} sim {ps:.3f} ({sn})" for g, _, pr, ps, _, sn in rows))
        if rnd == ROUNDS:
            break
        pts = []
        for g, souls, _, _, ratio, _ in rows:
            old = mechanics._interp_ln([(math.log(nw), m) for nw, m in src["points"]], souls)
            pts.append([round(souls), round(min(CLAMP[1], max(CLAMP[0], old * ratio / norm)), 4)])
        src["points"] = pts
        print("  points", pts)
    src["matched"] = (f"scripts/cast_timing/ult_rate_match.py: points rewritten to the real ult casts per unlocked "
                      f"fight by net worth bin {list(NW_BINS[1:-1])} against the audit duels")
    if "--write" in a:
        with open(UP.OUT, "w") as fh:
            json.dump(data, fh, indent=1)
            fh.write("\n")
        print("wrote", UP.OUT)


if __name__ == "__main__":
    main()
