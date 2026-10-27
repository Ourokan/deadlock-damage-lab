"""Overall build search: the builds that deal the most damage before dying, against real enemy builds that
fight back, with counterplay on.

Tyler asked (2026-10-16) for best overall builds, not pure dummy damage: survivability (vitality items and the
vitality investment spike), utility that changes a fight (stuns, silences, disarms, slows, cleanses, heals) and
how easily an item is countered must all count. One number captures them inside the sim:

    overall = damage this build deals to the enemy before it dies (30 s cap), each hit x P(a real fight is still
              going at its time)

averaged over the 41 typical real enemy builds at the same net worth (search/ "F" pool, weighted by how often each
hero reaches that worth). The enemy never dies (it refills, like the dummy) and its damage is x FOCUS: at 2 the
popular builds' median time alive is ~14 s, close to the real median time to kill (~13 s). So:
- more health / resist / lifesteal = longer alive = more damage dealt (vitality spikes count);
- fight length (2026-10-24): real Phantom+ fights between two heroes mostly end in a disengage, not a death (84% of
  66.7k fights in 260 replays; disengage median 7.5 s, mean 9 s to 30 s; sim/scripts/fight_length/fit_length.py), so
  a hit at t s counts x P(the two are still trading at t | nobody died) (deadsim.mechanics.real_length for the
  build's game phase, survive(fight_length=)). The ability and item landing factors carry a matching length_corr
  (sim/scripts/fight_length/length_factors.py). An opener counts in full, the 25th second of a fight ~1/50, so
  living past ~15 s or ramping for 20 s is worth less than in a 30 s fight to the death. Lane trades (lane_fight)
  keep their own 4 s model;
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
(hero_items: Mina imbues Mystic Expansion on Sanguine Retreat for a longer dash, Tyler 2026-10-21). Stalker's speed
procs only on weapon hits within 8 m (close_items): its gain is scaled by the hero's reach share at its real median
fight distance over the measured holders' (mostly close heroes), so far heroes like Vindicta (x0.25) get little of it
(Tyler 2026-10-25: Vindicta was recommended Stalker).
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
Team value (2026-10-24, the real win check found Heroic Aura, Mystic Reverb... never picked while winning): real
Phantom+ fights are rarely 1v1 (sim/data/team_value.json "positions", fit from 1 s match positions by
sim/scripts/team/fit_team.py: at 27k a fighting hero has 1.5 teammates within 35 m and 0.4 other enemies within 16 m
of its target). So
- area items also hit the other enemies near their centre: their damage in the duel x their real extra hits on other
  heroes per hit on the main target is added to the damage dealt (AREA_ITEMS; deadsim.mechanics.area_extra, measured
  from 260 Phantom+ replays' damage events by sim/scripts/team/area_hits.py: Mystic Reverb 0.99, Alchemical Fire
  0.94, Scourge 0.62, Torment Pulse 0.48, Capacitor 0.26, Cold Front 0.19, Arctic Blast 0.18, Tesla Bullets 0.07
  pooled over whole matches). Those extra hits grow with net worth (lane trades early, team fights late): area_damage
  uses them at the build's souls, one replay-fitted curve for every area item (0.2x the pooled value at <=7.5k, 0.5x
  at 10k, 0.95x at 18k, 1.1x from 22k; data/area_hits.json "phase"), so early Cold Front / Capacitor builds no longer
  get late-game team fight value. The position count (other enemies within the radius of the target or holder at 1 s samples) is the fallback; it gave
  Torment Pulse and Scourge ~0.06, since most position fight seconds are approach and poke at 15-20 m; Ricochet and
  Split Shot hit them through the duel's Mechanics.extra_targets (other enemies within Ricochet's 13 m). Hero
  abilities are left alone: their landing factors were fitted to real damage, which already counts every target;
- ally items (auras, ally heals and barriers) multiply the score by 1 + their team-only value per teammate in reach
  (sim/scripts/team/team_value.py: 3v3 fights with and without what reaches teammates, as a share of the holder's
  own damage) x the real number of teammates in reach (team_value).
Kill value (2026-10-24, Decay still in ~2/3 of the best builds while losing real games on every hero): damage
only matters through kills, and items' damage converts very unequally. Each item's own damage counts x its real
kill weight (KILL_WEIGHT, sim/data/kill_weight.json): Decay's % current health, non-lethal ticks land mostly on
targets that walk away (0.40 of its holder's other damage is followed by a kill), Siphon Bullets' 1.20.
Item use (2026-10-24): the sim casts every active the moment it can; damage actives carry a real damage factor
for that (item_landing), but debuff / buff / shield actives had none and counted in full in every fight. In 260
Phantom+ replays holders cast them in only part of their engagements (sim/data/item_use.json,
sim/scripts/item_use/fit_item_use.py: Knockdown 0.45, Cursed Relic 0.42, Disarming Hex 0.68, Rusted Barrel 0.74,
Rescue Beam 0.28 of the sim's use; Metal Skin as often as the sim), so in realistic mode each sits unused in the rest of
the spread fights (deadsim engine.unused_items). Ally actives' team value (team_value) is left as fitted.
Death cost (2026-10-25, the real win check found Cheat Death and late vitality winning while never picked): the 30 s
duel ends at a death, so dying cost nothing beyond the damage not dealt after it, while a real death costs the
respawn (~9 s at 0-5k net worth, ~65 s at 27k, ~85 s from 40k), the walk back, and the kill bounty the enemy team
gets (~1700 souls at 27-37k, worth ~73 s of the hero's own farm). The score is multiplied by death_value: the share
of the game a build spends fighting, (c + d_pop x L) / (c + d x L), where c = real alive seconds per engagement, L =
the seconds a death costs and d the build's deaths per engagement: the hero's real rate (sim/data/death_cost.json,
sim/scripts/death_cost/fit_death_cost.py: 0.15 / 0.26 / 0.22 per engagement in lane / mid / late, per hero ratio)
x the build's sim death chance over the popular build's, a death at t s counting x P(a real fight is still going at
t) (a build that dies after the real fight would have ended mostly lives). Lane stages: 1 (the lane test ends at
a death already). OPT-IN (DEATH_COST, off by default): it does not rank items more like real wins
(analysis/scripts/sim_vs_win.py --death, 42 heroes at 27k: all pairs Pearson 0.136 -> 0.128 with the bounty, 0.132 without;
per item 0.214 -> 0.194 / 0.205). It lifts Cheat Death (sim death chance x0.36, real edge +2.9) but every tank item
with it (Metal Skin -5.8, Rebuttal -2.2), and real holders of tank items barely die less: deaths per 10 min of
holders vs others at equal hero, net worth and length are 0.90-1.07 where the sim's death chance says 0.48-0.75
(analysis/scripts/death_check.py: log sim vs log real ratio r -0.04 over 1158 hero x item pairs). Real players
spend extra survivability on fighting more, not on dying less.
Real death rate (2026-10-25, follow-up): 74k Phantom+ matches' stat timelines (sim/scripts/fight_rate/, every ~3-5
min per player) show where it goes. At the same hero, net worth and game time, +10% max health = +5-7% damage taken
per minute (more or longer fights) and -5% deaths, but about the same damage dealt per minute. Across items, the
extra damage taken doesn't track real wins (r -0.04), holders' deaths per minute do (r -0.32; kills + assists
+0.39, and the sim already ranks items like those, r 0.62). So the score is multiplied by death_rate_value: the
death_value share with d = the hero's real deaths per engagement x the held items' real holder / non-holder death
ratios (sim/data/fight_rate.json at the budget's net worth, |z| >= 3, movement items left out; Cheat Death 0.67,
Restorative Locket 0.91, Spirit Resilience ~0.92, Metal Skin 1.04, Rebuttal 1.07). sim_vs_win at 27k: all pairs
0.133 -> 0.168, per item 0.209 -> 0.265, edges clear of noise 0.181 -> 0.229 (37k: 0.146 -> 0.174, 0.219 ->
0.264); Cheat Death's mean gain rank 119 -> 52
of 141, Rebuttal 25 -> 110, Metal Skin 82 -> 92. An "HP budget" fight rate (fight_value: fights per minute = max
health ^ the real damage-taken elasticity / sim health lost per fight) ranks items less like real wins in every
variant (0.133 -> 0.095-0.125) and stays OFF (FIGHT_RATE).
Not counted: vision, souls from farming (Monster Rounds), objective damage, debuffs from area items on the other
enemies.

Real win edge (Tyler 2026-10-24, "blend win edge into score"): the score is also multiplied by
exp(WIN_K x the sum of the held items' real win edges on this hero) / the popular build's (win_value). Edge = win-rate
points vs other same-slot same-tier items, Ritualist+, matched and shrunk toward the item's all-hero edge (lower for
items the hero seldom buys, build_win_check.rarity_fit)
(analysis/out/hero_item_edge.json; each patch rerun refreshes it from the new patch's builds with
pipeline/refresh_win_edge.py, keeping the last one when there are too few matches yet). The 1v1 score alone
ranked items almost unrelated to real wins (r 0.05 over 16 heroes): Decay was in 119 of ~200 best builds while
losing 2-5 points on every hero, and team auras / AoE / death saves (Heroic Aura, Mystic Reverb, Cheat Death) were
never picked. Movement items already carry a real-data value (movement_value) and are left out of the blend.

Damage elasticity (2026-10-27): the damage part counts as (damage before death / the popular build's) ^
DAMAGE_ELASTICITY 0.5, the real holders' damage per minute response to the sim's damage gain across items; damage
items had been ranked over same-tier items that win more (see DAMAGE_ELASTICITY).

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
import functools
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
from deadsim.accuracy import default_distance, hero_default_skill  # noqa: E402
from deadsim.build import compute_stats  # noqa: E402
from deadsim.mechanics import LENGTH_STEP, area_extra, reach_share_at, real_length, real_nearby  # noqa: E402
from survival import survive  # noqa: E402

MAX_TIME = 30.0
FOCUS = 2.0
# real fights mostly end in a disengage, not a death (sim/data/fight_length.json): each hit counts x P(a real fight
# is still going then), deadsim.mechanics.real_length at the build's net worth. False: every hit to the death or 30 s
FIGHT_LENGTH = True
_sk = {}
MOVE_PATH = os.path.join(ROOT, "..", "sim", "data", "movement_value.json")
_move = None
# close_items (Stalker): a hero closer than the measured holders gets at most this multiple of the measured gain
CLOSE_SCALE_MAX = 1.25


WIN_EDGE = os.path.join(ROOT, "..", "analysis", "out", "hero_item_edge.json")
# score factor per win-rate point of real edge: a +3 point item = x1.16, Decay on most heroes (-3.5) = x0.84, about
# the sim value Decay adds over a typical spirit item (~0.3-0.5 of the popular build's score at 27k)
WIN_K = 0.05
WIN_CAP = 4.0   # points
# losses need a narrower band than gains (one-sided 90%, not 95%): the band guards against the search chasing noisy
# gains, and rare picks' losses hold up on independent players while their honest, wider band
# (build_win_check.rarity_fit) would let Decay and co. back in at 1.96. 8 heroes at 27k with the rare-pick prior:
# 1.96 both ways let 13 items under -2 points into builds (was 9), counting every loss cost 14% damage before dying,
# 1.28 kept both (9 items, -0.5% damage) and dropped the rare gains (Heroic Aura, Diviner's Kevlar on Abrams/Lash).
WIN_NEG_Z = 1.28
_win = None


TEAM_PATH = os.path.join(ROOT, "..", "sim", "data", "team_value.json")
_team = None
# Real ally healing (2026-10-27, Restorative Locket had the top sim gain with a ~0 real win edge): the 3v3 fit heals
# the neediest teammate whenever the item is ready, and real Phantom+ holders of Healing Nova and Rescue Beam heal
# teammates about that much, but real Locket holders heal themselves: 6 HP/min to teammates vs 118 to self, where the
# 3v3 heals teammates 2.5x more than the holder. Each heal item's team value is x its real ally heal per minute over
# the 3v3's, relative to the heal items' median (sim/data/ally_heal.json, sim/scripts/team/ally_heal.py: Locket 0.072,
# Nova and Rescue Beam 1). Its self heal stays in the duel.
ALLY_HEAL = True
ALLY_HEAL_PATH = os.path.join(ROOT, "..", "sim", "data", "ally_heal.json")
_ally_heal = None
# area items: item -> (centre, radius m). "target": the hit lands around the holder's target (other enemies within
# the radius of it); "self": around the holder. Ricochet's bounce radius sets the duel's extra_targets.
AREA_ITEMS = {
    "Mystic Reverb": ("target", 16), "Alchemical Fire": ("target", 10), "Tesla Bullets": ("target", 8),
    "Capacitor": ("target", 10), "Scourge": ("self", 10), "Torment Pulse": ("self", 9), "Cold Front": ("self", 10),
    "Arctic Blast": ("self", 16),
}
RICOCHET_RADIUS = 13


# Kill value (2026-10-24): real damage is worth what it does to kills. Each item's own damage (in the duel, on other
# enemies and as splash) counts x its real kill weight: how often its damage is followed by the victim's death within
# 10 s, against the holder's own other damage in the same match (sim/scripts/kill_value/fit_kill_weight.py, 260
# Phantom+ replays; Decay 0.40, Return Fire 0.54, Ricochet 0.59, Headshot Booster 0.69, Tankbuster 0.70, Mystic
# Reverb 0.71 ... Escalating Exposure 1.17, Siphon Bullets 1.20). Hero abilities, gun and melee keep 1 (the holder's
# baseline).
KILL_WEIGHT = True
KILL_PATH = os.path.join(ROOT, "..", "sim", "data", "kill_weight.json")
_kill = None


DEATH_COST = False    # opt-in, see the docstring (does not track real wins)
DEATH_PATH = os.path.join(ROOT, "..", "sim", "data", "death_cost.json")
DEATH_BOUNTY = 1.0     # weight of the enemy team's kill bounty in a death's cost (0 = only the time dead)
DEATH_EPS = 0.01       # floor of the sim death chance in the ratio (a popular build that never dies)
_death = None


# Fight rate (2026-10-25): real tank-item holders die about as often as non-holders (analysis/scripts/death_check.py)
# but take more damage per minute: their extra health goes into taking more fights. Phantom+ stat timelines (sim/
# scripts/fight_rate/fit_fight_rate.py) at the same hero, net worth and game time: damage taken per minute rises with
# max health (elasticity ~0.7), damage dealt per HP of it barely moves. So a build's fights per minute = health it can
# spend per minute (max health ^ hp_elasticity) / health it loses per fight (sim: expected damage taken - healed over
# real fight lengths, LOSS_FLOOR x max health at least), relative to the popular build's, clamped to FIGHT_CLAMP.
# Tried 2026-10-25 and left OFF: it ranks items less like real wins (sim_vs_win all pairs 0.133 -> 0.095-0.125 over
# exponent variants): real holders' extra damage taken per minute doesn't track wins (r -0.04 over items), their
# deaths do. See death_rate_value.
FIGHT_RATE = False
FIGHT_RATE_PATH = os.path.join(ROOT, "..", "sim", "data", "fight_rate.json")
LOSS_FLOOR = 0.1
FIGHT_CLAMP = (0.67, 1.5)
_rate = None

# Real death rate (2026-10-25): the same timelines give each item's real deaths per minute, holders / non-holders
# at the same hero, net worth and game time (fight_rate.json items[budget], intervals at 0.75-1.35x the budget).
# Most tank items barely move it (Extra Health 1.0, Rebuttal 1.07, Metal Skin 1.0); Cheat Death 0.67, Restorative
# Locket 0.91, Spirit Resilience 0.91 do. Score x the share of the game spent fighting (c + d_pop L) / (c + d L),
# like death_value but with d = d_pop x the product of the held items' real ratios (|z| >= DEATH_RATE_Z, each and
# the product clamped to DEATH_RATE_CLAMP), not the sim death chance (which doesn't track real deaths, death_check).
# Movement items are left out: movement_value already counts their deaths (escape). An association at equal net
# worth, not a controlled effect: players who die less may also pick certain items.
DEATH_RATE = True
DEATH_RATE_Z = 3.0
DEATH_RATE_CLAMP = (0.5, 1.5)
_drate = {}

# Damage elasticity (2026-10-27, damage items scored over same-tier utility items that win more): across items, real
# Phantom+ holders' hero damage per minute rises only ~half as much as the sim's damage before death says (log real
# holder / non-holder damage ratio = 0.51 x log sim ratio over 141 items at 27k, both match-id halves 0.51-0.52,
# 0.45 at 37k; sim/scripts/fight_rate/holder_rates.py). Fights end, targets back off and teammates take kills, so a
# build's extra duel damage only partly becomes real damage. The score counts the damage ratio to the popular build
# ^ DAMAGE_ELASTICITY; the real-data factors (death rate, team value, movement, map time, win edge) keep full weight.
# sim_vs_win 27k: all pairs 0.180 -> 0.217, within slot and tier 0.220 -> 0.258, damage items 0.083 -> 0.114, per
# item 0.258 -> 0.306 (both hero halves). 1.0 = the old score.
DAMAGE_ELASTICITY = 0.5


def death_data():
    global _death
    if _death is None:
        with open(DEATH_PATH) as f:
            _death = json.load(f)
    return _death


def death_seconds(souls):
    """Seconds of the game a death costs at net worth souls: respawn + walk back + the enemy team's kill bounty in
    seconds of the hero's own farm (x DEATH_BOUNTY)."""
    d = death_data()
    rs = d["respawn_s"]
    if souls <= rs[0][0]:
        r = rs[0][1]
    elif souls >= rs[-1][0]:
        r = rs[-1][1]
    else:
        k = next(k for k in range(1, len(rs)) if rs[k][0] >= souls)
        (x0, y0), (x1, y1) = rs[k - 1], rs[k]
        r = y0 + (y1 - y0) * (souls - x0) / (x1 - x0)
    so = [b for b in d["souls"] if b["nw"] <= souls][-1]
    return r + d["phases"][game_phase(souls)]["walk_back_s"] + DEATH_BOUNTY * max(0.0, so["bounty"]) / so["soul_rate"]


