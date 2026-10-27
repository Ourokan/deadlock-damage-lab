"""High-level API: describe two loadouts, run a duel or a one-way time-to-kill.

    from deadsim import Loadout, duel, time_to_kill
    a = Loadout("Infernus", ["Extra Spirit", "Mystic Burst", "Toxic Bullets"], souls=12000)
    b = Loadout("Haze", ["Rapid Rounds", "Swift Striker"], souls=12000)
    print(duel(a, b, distance=15).summary())
"""
from __future__ import annotations

import bisect
import heapq
import dataclasses
import json
import os
import random
from dataclasses import dataclass, field
from functools import lru_cache

from .abilities import AbilityState, load_heroes
from .build import NET_WORTH_OFFSET, compute_stats
from .data import game, DATA_DIR
from .engine import MELEE_ITEMS, Engine, Fighter, Skill, _UNSET
from . import items_fx, patterns

# median number of ability events (unlock or upgrade) by net worth, from 200k current-patch ranked rows
_EVENTS_BY_SOULS = [(0, 1), (500, 2), (1000, 3), (2000, 5), (3000, 6), (4000, 7), (6000, 8), (8000, 9),
                    (10000, 10), (12000, 11), (16000, 12), (18000, 13), (26000, 14), (34000, 15), (50000, 16)]


def ability_events_for_souls(souls):
    i = bisect.bisect_right([s for s, _ in _EVENTS_BY_SOULS], souls) - 1
    return _EVENTS_BY_SOULS[max(0, i)][1]


@lru_cache(maxsize=64)
def popular_ability_order(hero_id, rank="oracle_plus"):
    """Most-played full ability order for the hero (list of ability ids, first occurrence = unlock)."""
    agg = os.path.join(DATA_DIR, "builds", "aggregates", "per_hero")
    for fn in os.listdir(agg):
        if fn.startswith(f"{hero_id}_"):
            rows = json.load(open(os.path.join(agg, fn)))[rank]["ability_order_stats"]
            rows = [r for r in rows if len(r["abilities"]) >= 16] or rows
            if rows:
                return tuple(max(rows, key=lambda r: r["matches"])["abilities"])
    return ()


# ability points a tier 1, 2 and 3 upgrade costs (4 abilities x 8 = the 32 points a hero earns by level 36)
UPGRADE_AP = (1, 2, 5)


def ability_budget(hero, souls):
    """(ability unlocks, ability points) a hero has earned at this net worth: one or the other per level reached
    (levels from souls - NET_WORTH_OFFSET, like compute_stats)."""
    hero = game().hero(hero)
    s = max(0.0, souls - NET_WORTH_OFFSET)
    got = [b for g, b in zip(hero.level_gold, hero.level_bonus) if s >= g]
    return got.count("unlock"), got.count("point")


def abilities_for_order(hero, order, souls):
    """(tiers, unlocked) after following `order` as far as this net worth's unlocks and ability points allow.

    order: ability ids in the Deadlock API's ability-order format (the first time an id appears unlocks it, each
    later time buys its next upgrade). Strictly in order: an upgrade waits until its points are there and nothing
    after it is bought first, like a player saving for a tier 3."""
    hero = game().hero(hero)
    ids = [a.id for a in hero.abilities]
    unlocks, points = ability_budget(hero, souls)
    tiers, unlocked = [0] * len(ids), [False] * len(ids)
    for aid in order:
        if aid not in ids:
            continue
        i = ids.index(aid)
        if not unlocked[i]:
            if unlocks < 1:
                break
            unlocks -= 1
            unlocked[i] = True
        elif tiers[i] < 3:
            if points < UPGRADE_AP[tiers[i]]:
                break
            points -= UPGRADE_AP[tiers[i]]
            tiers[i] += 1
    return tiers, unlocked


@dataclass
class Loadout:
    hero: object
    items: list = field(default_factory=list)
    souls: float | None = None              # net worth; defaults to the items' total cost
    level: int | None = None
    skill: Skill = field(default_factory=Skill)
    tiers: list | None = None                # upgrades bought per ability [t1, t2, t3, t4] (0-3); None = auto
    unlocked: list | None = None             # [bool]*4; None = auto from souls
    ability_order: list | None = None        # ability ids, API format (abilities_for_order); None = popular order
    imbues: dict = field(default_factory=dict)   # item name -> ability index (0-3); auto = best damage ability
    name: str | None = None

    def resolve(self):
        G = game()
        hero = G.hero(self.hero)
        items = [G.item(i) for i in self.items]
        return hero, items


