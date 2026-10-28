"""Paradox (hero_chrono).

Assumptions:
- Pulse Grenade: lands at spirit_accuracy; one pulse at landing, then every PulseInterval during AbilityDuration.
  Each pulse deals PulseDamage and adds a stack of DamageAmplificationPerStack% damage taken (from Paradox; 1v1 so
  damage_taken_amp), DebuffDuration. Without Mechanics.pulse_hits the time-slowed target stays inside for every
  pulse; with it pulse i deals and stacks x the real share of landed throws whose main victim takes more than i
  pulses (~2 of 5 in replays, data/pulse_hits.json), and the amp on Paradox's other hits is booked under Pulse
  Grenade as the game does (engine.BOOKED_AMPS).
- Time Wall: +FriendlyBulletDamageBonus% weapon damage for bullets Paradox shoots through it, scaled by
  TIMEWALL_SHOOT_THROUGH. Shooting through it for its whole duration gave the sim's Paradox hit 1.6x the real one
  (others 0.8-1.4x) and a gun share of 0.34 vs 0.24 real. In replays, only ~3% more of Paradox's gun hits on heroes
  land 1.3x+ above his local median than for heroes without such a buff (9.3% vs 5.8-7.0% for Wraith/Haze), so the
  +30-65% bonus reaches few hits. Blocking enemy bullets/projectiles is NOT modeled (no engine hook for a partial
  block). T2 silence lands on the target (wall dropped on them).
- Kinetic Carbine: spirit damage = MaxBonusBulletDamage + (EWeaponPower scale)% of the weapon damage, read as
  5 + 125 x (bullet damage / level-1 bullet damage) x (1 + weapon bonus), T3 scale 180. In replays (70 Phantom+
  matches) a Carbine hit is 10-17x Paradox's gun hit at every stage of the match (96 at 0-5 min, ~470 at 20-30 min):
  it grows with the per-level bullet damage too. Without that growth the late hit was ~0.55x real and the
  landing factor (capped at 1.5) could not make it up. Charged for MaxChargeDuration x CARBINE_CHARGE seconds
  (no shooting): in replays the gap from Paradox's previous gun shot to a mid-fight Carbine hit is mostly 2.5-6 s.
  Always a full charge, landing at spirit_accuracy; HeadshotBonus% at the caster's headshot rate. Time-stop = stun for MaxSlowDuration. The hit procs Mystic Shot like a gun hit (replays:
  73% of Paradox's Mystic Shot procs on heroes land with a Kinetic Carbine hit). Real hits are ~0.6x this
  formula and come ~2x as often per gun damage (scripts/mechanics/carbine_replays.py): 58% of real Carbine hits are
  pokes outside any fight, at full charge (median 21.5x his gun hit, the formula's size), and the hits in fights are
  CARBINE_FIGHT_HIT of that (13.7x, openers alike; scripts/fight_length/ability_pokes.py). So a cast in the duel
  deals CARBINE_FIGHT_HIT x the formula and the pokes beside it (Mechanics.pokes, fight.add_pokes) the full hit
  (validation/README.md "Carbine pokes").
- Paradoxical Swap: the projectile lands at spirit_accuracy; SwapDamage (+T3 MaxHealthDamage% of max health)
  on arrival. Both heroes are in transit for MinSwapTime: Paradox can't shoot, the target is stunned. T1 barrier
  = CombatBarrier (200 + 1.5 x spirit power).
"""
from deadsim.abilities import AbilityImpl, register
from deadsim.mechanics import pulse_survival

CARBINE_FIGHT_HIT = 0.64   # a Carbine hit in a fight / a poke's (real medians 13.7x / 21.5x his gun hit, see above)
CARBINE_CHARGE = 1.0   # share of MaxChargeDuration spent charging (replays, see above)
TIMEWALL_SHOOT_THROUGH = 0.1   # share of the wall's uptime Paradox's hits get the bonus (replays, see above)


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
        surv = pulse_survival(c.me)
        for i in range(n):
            w = 1.0 if surv is None else surv[min(i, len(surv) - 1)]
            if w > 0:
                c.after(delay + 0.3 + i * interval, self.pulse, c, w, surv is not None)

    def pulse(self, c, w=1.0, booked=False):
        if not c.me.alive or not c.foe.alive:
            return
        st = c.state
        d = c.dur("DebuffDuration")
        if c.now > st.get("until", -1):
            st["stacks"] = 0
        st["stacks"] = st.get("stacks", 0) + w
        st["until"] = c.now + d
        c.spirit_hit(c.val("PulseDamage"), hit_chance=w)
        tag = (self.s.ab.class_name, "damage_taken_amp", c.me.name) if booked else "pulse"
        c.debuff("damage_taken_amp", st["stacks"] * c.raw("DamageAmplificationPerStack") / 100, d, tag=tag)


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
        c.after(delay, c.buff, "weapon_pct", c.raw("FriendlyBulletDamageBonus") / 100 * TIMEWALL_SHOOT_THROUGH, d,
                "timewall")
        c.after(delay, c.buff, "weapon_pct_timewall", 1, d, "timewall_marker")
        if c.tier >= 2:
            c.debuff("silence", 1, c.dur("DebuffDuration"), delay=delay)


@register("citadel_ability_chrono_kinetic_carbine")
class KineticCarbine(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(40)

    def cast(self, c):
        charge = c.raw("MaxChargeDuration", 2.5) * CARBINE_CHARGE
        c.lock_gun(charge)
        c.after(charge, self.shoot, c)

    def shoot(self, c):
        if not c.me.alive or not c.foe.alive:
            return
        st = c.me.st
        growth = st.bullet_damage / max(1e-6, st.gun_charge * st.hero.weapon.get("bullet_damage", 1.0))
        dmg = c.raw("MaxBonusBulletDamage") + c.scale("MaxBonusBulletDamage") * growth * (1 + c.me.weapon_pct())
        dmg *= 1 + c.me.skill.headshot * c.raw("HeadshotBonus") / 100
        if c.me.e.length and getattr(c.me.e.mech, "pokes", False) and not c.me.counters.get("poke"):
            dmg *= CARBINE_FIGHT_HIT
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
