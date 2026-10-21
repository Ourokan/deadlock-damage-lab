"""Lash (hero_lash).

Assumptions:
- Ground Strike: always cast from the air after a jump/dash, falling FALL_HEIGHT m: StompDamage +
  StompDamagePerMeterPrimary x height (all of it within the 25 m primary range). T3 (+120% damage per meter, +0.04
  scaling) comes from the data via c.val. Reach = Radius + engage margin
  (+ DIVE_REACH since he dives in from the air). T2 knock-up/slow are movement-only and skipped.
- Grapple: movement only, so it is cast (as an engage) only when T2 is bought, for +WeaponDamageBonus% weapon
  damage over WeaponDamageBonusDuration. Lash keeps shooting while pulled.
- Flog: lock-on whip in a cone up to AbilityCastRange: damage, heals HealPctVsHeroes% of damage dealt; T2 fire-rate
  slow for EnemySlowDuration (FLOG_SLOW_DUR if T1 is not bought). T1 move slow skipped.
- Death Slam: single target, so Lash throws as soon as the lock forms (cast delay + TimeToGainLockonStack); the
  target is lifted and stunned for BoostTime + HangTime + SLAM_TIME, then takes ImpactDamage; T3 adds a
  StunDuration stun on landing. Lash can't shoot from cast until the slam.
"""
from deadsim.abilities import AbilityImpl, register

FALL_HEIGHT = 10.0   # m dropped before a typical Ground Strike (jump + air dash)
DIVE_REACH = 4.0     # extra horizontal reach from diving in from the air
FLOG_SLOW_DUR = 3.0  # fire-rate slow duration when T1 (EnemySlowDuration) isn't bought
SLAM_TIME = 0.3      # throw-to-impact time (SlamSpeed 1600 from ~6 m up)


def busy(c):
    return c.now < c.me.gun_locked_until


@register("citadel_ability_lash_down_strike")
class GroundStrike(AbilityImpl):
    kind = "aoe"

    def in_range(self, c):
        return c.within(c.rng("Radius") + DIVE_REACH)

    def should_cast(self, c):
        return not busy(c) and self.in_range(c)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay") + FALL_HEIGHT / c.raw("StrikeVelocity", 50.0)
        c.lock_gun(delay + c.raw("AbilityPostCastDuration"))
        per_m = c.val("StompDamagePerMeterPrimary")
        h = min(FALL_HEIGHT, c.raw("StompDamagePrimaryRange", 25.0))
        c.spirit_hit(c.val("StompDamage") + per_m * h, delay=delay)


@register("citadel_ability_lash")
class Grapple(AbilityImpl):
    kind = "target"

    def should_cast(self, c):
        return c.raw("WeaponDamageBonus") > 0 and not busy(c) and self.in_range(c)

    def cast(self, c):
        c.buff("weapon_pct", c.raw("WeaponDamageBonus") / 100, c.dur("WeaponDamageBonusDuration"),
               tag="grapple_wd")


@register("ability_lash_flog")
class Flog(AbilityImpl):
    kind = "target"

    def should_cast(self, c):
        return not busy(c) and self.in_range(c)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        dmg = c.val("Damage")
        heal = c.raw("HealPctVsHeroes") / 100

        def go():
            if not c.me.alive or not c.foe.alive:
                return
            amt = c.engine.damage(c.me, c.foe, dmg, "spirit", self.s.ab.name, is_ability=True, ability=self.s)
            c.heal(amt * heal)
            if c.raw("FireRateSlow"):
                c.debuff("fire_rate_slow", c.raw("FireRateSlow") / 100,
                         c.dur("EnemySlowDuration") or FLOG_SLOW_DUR * (1 + c.s.duration_pct()))
        c.after(delay, go)


@register("citadel_ability_lash_ultimate")
class DeathSlam(AbilityImpl):
    kind = "target"

    def should_cast(self, c):
        return not busy(c) and self.in_range(c) and c.foe.hp_frac > 0.1

    def cast(self, c):
        lock = c.raw("AbilityCastDelay") + c.raw("TimeToGainLockonStack", 0.7)
        air = c.raw("BoostTime", 1.0) + c.raw("HangTime", 0.6) + SLAM_TIME
        c.lock_gun(lock + air)
        c.debuff("stun", 1, air, delay=lock)
        c.spirit_hit(c.val("ImpactDamage"), delay=lock + air)
        if c.raw("StunDuration"):
            c.debuff("stun", 1, c.dur("StunDuration"), delay=lock + air, tag="deathslam_t3")