def death_chance(r, souls):
    """Sim chance that a fight is a death: 0 when the build lives through it, else P(a real fight is still going at
    the death's time) (the real disengage curve, real_length); 1 at a death without FIGHT_LENGTH."""
    if r["survived"]:
        return 0.0
    if not FIGHT_LENGTH:
        return 1.0
    c = real_length(souls)
    k = min(len(c) - 1, int(r["time_alive"] / LENGTH_STEP))
    return c[k]


def death_value(pd, pd_pop, hero, souls):
    """Share of the game a build spends fighting relative to the popular build's: (c + d_pop L) / (c + d L), c = the
    real alive seconds per engagement, L = death_seconds, d_pop = the hero's real deaths per engagement and d = d_pop x
    the build's sim death chance (death_chance, mean over enemies) / the popular build's. 1 when DEATH_COST is off."""
    if not DEATH_COST:
        return 1.0
    dd = death_data()
    row = dd["phases"][game_phase(souls)]
    d_pop = row["deaths_per_engagement"] * dd["heroes"].get(str(hero), {}).get("ratio", 1.0)
    d = d_pop * (pd + DEATH_EPS) / (pd_pop + DEATH_EPS)
    c, L = row["alive_s_per_engagement"], death_seconds(souls)
    return (c + d_pop * L) / (c + d * L)


