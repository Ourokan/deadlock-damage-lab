"""Lady Geist (hero_ghost).

Assumptions:
- Health costs: SelfDamagePct is read as a % of the ability's damage (Essence Bomb 30%, Malice 9% per shard),
  taken as spirit damage mitigated by Geist's own spirit resist, never lethal. (Doubt: the game may use % of
  current health.)
- Essence Bomb: lands after ArmingDuration at spirit_accuracy. T3 puddle deals BloodSpillDPSPercent of the
  bomb damage per second; the target stands in it PUDDLE_UPTIME of BloodSpillDuration.
- Life Drain: tether always holds (12-15 m duel range < MaxRange); drains every TickRate and heals Geist for
  LifeDrainHealthMult% of the damage dealt. Geist keeps shooting. T3 charges can't stack tethers on one
  target: a new tether is only cast once the previous one ended.
- Malice: shards fan out over SpreadAngleDegrees; a shard lands if it falls within HERO_WIDTH at the duel
  distance (times spirit_accuracy). Each shard that lands deals HealthToDamage and adds one stack (max MaxStacks) of
  VulnerabilityPerStack% damage taken (from Geist; 1v1 so applied as damage_taken_amp); recasting refreshes.
- Soul Exchange: swaps health fractions. Geist walks up to SWAP_APPROACH m beyond cast range + engage margin to
  reach the target (the 5.5 m range is shorter than the duel distance; movement is not modeled). The enemy can't drop below EnemyMinHealthPct; the health loss is
  recorded as pure damage. Cast only when Geist is at least SWAP_MIN_GAIN lower (fraction) than the target. Geist's
  side of the swap is her gate health (Fighter.self_gate_frac: short by her real entry deficit and the damage the real
  fight's other enemies add, Mechanics.entry_gate / gate_assist): real Geists swap at ~25% health on a ~90% target.
  With Mechanics.swap_full the swap lands whole on SWAP_LAND of casts (no landing factor: real swaps take ~half the
  target's max health, the factor had cut that to ~0.2). With Mechanics.swap_gap each fight's swap waits for a gap drawn
  from the real swaps' gaps (SWAP_GAPS, median 0.6) instead of SWAP_MIN_GAIN. First cast held to a real first cast time (Mechanics.execute_timing, data/execute_timing.json; None: not cast in
  this fight), then the gap gate.
"""
import math

from deadsim.abilities import AbilityImpl, register

PUDDLE_UPTIME = 0.5
SWAP_MIN_GAIN = 0.3
SWAP_APPROACH = 10.0    # m Geist walks in to reach Soul Exchange's 5.5 m cast range (she keeps shooting meanwhile)
SWAP_LAND = 0.93       # Mechanics.swap_full: real Soul Exchange hits per cast (scripts/mechanics/swap_real.py)
# Mechanics.swap_gap: the health gap (target - Geist) a real swap went out at, 20 quantiles (scripts/mechanics/swap_real.py)
SWAP_GAPS = (0.09, 0.17, 0.25, 0.34, 0.44, 0.47, 0.5, 0.52, 0.55, 0.59, 0.63, 0.65, 0.67, 0.7, 0.74, 0.76, 0.79, 0.82,
             0.87, 0.95)
HERO_WIDTH = 1.5        # m, hittable width of a hero for Malice's shard fan


