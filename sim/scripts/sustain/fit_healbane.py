"""Scale Healbane's anti-heal in the overall score to the real rate: sim heal prevented per second alive (popular
build + Healbane vs popular, typical real enemies, 30 s overall fights, Healbane at full strength) against real
Phantom+ holders' heal prevented per second in hero combat (sustain.json healbane_prevented_per_combat_s, from
fit_sustain.py). Writes healbane_landing = real / sim into sim/data/sustain.json.

Refit order (not run by CI, sim/data/sustain.json is a static snapshot): fit_sustain.py, then this script.
usage (repo root, search/work pools built): python3 sim/scripts/sustain/fit_healbane.py [--workers 4]
"""
import argparse
import dataclasses
import json
import os
import sys
from multiprocessing import Pool

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "damage", "scripts"))
import game_path as GP  # noqa: E402
import overall_search as O  # noqa: E402

S = O.S
HEROES = ("Haze", "Abrams", "Seven", "Infernus", "Lash", "Wraith", "Bebop", "Pocket")
BUDGETS = (18000, 27000)


def full(h):
    sk = O.skill(h)
    return dataclasses.replace(sk, item_landing={**(sk.item_landing or {}), "Healbane": 1.0})


def prevented(args):
    hero, b = args
    h = S.G().hero(hero).id
    pools = S.load_pools(b)
    hb_id = S.G().item("Healbane").id
    pop = [i for i in S.popular_build(h, GP.item_budget(b), pools) if i != hb_id]
    hb = GP.with_item(pop, hb_id)
    prev = t = 0.0
    for oh, oit, w in pools["F"]:
        kw = dict(max_time=O.MAX_TIME, focus=O.FOCUS, skill=full(h), enemy_skill=full(oh))
        a = O.survive(h, pop, b, oh, oit, **kw)
        c = O.survive(h, hb, b, oh, oit, **kw)
        prev += w * (a["enemy_healed"] - c["enemy_healed"])
        t += w * c["time_alive"]
    return prev / t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    with Pool(a.workers) as p:
        rates = p.map(prevented, [(h, b) for h in HEROES for b in BUDGETS])
    sim = sum(rates) / len(rates)
    with open(O.SUSTAIN_PATH) as f:
        sus = json.load(f)
    sus["healbane_sim_prevented_per_s"] = round(sim, 2)
    sus["healbane_landing"] = round(min(1.0, sus["healbane_prevented_per_combat_s"] / sim), 3)
    sus["healbane_landing_real"] = sus["healbane_prevented_per_combat_s"]   # fit_sustain drops a stale landing
    with open(O.SUSTAIN_PATH, "w") as f:
        json.dump(sus, f, indent=1)
    print(f"sim {sim:.2f} HP/s prevented vs real {sus['healbane_prevented_per_combat_s']} -> "
          f"healbane_landing {sus['healbane_landing']}")


if __name__ == "__main__":
    main()
