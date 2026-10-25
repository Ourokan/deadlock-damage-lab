"""Baba (hero_baba).

Assumptions:
- Threadsap: skillshot within AbilityCastRange; the thread bursts ExplodeTime after the cast for Damage and steals
  TechPowerGain spirit (stacking up to MaxStacks) for DebuffDuration: the target loses it, Baba gains
  StolenSpiritEffectiveness % of it. While Baba holds stolen spirit every gun bullet (pellet) that hits deals
  MagicDamagePerBullet spirit damage, booked as the game does under "Threadsap (gun)" (the API's damage matrix
  lists ability_baba_bubbling_brew_gun_damage as its own Threadsap source). T3 pull is movement only.
- Granny Long Legs: a self buff for AbilityDuration: StatusResistancePercent status resist and MeleeResist melee
  resist (T3 adds to both and MeleeLifesteal melee lifesteal). Each heavy melee landed meanwhile is a ground pound
  that also deals HeavyMeleeSpiritDamage; light kicks only knock back. Move speed / jumps are movement only.
  Cast on sight: she runs in on it (the bench is a brawling stance); its melee lands at her fitted melee rate.
- Baba's Brew: Baba throws the scalding brew (the burn: DamagePerSecond for BurnDuration and SpiritResistReduction
  spirit shred), the damaging one of the three. It is brewed for FireLockTime before the throw, except the first,
  assumed brewed before the fight. T3 BrewEffectiveness scales the burn and the shred
  (the API's EMultiplyBase upgrade, already in raw()). Barrier and silence brews
  are not modeled.
- Feed The Birds: cast within AbilityCastRange; Baba channels for TimeToMaxStacks (gun stopped, full bread count:
  the landing factor fits real partial counts), then after the mean BarrageStart delay the barrage deals
  BarrageMaxDamage and hexes the target (can't shoot or cast: stun) for HexDuration. The slow is skipped.
"""
from deadsim.abilities import AbilityImpl, register

STOLEN_KEY = "baba_stolen_until"


@register("ability_baba_bubbling_brew")
class Threadsap(AbilityImpl):
    kind = "skillshot"

    def start(self, c):
        c.state.update(stacks=0.0, until=-1.0)
        c.me.counters[STOLEN_KEY] = -1.0

    def cast(self, c):
        c.lock_gun(c.raw("AbilityCastDelay"))
        c.after(c.raw("ExplodeTime", 0.9), self.burst, c)

    def burst(self, c):
        if not (c.me.alive and c.foe.alive):
            return
        acc = c.me.skill.spirit_accuracy
        c.spirit_hit(c.val("Damage"))
        st = c.state
        if c.now >= st["until"]:
            st["stacks"] = 0.0
        st["stacks"] = min(c.val("MaxStacks"), st["stacks"] + c.val("TechPowerGain") * acc)
        d = c.dur("DebuffDuration")
        st["until"] = c.now + d
        c.debuff("spirit_power", -st["stacks"], d, tag="threadsap_stolen")
        c.buff("spirit_power", st["stacks"] * c.raw("StolenSpiritEffectiveness", 100) / 100, d, tag="threadsap_gain")
        c.me.counters[STOLEN_KEY] = c.now + d

    def on_damage_dealt(self, c, target, hit):
        if hit.source != "gun" or not hit.hits or c.now >= c.me.counters.get(STOLEN_KEY, -1.0):
            return
        c.engine.damage(c.me, target, c.val("MagicDamagePerBullet") * hit.hits, "spirit", "Threadsap (gun)",
                        is_ability=True, ability=self.s)


@register("ability_baba_bench_run")
class GrannyLongLegs(AbilityImpl):
    kind = "self"

    def start(self, c):
        c.state["until"] = -1.0

    def in_range(self, c):
        return True   # she runs in on the bench (BonusMoveSpeed); its melee lands at Baba's fitted melee rate

    def cast(self, c):
        d = c.dur("AbilityDuration")
        c.state["until"] = c.now + d
        c.buff("status_resist", c.raw("StatusResistancePercent") / 100, d)
        c.buff("melee_resist", c.raw("MeleeResist") / 100, d)

    def on_damage_dealt(self, c, target, hit):
        if hit.source != "melee" or c.now >= c.state["until"]:
            return
        if c.raw("MeleeLifesteal"):   # the engine has no melee lifesteal stat: healed here
            c.me.heal(hit.amount * c.raw("MeleeLifesteal") / 100, self.s.ab.name, "lifesteal")
        if not c.me.counters.get("melee_heavy"):
            return
        w = c.me.counters.get("melee_weight", 1.0)
        c.engine.damage(c.me, target, c.val("HeavyMeleeSpiritDamage") * w, "spirit", self.s.ab.name,
                        is_ability=True, ability=self.s)


@register("ability_baba_hexing_brew")
class BabasBrew(AbilityImpl):
    kind = "skillshot"

    def start(self, c):
        c.state["thrown"] = False

    def cast(self, c):
        brew = c.raw("FireLockTime", 4.5) if c.state.get("thrown") else 0.0
        c.state["thrown"] = True
        throw = brew + c.raw("AbilityChannelTime")
        c.lock_gun(c.raw("AbilityChannelTime"))
        acc = c.me.skill.spirit_accuracy
        d = c.dur("BurnDuration")
        c.dot(c.val("DamagePerSecond"), d, delay=throw, hit_chance=acc)
        c.debuff("spirit_shred", abs(c.raw("SpiritResistReduction")) / 100 * acc, d, delay=throw)


@register("ability_baba_ultimate_2")
class FeedTheBirds(AbilityImpl):
    kind = "target"

    def cast(self, c):
        ch = c.raw("AbilityCastDelay") + c.raw("TimeToMaxStacks", 3.5)
        c.lock_gun(ch + c.raw("AbilityPostCastDuration"))
        land = ch + (c.raw("BarrageStartDelayMin") + c.raw("BarrageStartDelayMax")) / 2
        c.spirit_hit(c.val("BarrageMaxDamage"), delay=land)
        c.debuff("stun", 1, c.raw("HexDuration"), delay=land)
