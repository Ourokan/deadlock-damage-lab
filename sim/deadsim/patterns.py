"""Per-hero fight behaviour: cast priority, setup before the ultimate, and abilities used before the fight starts.

Without this the sim casts every ready ability in slot order (1, 2, 3, ult). Real players open with a set combo:
Mo & Krill arrive under Burrow and Combo the target once it is knocked up, Seven stuns with Static Charge before
Storm Cloud, Warden roots with Binding Word before Last Stand. data/fight_patterns.json holds, per hero:

- order: ability class names in cast priority. Abilities not listed follow in slot order. Each hero file's own
  should_cast (range, health thresholds, heals when hurt) still decides whether an ability is cast at all.
- ult_after: the ultimate waits until one of these setup abilities was cast this fight. It stops waiting when no
  listed setup ability is ready (locked or on cooldown), when the target or the caster is below LOW_HP, or SETUP_WAIT
  s into the fight (every fight starts at t=0). A setup that is ready but out of range still holds the ult: players
  walk into range for it, and releasing the ult there fits the real damage mix worse (Lash, Bebop).
- prefight: an ability used to approach before the fight. At t=0 its impl's prefight(c) runs instead of cast(c),
  and its cooldown counts from impl.prefight_lead(c) s before the fight. Abilities without a prefight hook simply
  sit first in `order`.

Skill.fight_pattern=False keeps the old slot-order behaviour.
"""
from __future__ import annotations

import json
import os
import warnings
from functools import lru_cache

PATTERNS = os.path.join(os.path.dirname(__file__), "..", "data", "fight_patterns.json")
SETUP_WAIT = 4.0      # s the ultimate waits for its setup before it is cast anyway
LOW_HP = 0.3          # target (finish it) or caster (use it now) below this health share: no waiting


@lru_cache(maxsize=1)
def _load():
    """The patterns file is part of the sim: a missing or malformed file raises instead of silently falling back."""
    with open(PATTERNS) as fh:
        return json.load(fh)["heroes"]


def pattern(hero_id):
    return _load().get(str(hero_id))


class Plan:
    def __init__(self, f, row):
        self.f = f
        by_class = {a.ab.class_name: a for a in f.abilities}
        listed = row.get("order", []) + row.get("ult_after", []) + ([row["prefight"]] if row.get("prefight") else [])
        gone = [c for c in listed if c not in by_class]
        if gone:   # a patch renamed or removed an ability: rebuild data/fight_patterns.json
            warnings.warn(f"fight_patterns.json: {row.get('name')} lists abilities it no longer has: {gone}")
        first = [by_class[c] for c in row.get("order", []) if c in by_class]
        self.order = first + [a for a in f.abilities if a not in first]
        self.after = [by_class[c] for c in row.get("ult_after", []) if c in by_class]
        self.prefight = by_class.get(row.get("prefight"))

    def allows(self, st):
        """Extra gate on top of the ability's own should_cast."""
        if not st.ab.ultimate or not self.after:
            return True
        f = self.f
        if any(a.casts for a in self.after) or f.e.t >= SETUP_WAIT:
            return True
        if f.hp_frac < LOW_HP or (f.enemy is not None and f.enemy.hp_frac < LOW_HP):
            return True
        return not any(_castable(a) for a in self.after)


def _castable(a):
    """Is this ability ready (unlocked and a charge off cooldown)?"""
    if not a.unlocked or a.impl.kind == "passive":
        return False
    a._recharge()
    return a.charges > 0 and a.f.e.t >= a.ready_at


def attach(f, hero_id):
    """Give the fighter its hero's plan (f.plan, f.cast_order) unless the skill turns patterns off."""
    row = pattern(hero_id) if getattr(f.skill, "fight_pattern", True) else None
    if not row:
        return
    f.plan = Plan(f, row)
    f.cast_order = f.plan.order


def fight_start(f):
    """Run the prefight ability (once, at t=0) if the hero has one and it is unlocked."""
    plan = getattr(f, "plan", None)
    st = plan.prefight if plan else None
    if st is None or not st.unlocked or not f.skill.use_abilities or not hasattr(st.impl, "prefight"):
        return
    st.prefight()
