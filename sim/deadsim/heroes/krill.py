"""Mo & Krill (hero_krill).

Assumptions:
- Scorn: instant hit after the cast delay on the single target in radius; heals DamageHealMult x damage actually
  dealt (hero multiplier), counting the item procs the hit sets off (Quicksilver Reload, Mystic Burst ...). Replays
  show this: Mo's health jumps by 1.20 x (Scorn + Mystic Burst + Quicksilver) on the same tick. T3 debuff is modeled as a stacking damage_taken_amp (one stack per cast, 16 s each);
  in a 1v1 all damage the foe takes comes from Mo, so this equals "+15% damage from Mo & Krill".
- Burrow: Mo travels underground to the target (BURROW_TRAVEL s, gun locked, burrow bullet/spirit resist active),
  then emerges and spins on top of the target for SpinDuration (gun locked). The knock-up/slow are movement and
  skipped. Emerging marks Mo as "in melee range" for MELEE_WINDOW s so Combo can follow. With fight patterns on
  (default) the first Burrow happens before the fight: Mo emerges on the target at t=0 (Burrow.prefight).
- Sand Blast: wide cone, treated as always landing (kind aoe): damage + disarm for AbilityDuration.
- Combo: 4 m cast range, so it is cast only when within range (+ engage margin) or right after Burrow emerges.
  Stuns the target and deals DPS for the channel; Mo can't shoot. Channel breaks if Mo is stunned or dies.
  T1 +100% lifesteal heals the damage dealt; T2 +50% bullet resist during the channel. T3 (+40 DPS, +0.4 spirit
  scaling) comes from the data via c.val. Max-health-on-kill is ignored (fight ends at the kill).
"""
from deadsim.abilities import AbilityImpl, register

BURROW_TRAVEL = 1.5     # s underground before popping out on the target (engagement at ~12-15 m)
MELEE_WINDOW = 2.5      # s after emerging during which Mo counts as in Combo range
COMBO_TICK = 0.2


class _Base(AbilityImpl):
    """No new cast while another cast/channel has the gun locked."""

    def should_cast(self, c):
        return c.now >= c.me.gun_locked_until and self.cond(c)

    def cond(self, c):
        return self.in_range(c)


@register("ability_intimidate")
class Scorn(_Base):
    kind = "aoe"
    range_props = ("Radius",)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        dmg = c.val("Damage")

        def go():
            if not c.me.alive or not c.foe.alive:
                return
            before = sum(c.me.dmg_out.values())
            c.engine.damage(c.me, c.foe, dmg, "spirit", self.s.ab.name, is_ability=True, ability=self.s)
            c.heal((sum(c.me.dmg_out.values()) - before) * c.raw("DamageHealMult"))   # Scorn + the procs it set off
            if c.tier >= 3:
                c.debuff("damage_taken_amp", c.raw("DamageBonus") / 100, c.dur("DebuffDuration"),
                         tag=("scorn_t3", self.s.casts))
        c.after(delay, go)


@register("ability_burrow")
class Burrow(_Base):
    kind = "self"

    def in_range(self, c):
        return True   # it is the gap closer

    def cast(self, c):
        under = c.raw("AbilityCastDelay") + BURROW_TRAVEL
        spin = c.dur("SpinDuration")
        c.lock_gun(under + spin)
        c.buff("bullet_resist", c.raw("BulletResist") / 100, under, tag="burrow_br")
        c.buff("spirit_resist", c.raw("TechResist") / 100, under, tag="burrow_sr")
        c.dot(c.val("DPS"), spin, delay=under, tick=0.25)
        c.me.counters["krill_close_until"] = c.now + under + MELEE_WINDOW

    # Mo & Krill start most fights already burrowed (Tyler; data/fight_patterns.json "prefight"): the approach
    # happened before t=0, so the fight opens with Mo emerging and spinning on the target, Burrow's cooldown
    # already running for the time spent underground.
    def prefight_lead(self, c):
        return c.raw("AbilityCastDelay") + BURROW_TRAVEL

    def prefight(self, c):
        spin = c.dur("SpinDuration")
        c.lock_gun(spin)
        c.dot(c.val("DPS"), spin, tick=0.25)
        c.me.counters["krill_close_until"] = c.now + MELEE_WINDOW


@register("ability_throw_sand")
class SandBlast(_Base):
    kind = "aoe"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        c.spirit_hit(c.val("Damage"), delay=delay)
        c.debuff("disarm", 1, c.dur("AbilityDuration"), delay=delay)


@register("ability_ult_combo")
class Combo(_Base):
    kind = "target"

    def in_range(self, c):
        if c.now <= c.me.counters.get("krill_close_until", -1) and \
                c.now >= c.me.counters["krill_close_until"] - MELEE_WINDOW:
            return True
        return c.dist <= c.rng("AbilityCastRange") + c.me.skill.engage_margin

    def cast(self, c):
        dur = c.dur("AbilityChannelTime")
        dps = c.val("DPS")
        c.lock_gun(dur)
        c.debuff("stun", 1, dur)
        if c.tier >= 2:
            c.buff("bullet_resist", c.raw("BulletResist") / 100, dur, tag="combo_br")
        ls = c.raw("LifeStealPercentOnHit") / 100
        n = max(1, int(round(dur / COMBO_TICK)))
        per = dps * dur / n
        end = c.now + dur

        def tick(i):
            if not c.me.alive or not c.foe.alive or c.me.mods.active("stun") or c.now > end + 1e-6:
                return
            amt = c.engine.damage(c.me, c.foe, per, "spirit", self.s.ab.name, is_ability=True, ability=self.s,
                                  is_dot=True, is_ult=True)
            if ls:
                c.heal(amt * ls)
            if i + 1 < n:
                c.after(COMBO_TICK, tick, i + 1)
        c.after(COMBO_TICK, tick, 0)
