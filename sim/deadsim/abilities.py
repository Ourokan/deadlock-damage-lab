"""Hero ability layer.

Every ability gets an AbilityState in the fight. Its behaviour comes from an AbilityImpl subclass
registered by the ability's class_name (see deadsim/heroes/*.py). Abilities without a hand-written
implementation fall back to GenericAbility, which deals the ability's listed damage on cast.

Writing an implementation (the whole API an ability needs):

    from deadsim.abilities import AbilityImpl, register

    @register("ability_incendiary_projectile")          # class_name from data/game/abilities.json
    class Napalm(AbilityImpl):
        kind = "skillshot"                               # skillshot | target | aoe | self | passive
        def cast(self, c):                               # c is a CastCtx
            c.lock_gun(c.val("AbilityCastDelay"))        # can't shoot while casting
            c.spirit_hit(c.val("Damage"), delay=c.val("AbilityCastDelay"))
            c.debuff("damage_taken_amp", c.val("IncomingDamagePercentFromCaster") / 100, c.dur("DebuffDuration"))

CastCtx helpers: val(prop) (upgrades + spirit/boon/melee/weapon scaling + duration/range applied), raw(prop),
scale(prop) (scaling factor incl. upgrades), light_melee(),
dur(prop), tier (0-3 upgrades bought), sp (caster spirit power for this ability), dist (meters),
spirit_hit(amount, ...), dot(dps, duration, ...), bullet_hit(amount), debuff(key, value, duration),
buff(key, value, duration), barrier(amount, duration), heal(amount), lock_gun(seconds),
after(delay, fn), engine, me (Fighter), foe (Fighter).

Modifier keys understood by the engine (buff on caster / debuff on enemy):
    weapon_pct, fire_rate, fire_rate_slow, spirit_power, bullet_resist, spirit_resist,
    bullet_shred, spirit_shred, damage_taken_amp, spirit_amp_taken, bullet_amp_taken,
    damage_amp (caster: + all outgoing damage), outgoing_penalty, spirit_outgoing_penalty, bullet_lifesteal, spirit_lifesteal,
    heal_received, regen, max_health, evasion, crit_taken, reload_mult,
    stun, silence, disarm, invulnerable, bullet_immune, item_silence (value ignored for states).
Values are fractions (0.16 = 16%) except spirit_power, regen, max_health (flat).
"""
from __future__ import annotations

from .build import combine_resist

REGISTRY = {}
# scripts/cast_timing/fit_cast_timing.py's probe: every first cast acts as one held to real cast timing
# (AbilityState.held_opener), to measure the sim's own timing of abilities that only wait for a gate a held first
# cast skips (an ultimate's setup, Slam Fire's last shell)
PROBE_HELD = False


def register(*class_names):
    def deco(cls):
        for n in class_names:
            REGISTRY[n] = cls
        return cls
    return deco


DAMAGE_PROPS = ("Damage", "ImpactDamage", "ExplosionDamage", "ExplodeDamage", "BaseDamage", "LandingDamage",
                "StompDamage", "PulseDamage", "FullChargeDamage", "MaxDamage", "PerfectDamage", "DelayedDamage")
DPS_PROPS = ("DPS", "PulseDPS", "TurretDPS", "MaxDPS")
DUR_PROPS = ("AbilityDuration", "DebuffDuration", "DotDuration", "Duration", "AbilityChannelTime")


