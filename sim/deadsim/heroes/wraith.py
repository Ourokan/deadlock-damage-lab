"""Wraith (hero_wraith).

Assumptions:
- Card Trick: gun hits on the hero build card resource (CardResourcePerBulletHit, ...PerBulletCrit for
  headshots); every ResourcePerCard makes a card, stored up to the ability's max charges. Wraith enters the
  fight with a full hand (cards are farmed beforehand). Cards home (kind 'target'), one per
  CooldownBetweenCards. Suits rotate Spade, Diamond, Club, Heart (expected value of a random suit, no Jokers):
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
from deadsim.abilities import AbilityImpl, register

LIFT_APPROACH = 5.0     # m Wraith closes beyond cast range + engage margin to reach Telekinesis range
SUITS = ("spade", "diamond", "club", "heart")


@register("citadel_ability_card_toss")
class CardTrick(AbilityImpl):
    kind = "target"

    def start(self, c):
        c.state.update(cards=self.s.max_charges(), res=0.0, next=0.0, suit=0)

    def on_damage_dealt(self, c, target, hit):
        if hit.kind != "bullet" or hit.source != "gun" or not hit.hits:
            return
        st = c.state
        cap = self.s.max_charges()
        if st.get("cards", 0) >= cap:
            return
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
        return c.dist <= 30

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
        return c.dist <= c.rng("AbilityCastRange") + c.me.skill.engage_margin + LIFT_APPROACH

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.15

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        d = c.dur("AbilityDuration")
        c.debuff("stun", 1, d, delay=delay)
        c.spirit_hit(c.val("Damage"), delay=delay + d)
