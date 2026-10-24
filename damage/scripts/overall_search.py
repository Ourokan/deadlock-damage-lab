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
Movement (Tyler, 2026-10-21): the duel has no running (an escape would end it), so movement items are credited
outside it. The score is multiplied by each held item's value in sim/data/movement_value.json: the real Phantom+
chase (kill participation) x escape (deaths per 10 min) effect of holding it at the same hero, net worth and game
length (analysis/scripts/kill_participation.py, analysis/out/kill_participation.md), capped for 2 and 3+ items
at the measured value of holding that many (they overlap). A few items count as movement for one hero only
(hero_items: Mina imbues Mystic Expansion on Sanguine Retreat for a longer dash, Tyler 2026-10-21).
Sustain (2026-10-22, pro-play top items were mostly healing): the score is NET damage, damage dealt minus the
healing the enemy got during the fight (healing undoes damage; this is what makes Healbane's anti-heal count), and a
refill of the immortal enemy counts as a kill (Healbane's kill heal). Fights after the lane no longer start at full
health: the popular build arrives with the real Phantom+ spread of health at a fight start (sim/data/sustain.json
entry_deficit_q; half the fights start full), and a build that heals more in the gap_s seconds out of combat before
a fight arrives fuller in the fights that start short (entry_hp_start, scaled to real holders by fit_entry.py). Gap healing counts health regen, out-of-combat regen, Fortitude, heal pickups from medic troopers
(amped by Healing Booster) and the real out-of-fight rate of farm-heal items (Radiant Regeneration, Restorative Shot
on creeps, lifesteal on creeps...), all measured in sim/scripts/sustain/fit_sustain.py. Healing in the field also
saves trips back to the fountain (map_time: each item's real fountain saving on holders, TRIP_S).
Healbane's cut runs at the real heal-prevented rate (healbane_landing, sim/scripts/sustain/fit_healbane.py).
Not counted: team heals and team auras, vision, souls from farming (Monster Rounds), objective damage.

Real win edge (Tyler 2026-10-24, "blend win edge into score"): the score is also multiplied by
exp(WIN_K x the sum of the held items' real win edges on this hero) / the popular build's (win_value). Edge = win-rate
points vs other same-slot same-tier items, Ritualist+, matched and shrunk toward the item's all-hero edge
(analysis/out/hero_item_edge.json from analysis/scripts/build_win_check.py; a static snapshot). The 1v1 score alone
ranked items almost unrelated to real wins (r 0.05 over 16 heroes): Decay was in 119 of ~200 best builds while
losing 2-5 points on every hero, and team auras / AoE / death saves (Heroic Aura, Mystic Reverb, Cheat Death) were
never picked. Movement items already carry a real-data value (movement_value) and are left out of the blend.

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
import math
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
from deadsim.build import compute_stats  # noqa: E402
from survival import survive  # noqa: E402

MAX_TIME = 30.0
FOCUS = 2.0
_sk = {}
MOVE_PATH = os.path.join(ROOT, "..", "sim", "data", "movement_value.json")
_move = None


WIN_EDGE = os.path.join(ROOT, "..", "analysis", "out", "hero_item_edge.json")
# score factor per win-rate point of real edge: a +3 point item = x1.16, Decay on most heroes (-3.5) = x0.84, about
# the sim value Decay adds over a typical spirit item (~0.3-0.5 of the popular build's score at 27k)
WIN_K = 0.05
_win = None


def win_value(items, hero):
    """exp(WIN_K x sum of the held items' real per-hero win edges, in points); movement items left out (their real
    value is already in movement_value). 1.0 without data."""
    global _win
    if _win is None:
        try:
            d = json.load(open(WIN_EDGE))["heroes"]
        except (OSError, ValueError, KeyError):
            d = {}
        movement_value((), None)   # loads _move
        moving = _move[2] | {i for row in _move[3].values() for i in row}
        _win = {int(h): {int(i): v[0] for i, v in row.items() if int(i) not in moving} for h, row in d.items()}
    row = _win.get(int(hero), {})
    return math.exp(WIN_K * sum(row.get(i, 0.0) for i in set(items)))


def movement_value(items, hero=None):
    """Product of the held movement items' chase x escape values (1 = no movement item), capped by the measured
    value of holding that many movement items (stack_cap: they overlap, so two aren't worth the product).
    hero_items adds hero-specific movement items (Mina's Mystic Expansion on Sanguine Retreat), which count toward
    the stack cap like the others."""
    global _move
    if _move is None:
        g = S.G()
        with open(MOVE_PATH) as f:
            d = json.load(f)
        moving = set(d.get("movement_items", d["items"]))
        by_name = {it.name: i for i, it in g.items.items()}
        _move = ({i: d["items"][it.name] for i, it in g.items.items() if it.name in d["items"]},
                 {int(k): v for k, v in d.get("stack_cap", {}).items()},
                 {i for i, it in g.items.items() if it.name in moving},
                 {int(h): {by_name[n]: v for n, v in row.items() if n in by_name}
                  for h, row in d.get("hero_items", {}).items()})
    vals, caps, moving, hero_vals = _move
    extra = hero_vals.get(hero, {}) if hero is not None else {}
    held = set(items)
    v = 1.0
    for i in held:
        v *= extra.get(i, vals.get(i, 1.0))
    n = len(held & (moving | set(extra)))   # the caps were measured on any movement items held, weighted or not
    if n >= 2 and caps:
        v = min(v, caps[min(n, max(caps))])
    return v


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
        sk = hero_default_skill(S.G().hero(h).name, aim, badge=lo if lo > 0 else None, counterplay=True)
        # Healbane's anti-heal at the real heal-prevented rate (sim/data/sustain.json healbane_landing)
        _sk[h] = dataclasses.replace(sk, item_landing={**(sk.item_landing or {}),
                                                       "Healbane": sustain().get("healbane_landing", 1.0)})
    return _sk[h]


# each enemy hero gets a fixed spread-out point in the match (golden-ratio sequence), so long item cooldowns
# (Refresher 300 s...) are ready in their expected share of fights (deadsim engine.FIGHT_GAP)
PHASES = {}


def _phases():
    for k, h in enumerate(sorted(S.G().heroes)):
        PHASES[h] = ((k + 1) * 0.6180339887) % 1.0


def net_damage(r):
    """Damage dealt minus the healing the enemy got: healing undoes damage (Healbane, enemy lifesteal...)."""
    return max(0.0, r["damage_dealt"] - r.get("enemy_healed", 0.0))


def fight(h, items, oh, oitems, souls, phase=None, start_hp=None):
    sk = dataclasses.replace(skill(h), fight_phase=phase)
    esk = dataclasses.replace(skill(oh), fight_phase=None if phase is None else (phase + 0.5) % 1.0)
    r = survive(h, items, souls, oh, oitems, max_time=MAX_TIME, focus=FOCUS, skill=sk, enemy_skill=esk,
                start_hp=start_hp)
    return net_damage(r), r["time_alive"], r["survived"]


# Laning phase (Tyler, 2026-10-21: "in laning phase regen and other sources of healing can be more valuable than pure
# hp"). One 30 s fight never lets regen pay off, so the early game_path stages are scored as a lane instead: up to
# LANE_TRADES 1v1 trades of TRADE_S s (enemy focus 1), health carried from one trade to the next. Between trades
# (TRADE_GAP s) the hero heals its health regen the whole gap, out-of-combat regen after OOC_DELAY s and Fortitude's
# % of max health after its RestoreDelay (all amped by regen amp). Below BACK_FRAC health before a trade the hero
# backs (the rest of the lane is lost), and a death ends it too. Score = damage dealt over the whole lane.
# The trade length, gap and delay are assumptions, not fitted to replays.
LANE_TRADES = 5
TRADE_S = 4.0
TRADE_GAP = 25.0
OOC_DELAY = 10.0
BACK_FRAC = 0.25
LANE_FOCUS = 1.0


SUSTAIN_PATH = os.path.join(ROOT, "..", "sim", "data", "sustain.json")
_sustain = None


def sustain():
    """Real Phantom+ sustain inputs (sim/scripts/sustain/fit_sustain.py): heal pickups and farm-heal item rates per
    minute, fight entry health and the time out of combat before a fight, per phase (lane / mid / late)."""
    global _sustain
    if _sustain is None:
        with open(SUSTAIN_PATH) as f:
            _sustain = json.load(f)
    return _sustain


def game_phase(souls):
    """Phase of the real data a net worth falls in: lane ends ~9 min (~10k), late from ~25 min (~30k)."""
    return "lane" if souls < 10000 else "mid" if souls <= 27000 else "late"


def gap_heal(r, items, gap=TRADE_GAP, phase="lane"):
    """Health healed in `gap` s out of hero combat by the build of survive() result r (or build_stats()): health
    regen the whole gap, out-of-combat regen after OOC_DELAY, Fortitude after its RestoreDelay (scaled to real
    holders, fortitude_heal_scale: creeps and troopers reset it), medic trooper heal
    pickups (all amped by regen amp, so Healing Booster counts) and the real rate of farm-heal items (Radiant
    Regeneration, Restorative Shot on creeps, lifesteal on creeps..., amped by outgoing healing amp)."""
    amp = 1.0 + (r.get("regen_amp") or 0.0)
    h = r["regen"] * gap + r["ooc_regen"] * max(0.0, gap - OOC_DELAY)
    sus = sustain()
    h += sus["pickup_hp_per_min"][phase] / 60 * gap
    g = S.G()
    farm = 0.0
    for i in items:
        it = g.items[i]
        if it.class_name == "upgrade_chonky":    # Fortitude
            h += r["max_hp"] * it.props.get("HealLifePercentOutOfCombat", 0) / 100 \
                * max(0.0, gap - it.props.get("RestoreDelay", 10)) * sus.get("fortitude_heal_scale", {}).get(phase, 1.0)
        rate = sus["farm_heal_hp_per_min"].get(it.name)
        if rate:
            farm += rate[phase] / 60 * gap
    return h * amp + farm * (1.0 + (r.get("heal_amp_cast") or 0.0))


_stats = {}


def build_stats(h, items, souls):
    """The gap_heal inputs of a build without fighting."""
    key = (h, tuple(sorted(items)), souls)
    if key not in _stats:
        g = S.G()
        st = compute_stats(g.hero(h), [g.items[i] for i in key[1]], souls=souls)
        _stats[key] = {"regen": st.health_regen, "ooc_regen": st.ooc_regen, "regen_amp": st.heal_amp,
                       "heal_amp_cast": st.heal_amp_cast, "max_hp": st.max_health}
    return _stats[key]


# Trips back to base (2026-10-22): healing in the field saves fountain trips, so more time on the map. Real Phantom+
# holders of field-heal items heal less at the fountain than non-holders (matched hero x phase x net worth, each item
# shrunk toward the pooled pass-through, sim/scripts/sustain/fit_sustain.py fountain_saved_hp_per_min: Fortitude ~59
# HP/min, Healing Booster ~16, lifesteal 10-20). The popular build makes the real number of heal trips
# (heal_trips_per_min, ~2 per 10 min mid game); a build makes fewer when its items save fountain healing and when
# more max health makes each trip go further. A trip costs TRIP_S s (assumption).
TRIP_S = 40.0


def field_saving(items, ph):
    """Fountain healing per minute a build's field-heal items save (real holders vs non-holders)."""
    saved = sustain()["fountain_saved_hp_per_min"]
    g = S.G()
    return sum(saved.get(g.items[i].name, {}).get(ph, 0.0) for i in items)


def map_time(h, items, souls, pop):
    """Share of time on the map (not walking back to heal) of a build, the popular build making the real number of
    heal trips. Each HP/min of fountain healing a build saves over the popular build cuts the same share of the real
    fountain healing's trips (not of the popular build's: a popular build that already heals in the field must not
    make every further heal item worth more). Lane stages: 1 (the lane test already scores staying in lane)."""
    ph = game_phase(souls)
    sus = sustain()
    if ph == "lane" or not sus.get("heal_trips_per_min"):
        return 1.0
    f = sus["fountain_hp_per_min"][ph]
    need = max(0.0, f - (field_saving(items, ph) - field_saving(pop, ph)))
    trips = sus["heal_trips_per_min"][ph] * need / max(1.0, f) \
        * build_stats(h, pop, souls)["max_hp"] / build_stats(h, items, souls)["max_hp"]
    return max(0.1, 1.0 - trips * TRIP_S / 60.0)   # floor: a build always spends some time on the map


def entry_deficit(h, pop, souls):
    """Chip damage carried into a fight by the popular build, per quantile of the real entry health spread (half the
    fights start at full health), and the popular build's gap healing: the popular build arrives with the real entry
    health spread after healing for the real time out of combat before a fight."""
    ph = game_phase(souls)
    sus = sustain()
    r = build_stats(h, pop, souls)
    return [d * r["max_hp"] for d in sus["entry_deficit_q"][ph]], gap_heal(r, pop, sus["gap_s"][ph], ph)


def entry_hp_start(h, items, souls, deficit):
    """Mean health a build starts a fight with: max health minus the chip damage its gap healing didn't cover. More
    gap healing than the popular build's only helps in the fights that start short of full health; less costs in
    all of them. The difference is scaled to real item holders' entry health (entry_heal_scale,
    sim/scripts/sustain/fit_entry.py)."""
    ph = game_phase(souls)
    r = build_stats(h, items, souls)
    qs, pop_heal = deficit
    sus = sustain()
    extra = (gap_heal(r, items, sus["gap_s"][ph], ph) - pop_heal) * sus.get("entry_heal_scale", {}).get(ph, 1.0)
    return r["max_hp"] - sum(max(0.0, d - extra) for d in qs) / len(qs)


def healbane_gap_share(items, gap=TRADE_GAP):
    """Share of the enemy's gap healing left when the build holds Healbane (its debuff from the trade's last spirit
    hit covers the first AbilityDuration s of the gap)."""
    g = S.G()
    for i in items:
        it = g.items[i]
        if it.class_name == "upgrade_healbane":
            cut = abs(it.props.get("HealAmpReceivePenaltyPercent", 0)) / 100 * sustain().get("healbane_landing", 1.0)
            return 1.0 - cut * min(gap, it.props.get("AbilityDuration", 8)) / gap
    return 1.0


def lane_fight(h, items, oh, oitems, souls, phase=None, start_hp=None):
    """Net damage over a lane of trades, total time alive, share of the trades played (1 = lasted the lane).
    Both sides carry health between trades and heal in the gaps (gap_heal; Healbane cuts the enemy's). Each trade
    scores the damage dealt minus the enemy's healing in it. An enemy that dies (refills) or starts a trade below
    BACK_FRAC health has to back: the trades left count at this build's mean trade so far (the lane is free), so
    lane pressure, enemy sustain and anti-heal all count. start_hp is unused (the lane starts full)."""
    sk = dataclasses.replace(skill(h), fight_phase=phase)
    esk = dataclasses.replace(skill(oh), fight_phase=None if phase is None else (phase + 0.5) % 1.0)
    hp, ehp, dmg, t = None, None, 0.0, 0.0
    hb = healbane_gap_share(items)
    for k in range(LANE_TRADES):
        r = survive(h, items, souls, oh, oitems, max_time=TRADE_S, focus=LANE_FOCUS, skill=sk, enemy_skill=esk,
                    start_hp=hp, enemy_start_hp=ehp)
        dmg += net_damage(r)
        t += r["time_alive"]
        if not r["survived"]:
            return dmg, t, k / LANE_TRADES
        hp = min(r["max_hp"], r["final_hp"] + gap_heal(r, items))
        if "enemy" in r:
            emax = r["enemy_max_hp"]
            ehp = min(emax, r["enemy_final_hp"] + gap_heal(r["enemy"], oitems) * hb)
            if k + 1 < LANE_TRADES and (r["enemy_kills"] or ehp < BACK_FRAC * emax):
                left = LANE_TRADES - k - 1
                return dmg * (1 + left / (k + 1)), t + left * TRADE_S, 1.0
        if k + 1 < LANE_TRADES and hp < BACK_FRAC * r["max_hp"]:
            return dmg, t, (k + 1) / LANE_TRADES
    return dmg, t, 1.0


class Evaluator:
    """Drop-in for search.Evaluator: score = weighted mean damage before death / the popular build's."""
    fight = staticmethod(fight)

    def __init__(self, hero, budget, pools):
        self.h, self.souls, self.pools = hero, budget, pools
        self.cache = {}
        self.fights = 0
        self.norm = {}
        pop = tuple(sorted(S.popular_build(hero, S.item_budget(budget), pools)))
        self.deficit = entry_deficit(hero, pop, budget)
        self.pop = pop
        self.map_pop = map_time(hero, pop, budget, pop)
        for pool in ("S", "F", "F2"):
            self.norm[pool] = max(1.0, self._mean(self._rows(pop, pool), 2)) * movement_value(pop, hero) \
                * self._map(pop) * win_value(pop, hero)

    def _rows(self, items, pool):
        key = (tuple(sorted(items)), pool)
        if key not in self.cache:
            rows = []
            start = entry_hp_start(self.h, key[0], self.souls, self.deficit)
            for k, (oh, oitems, w) in enumerate(self.pools[pool]):
                d, t, alive = self.fight(self.h, key[0], oh, oitems, self.souls, phase=PHASES[oh], start_hp=start)
                rows.append((oh, w, d, t, alive))
                self.fights += 1
            self.cache[key] = rows
        return self.cache[key]

    def _map(self, items):
        """map_time relative to the popular build (lane stages: 1, the lane test already scores staying in lane)."""
        return map_time(self.h, items, self.souls, self.pop) / self.map_pop

    @staticmethod
    def _mean(rows, k):
        tw = sum(r[1] for r in rows)
        return sum(r[1] * float(r[k]) for r in rows) / tw

    def run(self, items, pool="F", detail=False):
        rows = self._rows(items, pool)
        dmg = self._mean(rows, 2)
        move = movement_value(items, self.h)
        mt = self._map(items)
        win = win_value(items, self.h)
        score = dmg * move * mt * win / self.norm[pool]
        if not detail:
            return score
        t = self._mean(rows, 3)
        return {
            "score": round(score, 4),
            "damage_before_death": round(dmg, 1),   # net of the enemy's healing
            "entry_hp": round(entry_hp_start(self.h, items, self.souls, self.deficit)),
            "time_alive_s": round(t, 2),
            "survived_30s": round(self._mean(rows, 4), 4),
            "dps_while_alive": round(dmg / max(0.1, t), 1),
            "movement_value": round(move, 4),
            "map_time": round(mt, 4),   # time on the map vs the popular build (fewer heal trips)
            "win_value": round(win, 4),  # real win-edge factor (win_value), before dividing by the popular build's
            "matchups": {str(r[0]): [round(r[2]), round(r[3], 2)] for r in rows},
        }


class LaneEvaluator(Evaluator):
    """Evaluator for the laning phase: damage over a lane of trades (lane_fight) / the popular build's."""
    fight = staticmethod(lane_fight)

    def run(self, items, pool="F", detail=False):
        d = super().run(items, pool, detail)
        if detail:
            d["mode"] = "lane"
            d["lane_share"] = d.pop("survived_30s")   # share of the lane's trades played before backing or dying
            d["trades"] = LANE_TRADES
        return d


class MixEvaluator:
    """End of the laning phase: score = LANE_WEIGHT x lane score + the rest x the overall fight score."""

    def __init__(self, hero, budget, pools, lane_weight=0.5):
        self.lane, self.fight = LaneEvaluator(hero, budget, pools), Evaluator(hero, budget, pools)
        self.w = lane_weight

    @property
    def fights(self):
        return self.lane.fights + self.fight.fights

    def run(self, items, pool="F", detail=False):
        if not detail:
            return self.w * self.lane.run(items, pool) + (1 - self.w) * self.fight.run(items, pool)
        d = self.fight.run(items, pool, True)
        lane = self.lane.run(items, pool, True)
        d["fight_score"] = d["score"]
        d["score"] = round(self.w * lane["score"] + (1 - self.w) * d["score"], 4)
        d["mode"] = "mix"
        d["lane_weight"] = self.w
        d["lane"] = {k: v for k, v in lane.items() if k != "matchups"}
        return d


def job(args):
    hero, budget = args
    path = os.path.join(JOBS, f"{hero}_{budget}.json")
    if os.path.exists(path):
        return path, "skip"
    lines = []
    res = S.search(hero, budget, log=lines.append)
    res.update({"log": lines, "objective": "overall", "movement": True, "bracket": S.BRACKET, "aim": BRACKETS[S.BRACKET][2], "focus": FOCUS, "max_time": MAX_TIME, "counterplay": True})
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