class CastCtx:
    def __init__(self, state):
        self.s = state

    # data access ----------------------------------------------------------------------------------
    @property
    def engine(self):
        return self.s.f.e

    @property
    def me(self):
        return self.s.f

    @property
    def foe(self):
        return self.s.f.enemy

    @property
    def tier(self):
        return self.s.tier

    @property
    def dist(self):
        return self.s.f.e.distance

    @property
    def now(self):
        return self.s.f.e.t

    @property
    def sp(self):
        return self.s.spirit_power()

    @property
    def state(self):
        """Per-fight scratch dict for this ability (stacks, toggles, ...)."""
        return self.s.scratch

    def _special(self, prop):
        """Bought scale / multiply upgrades for prop: [(upgrade_type, scale_stat_filter, bonus), ...]."""
        out = []
        for i, u in enumerate(self.s.ab.scale_upgrades):
            if i < self.s.tier and prop in u:
                out.extend(u[prop])
        return out

    def raw(self, prop, default=0.0):
        """Base value + bought flat upgrades (and EMultiplyBase % upgrades), no scaling. Cached per tier."""
        key = (prop, default, self.s.tier)
        cache = self.s.__dict__.setdefault("_raw_cache", {})
        v = cache.get(key)
        if v is None:
            v = cache[key] = self._raw(prop, default)
        return v

    def _raw(self, prop, default):
        ab = self.s.ab
        v = ab.props.get(prop)
        v = default if v is None else v
        for i, u in enumerate(ab.upgrades):
            if i < self.s.tier and prop in u and u[prop] is not None:
                v += u[prop]
        for t, _, b in self._special(prop):
            if t == "EMultiplyBase":
                v *= 1.0 + b / 100.0
        return v

    def scale(self, prop):
        """The property's scaling factor with bought EAddToScale / EMultiplyScale upgrades applied."""
        sc = self.s.ab.scale.get(prop)
        k = sc[2] if sc else 0.0
        for t, _, b in self._special(prop):
            if t == "EAddToScale":
                k += b
            elif t == "EMultiplyScale" and b:
                k *= b
        return k

    def scale_type(self, prop):
        """(scale class, stat type) of the property, or (None, None). A property with no base scale that gains
        an EAddToScale upgrade takes the upgrade's stat filter (spirit power when unset)."""
        sc = self.s.ab.scale.get(prop)
        if sc:
            return sc[0], sc[1]
        for t, filt, _ in self._special(prop):
            if t == "EAddToScale":
                return "scale_function_tech_damage" if filt in (None, "ETechPower") else None, filt or "ETechPower"
        return None, None

    def light_melee(self):
        """Hero light melee damage at the current level (base + per-boon growth), before melee % bonuses."""
        h = self.me.st.hero
        return h.base.get("light_melee_damage", 0.0) + self.me.st.boons * h.per_boon.get(
            "MODIFIER_VALUE_BASE_MELEE_DAMAGE_FROM_LEVEL", 0.0)

    def val(self, prop, default=0.0):
        """Value as the game would show it: upgrades, + scaling (spirit power, healing spirit scale, boons,
        light melee, weapon damage %), duration / range item bonuses."""
        v = self.raw(prop, default)
        cls, stype = self.scale_type(prop)
        k = self.scale(prop)
        if not k:
            return v
        if cls in ("scale_function_tech_damage", "scale_function_healing_spirit_scale") or stype == "ETechPower":
            v += k * self.sp
        elif stype == "ETechDuration" or cls == "scale_function_tech_duration":
            v *= 1.0 + self.s.duration_pct()
        elif stype in ("ETechRange", "ETechRadius"):
            v *= 1.0 + self.s.range_pct()
        elif stype == "ELevelUpBoons":
            v += k * self.me.st.boons
        elif stype == "ELightMeleeDamage":
            v += k * self.light_melee()
        elif stype == "EBaseWeaponDamageIncrease":
            v *= 1.0 + k * (self.me.st.weapon_pct + self.me.stat("weapon_pct"))
        return v

    def dur(self, prop, default=0.0):
        """Duration with ability-duration bonuses applied even if the property has no scale tag."""
        return self.raw(prop, default) * (1.0 + self.s.duration_pct())

    def rng(self, prop, default=0.0):
        return self.raw(prop, default) * (1.0 + self.s.range_pct())

    def within(self, reach):
        """Cast gate for an ability that reaches `reach` meters (range bonuses already applied): castable within
        reach + skill.engage_margin; up to skill.walk_in meters further the caster walks in first (gap / move speed
        s, the gun keeps firing); further away it isn't cast. With range spread (mechanics range_drift) the same
        as an expected wait: Engine.reach_ready."""
        sk = self.me.skill
        return self.engine.reach_ready(self.state, reach + sk.engage_margin, self.me, walk_in=sk.walk_in,
                                       mean_field=True)

    def reach(self, r):
        """Cast gate at a hard reach of r m (no engage margin or walk-in added): the target within r now. With range
        spread the same as within(): cast now, damage scaled by the expected wait for the target to come within r.
        Self buffs keep the median check: the expected wait only scales damage, so it can't price a buff."""
        if self.s.impl.kind == "self":
            return self.p_in(r) >= 0.5
        return self.engine.reach_ready(self.state, r, self.me, mean_field=True)

    def p_in(self, r):
        """Share of fight time the target is within r m (1 or 0 at a fixed distance): scales an effect that only
        lands inside a radius; p_in(r) >= 0.5 is the median-distance check, for all-or-nothing effects."""
        return self.engine.p_within(r)

    # effects --------------------------------------------------------------------------------------
    def spirit_hit(self, amount, *, delay=0.0, name=None, hit_chance=None, ignore_resist=False, nonlethal=False,
                   weapon_proc=False):
        """Instant spirit damage to the enemy (after delay). hit_chance defaults to caster's spirit_accuracy for
        skillshots and 1.0 otherwise. weapon_proc: the hit also procs Mystic Shot like a gun hit."""
        f, e = self.me, self.foe
        name = name or self.s.ab.name
        if hit_chance is None:
            hit_chance = f.skill.spirit_accuracy if self.s.impl.kind == "skillshot" else 1.0
        amount *= hit_chance

        def go():
            if f.alive or self.s.impl.post_mortem:
                f.e.damage(f, e, amount, "spirit", name, is_ability=True, ability=self.s,
                           is_ult=self.s.ab.ultimate, ignore_resist=ignore_resist, nonlethal=nonlethal,
                           weapon_proc=weapon_proc)
        if delay > 0:
            f.e.after(delay, go)
        else:
            go()

    def bullet_hit(self, amount, *, delay=0.0, name=None, headshots=0, hits=1):
        f, e = self.me, self.foe
        name = name or self.s.ab.name

        def go():
            f.e.damage(f, e, amount, "bullet", name, is_ability=True, ability=self.s, headshots=headshots, hits=hits)
        if delay > 0:
            f.e.after(delay, go)
        else:
            go()

    def dot(self, dps, duration, *, tick=0.5, name=None, kind="spirit", tag=None, delay=0.0, hit_chance=1.0, **kw):
        """Extra keywords (nonlethal, procs, ...) go to Engine.dot."""
        f, e = self.me, self.foe
        name = name or self.s.ab.name

        def go():
            f.e.dot(f, e, dps * hit_chance, duration, name, kind=kind, tick=tick, tag=tag or name,
                    is_ability=True, ability=self.s, is_ult=self.s.ab.ultimate, **kw)
        if delay > 0:
            f.e.after(delay, go)
        else:
            go()

    def gun_volley(self, n_bullets, per_bullet=None, *, name=None, accuracy=None, headshots=True, procs=True,
                   extra_pct=0.0, kind="bullet", landed=False, weapon_proc=False):
        """Fire n bullets from an ability (e.g. a gun-based ultimate). per_bullet defaults to the hero's
        current gun bullet (weapon %, falloff included; out of the gun's range the bullets miss). Accuracy/headshots use
        the caster's skill. landed=True: the landing factor was applied another way, so the engine does not scale the
        damage by it. weapon_proc=True: the ability fires the weapon itself, so its bullets proc on-hit items like gun
        bullets (Hit.gun_bullet)."""
        f, e = self.me, self.foe
        eng = f.e
        base, crit = eng.bullet_damage(f, extra_pct)
        per = base if per_bullet is None else per_bullet
        acc = f.skill.accuracy if accuracy is None else accuracy
        hits = f.hit_acc.take(min(1.0, acc * (1.0 - e.stat("evasion")) * eng.hit_reach(f.st)), int(n_bullets))
        if hits <= 0:
            return 0
        heads = f.head_acc.take(f.skill.headshot, hits) if headshots else 0
        crit_eff = 1.0 + (crit - 1.0) * e.st.crit_received_scale
        raw = per * (hits - heads) + per * crit_eff * heads
        eng.damage(f, e, raw, kind, name or self.s.ab.name, is_ability=True, ability=self.s,
                   headshots=heads, hits=hits, procs=procs, is_ult=self.s.ab.ultimate, landed=landed,
                   weapon_proc=weapon_proc)
        return hits

    def melee_hit(self, amount, *, name=None, delay=0.0):
        f, e = self.me, self.foe
        amount *= f.melee_mult()

        def go():
            f.e.damage(f, e, amount, "melee", name or self.s.ab.name, is_ability=True, ability=self.s)
        if delay > 0:
            f.e.after(delay, go)
        else:
            go()

    def debuff(self, key, value, duration, tag=None, delay=0.0):
        """Effect on the enemy. Status resist shortens it."""
        e = self.foe
        tag = tag or (self.s.ab.class_name, key)
        dur = duration * (1.0 - e.st.status_resist - e.stat("status_resist"))

        def go():
            if not e.alive:
                return
            if self.me.e.mech is not None and "spell_parry" in e.counters:
                from .mechanics import spell_blocked
                if spell_blocked(self.me.e, self.me, e, self.s):
                    return
            e.mods.add(key, value, dur, tag)
            e.mark_debuff(key, tag)
            if key in ("stun", "silence", "disarm", "immobilize"):
                for fx in e.items_fx:
                    g = getattr(fx, "on_cc", None)
                    if g:
                        g(e, key)
        if delay > 0:
            self.me.e.after(delay, go)
        else:
            go()

    def dot_track(self, tag, until, buildup=False):
        """For a DoT whose ticks the ability schedules itself (not via dot): show it to the enemy's Dispel Magic
        (Fighter.afflicted) until `until`; buildup=True for a DoT the enemy's gun keeps re-applying
        (Fighter.buildup_dot). Returns the enemy's dispel epoch; ticks stop once dot_live(epoch) is False
        (Fighter.dispel bumps it)."""
        e = self.foe
        e.counters.setdefault("dot_until", {})[tag] = until
        if buildup:
            e.counters.setdefault("buildup_dots", set()).add(tag)
        return e.counters.get("dispel_epoch", 0)

    def dot_live(self, epoch):
        return self.foe.counters.get("dispel_epoch", 0) == epoch

    def buff(self, key, value, duration, tag=None):
        self.me.mods.add(key, value, duration, tag or (self.s.ab.class_name, key))

    def barrier(self, amount, duration):
        self.me.add_barrier(amount, duration)

    def heal(self, amount):
        return self.me.heal(amount, self.s.ab.name, "ability")

    def self_damage(self, amount, kind="pure"):
        """Health cost on the caster: resisted like damage of `kind` (pure = unresisted), never lethal, not
        counted as damage dealt or taken."""
        f = self.me
        if kind == "spirit":
            amount *= 1.0 - combine_resist(f.spirit_resists(), ())
        elif kind == "bullet":
            amount *= 1.0 - combine_resist(f.bullet_resists(), ())
        f.hp = max(1.0, f.hp - max(0.0, amount))

    def lock_gun(self, seconds):
        f = self.me
        f.gun_locked_until = max(f.gun_locked_until, f.e.t + max(0.0, seconds))

    def after(self, delay, fn, *args):
        self.me.e.after(delay, fn, *args)


