"""Solomon (hero_chessmaster). Released 2026-10-09: modeled from the tooltip text and data only.

The "Move" alt fire (ability_chessmaster_movechesspiece) moves the active piece. Assumptions:
- Setup Bishop: thrown at the target for ImpactDamage (skillshot). The bishop then stays for the whole fight and
  is not killed. Every MoveCooldown Solomon moves it through the target: Damage spirit at spirit_accuracy (each
  pass after the first takes -MultiHitPenaltyPercentage%), and the diagonal squares then deal DPS for
  SQUARE_EXPOSURE s per move, per piece (T2 +1 piece). T3: each square exposure adds a -2.5% spirit resist stack
  (spirit shred, MaxStacks, StackDuration). Cast once; the "recall to refund" flow is not modeled.
- Kingside Knight: self-cast (king): 2x CombatBarrier for BuffDuration, cast once Solomon has lost over 10% health.
  The first time that barrier breaks during the buff, Solomon uses Move: invulnerable for MinKingMoveDuration
  (1 s, raw data), with the gun locked meanwhile. T3: the move cleanses Solomon's debuffs.
- Rook Battery: skillshot. One hit of Damage (both rooks pass the same target, MaxTriggers 1) + immobilize.
  T1: -25% fire rate for DebuffDuration. T2: +5% current health. No walls in a 1v1, so no reflections.
- Develop Queen: the queen crashes on the target (Damage at spirit_accuracy). After QUEEN_LINE_DELAY its square
  lines deal Damage again and stun for StunDuration, times QUEEN_LINE_HIT (the target may stand off the lines).
  The listed DPS is taken to be the short square linger and is skipped. Each of the QueenBonusMoves moves (one per
  MoveCooldown) repeats both. T2 Checkmate: executes the target once he is below CheckmateThreshold (200 + 5 per
  boon).
"""
from deadsim.abilities import AbilityImpl, register

SQUARE_EXPOSURE = 1.0     # s the target spends on bishop squares per move
QUEEN_LINE_DELAY = 1.0    # s between the queen landing and its square lines firing
QUEEN_LINE_HIT = 0.6      # share of line volleys that catch the target
KING_MOVE_TIME = 1.0      # MinKingMoveDuration in ability_chessmaster_movechesspiece (raw)
DEBUFF_KEYS = ("stun", "silence", "disarm", "immobilize", "fire_rate_slow", "outgoing_penalty",
               "spirit_outgoing_penalty", "damage_taken_amp", "spirit_amp_taken", "bullet_amp_taken",
               "bullet_shred", "spirit_shred", "item_silence", "crit_taken")


def cd_keep(c):
    base = c.raw("AbilityCooldown")
    return c.s.cooldown() / base if base else 1.0


@register("ability_chessmaster_throwbishop")
class SetupBishop(AbilityImpl):
    kind = "skillshot"

    def start(self, c):
        c.state.update(out=False, passes=0, stacks=0)

    def should_cast(self, c):
        return not c.state["out"] and self.in_range(c)

    def cast(self, c):
        d = c.raw("AbilityCastDelay")
        c.lock_gun(d)
        c.spirit_hit(c.val("ImpactDamage"), delay=d)
        c.state["out"] = True
        c.after(d + c.raw("MoveCooldown", 3.0) * cd_keep(c), self.move, c)

    def move(self, c):
        if not c.me.alive or not c.foe.alive:
            return
        st = c.state
        acc = c.me.skill.spirit_accuracy
        pen = 1.0 - (c.raw("MultiHitPenaltyPercentage") / 100 if st["passes"] else 0.0)
        st["passes"] += 1
        c.spirit_hit(c.val("Damage") * pen * acc, hit_chance=1.0)
        pieces = max(1, int(c.raw("MaxPieces", 1)))
        c.dot(c.val("DPS") * pieces, SQUARE_EXPOSURE, tick=c.raw("DPSTickInterval", 0.25), hit_chance=acc,
              name=self.s.ab.name + " squares", tag="bishop_sq")
        if c.raw("TechArmorDamageReductionPerStack"):
            st["stacks"] = min(int(c.raw("MaxStacks")), st["stacks"] + 1)
            c.debuff("spirit_shred", st["stacks"] * abs(c.raw("TechArmorDamageReductionPerStack")) / 100 * acc,
                     c.raw("StackDuration", 10), tag="bishop_shred")
        c.after(c.raw("MoveCooldown", 3.0) * cd_keep(c), self.move, c)


