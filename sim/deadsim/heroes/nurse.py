"""Nurse Harrow (hero_nurse).

Assumptions (replay numbers from scripts/nurse/nurse_replays.py and the hero-vs-hero DamageEvents of 234 Phantom+
replays, 2026-10-25):
- Leech stacks (collected leeches): each gives RegenPerLeechPickup regen, FireRatePerLeechPickup% fire rate and,
  with T2, SpiritPowerPerLeechStack spirit power, up to MaxLeechBonusStacks. A fight starts with the stacks real
  Nurses hold at that net worth (STACKS_BY_SOULS: m_iLeechCount at 1797 Leech Therapy casts in 40 replays; deaths
  cost stacks, so mid game sits near 8 of 10).
- Leech Therapy: one leech feeds on the target (replays: one tick stream per victim at DPS x TickRate, not
  LeechCount streams), DPS for AbilityDuration. Reach: the jar's Radius + LeechCrawlRadius (leeches crawl to
  enemies near where it breaks). While attached, the target's buffs run out LeechEatDurationPerSecond s faster per
  second. The fed leech is picked up PICKUP_S after the cast (replays: median stack gain 12.9 s after a cast), then
  Nurse heals HealPercentOfLeechDamage% of the damage it dealt and gains a stack. Stamina (T1) not modeled.
- Wretched Vapors: cast on cooldown once the fight is on (57% of real casts come before any hero damage in the
  3 s before), on herself with weight SELF_CAST (real Nurses mostly vapor allies, see SELF_CAST). Rush: +RushTimeScaleBonusPercent% speed (fire rate, reload) for AbilityDuration; every incoming hit is
  deferred into specters (DeferredDamagePercent). Healing removes specters first. When the rush ends the remaining
  specters hit for +DeferredDamageBonusPercent%, booked as the enemy's damage (the game credits the attacker with
  ability_nurse_adrenaline_rush), and the crash slows Nurse by CrashTimeScalePenaltyPercent% for CrashDuration.
  T2: +HealingEffectivenessPercent% healing received during the rush. T3: dispels Nurse's debuffs on cast (only if SELF_CAST >= 0.5).
  Cooldown speed-up from the time scale is not modeled; DamageSpiritThresholdPercent (specter size) is ignored.
- Healing Needles: the syringes only heal allies, and a duel has none: never used.
- Lurking Terrors: AbilityCastDelay to open the bag, then an AbilityChannelTime channel; Nurse can't shoot
  meanwhile (guess: both hands on the bag) and a stun ends it. The target faces Nurse while it fights her, so it
  builds terror for BuildupTime, then flees in fear (disarm + silence) for DebuffDuration +
  FearDurationPerLeechStack per stack, then builds again; it takes full DPS throughout (facing her or feared) and
  FireRateSlow% fire-rate slow. T3: Nurse is immune to damage while channeling. Real ult casts hit the main target
  4.2 s of the 7 s on average (they flee out of the cone) and 2.6 heroes: the landing factor absorbs both.
"""
from deadsim.abilities import AbilityImpl, register

# mean m_iLeechCount at Leech Therapy casts by Nurse net worth (souls, stacks), linear in between
STACKS_BY_SOULS = ((0, 1.0), (2500, 2.75), (7500, 7.2), (12500, 7.25), (17500, 8.2), (22500, 8.2), (27500, 7.8),
                   (32500, 10.3), (40000, 10.9))
PICKUP_S = 12.9      # s from a Leech Therapy cast to Nurse picking the fed leech up (replay median stack gain)
CRASH_SRC = "Wretched Vapors (crash)"
# Real Nurses mostly put the vapors on allies: crash damage on Nurse herself is 4.9% of the hero damage she takes
# (234 replays) vs ~40% if she self-cast it in every duel. A duel has no ally, so the rush counts as an expected
# value: SELF_CAST of the deferral, speed-up and crash (scripts/nurse/fit_vapors.py matches the 4.9%).
SELF_CAST = 0.2


def start_stacks(souls):
    pts = STACKS_BY_SOULS
    if souls <= pts[0][0]:
        return pts[0][1]
    for (s0, v0), (s1, v1) in zip(pts, pts[1:]):
        if souls <= s1:
            return v0 + (v1 - v0) * (souls - s0) / (s1 - s0)
    return pts[-1][1]


def leech_ability(f):
    return next((a for a in f.abilities if a.ab.class_name == "ability_nurse_leech_therapy"), None)


def stacks(f):
    return f.counters.get("leech_stacks", 0.0)