def fight_rate_data():
    global _rate
    if _rate is None:
        with open(FIGHT_RATE_PATH) as f:
            _rate = json.load(f)
        with open(os.path.join(ROOT, "..", "data", "patch.json")) as f:
            patch = json.load(f)["patch"]
        if _rate.get("patch") != patch:   # static fit: CI can't refit it (the timelines live in the shared folder)
            print(f"warning: {FIGHT_RATE_PATH} is from patch {_rate.get('patch')}, the sim is on {patch}; rerun "
                  "sim/scripts/fight_rate/fetch_rates.py and fit_fight_rate.py", file=sys.stderr)
    return _rate


def death_rates(souls):
    """{item id: real deaths-per-minute ratio of holders} for the fit budget nearest souls (|z| >= DEATH_RATE_Z,
    movement items left out)."""
    d = fight_rate_data()["items"]
    b = min(d, key=lambda k: abs(math.log(int(k) / souls)))
    if b not in _drate:
        movement_value(())   # loads _move
        moving = _move[2] | {i for row in _move[3].values() for i in row}
        lo, hi = DEATH_RATE_CLAMP
        by_name = {it.name: i for i, it in S.G().items.items()}
        gone = sorted(n for n in d[b]["items"] if n not in by_name)
        if gone:   # renamed or removed by a patch: their ratios are dropped (pipeline/smoke_test.py checks this)
            print(f"warning: {FIGHT_RATE_PATH} names items the game no longer has: {gone}", file=sys.stderr)
        _drate[b] = {by_name[n]: max(lo, min(hi, e["deaths"][0])) for n, e in d[b]["items"].items()
                     if n in by_name and by_name[n] not in moving and abs(e["deaths"][1]) >= DEATH_RATE_Z}
    return _drate[b]


