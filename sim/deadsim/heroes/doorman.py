"""The Doorman (hero_doorman).

Assumptions:
- Call Bell: impact is a skillshot; the Doorman shoots the bell to detonate it BELL_DETONATE s after the throw
  (fuse is ProjectileFuse otherwise). The explosion (Radius 5.5) lands at the same spirit-accuracy rate as the impact.
  The -40% accuracy debuff has no engine key; it is modeled as evasion on the Doorman worth ACC_TO_EVASION of the
  listed value for AbilityDuration. Throw reach BELL_RANGE (no cast range in data).
- Doorway: no combat effect in a 1v1 except T2's barrier on first travel (CombatBarrier,
  BarrierDuration). Without T2 it is never cast; with T2 it is cast as an escape below DOORWAY_HP.
- Luggage Cart: one hit of CartDamage (skillshot). T2 wall impact: WallImpactDamage (75 + 0.6 x spirit),
  landing on WALL_CHANCE of carts; T3 stun on the same wall impacts.
- Hotel Guest: cast range is short (7 m); the Doorman walks HOTEL_APPROACH m further in than for other
  abilities to land his ult (otherwise it never casts at his usual fighting distance). The target is removed
  (invulnerable, can't act) for the stay. They check out in time on
  1 - LATE_CHANCE of casts after HOTEL_ONTIME of AbilityDuration; otherwise they stay the full duration and take
  LateCheckoutDamage (+ T2 stun). Damage is paid on return. The Doorman holds fire meanwhile.
"""
from deadsim.abilities import AbilityImpl, register

BELL_DETONATE = 1.0
BELL_RANGE = 25.0
ACC_TO_EVASION = 0.5
DOORWAY_HP = 0.4
WALL_CHANCE = 0.5
LATE_CHANCE = 0.35
HOTEL_ONTIME = 0.75
HOTEL_APPROACH = 5.0   # m the Doorman walks in (beyond the usual engage margin) to reach a target for his ult


@register("ability_doorman_bomb")
class CallBell(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.dist <= BELL_RANGE

    def cast(self, c):
        c.lock_gun(c.raw("AbilityPostCastDuration"))
        c.spirit_hit(c.val("ImpactDamage"), delay=0.3)
        acc = c.me.skill.spirit_accuracy
        boom = min(BELL_DETONATE, c.val("ProjectileFuse"))
        c.spirit_hit(c.val("ExplosionDamage"), delay=boom, hit_chance=acc)
        ev = abs(c.raw("DebuffAccuracy")) / 100 * ACC_TO_EVASION * acc
        c.after(boom, lambda: c.me.mods.add("evasion", ev, c.dur("AbilityDuration"), ("doorman_bell", "evasion")))


@register("ability_doorman_doorway")
class Doorway(AbilityImpl):
    kind = "self"

    def should_cast(self, c):
        return c.tier >= 2 and c.me.hp_frac < DOORWAY_HP

    def cast(self, c):
        c.barrier(c.val("CombatBarrier"), c.dur("BarrierDuration"))


@register("ability_doorman_luggage_cart")
class LuggageCart(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        c.spirit_hit(c.val("CartDamage"), delay=delay + 0.3)
        if c.tier >= 2 and c.me.acc("doorman_wall").take(WALL_CHANCE * c.me.skill.spirit_accuracy):
            c.spirit_hit(c.val("WallImpactDamage"), delay=delay + 0.8, hit_chance=1.0)
            if c.tier >= 3:
                c.debuff("stun", 1, c.dur("StunDuration"), delay=delay + 0.8)


@register("ability_doorman_hotel")
class HotelGuest(AbilityImpl):
    kind = "target"

    def in_range(self, c):
        return c.within(c.rng("AbilityCastRange") + HOTEL_APPROACH)

    def cast(self, c):
        ch = c.raw("AbilityChannelTime", 1.0)
        late = bool(c.me.acc("doorman_late").take(LATE_CHANCE))
        stay = c.dur("AbilityDuration") * (1.0 if late else HOTEL_ONTIME)
        c.lock_gun(ch + stay)
        foe = c.foe

        def send():
            if not foe.alive or not c.me.alive:
                return
            foe.mods.add("invulnerable", 1, stay, "hotel_guest")
            foe.mods.add("stun", 1, stay, "hotel_guest")
            c.after(stay, back)

        def back():
            c.spirit_hit(c.val("Damage"))
            if late:
                c.spirit_hit(c.val("LateCheckoutDamage"))
                if c.raw("LateCheckoutStun"):
                    c.debuff("stun", 1, c.raw("LateCheckoutStun"))
        c.after(ch, send)
