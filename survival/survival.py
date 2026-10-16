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
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
import dataclasses  # noqa: E402
from deadsim import mechanics  # noqa: E402

_skill, _dist = {}, {}


class _Refill:
    """Lethal damage refills the enemy (same trick as the damage tool's immortal dummy)."""
    item = None
    name = "immortal"

    def on_lethal(self, f, attacker):
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
            skill: Skill | None = None, enemy_skill: Skill | None = None, distance=None, focus=1.0):
    G = game()
    hn, en = G.hero(hero).name, G.hero(enemy).name
    # movement off: running away would count as surviving, which isn't what this search measures
    mech = dataclasses.replace(mechanics.DEFAULT, movement=False) if mechanics.DEFAULT else None
    e = Engine(distance=distance if distance is not None else (_d(hn) + _d(en)) / 2, max_time=max_time, mech=mech)
    me = make_fighter(e, Loadout(hero, list(items), souls=souls, skill=skill or _sk(hn, aim)), "me")
    foe = make_fighter(e, Loadout(enemy, list(enemy_items), souls=enemy_souls or souls,
                                  skill=enemy_skill or _sk(en, enemy_aim)), "enemy")
    foe.items_fx.append(_Refill())
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
        "damage_dealt": round(sum(me.dmg_out.values()), 1),
    }
