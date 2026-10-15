"""Grey Talon (hero_orion).

Assumptions:
- Charged Shot: spirit damage after the AbilityCastDelay charge (gun locked meanwhile). T3's improved scaling
  comes from the ability's scale upgrades via c.val.
- Rain of Arrows: airborne for AbilityDuration after AbilityCastDelay. Each gun shot gets +WeaponDamageBonus
  flat damage (data: FLAT_BULLET_DAMAGE_POST_SCALE, not multiplied by weapon damage) and the multishot adds
  (BulletSplitShot - 1) x MULTISHOT_SHARE extra bullets' worth of damage against a single hero. T3 lifesteal and
  evasion for the airborne time. The T1 slow is movement only.
- Spirit Snare: thrown on the target; it triggers after ArmTime + TripTime with probability SNARE_TRIGGER
  (the enemy may leave the radius before it arms). On trigger: Damage, and Curse = silence + disarm + item
  silence for TetherDuration. T2 bullet-resist shred.
- Guided Owl: Talon can't shoot during the 1.5 s cast and the flight (distance / OWL_SPEED); lands with spirit
  accuracy, Damage + stun. Not cast while Rain of Arrows is active. T3 executes a target left below LowHealthEnemyThresholdPct.
"""
from deadsim.abilities import AbilityImpl, register

MULTISHOT_SHARE = 0.4    # share of the extra split arrows that also hit a single hero target
SNARE_TRIGGER = 0.7      # chance the armed trap catches the enemy
OWL_SPEED = 30.0         # m/s average owl flight speed (not in data)


@register("ability_charged_shot")
class ChargedShot(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        c.spirit_hit(c.val("Damage"), delay=delay)


@register("ability_power_jump")
class RainOfArrows(AbilityImpl):
    kind = "self"

    def in_range(self, c):
        return True

    def start(self, c):
        c.state["from"] = c.state["until"] = -1.0

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        T = c.dur("AbilityDuration")
        c.state["from"], c.state["until"] = c.now + delay, c.now + delay + T
        if c.tier >= 3:
            c.buff("bullet_lifesteal", c.raw("BulletLifestealPercent") / 100, delay + T)
            c.buff("spirit_lifesteal", c.raw("TechLifestealPercent") / 100, delay + T)
            c.buff("evasion", c.raw("EvasionPercent") / 100, delay + T)

    def on_shot(self, c, ctx):
        if not (c.state["from"] <= c.now < c.state["until"]):
            return
        f = c.me
        base, _ = c.engine.bullet_damage(f, ctx["extra_pct"])
        flat = c.raw("WeaponDamageBonus") / max(0.1, base * ctx["dmg_mult"])
        split = 1.0 + (c.raw("BulletSplitShot", 1) - 1.0) * MULTISHOT_SHARE
        ctx["dmg_mult"] *= (1.0 + flat) * split


@register("ability_immobilize_trap")
class SpiritSnare(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return True    # thrown; no cast range in data

    def cast(self, c):
        if not c.me.acc("snare").take(SNARE_TRIGGER * c.me.skill.spirit_accuracy):
            return
        delay = c.raw("ArmTime") + c.raw("TripTime")
        d = c.dur("TetherDuration")
        c.spirit_hit(c.raw("Damage"), delay=delay, hit_chance=1.0)
        for key in ("silence", "disarm", "item_silence"):
            c.debuff(key, 1, d, delay=delay)
        if c.tier >= 2:
            c.debuff("bullet_shred", abs(c.raw("BulletArmorReduction")) / 100, c.dur("DebuffDuration"), delay=delay)


@register("ability_guided_arrow")
class GuidedOwl(AbilityImpl):
    kind = "skillshot"
    range_props = ()

    def should_cast(self, c):
        for ab in c.me.abilities:      # don't waste Rain of Arrows air time piloting the owl
            if ab.ab.class_name == "ability_power_jump" and ab.unlocked and c.now < ab.scratch.get("until", -1):
                return False
        return c.foe.hp_frac > 0.1

    def cast(self, c):
        delay = c.raw("AbilityCastDelay") + c.dist / OWL_SPEED
        c.lock_gun(delay)
        if not c.me.acc("owl").take(c.me.skill.spirit_accuracy):
            return
        c.spirit_hit(c.val("Damage"), delay=delay, hit_chance=1.0)
        c.debuff("stun", 1, c.dur("StunDuration"), delay=delay)
        if c.tier >= 3:
            c.after(delay + 0.01, self.execute, c)

    def execute(self, c):
        e = c.foe
        if e.alive and e.hp_frac < c.raw("LowHealthEnemyThresholdPct") / 100:
            c.engine.damage(c.me, e, e.hp + e.barrier_total() + 1.0, "spirit", "Guided Owl execute",
                            ignore_resist=True, is_ability=True, ability=self.s, is_ult=True)