@register("ability_chessmaster_knightbuff")
class KingsideKnight(AbilityImpl):
    kind = "self"

    def start(self, c):
        c.state.update(entry=None, moved=True, until=-1.0)

    def should_cast(self, c):
        return c.foe.alive and c.me.hp_frac < 0.9

    def cast(self, c):
        dur = c.dur("BuffDuration")
        c.barrier(2.0 * c.val("CombatBarrier"), dur)
        c.state.update(entry=c.me.barriers[-1], moved=False, until=c.now + dur)

    def on_damage_taken(self, c, src, hit):
        st = c.state
        e = st.get("entry")
        if st["moved"] or not e or e[0] > 0 or c.now >= st["until"]:
            return
        st["moved"] = True
        c.buff("invulnerable", 1, KING_MOVE_TIME, tag="king_move")
        c.lock_gun(KING_MOVE_TIME)
        if c.raw("RemoveDebuffs"):
            c.after(KING_MOVE_TIME, self.cleanse, c)

    def cleanse(self, c):
        for k in DEBUFF_KEYS:
            c.me.mods.d.pop(k, None)


@register("ability_chessmaster_forkpiece")
class RookBattery(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(25.0 + c.me.skill.engage_margin)   # rooks travel forward; no cast range in data

    def cast(self, c):
        d = c.raw("AbilityCastDelay") + c.raw("DetonationDelay")
        c.lock_gun(c.raw("AbilityCastDelay"))
        c.spirit_hit(c.val("Damage"), delay=d)
        acc = c.me.skill.spirit_accuracy
        c.debuff("immobilize", 1, c.dur("ImmobilizeDuration") * acc, delay=d)
        if c.raw("FireRateSlow"):
            c.debuff("fire_rate_slow", c.raw("FireRateSlow") / 100 * acc, c.dur("DebuffDuration"), delay=d)
        if c.raw("CurrentHealthPercent"):
            c.after(d, self.pct, c, acc)

    def pct(self, c, acc):
        if c.me.alive:
            c.spirit_hit(c.raw("CurrentHealthPercent") / 100 * c.foe.hp * acc, hit_chance=1.0)


@register("ability_chessmaster_queen")
class DevelopQueen(AbilityImpl):
    kind = "skillshot"

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.15

    def cast(self, c):
        d = c.raw("AbilityCastDelay")
        c.lock_gun(d)
        moves = int(c.raw("QueenBonusMoves"))
        step = c.raw("MoveCooldown", 5.0) * cd_keep(c)
        for i in range(moves + 1):
            c.after(d + i * step, self.land, c)

    def land(self, c):
        if not c.me.alive or not c.foe.alive:
            return
        acc = c.me.skill.spirit_accuracy
        dmg = c.val("Damage")
        c.spirit_hit(dmg * acc, hit_chance=1.0)
        self.checkmate(c)
        c.spirit_hit(dmg * QUEEN_LINE_HIT, delay=QUEEN_LINE_DELAY, hit_chance=1.0)
        c.debuff("stun", 1, c.dur("StunDuration") * QUEEN_LINE_HIT, delay=QUEEN_LINE_DELAY)
        c.after(QUEEN_LINE_DELAY + 0.01, self.checkmate, c)

    def checkmate(self, c):
        thr = c.val("CheckmateThreshold") if c.tier >= 2 else 0.0
        if thr and c.me.alive and c.foe.alive and c.foe.hp <= thr:
            c.engine.damage(c.me, c.foe, c.foe.hp + c.foe.barrier_total() + 1, "spirit", "Checkmate",
                            ignore_resist=True, is_ability=True, ability=self.s, is_ult=True)