class AbilityImpl:
    kind = "skillshot"         # skillshot | target | aoe | self | passive
    post_mortem = False        # keeps dealing damage after the caster dies (e.g. projectiles in flight)
    modeled = True             # False for GenericAbility so reports can flag it
    spirit_procs = False       # its melee hits proc Mystic Burst / Tankbuster like spirit ability hits (Uppercut)
    tankbuster_chance = None   # spirit_procs hits release Tankbuster on this share of hits, ignoring its MinimumDamage

    def held(self, c: CastCtx):
        """The slot's first-cast hold (mechanics.hold_first_casts, AbilityState.held_until) applies to this cast.
        Silver's wolf abilities share a slot with human abilities whose real holds don't time them."""
        return True

    def __init__(self, state):
        self.s = state

    range_props = ("AbilityCastRange", "Radius", "Range")

    def in_range(self, c: CastCtx):
        """Within the ability's reach. Players close a few meters to land abilities, so the caster's
        skill.engage_margin (default 5 m) is added."""
        r = 0.0
        for p in self.range_props:
            r = c.rng(p)
            if r:
                break
        return r <= 0 or c.within(r)

    def should_cast(self, c: CastCtx):
        """Cast as soon as it's ready and the target is in range. Override for conditional casts."""
        return self.in_range(c)

    def cast(self, c: CastCtx):
        pass

    def start(self, c: CastCtx):
        """Called once at fight start (passives, innate effects)."""

    def prefight_lead(self, c: CastCtx):
        """Seconds before t=0 a prefight cast happened (only for impls that define prefight(c))."""
        return 0.0


