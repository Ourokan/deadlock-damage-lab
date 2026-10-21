"""Dynamo (hero_dynamo).

Assumptions:
- Kinetic Pulse: the knock-up is movement only (no stun); T2 bullet-resist shred applies on hit.
- Quantum Entanglement: used defensively below DEFENSIVE_HP; Dynamo is untargetable (invulnerable) and can't
  shoot for AbilityDuration. T3 halves the remaining duration of Dynamo's debuffs.
- Rejuvenating Aurora: channel, cast below HEAL_HP; Dynamo can't shoot while channelling (melee/dash only);
  a stun breaks the channel. Heal lingers AuraLingerDuration after the channel. T3 (NoChannel) removes the
  channel, so Dynamo keeps shooting, and adds HealMaxHealthPercent of max health per second.
- Singularity: stuns the target for the whole channel (status resist shortens it) while ticking DPS; Dynamo
  can't shoot during the channel. Cast when the target is within VacuumRadius + engage margin + ULT_APPROACH
  (Dynamo closes in first; the 7 m radius is under the ~14.5 m duel distance; movement not modeled).
"""
from deadsim.abilities import AbilityImpl, register

DEFENSIVE_HP = 0.35   # Quantum Entanglement used to dodge damage when this low
HEAL_HP = 0.55        # Rejuvenating Aurora used below this health fraction
ULT_APPROACH = 5.0    # m Dynamo walks/blinks in beyond VacuumRadius + engage margin to start Singularity
ENEMY_DEBUFFS = ("stun", "silence", "disarm", "item_silence", "damage_taken_amp", "spirit_amp_taken",
                 "bullet_amp_taken", "bullet_shred", "spirit_shred", "fire_rate_slow", "outgoing_penalty",
                 "spirit_outgoing_penalty", "crit_taken")


@register("citadel_ability_stomp")
class KineticPulse(AbilityImpl):
    kind = "skillshot"
    range_props = ("StompRange",)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        c.spirit_hit(c.val("Damage"), delay=delay)
        if c.tier >= 2:
            hit = c.me.skill.spirit_accuracy
            c.debuff("bullet_shred", abs(c.raw("BulletResistReduction")) / 100 * hit, c.dur("SlowDuration"), delay=delay)


@register("citadel_ability_void_sphere")
class QuantumEntanglement(AbilityImpl):
    kind = "self"

    def in_range(self, c):
        return True

    def should_cast(self, c):
        return c.me.hp_frac < DEFENSIVE_HP and c.foe.alive

    def cast(self, c):
        d = c.raw("AbilityDuration")
        c.buff("invulnerable", 1, d)
        c.lock_gun(d)
        if c.tier >= 3:
            keep = 1.0 - c.raw("ReduceDebuffs") / 100
            now = c.now
            for key in ENEMY_DEBUFFS:
                tags = c.me.mods.d.get(key, {})
                for tg, (v, exp) in list(tags.items()):
                    if exp > now:
                        tags[tg] = (v, now + (exp - now) * keep)


@register("citadel_ability_nikuman")
class RejuvenatingAurora(AbilityImpl):
    kind = "self"

    def in_range(self, c):
        return True

    def should_cast(self, c):
        return c.me.hp_frac < HEAL_HP

    def cast(self, c):
        T = c.dur("AbilityChannelTime")
        channel = c.tier < 3
        if channel:
            c.lock_gun(T)
        c.state["end"] = c.now + T
        c.state["linger_end"] = c.now + T + c.raw("AuraLingerDuration")
        c.after(0.5, self.tick, c, channel)

    def tick(self, c, channel):
        st = c.state
        if not c.me.alive or c.engine.over:
            return
        if channel and c.now <= st["end"] + 1e-9 and c.me.mods.active("stun"):
            st["end"] = st["linger_end"] = c.now          # channel broken
            c.me.gun_locked_until = c.now
            return
        if c.now > st["linger_end"] + 1e-9:
            return
        hps = c.val("HealingPerSecond") + c.raw("HealMaxHealthPercent") / 100 * c.me.max_hp
        c.heal(hps * 0.5)
        c.after(0.5, self.tick, c, channel)


@register("citadel_ability_self_vacuum")
class Singularity(AbilityImpl):
    kind = "aoe"
    range_props = ("VacuumRadius",)

    def in_range(self, c):
        return c.within(c.rng("VacuumRadius") + ULT_APPROACH)

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.15

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        T = c.dur("AbilityChannelTime")
        c.lock_gun(delay + T)
        c.debuff("stun", 1, T, delay=delay)
        c.state["end"] = c.now + delay + T
        tick = c.raw("TickRate", 0.25)
        c.after(delay + tick, self.tick, c, tick)

    def tick(self, c, tick):
        if not c.me.alive or not c.foe.alive or c.now > c.state["end"] + 1e-9:
            return
        if c.me.mods.active("stun"):
            c.me.gun_locked_until = c.now
            return
        dps = c.val("DPS") + c.raw("DPSPercentHealth") / 100 * c.foe.max_hp
        c.engine.damage(c.me, c.foe, dps * tick, "spirit", self.s.ab.name, is_ability=True, ability=self.s,
                        is_dot=True, is_ult=True)
        c.after(tick, self.tick, c, tick)
