"""Abilities by build (Mechanics.ability_lean): do real players with more souls in spirit items cast their abilities
sooner in a fight, and recast them sooner once the cooldown is up?

The damage audit had every hero's ability share ~4% under and its item share ~10% over on spirit builds, comparing
players of the same hero in the same fifth of the match (each item's own rate was flat with spirit item souls), and
the sim drew a build's first-cast holds (cast_timing) and recast waits (recast_timing) from one real curve per ability.

real: the rows of fit_cast_timing.py real (first cast per pair fight) and recast_timing.py real (each recast chance),
with the fighter's real build at that minute (fit_cast_timing.build_cols: spirit item souls, net worth, cooldown
reduction). A Cox model stratified by hero ability (Breslow ties) gives each covariate's log hazard ratio per 1000
souls: first casts 0.0060 +- 0.0006 for spirit item souls with net worth (-0.0008) and cooldown reduction in the model
(the sim already has cdr_ready), 0.0079 / 0.0075 in the even / odd match halves without cdr; recasts 0.0078 +- 0.0019.
--write: data/ability_lean.json (each hero's mean spirit item souls over its first-cast chances, the curve's center).

usage: python3 -I ability_lean.py [--half 0|1] [--write] [--workers 4]
"""
import collections
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "fight_length"))
sys.path.insert(0, HERE)
import fit_cast_timing as CT  # noqa: E402
import fit_length as FL  # noqa: E402
import recast_timing as RT  # noqa: E402

OUT = os.path.join(ROOT, "data", "ability_lean.json")
CT.BUILD_COLS = True


def jobs(half):
    from deadsim import game
    G = game()
    mids = {f.split(".")[0] for f in os.listdir(CT.CASTS) if f.endswith(".ndjson.gz")}
    mids &= {f.split(".")[0] for f in os.listdir(CT.FIGHTS) if f.endswith(".ndjson.gz")}
    if half is not None:
        mids = {m for m in mids if int(m) % 2 == half}
    sample = FL.load_sample(CT.SAMPLE, mids)
    first = {h.id: {ab.id: ab.class_name for ab in h.abilities} for h in G.heroes.values()}
    recast = {h.id: RT.slot_classes(h) for h in G.heroes.values()}
    base = [(os.path.join(CT.FIGHTS, f"{mid}.ndjson.gz"), os.path.join(CT.CASTS, f"{mid}.ndjson.gz"), sample[mid])
            for mid in sorted(mids) if mid in sample]
    return [b + (first, {}) for b in base], [b + (recast,) for b in base]


def cox(strata, k):
    """Stratified Cox (Breslow ties) by Newton: coefficients and standard errors. strata: [(t, event, X)]."""
    b = np.zeros(k)

    def grad(b):
        L, g, H = 0.0, np.zeros(k), np.zeros((k, k))
        for t, e, X in strata:
            eta = X @ b
            w = np.exp(eta)
            cw, cwx = np.cumsum(w), np.cumsum(w[:, None] * X, 0)
            cwxx = np.cumsum(w[:, None, None] * X[:, :, None] * X[:, None, :], 0)
            j = (np.searchsorted(-t, -t, side="right") - 1)[e > 0]
            ev = np.nonzero(e)[0]
            m = cwx[j] / cw[j][:, None]
            L += eta[ev].sum() - np.log(cw[j]).sum()
            g += (X[ev] - m).sum(0)
            H -= (cwxx[j] / cw[j][:, None, None]).sum(0) - np.einsum("ni,nj->ij", m, m)
        return L, g, H
    for _ in range(8):
        _, g, H = grad(b)
        b = b - np.linalg.solve(H, g)
    _, g, H = grad(b)
    return b, np.sqrt(np.diag(np.linalg.inv(-H)))


def strata_of(rows, cols):
    """rows: (stratum, time, event, {covariate: value}) -> [(t desc, event, X)]."""
    by = collections.defaultdict(list)
    for key, t, e, c in rows:
        by[key].append([t, e] + [c[x] for x in cols])
    out = []
    for rs in by.values():
        if len(rs) >= 20:
            a = np.array(rs, float)
            a = a[np.argsort(-a[:, 0])]
            out.append((a[:, 0], a[:, 1], a[:, 2:]))
    return out


def main():
    args = sys.argv[1:]
    half = int(args[args.index("--half") + 1]) if "--half" in args else None
    workers = int(args[args.index("--workers") + 1]) if "--workers" in args else 4
    fj, rj = jobs(half)
    first, recast = [], []
    with Pool(workers) as p:
        for rs in p.imap_unordered(CT.real_rows, fj):
            for hid, cls, u, d, _, _, ss, nw, cdr, _ in rs:
                first.append(((hid, cls), u if u is not None else d, u is not None,
                              {"spirit": ss / 1000, "nw": nw / 1000, "cdr10": cdr * 10}, hid, ss))
        for rs in p.imap_unordered(RT.real_rows, rj):
            for hid, cls, d, left, _, ss, nw, cdr, _ in rs:
                recast.append(((hid, cls), max(0.0, d) if d is not None else left, d is not None,
                               {"spirit": ss / 1000, "nw": nw / 1000, "cdr10": cdr * 10}, hid, ss))
    for name, rows in (("first casts", first), ("recasts", recast)):
        for cols in (["spirit"], ["spirit", "nw", "cdr10"]):
            b, se = cox(strata_of([r[:4] for r in rows], cols), len(cols))
            print(f"{name:12s} {len(rows):6d} rows  " + "  ".join(f"{c} {x:+.4f} +- {s:.4f}" for c, x, s in zip(cols, b, se)))
    if "--write" in args:
        acc = collections.defaultdict(list)
        for r in first:
            acc[r[4]].append(r[5])
        out = {"source": f"{len(fj)} Phantom+ replays, pair fights: first casts (scripts/cast_timing/ability_lean.py)",
               "note": "center: each hero's mean spirit item souls over its real first-cast chances; a build with s spirit "
                       "item souls casts at hazard exp(Mechanics.ability_lean x (s - center) / 1000) of the hero's real curves",
               "center": {str(h): round(sum(v) / len(v)) for h, v in sorted(acc.items())}}
        with open(OUT, "w") as fh:
            json.dump(out, fh, indent=1)
            fh.write("\n")
        print("wrote", OUT)


if __name__ == "__main__":
    main()
