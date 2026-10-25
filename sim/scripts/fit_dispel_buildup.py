"""Fit Skill.dot_cleanse_share_buildup (share of build-up DoT episodes, Afterburn / Toxic Bullets, a Dispel Magic
holder spends it on) to real Afterburn damage on Dispel holders.

Real side: counters/scripts/cleanse_real.py "Dispel Magic" ... Infernus -> counters/work/cleanse_dispel_magic_<badge>.json:
per 3-minute window and Infernus dealer, damage per max HP taken by Dispel holders / by teammates without it.
Holders get shot by Infernus more (gun ratio 1.16), so the target is Afterburn's ratio / Napalm's (same caster,
same targeting, nothing for Dispel to purge but a debuff; it also cancels the holders' 10% spirit resist on the sim
side, since real damage-matrix values are before resists).

Sim side as fit_dispel.py: real (Infernus, Dispel holder) item snapshots from the same matches, dueled FIGHT_S at the
bracket's aim and reaction time with counterplay on, the holder at HP_MULT x health so the window is fixed, the
other DoT share at its own fit. Ratio(s) = (Afterburn / Napalm with share s) / (the same with Dispel removed).

usage (repo root, player_builds linked or PLAYER_BUILDS set): python3 sim/scripts/fit_dispel_buildup.py [min_badge] [n_pairs] [days]
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
from deadsim.accuracy import hero_default_skill  # noqa: E402

G = game()
DISPEL = G.item("Dispel Magic").id
INFERNUS = G.hero("Infernus").id
SHARES = (0.0, 0.25, 0.5, 0.75, 1.0)
SEEDS = 6
SETTLE_S = 120
HP_MULT = 50.0
FIGHT_S = 30.0   # as fit_dispel.py
BUILDS = os.environ.get("PLAYER_BUILDS", os.path.join(ROOT, "data", "builds", "player_builds"))


def held_at(row, t):
    own = [i for i, bought, sold in row["purchases"] if bought <= t and (not sold or sold > t) and i in G.items]
    used = {c for i in own for c in G.items[i].components}
    return [i for i in own if G.items[i].class_name not in used]


def pairs(min_badge, n, days):
    files = sorted(glob.glob(os.path.join(BUILDS, "*.jsonl.gz")))[-days:]
    by_match, seen = defaultdict(list), set()
    for fn in files:
        for line in gzip.open(fn, "rt"):
            r = json.loads(line)
            if (r["badge"] or 0) < min_badge or (r["match_id"], r["account_id"]) in seen or r["hero_id"] not in G.heroes:
                continue
            seen.add((r["match_id"], r["account_id"]))
            by_match[r["match_id"]].append(r)
    out = []
    for rows in by_match.values():
        for d in rows:
            if d["hero_id"] != INFERNUS:
                continue
            for x in rows:
                tx = next((b for i, b, _ in x["purchases"] if i == DISPEL), None)
                if x["won"] == d["won"] or tx is None:
                    continue
                t = tx + SETTLE_S
                xi = held_at(x, t)
                if t < min(d["duration_s"], x["duration_s"]) and DISPEL in xi:
                    out.append((held_at(d, t), x["hero_id"], xi))
    random.seed(7)
    return random.sample(out, min(n, len(out)))


def dealt(a, b, seed):
    e = Engine(rng=random.Random(seed), max_time=FIGHT_S)
    fa, fb = make_fighter(e, a, "A"), make_fighter(e, b, "B")
    fb.max_hp_base *= HP_MULT
    fb.hp = fb.max_hp
    r = e.run(fa, fb).a_dmg
    return r.get("Afterburn", 0.0), r.get("Napalm", 0.0)


def run(args):
    (di, xh, xi), badge = args
    a = Loadout("Infernus", di, skill=hero_default_skill("Infernus", badge=badge, counterplay=True))
    xsk = hero_default_skill(G.hero(xh).name, badge=badge, counterplay=True)
    res = {}
    for name, items, share in [("none", [i for i in xi if i != DISPEL], 0.0)] + [(str(s), xi, s) for s in SHARES]:
        b = Loadout(xh, items, skill=dataclasses.replace(xsk, dot_cleanse_share_buildup=share))
        v = [dealt(a, b, s) for s in range(SEEDS)]
        res[name] = [sum(x[0] for x in v) / SEEDS, sum(x[1] for x in v) / SEEDS]
    return res


def solve(grid, r):
    for (s0, r0), (s1, r1) in zip(grid, grid[1:]):
        if r1 <= r <= r0 and r0 > r1:
            return s0 + (r0 - r) / (r0 - r1) * (s1 - s0)
    return 0.0 if r > grid[0][1] else 1.0


def main():
    min_badge = int(sys.argv[1]) if len(sys.argv) > 1 else 91
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    real = json.load(open(os.path.join(ROOT, "counters", "work", f"cleanse_dispel_magic_{min_badge}.json")))
    g = real["by_dealer"]["Infernus"]["groups"]
    ab, na = g["Afterburn"], g["Napalm"]
    target = ab["ratio"] / na["ratio"]
    lo, hi = ab["ci90"][0] / na["ratio"], ab["ci90"][1] / na["ratio"]
    ps = pairs(min_badge, n, days)
    with Pool(os.cpu_count()) as p:
        rows = p.map(run, [(x, min_badge) for x in ps])
    base = [sum(r["none"][0] for r in rows), sum(r["none"][1] for r in rows)]

    def rel(key):
        return (sum(r[key][0] for r in rows) / base[0]) / (sum(r[key][1] for r in rows) / base[1])
    grid = [(s, rel(str(s))) for s in SHARES]
    out = {"min_badge": min_badge, "real_matches": real["matches"],
           "real_windows": real["by_dealer"]["Infernus"]["windows"],
           "real_afterburn_ratio": round(ab["ratio"], 3), "real_napalm_ratio": round(na["ratio"], 3),
           "real_gun_ratio": round(g["gun"]["ratio"], 3),
           "real_kill_ratio_vs_infernus": round(real["by_dealer"]["Infernus"]["kill_ratio"], 3),
           "target": round(target, 3), "target_90ci": [round(lo, 3), round(hi, 3)],
           "sim_pairs": len(rows), "sim_seeds": SEEDS, "fight_s": FIGHT_S,
           "sim_ratio_by_share": {str(s): round(r, 3) for s, r in grid},
           "fitted_share": round(solve(grid, target), 3),
           "fitted_share_90ci": [round(solve(grid, hi), 3), round(solve(grid, lo), 3)],
           "at_ceiling": target < grid[-1][1]}
    print(json.dumps(out, indent=1))
    os.makedirs(os.path.join(ROOT, "sim", "validation", "dispel"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "sim", "validation", "dispel", f"buildup_fit_{min_badge}.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