def death_rate_value(items, hero, souls):
    """(c + d_pop L) / (c + d L): c = real alive seconds per engagement, L = death_seconds, d_pop = the hero's real
    deaths per engagement, d = d_pop x the product of the held items' real death ratios (death_rates). Divided by
    the popular build's in the score. 1 when DEATH_RATE is off."""
    if not DEATH_RATE:
        return 1.0
    rates = death_rates(souls)
    ratio = 1.0
    for i in set(items):
        ratio *= rates.get(i, 1.0)
    lo, hi = DEATH_RATE_CLAMP
    ratio = max(lo, min(hi, ratio))
    dd = death_data()
    row = dd["phases"][game_phase(souls)]
    d_pop = row["deaths_per_engagement"] * dd["heroes"].get(str(hero), {}).get("ratio", 1.0)
    c, L = row["alive_s_per_engagement"], death_seconds(souls)
    return (c + d_pop * L) / (c + d_pop * ratio * L)


def fight_value(loss, loss_pop, hp, hp_pop, souls):
    """Fights per minute of a build relative to the popular build's: (hp / hp_pop) ^ e x loss_pop / loss, loss = mean
    health lost per fight (floored at LOSS_FLOOR x max health), e = the real elasticity of damage taken per minute to
    max health in the build's game phase. 1 when FIGHT_RATE is off."""
    if not FIGHT_RATE or loss_pop <= 0:   # lane fights carry no health lost (the lane test scores staying in lane)
        return 1.0
    e = fight_rate_data()["hp_elasticity"][game_phase(souls)]
    lo, hi = FIGHT_CLAMP
    v = (hp / hp_pop) ** e * max(loss_pop, LOSS_FLOOR * hp_pop) / max(loss, LOSS_FLOOR * hp)
    return max(lo, min(hi, v))


