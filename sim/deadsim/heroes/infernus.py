"""Infernus (hero_inferno). Reference implementation for the ability API.

Assumptions:
- Flame Dash: the dash passes through the target, who then stands in the trail for TRAIL_UPTIME of its duration.
- Concussive Combustion: Infernus can't shoot during the 3.25 s fuse; cast only when the target is within the
  radius (plus engage margin) and isn't already nearly dead from the gun.
"""
from deadsim.abilities import AbilityImpl, register

TRAIL_UPTIME = 0.5


@register("ability_incendiary_projectile")
class Napalm(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        c.spirit_hit(c.val("Damage"), delay=delay)
        d = c.dur("DebuffDuration")
        hit = c.me.skill.spirit_accuracy
        c.debuff("damage_taken_amp", c.raw("IncomingDamagePercentFromCaster") / 100 * hit, d, delay=delay)
        if c.tier >= 2:   # T2: +15% lifesteal against napalmed targets
            ls = c.raw("LifestealPercentHero") / 100 * hit
            c.buff("bullet_lifesteal", ls, d, tag="napalm_ls")
            c.buff("spirit_lifesteal", ls, d, tag="napalm_ls_s")
        if c.tier >= 3:
            c.debuff("heal_received", c.raw("HealAmpReceivePenaltyPercent") / 100 * hit, d, delay=delay)


@register("ability_flame_dash")
class FlameDash(AbilityImpl):
    kind = "aoe"
    range_props = ("FlameAuraRadius",)

    def in_range(self, c):
        return c.dist <= 12.0 + c.me.skill.engage_margin   # dash distance ~12 m

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        trail = c.dur("GroundFlameDuration") * TRAIL_UPTIME
        c.dot(c.val("DPS"), trail, delay=delay, tick=c.raw("TickRate", 0.5))


@register("ability_afterburn")
class Afterburn(AbilityImpl):
    """Passive: bullet hits build up a burn (8.1% per hit, 15.4% per headshot). While burning, hits extend
    the burn by 0.5 s (1 s on headshots) up to BurnDuration. Damage ticks every 0.5 s."""
    kind = "passive"

    def start(self, c):
        c.state.update(meter=0.0, last=-99.0, burn_until=-1.0, ticking=False)

    def on_damage_dealt(self, c, target, hit):
        if hit.kind != "bullet" or not hit.hits or hit.source == self.s.ab.name:
            return
        st = c.state
        now = c.now
        body = hit.hits - hit.headshots
        if now < st["burn_until"]:
            ext = body * c.raw("RefillDuration", 0.5) + hit.headshots * c.raw("RefillDurationCrit", 1.0)
            st["burn_until"] = min(now + c.dur("BurnDuration"), st["burn_until"] + ext)
            return
        if now - st["last"] > c.raw("BuildUpDuration", 17):
            st["meter"] = 0.0
        st["last"] = now
        st["meter"] += body * c.raw("BuildUpBulletPercentPerHit") + hit.headshots * c.raw("CritBuildup")
        if st["meter"] >= 100:
            st["meter"] = 0.0
            st["burn_until"] = now + c.dur("BurnDurationBase", 3.0)
            if not st["ticking"]:
                st["ticking"] = True
                c.after(c.raw("TickRate", 0.5), self.tick, c)

    def tick(self, c):
        st = c.state
        if c.now > st["burn_until"] + 1e-9 or not c.foe.alive or not c.me.alive:
            st["ticking"] = False
            return
        tick = c.raw("TickRate", 0.5)
        c.engine.damage(c.me, c.foe, c.val("DPS") * tick, "spirit", self.s.ab.name, is_ability=True,
                        ability=self.s, is_dot=True)
        if c.tier >= 2:
            c.debuff("spirit_outgoing_penalty", abs(c.raw("OutgoingTechDamagePercent")) / 100, tick + 0.05)
        c.after(tick, self.tick, c)


@register("ability_fire_bomb")
class ConcussiveCombustion(AbilityImpl):
    kind = "aoe"
    range_props = ("Radius",)

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.15

    def cast(self, c):
        delay = c.raw("ExplodeDelay", 3.25)
        c.lock_gun(delay)
        c.spirit_hit(c.val("Damage"), delay=delay)
        c.debuff("stun", 1, c.dur("StunDuration"), delay=delay)
        if c.tier >= 2:
            c.buff("spirit_lifesteal", c.raw("LifeStealPercentOnHit") / 100, delay + 0.2, tag="combust_ls")
