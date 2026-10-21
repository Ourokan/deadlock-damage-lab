"""Mirage (hero_mirage).

Assumptions:
- Fire Scarabs: each charge infests the target for StealDuration: DPS spirit damage, Mirage heals for the damage
  dealt, and the target deals OutgoingDamagePenaltyPercent less damage. Scarabs from separate charges stack
  (MaxStacks 100). T3 +0.13 spirit scaling comes from the data via c.val. Reach SCARAB_RANGE.
- Dust Devil: Mirage travels as the tornado (can't shoot) for cast range / TornadoSpeed, hits once for Damage,
  then gains WhirlwindEvasionChance evasion for WhirlwindDuration. The lift (0.2-0.5 s) and slow are movement
  and are skipped. T3 recast: a second tornado RECAST_DELAY later (T3 +0.6 spirit scaling via c.val).
- Djinn's Mark: every gun hit applies a mark if the per-target ProcCooldown is ready; each mark doubles the
  pending damage and refreshes VictimStackDuration. Mirage consumes the marks with the active at max stacks (or
  when the pending damage would kill); otherwise they pop on expiry. T3 stuns on max marks.
- Traveler: a map teleport with no 1v1 combat effect except its upgrades, which are applied as if Mirage
  teleported in at fight start: T1 +BonusFireRate for MovementSpeedBonusDuration, T2 barrier
  CombatBarrier (400 + spirit scaling) for BARRIER_DURATION.
"""
from deadsim.abilities import AbilityImpl, register

SCARAB_RANGE = 25.0          # m, scarab projectiles (no range in data)
RECAST_DELAY = 1.0           # s between the Dust Devil cast and its T3 recast
BARRIER_DURATION = 6.0       # s, combat barrier duration (not in data)


@register("mirage_fire_beetles")
class FireScarabs(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(SCARAB_RANGE)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        acc = c.me.skill.spirit_accuracy
        dps = c.val("DPS") * acc
        d = c.dur("StealDuration")
        c.debuff("outgoing_penalty", abs(c.raw("OutgoingDamagePenaltyPercent")) / 100 * acc, d, delay=delay)
        c.state["n"] = c.state.get("n", 0) + 1
        tick = 0.5
        n = max(1, int(round(d / tick)))
        c.after(delay + tick, self.tick, c, dps * tick, n, c.state["n"])

    def tick(self, c, amount, left, idx):
        f, e = c.me, c.foe
        if not (f.alive and e.alive):
            return
        dealt = c.engine.damage(f, e, amount, "spirit", self.s.ab.name, is_ability=True, ability=self.s, is_dot=True)
        c.heal(dealt)
        if left > 1:
            c.after(0.5, self.tick, c, amount, left - 1, idx)


@register("mirage_tornado")
class DustDevil(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        self.tornado(c)
        if c.tier >= 3 and c.raw("RecastWindow"):
            c.after(RECAST_DELAY + self.travel(c), self.tornado, c)

    def travel(self, c):
        return c.raw("AbilityCastDelay") + c.rng("AbilityCastRange", 20) / max(1.0, c.raw("TornadoSpeed", 24))

    def tornado(self, c):
        if not (c.me.alive and c.foe.alive):
            return
        t = self.travel(c)
        c.lock_gun(t)
        c.spirit_hit(c.val("Damage"), delay=min(t, c.raw("AbilityCastDelay") + c.dist / max(1.0, c.raw("TornadoSpeed", 24))))
        c.after(t, lambda: c.buff("evasion", c.raw("WhirlwindEvasionChance") / 100, c.dur("WhirlwindDuration"),
                                  tag="whirlwind"))


@register("mirage_sand_phantom")
class DjinnsMark(AbilityImpl):
    kind = "target"

    def start(self, c):
        c.state.update(stacks=0, next_proc=0.0, expire=-1.0, gen=0)

    def cd_mult(self):
        base = self.s.ctx.raw("AbilityCooldown")
        return self.s.cooldown() / base if base else 1.0

    def pending(self, c):
        n = c.state["stacks"]
        if n <= 0:
            return 0.0
        return c.val("ProcDamageBase") * c.raw("DMarkMultiplierPerStack", 2.0) ** (n - 1)

    def on_damage_dealt(self, c, target, hit):
        if hit.kind != "bullet" or hit.source != "gun" or not hit.hits:
            return
        st = c.state
        if c.now < st["next_proc"] or not target.alive:
            return
        st["next_proc"] = c.now + c.raw("ProcCooldown") * self.cd_mult()
        st["stacks"] = min(int(c.raw("MaxStacks", 4)), st["stacks"] + 1)
        st["gen"] += 1
        d = c.dur("VictimStackDuration")
        st["expire"] = c.now + d
        c.after(d, self.expire, c, st["gen"])

    def expire(self, c, gen):
        if c.state["gen"] == gen and c.state["stacks"] > 0:
            self.pop(c)

    def pop(self, c):
        st = c.state
        full = st["stacks"] >= int(c.raw("MaxStacks", 4))
        dmg = self.pending(c)
        st["stacks"] = 0
        st["gen"] += 1
        c.spirit_hit(dmg)
        if full and c.raw("StunDuration"):
            c.debuff("stun", 1, c.raw("StunDuration"))

    def should_cast(self, c):
        st = c.state
        if st["stacks"] <= 0:
            return False
        return st["stacks"] >= int(c.raw("MaxStacks", 4)) or self.pending(c) >= c.foe.hp

    def cast(self, c):
        self.pop(c)


@register("mirage_teleport")
class Traveler(AbilityImpl):
    kind = "self"

    def should_cast(self, c):
        return c.tier >= 1 and c.now < 0.5   # only matters as the fight opener

    def cast(self, c):
        if c.raw("BonusFireRate"):
            c.buff("fire_rate", c.raw("BonusFireRate") / 100, c.dur("MovementSpeedBonusDuration"), tag="traveler")
        if c.raw("CombatBarrier"):
            c.barrier(c.val("CombatBarrier"), BARRIER_DURATION)
