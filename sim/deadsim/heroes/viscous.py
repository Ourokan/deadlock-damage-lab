"""Viscous (hero_viscous).

Assumptions:
- Splatter: skillshot thrown up to THROW_RANGE. First explosion deals Damage; each of the MaxBounces bounces deals
  Second/Third/FourthHitDamagePercentage of it and catches the target BOUNCE_HIT of the time. Puddle slow skipped.
  T3 "improved spirit scaling" (Damage +0.9) comes from the data via c.val.
- The Cube: self-cast only, as a defensive panic button below CUBE_HP: invulnerable, can't shoot/cast for
  AbilityDuration, BonusHealthRegen per second (+ healing spirit scale, via c.val). T3 purges stun/silence/
  disarm/slows at cast. T1 post-cube move speed skipped.
- Puddle Punch: skillshot (can be dodged/parried). Melee damage = c.val("Damage") (flat + 0.6 x light melee);
  T3 zeroes that (Damage -40, scale x0) and deals DamageHeavyMelee + 0.6 x heavy melee. The engine has no heavy
  melee helper: heavy melee = hero heavy_melee_damage grown by the same per-boon ratio as light melee, and the
  T3 scale (stat filter unset in the data) is applied to it by hand rather than via c.val (which would read it
  as spirit scaling). Knock-up/slow are movement-only. T2 lifesteal heals LifeStealPercentOnHit% of damage dealt.
- Goo Ball: rolls in (ROLL_IN s), hits the target BALL_HITS times REHIT s apart (Damage + stun each; T3 +0.2 spirit
  scaling via c.val), then Viscous exits the ball. Can't shoot while rolling; ball bullet/spirit resist
  applies from cast to exit.
"""
from deadsim.abilities import AbilityImpl, register

THROW_RANGE = 30.0
BOUNCE_HIT = 0.5
CUBE_HP = 0.3
ROLL_IN = 1.5
BALL_HITS = 2
REHIT = 2.5
BOUNCE_PCTS = ("SecondHitDamagePercentage", "ThirdHitDamagePercentage", "FourthHitDamagePercentage")


def busy(c):
    return c.now < c.me.gun_locked_until


@register("viscous_goo_grenade")
class Splatter(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(THROW_RANGE)

    def should_cast(self, c):
        return not busy(c) and self.in_range(c)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay") + c.dist / 25.0   # flight time
        c.lock_gun(c.raw("AbilityCastDelay") + c.raw("AbilityPostCastDuration"))
        if not c.me.acc("splatter").take(c.me.skill.spirit_accuracy, 1):
            return
        dmg = c.val("Damage")
        c.spirit_hit(dmg, delay=delay, hit_chance=1.0)
        for i in range(min(int(c.raw("MaxBounces")), len(BOUNCE_PCTS))):
            c.spirit_hit(dmg * c.raw(BOUNCE_PCTS[i]), delay=delay + 0.4 * (i + 1), hit_chance=BOUNCE_HIT)


@register("viscous_restorative_goo")
class TheCube(AbilityImpl):
    kind = "self"

    def should_cast(self, c):
        return c.me.hp_frac < CUBE_HP

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        d = c.dur("AbilityDuration")
        f = c.me
        if c.raw("PurgeDebuffs"):
            for k in ("stun", "silence", "disarm", "immobilize", "fire_rate_slow"):
                f.mods.d.pop(k, None)
        c.lock_gun(delay + d)
        c.buff("invulnerable", 1, delay + d, tag="cube")
        c.buff("silence", 1, delay + d, tag="cube_self")
        c.buff("regen", c.val("BonusHealthRegen"), delay + d, tag="cube_regen")


@register("viscous_telepunch")
class PuddlePunch(AbilityImpl):
    kind = "skillshot"

    def should_cast(self, c):
        return not busy(c) and self.in_range(c)

    def cast(self, c):
        if not c.me.acc("punch").take(c.me.skill.spirit_accuracy, 1):
            return
        if c.raw("UseHeavyMelee"):
            h = c.me.st.hero
            light0 = h.base.get("light_melee_damage") or 1.0
            heavy = h.base.get("heavy_melee_damage", 0.0) * c.light_melee() / light0
            dmg = c.raw("DamageHeavyMelee") + c.scale("DamageHeavyMelee") * heavy + max(0.0, c.val("Damage"))
        else:
            dmg = c.val("Damage")
        ls = c.raw("LifeStealPercentOnHit") / 100
        amp = c.me.melee_mult()

        def go():
            if not c.me.alive or not c.foe.alive:
                return
            amt = c.engine.damage(c.me, c.foe, dmg * amp, "melee", self.s.ab.name, is_ability=True, ability=self.s)
            if ls:
                c.heal(amt * ls)
        c.after(0.2, go)


@register("viscous_goo_bowling_ball")
class GooBall(AbilityImpl):
    kind = "target"

    def in_range(self, c):
        return True   # it is a gap closer

    def should_cast(self, c):
        return not busy(c) and c.foe.hp_frac > 0.1

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        hits = [delay + ROLL_IN + REHIT * i for i in range(BALL_HITS)]
        end = min(delay + c.dur("AbilityDuration"), hits[-1] + 0.5)
        hits = [t for t in hits if t < end]
        c.lock_gun(end)
        c.buff("bullet_resist", c.raw("BulletResist") / 100, end, tag="gooball_br")
        c.buff("spirit_resist", c.raw("TechResist") / 100, end, tag="gooball_sr")
        dmg = c.val("Damage")
        for t in hits:
            c.spirit_hit(dmg, delay=t)
            c.debuff("stun", 1, c.dur("StunDuration"), delay=t, tag=("gooball_stun", t))