@register("ability_nurse_leech_therapy")
class LeechTherapy(AbilityImpl):
    kind = "aoe"

    def in_range(self, c):
        return c.within(c.rng("Radius") + c.val("LeechCrawlRadius"))

    def start(self, c):
        c.me.counters["leech_stacks"] = min(self.max_stacks(c), start_stacks(c.me.st.souls))
        self.apply_stacks(c)

    def max_stacks(self, c):
        return c.raw("MaxLeechBonusStacks", 10.0)

    def apply_stacks(self, c):
        n = stacks(c.me)
        tag = "leech_stacks"
        c.me.mods.add("regen", n * c.val("RegenPerLeechPickup"), 1e9, (tag, "regen"))
        c.me.mods.add("fire_rate", n * c.raw("FireRatePerLeechPickup") / 100, 1e9, (tag, "fire_rate"))
        if c.raw("SpiritPowerPerLeechStack"):
            c.me.mods.add("spirit_power", n * c.raw("SpiritPowerPerLeechStack"), 1e9, (tag, "spirit_power"))

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        tick = c.raw("TickRate", 0.38)
        n = max(1, int(round(c.dur("AbilityDuration") / tick)))
        leech = {"left": n, "dealt": 0.0, "epoch": c.dot_track("leech_therapy", c.now + delay + n * tick)}
        c.after(delay + tick, self.tick, c, leech, tick)
        c.after(PICKUP_S, self.pickup, c, leech)

    def tick(self, c, leech, tick):
        foe = c.foe
        if not foe.alive or not c.dot_live(leech["epoch"]):
            return
        leech["dealt"] += c.engine.damage(c.me, foe, c.val("DPS") * tick, "spirit", self.s.ab.name, is_ability=True,
                                          ability=self.s, is_dot=True)
        eat = c.raw("LeechEatDurationPerSecond") * tick   # the target's buffs run out faster
        debuffs = foe.counters.get("debuffs", set())
        for key, tags in foe.mods.d.items():
            for tg, (v, exp) in list(tags.items()):
                if (key, tg) not in debuffs and exp > c.now:
                    tags[tg] = (v, exp - eat)
        leech["left"] -= 1
        if leech["left"] > 0:
            c.after(tick, self.tick, c, leech, tick)

    def pickup(self, c, leech):
        if not c.me.alive or c.engine.over:
            return
        c.heal(leech["dealt"] * c.raw("HealPercentOfLeechDamage", 100.0) / 100)
        c.me.counters["leech_stacks"] = min(self.max_stacks(c), stacks(c.me) + 1)
        self.apply_stacks(c)


class _Specters:
    """Pseudo item effect on Nurse: while the rush lasts, incoming damage is deferred into specters."""

    def __init__(self, impl):
        self.impl = impl

    def reduce_incoming(self, f, src, amt, kind, is_dot):
        st = self.impl.s.scratch
        if f.e.t >= st.get("rush_end", -1.0):
            return amt
        part = amt * SELF_CAST * self.impl.s.ctx.raw("DeferredDamagePercent", 100.0) / 100
        st["pending"] = st.get("pending", 0.0) + part
        return amt - part


# An allied Nurse's vapors on a duel fighter (Mechanics.ally_vapors): the share of a fighter's incoming damage her rush
# defers when a teammate is Nurse Harrow, fitted so the audit's crash share of the attackers' damage matches real
# Phantom+ matches (scripts/nurse/fit_ally_vapors.py: crash credit is 1.50% of the damage of players facing a Nurse,
# 0 for the rest; the duels booked 0.08% with only her self-cast, 1.48% with this share). The crash comes CRASH_DELAY s after the hit (half of a 4 s rush).
ALLY_VAPORS = 0.018
CRASH_DELAY = 2.0
NURSE_HERO = "Nurse Harrow"


def ally_vapors_share(team, hero):
    """Mechanics.ally_vapors share for a fighter of hero (name) whose real team holds heroes team (names)."""
    return ALLY_VAPORS if hero != NURSE_HERO and NURSE_HERO in team else 0.0


_VAPOR_PROPS = None


def _vapor_props():
    global _VAPOR_PROPS
    if _VAPOR_PROPS is None:
        from deadsim import game
        h = next(h for h in game().heroes.values() if h.name == NURSE_HERO)
        ab = next(a for a in h.abilities if a.class_name == "ability_nurse_adrenaline_rush")
        _VAPOR_PROPS = (ab.props.get("DeferredDamagePercent", 100.0) / 100,
                        ab.props.get("DeferredDamageBonusPercent", 30.0) / 100)
    return _VAPOR_PROPS


class AllyVapors:
    """Pseudo item effect on a fighter vapored by an allied Nurse (expected value, weight w): w x DeferredDamagePercent
    of each incoming hit is deferred, then crashes CRASH_DELAY s later at +DeferredDamageBonusPercent, credited to
    the attacker as CRASH_SRC (no procs), like the crash on a self-cast Nurse."""

    def __init__(self, w):
        self.w = w

    def reduce_incoming(self, f, src, amt, kind, is_dot):
        defer, bonus = _vapor_props()
        part = amt * self.w * defer
        if part > 0 and src is not None and src is not f:
            f.e.after(CRASH_DELAY, self.crash, f, src, part * (1.0 + bonus))
        return amt - part

    def crash(self, f, src, dmg):
        if f.alive and not f.e.over:
            f.e.damage(src, f, dmg, "pure", CRASH_SRC, pure=True, procs=False)