def _auto_abilities(hero, souls):
    order = popular_ability_order(hero.id)
    n = ability_events_for_souls(souls)
    ids = [a.id for a in hero.abilities]
    tiers, unlocked = [0] * len(ids), [False] * len(ids)
    if not order:
        return [min(3, n // 4)] * len(ids), [True] * len(ids)
    for aid in order[:n]:
        if aid not in ids:
            continue
        i = ids.index(aid)
        if not unlocked[i]:
            unlocked[i] = True
        else:
            tiers[i] = min(3, tiers[i] + 1)
    return tiers, unlocked


IMBUE_CLASSES = ("upgrade_magic_reach", "upgrade_magic_tempo", "upgrade_arcane_extension", "upgrade_magic_storm",
                 "upgrade_quick_silver", "upgrade_ethereal_bullets", "upgrade_mystic_reverb",
                 "upgrade_bulletshredimbue", "upgrade_ability_power_shard", "upgrade_frostbite_charm")


# imbue slot by item where players don't follow the hero's usual imbue slot (Tyler, 2026-10-21: Mina puts Mystic
# Expansion on Sanguine Retreat for a longer dash, not on Rake)
IMBUE_OVERRIDE = {("hero_vampirebat", "upgrade_magic_reach"): "ability_vampirebat_batblink"}


def _default_imbue_target(hero, unlocked):
    """Imbue the unlocked non-ultimate ability with the highest listed base damage."""
    best, best_v = None, -1
    for i, ab in enumerate(hero.abilities):
        if not unlocked[i] or ab.ultimate:
            continue
        v = 0.0
        for p in ("Damage", "ImpactDamage", "DPS", "ExplosionDamage", "BaseDamage"):
            if ab.props.get(p):
                v = max(v, ab.props[p] * (3 if p == "DPS" else 1))
        if v > best_v:
            best, best_v = i, v
    return best if best is not None else 0


def melee_build_mult(skill, items):
    """Skill.melee_item_mult entry for this build's count of melee items (1 when unset)."""
    m = skill.melee_item_mult
    if not m:
        return 1.0
    return m[min(len(m) - 1, sum(1 for it in items if it.class_name in MELEE_ITEMS))]


def heavy_holder_skill(skill, hero, items):
    """Mechanics.heavy_holders: a Melee Charge / Crushing Fists holder's rotation at the hero's real heavy share, the
    melee rate cut by the heavier mean hit so melee damage (and gun time lost to swings, about) stays the fitted one."""
    from .mechanics import HEAVY_OPENERS, holder_heavy_share
    if skill.melee_rate <= 0 or not any(it.class_name in HEAVY_OPENERS for it in items):
        return skill
    light = hero.base.get("light_melee_damage", 0.0)
    if light <= 0:
        return skill
    r = (hero.base.get("heavy_melee_damage", 0.0) or 2.32 * light) / light
    h = holder_heavy_share(hero.id)
    old = skill.heavy_share
    return dataclasses.replace(skill, heavy_share=h,
                               melee_rate=skill.melee_rate * (1 - old + old * r) / (1 - h + h * r))


def make_fighter(engine, lo: Loadout, name=None):
    load_heroes()
    hero, items = lo.resolve()
    st = compute_stats(hero, items, lo.souls, lo.level)
    skill = lo.skill
    if engine.mech is not None and skill.ability_landing_mech:
        skill = dataclasses.replace(skill, ability_landing=skill.ability_landing_mech)
    # damage booked over real fight lengths: the factors with that part taken out (hits land at the corrected
    # rate, so these move the fight itself, unlike the booking)
    if engine.length:
        c = skill.ability_length_corr
        if c and skill.ability_landing:
            skill = dataclasses.replace(skill, ability_landing={k: v * c.get(k, 1.0) for k, v in skill.ability_landing.items()})
        c = skill.item_length_corr
        if c and skill.item_landing:
            il = skill.item_landing
            skill = dataclasses.replace(skill, item_landing={k: il.get(k, 1.0) * c.get(k, 1.0) for k in set(il) | set(c)})
    if skill.melee_item_mult:
        skill = dataclasses.replace(skill, melee_rate=skill.melee_rate * melee_build_mult(skill, items))
    if engine.mech is not None and getattr(engine.mech, "heavy_holders", False):
        skill = heavy_holder_skill(skill, hero, items)
    f = Fighter(engine, name or lo.name or hero.name, st, skill)
    if lo.ability_order:
        tiers, unlocked = abilities_for_order(hero, lo.ability_order, st.souls)
    else:
        tiers, unlocked = _auto_abilities(hero, st.souls)
    if lo.tiers is not None:
        tiers = list(lo.tiers)
    if lo.unlocked is not None:
        unlocked = list(lo.unlocked)
    imbue_map = {}
    for it in items:
        if it.class_name in IMBUE_CLASSES:
            idx = lo.imbues.get(it.name, lo.imbues.get(it.class_name))
            over = IMBUE_OVERRIDE.get((hero.class_name, it.class_name))
            if idx is None and over:
                idx = next((i for i, ab in enumerate(hero.abilities) if ab.class_name == over), None)
            if idx is None and skill.fight_pattern:
                idx = patterns.imbue_target(hero, unlocked)
            if idx is None:
                idx = _default_imbue_target(hero, unlocked)
            imbue_map.setdefault(idx, []).append(it)
    for i, ab in enumerate(hero.abilities):
        f.abilities.append(AbilityState(f, ab, tiers[i] if i < len(tiers) else 0,
                                        unlocked[i] if i < len(unlocked) else True, imbue_map.get(i, ())))
    items_fx.attach(f, items)
    patterns.attach(f, hero.id)
    if engine.mech is not None:
        from . import mechanics
        mechanics.attach(f, items)
        if engine.length and getattr(engine.mech, "opener_timing", False):
            # only sources whose landing factor has a length correction: the correction (length_factors.py) keeps
            # their level as fitted, the hold only moves where in a fight the damage counts
            corr = set(skill.ability_length_corr) | set(skill.item_length_corr)
            f.opener_hold = {k: q for k, q in mechanics.opener_holds(hero, items).items() if k in corr}
    return f


def duel(a: Loadout, b: Loadout, distance=15.0, max_time=30.0, rng=None, log=False, mechanics=_UNSET):
    """Both sides fight until one dies or max_time passes. mechanics: deadsim.mechanics.Mechanics (parry, summons,
    movement, nearby enemies) or None for the earlier model; unset = mechanics.DEFAULT."""
    e = Engine(distance=distance, max_time=max_time, rng=rng, log=log, mech=mechanics)
    fa = make_fighter(e, a, (a.name or game().hero(a.hero).name) + " (A)")
    fb = make_fighter(e, b, (b.name or game().hero(b.hero).name) + " (B)")
    r = e.run(fa, fb)
    if e.length and getattr(e.mech, "pokes", False):
        add_pokes(r.a_dmg, r.a_exp, a, b, distance, rng, e.mech)
        add_pokes(r.b_dmg, r.b_exp, b, a, distance, rng, e.mech)
    return r


POKE_S = 10.0   # s a poke cast's hits and procs (Mystic Reverb's echo, DoTs) get to land


def add_pokes(dmg, exp, me: Loadout, foe: Loadout, distance, rng, mech):
    """Mechanics.pokes: me's real poke hits beside a fight with foe (mechanics.poke_rows, data/ability_pokes.json).
    A poke is one cast of the ability on foe in a fresh engine (both at full health, cooldowns ready, no gun, no
    other casts), run POKE_S s; its damage and the item procs riding on it (Tankbuster, Mystic Burst, Mystic Shot,
    Mystic Reverb's echo) are added x pokes_per_fight to dmg (in full) and exp (expected over real fight lengths:
    a poke is outside the fight, so in full there too). The cast always lands and its damage counts x the caster's
    spirit_accuracy (the expected hit: one roll per poke would be all or nothing, and with rng None always the
    same). The fight itself (health, winner, time) is untouched: in real games the target has the time to heal up
    before the next fight. Only the damage totals get the pokes, not the fight's time profile (dmg_by_2s,
    dmg_first, PROFILE_SOURCES tallies), which describe the fight."""
    from .mechanics import poke_rows
    hero, _ = me.resolve()
    land = me.skill.spirit_accuracy
    me = dataclasses.replace(me, skill=dataclasses.replace(me.skill, spirit_accuracy=1.0))
    for cls, k in poke_rows(hero).items():
        e = Engine(distance=distance, max_time=POKE_S, mech=mech,
                   rng=None if rng is None else random.Random(rng.random()))
        f, g = make_fighter(e, me, "poker"), make_fighter(e, foe, "target")
        f.enemy, g.enemy = g, f
        e.fighters = [f, g]
        for x in (f, g):
            for fx in x.items_fx:
                h = getattr(fx, "on_start", None)
                if h:
                    h(x)
            for ab in x.abilities:
                ab.start()
        ab = next((x for x in f.abilities if x.ab.class_name == cls and x.unlocked), None)
        if ab is None:
            continue
        f.counters["poke"] = True   # the impl can tell a poke from a cast in the fight (KineticCarbine)
        ab.cast()
        while e.q and not e.over:
            t, _, fn, args = heapq.heappop(e.q)
            if t > POKE_S:
                break
            e.t = t
            fn(*args)
        for name, v in f.dmg_out.items():
            dmg[name] = dmg.get(name, 0.0) + k * land * v
            exp[name] = exp.get(name, 0.0) + k * land * v


def time_to_kill(attacker: Loadout, defender: Loadout, distance=15.0, max_time=60.0, rng=None, log=False,
                 mechanics=_UNSET):
    """Defender does not shoot or cast (its passive and reactive items still work). Returns FightResult;
    .time is the TTK (max_time if the defender survives)."""
    e = Engine(distance=distance, max_time=max_time, rng=rng, log=log, mech=mechanics)
    fa = make_fighter(e, attacker, "attacker")
    fb = make_fighter(e, defender, "defender")
    # a dummy stands still: it doesn't run away, parry or time Counterspell
    fb.skill = Skill(accuracy=0.0, headshot=0.0, use_abilities=False, use_actives=defender.skill.use_actives,
                     flee_hp=0.0, parry_rate=0.0, spell_parry_rate=0.0,
                     spell_parry_rate_ult=0.0)
    return e.run(fa, fb, one_way=True)
