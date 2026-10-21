"""Holliday (hero_astro).

Assumptions:
- Powder Keg: thrown at the target and detonated by Holliday shooting it, which costs one gun shot
  (gun locked for cast delay + one shot cycle) and lands KEG_DETONATE_DELAY after the cast. Each barrel's burn
  is its own DoT, so overlapping barrels stack. Knock-up is movement only.
- Bounce Pad: Holliday bounces onto the target (reach BOUNCE_REACH) and lands BOUNCE_AIR_TIME later dealing
  StompDamage (+ T3 stun); she can shoot while airborne. Landing on the target is aimed, so the stomp lands
  at the skillshot rate.
- Crackshot: passive with its own cooldown; the first gun headshot while ready deals Damage as spirit damage.
  T2 adds bullet-resist shred, T3 cuts the remaining cooldown by 6 s per hero headshot.
- Spirit Lasso: Damage once on the grab and a stun for AbilityDuration; Holliday keeps shooting while dragging
  (needed for the lasso + barrel combo).
"""
from deadsim.abilities import AbilityImpl, register

KEG_DETONATE_DELAY = 0.6   # throw + arm + Holliday shooting the barrel
KEG_THROW_RANGE = 20.0     # m a barrel can be thrown (not in data)
BOUNCE_REACH = 20.0        # m Holliday can cover with a bounce pad to land on the target
BOUNCE_AIR_TIME = 1.5      # s airborne before the landing stomp


@register("ability_explosive_barrel")
class PowderKeg(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(KEG_THROW_RANGE + c.me.skill.engage_margin)

    def cast(self, c):
        cd = c.raw("AbilityCastDelay")
        c.lock_gun(cd + c.me.st.cycle_time / max(0.05, 1.0 + c.me.fire_rate()))
        delay = cd + KEG_DETONATE_DELAY
        c.spirit_hit(c.val("ImpactDamage"), delay=delay)
        hit = c.me.skill.spirit_accuracy
        c.dot(c.val("DPS"), c.raw("BurnDuration", 3.0), delay=delay, tick=c.raw("TickRate", 0.5),
              hit_chance=hit, tag=f"keg{self.s.casts}")


@register("ability_bounce_pad")
class BouncePad(AbilityImpl):
    kind = "skillshot"     # landing the stomp on the target is aimed like a skillshot

    def in_range(self, c):
        return c.reach(BOUNCE_REACH)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay") + BOUNCE_AIR_TIME
        if not c.me.acc("bounce_pad").take(c.me.skill.spirit_accuracy):
            return
        c.spirit_hit(c.val("StompDamage"), delay=delay, hit_chance=1.0)
        if c.tier >= 3:
            c.debuff("stun", 1, c.dur("StompStunDuration"), delay=delay)


@register("ability_crackshot")
class Crackshot(AbilityImpl):
    kind = "passive"

    def start(self, c):
        c.state["ready"] = 0.0

    def on_damage_dealt(self, c, target, hit):
        if hit.source != "gun" or not hit.headshots or not target.alive:
            return
        st = c.state
        if c.now < st["ready"]:
            if c.tier >= 3:
                st["ready"] += c.raw("AbilityCooldownPerHeadshot") * hit.headshots
            return
        st["ready"] = c.now + self.s.cooldown()
        c.spirit_hit(c.val("Damage"), hit_chance=1.0)
        if c.tier >= 2:
            c.debuff("bullet_shred", abs(c.raw("BulletResistReduction")) / 100, c.dur("BulletResistReductionDuration"))


@register("ability_gravity_lasso")
class SpiritLasso(AbilityImpl):
    kind = "skillshot"

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.15

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        hit = c.me.acc("lasso").take(c.me.skill.spirit_accuracy)
        if not hit:
            return
        c.spirit_hit(c.val("Damage"), delay=delay, hit_chance=1.0)
        c.debuff("stun", 1, c.dur("AbilityDuration"), delay=delay)
