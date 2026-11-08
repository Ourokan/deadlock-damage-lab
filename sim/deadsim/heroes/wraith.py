"""Wraith (hero_wraith).

Assumptions:
- Card Trick: gun hits on the hero build card resource (CardResourcePerBulletHit, ...PerBulletCrit for
  headshots); every ResourcePerCard makes a card, stored up to the ability's max charges. Wraith enters the
  fight with a full hand (cards are farmed beforehand). Cards home (kind 'target'), one per
  CooldownBetweenCards. With fight draws (Skill.fight_phase or the engine rng) the opening hand is drawn from
  Phantom+ replays instead (ENTRY_HAND), capped at max charges. Suits rotate Spade, Diamond, Club, Heart (expected value of a random suit, no Jokers):
  Spade +SpadeDamageBonus% damage, Diamond shreds bullet and spirit resist by DiamondResistShred% for
  DiamondResistShredDuration, Club slow (ignored), Heart heals HeartHeal.
- Project Mind: a teleport, so only cast when T2's barrier exists and Wraith is under 50% health. Barrier =
  CombatBarrier (300 + 1.7 x spirit power from T2).
- Full Auto: +BonusFireRate% fire rate and MagicDamagePerBullet spirit damage per bullet hit. T3 unlimited ammo
  is modeled as enough bonus ammo for the duration (removed at the end); a reload already in progress finishes.
- Telekinesis: Wraith walks up to LIFT_APPROACH m beyond cast range + engage margin to reach the target (the
  10 m range is under the ~16 m duel distance; movement not modeled). After AbilityCastDelay the target is lifted (stunned) for AbilityDuration, then slammed for
  Damage. Wraith keeps shooting the lifted target (channel not modeled).
"""
import zlib

from deadsim.abilities import AbilityImpl, register

LIFT_APPROACH = 5.0     # m Wraith closes beyond cast range + engage margin to reach Telekinesis range
SUITS = ("spade", "diamond", "club", "heart")

# Wraith's hand at a fight's start, Phantom+ replays (2026-11-08, 890 distinct replays, 4,538 engagements of >= 3 s
# with a gap of >= 10 s before): cards that hit a hero within 3 s of the first one (0 when none hit in the whole
# engagement, 22%). Real Wraiths spend cards on creeps and pokes between fights: 1.4 per opening burst (1.8 within
# 3 s of a first card) where the sim's full hand of 4 threw 3.9; first card a median 2.5 s in, both. Shares of
# 0, 1, 2, 3, 4, 5+ cards.
ENTRY_HAND = (984, 1822, 1040, 452, 162, 78)
ENTRY_HAND_DRAW = True
MELEE_CARDS = True   # melee hits build cards too (CardResourcePerLightMelee 10, PerHeavyMelee 25)


def entry_hand(c, cap):
    """Cards at the fight's start: a draw from ENTRY_HAND, capped at cap; cap (a full hand) without fight draws."""
    f = c.me
    phase, rng = f.skill.fight_phase, f.e.rng
    if not ENTRY_HAND_DRAW or (phase is None and rng is None):
        return cap
    u = (phase + zlib.crc32(f"wraith_hand|{f.name}".encode()) / 2 ** 32) % 1.0 if phase is not None else rng.random()
    tot, acc = sum(ENTRY_HAND), 0
    for k, n in enumerate(ENTRY_HAND):
        acc += n
        if u < acc / tot:
            return min(cap, k)
    return cap


@register("citadel_ability_card_toss")
class CardTrick(AbilityImpl):
    kind = "target"

    def start(self, c):
        c.state.update(cards=entry_hand(c, self.s.max_charges()), res=0.0, next=0.0, suit=0)

    def on_damage_dealt(self, c, target, hit):
        melee = MELEE_CARDS and hit.kind == "melee" and hit.source == "melee"
        if not melee and (hit.kind != "bullet" or hit.source != "gun" or not hit.hits):
            return
        st = c.state
        cap = self.s.max_charges()
        if st.get("cards", 0) >= cap:
            return
        if melee:   # CardResourcePerLightMelee / PerHeavyMelee (the sim built cards from gun hits only)
            heavy = c.me.counters.get("melee_heavy")
            w = c.me.counters.get("melee_weight", 1.0)
            st["res"] += w * c.raw("CardResourcePerHeavyMelee" if heavy else "CardResourcePerLightMelee")
        else:
            body = hit.hits - hit.headshots
            st["res"] += body * c.raw("CardResourcePerBulletHit") + hit.headshots * c.raw("CardResourcePerBulletCrit")
        per = c.raw("ResourcePerCard", 100)
        while st["res"] >= per and st["cards"] < cap:
            st["res"] -= per
            st["cards"] += 1

    def should_cast(self, c):
        st = c.state
        return st.get("cards", 0) >= 1 and c.now >= st.get("next", 0.0) and self.in_range(c)

    def cast(self, c):
        st = c.state
        st["cards"] -= 1
        st["next"] = c.now + c.raw("CooldownBetweenCards", 0.5)
        c.lock_gun(c.raw("AbilityPostCastDuration"))
        suit = SUITS[st["suit"] % 4]
        st["suit"] += 1
        dmg = c.val("Damage")
        if suit == "spade":
            dmg *= 1 + c.raw("SpadeDamageBonus") / 100
        elif suit == "diamond":
            shred = abs(c.raw("DiamondResistShred")) / 100
            d = c.raw("DiamondResistShredDuration", 5.0)
            c.debuff("bullet_shred", shred, d, tag="card_diamond_b")
            c.debuff("spirit_shred", shred, d, tag="card_diamond_s")
        elif suit == "heart":
            c.heal(c.val("HeartHeal"))
        c.spirit_hit(dmg)


@register("citadel_ability_projectmind")
class ProjectMind(AbilityImpl):
    kind = "self"

    def should_cast(self, c):
        return c.tier >= 2 and c.me.hp_frac < 0.5

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        amt = c.val("CombatBarrier")
        c.after(delay, c.barrier, amt, c.dur("BarrierDuration"))


@register("citadel_ability_wraith_rapidfire")
class FullAuto(AbilityImpl):
    kind = "self"

    def in_range(self, c):
        return c.reach(30)

    def cast(self, c):
        d = c.dur("AbilityDuration")
        c.state["until"] = c.now + d
        fr = c.raw("BonusFireRate") / 100
        c.buff("fire_rate", fr, d)
        if c.tier >= 3 and c.raw("UnlimitedAmmo"):
            st = c.me.st
            c.me.bonus_ammo += int(d * (1 + c.me.fire_rate() + fr) / st.cycle_time) + 1
            c.after(d, self.end_ammo, c)

    def end_ammo(self, c):
        c.me.bonus_ammo = 0

    def on_damage_dealt(self, c, target, hit):
        if hit.kind == "bullet" and hit.source == "gun" and hit.hits and c.now <= c.state.get("until", -1):
            c.spirit_hit(c.val("MagicDamagePerBullet") * hit.hits, hit_chance=1.0)


@register("citadel_ability_psychic_lift")
class Telekinesis(AbilityImpl):
    kind = "target"
    range_props = ("AbilityCastRange",)

    def in_range(self, c):
        return c.within(c.rng("AbilityCastRange") + LIFT_APPROACH)

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.15

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        d = c.dur("AbilityDuration")
        c.debuff("stun", 1, d, delay=delay)
        c.spirit_hit(c.val("Damage"), delay=delay + d)
