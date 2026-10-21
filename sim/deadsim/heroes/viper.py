"""Vyper (hero_viper).

Assumptions:
- Screwjab Dagger: Damage + DamagePerStack x (stacks already on the target); each landed dagger adds a stack
  (MaxStacks) lasting StackDuration. Slow is skipped. T2 bullet resist reduction (base + per stack) is applied
  as bullet shred for StackDuration. T3 refunds CooldownRefundPercent of the charge cooldown on hit.
  Thrown out to DAGGER_RANGE.
- Lethal Venom: lock-on (AbilityCastRange + 0.2 m per boon). After VenomDuration it deals damage interpolated
  between VenomMinDamage (target at >= 100% health) and VenomMaxDamage (target at <= 30%) from the target's
  health at that moment. Vyper casts it once the target is below VENOM_CAST_HP. T2 healing penalty lasts while
  the venom is pending. T3: each gun hit adds BuildUpPerShot % (resets after BuildUpDuration without hits);
  at 100% a venom is applied if none is pending. Venom ignores Petrify's damage block.
- Slither: movement only. T3 barrier CombatBarrier (180 + spirit scaling, via c.val) for BuffDuration,
  on every slide, which is assumed to be used whenever the T3 cooldown is ready.
- Petrifying Bola: assumed direct hit: Damage + PetrifyDamage, then the target is stunned and immune to damage
  for PetrifyDuration. Vyper stops shooting meanwhile (would be wasted). Thrown out to BOLA_RANGE.
"""
from deadsim.abilities import AbilityImpl, register

DAGGER_RANGE = 30.0          # m (no range in data)
BOLA_RANGE = 25.0            # m (no range in data)
VENOM_CAST_HP = 0.75         # cast Lethal Venom once the target is below this health fraction


def venom_damage(c, ab_ctx, target):
    lo, hi = ab_ctx.val("VenomMinDamage"), ab_ctx.val("VenomMaxDamage")
    hp_hi = ab_ctx.raw("VenomMinDamageHealthPercentage", 100) / 100
    hp_lo = ab_ctx.raw("VenomMaxDamageHealthPercentage", 30) / 100
    x = (hp_hi - target.hp_frac) / max(1e-6, hp_hi - hp_lo)
    return lo + (hi - lo) * min(1.0, max(0.0, x))


@register("ability_viper_debuffdagger")
class ScrewjabDagger(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(DAGGER_RANGE)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        st = c.state
        if c.now > st.get("until", -1):
            st["stacks"] = 0
        stacks = st.get("stacks", 0)
        c.spirit_hit(c.val("Damage") + c.val("DamagePerStack") * stacks, delay=delay)
        st["stacks"] = min(int(c.raw("MaxStacks", 3)), stacks + 1)
        sd = c.dur("StackDuration", 10)
        st["until"] = c.now + sd
        acc = c.me.skill.spirit_accuracy
        if c.raw("BulletResistReduction"):
            red = abs(c.raw("BulletResistReduction")) + abs(c.raw("BulletResistReductionPerStack")) * st["stacks"]
            c.debuff("bullet_shred", red / 100 * acc, sd, delay=delay)
        if c.raw("CooldownRefundPercent") and self.s.next_charge:
            self.s.next_charge -= c.raw("CooldownRefundPercent") / 100 * self.s.cooldown() * acc


@register("ability_viper_venom")
class LethalVenom(AbilityImpl):
    kind = "target"

    def start(self, c):
        c.state.update(pending_until=-1.0, meter=0.0, last=-99.0)

    def in_range(self, c):
        r = c.raw("AbilityCastRange", 10) + 0.2 * c.me.st.boons
        r *= 1.0 + self.s.range_pct()
        return c.within(r)

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac <= VENOM_CAST_HP and c.now >= c.state["pending_until"]

    def cast(self, c):
        self.apply(c)

    def apply(self, c):
        d = c.raw("VenomDuration", 3.0)
        c.state["pending_until"] = c.now + d
        if c.raw("HealAmpReceivePenaltyPercent"):
            c.debuff("heal_received", c.raw("HealAmpReceivePenaltyPercent") / 100, d)
        c.after(d, self.trigger, c)

    def trigger(self, c):
        f, e = c.me, c.foe
        if not (f.alive and e.alive):
            return
        dmg = venom_damage(c, c, e)
        # Lethal Venom ignores Petrify's damage block: lift our own petrify immunity for this hit.
        petr = e.mods.d.get("invulnerable", {}).get("viper_petrify")
        if petr:
            e.mods.remove("invulnerable", "viper_petrify")
        c.spirit_hit(dmg)
        if petr and e.alive:
            e.mods.d.setdefault("invulnerable", {})["viper_petrify"] = petr

    def on_damage_dealt(self, c, target, hit):
        if not c.raw("BuildUpPerShot") or hit.kind != "bullet" or hit.source != "gun" or not hit.hits:
            return
        st = c.state
        if c.now < st["pending_until"]:
            return
        if c.now - st["last"] > c.raw("BuildUpDuration", 5):
            st["meter"] = 0.0
        st["last"] = c.now
        st["meter"] += hit.hits * c.raw("BuildUpPerShot")
        if st["meter"] >= 100:
            st["meter"] = 0.0
            self.apply(c)


@register("ability_viper_snakedash")
class Slither(AbilityImpl):
    kind = "self"

    def should_cast(self, c):
        return c.tier >= 3 and c.raw("AbilityCooldown") > 0

    def cast(self, c):
        c.barrier(c.val("CombatBarrier"), c.dur("BuffDuration", 4))


@register("ability_viper_petrifybola")
class PetrifyingBola(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(BOLA_RANGE)

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.15

    def cast(self, c):
        delay = c.raw("AbilityCastDelay") + c.dist / 25.0   # bola flight ~25 m/s
        c.lock_gun(c.raw("AbilityCastDelay"))
        c.spirit_hit(c.val("Damage") + c.val("PetrifyDamage"), delay=delay)
        acc = c.me.skill.spirit_accuracy
        d = c.raw("PetrifyDuration") * acc
        c.debuff("stun", 1, d, delay=delay + 0.01)
        c.debuff("invulnerable", 1, d, tag="viper_petrify", delay=delay + 0.01)
        c.after(delay, lambda: c.lock_gun(d * (1.0 - c.foe.st.status_resist)))