def kill_weights():
    """{item name: real kill weight} (sim/data/kill_weight.json), {} when KILL_WEIGHT is off. The file is a static
    fit refreshed by hand (the replays live in the shared folder, CI can't refit it): after a patch that reworks an
    item's damage, rerun sim/scripts/kill_value/fit_kill_weight.py on new replays."""
    global _kill
    if not KILL_WEIGHT:
        return {}
    if _kill is None:
        with open(KILL_PATH) as f:   # committed file: missing = broken checkout, fail rather than publish unweighted
            _kill = {n: v["weight"] for n, v in json.load(f)["items"].items()}
    return _kill


def kill_cut(by):
    """Damage of a {source: damage} dict that real kills don't back: sum of (1 - kill weight) x each item's damage."""
    kw = kill_weights()
    return sum((1.0 - kw[k]) * v for k, v in by.items() if k in kw)


def team_data():
    global _team
    if _team is None:
        with open(TEAM_PATH) as f:
            _team = json.load(f)
        with open(os.path.join(ROOT, "..", "data", "patch.json")) as f:
            patch = json.load(f)["patch"]
        fit = _team.get("items", {}).get("patch")
        if fit != patch:
            print(f"warning: {TEAM_PATH} ally item values are from patch {fit}, the sim is on {patch}; "
                  "rerun sim/scripts/team/team_value.py", file=sys.stderr)
    return _team


