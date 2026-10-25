"""Victor (hero_frank).

Assumptions:
- Self-damage (Jumpstart, Aura of Suffering) is spirit damage to himself (his spirit resist applies), can't kill
  Victor and is not counted as damage dealt. It charges the Pain Battery like any other damage.
- Pain Battery: starts empty; full after taking StoredDamageHealthPercentRequired % of max health
  (generation x (1 + cooldown reduction), per the ETechCooldown tag on BatteryGenerationPercent). 7 bolts hit
  the target once (Damage, once per target).
- Jumpstart: TotalHealthRegen is healed over AbilityDuration, decaying linearly. Cast when below
  JUMPSTART_HP.
- Aura of Suffering: toggled on once the target is in radius and kept on; enemy DPS ramps linearly from MinDPS
  to MaxDPS over AbilityDuration; Victor takes SelfDPS (flat) per second. T2's MinDps key is added by hand
  (data spells it differently).
- Shocking Reanimation: on lethal damage Victor is invulnerable and can't act for RespawnDelay, then revives
  with RespawnHealthPercent and hits Damage + stun if the target is within Radius. T1: +BonusFireRate and
  BonusDamagePerBullet spirit damage per bullet hit (6 + 0.06 x spirit), only while the ult is on cooldown.
  Carried over from earlier fights (CARRY_COOLDOWN): in real Phantom+ games the ult is still on cooldown at the
  start of 11% of Victor's lane fights and ~30-50% later (data/victor_revive.json, scripts/mechanics/victor_revive.py:
  seconds since his last revive at each fight start). Fights that book damage over real fight lengths and have an
  rng or a fight phase draw that time: with it under the cooldown the duel starts with the ult on cooldown for the
  rest (no revive, the T1 bonus on). Other fights (dummy page, deterministic) start with it ready.
"""
import json
import os
import zlib

from deadsim.abilities import AbilityImpl, register

JUMPSTART_HP = 0.6       # cast Jumpstart below this health fraction
SELF_TAG = "victor_self"
CARRY_COOLDOWN = True
_carry = None


def carried_cooldown(c, s):
    """Seconds of Shocking Reanimation's cooldown left from an earlier fight when this one starts (0 = ready)."""
    global _carry
    f, e = c.me, c.engine
    if not CARRY_COOLDOWN or getattr(e, "length", None) is None:
        return 0.0
    if f.skill.fight_phase is not None:
        r = (f.skill.fight_phase + zlib.crc32(f"victor_revive|{f.name}".encode()) / 2 ** 32) % 1.0
    elif e.rng is not None:
        r = e.rng.random()
    else:
        return 0.0
    if _carry is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "..", "data", "victor_revive.json")) as fh:
            _carry = json.load(fh)["phases"]
    souls = f.st.souls
    qs = _carry["lane" if souls < 10000 else "mid" if souls <= 27000 else "late"]
    since = qs[min(len(qs) - 1, int(r * len(qs)))]
    return 0.0 if since is None else max(0.0, s.cooldown() - since)


def find(c, class_name):
    for ab in c.me.abilities:
        if ab.ab.class_name == class_name:
            return ab
    return None


def self_damage(c, amount):
    """Spirit self-damage (resisted, never lethal, not counted as damage); it charges the Pain Battery."""
    f = c.me
    before = f.hp
    c.self_damage(amount, kind="spirit")
    amt = before - f.hp
    bat = find(c, "ability_frank_shocktarget2")
    if bat is not None and bat.unlocked:
        bat.impl.charge(bat.ctx, amt)


@register("ability_frank_shocktarget2")
class PainBattery(AbilityImpl):
    kind = "target"

    def start(self, c):
        c.state["stored"] = 0.0

    def charge(self, c, amount):
        gen = c.raw("BatteryGenerationPercent", 100) / 100 * (1.0 + c.me.st.cdr)
        c.state["stored"] = c.state.get("stored", 0.0) + amount * gen

    def full(self, c):
        return c.state.get("stored", 0.0) >= c.raw("StoredDamageHealthPercentRequired", 40) / 100 * c.me.max_hp

    def on_damage_taken(self, c, attacker, hit):
        self.charge(c, hit.amount)

    def should_cast(self, c):
        return self.full(c) and self.in_range(c)

    def cast(self, c):
        c.state["stored"] = 0.0
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay + c.raw("AbilityPostCastDuration"))
        c.spirit_hit(c.val("Damage"), delay=delay)
        if c.tier >= 3:
            pct = c.raw("MissingHealthPercentHeal") / 100
            c.after(delay, lambda: c.me.alive and c.heal((c.me.max_hp - c.me.hp) * pct))


