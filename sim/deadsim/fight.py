"""High-level API: describe two loadouts, run a duel or a one-way time-to-kill.

    from deadsim import Loadout, duel, time_to_kill
    a = Loadout("Infernus", ["Extra Spirit", "Mystic Burst", "Toxic Bullets"], souls=12000)
    b = Loadout("Haze", ["Rapid Rounds", "Swift Striker"], souls=12000)
    print(duel(a, b, distance=15).summary())
"""
from __future__ import annotations

import bisect
import dataclasses
import json
import os
from dataclasses import dataclass, field
from functools import lru_cache

from .abilities import AbilityState, load_heroes
from .build import compute_stats
from .data import game, DATA_DIR
from .engine import Engine, Fighter, Skill, _UNSET
from . import items_fx

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


@dataclass
class Loadout:
    hero: object
    items: list = field(default_factory=list)
    souls: float | None = None              # net worth; defaults to the items' total cost
    level: int | None = None
    skill: Skill = field(default_factory=Skill)
    tiers: list | None = None                # upgrades bought per ability [t1, t2, t3, t4] (0-3); None = auto
    unlocked: list | None = None             # [bool]*4; None = auto from souls
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


def make_fighter(engine, lo: Loadout, name=None):
    load_heroes()
    hero, items = lo.resolve()
    st = compute_stats(hero, items, lo.souls, lo.level)
    skill = lo.skill
    if engine.mech is not None and skill.ability_landing_mech:
        skill = dataclasses.replace(skill, ability_landing=skill.ability_landing_mech)
    f = Fighter(engine, name or lo.name or hero.name, st, skill)
    tiers, unlocked = _auto_abilities(hero, st.souls)
    if lo.tiers is not None:
        tiers = list(lo.tiers)
    if lo.unlocked is not None:
        unlocked = list(lo.unlocked)
    imbue_map = {}
    for it in items:
        if it.class_name in IMBUE_CLASSES:
            idx = lo.imbues.get(it.name, lo.imbues.get(it.class_name))
            if idx is None:
                idx = _default_imbue_target(hero, unlocked)
            imbue_map.setdefault(idx, []).append(it)
    for i, ab in enumerate(hero.abilities):
        f.abilities.append(AbilityState(f, ab, tiers[i] if i < len(tiers) else 0,
                                        unlocked[i] if i < len(unlocked) else True, imbue_map.get(i, ())))
    items_fx.attach(f, items)
    if engine.mech is not None:
        from . import mechanics
        mechanics.attach(f, items)
    return f


def duel(a: Loadout, b: Loadout, distance=15.0, max_time=30.0, rng=None, log=False, mechanics=_UNSET):
    """Both sides fight until one dies or max_time passes. mechanics: deadsim.mechanics.Mechanics (parry, summons,
    movement, nearby enemies) or None for the earlier model; unset = mechanics.DEFAULT."""
    e = Engine(distance=distance, max_time=max_time, rng=rng, log=log, mech=mechanics)
    fa = make_fighter(e, a, (a.name or game().hero(a.hero).name) + " (A)")
    fb = make_fighter(e, b, (b.name or game().hero(b.hero).name) + " (B)")
    return e.run(fa, fb)


def time_to_kill(attacker: Loadout, defender: Loadout, distance=15.0, max_time=60.0, rng=None, log=False,
                 mechanics=_UNSET):
    """Defender does not shoot or cast (its passive and reactive items still work). Returns FightResult;
    .time is the TTK (max_time if the defender survives)."""
    e = Engine(distance=distance, max_time=max_time, rng=rng, log=log, mech=mechanics)
    fa = make_fighter(e, attacker, "attacker")
    fb = make_fighter(e, defender, "defender")
    fb.skill = Skill(accuracy=0.0, headshot=0.0, use_abilities=False, use_actives=defender.skill.use_actives)
    return e.run(fa, fb, one_way=True)
