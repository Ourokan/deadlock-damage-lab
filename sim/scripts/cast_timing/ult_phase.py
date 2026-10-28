"""How often real Phantom+ players cast their ultimate in a fight, by game phase (data/ult_phase.json,
Mechanics.ult_phase).

The first-cast holds (data/cast_timing.json, fit_cast_timing.py) are one curve per ability over the whole match. Real
ults go out in fewer fights early on: P(ult cast by 20 s of a pair fight) is 0.88x the hero's whole-match share
before 45% of the match, 1.06x to 75%, 1.02x after (all heroes; Solomon 0.53 / 1.50 / 0.78, Infernus 0.76 / 1.15 /
1.07). With the pooled hold the sim's ult share of damage was 0.94x real around 30% of the match, the big-burst ults
most (Violet 0.19 sim vs 0.11 real, Solomon 0.19 vs 0.12): scripts/phase_mix.py, validation/README.md.

real: the fight-length replays' pair fights and ability casts (as fit_cast_timing.py real). For each fighter and its
ult (unlocked: cast before in the match, in the fight, or the fourth ability unlock reached at the fighter's net
worth; "cast before" alone leaves out the fights between the unlock and the first cast): the first cast from PRE_S
before the fight's first hit, censored by the fight's end, the fight's match fraction and the fighter's net worth then.
fit: per hero, the Kaplan-Meier P(cast by HORIZON) in each match-fraction bin over the hero's whole-match one, shrunk
in ln to the pooled ratio of the bin (SHRINK fights of weight), at the bin's median net worth. Heroes with an ult
hold only (cast_timing.json); gated ults keep their own timing.
In the sim (mechanics.hold_first_casts): the hold's cast share c becomes min(CAP, c x mult(net worth)), holds in the
cast part keep their order and stretch over the new share, the not-cast part shrinks into what is left.

Rows with "matched" (scripts/cast_timing/ult_rate_match.py: Nurse Harrow, Dynamo) are kept as they are by fit --write.

usage: python3 -I ult_phase.py real [workers]   -> /mnt/project-files/analysis/work/ult_phase/rows.pkl
       python3 -I ult_phase.py fit [--parity even|odd] [--write]   (--parity: fit on that half of the matches by id)
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

ROWS = "/mnt/project-files/analysis/work/ult_phase/rows.pkl"
OUT = os.path.join(ROOT, "data", "ult_phase.json")
BINS = (0.0, 0.45, 0.75, 1.01)   # match fraction
SHRINK = 3000   # fights (split-half: held-out cast-share error 1693 / 1952 off, 1560 / 1703 at 3000, 1775 / 1851 at 300)
CLAMP = (0.3, 3.0)


def real_rows(args):
    """[(match id, hero id, ult class, first cast s or None, fight length s, match fraction, net worth)]."""
    from deadsim.fight import ability_budget
    fn, cast_fn, m, ults = args
    hero, ev = OT.read(fn)
    by_hero = {p["hero_id"]: p for p in m["players"]}
    rows = CT.real_casts([json.loads(line) for line in gzip.open(cast_fn, "rt")])
    off = statistics.median([r["tick"] / CT.T - r["v"] for r in rows]) if rows else 0.0
    casts = collections.defaultdict(list)
    for r in rows:
        casts[(r["a"], int(r["s"]))].append(r["tick"] / CT.T)
    for v in casts.values():
        v.sort()
    out = []
    for pawn, sp in RT.pair_spans(hero, ev, by_hero).items():
        hid = hero.get(pawn)
        if hid not in ults or hid not in by_hero:
            continue
        p = by_hero[hid]
        aid, cls = ults[hid]
        cs = casts.get((pawn, aid), [])
        for t0, t1 in sorted(sp):
            k = bisect.bisect_left(cs, t0 - CT.PRE_S)
            first = cs[k] if k < len(cs) and cs[k] <= t1 else None
            g = t0 - off
            nw = FL.nw_at(p["stats"], g)
            # unlocked: cast before in the match, or the fourth ability unlock reached at this net worth (a fight
            # after the unlock without a cast so far is a fight without the ult, not one left out)
            if first is None and not k and (nw is None or ability_budget(hid, nw)[0] < 4):
                continue
            out.append((m["match_id"], hid, cls, None if first is None else max(0.0, first - t0), t1 - t0,
                        g / m["duration_s"], nw))
    return out


def real(workers):
    from deadsim import game
    G = game()
    ults = {h.id: next(((ab.id, ab.class_name) for ab in h.abilities if ab.ultimate), None) for h in G.heroes.values()}
    ults = {h: u for h, u in ults.items() if u}
    mids = {f.split(".")[0] for f in os.listdir(CT.CASTS) if f.endswith(".ndjson.gz")}
    mids &= {f.split(".")[0] for f in os.listdir(CT.FIGHTS) if f.endswith(".ndjson.gz")}
    sample = FL.load_sample(CT.SAMPLE, mids)
    jobs = [(os.path.join(CT.FIGHTS, f"{mid}.ndjson.gz"), os.path.join(CT.CASTS, f"{mid}.ndjson.gz"), sample[mid], ults)
            for mid in sorted(mids) if mid in sample]
    rows = []
    with Pool(workers) as p:
        for rs in p.imap_unordered(real_rows, jobs):
            rows += rs
    os.makedirs(os.path.dirname(ROWS), exist_ok=True)
    with open(ROWS, "wb") as fh:
        pickle.dump(rows, fh)
    print(len(rows), "fight starts x ults from", len(jobs), "matches")


def by_horizon(rows):
    """Kaplan-Meier P(cast by CT.HORIZON | fight going) of (first, length) rows."""
    return CT.km(rows)[CT.GRID.index(CT.HORIZON)]


def fit(parity=None, write=False):
    from deadsim import game
    from deadsim.mechanics import cast_holds
    G = game()
    holds = cast_holds()
    with open(ROWS, "rb") as fh:
        rows = [r for r in pickle.load(fh) if r[6] is not None and r[5] > 0]
    if parity is not None:
        rows = [r for r in rows if r[0] % 2 == parity]
    by = collections.defaultdict(list)
    for r in rows:
        if holds.get(CT.cls_key(r[1], r[2])):
            by[r[1], r[2]].append(r)
    nb = len(BINS) - 1
    pts = {}
    for key, rs in by.items():
        allp = by_horizon([(r[3], r[4]) for r in rs])
        if allp <= 0:
            continue
        row = []
        for b in range(nb):
            sub = [r for r in rs if BINS[b] <= r[5] < BINS[b + 1]]
            if not sub:
                row = None
                break
            p = by_horizon([(r[3], r[4]) for r in sub])
            row.append((len(sub), statistics.median(r[6] for r in sub), math.log(max(p, 0.01) / allp)))
        if row:
            pts[key] = row
    pooled = []
    for b in range(nb):
        w = sum(v[b][0] for v in pts.values())
        pooled.append(sum(v[b][0] * v[b][2] for v in pts.values()) / w)
    out = {}
    for (hid, cls), row in sorted(pts.items(), key=lambda x: G.hero(x[0][0]).name):
        mults = []
        for b, (n, nw, lr) in enumerate(row):
            s = (n * lr + SHRINK * pooled[b]) / (n + SHRINK)
            mults.append([round(nw), round(min(CLAMP[1], max(CLAMP[0], math.exp(s))), 4)])
        out[CT.cls_key(hid, cls)] = {"name": G.hero(hid).name, "fights": [n for n, _, _ in row],
                                     "raw": [round(math.exp(lr), 3) for _, _, lr in row], "points": mults}
        print(f"{G.hero(hid).name:14s} fights {' '.join(f'{n:5d}' for n, _, _ in row)}  raw "
              f"{' '.join(f'{math.exp(lr):.2f}' for _, _, lr in row)}  mult {' '.join(f'{m:.2f}@{nw}' for nw, m in mults)}")
    print("pooled", [round(math.exp(v), 3) for v in pooled])
    if write:
        if os.path.exists(OUT):   # rows matched to the sim's own response (ult_rate_match.py) keep their points
            with open(OUT) as fh:
                old = json.load(fh)["sources"]
            out.update({k: v for k, v in old.items() if v.get("matched")})
        with open(OUT, "w") as fh:
            json.dump({"source": "Phantom+ fight-length replays, pair fights, P(ult cast by "
                                 f"{CT.HORIZON:.0f} s) per match-fraction bin {list(BINS[:-1])} over the whole match "
                                 "(scripts/cast_timing/ult_phase.py)",
                       "note": "ult hold cast share x mult at the fighter's net worth, linear in ln net worth between "
                               "points, flat outside (Mechanics.ult_phase)",
                       "pooled": [round(math.exp(v), 4) for v in pooled], "sources": out}, fh, indent=1)
            fh.write("\n")
        print("wrote", OUT)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "real":
        real(int(a[1]) if len(a) > 1 else os.cpu_count())
    elif a and a[0] == "fit":
        par = None
        if "--parity" in a:
            par = 0 if a[a.index("--parity") + 1] == "even" else 1
        fit(par, "--write" in a)
    else:
        print(__doc__)
