"""Warden (hero_warden).

Assumptions:
- Alchemical Flask: skillshot projectile, thrown up to THROW_RANGE. Damage + weapon damage debuff
  (WeaponPowerDebuff, additive weapon %, as weapon_pct on the target) for DebuffDuration; T3 adds FireRateSlow.
  Move slow / stamina loss skipped.
- Willpower: barrier (CombatBarrier) for AbilityDuration; T3 adds status resist. T3 "improved barrier scaling" (+2.1 spirit
  scaling on CombatBarrier) comes from the data via c.val. Cast only once Warden has lost HURT_HP of health
  (it is a reactive shield).
- Binding Word: 2.8 s later the target is damaged + immobilized unless it escaped EscapeRange (20 m) in time; we
  assume it lands BIND_LAND of the time (also times the caster's spirit accuracy, it's an aimed curse).
  Immobilize is movement-only. T1: +20% bullet damage taken for BulletArmorReductionDuration on landing.
  T3: target is silenced for the escape window.
- Last Stand: 2 s charge, then pulses every PulseInterval for AbilityDuration, healing HealthStealPctHero% of
  damage dealt. Bullet/spirit resist (incl. T3 +30%) applies during charge and channel. Warden can't shoot.
  Before T3 (unstoppable) a stun on Warden cancels the remaining pulses. Cast when the target is within Radius
  (+ engage margin) and not almost dead.
"""
from deadsim.abilities import AbilityImpl, register

THROW_RANGE = 30.0
HURT_HP = 0.85
BIND_LAND = 0.7


class _Base(AbilityImpl):
    """No new cast while another cast/channel has the gun locked."""

    def should_cast(self, c):
        return c.now >= c.me.gun_locked_until and self.cond(c)

    def cond(self, c):
        return self.in_range(c)


@register("ability_warden_crowd_control")
class AlchemicalFlask(_Base):
    kind = "skillshot"

    def in_range(self, c):
        return c.dist <= THROW_RANGE

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        if not c.me.acc("warden_flask").take(c.me.skill.spirit_accuracy, 1):
            return
        c.spirit_hit(c.val("Damage"), delay=delay, hit_chance=1.0)
        d = c.dur("DebuffDuration")
        c.debuff("weapon_pct", -abs(c.raw("WeaponPowerDebuff")) / 100, d, delay=delay)
        if c.raw("FireRateSlow"):
            c.debuff("fire_rate_slow", c.raw("FireRateSlow") / 100, d, delay=delay)


@register("ability_warden_high_alert")
class Willpower(_Base):
    kind = "self"

    def cond(self, c):
        return c.me.hp_frac < HURT_HP

    def cast(self, c):
        d = c.dur("AbilityDuration")
        c.barrier(c.val("CombatBarrier"), d)
        if c.raw("StatusResistancePercent"):
            c.buff("status_resist", c.raw("StatusResistancePercent") / 100, d)


@register("ability_warden_lock_down")
class BindingWord(_Base):
    kind = "target"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        esc = c.raw("EscapeTime", 2.8)
        c.lock_gun(delay)
        if c.raw("SilenceDebuff"):
            c.debuff("silence", 1, esc, delay=delay)
        if not c.me.acc("warden_bind").take(BIND_LAND * c.me.skill.spirit_accuracy, 1):
            return
        t = delay + esc
        c.spirit_hit(c.val("Damage"), delay=t, hit_chance=1.0)
        c.debuff("immobilize", 1, c.dur("ImmobilizeDuration"), delay=t)
        if c.raw("BulletArmorReduction"):
            c.after(t, lambda: c.debuff("bullet_amp_taken", c.raw("BulletArmorReduction") / 100,
                                        c.raw("BulletArmorReductionDuration")))


@register("ability_warden_riot_protocol")
class LastStand(_Base):
    kind = "aoe"
    range_props = ("Radius",)

    def cond(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.15

    def cast(self, c):
        charge = c.raw("AbilityCastDelay", 2.0)
        dur = c.dur("AbilityDuration")
        iv = c.raw("PulseInterval", 0.5)
        c.lock_gun(charge + dur)
        c.buff("bullet_resist", c.raw("BulletResist") / 100, charge + dur, tag="laststand_br")
        c.buff("spirit_resist", c.raw("TechResist") / 100, charge + dur, tag="laststand_sr")
        per = c.val("PulseDPS") * iv
        steal = c.raw("HealthStealPctHero") / 100
        unstoppable = c.tier >= 3
        n = max(1, int(round(dur / iv)))
        st = {"broken": False}

        def pulse(i):
            if st["broken"] or not c.me.alive or not c.foe.alive:
                return
            if not unstoppable and c.me.mods.active("stun"):
                st["broken"] = True
                c.me.gun_locked_until = c.now
                c.me.mods.remove("bullet_resist", "laststand_br")
                c.me.mods.remove("spirit_resist", "laststand_sr")
                return
            amt = c.engine.damage(c.me, c.foe, per, "spirit", self.s.ab.name, is_ability=True, ability=self.s,
                                  is_ult=True)
            c.heal(amt * steal)
            if i + 1 < n:
                c.after(iv, pulse, i + 1)
        c.after(charge + iv, pulse, 0)
