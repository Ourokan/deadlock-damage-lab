"""McGinnis (hero_forge).

Assumptions:
- Mini Turret: placed near the fight, it shoots the target for TurretLifetime at TurretDPS (x AttackSpeedMult;
  T3 +25%), with linear falloff to 0 between TurretAttackFalloffStart/End (fights are inside the start).
  The target doesn't kill turrets. Each charge is a separate turret. First shot after deploy + attack delay.
  TURRET_PACING (with Mechanics.fight_length and cast_timing, in fights with an rng or a fight phase): after each
  turret the next one waits a gap drawn from real Phantom+ fights for the game phase (data/turret_gaps.json,
  scripts/mechanics/turret_gaps.py) as well as for its charge. Casting every charge on sight dropped ~2.6 turrets by
  10 s into a fight against real 0.9 (lane) to 1.1 (late): real players spread them, median ~9 s apart.
- Medicinal Specter: McGinnis stands in it; +ExternalBonusHealthRegen regen (spirit-scaled healing) for the
  duration; T3 adds MaxHealthRegenPct of max health per second and +SpiritResist. Cast only below 70% health.
- Spectral Wall: erupted on the target WALL_ERUPT_DELAY after cast, landing at spirit_accuracy, dealing
  Damage. T1 +BonusDamagePercent damage taken for DebuffDuration; T3 adds CreateTurrets turrets (Mini Turret
  stats) for TurretLifeTime, booked as "Mini Turret (wall)" since the game credits turret damage to Mini Turret. Slow ignored.
- With deadsim.mechanics summons on, each turret has TurretBaseHealth (+ boons) health and TechResist spirit resist,
  the enemy can shoot it (targeting fitted to replays, data/summon_targeting.json), and its damage stops when it dies.
- Heavy Barrage: McGinnis can't shoot while barraging; rockets fire at GrenadesPerSecond for AbilityDuration and
  ROCKET_HIT_FRAC of them hit a moving target (x spirit_accuracy). A stun ends the barrage.
"""
import json
import math
import os
import zlib

from deadsim.abilities import AbilityImpl, register
from deadsim.mechanics import LENGTH_PHASES, add_summon

WALL_ERUPT_DELAY = 0.6
ROCKET_HIT_FRAC = 0.6
TURRET_PACING = True
_GAPS = None


def turret_gaps(souls):
    """Equal-probability real gaps (s) between Mini Turrets placed in a fight at net worth souls, None = no next one."""
    global _GAPS
    if _GAPS is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "..", "data", "turret_gaps.json")) as fh:
            _GAPS = json.load(fh)["phases"]
    ph = next((n for hi, n in LENGTH_PHASES if souls < hi), "late")
    return _GAPS[ph]["gaps"]


def turret_summon(c, tc, life, delay, name="Mini Turret"):
    """The turret as a target the enemy can shoot (None unless deadsim.mechanics summons are on)."""
    return add_summon(c.me, name, tc.val("TurretBaseHealth"), spirit_resist=tc.raw("TechResist") / 100,
                      life=life, delay=delay, kind="mcginnis_turret")


def turret_dps(tc):
    """DPS of one Mini Turret on the target, from the Mini Turret ability's context."""
    dps = tc.val("TurretDPS") * (1 + (tc.raw("AttackSpeedMult", 100) - 100) / 100)
    s, e = tc.rng("TurretAttackFalloffStart"), tc.rng("TurretAttackFalloffEnd")
    return dps * tc.engine.spread_mean(lambda x: 1.0 if x <= s else max(0.0, 1 - (x - s) / max(0.1, e - s)))


