"""Rat King (hero_ratking).

Assumptions:
- EBaseWeaponDamageIncrease scaling (Scrap Grenade, Rule Ratannia): value * (1 + k * weapon damage %) via c.val.
- Scrap Grenade: bullet damage (gets bullet resist and procs). Detonations go off at FirstBounceDetonateTimer, then
  every AdditionalBounceDetonateTimer. T3's extra detonation is the big final one (BigExplosionDamage +300, weapon-scaled x1.0)
  after FinalBounceDetonateTimer. Each detonation
  lands at spirit_accuracy. The slow is ignored.
- Rat Swarm: skillshot. RatsAttached rats (+RAT_T2_EXTRA at T2, max MaxRats) bite n / BiteInterval times per
  second for AbilityDuration * RAT_UPTIME (the target dashes some off). Each bite deals DamagePerBite spirit and
  stacks ArmorReductionPerBite bullet resist reduction (modeled as bullet shred) for DebuffDuration. The base -1%
  per bite exists only in raw/items.json (BASE_SHRED_PER_BITE).
- Royal Pestments: barrier of MaxHealthPct% max health for AbilityDuration, cast once Rat King has lost over 5%
  health. While it holds, enemy gun damage has a ReturnFireChance% chance to be deflected. Expected value: that
  share of the bullet damage is reflected back as bullet damage and given back to the barrier. T3: hits over
  MaxDamagePerHit are capped (the excess is refunded). The note that the barrier ignores resists is not modeled.
- Rule, Ratannia!: Rat King charges for AbilityCastDelay (gun locked), then the banner lands after TossDuration
  for Damage (bullet, guess) to a target within Radius. Rat King then gets AllyDamageReduction% damage reduction
  (bullet + spirit resist) for FlagDuration while he stays near the banner. The enemy slow is ignored.
"""
from deadsim.abilities import AbilityImpl, register

RAT_T2_EXTRA = 1      # extra rats attached at T2 ("Increased Swarm Size"), guess
RAT_UPTIME = 0.75     # share of AbilityDuration the rats stay attached before dashes shake them off
BASE_SHRED_PER_BITE = 1.0   # % bullet resist per bite before T3 (raw/items.json ArmorReductionPerBite; abilities.json drops it)
PESTMENTS_HP_TRIGGER = 0.95


def big_explosion(c):
    """BigExplosionDamage scales with weapon damage (raw/items.json: EBaseWeaponDamageIncrease, +1.0 from T3), but
    abilities.json lacks the property, so c.val would read the T3 EAddToScale as spirit scaling."""
    return c.raw("BigExplosionDamage") * (1.0 + c.scale("BigExplosionDamage") * (c.me.st.weapon_pct + c.me.stat("weapon_pct")))


@register("ability_ratking_scrap_grenade")
class ScrapGrenade(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.dist <= 20.0 + c.me.skill.engage_margin   # thrown, no cast range in data

    def cast(self, c):
        acc = c.me.skill.spirit_accuracy
        t = c.raw("FirstBounceDetonateTimer", 0.8)
        dmg = c.val("DamagePerShrapnel") * acc
        n = int(c.raw("Detonations") - (1 if c.tier >= 3 else 0))
        for i in range(n):
            c.bullet_hit(dmg, delay=t)
            if i < n - 1:
                t += c.raw("AdditionalBounceDetonateTimer", 0.7)
        if c.tier >= 3:
            big = big_explosion(c) * acc
            c.bullet_hit(big, delay=t + c.raw("FinalBounceDetonateTimer", 1.5))


@register("ability_ratking_ratnibble")
class RatSwarm(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        n = c.raw("RatsAttached", 2) + (RAT_T2_EXTRA if c.tier >= 2 else 0)
        n = min(n, c.raw("MaxRats", 5))
        tick = c.raw("BiteInterval", 1.0) / n
        bites = int(c.dur("AbilityDuration") * RAT_UPTIME / tick)
        acc = c.me.skill.spirit_accuracy
        c.state["shred"] = (BASE_SHRED_PER_BITE + abs(c.raw("ArmorReductionPerBite"))) / 100 * acc
        c.state["dmg"] = c.val("DamagePerBite") * acc
        c.after(0.6, self.bite, c, bites, tick)   # ~0.6 s for the swarm to reach and leap on the target

    def bite(self, c, left, tick):
        if left <= 0 or not c.foe.alive or not c.me.alive:
            return
        c.spirit_hit(c.state["dmg"], hit_chance=1.0)
        if c.state["shred"]:
            c.debuff("bullet_shred", c.state["shred"], c.dur("DebuffDuration"), tag=object())
        c.after(tick, self.bite, c, left - 1, tick)


@register("ability_ratking_ratarmor")
class RoyalPestments(AbilityImpl):
    kind = "self"

    def start(self, c):
        c.state["entry"] = None

    def should_cast(self, c):
        return c.foe.alive and c.me.hp_frac < PESTMENTS_HP_TRIGGER

    def cast(self, c):
        c.barrier(c.raw("MaxHealthPct") / 100 * c.me.max_hp, c.dur("AbilityDuration"))
        c.state["entry"] = c.me.barriers[-1]

    def on_damage_taken(self, c, src, hit):
        e = c.state.get("entry")
        if not e or c.now >= e[1]:
            return
        held = e[0] > 0
        cap = c.raw("MaxDamagePerHit")
        if cap and hit.amount > cap:
            c.me.hp = min(c.me.max_hp, c.me.hp + hit.amount - cap)
        if held and hit.kind == "bullet" and hit.source == "gun" and hit.amount > 0:
            p = min(1.0, c.val("ReturnFireChance") / 100)
            e[0] += hit.amount * p
            c.engine.damage(c.me, c.foe, hit.raw * p * c.raw("BulletDamageReflectedPct", 100) / 100, "bullet",
                            self.s.ab.name, is_ability=True, ability=self.s, procs=False)


@register("ability_ratking_standard_bearer")
class RuleRatannia(AbilityImpl):
    kind = "aoe"
    range_props = ("Radius",)

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.1

    def cast(self, c):
        charge = c.raw("AbilityCastDelay")
        c.lock_gun(charge)
        c.bullet_hit(c.val("Damage"), delay=charge + c.raw("TossDuration"))
        c.after(charge, self.plant, c)

    def plant(self, c):
        if not c.me.alive:
            return
        red = c.raw("AllyDamageReduction") / 100
        d = c.dur("FlagDuration")
        c.buff("bullet_resist", red, d, tag="ratannia_b")
        c.buff("spirit_resist", red, d, tag="ratannia_s")
