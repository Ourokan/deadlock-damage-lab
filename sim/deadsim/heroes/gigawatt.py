"""Seven (hero_gigawatt).

Assumptions:
- Lightning Ball: the ball slows down on the target, who stays inside it for BALL_CONTACT_FRAC of its lifetime.
  Ticks every TickRate; landing rate = spirit_accuracy.
- Static Charge: the charge sits on the target, so the delayed explosion always hits it.
- Power Surge: in a 1v1 only the target is shocked once per trigger pull (burst) that hits; chain bonuses
  (BonusPerChain) need extra targets and are ignored. At most one proc per ChainTickRate. T3 shreds spirit resist on each proc.
- Storm Cloud: Seven can't shoot while channeling; target is damaged every DamageInterval while inside the
  expanding radius (line of sight assumed). A stun on Seven ends the channel. One lightning strike
  (LightningStrikes) lands on the target at the start. Cast only when the target is above 20% and the cloud's
  DPS beats Seven's expected gun DPS (incl. Power Surge), since he can't shoot while channeling.
"""
from deadsim.abilities import AbilityImpl, register

BALL_CONTACT_FRAC = 0.5
def gun_dps(c):
    """Sustained expected gun DPS (no reload), incl. an active Power Surge proc per trigger pull."""
    f = c.me
    st = f.st
    per, crit = c.engine.bullet_damage(f)
    pulls = (1.0 + f.fire_rate()) / st.cycle_time
    acc = f.skill.accuracy
    dps = per * st.pellets * st.burst_count * pulls * acc * (1 + f.skill.headshot * (crit - 1))
    for ab in f.abilities:
        if ab.ab.class_name == "ability_power_surge" and c.now < ab.scratch.get("until", -1):
            dps += ab.ctx.val("DamagePerChain") * pulls * min(1.0, acc * st.burst_count)
    return dps


@register("citadel_ability_lightning_ball")
class LightningBall(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        contact = c.dur("MaxLifetime") * BALL_CONTACT_FRAC
        c.dot(c.val("DPS"), contact, tick=max(0.1, c.raw("TickRate", 0.1)), delay=delay,
              hit_chance=c.me.skill.spirit_accuracy, tag=("ball", c.now))


@register("citadel_ability_static_charge")
class StaticCharge(AbilityImpl):
    kind = "target"
    range_props = ("AbilityCastRange",)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        boom = delay + c.raw("ShockDelay", 3.5)
        c.spirit_hit(c.val("Damage"), delay=boom)
        c.debuff("stun", 1, c.dur("StunDuration"), delay=boom)


@register("ability_power_surge")
class PowerSurge(AbilityImpl):
    kind = "self"
    range_props = ()

    def in_range(self, c):
        return c.dist <= 30

    def cast(self, c):
        c.lock_gun(c.raw("AbilityCastDelay"))
        c.state["until"] = c.now + c.dur("AbilityDuration")

    def on_damage_dealt(self, c, target, hit):
        st = c.state
        if hit.kind != "bullet" or hit.source != "gun" or not hit.hits or c.now > st.get("until", -1):
            return
        if c.now < st.get("next", 0.0):     # at most one shock per ChainTickRate
            return
        st["next"] = c.now + c.raw("ChainTickRate", 0.2) - 1e-6
        c.spirit_hit(c.val("DamagePerChain"), hit_chance=1.0)
        if c.tier >= 3:
            c.debuff("spirit_shred", abs(c.raw("TechResistDebuff")) / 100, c.dur("DebuffDuration"))


@register("citadel_ability_storm_cloud")
class StormCloud(AbilityImpl):
    kind = "aoe"
    range_props = ("Radius",)

    def should_cast(self, c):
        """Only worth giving up the gun when the cloud out-damages it (both before resists)."""
        return self.in_range(c) and c.foe.hp_frac > 0.2 and c.val("DPS") >= gun_dps(c)

    def cast(self, c):
        chan = c.dur("AbilityChannelTime")
        c.lock_gun(chan)
        st = c.state
        st["end"] = c.now + chan
        st["start"] = c.now
        if c.tier >= 1:
            st["res_tag"] = ("storm_res", c.now)
            c.buff("bullet_resist", c.raw("BulletResistOnActive") / 100, chan, tag=st["res_tag"])
        if c.raw("LightningStrikes"):
            c.spirit_hit(c.val("LightningStrikeDamage"), delay=c.raw("LightningStrikeDelay"), name="Storm Cloud")
        c.after(c.raw("DamageInterval", 0.3), self.tick, c)

    def tick(self, c):
        st = c.state
        me, foe = c.me, c.foe
        if not me.alive or not foe.alive or c.now > st["end"] + 1e-9:
            return
        if me.mods.active("stun"):          # channel broken
            me.gun_locked_until = c.now
            if "res_tag" in st:
                me.mods.remove("bullet_resist", st["res_tag"])
            return
        dt = c.raw("DamageInterval", 0.3)
        r0, r1 = c.rng("InitialRadius"), c.rng("Radius")
        grow = min(1.0, (c.now - st["start"]) / max(0.1, c.raw("ExpandTime", 3.5)))
        if c.dist <= r0 + (r1 - r0) * grow:
            c.engine.damage(me, foe, c.val("DPS") * dt, "spirit", self.s.ab.name, is_ability=True,
                            ability=self.s, is_dot=True, is_ult=True)
        c.after(dt, self.tick, c)
