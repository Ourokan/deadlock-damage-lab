"""Shiv (hero_shiv).

Assumptions:
- Rage (passive half of Killing Blow; only active once the ult is unlocked): bullet / spirit damage dealt adds
  RagePerWeaponDamage / RagePerSpiritDamage per point; the bar holds RAGE_MAX (= BonusAbilityResource) rage.
  Drain only starts RageDrainDelayDuration s after the last damage, which never happens mid-fight, so it is
  ignored. At full rage Shiv deals +BuffDamage% damage, modeled as damage_taken_amp on the target (1v1).
- Serrated Knives: skillshot; each landed knife adds a bleed stack and refreshes the bleed; the bleed ticks
  stacks x BleedDPSPerStack every BleedTickRate. Stacks reset once the bleed lapses. At full rage each knife also
  deals FullRageCurrentHealthDamagePct (+ scaling) of the target's current health. T3 (+12 bleed DPS per stack,
  +0.07 spirit scaling) comes from the data via c.val.
- Slice and Dice: aimed dash (skillshot) through the target within DashRange: impact damage + stacking spirit
  resist reduction (TechArmorDamageReduction, one stack per hit, DebuffDuration each). T3 refunds
  CooldownReductionOnHit s on a hero hit.
- Bloodletting: passive part defers DamagePctDeferred% of every incoming hit (+DamagePctDeferredMaxRage% at full
  rage), taken back evenly over DeferredDamageDuration (1 s ticks). Implemented as a reduce_incoming hook, so it
  acts before barrier and lethality. Active clears DeferClearPct% of the pending deferred damage; cast only when
  at least CLEAR_MIN damage is pending. T3 data (+15 DamagePctDeferred) used as is.
- Killing Blow: cast only when the target is below EnemyHealthPercent (buffer ignored) and in cast range (+ the
  usual engage margin): executes (pure damage = remaining health). The recast window is irrelevant in 1v1.
"""
from deadsim.abilities import AbilityImpl, register

CLEAR_MIN = 120.0       # min pending deferred damage worth clearing with Bloodletting's active
DEFER_TICK = 1.0
DEFER_SRC = "Bloodletting (deferred)"


def full_rage(f):
    return f.counters.get("shiv_full_rage", False)


@register("citadel_ability_shiv_dagger")
class SerratedKnives(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.dist <= 30.0   # thrown projectile, no range in data

    def start(self, c):
        c.state.update(stacks=0, until=-1.0)

    def cast(self, c):
        delay = c.raw("AbilityChannelTime")
        c.lock_gun(delay + c.raw("AbilityPostCastDuration"))
        if not c.me.acc("shiv_knife").take(c.me.skill.spirit_accuracy, 1):
            return
        c.after(delay, self.land, c)

    def land(self, c):
        if not c.me.alive or not c.foe.alive:
            return
        st = c.state
        if c.now > st["until"]:
            st["stacks"] = 0
        st["stacks"] += 1
        dur = c.val("BleedDuration")
        st["until"] = c.now + dur
        per = c.val("BleedDPSPerStack")
        c.dot(per * st["stacks"], dur, tick=c.raw("BleedTickRate", 1.0), tag="shiv_bleed")
        if full_rage(c.me):
            pct = c.val("FullRageCurrentHealthDamagePct") / 100
            c.spirit_hit(c.foe.hp * pct, hit_chance=1.0, name="Serrated Knives (rage)")


@register("citadel_ability_shiv_dash")
class SliceAndDice(AbilityImpl):
    kind = "skillshot"
    range_props = ("DashRange",)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay + c.raw("AbilityPostCastDuration"))
        if not c.me.acc("shiv_dash").take(c.me.skill.spirit_accuracy, 1):
            return
        c.spirit_hit(c.val("ImpactDamage"), delay=delay, hit_chance=1.0)
        c.debuff("spirit_shred", abs(c.raw("TechArmorDamageReduction")) / 100, c.dur("DebuffDuration"),
                 tag=("shiv_dash_shred", self.s.casts), delay=delay)
        red = c.raw("CooldownReductionOnHit")
        if red:
            self.s.ready_at -= red
            self.s.next_charge = self.s.ready_at