def near(kind, radius, souls):
    """Real mean count of enemies / teammates in reach in a Phantom+ fight second (deadsim.mechanics.real_nearby)."""
    return real_nearby(kind, radius, souls)


def area_damage(r, souls):
    """Damage the duel's area items (AREA_ITEMS) and splash (Ricochet, Split Shot) deal to the other enemies."""
    by = r.get("damage_by_source", {})
    kw = kill_weights()
    extra = 0.0
    for name, (c, rad) in AREA_ITEMS.items():
        k = area_extra(name, souls)    # replay-measured at this net worth; the position count is the fallback
        extra += by.get(name, 0.0) * kw.get(name, 1.0) * (k if k is not None else near("extra" if c == "target" else "extra_self", rad, souls))
    return extra + r.get("splash_dealt", 0.0) - kill_cut(r.get("splash_by_source", {}))


def team_value(items, souls):
    """1 + the held ally items' team-only value (share of the holder's damage it gives teammates, per teammate in the
    3v3) x real teammates in reach / the 3v3's (team_value.json items). Only fits clear of their 95% band count.
    The 3v3 fit casts ally actives whenever ready; their real use share (item_use.json) is NOT applied here: the
    fitted value mixes the passive aura (Heroic Aura's ally bullet resist...) with the active, and scaling all of it
    by the active's share moved the sim further from real wins (Heroic Aura +2.6 win points already under).
    Heal items are x their real ally heal share (ALLY_HEAL: Restorative Locket is used on the holder itself)."""
    vals = team_data().get("items", {}).get("values", {})
    heal = ally_heal() if ALLY_HEAL else {}
    g = S.G()
    v = 1.0
    for i in set(items):
        spec = vals.get(g.item(i).name)
        if not spec:
            continue
        bud = spec["budgets"]
        b = min(bud, key=lambda k: abs(math.log(int(k) / souls)))
        kind = {"allies": "allies", "any": "any_ally", "enemies": "extra_self"}[spec["reach"]]
        if bud[b]["value"] > 1.96 * bud[b].get("se", 0.0):   # the search would chase lucky noisy fits
            v += bud[b]["value"] * near(kind, spec["radius_m"], souls) / spec["reach_sim"] \
                * heal.get(g.item(i).name, 1.0)
    return v


def ally_heal():
    """{heal item name: real ally heal factor} (sim/data/ally_heal.json); items it doesn't name count 1."""
    global _ally_heal
    if _ally_heal is None:
        with open(ALLY_HEAL_PATH) as f:
            d = json.load(f)
        with open(os.path.join(ROOT, "..", "data", "patch.json")) as f:
            patch = json.load(f)["patch"]
        if d.get("patch") != patch:   # static file: the sustain replays live in the shared folder, CI can't refit it
            print(f"warning: {ALLY_HEAL_PATH} is from patch {d.get('patch')}, the sim is on {patch}; "
                  "rerun sim/scripts/team/ally_heal.py on new sustain replays", file=sys.stderr)
        _ally_heal = {n: e["factor"] for n, e in d["items"].items()}
    return _ally_heal


