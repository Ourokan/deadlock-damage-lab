"""Paradox (hero_chrono).

Assumptions:
- Pulse Grenade: lands at spirit_accuracy; the time-slowed target stays inside for every pulse
  (one at landing, then every PulseInterval during AbilityDuration). Each pulse deals PulseDamage and adds a
  stack of DamageAmplificationPerStack% damage taken (from Paradox; 1v1 so damage_taken_amp), DebuffDuration.
- Time Wall: placed between the fighters, Paradox shoots through it for its whole duration: +FriendlyBullet-
  DamageBonus% weapon damage. Blocking enemy bullets/projectiles is NOT modeled (no engine hook for a partial
  block). T2 silence lands on the target (wall dropped on them).
- Kinetic Carbine: spirit damage = MaxBonusBulletDamage + (EWeaponPower scale)% of the weapon damage, read as
  5 + 125 x (1 + weapon bonus), T3 scale 180 (low confidence: the data's EWeaponPower meaning is unclear). Charged for
  CARBINE_CHARGE seconds (no shooting), always a full charge, landing at spirit_accuracy; HeadshotBonus% at
  the caster's headshot rate. Time-stop = stun for MaxSlowDuration. The hit procs Mystic Shot like a gun hit (replays:
  73% of Paradox's Mystic Shot procs on heroes land with a Kinetic Carbine hit).
- Paradoxical Swap: the projectile lands at spirit_accuracy; SwapDamage (+T3 MaxHealthDamage% of max health)
  on arrival. Both heroes are in transit for MinSwapTime: Paradox can't shoot, the target is stunned. T1 barrier
  = CombatBarrier (200 + 1.5 x spirit power).
"""
from deadsim.abilities import AbilityImpl, register

CARBINE_CHARGE = 1.0


@register("citadel_ability_chrono_pulse_grenade")
class PulseGrenade(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(25 + c.me.skill.engage_margin)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        if not c.me.acc("pulse_land").take(c.me.skill.spirit_accuracy):
            return
        interval = c.raw("PulseInterval", 0.8)
        n = 1 + int(c.dur("AbilityDuration") / interval + 1e-6)
        for i in range(n):
            c.after(delay + 0.3 + i * interval, self.pulse, c)

    def pulse(self, c):
        if not c.me.alive or not c.foe.alive:
            return
        st = c.state
        d = c.dur("DebuffDuration")
        if c.now > st.get("until", -1):
            st["stacks"] = 0
        st["stacks"] = st.get("stacks", 0) + 1
        st["until"] = c.now + d
        c.spirit_hit(c.val("PulseDamage"), hit_chance=1.0)
        c.debuff("damage_taken_amp", st["stacks"] * c.raw("DamageAmplificationPerStack") / 100, d, tag="pulse")


@register("citadel_ability_chrono_time_wall")
class TimeWall(AbilityImpl):
    kind = "aoe"

    def in_range(self, c):
        return c.reach(30)

    def should_cast(self, c):
        return self.in_range(c) and not c.me.mods.active("weapon_pct_timewall")

    def cast(self, c):
        delay = c.raw("AbilityCastDelay") + c.raw("TimeWallFormationTime")
        c.lock_gun(c.raw("AbilityCastDelay"))
        d = c.dur("AbilityDuration")
        c.after(delay, c.buff, "weapon_pct", c.raw("FriendlyBulletDamageBonus") / 100, d, "timewall")
        c.after(delay, c.buff, "weapon_pct_timewall", 1, d, "timewall_marker")
        if c.tier >= 2:
            c.debuff("silence", 1, c.dur("DebuffDuration"), delay=delay)


@register("citadel_ability_chrono_kinetic_carbine")
class KineticCarbine(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(40)

    def cast(self, c):
        c.lock_gun(CARBINE_CHARGE)
        c.after(CARBINE_CHARGE, self.shoot, c)

    def shoot(self, c):
        if not c.me.alive or not c.foe.alive:
            return
        dmg = c.raw("MaxBonusBulletDamage") + c.scale("MaxBonusBulletDamage") * (1 + c.me.weapon_pct())
        dmg *= 1 + c.me.skill.headshot * c.raw("HeadshotBonus") / 100
        if c.me.acc("carbine").take(c.me.skill.spirit_accuracy):
            c.spirit_hit(dmg, hit_chance=1.0, weapon_proc=True)
            c.debuff("stun", 1, c.dur("MaxSlowDuration"))


@register("citadel_ability_chrono_swap")
class ParadoxicalSwap(AbilityImpl):
    kind = "skillshot"
    range_props = ("AbilityCastRange",)

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.15

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        t = c.raw("MinSwapTime", 0.6)
        c.lock_gun(delay + t)
        if c.tier >= 1:
            c.barrier(c.val("CombatBarrier"), c.dur("BarrierDuration"))
        if not c.me.acc("swap_land").take(c.me.skill.spirit_accuracy):
            return
        dmg = c.val("SwapDamage") + c.foe.max_hp * c.raw("MaxHealthDamage") / 100
        c.debuff("stun", 1, t, delay=delay)
        c.spirit_hit(dmg, delay=delay + t, hit_chance=1.0)
