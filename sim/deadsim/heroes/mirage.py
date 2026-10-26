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
  when the pending damage would kill); otherwise they pop on expiry. T3 stuns on max marks. A first cast held to
  real cast timing (mechanics.cast_timing) pops the marks there are then.
  Gaps (MARK_GAPS): real Mirage often lands no gun hit on the target for a while (casting, reloading, out of sight),
  so after ~half his marks no new mark comes within VictimStackDuration and they pop on expiry, low-stack and early
  (data/djinn_gaps.json, scripts/mechanics/djinn_gaps.py). Fights that book damage over real fight lengths and have
  an rng or a fight phase draw, after each mark, whether the next one misses that window: then no gun hit marks
  until the marks have expired. Other fights (dummy page, deterministic) keep marking every hit.
- Traveler: a map teleport with no 1v1 combat effect except its upgrades, which are applied as if Mirage
  teleported in at fight start: T1 +BonusFireRate for MovementSpeedBonusDuration, T2 barrier
  CombatBarrier (400 + spirit scaling) for BARRIER_DURATION.
"""
import json
import os
import zlib

from deadsim.abilities import AbilityImpl, register

SCARAB_RANGE = 25.0          # m, scarab projectiles (no range in data)
RECAST_DELAY = 1.0           # s between the Dust Devil cast and its T3 recast
BARRIER_DURATION = 6.0       # s, combat barrier duration (not in data)
MARK_GAPS = True
GAPS_ROW = "all"             # data/djinn_gaps.json row (the split-half check uses "even" / "odd")
_gaps = None


def gap_chance(d):
    """Real P(no next Djinn's Mark within d s of a mark | the fight goes on), linear on the data's grid."""
    global _gaps
    if _gaps is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "..", "data", "djinn_gaps.json")) as fh:
            _gaps = json.load(fh)
    xs, ys = _gaps["duration_s"], _gaps[GAPS_ROW]
    if d <= xs[0]:
        return ys[0]
    for k in range(1, len(xs)):
        if d <= xs[k]:
            w = (d - xs[k - 1]) / (xs[k] - xs[k - 1])
            return ys[k - 1] + w * (ys[k] - ys[k - 1])
    return ys[-1]


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
        epoch = c.dot_track(("scarabs", c.state["n"]), c.now + delay + n * tick)
        c.after(delay + tick, self.tick, c, dps * tick, n, c.state["n"], epoch)

    def tick(self, c, amount, left, idx, epoch):
        f, e = c.me, c.foe
        if not (f.alive and e.alive) or not c.dot_live(epoch):
            return
        dealt = c.engine.damage(f, e, amount, "spirit", self.s.ab.name, is_ability=True, ability=self.s, is_dot=True)
        c.heal(dealt)
        if left > 1:
            c.after(0.5, self.tick, c, amount, left - 1, idx, epoch)


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
    # a held first cast pops the marks there are, from the first gun hit on (fit_cast_timing.py measures it with
    # PROBE_HELD; "first_hit": its probe waits for that hit, so it counts as on sight by PROBE_SIGHT_S)
    held_opens = "first_hit"

    def start(self, c):
        c.state.update(stacks=0, next_proc=0.0, expire=-1.0, gen=0, gap_until=-1.0, draws=0)

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
        if c.now < st["next_proc"] or c.now <= st["gap_until"] or not target.alive:
            return
        st["next_proc"] = c.now + c.raw("ProcCooldown") * self.cd_mult()
        st["stacks"] = min(int(c.raw("MaxStacks", 4)), st["stacks"] + 1)
        st["gen"] += 1
        d = c.dur("VictimStackDuration")
        st["expire"] = c.now + d
        c.after(d, self.expire, c, st["gen"])
        u = self.gap_draw(c)
        if u is not None and u < gap_chance(d):
            st["gap_until"] = st["expire"]   # no mark until these have expired and popped

    def gap_draw(self, c):
        """MARK_GAPS draw for the mark just applied: phase (one quasi-random value per mark index) or rng; None in
        fights that don't book real fight lengths or have neither."""
        f, e = c.me, c.engine
        if not MARK_GAPS or getattr(e, "length", None) is None:
            return None
        n = c.state["draws"] = c.state["draws"] + 1
        if f.skill.fight_phase is not None:
            return (f.skill.fight_phase + zlib.crc32(f"djinn_gap|{f.name}|{n}".encode()) / 2 ** 32) % 1.0
        if e.rng is not None:
            return e.rng.random()
        return None

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
        if self.s.held_opener():
            return True   # real Mirage's first pop comes at his real cast time, at whatever marks
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
