"""Overall build search: the builds that deal the most damage before dying, against real enemy builds that
fight back, with counterplay on.

Tyler asked (2026-10-16) for best overall builds, not pure dummy damage: survivability (vitality items and the
vitality investment spike), utility that changes a fight (stuns, silences, disarms, slows, cleanses, heals) and
how easily an item is countered must all count. One number captures them inside the sim:

    overall = damage this build deals to the enemy before it dies (30 s cap)

averaged over the 41 typical real enemy builds at the same net worth (search/ "F" pool, weighted by how often each
hero reaches that worth). The enemy never dies (it refills, like the dummy) and its damage is x FOCUS: at 2 the
popular builds' median time alive is ~14 s, close to the real median time to kill (~13 s). So:
- more health / resist / lifesteal = longer alive = more damage dealt (vitality spikes count);
- CC and debuffs on the enemy (stun, silence, disarm, slow, Healbane...) count when they cut its damage;
- the enemy plays its real build: its resists, its Dispel Magic (cleanses Decay/Toxic Bullets), its Metal Skin;
- counterplay (deadsim accuracy.hero_default_skill(counterplay=True)): targets walk out of Alchemical Fire after
  2 s (1.5 s from Ascendant), and items whose own damage the 1v1 sim over-predicts versus real matches are scaled
  down (data/item_landing.json: Mercurial Magnum 0.18, Focus Lens 0.37, Toxic Bullets 0.53, Mystic Shot 0.76...),
  and active items with cooldowns over 60 s (Refresher...) are ready only in their expected share of fights.
Not counted: movement (escape, chase, mobility items), team heals and team auras, vision.

Scores are relative to the hero's most popular real build (1.0 = popular). Same search machinery as the duel search
(search/scripts/search.py: screen on 16 enemies, confirm on 41, up to 8 rounds, same budget rules).

Rank bracket (--bracket, default build_pool.PRIMARY = phantom): the enemy builds come from that bracket's pools and
both sides use its aim percentile and its lowest badge (Alchemical Fire walk-out time, Dispel Magic timing).

usage: python3 scripts/overall_search.py [--workers 4] [--heroes Haze] [--budgets 27000] [--bracket phantom]
Writes work/jobs_overall_<bracket>/<hero_id>_<budget>.json (resumes); scripts/export_overall.py builds out/overall.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "..", "sim"))
sys.path.insert(0, os.path.join(ROOT, "..", "search", "scripts"))
sys.path.insert(0, os.path.join(ROOT, "..", "survival"))

import search as S  # noqa: E402
from build_pool import BRACKETS, BUDGETS, PRIMARY  # noqa: E402
from deadsim.accuracy import hero_default_skill  # noqa: E402
from survival import survive  # noqa: E402

MAX_TIME = 30.0
FOCUS = 2.0
_sk = {}


def jobs_dir(bracket):
    return os.path.join(ROOT, "work", "jobs_overall_" + bracket)


def set_bracket(bracket):
    global JOBS
    S.BRACKET, JOBS = bracket, jobs_dir(bracket)
    _sk.clear()


set_bracket(PRIMARY)


def skill(h):
    if h not in _sk:
        lo, _, aim, _ = BRACKETS[S.BRACKET]
        _sk[h] = hero_default_skill(S.G().hero(h).name, aim, badge=lo if lo > 0 else None, counterplay=True)
    return _sk[h]


# each enemy hero gets a fixed spread-out point in the match (golden-ratio sequence), so long item cooldowns
# (Refresher 300 s...) are ready in their expected share of fights (deadsim engine.FIGHT_GAP)
PHASES = {}


def _phases():
    for k, h in enumerate(sorted(S.G().heroes)):
        PHASES[h] = ((k + 1) * 0.6180339887) % 1.0


def fight(h, items, oh, oitems, souls, phase=None):
    sk = dataclasses.replace(skill(h), fight_phase=phase)
    esk = dataclasses.replace(skill(oh), fight_phase=None if phase is None else (phase + 0.5) % 1.0)
    r = survive(h, items, souls, oh, oitems, max_time=MAX_TIME, focus=FOCUS, skill=sk, enemy_skill=esk)
    return r["damage_dealt"], r["time_alive"], r["survived"]


class Evaluator:
    """Drop-in for search.Evaluator: score = weighted mean damage before death / the popular build's."""

    def __init__(self, hero, budget, pools):
        self.h, self.souls, self.pools = hero, budget, pools
        self.cache = {}
        self.fights = 0
        self.norm = {}
        pop = tuple(sorted(S.popular_build(hero, S.item_budget(budget), pools)))
        for pool in ("S", "F", "F2"):
            self.norm[pool] = max(1.0, self._mean(self._rows(pop, pool), 2))

    def _rows(self, items, pool):
        key = (tuple(sorted(items)), pool)
        if key not in self.cache:
            rows = []
            for k, (oh, oitems, w) in enumerate(self.pools[pool]):
                d, t, alive = fight(self.h, key[0], oh, oitems, self.souls, phase=PHASES[oh])
                rows.append((oh, w, d, t, alive))
                self.fights += 1
            self.cache[key] = rows
        return self.cache[key]

    @staticmethod
    def _mean(rows, k):
        tw = sum(r[1] for r in rows)
        return sum(r[1] * float(r[k]) for r in rows) / tw

    def run(self, items, pool="F", detail=False):
        rows = self._rows(items, pool)
        dmg = self._mean(rows, 2)
        score = dmg / self.norm[pool]
        if not detail:
            return score
        t = self._mean(rows, 3)
        return {
            "score": round(score, 4),
            "damage_before_death": round(dmg, 1),
            "time_alive_s": round(t, 2),
            "survived_30s": round(self._mean(rows, 4), 4),
            "dps_while_alive": round(dmg / max(0.1, t), 1),
            "matchups": {str(r[0]): [round(r[2]), round(r[3], 2)] for r in rows},
        }


