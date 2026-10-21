"""Vindicta (hero_hornet).

Assumptions:
- Stake: Damage on capture; the tether itself is movement-only.
- Flight: while flying every gun bullet that hits adds MagicDamagePerBullet spirit damage. T1's +50% ammo is
  given as bonus ammo on cast (removed when Flight ends). Accuracy while flying is unchanged.
- Crow Familiar: landing rate = spirit_accuracy. Bleed deals DotHealthPercent of the target's *current* health
  per TickRate as spirit damage for DebuffDuration. Resist reductions applied as bullet/spirit shred.
- Assassinate: spirit damage (as in game); scoping for TimeToFullCharge locks the gun and the shot is always
  full charge. HeadshotBonus (+20%) is applied at the caster's headshot rate. Used as an execute: only when the
  target is under LowHealthEnemyThresholdPct or the shot would kill.
"""
from deadsim.abilities import AbilityImpl, register

@register("citadel_ability_hornet_chain")
class Stake(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(25 + c.me.skill.engage_margin)   # thrown projectile, ~25 m practical range

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        c.spirit_hit(c.val("Damage"), delay=delay)


@register("citadel_ability_hornet_leap")
class Flight(AbilityImpl):
    kind = "self"

    def in_range(self, c):
        return True

    def cast(self, c):
        d = c.dur("AbilityDuration")
        c.lock_gun(c.raw("AbilityChannelTime"))
        c.state["until"] = c.now + d
        if c.tier >= 1:
            extra = int(c.me.st.clip * c.raw("BonusClipSizePercent") / 100)
            c.me.bonus_ammo += extra
            c.after(d, self.end_ammo, c)

    def end_ammo(self, c):
        c.me.bonus_ammo = 0

    def on_damage_dealt(self, c, target, hit):
        if hit.kind == "bullet" and hit.source == "gun" and hit.hits and c.now <= c.state.get("until", -1):
            c.spirit_hit(c.val("MagicDamagePerBullet") * hit.hits, hit_chance=1.0)


@register("citadel_ability_hornet_sting")
class CrowFamiliar(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(30 + c.me.skill.engage_margin)

    def cast(self, c):
        c.lock_gun(c.raw("AbilityPostCastDuration"))
        acc = c.me.skill.spirit_accuracy
        if not c.me.acc("crow_land").take(acc):
            return
        d = c.dur("DebuffDuration")
        c.spirit_hit(c.val("ImpactDamage"), hit_chance=1.0)
        c.debuff("bullet_shred", abs(c.raw("BulletResistReduction")) / 100, d)
        c.debuff("spirit_shred", abs(c.raw("TechArmorDamageReduction")) / 100, d)
        if c.tier >= 1:
            c.debuff("heal_received", c.raw("HealAmpReceivePenaltyPercent") / 100, d)
        token = object()
        c.state["bleed"] = token
        tick = c.raw("TickRate", 1.0)
        n = max(1, int(round(d / tick)))
        c.after(tick, self.bleed, c, token, n)

    def bleed(self, c, token, n):
        if c.state.get("bleed") is not token or not c.foe.alive or not c.me.alive or n <= 0:
            return
        amt = c.foe.hp * c.raw("DotHealthPercent") / 100
        c.engine.damage(c.me, c.foe, amt, "spirit", self.s.ab.name, is_ability=True, ability=self.s, is_dot=True)
        c.after(c.raw("TickRate", 1.0), self.bleed, c, token, n - 1)


@register("citadel_ability_hornet_snipe")
class Assassinate(AbilityImpl):
    kind = "skillshot"

    def damage(self, c, low):
        dmg = c.val("Damage") + (c.val("LowHealthEnemyDamageBonus") if low else 0.0)
        return dmg * (1 + c.me.skill.headshot * c.raw("HeadshotBonus") / 100)

    def should_cast(self, c):
        thr = c.raw("LowHealthEnemyThresholdPct", 50) / 100
        if c.foe.hp_frac < thr:
            return True
        res = 1 - sum(c.foe.st.spirit_resist) if c.foe.st.spirit_resist else 1.0
        return self.damage(c, False) * c.me.skill.spirit_accuracy * res >= c.foe.hp

    def cast(self, c):
        charge = c.raw("TimeToFullCharge", 1.0)
        c.lock_gun(charge)
        c.after(charge, self.shoot, c)

    def shoot(self, c):
        if not c.me.alive or not c.foe.alive:
            return
        low = c.foe.hp_frac < c.raw("LowHealthEnemyThresholdPct", 50) / 100
        c.spirit_hit(self.damage(c, low))
