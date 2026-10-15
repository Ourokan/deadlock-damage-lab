"""Kelvin (hero_kelvin).

Assumptions:
- Frost Grenade: thrown at the enemy; it heals Kelvin only when he stands inside the cloud (distance <= Radius).
  The slow is movement only.
- Ice Path: no combat effect without upgrades (never cast then). With T1 Kelvin gets +35% bullet resist, with
  T3 +35% spirit resist and +20 spirit power, for the whole duration (assumed on the path the whole time).
- Arctic Beam: channel for AbilityDuration, no gun meanwhile; uptime on target = caster's spirit accuracy.
  Fire-rate slow ramps linearly to MaxFireRateSlowPercent over MaxSlowTime and lingers SlowDuration.
  A stun breaks the channel.
- Frozen Shelter: cast on himself below SHELTER_HP. With the enemy outside the dome (distance > Radius) the
  dome blocks all damage both ways (Kelvin invulnerable, gun locked) for SHELTER_BLOCK of the duration;
  Kelvin regenerates BonusHealthRegen per second. T3 purges Kelvin's debuffs.
"""
from deadsim.abilities import AbilityImpl, register

SHELTER_HP = 0.35
SHELTER_BLOCK = 1.0     # share of the dome duration the enemy stays outside (can't damage Kelvin)
ENEMY_DEBUFFS = ("stun", "silence", "disarm", "item_silence", "damage_taken_amp", "spirit_amp_taken",
                 "bullet_amp_taken", "bullet_shred", "spirit_shred", "fire_rate_slow", "outgoing_penalty",
                 "spirit_outgoing_penalty", "crit_taken")


@register("ability_ice_grenade")
class FrostGrenade(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        c.spirit_hit(c.val("Damage"), delay=delay)
        if c.dist <= c.rng("Radius"):
            c.heal(c.val("HealAmount"))


@register("ability_icepath")
class IcePath(AbilityImpl):
    kind = "self"

    def in_range(self, c):
        return True

    def should_cast(self, c):
        return c.tier >= 1

    def cast(self, c):
        d = c.dur("AbilityDuration")
        if c.tier >= 1:
            c.buff("bullet_resist", c.raw("BulletResist") / 100, d)
        if c.tier >= 3:
            c.buff("spirit_resist", c.raw("BonusSpiritPct") / 100, d)
            c.buff("spirit_power", c.raw("BonusSpirit"), d)


@register("ability_icebeam")
class ArcticBeam(AbilityImpl):
    kind = "skillshot"
    range_props = ("PathLength",)

    def cast(self, c):
        T = c.dur("AbilityDuration")
        c.lock_gun(T)
        st = c.state
        st["start"], st["end"] = c.now, c.now + T
        c.after(c.raw("TickRate", 0.1), self.tick, c)

    def tick(self, c):
        st = c.state
        tick = c.raw("TickRate", 0.1)
        if not c.me.alive or not c.foe.alive or c.now > st["end"] + 1e-9:
            return
        if c.me.mods.active("stun"):
            c.me.gun_locked_until = c.now
            return
        up = c.me.skill.spirit_accuracy
        c.engine.damage(c.me, c.foe, c.val("DPS") * tick * up, "spirit", self.s.ab.name,
                        is_ability=True, ability=self.s, is_dot=True)
        ramp = min(1.0, (c.now - st["start"]) / max(0.1, c.raw("MaxSlowTime", 2.0)))
        slow = c.raw("MaxFireRateSlowPercent") / 100 * ramp * up
        c.debuff("fire_rate_slow", slow, tick + c.dur("SlowDuration"))
        c.after(tick, self.tick, c)


@register("ability_ice_dome")
class FrozenShelter(AbilityImpl):
    kind = "self"

    def in_range(self, c):
        return True

    def should_cast(self, c):
        return c.me.hp_frac < SHELTER_HP and c.foe.alive

    def cast(self, c):
        delay = c.raw("AbilityCastDelay") + c.raw("GrowTime")
        d = c.dur("AbilityDuration")
        if c.tier >= 3:
            for key in ENEMY_DEBUFFS:
                c.me.mods.d.pop(key, None)
        if c.dist > c.rng("Radius"):
            block = d * SHELTER_BLOCK
            c.after(delay, lambda: c.buff("invulnerable", 1, block))
            c.lock_gun(delay + block)
        c.after(delay, lambda: c.buff("regen", c.val("BonusHealthRegen"), d))
