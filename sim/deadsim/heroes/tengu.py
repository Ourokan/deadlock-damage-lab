"""Ivy (hero_tengu).

Assumptions:
- "Increased spirit scaling" upgrades (Thorns T2, Stone Form T3, Air Drop T1/T3) come from the data via c.val.
- Entangling Thorns: thrown up to THROW_RANGE; the target stands in it for THORN_UPTIME of the duration (it
  slows, but they walk out). T3 immobilize is movement-only and skipped.
- Kudzu Connection: no ally in a 1v1, so Ivy gets 50% of the bonuses (NO_TETHER_FACTOR): fire rate and bullet
  lifesteal for AbilityDuration (lifesteal's healing spirit scale applied by c.val).
  T3 (always active) = permanent buff from fight start.
- Stone Form: invulnerable and unable to shoot for cast delay + LiftTime, then slams for damage + stun in
  Radius and heals MaxHealthRegen% of max health. She can drift MoveSpeedMax m/s while lifted, so reach is
  Radius + MoveSpeedMax*LiftTime (+ engage margin). Also used defensively below DEFENSIVE_HP even out of reach.
- Air Drop: self-cast (no ally): Ivy flies FLY_TIME s (can't shoot), drops the bomb on the target (ExplodeDamage,
  T2 slow skipped, T3 silence), then gets +AirDropOutgoingDamagePercent outgoing damage (damage_amp) for BuffDuration. T1 barrier:
  AirDropBulletShield (300 + spirit scaling) for BARRIER_TIME.
"""
from deadsim.abilities import AbilityImpl, register

THROW_RANGE = 25.0
THORN_UPTIME = 0.75
NO_TETHER_FACTOR = 0.5
DEFENSIVE_HP = 0.4
FLY_TIME = 2.0
BARRIER_TIME = 8.0      # not in data; assume it lasts as long as the outgoing damage buff


@register("citadel_ability_tengu_urn")
class EntanglingThorns(AbilityImpl):
    kind = "aoe"

    def in_range(self, c):
        return c.reach(THROW_RANGE)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        dps = c.val("DPS")
        c.dot(dps, c.dur("AbilityDuration") * THORN_UPTIME, delay=delay, tick=c.raw("TickRate", 0.25),
              tag=("thorns", self.s.casts))


@register("citadel_ability_tangotether")
class KudzuConnection(AbilityImpl):
    kind = "self"

    def _apply(self, c, dur):
        c.buff("fire_rate", c.val("BonusFireRate") / 100 * NO_TETHER_FACTOR, dur, tag="kudzu_fr")
        c.buff("bullet_lifesteal", c.val("BulletLifestealPercent") / 100 * NO_TETHER_FACTOR, dur, tag="kudzu_ls")

    def start(self, c):
        if c.tier >= 3:
            self._apply(c, 1e6)

    def should_cast(self, c):
        return c.tier < 3

    def cast(self, c):
        self._apply(c, c.dur("AbilityDuration"))


@register("citadel_ability_tengu_stone_form")
class StoneForm(AbilityImpl):
    kind = "aoe"

    def in_range(self, c):
        reach = c.rng("Radius") + c.raw("MoveSpeedMax") * c.raw("LiftTime", 1.0)
        return c.within(reach)

    def should_cast(self, c):
        if c.now < c.me.gun_locked_until:     # mid Air Drop / other cast
            return False
        return self.in_range(c) or c.me.hp_frac < DEFENSIVE_HP

    def cast(self, c):
        t = c.raw("AbilityCastDelay") + c.raw("LiftTime", 1.0)
        c.lock_gun(t)
        c.buff("invulnerable", 1, t, tag="stone_form")
        if self.in_range(c):
            c.spirit_hit(c.val("Damage"), delay=t)
            c.debuff("stun", 1, c.dur("StunDuration"), delay=t)
        c.after(t, lambda: c.heal(c.me.max_hp * c.raw("MaxHealthRegen") / 100))


@register("citadel_ability_tengu_airlift")
class AirDrop(AbilityImpl):
    kind = "aoe"
    range_props = ("OnLandDamageRadius",)

    def should_cast(self, c):
        return c.now >= c.me.gun_locked_until and self.in_range(c)   # not while in Stone Form

    def cast(self, c):
        t = c.raw("AbilityCastDelay") + FLY_TIME
        c.lock_gun(t)
        c.spirit_hit(c.val("ExplodeDamage"), delay=t)
        if c.tier >= 3:
            c.debuff("silence", 1, c.dur("SilenceDuration"), delay=t)

        def land():
            if not c.me.alive:
                return
            c.buff("damage_amp", c.raw("AirDropOutgoingDamagePercent") / 100, c.dur("BuffDuration"),
                   tag="airdrop_amp")
            if c.tier >= 1:
                c.barrier(c.val("AirDropBulletShield"), BARRIER_TIME)
        c.after(t, land)
