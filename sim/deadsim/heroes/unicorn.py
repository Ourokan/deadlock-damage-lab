"""Celeste (hero_unicorn).

Assumptions:
- Light Eater: the cone always hits (10 m cone, fight at 12-15 m). For AbilityDuration, Celeste's gun hits on the
  target deal the listed Damage as spirit damage, at most once per TickRate. The hero spirit lifesteal is a buff
  for the same window. AbilityDuration scales with spirit power (data) and ability duration items.
- Dazzling Trick: cast when Celeste has lost over 10% health, by DAZZLE_BY_S into the fight anyway (Phantom+
  replays: median first cast 2.56 s), and with T3 right before Shining Wonder so the orb can bounce off the prism.
  A health trigger alone made a Celeste who arrives at full health cast her ult without the prism (a quarter of
  the ult damage), so healing items cost her damage. If the prism barrier breaks before MaxLifetime, the
  foe is silenced and takes BarrierDamagePercentage of the barrier as spirit damage, if within ExplodeRadius.
- Radiant Daggers: ground-targeted, so it is a skillshot that lands after cast delay + PreExplosionDuration.
  Each expected hit adds a stack (spirit_accuracy of a stack) after BuffDelay. +MagicIncreasePerStack% spirit
  damage is modeled as spirit_amp_taken on the foe (only Celeste damages him in a 1v1). T3 adds fire rate per stack.
- Shining Wonder: one aimed hit. In a 1v1 there is nothing else to bounce to. With Dazzling Trick T3 ("allows
  Shining Wonder bounce") and the prism up, the orb bounces back off Celeste once per ORB_ROUNDTRIP, up to
  MaxBounces // 2 extra hits while the prism lasts (guess).
"""
from deadsim.abilities import AbilityImpl, register

ORB_ROUNDTRIP = 1.0   # s for the ult orb to bounce prism -> enemy (not in data)
DAZZLE_HP_TRIGGER = 0.9
DAZZLE_BY_S = 2.5


# ---- Celeste ---------------------------------------------------------------------------------------------
@register("ability_unicorn_radiantblast")
class LightEater(AbilityImpl):
    kind = "aoe"

    def start(self, c):
        c.state.update(until=-1.0, next=0.0)

    def cast(self, c):
        d = c.raw("AbilityCastDelay")
        c.lock_gun(d)
        c.spirit_hit(c.val("FlareDamage"), delay=d)
        dur = c.val("AbilityDuration") * (1.0 + c.s.duration_pct())
        c.state["until"] = c.now + d + dur
        c.state["dmg"] = c.val("Damage")
        c.buff("spirit_lifesteal", c.raw("AbilityLifestealPercentHero") / 100, d + dur, tag="light_eater_ls")

    def on_damage_dealt(self, c, target, hit):
        st = c.state
        if hit.kind != "bullet" or hit.source != "gun" or not hit.hits:
            return
        if c.now < st["until"] and c.now >= st["next"]:
            st["next"] = c.now + c.raw("TickRate", 0.5)
            c.spirit_hit(st["dmg"], hit_chance=1.0)


@register("ability_unicorn_prismaticguard")
class DazzlingTrick(AbilityImpl):
    kind = "self"

    def start(self, c):
        c.state.update(entry=None, popped=True)

    def should_cast(self, c):
        return c.foe.alive and (c.me.hp_frac < DAZZLE_HP_TRIGGER or c.now >= DAZZLE_BY_S or self.ult_next(c))

    def ult_next(self, c):
        """T3 lets Shining Wonder bounce off the prism: put the prism up when the ult is ready to go."""
        if c.tier < 3:
            return False
        return any(ab.ab.class_name == "ability_unicorn_dazzlingorb" and ab.unlocked and ab.ready_at + ab.recast_wait <= c.now
                   for ab in c.me.abilities)

    def cast(self, c):
        amt = c.val("CombatBarrier")
        c.barrier(amt, c.dur("MaxLifetime"))
        c.state.update(entry=c.me.barriers[-1], popped=False, amount=amt)

    def prism_left(self, c):
        """Seconds the prism still stands (0 if gone)."""
        e = c.state.get("entry")
        if not e or c.state.get("popped") or e[0] <= 0:
            return 0.0
        return max(0.0, e[1] - c.now)

    def on_damage_taken(self, c, src, hit):
        st = c.state
        e = st.get("entry")
        if not e or st["popped"] or e[0] > 0 or c.now >= e[1]:
            return
        st["popped"] = True
        p = c.p_in(c.rng("ExplodeRadius"))
        if p > 0:
            c.spirit_hit(c.raw("BarrierDamagePercentage") / 100 * st["amount"] * p, hit_chance=1.0)
            c.debuff("silence", 1, c.dur("DebuffDuration") * p)


@register("ability_unicorn_luminousstrike")
class RadiantDaggers(AbilityImpl):
    kind = "skillshot"

    def start(self, c):
        c.state["stacks"] = 0.0

    def cast(self, c):
        delay = c.raw("AbilityCastDelay") + c.raw("PreExplosionDuration")
        c.lock_gun(c.raw("AbilityCastDelay"))
        c.spirit_hit(c.val("ImpactDamage"), delay=delay)
        c.after(delay + c.raw("BuffDelay"), self.stack, c, c.me.skill.spirit_accuracy)

    def stack(self, c, amount):
        if not c.me.alive or not c.foe.alive:
            return
        st = c.state
        st["stacks"] = min(c.raw("BuffMaxStacks"), st["stacks"] + amount)
        dur = c.raw("BuffDuration")
        c.foe.mods.add("spirit_amp_taken", st["stacks"] * c.raw("MagicIncreasePerStack") / 100, dur,
                       ("celeste_daggers", "amp"))
        if c.raw("FireRatePerStack"):
            c.buff("fire_rate", st["stacks"] * c.raw("FireRatePerStack") / 100, dur, tag="celeste_daggers_fr")


@register("ability_unicorn_dazzlingorb")
class ShiningWonder(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        d = c.raw("AbilityCastDelay")
        c.lock_gun(d)
        dmg = c.val("Damage")
        c.spirit_hit(dmg, delay=d)
        for ab in c.me.abilities:
            if ab.ab.class_name == "ability_unicorn_prismaticguard" and ab.unlocked and ab.tier >= 3:
                left = ab.impl.prism_left(ab.ctx) - d
                n = min(int(c.raw("MaxBounces")) // 2, int(max(0.0, left) / ORB_ROUNDTRIP))
                for i in range(1, n + 1):
                    c.spirit_hit(dmg, delay=d + i * ORB_ROUNDTRIP)