@register("ability_frank_selfzap")
class Jumpstart(AbilityImpl):
    kind = "self"

    def should_cast(self, c):
        return c.me.hp_frac < JUMPSTART_HP

    def cast(self, c):
        self_damage(c, c.me.hp * c.raw("CurrentHealthPercentDamage") / 100)
        total = c.val("TotalHealthRegen")   # healing spirit scale (+ T3 scaling upgrade)
        d = c.dur("AbilityDuration")
        n = max(1, int(d / 0.5))
        # linear decay: weights n, n-1, ..., 1
        wsum = n * (n + 1) / 2
        for i in range(n):
            amt = total * (n - i) / wsum
            c.after(0.5 * (i + 1), lambda a=amt: c.me.alive and c.heal(a))
        if c.tier >= 3:
            c.buff("status_resist", c.raw("StatusResistancePercent") / 100, d)


@register("ability_frank_painaura")
class AuraOfSuffering(AbilityImpl):
    kind = "aoe"
    range_props = ("Radius",)

    def should_cast(self, c):
        return not c.state.get("on") and self.in_range(c)

    def cast(self, c):
        c.state["on"] = True
        c.state["t0"] = c.now
        c.after(c.raw("TickRate", 0.25), self.tick, c)

    def tick(self, c):
        if not c.me.alive or not c.foe.alive or c.engine.over:
            return
        tick = c.raw("TickRate", 0.25)
        if c.me.mods.active("stun"):          # e.g. during Shocking Reanimation the aura drops
            c.state["on"] = False
            return
        ramp = min(1.0, (c.now - c.state["t0"]) / max(0.1, c.raw("AbilityDuration", 8)))
        lo = c.val("MinDPS") + c.raw("MinDps")
        hi = c.val("MaxDPS")
        dps = lo + (hi - lo) * ramp
        if self.in_range(c):
            c.engine.damage(c.me, c.foe, dps * tick, "spirit", self.s.ab.name, is_ability=True, ability=self.s,
                            is_dot=True)
            if c.tier >= 3:
                c.debuff("damage_taken_amp", c.raw("IncomingDamagePercent") / 100, tick + 0.05)
        self_damage(c, c.raw("SelfDPS") * tick)
        c.after(tick, self.tick, c)


class _Revive:
    """Injected into Victor's items_fx so the engine asks it before he dies."""

    def __init__(self, st):
        self.st = st

    def on_lethal(self, f, src):
        s = self.st
        c = s.ctx
        if not s.unlocked or c.now < s.ready_at:
            return False
        s.casts += 1
        s.ready_at = c.now + s.cooldown()
        c.state["cd_until"] = s.ready_at
        f.hp = 1.0
        wait = c.raw("RespawnDelay", 3.0)
        f.mods.add("invulnerable", 1, wait, "victor_revive")
        f.mods.add("stun", 1, wait, "victor_revive")
        f.e.note(f"{f.name} Shocking Reanimation")

        def revive():
            if not f.alive or f.e.over:
                return
            f.hp = max(f.hp, f.max_hp * min(1.0, c.raw("RespawnHealthPercent") / 100))
            p = c.p_in(c.rng("Radius"))   # share of the time the target is in the blast
            if p > 0:
                c.spirit_hit(c.val("Damage") * p)
                c.debuff("stun", 1, c.dur("StunDuration") * p)
        f.e.after(wait, revive)
        return True


@register("ability_frank_revive")
class ShockingReanimation(AbilityImpl):
    kind = "passive"

    def start(self, c):
        c.me.items_fx.append(_Revive(self.s))
        c.state["cd_until"] = -1.0
        left = carried_cooldown(c, self.s) if self.s.unlocked else 0.0
        if left > 0:
            self.s.ready_at = c.now + left
            c.state["cd_until"] = self.s.ready_at
        if c.tier >= 1:
            c.me.stat_hooks.append(
                lambda f: {"fire_rate": c.raw("BonusFireRate") / 100} if c.now < c.state["cd_until"] else {})

    def on_shot(self, c, ctx):
        if c.tier >= 1 and c.now < c.state["cd_until"]:
            ctx["bonus_spirit"].append((c.val("BonusDamagePerBullet"), self.s.ab.name))