def win_value(items, hero):
    """exp(WIN_K x sum of the held items' real per-hero win edges, in points). Only positive edges clear of their 95%
    band count (losses: one-sided 90%, WIN_NEG_Z), each capped at +-WIN_CAP (the search maximises, so it
    would chase noisy edges of rare items); movement items are left out (their real value is already in
    movement_value). A warning is printed when the edges' patch differs from data/patch.json (the rerun kept the last
    snapshot)."""
    global _win
    if _win is None:
        with open(WIN_EDGE) as f:
            d = json.load(f)
        with open(os.path.join(ROOT, "..", "data", "patch.json")) as f:
            patch = json.load(f)["patch"]
        if d["meta"].get("patch") != patch:
            print(f"warning: {WIN_EDGE} is from patch {d['meta'].get('patch')}, the sim is on {patch}; "
                  "too few new matches yet (pipeline/refresh_win_edge.py)", file=sys.stderr)
        movement_value((), None)   # loads _move
        moving = _move[2] | {i for row in _move[3].values() for i in row}
        _win = {int(h): {int(i): max(-WIN_CAP, min(WIN_CAP, v[0])) for i, v in row.items()
                         if int(i) not in moving and (v[0] > 1.96 * v[1] or v[0] < -WIN_NEG_Z * v[1])}
                for h, row in d["heroes"].items()}
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
                  for h, row in d.get("hero_items", {}).items()},
                 {by_name[n]: c for n, c in d.get("close_items", {}).items() if n in by_name})
    vals, caps, moving, hero_vals, close = _move
    extra = hero_vals.get(hero, {}) if hero is not None else {}
    held = set(items)
    v = 1.0
    for i in held:
        x = extra.get(i, vals.get(i, 1.0))
        if i in close and hero is not None:
            x = 1.0 + (x - 1.0) * close_scale(i, hero)
        v *= x
    n = len(held & (moving | set(extra)))   # the caps were measured on any movement items held, weighted or not
    if n >= 2 and caps:
        v = min(v, caps[min(n, max(caps))])
    return v


@functools.lru_cache(maxsize=None)
def close_scale(item, hero):
    """A close_items movement item's speed procs on weapon hits within radius_m: the hero's reach share at its real
    median fight distance / the share of the players its value was measured on (Stalker: Vindicta ~0.25, Abrams
    ~1.14). Capped so the item stays within the file's 1.25 per-item cap."""
    c = _move[4][item]
    k = reach_share_at(default_distance(hero), c["radius_m"] + 0.5, c["cooldown_s"]) / c["holder_share"]
    return min(k, CLOSE_SCALE_MAX)


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
    """Damage dealt minus the healing the enemy got: healing undoes damage (Healbane, enemy lifesteal...). Items'
    damage counts x their real kill weight (kill_cut)."""
    return max(0.0, r["damage_dealt"] - kill_cut(r.get("damage_by_source", {})) - r.get("enemy_healed", 0.0))


