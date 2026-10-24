"""Fit Counterspell's spell parry rates (Skill.spell_parry_rate for enemy non-ultimate aimed casts,
Skill.spell_parry_rate_ult for ultimates) to real ability damage taken by Counterspell holders.

Real side: counters/scripts/cleanse_real.py Counterspell -> counters/work/cleanse_counterspell_<badge>.json: in one
3-minute damage-matrix window from one enemy dealer, ability damage (per max HP) taken by holders / by teammates who
haven't bought it, separately for the dealer's ultimate and other abilities. Counterspell does nothing against guns,
so the gun ratio of the same pairs is the control for who gets targeted (holders are different heroes and play
differently): target = ability ratio / gun ratio.

Sim side, as fit_dispel.py: real (enemy, Counterspell holder) item snapshots from the same matches (holder's items
SETTLE_S after buying it), dueled 30 s at the bracket's aim with counterplay on; the holder has HP_MULT x health so
the window is fixed, as in the real comparison. ratio(r, r_ult) = enemy ability damage to the holder at those rates /
to the same holder with Counterspell but no parry, each per the holder's max HP like the real side (without that,
%-health abilities such as Soul Exchange dominate at HP_MULT x health, and Counterspell's +50 HP x HP_MULT with them). Then the 2-d grid is interpolated to
meet both real targets.

usage (repo root, player_builds linked or PLAYER_BUILDS set): python3 sim/scripts/fit_counterspell.py [min_badge] [n_pairs] [days]
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
CS = G.item("Counterspell").id
RATES = (0.0, 0.05, 0.1, 0.2, 0.4)
RATES_ULT = (0.0, 0.25, 0.5, 0.75, 1.0)
SEEDS = 3
SETTLE_S = 120
HP_MULT = 50.0
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
        for x in rows:
            tx = next((b for i, b, _ in x["purchases"] if i == CS), None)
            if tx is None:
                continue
            t = tx + SETTLE_S
            xi = held_at(x, t)
            if t >= x["duration_s"] or CS not in xi:
                continue
            for d in rows:
                if d is not x and d["won"] != x["won"]:   # enemy team
                    out.append((d["hero_id"], held_at(d, t), x["hero_id"], xi))
    random.seed(7)
    return random.sample(out, min(n, len(out)))


def ability_dmg(a, b, seed, ult_names):
    e = Engine(rng=random.Random(seed))
    fa, fb = make_fighter(e, a, "A"), make_fighter(e, b, "B")
    fb.max_hp_base *= HP_MULT
    fb.hp = fb.max_hp
    r = e.run(fa, fb)
    ult = non = 0.0
    for k, v in r.a_dmg.items():
        if any(k.startswith(n) for n in ult_names):
            ult += v
        elif any(k.startswith(n) for n in ab_names(a.hero)):
            non += v
    return non / fb.max_hp, ult / fb.max_hp   # per max HP, as the real side: %-health abilities scale with HP_MULT


def ab_names(hero, ult=None):
    return [x.name for x in G.hero(hero).abilities if ult is None or bool(x.ultimate) == ult]


def run(args):
    (dh, di, xh, xi), badge = args
    dn, xn = G.hero(dh).name, G.hero(xh).name
    a = Loadout(dn, di, skill=hero_default_skill(dn, badge=badge, counterplay=True))
    xsk = hero_default_skill(xn, badge=badge, counterplay=True)
    ult_names = ab_names(dn, True)
    res = {}
    arms = [("none", [i for i in xi if i != CS], 0.0, 0.0)] + [
        (f"{r}|{u}", xi, r, u) for r in RATES for u in RATES_ULT]
    for name, items, r, u in arms:
        b = Loadout(xn, items, skill=dataclasses.replace(xsk, spell_parry_rate=r, spell_parry_rate_ult=u))
        tot = [0.0, 0.0]
        for s in range(SEEDS):
            n, ul = ability_dmg(a, b, s, ult_names)
            tot[0] += n / SEEDS
            tot[1] += ul / SEEDS
        res[name] = tot
    return res


def interp(xs, ys, y):
    """x where the falling curve ys(xs) meets y, clipped to the grid."""
    for x0, x1, y0, y1 in zip(xs, xs[1:], ys, ys[1:]):
        if y1 <= y <= y0 and y0 > y1:
            return x0 + (y0 - y) / (y0 - y1) * (x1 - x0)
    return xs[0] if y > ys[0] else xs[-1]


def main():
    min_badge = int(sys.argv[1]) if len(sys.argv) > 1 else 91
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    real = json.load(open(os.path.join(ROOT, "counters", "work", f"cleanse_counterspell_{min_badge}.json")))
    g = real["by_dealer"]["any"]["groups"]
    gun = g["gun"]["ratio"]
    tgt = {"non": g["abilities:non-ult"]["ratio"] / gun, "ult": g["abilities:ult"]["ratio"] / gun}
    tgt_ci = {"non": [x / gun for x in g["abilities:non-ult"]["ci90"]], "ult": [x / gun for x in g["abilities:ult"]["ci90"]]}
    ps = pairs(min_badge, n, days)
    with Pool(os.cpu_count()) as p:
        rows = p.map(run, [(x, min_badge) for x in ps])
    # against the item held with no parry at all: holding it already changes the fixed-window duel (the holder's
    # spirit power and HP shorten or lengthen the fight; 0.90 / 1.07 of no item in the first fit), which the real
    # side's gun control removes too. "none" is kept for reference.
    none = [sum(r["none"][0] for r in rows), sum(r["none"][1] for r in rows)]
    base = [sum(r["0.0|0.0"][0] for r in rows), sum(r["0.0|0.0"][1] for r in rows)]
    grid = {(r, u): (sum(x[f"{r}|{u}"][0] for x in rows) / base[0], sum(x[f"{r}|{u}"][1] for x in rows) / base[1])
            for r in RATES for u in RATES_ULT}
    # alternate: non-ult rate given the ult rate, ult rate given the non-ult rate (bilinear on the grid)

    def at(r, u):
        def lin(xs, x):
            for i in range(len(xs) - 1):
                if xs[i] <= x <= xs[i + 1]:
                    return i, (x - xs[i]) / (xs[i + 1] - xs[i])
            return len(xs) - 2, 1.0
        i, fr = lin(RATES, r)
        j, fu = lin(RATES_ULT, u)
        out = []
        for k in (0, 1):
            v00, v10 = grid[(RATES[i], RATES_ULT[j])][k], grid[(RATES[i + 1], RATES_ULT[j])][k]
            v01, v11 = grid[(RATES[i], RATES_ULT[j + 1])][k], grid[(RATES[i + 1], RATES_ULT[j + 1])][k]
            out.append((v00 * (1 - fr) + v10 * fr) * (1 - fu) + (v01 * (1 - fr) + v11 * fr) * fu)
        return out

    def fit(tn, tu):
        r, u = 0.05, 0.25
        for _ in range(30):
            fine_r = [RATES[0] + (RATES[-1] - RATES[0]) * k / 200 for k in range(201)]
            r = interp(fine_r, [at(x, u)[0] for x in fine_r], tn)
            fine_u = [k / 200 for k in range(201)]
            u = interp(fine_u, [at(r, x)[1] for x in fine_u], tu)
        return round(r, 3), round(u, 3)

    r, u = fit(tgt["non"], tgt["ult"])
    lo = fit(tgt_ci["non"][1], tgt_ci["ult"][1])
    hi = fit(tgt_ci["non"][0], tgt_ci["ult"][0])
    out = {"min_badge": min_badge, "real_matches": real["matches"],
           "real_ratio": {"gun": round(gun, 3), "non_ult": round(g["abilities:non-ult"]["ratio"], 3),
                          "ult": round(g["abilities:ult"]["ratio"], 3)},
           "real_ratio_90ci": {"gun": g["gun"]["ci90"], "non_ult": g["abilities:non-ult"]["ci90"], "ult": g["abilities:ult"]["ci90"]},
           "target_vs_gun": {k: round(v, 3) for k, v in tgt.items()},
           "sim_pairs": len(rows), "sim_seeds": SEEDS,
           "sim_item_no_parry_vs_none": [round(base[0] / none[0], 3), round(base[1] / none[1], 3)],
           "sim_ratio": {f"{r_}|{u_}": [round(a, 3), round(b, 3)] for (r_, u_), (a, b) in grid.items()},
           "fitted_rate": r, "fitted_rate_ult": u,
           "fitted_rate_90ci": [lo[0], hi[0]], "fitted_rate_ult_90ci": [lo[1], hi[1]],
           "sim_ratio_at_fit": [round(x, 3) for x in at(r, u)],
           # a target above the zero-rate ratio clips to rate 0: then the fit and its CI are the grid floor
           "at_floor": [tgt["non"] >= at(0.0, u)[0], tgt["ult"] >= at(r, 0.0)[1]]}
    print(json.dumps({k: v for k, v in out.items() if k != "sim_ratio"}, indent=1))
    os.makedirs(os.path.join(ROOT, "sim", "validation", "counterspell"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "sim", "validation", "counterspell", f"fit_{min_badge}.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