@register("citadel_ability_shieldedsentry")
class MiniTurret(AbilityImpl):
    kind = "aoe"
    range_props = ("TurretAttackRange",)

    def should_cast(self, c):
        return c.now >= c.state.get("next_at", -math.inf) and super().should_cast(c)

    def pace(self, c):
        """TURRET_PACING: hold the next turret of this fight by a real gap (see the module notes)."""
        e, f = c.engine, c.me
        if not TURRET_PACING or not e.length or e.mech is None or not getattr(e.mech, "cast_timing", False):
            return
        phase = f.skill.fight_phase
        if phase is None and e.rng is None:
            return
        k = c.state["placed"] = c.state.get("placed", 0) + 1
        if phase is not None:
            u = (phase + zlib.crc32(f"turret{k}|{f.name}".encode()) / 2 ** 32) % 1.0
        else:
            u = e.rng.random()
        q = turret_gaps(f.st.souls)
        h = q[min(len(q) - 1, int(u * len(q)))]
        c.state["next_at"] = math.inf if h is None else c.now + h

    def cast(self, c):
        self.pace(c)
        start = c.raw("AbilityCastDelay") + c.raw("TurretDeployTime") + c.raw("TurretAttackDelay")
        c.lock_gun(c.raw("AbilityCastDelay"))
        life = c.dur("TurretLifetime")
        s = turret_summon(c, c, life, start)
        c.dot(turret_dps(c), life, tick=c.raw("TickRate", 0.5), delay=start, tag=("turret", c.now), guard=s)


@register("citadel_ability_mobile_resupply")
class MedicinalSpecter(AbilityImpl):
    kind = "self"

    def should_cast(self, c):
        return c.me.hp_frac < 0.7

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        d = c.dur("AbilityDuration")
        regen = c.val("ExternalBonusHealthRegen")
        if c.tier >= 3:
            regen += c.me.max_hp * c.raw("MaxHealthRegenPct") / 100
            c.buff("spirit_resist", c.raw("SpiritResist") / 100, d + delay)
        c.buff("regen", regen, d + delay)


@register("citadel_ability_fissure_wall")
class SpectralWall(AbilityImpl):
    kind = "skillshot"
    range_props = ("AbilityCastRange",)

    def cast(self, c):
        c.lock_gun(0.2)
        if not c.me.acc("mcg_wall").take(c.me.skill.spirit_accuracy):
            return
        c.spirit_hit(c.val("Damage"), delay=WALL_ERUPT_DELAY, hit_chance=1.0)
        if c.tier >= 1:
            c.debuff("damage_taken_amp", c.raw("BonusDamagePercent") / 100, c.dur("DebuffDuration"),
                     delay=WALL_ERUPT_DELAY)
        if c.tier >= 3:
            tc = next((a.ctx for a in c.me.abilities if a.ab.class_name == "citadel_ability_shieldedsentry"), None)
            if tc is not None:
                for i in range(int(c.raw("CreateTurrets"))):
                    s = turret_summon(c, tc, c.dur("TurretLifeTime"), WALL_ERUPT_DELAY, "Mini Turret (wall)")
                    c.dot(turret_dps(tc), c.dur("TurretLifeTime"), tick=0.5, delay=WALL_ERUPT_DELAY,
                          name="Mini Turret (wall)", tag=("wall_turret", c.now, i), guard=s)


@register("citadel_ability_rocket_barrage")
class HeavyBarrage(AbilityImpl):
    kind = "skillshot"
    range_props = ("AbilityCastRange",)

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.25

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        d = c.dur("AbilityDuration")
        c.lock_gun(delay + d)
        c.state["end"] = c.now + delay + d
        c.after(delay + c.raw("IntervalRampUpStart", 0.35), self.rocket, c)

    def rocket(self, c):
        me, foe = c.me, c.foe
        if not me.alive or not foe.alive or c.now > c.state["end"] + 1e-9:
            return
        if me.mods.active("stun"):
            me.gun_locked_until = c.now
            return
        land = me.acc("mcg_rockets").take(ROCKET_HIT_FRAC * me.skill.spirit_accuracy)
        if land:
            c.spirit_hit(c.val("DamagePerRocket") * land, hit_chance=1.0)
        c.after(1.0 / max(0.1, c.raw("GrenadesPerSecond", 6.0)), self.rocket, c)
