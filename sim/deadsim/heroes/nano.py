"""Calico (hero_nano).

Assumptions:
- Gloom Bombs: on a landed throw BOMBS_ON_TARGET of the GrenadeCount bombs reach the target; the first deals
  full Damage, each further bomb MultiHitPenaltyPercentage %. Detonates after cast delay + Lifetime.
  T2 melee-resist shred stacks per bomb.
- Leaping Slash: dash (AbilityCastRange + engage margin) then a melee hit of ImpactDamage + 0.8 x light melee
  damage, heals HealAmount on hero hit; T3 refunds CooldownRefundPercent of the cooldown on hero hit.
- Ava: cat form deals no damage, so it is only used as a pre-fight approach (cast at fight start) and only
  with T3, assumed fully built up: +OutgoingDamagePercent outgoing damage (damage_amp) for DamageAmpDuration.
- Return to Shadows: Calico is untargetable and can't shoot for AbilityChannelTime; Damage on cast and again
  on return. T3 on completion heals HealAmount and refunds all other ability cooldowns.
"""
from deadsim.abilities import AbilityImpl, register

BOMBS_ON_TARGET = 0.75   # share of the cluster's bombs that reach a hero hit by the throw


@register("ability_nano_clustergrenade")
class GloomBombs(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return True    # thrown (TossSpeed), no cast range in data

    def cast(self, c):
        cd = c.raw("AbilityCastDelay")
        c.lock_gun(cd)
        delay = cd + c.raw("Lifetime")
        n = max(1.0, c.raw("GrenadeCount") * BOMBS_ON_TARGET)
        mult = 1.0 + (n - 1.0) * c.raw("MultiHitPenaltyPercentage", 100) / 100
        c.spirit_hit(c.val("Damage") * mult, delay=delay)
        if c.tier >= 2:
            hit = c.me.skill.spirit_accuracy
            for i in range(int(round(n))):
                c.debuff("melee_resist", c.raw("MeleeResistReduction") / 100 * hit,
                         c.dur("MeleeResistReductionDuration"), tag=("gloom_melee", i), delay=delay)


@register("ability_nano_dash")
class LeapingSlash(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay + 0.3)
        if not c.me.acc("leaping_slash").take(c.me.skill.spirit_accuracy):
            return
        c.melee_hit(c.val("ImpactDamage"), delay=delay)
        c.after(delay, c.heal, c.val("HealAmount"))
        if c.tier >= 3:
            refund = self.s.cooldown() * c.raw("CooldownRefundPercent") / 100
            self.s.ready_at -= refund
            self.s.next_charge = self.s.ready_at


@register("ability_nano_catform")
class Ava(AbilityImpl):
    kind = "self"

    def in_range(self, c):
        return True

    def should_cast(self, c):
        return c.tier >= 3 and self.s.casts == 0

    def cast(self, c):
        c.buff("damage_amp", c.raw("OutgoingDamagePercent") / 100, c.dur("DamageAmpDuration"))


@register("ability_nano_shadow_pulse")
class ReturnToShadows(AbilityImpl):
    kind = "aoe"

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.1

    def cast(self, c):
        T = c.raw("AbilityChannelTime")
        c.buff("invulnerable", 1, T)
        c.lock_gun(T)
        c.spirit_hit(c.val("Damage"))
        c.spirit_hit(c.val("Damage"), delay=T)
        if c.tier >= 3:
            c.after(T, self.complete, c)

    def complete(self, c):
        if not c.me.alive:
            return
        c.heal(c.raw("HealAmount"))
        for ab in c.me.abilities:
            if ab is not self.s:
                ab.reset_cooldown()
