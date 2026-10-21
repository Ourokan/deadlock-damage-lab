"""Damage test against a configurable dummy: the entry point the web page (step 4) exposes.

    import sys; sys.path[:0] = ["/mnt/project-files/sim", "/mnt/project-files/damage"]
    from dummy import Dummy, damage_test
    from deadsim import Skill

    d = Dummy(hp=3000, bullet_resist=0.25, spirit_resist=0.1)                    # plain stats
    d = Dummy(hero="Abrams", items=["Bullet Resilience", "Extra Health"], souls=27000)  # a real build as dummy
    r = damage_test("Haze", ["Mercurial Magnum", "Toxic Bullets"], souls=27000, dummy=d)
    r["damage"]          # {"5s": ..., "15s": ..., "30s": ...} damage dealt by each mark
    r["dps"], r["sources"], r["timeline"]   # DPS per mark, damage by source, cumulative damage every 0.5 s

The dummy never shoots or casts. Its items' passive stats and reactive effects (resists, barriers, damage
reduction) apply; their actives don't. With `immortal=True` (default) lethal damage refills it, so damage keeps
counting; with False the run stops when it dies and `r["kill_time"]` is set. Numbers given in Dummy override what
the hero and items would give: `hp` replaces max HP, each `*_resist` (0-1) replaces that resist entirely.
Attacker aim: `skill` (deadsim Skill) or `aim` percentile of the hero's ranked players (p25/p50/p75/p90).
Attacker abilities: the popular real order by default; `ability_order` (ability ids, Deadlock API format) follows that
order instead, as far as the net worth's ability points go (deadsim.fight.abilities_for_order).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from deadsim import Loadout, Skill
from deadsim.accuracy import default_distance, hero_default_skill
from deadsim.data import game
from deadsim.engine import Engine
from deadsim.fight import make_fighter


@dataclass
class Dummy:
    hp: float | None = None                 # None = from hero + items + souls
    bullet_resist: float | None = None      # 0-1; None = from items
    spirit_resist: float | None = None
    melee_resist: float | None = None
    items: list = field(default_factory=list)
    hero: str | int = "Haze"                # base stats and hitbox only; abilities are removed
    souls: float | None = None              # None = the attacker's souls
    immortal: bool = True
    zone_exit_s: float | None = None        # walks out of ground zones (Alchemical Fire) after this long; None = stays


class _Refill:
    item = None
    name = "dummy"

    def on_lethal(self, f, attacker):
        f.hp = f.max_hp
        return True


def damage_test(hero, items, souls=None, dummy: Dummy | None = None, skill: Skill | None = None, aim="p50",
                marks=(5.0, 15.0, 30.0), distance=None, tiers=None, imbues=None, ability_order=None):
    G = game()
    dummy = dummy or Dummy()
    hname = G.hero(hero).name
    skill = skill or hero_default_skill(hname, aim)
    t_max = max(marks)
    e = Engine(distance=distance if distance is not None else default_distance(hname), max_time=t_max)
    a = make_fighter(e, Loadout(hero, list(items), souls=souls, skill=skill, tiers=tiers, imbues=imbues or {},
                                   ability_order=ability_order),
                     "attacker")
    d = make_fighter(e, Loadout(dummy.hero, list(dummy.items), souls=dummy.souls or a.st.souls,
                                skill=Skill(accuracy=0, headshot=0, use_abilities=False, use_actives=False,
                                            zone_exit_s=dummy.zone_exit_s)), "dummy")
    d.abilities = []
    if dummy.immortal:
        d.items_fx.append(_Refill())
    for attr, v in (("bullet_resist", dummy.bullet_resist), ("spirit_resist", dummy.spirit_resist),
                    ("melee_resist", dummy.melee_resist)):
        if v is not None:
            setattr(d.st, attr, [v] if v else [])
    if dummy.hp is not None:
        d.max_hp_base = d.hp = dummy.hp
    got, timeline = {}, []
    for t in marks:
        if t < t_max:
            e.at(t, lambda t=t: got.__setitem__(t, sum(a.dmg_out.values())))
    step = 0.5
    for k in range(1, int(t_max / step) + 1):
        e.at(k * step, lambda k=k: timeline.append((round(k * step, 2), round(sum(a.dmg_out.values()), 1))))
    e.run(a, d, one_way=True)
    total = sum(a.dmg_out.values())
    for t in marks:
        got.setdefault(t, total)
    return {
        "damage": {f"{t:g}s": round(v, 1) for t, v in got.items()},
        "dps": {f"{t:g}s": round(v / t, 1) for t, v in got.items()},
        "sources": {k: round(v, 1) for k, v in sorted(a.dmg_out.items(), key=lambda x: -x[1])},
        "timeline": timeline,
        "kill_time": d.death_time,
        "dummy_max_hp": round(d.max_hp), "attacker_souls": a.st.souls,
    }
