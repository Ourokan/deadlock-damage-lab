"""Drifter (hero_drifter).

Assumptions:
- Rend: cone swipe (AbilityCastRange) dealing BonusDamage spirit damage (the only damage value in the data). If
  the target is within RangeForBonusDamage (+ engage margin: Drifter closes in) it also takes a light melee hit
  (hero light melee damage + per-boon growth, melee bonuses applied); T3 swaps that for the DamageHeavyMelee scale (0.55) x heavy
  melee damage (heavy grows with boons in proportion to light) and silences for DebuffDuration. Drifter can't shoot during cast + post-cast.
- Stalker's Mark: skillshot (reach MARK_RANGE) bleed for AbilityDuration dealing DotHealthPercent % of the
  target's max health per second (spirit scaling adds to the percent). T1 bullet shred and T3 healing penalty
  last for the bleed. The teleport is movement (ignored).
- Bloodscent: in a 1v1 the target is always isolated, so Drifter permanently deals AmpDamagePercent more damage.
  The extra is booked as its own "Bloodscent" hit (as the game's damage report does) after each damaging hit that
  procs on-hit effects, unresisted since the amplified hit was already resisted. Kill rewards don't matter here.
- Eternal Night: darkness only limits vision beyond SmallVisionDistance and makes the target isolated (already
  always true in a 1v1). Within SmallVisionDistance it has no combat effect, so it is only cast when the fight is
  farther than that; then the blinded target misses DARK_MISS of its shots at Drifter (evasion) for the duration.
"""
from deadsim.abilities import AbilityImpl, register

MARK_RANGE = 30.0     # m, Stalker's Mark projectile reach (no range in data)
DARK_MISS = 0.5       # share of shots a darkness-blinded target misses beyond its vision distance (guess)


@register("drifter_blood_blast")
class Rend(AbilityImpl):
    kind = "aoe"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay + c.raw("AbilityPostCastDuration"))
        c.spirit_hit(c.val("BonusDamage"), delay=delay)
        if c.dist <= c.rng("RangeForBonusDamage") + c.me.skill.engage_margin:
            melee = c.light_melee()
            if c.raw("UseHeavyMelee"):   # T3: DamageHeavyMelee is a scale-only upgrade (x heavy melee damage)
                base = c.me.st.hero.base
                heavy = base.get("heavy_melee_damage", 0.0) * melee / max(1.0, base.get("light_melee_damage", 1.0))
                melee = heavy * c.scale("DamageHeavyMelee")
            c.melee_hit(melee, delay=delay)
            if c.raw("DebuffDuration"):
                c.debuff("silence", 1, c.raw("DebuffDuration"), delay=delay)


@register("drifter_shadow_mark")
class StalkersMark(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(MARK_RANGE)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        d = c.dur("AbilityDuration")
        acc = c.me.skill.spirit_accuracy
        pct = c.val("DotHealthPercent") / 100
        dps = pct * c.foe.max_hp
        c.dot(dps, d, delay=delay, tick=c.raw("TickRate", 0.5), hit_chance=acc)
        if c.raw("BulletResistReduction"):
            c.debuff("bullet_shred", abs(c.raw("BulletResistReduction")) / 100 * acc, d, delay=delay)
        if c.raw("HealAmpReceivePenaltyPercent"):
            c.debuff("heal_received", c.raw("HealAmpReceivePenaltyPercent") / 100 * acc, d, delay=delay)


@register("ability_drifter_hunger")
class Bloodscent(AbilityImpl):
    kind = "passive"

    def on_damage_dealt(self, c, target, hit):
        if hit.source == self.s.ab.name or hit.amount <= 0 or not target.alive:
            return
        f = c.me
        # book the amplified part under Bloodscent (as the game does); undo the generic multipliers that
        # Engine.damage applies again so the extra is exactly AmpDamagePercent of the hit
        mult = (f.st.outgoing_mult * (1.0 - f.stat("outgoing_penalty")) * (1.0 + f.stat("damage_amp"))
                * (1.0 + target.stat("damage_taken_amp")))
        extra = hit.amount * c.raw("AmpDamagePercent") / 100 / max(1e-6, mult)
        c.engine.damage(f, target, extra, "pure", self.s.ab.name, is_ability=True, ability=self.s, procs=False)


@register("drifter_darkness")
class EternalNight(AbilityImpl):
    kind = "self"

    def should_cast(self, c):
        return c.dist > c.raw("SmallVisionDistance", 15)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        c.after(delay, lambda: c.buff("evasion", DARK_MISS, c.dur("AbilityDuration"), tag="eternal_night"))
