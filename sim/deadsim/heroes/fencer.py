"""Apollo (hero_fencer).

Assumptions:
- Disengaging Sigil: the sigil is drawn SIGIL_OFFSET m in front, so it reaches SIGIL_OFFSET + SigilRadius. The
  leap back is skipped. T1 fire rate buff for BuffDuration; T3 recast lands a second sigil RECAST_DELAY s later.
- Riposte: cast while the enemy is shooting and within DashRange; Apollo can't shoot during the
  AbilityChannelTime window. The first enemy damage instance in the window is negated (any instance, the
  DamageThreshold is ignored), then Apollo is invulnerable for RIPOSTE_INVULN, dashes in, stuns
  (StunDuration), reduces melee resist and follows up with one light melee (Riposte itself deals no damage in
  the game, so the follow-up is booked as melee). If nothing hits him, it whiffs. T3 lifesteal 75% (bullet + spirit) for TargetLifestealDuration.
- Flawless Advance: MaxStabs lunges STAB_INTERVAL apart, each a skillshot; PERFECT_RATE of them are perfect
  (PerfectDamage), the rest MaxDamageBeforePerfect. Gun locked while lunging. T1 heals HealFixedHealth per
  perfect hit (35 + 1.3 x spirit per the data; the tooltip only says "Heal 35", so the scaling is doubtful). T2 bullet resist
  for DashBuffDuration per lunge. T3: flat damage adds and x1.15 spirit scaling (applied by c.val).
- Itani Lo Sahn: cast when the target is at or below ULT_HP. After the 1.5 s charge the slash lands
  (skillshot): ImpactDamage, then the target is frozen (stun, no healing, takes 70% less damage) for
  DebuffDuration while Apollo is invulnerable and locked; on expiry DelayedDamage, +BonusDamagePercent if the
  target is below LowHealthEnemyThresholdPct.
"""
from deadsim.abilities import AbilityImpl, register

SIGIL_OFFSET = 3.0
RECAST_DELAY = 1.5
RIPOSTE_INVULN = 0.5
STAB_INTERVAL = 0.9
PERFECT_RATE = 0.7
ULT_HP = 0.6


@register("ability_fencer_throwblade")
class DisengagingSigil(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.within(SIGIL_OFFSET + c.val("SigilRadius"))

    def cast(self, c):
        delay = c.raw("AbilityCastDelay", 0.5)
        c.lock_gun(delay)
        c.spirit_hit(c.val("Damage"), delay=delay)
        if c.tier >= 1:
            c.buff("fire_rate", c.raw("BonusFireRate") / 100, c.raw("BuffDuration"))
        if c.tier >= 3:
            c.spirit_hit(c.val("Damage"), delay=delay + RECAST_DELAY)


class _Parry:
    """Injected into Apollo's items_fx: negates the first hit during the Riposte window."""

    def __init__(self, st):
        self.st = st

    def reduce_incoming(self, f, src, amt, kind, is_dot):
        c = self.st.ctx
        if c.state.get("window_until", -1) < c.now or is_dot:
            return amt
        c.state["window_until"] = -1
        self.st.impl.counter(c)
        return 0.0


@register("ability_fencer_riposte")
class Riposte(AbilityImpl):
    kind = "target"
    range_props = ("DashRange",)

    def start(self, c):
        c.me.items_fx.append(_Parry(self.s))

    def should_cast(self, c):
        foe = c.foe
        return self.in_range(c) and foe.can_shoot() and foe.clip > 0

    def cast(self, c):
        w = c.raw("AbilityChannelTime", 0.8)
        c.state["window_until"] = c.now + w
        c.lock_gun(w)

    def counter(self, c):
        f = c.me
        f.mods.add("invulnerable", 1, RIPOSTE_INVULN, "riposte")
        f.gun_locked_until = c.now
        c.debuff("stun", 1, c.val("StunDuration"))
        c.debuff("melee_resist", c.raw("MeleeResistReduction") / 100, c.val("MeleeResistReductionDuration"))
        c.melee_hit(c.light_melee(), delay=0.2, name="Melee (Riposte follow-up)")
        if c.tier >= 3:
            ls = c.raw("TargetLifesteal") / 100
            d = c.raw("TargetLifestealDuration")
            c.buff("bullet_lifesteal", ls, d)
            c.buff("spirit_lifesteal", ls, d)


@register("ability_fencer_lunge")
class FlawlessAdvance(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.within(c.val("SlashLength"))

    def cast(self, c):
        n = int(c.raw("MaxStabs", 3))
        start = c.raw("AbilityCastDelay")
        c.lock_gun(start + n * STAB_INTERVAL)
        perfect = c.val("PerfectDamage")
        good = c.val("MaxDamageBeforePerfect")
        for i in range(n):
            t = start + (i + 1) * STAB_INTERVAL
            is_perfect = bool(c.me.acc("apollo_perfect").take(PERFECT_RATE))
            c.spirit_hit(perfect if is_perfect else good, delay=t)
            if is_perfect and c.tier >= 1:
                heal = c.val("HealFixedHealth") * c.me.skill.spirit_accuracy
                c.after(t, lambda h=heal: c.me.alive and c.heal(h))
            if c.tier >= 2:
                c.after(t - STAB_INTERVAL + 0.3, lambda: c.buff("bullet_resist", c.raw("BulletResist") / 100,
                                                                 c.raw("DashBuffDuration")))


@register("ability_fencer_ultimate")
class ItaniLoSahn(AbilityImpl):
    kind = "skillshot"
    range_props = ("DashRange",)

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac <= ULT_HP

    def cast(self, c):
        charge = c.raw("AbilityCastDelay", 1.5)
        frozen = c.raw("DebuffDuration", 1.8)
        c.lock_gun(charge + frozen)
        if not c.me.acc("apollo_ult").take(c.me.skill.spirit_accuracy):
            return

        def slash():
            if not c.me.alive or not c.foe.alive:
                return
            c.spirit_hit(c.val("ImpactDamage"), hit_chance=1.0)
            foe = c.foe
            foe.mods.add("stun", 1, frozen, "itani")
            foe.mods.add("heal_received", -1.0, frozen, "itani")
            foe.mods.add("damage_taken_amp", -c.raw("IncomingDamageReductionPercent") / 100, frozen, "itani")
            c.me.mods.add("invulnerable", 1, frozen, "itani")
            c.after(frozen, finish)

        def finish():
            if not c.foe.alive:
                return
            dmg = c.val("DelayedDamage")
            if c.foe.hp_frac < c.raw("LowHealthEnemyThresholdPct", 50) / 100:
                dmg *= 1.0 + c.raw("BonusDamagePercent") / 100
            c.spirit_hit(dmg, hit_chance=1.0)
        c.after(charge, slash)