@register("ability_blood_bomb")
class EssenceBomb(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(25 + c.me.skill.engage_margin)

    def cast(self, c):
        dmg = c.val("Damage")
        c.self_damage(dmg * c.raw("SelfDamagePct") / 100, kind="spirit")
        arm = c.raw("ArmingDuration", 0.65)
        c.spirit_hit(dmg, delay=arm)
        if c.tier >= 3:
            acc = c.me.skill.spirit_accuracy
            c.dot(dmg * c.raw("BloodSpillDPSPercent") / 100, c.dur("BloodSpillDuration") * PUDDLE_UPTIME,
                  delay=arm, hit_chance=acc, tag=("geist_puddle", c.now))


@register("ability_life_drain")
class LifeDrain(AbilityImpl):
    kind = "target"
    range_props = ("AbilityCastRange",)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        tick = c.raw("TickRate", 0.1)
        n = max(1, int(round(c.dur("AbilityDuration") / tick)))
        token = object()
        c.state["tether"] = token
        c.state["until"] = c.now + delay + n * tick
        c.after(delay + tick, self.tick, c, n, token)

    def should_cast(self, c):
        return self.in_range(c) and c.now >= c.state.get("until", -1)   # one tether per target

    def tick(self, c, n, token):
        me, foe = c.me, c.foe
        if c.state.get("tether") is not token:
            return
        p = c.p_in(c.rng("MaxRange"))   # drains the share of the time the target is in range (breaks only at p = 0)
        if n <= 0 or not me.alive or not foe.alive or me.mods.active("stun") or p <= 0:
            return
        tick = c.raw("TickRate", 0.1)
        dealt = c.engine.damage(me, foe, c.val("LifeDrainPerSecond") * tick * p, "spirit", self.s.ab.name,
                                is_ability=True, ability=self.s, is_dot=True)
        if dealt:
            c.heal(dealt * c.raw("LifeDrainHealthMult", 100) / 100)
        c.after(tick, self.tick, c, n - 1, token)


@register("ability_blood_shards")
class Malice(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(25 + c.me.skill.engage_margin)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay + c.raw("AbilityPostCastDuration"))
        shards = int(c.raw("NumBloodShards"))
        dmg = c.val("HealthToDamage")
        c.self_damage(dmg * shards * c.raw("SelfDamagePct") / 100, kind="spirit")
        spread = 2 * max(1.0, c.dist) * math.tan(math.radians(c.raw("SpreadAngleDegrees") / 2))
        frac = min(1.0, HERO_WIDTH / spread) if spread > 0 else 1.0
        landed = c.me.acc("malice").take(c.me.skill.spirit_accuracy * frac, shards)
        if not landed:
            return
        c.after(delay, self.land, c, landed, dmg)

    def land(self, c, landed, dmg):
        st = c.state
        if c.now > st.get("until", -1):
            st["stacks"] = 0
        d = c.dur("DebuffDuration")
        st["until"] = c.now + d
        for _ in range(landed):
            st["stacks"] = min(int(c.raw("MaxStacks", 5)), st.get("stacks", 0) + 1)
            c.debuff("damage_taken_amp", st["stacks"] * c.raw("VulnerabilityPerStack") / 100, d, tag="malice")
            c.spirit_hit(dmg, hit_chance=1.0)


@register("ability_health_swap")
class SoulExchange(AbilityImpl):
    kind = "target"
    range_props = ("AbilityCastRange",)

    def in_range(self, c):
        return c.within(c.rng("AbilityCastRange") + SWAP_APPROACH)

    def draw_plan(self, c, u):
        """Mechanics.execute_timing: the first cast's hold from draw u (mechanics.execute_plans)."""
        from deadsim.mechanics import execute_timing_data
        q = execute_timing_data()["soul_exchange"]["holds"]
        h = q[min(len(q) - 1, int(u * len(q)))]
        self.s.held_until = c.now + (math.inf if h is None else h)
        if getattr(c.engine.mech, "swap_gap", False):
            # Mechanics.swap_gap: the gap this fight's swap waits for, on a draw independent of the hold's
            self.s.swap_gap = SWAP_GAPS[min(len(SWAP_GAPS) - 1, int(math.modf(u * 7919.0)[0] * len(SWAP_GAPS)))]

    def should_cast(self, c):
        gap = getattr(self.s, "swap_gap", None)
        need = max(SWAP_MIN_GAIN if gap is None else gap, c.raw("MinDiffToCast"))
        return self.in_range(c) and c.foe.hp_frac - c.me.self_gate_frac >= need

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay + c.raw("AbilityDuration"))
        c.after(delay, self.swap, c)

    def swap(self, c):
        me, foe = c.me, c.foe
        if not me.alive or not foe.alive:
            return
        whole = getattr(c.engine.mech, "swap_full", False)
        if whole and not me.acc("swap").take(SWAP_LAND):
            return   # missed (out of reach when it went off)
        mf, ff = me.self_gate_frac, foe.hp_frac
        new_foe = max(mf, c.raw("EnemyMinHealthPct", 30) / 100) * foe.max_hp
        loss = foe.hp - new_foe
        if loss > 0:
            c.engine.damage(me, foe, loss, "pure", self.s.ab.name, ignore_resist=True, is_ability=True,
                            ability=self.s, is_ult=True, procs=False, nonlethal=True, landed=whole)
        me.hp = max(me.hp, ff * me.max_hp)
        if c.tier >= 2:
            c.debuff("silence", 1, c.dur("SilenceDuration"))
        if c.tier >= 3:
            d = c.dur("SelfBuffDuration")
            c.buff("spirit_power", c.raw("BonusSpirit"), d)
            c.buff("fire_rate", c.raw("BonusFireRate") / 100, d)
            c.buff("spirit_resist", c.raw("TechResist") / 100, d)
