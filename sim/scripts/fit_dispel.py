"""Fit Skill.dot_cleanse_delay (how long a Dispel Magic holder lets an enemy DoT run) to real Decay damage.

Real side: damage/scripts/decay_vs_dispel.py -> damage/work/decay_vs_dispel_<badge>.json, ratio = Decay damage a
Dispel holder takes / what a teammate without it takes (same Decay owner, same 3-minute window). It folds in
everything that keeps Dispel off a DoT: cooldown, used on a stun or silence first, not noticing.

Sim side: real (Decay holder, Dispel holder) item snapshots from the same Phantom+ matches (data/builds/player_builds,
items held 120 s after both bought their item), dueled at the bracket's aim with counterplay on. ratio(d) = Decay
damage to the target holding Dispel with dot_cleanse_delay d / to the same target with Dispel removed. The fitted
delay is where ratio(d) meets the real ratio (None = only below 50% health, inf = never on a DoT).

usage (repo root, player_builds linked): python3 sim/scripts/fit_dispel.py [min_badge] [n_pairs] [days]
"""
import dataclasses
import glob
import gzip
import json
import math
import os
import random
import sys
from collections import defaultdict
from multiprocessing import Pool

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "sim"))
from deadsim import Loadout, duel, game  # noqa: E402
from deadsim.accuracy import hero_default_skill  # noqa: E402

G = game()
DECAY, DISPEL = G.item("Decay").id, G.item("Dispel Magic").id
DELAYS = (0.5, 1.5, 3.0, 5.0, 7.0, 9.0, 11.0, None, math.inf)
SEEDS = 4
SETTLE_S = 120   # snapshot this long after the later of the two buys


def held_at(row, t):
    """Item ids owned at time t, without components that an owned upgrade consumed."""
    own = [i for i, bought, sold in row["purchases"] if bought <= t and (not sold or sold > t) and i in G.items]
    used = {c for i in own for c in G.items[i].components}
    return [i for i in own if G.items[i].class_name not in used]


def pairs(min_badge, n, days):
    files = sorted(glob.glob(os.path.join(ROOT, "data", "builds", "player_builds", "*.jsonl.gz")))[-days - 1:-1]
    by_match, seen = defaultdict(list), set()
    for fn in files:
        for line in gzip.open(fn, "rt"):
            r = json.loads(line)
            if (r["badge"] or 0) < min_badge or (r["match_id"], r["account_id"]) in seen:
                continue
            seen.add((r["match_id"], r["account_id"]))
            if r["hero_id"] in G.heroes and any(i in (DECAY, DISPEL) for i, _, _ in r["purchases"]):
                by_match[r["match_id"]].append(r)
    out = []
    for rows in by_match.values():
        for d in rows:
            for x in rows:
                if d is x:
                    continue
                td = next((b for i, b, _ in d["purchases"] if i == DECAY), None)
                tx = next((b for i, b, _ in x["purchases"] if i == DISPEL), None)
                if td is None or tx is None:
                    continue
                t = max(td, tx) + SETTLE_S
                di, xi = held_at(d, t), held_at(x, t)
                if t < min(d["duration_s"], x["duration_s"]) and DECAY in di and DISPEL in xi:
                    out.append((d["hero_id"], di, x["hero_id"], xi))
    random.seed(7)
    return random.sample(out, min(n, len(out)))


def run(args):
    (dh, di, xh, xi), badge = args
    dsk = hero_default_skill(G.hero(dh).name, badge=badge, counterplay=True)
    xsk = hero_default_skill(G.hero(xh).name, badge=badge, counterplay=True)
    a = Loadout(dh, di, skill=dsk)
    res = {}
    for name, items, delay in [("none", [i for i in xi if i != DISPEL], None)] + [(d, xi, d) for d in DELAYS]:
        b = Loadout(xh, items, skill=dataclasses.replace(xsk, dot_cleanse_delay=delay))
        res[str(name)] = sum(duel(a, b, rng=random.Random(s)).a_dmg.get("Decay", 0.0) for s in range(SEEDS)) / SEEDS
    return res


def main():
    min_badge = int(sys.argv[1]) if len(sys.argv) > 1 else 91
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    real = json.load(open(os.path.join(ROOT, "damage", "work", f"decay_vs_dispel_{min_badge}.json")))
    ps = pairs(min_badge, n, days)
    with Pool(os.cpu_count()) as p:
        rows = p.map(run, [(x, min_badge) for x in ps])
    base = sum(r["none"] for r in rows)
    ratio = {k: sum(r[k] for r in rows) / base for k in rows[0] if k != "none"}
    # ratio rises with the delay; interpolate the real ratio on the finite delays
    fin = [(d, ratio[str(d)]) for d in DELAYS if d is not None and math.isfinite(d)]
    fit = None
    if real["ratio"] <= fin[0][1]:
        fit = fin[0][0]
    for (d0, r0), (d1, r1) in zip(fin, fin[1:]):
        if fit is None and r0 <= real["ratio"] <= r1 and r1 > r0:
            fit = d0 + (real["ratio"] - r0) / (r1 - r0) * (d1 - d0)
    out = {"min_badge": min_badge, "pairs": len(rows), "real_ratio": real["ratio"], "real_ratio_90ci": real["ratio_90ci"],
           "sim_ratio_by_delay": {k: round(v, 3) for k, v in ratio.items()},
           "fitted_delay_s": None if fit is None else round(fit, 1),
           "note": "fitted_delay_s None = real ratio above every finite delay (Dispel ~never used on Decay)"}
    print(json.dumps(out, indent=1))
    os.makedirs(os.path.join(ROOT, "sim", "validation", "dispel"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "sim", "validation", "dispel", f"fit_{min_badge}.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
