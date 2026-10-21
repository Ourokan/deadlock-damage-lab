"""Paige (hero_bookworm).

Assumptions:
- Bookwyrm: the dragon hits once (Damage after StartupDelay), then the target stands in the burning trail for
  TRAIL_UPTIME of GroundFlameDuration plus the DebuffDuration linger. Reach is DragonTravelRange.
- Plot Armor: Paige casts it on herself (the only ally in a 1v1). Weapon bonus (BaseAttackDamagePercent) and the
  T1 fire rate (14% + 0.16 x spirit) last while the barrier holds. BonusSpiritDamagePercent is not in the
  description and is ignored. The shove is skipped.
- Captivating Read: skillshot (target can walk out during DetonationDelay); immobilize applied as a state with
  no movement effect. T3 spirit resist reduction modeled as spirit shred.
- Rallying Charge: the target is hit by one knight (not both waves). Amp grows with travelled distance; we
  assume the knights travel the fight distance, so amp = MaxAmp * dist / MaxAmpDistance. Allied heal ignored.
"""
from deadsim.abilities import AbilityImpl, register

TRAIL_UPTIME = 0.5


@register("ability_bookworm_dragonfire")
class Bookwyrm(AbilityImpl):
    kind = "skillshot"
    range_props = ("DragonTravelRange",)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay") + c.raw("StartupDelay")
        c.lock_gun(c.raw("AbilityCastDelay"))
        c.spirit_hit(c.val("Damage"), delay=delay)
        burn = c.dur("GroundFlameDuration") * TRAIL_UPTIME + c.dur("DebuffDuration")
        c.dot(c.val("DPS"), burn, delay=delay, tick=c.raw("TickRate", 0.3), hit_chance=c.me.skill.spirit_accuracy)


@register("ability_bookworm_knightbarrier")
class PlotArmor(AbilityImpl):
    kind = "self"

    def should_cast(self, c):
        return c.reach(40)     # in combat

    def cast(self, c):
        d = c.dur("AbilityDuration")
        c.barrier(c.val("CombatBarrier"), d)
        b = c.me.barriers[-1]
        wpn = c.val("BaseAttackDamagePercent") / 100
        fr = c.val("BonusFireRate") / 100
        end = c.now + d

        def hook(f):
            if f.e.t < end and b[0] > 0:
                return {"weapon_pct": wpn, "fire_rate": fr}
            return {}
        if "plot_hook" in c.state:
            c.me.stat_hooks.remove(c.state["plot_hook"])
        c.state["plot_hook"] = hook
        c.me.stat_hooks.append(hook)


@register("ability_bookworm_aoemagic")
class CaptivatingRead(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        cd = c.raw("AbilityCastDelay")
        c.lock_gun(cd)
        delay = cd + c.raw("DetonationDelay", 1.25)
        acc = c.me.skill.spirit_accuracy
        c.spirit_hit(c.val("Damage"), delay=delay)
        c.debuff("immobilize", 1, c.dur("ImmobilizeDuration") * acc, delay=delay)
        if c.tier >= 3:
            c.debuff("spirit_shred", abs(c.raw("TechArmorDamageReduction")) / 100 * acc, c.dur("DebuffDuration"),
                     delay=delay)


@register("ability_bookworm_knightcharge")
class RallyingCharge(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        ch = c.raw("AbilityChannelTime", 0.7)
        c.lock_gun(ch)
        amp = c.raw("MaxAmp") / 100 * min(1.0, c.dist / max(1.0, c.raw("MaxAmpDistance", 250)))
        c.spirit_hit(c.val("Damage") * (1.0 + amp), delay=ch)
        c.debuff("stun", 1, c.dur("StunDuration") * c.me.skill.spirit_accuracy, delay=ch)