class GenericAbility(AbilityImpl):
    """Fallback: listed instant damage on cast + DPS over its duration. Marked unmodeled in reports."""
    modeled = False

    def should_cast(self, c):
        return (c.raw("AbilityCooldown") > 0 and self.in_range(c)
                and (any(c.raw(p) for p in DAMAGE_PROPS) or any(c.raw(p) for p in DPS_PROPS)))

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        for p in DAMAGE_PROPS:
            if c.raw(p):
                c.spirit_hit(c.val(p), delay=delay)
                break
        for p in DPS_PROPS:
            if c.raw(p):
                d = next((c.dur(q) for q in DUR_PROPS if c.raw(q)), 3.0)
                c.dot(c.val(p), d, delay=delay)
                break


class AbilityState:
    def __init__(self, fighter, ab, tier=0, unlocked=True, imbues=()):
        self.f = fighter
        self.ab = ab
        self.tier = tier
        self.unlocked = unlocked
        self.imbues = list(imbues)       # Item objects imbued on this ability
        self.scratch = {}
        impl_cls = REGISTRY.get(ab.class_name, GenericAbility)
        self.impl = impl_cls(self)
        self.ctx = CastCtx(self)
        self.charges = 0
        self.next_charge = 0.0
        self.ready_at = 0.0
        self.held_until = 0.0   # first cast held to real cast timing (mechanics.hold_first_casts); not a cooldown
        self.precast_at = None   # mechanics.precast: cast this long before the fight start
        self.timed = False       # the first cast has a real cast timing hold (patterns.Plan skips the ult's wait)
        self.recast_wait = 0.0   # mechanics.recast_timing: the next cast waits this long past ready_at (inf: not this fight)
        self.casts = 0
        self.resets = 0

    # stats --------------------------------------------------------------------------------------------
    def is_charged(self):
        return self.ctx.raw("AbilityCooldownBetweenCharge") > 0 or self.ctx.raw("AbilityCharges") >= 2

    def max_charges(self):
        n = int(round(self.ctx.raw("AbilityCharges"))) or 1
        if self.is_charged():
            n += self.f.st.bonus_charges
        return n

    def spirit_power(self):
        f = self.f
        sp = f.spirit_power()
        if self.is_charged():
            sp += f.st.charged_spirit
        for it in self.imbues:
            if it.class_name == "upgrade_magic_storm":
                sp += it.p("ImbuedTechPower")
        sp += self.scratch.get("_bonus_spirit", 0.0)
        return sp

    def duration_pct(self):
        d = self.f.st.duration_pct
        for it in self.imbues:
            if it.class_name == "upgrade_arcane_extension":
                d += it.p("BonusAbilityDurationPercent") / 100
        return d + self.scratch.get("_bonus_duration", 0.0)

    def range_pct(self):
        r = self.f.st.range_pct
        for it in self.imbues:
            if it.class_name in ("upgrade_magic_reach", "upgrade_bulletshredimbue"):
                r += it.p("TechRangeMultiplier") / 100
        return r

    def cooldown(self):
        base = self.ctx.raw("AbilityCooldown")
        reds = [self.f.st.cdr, self.f.stat("cdr")]
        if self.is_charged():
            reds.append(self.f.st.charged_cdr)
        if self.ab.ultimate:
            reds.append(self.f.st.ult_cdr)
        for it in self.imbues:
            if it.class_name == "upgrade_magic_tempo":
                reds.append(it.p("CooldownReduction") / 100)
        keep = 1.0
        for r in reds:
            keep *= (1.0 - max(0.0, min(0.95, r)))
        return base * keep

    def charge_delay(self):
        return self.ctx.raw("AbilityCooldownBetweenCharge") * (1.0 - self.f.st.charge_delay_red)

    # lifecycle ----------------------------------------------------------------------------------------
    def start(self):
        self.charges = self.max_charges()
        self.ready_at = self.f.e.t
        if self.unlocked:
            self.impl.start(self.ctx)

    def held_opener(self):
        """The next cast is the first one and is held to real cast timing (mechanics.cast_timing): gates a real
        opener doesn't wait for (an ultimate's setup, Slam Fire's last shell) let it go."""
        return (self.timed or PROBE_HELD) and not self.casts

    def _recharge(self):
        t = self.f.e.t
        while self.charges < self.max_charges() and self.next_charge and t >= self.next_charge:
            self.charges += 1
            self.next_charge = self.next_charge + self.cooldown() if self.charges < self.max_charges() else 0.0

    def try_cast(self):
        if not self.unlocked or self.impl.kind == "passive":
            return False
        t = self.f.e.t
        self._recharge()
        if self.charges <= 0 or t < self.ready_at + self.recast_wait or (t < self.held_until and self.impl.held(self.ctx)):
            return False
        if self.f.counters.get("fleeing") and self.impl.kind != "self":
            return False
        if not self.impl.should_cast(self.ctx) or (self.f.plan is not None and not self.f.plan.allows(self)):
            self.scratch.pop("_reach_delay", None)   # a reach gate may have passed inside a condition that failed
            return False
        self.cast()
        return True

    def prefight(self):
        """Cast before the fight (deadsim.patterns): the impl's prefight(c) runs at t=0 in place of cast(c), and the
        cooldown counts from impl.prefight_lead(c) s earlier."""
        lead = self.impl.prefight_lead(self.ctx)
        self.scratch["prefight"] = True
        self.cast()
        self.scratch.pop("prefight", None)
        self.ready_at -= lead
        if self.next_charge:
            self.next_charge -= lead

    def cast(self):
        f = self.f
        t = f.e.t
        self.casts += 1
        self.charges -= 1
        if self.max_charges() > 1:
            if not self.next_charge:
                self.next_charge = t + self.cooldown()
            self.ready_at = t + self.charge_delay()
        else:
            self.ready_at = t + self.cooldown()
            self.next_charge = self.ready_at
        if f.e.length and f.e.mech is not None and getattr(f.e.mech, "recast_timing", False):
            from .mechanics import recast_wait
            self.recast_wait = recast_wait(self)
        f.e.note(f"{f.name} casts {self.ab.name}")
        if getattr(f.e, "profile_casts", False):
            f.cast_first.setdefault(self.ab.class_name, t)
        wait = self.scratch.pop("_reach_delay", 0.0)   # range spread: damage x cooldown / (cooldown + expected wait)
        cd = self.cooldown()   # time per cast: charges recharge one per cooldown, so the gap between charges isn't it
        self.scratch["_avail"] = cd / (cd + wait) if wait > 0 and cd > 0 else 1.0
        for fx in f.items_fx:
            g = getattr(fx, "on_cast", None)
            if g:
                g(f, self)
        # every enemy hero sees the cast (one in a duel; team.TeamEngine sets f.foes)
        for en in getattr(f, "foes", None) or ([f.enemy] if f.enemy is not None else []):
            if not en.alive:
                continue
            for fx in en.items_fx:
                g = getattr(fx, "on_enemy_cast", None)
                if g:
                    g(en, self)
        if self.scratch.get("prefight"):
            self.impl.prefight(self.ctx)
        else:
            self.impl.cast(self.ctx)
        if f.e.mech is not None:
            from .mechanics import after_cast
            after_cast(self)
        self.scratch.pop("_bonus_spirit", None)
        self.scratch.pop("_bonus_duration", None)
        self.scratch.pop("_walk_in_at", None)

    def reset_cooldown(self, redraw=True):
        """Ready now (Refresher, Shadow Transformation...). With Mechanics.recast_timing the next cast waits a fresh real
        recast wait from now (redraw; RESET_REDRAW): real players don't jump on a reset ability any faster than on one
        whose cooldown ran out (their recast curves already hold the resets, as early recasts). The draw is among the
        waits of casts that came (never "not again this fight"); an ability already off cooldown keeps its wait."""
        e = self.f.e
        left = max(0.0, self.ready_at + self.recast_wait - e.t)   # an ability already off cooldown keeps its wait
        on_cd = e.t < self.ready_at
        self.charges = self.max_charges()
        self.ready_at = e.t
        self.recast_wait = 0.0
        self.next_charge = 0.0
        if redraw and RESET_REDRAW and e.length and e.mech is not None and getattr(e.mech, "recast_timing", False):
            if not on_cd:
                self.recast_wait = left
                return
            from .mechanics import recast_wait
            self.resets += 1
            self.recast_wait = recast_wait(self, n=f"reset{self.casts}.{self.resets}", finite=True)


RESET_REDRAW = True   # reset_cooldown draws a fresh recast wait (Mechanics.recast_timing)

_LOADED = False


def load_heroes():
    """Import every module in deadsim/heroes so their @register decorators run (once per process)."""
    global _LOADED
    if _LOADED:
        return
    _LOADED = True
    import importlib
    import pkgutil
    from . import heroes
    for m in pkgutil.iter_modules(heroes.__path__):
        importlib.import_module(f"{heroes.__name__}.{m.name}")