def job(args):
    hero, budget = args
    path = os.path.join(JOBS, f"{hero}_{budget}.json")
    if os.path.exists(path):
        return path, "skip"
    lines = []
    res = S.search(hero, budget, log=lines.append)
    res.update({"log": lines, "objective": "overall", "bracket": S.BRACKET, "aim": BRACKETS[S.BRACKET][2], "focus": FOCUS, "max_time": MAX_TIME, "counterplay": True})
    json.dump(res, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    b, p = res["builds"][0]["F"], res["popular"]["F"]
    return path, (f"{res['hero']} {budget}: dmg before death {b['damage_before_death']:.0f} vs popular "
                  f"{p['damage_before_death']:.0f}, alive {b['time_alive_s']}s vs {p['time_alive_s']}s "
                  f"({res['fights']} fights, {res['seconds']}s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--heroes", default="")
    ap.add_argument("--budgets", default="")
    ap.add_argument("--bracket", default=PRIMARY, choices=list(BRACKETS))
    a = ap.parse_args()
    set_bracket(a.bracket)
    S.Evaluator = Evaluator
    S.MIN_GAIN = 0.004
    _phases()
    g = S.G()
    heroes = [g.hero(int(h) if h.isdigit() else h).id for h in a.heroes.split(",") if h] or sorted(g.heroes)
    budgets = [int(b) for b in a.budgets.split(",") if b] or [27000, 18000, 37000, 10000, 50000]
    os.makedirs(JOBS, exist_ok=True)
    jobs = [(h, b) for b in budgets for h in heroes]
    with Pool(a.workers) as p:
        for path, msg in p.imap_unordered(job, jobs):
            print(time.strftime("%H:%M:%S"), msg, flush=True)


if __name__ == "__main__":
    S.Evaluator = Evaluator
    main()
