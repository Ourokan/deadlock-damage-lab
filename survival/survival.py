"""Survival test: how long a hero's build stays alive against a real enemy build that never dies.

    import sys; sys.path[:0] = ["/mnt/project-files/sim", "/mnt/project-files/survival"]
    from survival import survive
    r = survive("Abrams", ["Extra Health", "Bullet Resilience"], souls=27000,
                enemy="Haze", enemy_items=["Mercurial Magnum", "Toxic Bullets"])
    r["time_alive"], r["damage_taken"], r["healing"], r["damage_dealt"]

Both sides act normally (gun, abilities on cooldown, actives, melee) at the hero's ranked median aim with real
ability landing and melee rates, at the mean of both heroes' real fight distances. The enemy refills to full HP
instead of dying, so the fight always ends with the tested hero's death (or at max_time). The tested hero still
shoots back, so lifesteal, on-hit healing and damage-taken effects all count.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "sim"))

from deadsim import Loadout, Skill  # noqa: E402
from deadsim.accuracy import default_distance, hero_default_skill  # noqa: E402
from deadsim.data import game  # noqa: E402
from deadsim.engine import Engine, kill_hooks  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
import dataclasses  # noqa: E402
from deadsim import mechanics  # noqa: E402

_skill, _dist = {}, {}


class _Refill:
    """Lethal damage refills the enemy (same trick as the damage tool's immortal dummy). A refill counts as a kill:
    the attacker's on-kill items fire (Healbane's heal)."""
    item = None
    name = "immortal"

    def __init__(self):
        self.kills = 0

    def on_lethal(self, f, attacker):
        self.kills += 1
        kill_hooks(attacker, f)
        f.hp = f.max_hp
        return True


def _sk(name, aim):
    k = (name, aim)
    if k not in _skill:
        _skill[k] = hero_default_skill(name, aim)
    return _skill[k]


def _d(name):
    if name not in _dist:
        _dist[name] = default_distance(name)
    return _dist[name]


def survive(hero, items, souls, enemy, enemy_items, enemy_souls=None, max_time=60.0, aim="p50", enemy_aim="p50",
            skill: Skill | None = None, enemy_skill: Skill | None = None, distance=None, focus=1.0, start_hp=None,
            enemy_start_hp=None, extra_targets=0.0, fight_length=None):
    """start_hp / enemy_start_hp: the fight starts with this much health (lane trades carry health over), else full.
    enemy_healed is the healing the enemy got (it undoes damage dealt), enemy_final_hp its health at the end with
    each refill counted in enemy_kills. extra_targets: other enemy heroes next to the target (Mechanics.extra_targets:
    Ricochet bounces and Split Shot pellets on them are booked in splash_dealt, not in damage_dealt).
    fight_length: a Mechanics.fight_length curve (deadsim.mechanics.real_length): damage_dealt, damage_by_source,
    splash_dealt and enemy_healed are then expected over real fight lengths (each hit x P(the fight still goes
    on), real fights mostly end in a disengage), damage_dealt_full keeps every hit; time_alive, survived and the
    damage taken are the fight's own."""
    G = game()
    hn, en = G.hero(hero).name, G.hero(enemy).name
    # movement off: running away would count as surviving, which isn't what this search measures
    mech = dataclasses.replace(mechanics.DEFAULT, movement=False, extra_targets=extra_targets,
                               fight_length=fight_length) if mechanics.DEFAULT else None
    e = Engine(distance=distance if distance is not None else (_d(hn) + _d(en)) / 2, max_time=max_time, mech=mech)
    me = make_fighter(e, Loadout(hero, list(items), souls=souls, skill=skill or _sk(hn, aim)), "me")
    foe = make_fighter(e, Loadout(enemy, list(enemy_items), souls=enemy_souls or souls,
                                  skill=enemy_skill or _sk(en, enemy_aim)), "enemy")
    if start_hp is not None:
        me.hp = max(1.0, min(start_hp, me.max_hp))
    if enemy_start_hp is not None:
        foe.hp = max(1.0, min(enemy_start_hp, foe.max_hp))
    refill = _Refill()
    foe.items_fx.append(refill)
    foe.st.outgoing_mult *= focus
    max_hp = me.max_hp
    r = e.run(me, foe)
    t = me.death_time if me.death_time is not None else max_time
    taken = dict(me.dmg_in)
    return {
        "time_alive": round(t, 2),
        "survived": me.death_time is None,
        "max_hp": round(max_hp),
        "final_hp": round(max(0.0, me.hp), 1),
        "damage_taken": round(sum(taken.values()), 1),
        "damage_taken_by_source": {k: round(v, 1) for k, v in sorted(taken.items(), key=lambda x: -x[1])},
        "healing": round(getattr(me, "healed", 0.0) or 0.0, 1),
        # expected over real fight lengths like damage_dealt (the enemy's hits on me x P(the fight still goes on))
        "damage_taken_exp": round(sum(foe.dmg_exp.values()), 1),
        "healing_exp": round(me.healed_exp, 1),
        "damage_dealt": round(sum(me.dmg_exp.values()), 1),
        "damage_dealt_full": round(sum(me.dmg_out.values()), 1),
        "damage_by_source": {k: round(v, 1) for k, v in me.dmg_exp.items() if v},
        "splash_dealt": round(sum(me.counters.get("splash_exp", {}).values()), 1),
        "splash_by_source": {k: round(v, 1) for k, v in me.counters.get("splash_exp", {}).items() if v},
        "regen": me.st.health_regen, "ooc_regen": me.st.ooc_regen, "regen_amp": me.st.heal_amp,
        "heal_amp_cast": me.st.heal_amp_cast,
        "enemy_healed": round(foe.healed_exp, 1),
        "enemy_final_hp": round(max(0.0, foe.hp), 1),
        "enemy_max_hp": round(foe.max_hp),
        "enemy_kills": refill.kills,
        "enemy": {"regen": foe.st.health_regen, "ooc_regen": foe.st.ooc_regen, "regen_amp": foe.st.heal_amp,
                  "heal_amp_cast": foe.st.heal_amp_cast, "max_hp": round(foe.max_hp)},
    }
