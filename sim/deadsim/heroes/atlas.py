"""Abrams (hero_atlas).

Assumptions:
- Siphon Life: the target stays inside Radius (plus engage margin) for the whole duration; Abrams keeps shooting
  and heals HealingFactor% of the damage dealt.
- Shoulder Charge: hits when the target is within CHARGE_REACH; stun (StunDuration, T2 longer) only when the
  target is pinned against a wall, WALL_HIT_RATE of casts (deterministic accumulator). T3 '+1.5 Weapon Damage'
  is read as +1.5 flat damage per pellet, converted to weapon % for 6 s. T1 slow ignored.
  Combo: with Skill.combo_melee (default on) every landed charge is followed by a heavy melee when the target is
  released (the standard charge into heavy melee), weighted by the charge's landing factor; the fitted melee rotation rate already accounts for it.
- Infernal Resilience: damage taken is pooled each RegenDamageInterval and regenerated over
  RegenIncomingDamageDuration. BonusHealthRegen is a permanent +regen. T1 +200 max health, T3 +20% status resist.
  T2 melee lifesteal ignored (no melee in the default rotation).
- Seismic Impact: leap takes LEAP_TIME (no shooting), then Damage + stun. T3 'unstoppable' approximated as
  100% status resist for ImmunityDuration. Cast only on a target with more than 20% health within LEAP_REACH.
"""
from deadsim.abilities import AbilityImpl, register

CHARGE_REACH = 20.0
WALL_HIT_RATE = 0.5
LEAP_TIME = 1.0
LEAP_REACH = 30.0


@register("citadel_ability_bull_heal")
class SiphonLife(AbilityImpl):
    kind = "aoe"
    range_props = ("Radius",)

    def cast(self, c):
        tick = c.raw("TickRate", 0.25)
        n = max(1, int(round(c.dur("AbilityDuration") / tick)))
        c.after(tick, self.tick, c, n)

    def tick(self, c, n):
        me, foe = c.me, c.foe
        if n <= 0 or not me.alive or not foe.alive:
            return
        tick = c.raw("TickRate", 0.25)
        dealt = c.engine.damage(me, foe, c.val("DPS") * tick, "spirit", self.s.ab.name, is_ability=True,
                                ability=self.s, is_dot=True)
        if dealt:
            c.heal(dealt * c.raw("HealingFactor") / 100)
        c.after(tick, self.tick, c, n - 1)


@register("citadel_ability_bull_charge")
class ShoulderCharge(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(CHARGE_REACH)

    def cast(self, c):
        d = c.dur("AbilityDuration")
        hit_t = min(d, c.dist / c.raw("ChargeSpeedMax", 30.0) + 0.2)
        c.lock_gun(hit_t + c.raw("CollidePlayersStopTime"))
        if not c.me.acc("abrams_charge").take(c.me.skill.spirit_accuracy):
            return
        c.spirit_hit(c.val("Damage"), delay=hit_t, hit_chance=1.0)
        if c.me.acc("abrams_wall").take(WALL_HIT_RATE):
            c.debuff("stun", 1, c.dur("StunDuration"), delay=hit_t)
        if c.me.skill.combo_melee:
            c.after(hit_t + c.raw("CollidePlayersStopTime"), self.combo, c)
        if c.tier >= 3 and c.me.st.bullet_damage:
            pct = c.raw("WeaponDamageBonus") / c.me.st.bullet_damage
            c.after(hit_t, c.buff, "weapon_pct", pct, c.raw("WeaponPowerIncreaseDuration"))


    def combo(self, c):
        if c.me.alive and c.foe.alive and not c.engine.over and not c.me.mods.active("stun"):
            # lands as often as real charges connect (the charge's fitted landing factor, also when the skill
            # has landing factors off, so the melee rate fit and default fights agree)
            w = c.me.skill.ability_landing.get(self.s.ab.name)
            if w is None:
                from deadsim.accuracy import ability_landing
                w = ability_landing("Abrams").get(self.s.ab.name, 1.0)
            w = min(1.0, w)
            c.engine.melee_hit(c.me, heavy=True, w=w)


@register("citadel_ability_passive_beefy")
class InfernalResilience(AbilityImpl):
    kind = "passive"

    def start(self, c):
        me = c.me
        forever = 1e9
        if c.raw("BonusHealthRegen"):
            c.buff("regen", c.raw("BonusHealthRegen"), forever, tag="beefy_regen")
        if c.tier >= 1:
            c.buff("max_health", c.raw("BonusMaxHealth"), forever, tag="beefy_hp")
            me.hp += c.raw("BonusMaxHealth")
        if c.tier >= 3:
            c.buff("status_resist", c.raw("StatusResistancePercent") / 100, forever, tag="beefy_sr")
        c.state["pool"] = 0.0
        c.after(c.raw("RegenDamageInterval", 1.0), self.flush, c)

    def on_damage_taken(self, c, src, hit):
        c.state["pool"] = c.state.get("pool", 0.0) + hit.amount * c.raw("RegenIncomingDamagePercent") / 100

    def flush(self, c):
        if not c.me.alive or c.engine.over:
            return
        pool = c.state.get("pool", 0.0)
        if pool > 0:
            d = c.raw("RegenIncomingDamageDuration", 20.0)
            c.buff("regen", pool / d, d, tag=("beefy", c.now))
            c.state["pool"] = 0.0
        c.after(c.raw("RegenDamageInterval", 1.0), self.flush, c)


@register("citadel_ability_bull_leap")
class SeismicImpact(AbilityImpl):
    kind = "aoe"

    def should_cast(self, c):
        return c.reach(LEAP_REACH) and c.foe.hp_frac > 0.2

    def cast(self, c):
        c.lock_gun(LEAP_TIME)
        if c.tier >= 3:
            c.buff("status_resist", 1.0, c.dur("ImmunityDuration"), tag="seismic_unstoppable")
        c.spirit_hit(c.val("Damage"), delay=LEAP_TIME)
        c.debuff("stun", 1, c.dur("StunDuration"), delay=LEAP_TIME)
