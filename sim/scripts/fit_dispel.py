"""Fit Skill.dot_cleanse_share (the share of enemy DoTs a Dispel Magic holder spends it on) to real Decay damage.

Real side: damage/scripts/decay_vs_dispel.py -> damage/work/decay_vs_dispel_<badge>.json, ratio = Decay damage a
Dispel holder takes / what a teammate without it takes (same Decay owner, same 3-minute window). It folds in
everything that keeps Dispel off a DoT: cooldown, used on a stun or silence first, not noticing.

Sim side: real (Decay holder, Dispel holder) item snapshots from the same matches (data/builds/player_builds, items
held 120 s after both bought their item), dueled at the bracket's aim and reaction time (accuracy.dot_cleanse_delay)
with counterplay on. ratio(s) = Decay damage to the target holding Dispel with dot_cleanse_share s / to the same
target with Dispel removed. Real ratios compare fixed 3-minute windows, so the holder's longer survival (Dispel's
resist and heal) must not add Decay ticks: the target gets HP_MULT x health and can't die in the 30 s duel. (With
normal HP the share-0 ratio was 1.06-1.12 and the Phantom+ fit 0.43.) Dispel's spirit resist still lowers each tick,
as it does for real holders. Each bracket runs at its lowest badge (91 / 111 / 0), not weighted by real badges.
Duels use an engine rng, so the share is a random draw per DoT; it averages to the same share as the deterministic
phase-spread pick the overall score uses. ratio is
linear in s, so the fit solves it on a grid; the real 90% CI is mapped the same way.

usage (repo root, player_builds linked): python3 sim/scripts/fit_dispel.py [min_badge] [n_pairs] [days]
"""
import dataclasses
import glob
import gzip
import json
import os
import random
import sys
from collections import defaultdict
from multiprocessing import Pool

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "sim"))
from deadsim import Loadout, game  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.accuracy import dot_cleanse_delay, hero_default_skill  # noqa: E402

G = game()
DECAY, DISPEL = G.item("Decay").id, G.item("Dispel Magic").id
SHARES = (0.0, 0.25, 0.5, 0.75, 1.0)
SEEDS = 8
SETTLE_S = 120
HP_MULT = 50.0   # the Dispel holder can't die in the duel (fixed window, see the docstring)


def decay_dealt(a, b, seed):
    """Decay damage A deals to B in a 30 s duel where B can't die: Decay takes % of current HP, so the ratio
    between the two arms doesn't depend on the HP scale."""
    e = Engine(rng=random.Random(seed))
    fa, fb = make_fighter(e, a, "A"), make_fighter(e, b, "B")
    fb.max_hp_base *= HP_MULT
    fb.hp = fb.max_hp
    return e.run(fa, fb).a_dmg.get("Decay", 0.0)   # snapshot this long after the later of the two buys


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
    xsk = dataclasses.replace(hero_default_skill(G.hero(xh).name, badge=badge, counterplay=True),
                              dot_cleanse_delay=dot_cleanse_delay(badge))
    a = Loadout(dh, di, skill=dsk)
    res = {}
    for name, items, share in [("none", [i for i in xi if i != DISPEL], 0.0)] + [(s, xi, s) for s in SHARES]:
        b = Loadout(xh, items, skill=dataclasses.replace(xsk, dot_cleanse_share=share))
        res[str(name)] = sum(decay_dealt(a, b, s) for s in range(SEEDS)) / SEEDS
    return res


def solve(grid, r):
    """Share where the sim ratio meets r (grid: [(share, ratio)], ratio falling with share), clipped to 0-1."""
    for (s0, r0), (s1, r1) in zip(grid, grid[1:]):
        if r1 <= r <= r0 and r0 > r1:
            return s0 + (r0 - r) / (r0 - r1) * (s1 - s0)
    return 0.0 if r > grid[0][1] else 1.0


def main():
    min_badge = int(sys.argv[1]) if len(sys.argv) > 1 else 91
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    real = json.load(open(os.path.join(ROOT, "damage", "work", f"decay_vs_dispel_{min_badge}.json")))
    ps = pairs(min_badge, n, days)
    with Pool(os.cpu_count()) as p:
        rows = p.map(run, [(x, min_badge) for x in ps])
    base = sum(r["none"] for r in rows)
    grid = [(s, sum(r[str(s)] for r in rows) / base) for s in SHARES]
    lo, hi = real["ratio_90ci"]
    out = {"min_badge": min_badge, "real_matches": real["matches"], "real_paired_windows": real["paired_windows"],
           "real_ratio": round(real["ratio"], 3), "real_ratio_90ci": [round(lo, 3), round(hi, 3)],
           "sim_pairs": len(rows), "sim_seeds": SEEDS, "reaction_s": dot_cleanse_delay(min_badge),
           "sim_ratio_by_share": {str(s): round(r, 3) for s, r in grid},
           "fitted_share": round(solve(grid, real["ratio"]), 3),
           "fitted_share_90ci": [round(solve(grid, hi), 3), round(solve(grid, lo), 3)]}
    print(json.dumps(out, indent=1))
    os.makedirs(os.path.join(ROOT, "sim", "validation", "dispel"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "sim", "validation", "dispel", f"fit_{min_badge}.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
