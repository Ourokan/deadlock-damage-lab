"""Bebop (hero_bebop).

Assumptions:
- Grapple Arm: lands with spirit accuracy after AbilityCastDelay + HookImpactDelay and pulls the target into
  melee range for HOOK_CLOSE_WINDOW s (the engine distance is fixed, so the pull only unlocks Bebop's close-range
  abilities). Bebop can't shoot during cast + post-cast. T1: +20% bullet damage taken by the victim.
- Exploding Uppercut: a light-melee-strength hit (UppercutDamage + light melee damage) when the target is within
  MeleeAttackLength (+ engage margin) or was just hooked. The landing explosion only damages *other* enemies,
  so it deals nothing in a 1v1. T2: +BuffBaseWeaponPct weapon damage for UppercutBuffOnHit s; T3: Grapple Arm
  cooldown reset and heal MissingHPHeal % of missing health.
- Sticky Bomb: target ability (cast range + margin, or after a hook); explodes after FuseTime. The permanent
  per-hit stacks grow within the fight (BonusDamagePctPerPlayerHit per earlier hit). Self damage ignored
  (Bebop has moved away by the fuse).
- Hyper Beam: cast after the hook / uppercut / sticky combo is spent; no other ability during the beam.
  AbilityCastDelay wind-up then an AbilityChannelTime beam; Bebop can't shoot. Beam uptime on the
  target = caster's spirit accuracy; full damage (beyond BeamCloseRadius). A stun breaks the channel. T3 heals
  BeamLifesteal % of the damage dealt.
"""
from deadsim.abilities import AbilityImpl, register

HOOK_CLOSE_WINDOW = 3.0   # s the hooked target stays in melee / sticky range after the pull
HOOK_KEY = "bebop_hooked_until"
FLIGHT_KEY = "bebop_hook_flight"
BEAM_KEY = "bebop_beam_until"


def hooked(c):
    return c.now < c.me.counters.get(HOOK_KEY, -1.0)


def beaming(c):
    return c.now < c.me.counters.get(BEAM_KEY, -1.0)


def combo_ready(c):
    """Another close-range ability can still be cast (the beam waits for the hook combo)."""
    if c.now < c.me.counters.get(FLIGHT_KEY, -1.0):
        return True
    for ab in c.me.abilities:
        if ab.unlocked and ab.ab.class_name in ("citadel_ability_uppercut", "citadel_ability_sticky_bomb"):
            ab._recharge()
            if ab.charges > 0 and c.now >= ab.ready_at and ab.impl.in_range(ab.ctx):
                return True
    return False


@register("citadel_ability_uppercut")
class ExplodingUppercut(AbilityImpl):
    kind = "target"

    def in_range(self, c):
        return hooked(c) or c.within(c.rng("MeleeAttackLength", 6.0))

    def should_cast(self, c):
        return self.in_range(c) and not beaming(c)

    def cast(self, c):
        c.melee_hit(c.val("UppercutDamage"))
        if c.tier >= 2:
            c.buff("weapon_pct", c.raw("BuffBaseWeaponPct") / 100, c.raw("UppercutBuffOnHit"))
        if c.tier >= 3:
            c.heal(c.raw("MissingHPHeal") / 100 * (c.me.max_hp - c.me.hp))
            for ab in c.me.abilities:
                if ab.ab.class_name == "citadel_ability_hook":
                    ab.reset_cooldown()


@register("citadel_ability_sticky_bomb")
class StickyBomb(AbilityImpl):
    kind = "target"

    def in_range(self, c):
        return hooked(c) or super().in_range(c)

    def should_cast(self, c):
        return self.in_range(c) and not beaming(c)

    def start(self, c):
        c.state["hits"] = 0

    def cast(self, c):
        fuse = c.raw("FuseTime", 3.5)
        bonus = c.state["hits"] * c.val("BonusDamagePctPerPlayerHit") / 100
        c.spirit_hit(c.val("Damage") * (1.0 + bonus), delay=fuse)
        c.state["hits"] += 1


@register("citadel_ability_hook")
class GrappleArm(AbilityImpl):
    kind = "skillshot"

    def should_cast(self, c):
        return self.in_range(c) and not beaming(c)

    def cast(self, c):
        cd = c.raw("AbilityCastDelay")
        c.lock_gun(cd + c.raw("AbilityPostCastDuration"))
        if not c.me.acc("grapple").take(c.me.skill.spirit_accuracy):
            return
        land = cd + c.raw("HookImpactDelay")
        c.me.counters[FLIGHT_KEY] = c.now + land
        c.after(land, self.pulled, c)
        if c.tier >= 1:
            c.debuff("bullet_amp_taken", c.raw("BulletAmp") / 100, c.raw("BulletAmpDuration"), delay=land)

    def pulled(self, c):
        c.me.counters[HOOK_KEY] = c.now + HOOK_CLOSE_WINDOW


@register("citadel_ability_bebop_laser_beam")
class HyperBeam(AbilityImpl):
    kind = "skillshot"
    range_props = ("BeamLength",)

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.2 and not combo_ready(c)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        T = c.dur("AbilityChannelTime")
        c.lock_gun(delay + T)
        c.me.counters[BEAM_KEY] = c.now + delay + T
        c.state["end"] = c.now + delay + T
        c.after(delay, self.tick, c)

    def tick(self, c):
        iv = c.raw("Interval", 0.1) * 2     # 0.2 s ticks (the game ticks at 0.1 s)
        if not c.me.alive or not c.foe.alive or c.now > c.state["end"] + 1e-9:
            return
        if c.me.mods.active("stun"):
            c.me.gun_locked_until = c.now
            c.me.counters[BEAM_KEY] = c.now
            return
        dmg = c.engine.damage(c.me, c.foe, c.val("DPS") * iv * c.me.skill.spirit_accuracy, "spirit",
                              self.s.ab.name, is_ability=True, ability=self.s, is_dot=True, is_ult=True)
        if c.tier >= 3 and dmg:
            c.heal(dmg * c.raw("BeamLifesteal") / 100)
        c.after(iv, self.tick, c)