def fight(h, items, oh, oitems, souls, phase=None, start_hp=None):
    sk = dataclasses.replace(skill(h), fight_phase=phase)
    esk = dataclasses.replace(skill(oh), fight_phase=None if phase is None else (phase + 0.5) % 1.0)
    r = survive(h, items, souls, oh, oitems, max_time=MAX_TIME, focus=FOCUS, skill=sk, enemy_skill=esk,
                start_hp=start_hp, extra_targets=near("extra", RICOCHET_RADIUS, souls),
                fight_length=real_length(souls) if FIGHT_LENGTH else None)
    return (net_damage(r) + area_damage(r, souls), r["time_alive"], r["survived"], death_chance(r, souls),
            r["damage_taken_exp"] - r["healing_exp"], r["healing_by_source"])


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
    lane pressure, enemy sustain and anti-heal all count. start_hp is unused (the lane starts full). Area items and
    Ricochet also hit other enemies here: real lane fights aren't pure 1v1s either (team_value.json 10k bin)."""
    sk = dataclasses.replace(skill(h), fight_phase=phase)
    esk = dataclasses.replace(skill(oh), fight_phase=None if phase is None else (phase + 0.5) % 1.0)
    hp, ehp, dmg, t = None, None, 0.0, 0.0
    hb = healbane_gap_share(items)
    for k in range(LANE_TRADES):
        r = survive(h, items, souls, oh, oitems, max_time=TRADE_S, focus=LANE_FOCUS, skill=sk, enemy_skill=esk,
                    start_hp=hp, enemy_start_hp=ehp, extra_targets=near("extra", RICOCHET_RADIUS, souls))
        dmg += net_damage(r) + area_damage(r, souls)
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
        self.norm, self.dmg_norm = {}, {}
        pop = tuple(sorted(S.popular_build(hero, S.item_budget(budget), pools)))
        self.deficit = entry_deficit(hero, pop, budget)
        self.pop = pop
        self.map_pop = map_time(hero, pop, budget, pop)
        self.pd_pop, self.loss_pop = {}, {}
        self.hp_pop = build_stats(hero, pop, budget)["max_hp"]
        for pool in ("S", "F", "F2"):
            rows = self._rows(pop, pool)
            self.pd_pop[pool] = self._death(rows)
            self.loss_pop[pool] = self._loss(rows)
            self.dmg_norm[pool] = max(1.0, self._mean(rows, 2))
            self.norm[pool] = movement_value(pop, hero) \
                * self._map(pop) * win_value(pop, hero) * team_value(pop, budget) * death_rate_value(pop, hero, budget)

    def _rows(self, items, pool):
        key = (tuple(sorted(items)), pool)
        if key not in self.cache:
            rows = []
            start = entry_hp_start(self.h, key[0], self.souls, self.deficit)
            for k, (oh, oitems, w) in enumerate(self.pools[pool]):
                d, t, alive, *pd = self.fight(self.h, key[0], oh, oitems, self.souls, phase=PHASES[oh],
                                              start_hp=start)
                # lane fights: no death chance or health lost
                rows.append((oh, w, d, t, alive, pd[0] if pd else 0.0, pd[1] if len(pd) > 1 else 0.0,
                             pd[2] if len(pd) > 2 else {}))
                self.fights += 1
            self.cache[key] = rows
        return self.cache[key]

    def _map(self, items):
        """map_time relative to the popular build (lane stages: 1, the lane test already scores staying in lane)."""
        return map_time(self.h, items, self.souls, self.pop) / self.map_pop

    def _death(self, rows):
        """Mean sim death chance over the enemies (rows without one: 0)."""
        tw = sum(r[1] for r in rows)
        return sum(r[1] * (r[5] if len(r) > 5 else 0.0) for r in rows) / tw

    def _loss(self, rows):
        """Mean health lost per fight over the enemies (rows without one: 0)."""
        tw = sum(r[1] for r in rows)
        return sum(r[1] * (r[6] if len(r) > 6 else 0.0) for r in rows) / tw

    @staticmethod
    def _heals(rows):
        """Mean healing per fight over the enemies, by heal source (survive's healing_by_source)."""
        tw, out = sum(r[1] for r in rows), {}
        for r in rows:
            for k, v in (r[7] if len(r) > 7 else {}).items():
                out[k] = out.get(k, 0.0) + r[1] * v / tw
        return {k: round(v, 1) for k, v in sorted(out.items(), key=lambda x: -x[1]) if v >= 0.5}

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
        team = team_value(items, self.souls)
        pd = self._death(rows)
        death = death_value(pd, self.pd_pop[pool], self.h, self.souls)
        loss = self._loss(rows)
        rate = fight_value(loss, self.loss_pop[pool], build_stats(self.h, items, self.souls)["max_hp"], self.hp_pop,
                           self.souls)
        drate = death_rate_value(items, self.h, self.souls)
        score = (max(0.0, dmg) / self.dmg_norm[pool]) ** DAMAGE_ELASTICITY * move * mt * win * team * death * rate * drate \
            / self.norm[pool]
        if not detail:
            return score
        t = self._mean(rows, 3)
        return {
            "score": round(score, 4),
            "damage_before_death": round(dmg, 1),   # net of the enemy's healing
            "damage_elasticity": DAMAGE_ELASTICITY,   # the score counts the damage ratio ^ this
            "entry_hp": round(entry_hp_start(self.h, items, self.souls, self.deficit)),
            "time_alive_s": round(t, 2),
            "survived_30s": round(self._mean(rows, 4), 4),
            "dps_while_alive": round(dmg / max(0.1, t), 1),
            "movement_value": round(move, 4),
            "map_time": round(mt, 4),   # time on the map vs the popular build (fewer heal trips)
            "win_value": round(win, 4),  # real win-edge factor (win_value), before dividing by the popular build's
            "team_value": round(team, 4),  # ally items' value to teammates (team_value), same
            "death_chance": round(pd, 4),  # sim chance a fight is a real death (death_chance), mean over enemies
            "death_value": round(death, 4),  # share of the game fighting vs the popular build (death_value)
            "hp_lost_per_fight": round(loss, 1),  # expected damage taken - healed over real fight lengths
            "healing_by_source": self._heals(rows),  # mean healing per fight (expected over real lengths) by source
            "fight_rate": round(rate, 4),  # fights per minute vs the popular build (fight_value)
            "death_rate_value": round(drate, 4),  # real holders' deaths (death_rate_value), before the popular's
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
    S.SWAPS = True
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
