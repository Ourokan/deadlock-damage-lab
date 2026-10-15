"""Yamato (hero_yamato).

Assumptions:
- Power Slash: always channelled to full charge (AbilityCastDelay 1.4 s, gun locked, BulletResist during the
  channel), then FullChargeDamage along SlashLength (skillshot). A stun during the channel cancels it.
  T3 (+150 damage, +0.5 spirit scaling) comes from the data via c.val. T1 slow skipped.
- Flying Slash: grapple to the target in AbilityCastRange, then one melee strike. The data has no damage number,
  so it deals one light melee (c.light_melee(), melee bonuses apply). T2: +SpiritBonus spirit power for
  BuffDuration. The slow is skipped.
- Crimson Slash: cone of Radius in front, assumed to hit. Damage + fire-rate slow for DebuffDuration; on hit heals
  HealFixedHealth (+ healing spirit scale) + T2 HealMaxHealth% of max health. T1 melee buff applied. T3
  "increased scaling" (Damage +0.6, HealFixedHealth +0.4) comes from the data via c.val.
- Shadow Transformation: AbilityChannelTime invulnerable transformation (can't shoot), then refreshes the other
  abilities, gives bullet/spirit resist, T1 weapon damage, and abilities 60% faster (cdr 1 - 1/1.6 on casts made
  during the form) for AbilityDuration. Status immunity: stun/silence/disarm/slows on Yamato are purged every
  0.1 s while in shadow form. Cast once two other abilities are on cooldown (so the refresh is worth something).
  Kill extension / heal are irrelevant in a 1v1.
"""
from deadsim.abilities import AbilityImpl, register

NEG_STATUS = ("stun", "silence", "disarm", "immobilize", "fire_rate_slow", "item_silence")


def busy(c):
    """Mid channel / cast animation: no other ability can be started."""
    return c.now < c.me.gun_locked_until


@register("citadel_ability_power_slash")
class PowerSlash(AbilityImpl):
    kind = "skillshot"
    range_props = ("SlashLength",)

    def should_cast(self, c):
        return not busy(c) and self.in_range(c)

    def cast(self, c):
        ch = c.raw("AbilityCastDelay", 1.4)
        c.lock_gun(ch + c.raw("AbilityPostCastDuration"))
        c.buff("bullet_resist", c.raw("BulletResist") / 100, ch, tag="powerslash_br")
        dmg = c.val("FullChargeDamage")
        n = max(1, int(round(ch / 0.1)))

        def step(i):
            if not c.me.alive or not c.foe.alive:
                return
            if c.me.mods.active("stun"):
                return   # channel interrupted
            if i + 1 < n:
                c.after(ch / n, step, i + 1)
            else:
                c.spirit_hit(dmg)
        c.after(ch / n, step, 0)


@register("citadel_ability_flying_strike")
class FlyingSlash(AbilityImpl):
    kind = "target"

    def should_cast(self, c):
        return not busy(c) and self.in_range(c)

    def cast(self, c):
        travel = min(1.0, c.dist / 30.0)   # hook + reel in
        c.lock_gun(travel + c.raw("AbilityPostCastDuration"))
        c.melee_hit(c.light_melee(), delay=travel)
        if c.raw("SpiritBonus"):
            c.buff("spirit_power", c.raw("SpiritBonus"), c.dur("BuffDuration"), tag="flying_slash_sp")


@register("citadel_ability_healing_slash")
class CrimsonSlash(AbilityImpl):
    kind = "aoe"
    range_props = ("Radius",)

    def should_cast(self, c):
        return not busy(c) and self.in_range(c)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay + c.raw("AbilityPostCastDuration"))
        c.spirit_hit(c.val("Damage"), delay=delay)
        c.debuff("fire_rate_slow", c.raw("FireRateSlow") / 100, c.dur("DebuffDuration"), delay=delay)
        heal = c.val("HealFixedHealth") + c.me.max_hp * c.raw("HealMaxHealth") / 100

        def on_hit():
            if not c.me.alive:
                return
            c.heal(heal)
            if c.raw("BuffMeleeDamage"):
                c.buff("melee_pct", c.raw("BuffMeleeDamage") / 100, c.dur("BuffDuration"), tag="crimson_melee")
        c.after(delay, on_hit)


@register("citadel_ability_infinity_slash")
class ShadowTransformation(AbilityImpl):
    kind = "self"

    def should_cast(self, c):
        others = [a for a in c.me.abilities if a is not self.s and a.unlocked and a.impl.kind != "passive"]
        on_cd = sum(1 for a in others if a.ready_at > c.now + 2.0)
        return not busy(c) and (on_cd >= 2 or c.me.hp_frac < 0.35)

    def cast(self, c):
        ch = c.raw("AbilityChannelTime", 1.5)
        dur = c.dur("AbilityDuration")
        c.lock_gun(ch)
        c.buff("invulnerable", 1, ch, tag="shadow_transform")

        def begin():
            if not c.me.alive:
                return
            for a in c.me.abilities:
                if a is not self.s:
                    a.reset_cooldown()
            c.buff("bullet_resist", c.raw("BulletResist") / 100, dur, tag="shadow_br")
            c.buff("spirit_resist", c.raw("TechResist") / 100, dur, tag="shadow_sr")
            c.buff("cdr", 1.0 - 1.0 / (1.0 + c.raw("AbilitySpeedPct") / 100), dur, tag="shadow_cdr")
            if c.raw("WeaponDamageBonus"):
                c.buff("weapon_pct", c.raw("WeaponDamageBonus") / 100, dur, tag="shadow_wp")
            purge(c.now + dur)

        def purge(until):
            if c.now > until or not c.me.alive:
                return
            for k in NEG_STATUS:
                c.me.mods.d.pop(k, None)
            for k in ("weapon_pct", "spirit_power"):
                for tg, (v, exp) in list(c.me.mods.d.get(k, {}).items()):
                    if v < 0:
                        del c.me.mods.d[k][tg]
            c.after(0.1, purge, until)
        c.after(ch, begin)
