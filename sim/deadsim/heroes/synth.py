"""Pocket (hero_synth).

Assumptions:
- Barrage: the ProjectileAmount projectiles are spread evenly over the channel; Pocket can't shoot while
  channelling (modeled as a self-silence so nothing else is cast meanwhile). Each landed projectile adds one amp stack (AmpPercentPerStack, damage_amp on all outgoing damage) that lasts
  AmpDuration from the latest hit. Lobbed long-range attack: usable out to BARRAGE_RANGE.
- Flying Cloak: one hit of Damage on the target (it passes through once). Travels ~CLOAK_RANGE. T2 "+5 Weapon
  Damage" is read as +5% weapon damage (doubtful: tooltip unit unclear). Teleport is movement (ignored).
- Enchanter's Satchel: Pocket is invulnerable and can't shoot for the full channel, then deals Damage (radius 12).
  T3 slow uses the data FireRateSlow (40%) rather than the tooltip's 32%.
- Affliction: non-lethal, proc-less DoT for DebuffDuration. T3 (+13 DPS, +0.1 spirit scaling) comes from the
  data via c.val; T3 also blocks all healing.
"""
from deadsim.abilities import AbilityImpl, register

BARRAGE_RANGE = 30.0      # m, lobbed projectiles (no range in data)
CLOAK_RANGE = 25.0        # m, cloak travel distance (no range in data)


@register("synth_barrage")
class Barrage(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.dist <= BARRAGE_RANGE

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        chan = c.dur("AbilityChannelTime", 2.0)
        n = max(1, int(c.raw("ProjectileAmount", 4)))
        c.lock_gun(delay + chan)
        c.buff("silence", 1, delay + chan, tag="barrage_channel")   # no other casts while channelling
        dmg = c.val("DamagePerProjectile")
        acc = c.me.skill.spirit_accuracy
        for i in range(n):
            c.after(delay + chan * (i + 0.5) / n, self.projectile, c, dmg, acc)

    def projectile(self, c, dmg, acc):
        if not (c.me.alive and c.foe.alive):
            return
        c.spirit_hit(dmg)
        st = c.state
        if c.now > st.get("amp_until", -1):
            st["stacks"] = 0.0
        st["stacks"] = st.get("stacks", 0.0) + acc
        d = c.dur("AmpDuration")
        st["amp_until"] = c.now + d
        c.buff("damage_amp", c.raw("AmpPercentPerStack") / 100 * st["stacks"], d, tag="barrage_amp")


@register("synth_plasma_flux")
class FlyingCloak(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.dist <= CLOAK_RANGE

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        c.spirit_hit(c.val("Damage"), delay=delay)
        if c.tier >= 2:
            c.buff("weapon_pct", c.raw("WeaponDamageBonus") / 100, c.dur("WeaponDamageBonusDuration"))


@register("synth_pulse")
class EnchantersSatchel(AbilityImpl):
    kind = "aoe"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        chan = c.dur("AbilityChannelTime", 1.5)
        c.lock_gun(delay + chan)
        c.buff("invulnerable", 1, delay + chan, tag="satchel")
        c.buff("silence", 1, delay + chan, tag="satchel_channel")   # any action would end the satchel early
        c.spirit_hit(c.val("Damage"), delay=delay + chan)
        if c.tier >= 3:
            c.debuff("fire_rate_slow", c.raw("FireRateSlow") / 100, c.dur("DebuffDuration"), delay=delay + chan)


@register("synth_affliction")
class Affliction(AbilityImpl):
    kind = "aoe"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        dps = c.val("DPS")
        d = c.dur("DebuffDuration")
        f, e, s = c.me, c.foe, self.s
        c.after(delay, lambda: e.alive and f.e.dot(f, e, dps, d, s.ab.name, tick=c.raw("DamageInterval", 0.5),
                                                    is_ability=True, ability=s, is_ult=True,
                                                    nonlethal=True, procs=False))
        if c.raw("DisableHealing"):
            c.debuff("heal_received", -1.0, d, delay=delay)