@register("ability_nurse_adrenaline_rush")
class WretchedVapors(AbilityImpl):
    kind = "self"

    def in_range(self, c):
        return c.foe.alive

    def start(self, c):
        c.state.update(pending=0.0, rush_end=-1.0)
        c.me.items_fx.append(_Specters(self))
        f, heal = c.me, c.me.heal

        def specter_heal(amount, source="heal", kind="regen", origin=None):
            # healing removes specters first (counted as healing done), the rest heals as usual
            st = self.s.scratch
            if st["pending"] > 0 and f.alive and amount > 0:
                amp = f.st.heal_amp if kind == "regen" else f.st.heal_amp_cast
                eff = amount * max(0.0, 1.0 + amp + f.stat("heal_received"))
                if eff > 0:
                    used = min(st["pending"], eff)
                    st["pending"] -= used
                    f.healed += used
                    f.healed_exp += used * f.e.length_w()
                    amount *= 1.0 - used / eff
                    if amount <= 0:
                        return used
                    return used + heal(amount, source, kind, origin)
            return heal(amount, source, kind, origin)
        f.heal = specter_heal

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        c.after(delay, self.rush, c)

    def rush(self, c):
        if not c.me.alive:
            return
        d = c.dur("AbilityDuration")
        speed = c.val("RushTimeScaleBonusPercent") / 100
        if c.tier >= 3 and SELF_CAST >= 0.5:
            c.me.dispel()
        c.buff("fire_rate", speed * SELF_CAST, d, tag="vapors_rush_fr")
        c.buff("reload_mult", (1.0 / (1.0 + speed) - 1.0) * SELF_CAST, d, tag="vapors_rush_rl")
        if c.raw("HealingEffectivenessPercent"):
            c.buff("heal_received", c.raw("HealingEffectivenessPercent") / 100 * SELF_CAST, d, tag="vapors_heal")
        c.state["rush_end"] = c.now + d
        c.after(d, self.crash, c)

    def crash(self, c):
        st = c.state
        f = c.me
        if not f.alive or c.engine.over:
            st["pending"] = 0.0
            return
        slow = c.raw("CrashTimeScalePenaltyPercent") / 100
        cd = c.raw("CrashDuration", 4.0)
        c.buff("fire_rate", -slow * SELF_CAST, cd, tag="vapors_crash_fr")
        c.buff("reload_mult", (1.0 / max(0.1, 1.0 - slow) - 1.0) * SELF_CAST, cd, tag="vapors_crash_rl")
        dmg = st["pending"] * (1.0 + c.raw("DeferredDamageBonusPercent") / 100)
        st["pending"] = 0.0
        if dmg > 0 and c.foe is not None:
            c.engine.damage(c.foe, f, dmg, "pure", CRASH_SRC, pure=True, procs=False)


@register("ability_nurse_healing_needles")
class HealingNeedles(AbilityImpl):
    kind = "passive"   # heals allies only; no ally in a 1v1


@register("ability_nurse_fear")
class LurkingTerrors(AbilityImpl):
    kind = "aoe"
    range_props = ("AbilityCastRange",)

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.15

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        T = c.dur("AbilityChannelTime")
        c.lock_gun(delay + T)
        if c.raw("ChannelDamageImmune"):
            c.buff("invulnerable", 1, delay + T, tag="terrors_immune")
        tick = c.raw("TickRate", 0.15)
        c.state.update(end=c.now + delay + T, terror=0.0, feared_until=-1.0)
        c.after(delay + tick, self.tick, c, tick)

    def tick(self, c, tick):
        st = c.state
        f, foe = c.me, c.foe
        if not f.alive or not foe.alive or c.now > st["end"] + 1e-9:
            return
        if f.mods.active("stun"):   # channel broken
            f.gun_locked_until = c.now
            f.mods.remove("invulnerable", "terrors_immune")
            return
        c.engine.damage(f, foe, c.val("DPS") * tick, "spirit", self.s.ab.name, is_ability=True, ability=self.s,
                        is_dot=True, is_ult=True)
        c.debuff("fire_rate_slow", c.raw("FireRateSlow") / 100, tick + c.raw("SlowLingerDuration", 0.5),
                 tag="terrors_slow")
        if c.now >= st["feared_until"]:
            st["terror"] += tick
            if st["terror"] >= c.raw("BuildupTime", 1.3):
                fear = c.dur("DebuffDuration") + c.raw("FearDurationPerLeechStack") * stacks(f)
                c.debuff("disarm", 1, fear, tag="terrors_fear")
                c.debuff("silence", 1, fear, tag="terrors_fear_s")
                st["terror"] = 0.0
                st["feared_until"] = c.now + fear
        c.after(tick, self.tick, c, tick)