class _Deferrer:
    """Pseudo item effect on Shiv: defers part of incoming damage (Bloodletting passive)."""

    def __init__(self, impl):
        self.impl = impl

    def reduce_incoming(self, f, src, amt, kind, is_dot):
        impl = self.impl
        c = impl.s.ctx
        if not impl.s.unlocked or c.state.get("bypass"):
            return amt
        pct = c.raw("DamagePctDeferred") + (c.raw("DamagePctDeferredMaxRage") if full_rage(f) else 0.0)
        part = amt * pct / 100
        if part <= 0:
            return amt
        n = max(1, int(round(c.raw("DeferredDamageDuration", 6.0) / DEFER_TICK)))
        c.state["pending"].append([part / n, n])
        c.state["total"] += part
        if not c.state["ticking"]:
            c.state["ticking"] = True
            c.after(DEFER_TICK, impl.tick, c)
        return amt - part


@register("citadel_ability_shiv_defer_damage")
class Bloodletting(AbilityImpl):
    kind = "self"

    def start(self, c):
        c.state.update(pending=[], total=0.0, ticking=False, bypass=False)
        c.me.items_fx.append(_Deferrer(self))

    def tick(self, c):
        st = c.state
        if not c.me.alive or c.engine.over:
            st["ticking"] = False
            return
        dmg = 0.0
        for p in st["pending"]:
            dmg += p[0]
            p[1] -= 1
        st["pending"] = [p for p in st["pending"] if p[1] > 0]
        st["total"] = sum(p[0] * p[1] for p in st["pending"])
        if dmg > 0:
            f = c.me
            f.hp -= dmg
            f.dmg_in[DEFER_SRC] = f.dmg_in.get(DEFER_SRC, 0.0) + dmg
            c.foe.dmg_out[DEFER_SRC] = c.foe.dmg_out.get(DEFER_SRC, 0.0) + dmg
            if f.hp <= 0:    # let the engine handle death (on_lethal items etc.)
                f.hp = 1e-6
                st["bypass"] = True
                c.engine.damage(c.foe, f, 1.0, "pure", DEFER_SRC, ignore_resist=True, procs=False)
                st["bypass"] = False
        if st["pending"]:
            c.after(DEFER_TICK, self.tick, c)
        else:
            st["ticking"] = False

    def should_cast(self, c):
        return c.state.get("total", 0.0) >= CLEAR_MIN

    def cast(self, c):
        keep = 1.0 - c.raw("DeferClearPct") / 100
        def go():
            for p in c.state["pending"]:
                p[0] *= keep
            c.state["total"] *= keep
        c.lock_gun(c.raw("AbilityCastDelay"))
        c.after(c.raw("AbilityCastDelay"), go)


@register("citadel_ability_shiv_killing_blow")
class KillingBlow(AbilityImpl):
    kind = "target"

    def start(self, c):
        c.state["rage"] = 0.0
        c.me.counters["shiv_full_rage"] = False

    def on_damage_dealt(self, c, target, hit):
        if c.me.counters.get("shiv_full_rage") or hit.amount <= 0:
            return
        if hit.kind == "bullet":
            c.state["rage"] += hit.amount * c.raw("RagePerWeaponDamage")
        elif hit.kind == "spirit":
            c.state["rage"] += hit.amount * c.raw("RagePerSpiritDamage")
        if c.state["rage"] >= c.raw("BonusAbilityResource", 10.0):
            c.me.counters["shiv_full_rage"] = True
            c.engine.note(f"{c.me.name} reaches full rage")
            c.debuff("damage_taken_amp", c.raw("BuffDamage") / 100, 1e6, tag="shiv_rage")

    def should_cast(self, c):
        thr = c.raw("EnemyHealthPercent") / 100
        return c.foe.hp_frac < thr and c.within(c.rng("AbilityCastRange"))

    def cast(self, c):
        delay = max(c.raw("AbilityCastDelay"), c.raw("MinTimeToTarget"))
        c.lock_gun(delay + c.raw("AbilityPostCastDuration"))

        def go():
            if c.me.alive and c.foe.alive:
                c.engine.damage(c.me, c.foe, c.foe.hp + 1.0, "pure", self.s.ab.name, ignore_resist=True,
                                is_ability=True, ability=self.s, is_ult=True)
        c.after(delay, go)
