"""Event-driven 1v1 fight engine.

Two Fighters shoot each other (and cast abilities / use items) until one dies or time runs out.
Chance-based things (accuracy, headshots, proc chances, deflects) default to *deterministic expected-value
accumulators*: a 57% accuracy gun lands exactly 57 of every 100 bullets, spread evenly. This keeps results
smooth and repeatable for build search. Pass `rng=random.Random(seed)` to sample instead (Monte Carlo).

Damage pipeline for one instance (see Engine.damage):
    raw (already includes attacker's weapon% / spirit scaling)
    * attacker outgoing multipliers (items, debuffs like Inhibitor / Silencer)
    * (1 + target damage-taken amps)            e.g. Napalm, Escalating Exposure (spirit only)
    * (1 - target resist after reductions)      resist stacking per build.combine_resist
    -> target immunities, damage-reduction procs, barrier, health, death prevention
    -> attacker lifesteal, then on-hit hooks for both sides.
"""
from __future__ import annotations

import heapq
import itertools
import math
from dataclasses import dataclass, field

from .build import Stats, combine_resist, stack_cdr
from .patterns import fight_start

INF = float("inf")
# Melee rotation (assumptions; the API has no light/heavy split): share of landed melees that are heavy, and how
# long each melee stops the gun.
HEAVY_SHARE = 0.3
MELEE_LIGHT_TIME = 0.6
MELEE_HEAVY_TIME = 1.1
# Below MELEE_MIN_RATE hits/s a melee event fires every 1/MELEE_MIN_RATE s with a fractional weight (expected
# damage), so rare meleers still melee within a short fight.
MELEE_MIN_RATE = 0.2
# items bought for melee: holders melee more often than the hero's average player (data/melee_items.json,
# Skill.melee_item_mult)
MELEE_ITEMS = frozenset({"upgrade_melee_charge", "upgrade_crushing_fists", "upgrade_boxing_glove",
                         "upgrade_lifestrike_gauntlets", "upgrade_spirit_snatch", "upgrade_acolytes_glove",
                         "upgrade_melee_rebuttal"})
# range spread (deadsim.mechanics range_drift): 7-point Gauss-Hermite nodes (weight e^-x^2) with weights normalized to
# sum 1; a standard normal value is sqrt(2) x
_GH = ((-2.6519613568, 0.000548268858), (-1.6735516288, 0.0307571239), (-0.8162878829, 0.240123178),
       (0.0, 0.457142857), (0.8162878829, 0.240123178), (1.6735516288, 0.0307571239), (2.6519613568, 0.000548268858))
REACH_P_FLOOR = 0.01    # waiting for drift to bring a far target in reach: tau / max(p, floor)
GUN_POLL = 0.1          # longest a locked gun sleeps before re-checking the lock


# ---------------------------------------------------------------------------------------------------
# Effects / modifiers
# ---------------------------------------------------------------------------------------------------
class Mods:
    """Timed modifiers on a fighter. key -> {tag: (value, expire)}; same tag refreshes/replaces."""

    __slots__ = ("d", "engine")

    def __init__(self, engine):
        self.d = {}
        self.engine = engine

    def add(self, key, value, duration, tag=None):
        now = self.engine.t
        tags = self.d.setdefault(key, {})
        tags[tag if tag is not None else object()] = (value, now + duration)

    def remove(self, key, tag):
        self.d.get(key, {}).pop(tag, None)

    def values(self, key):
        tags = self.d.get(key)
        if not tags:
            return []
        now = self.engine.t
        out = []
        dead = []
        for tg, (v, exp) in tags.items():
            if exp > now:
                out.append(v)
            else:
                dead.append(tg)
        for tg in dead:
            del tags[tg]
        return out

    def sum(self, key):
        v = self.values(key)
        return sum(v) if v else 0.0

    def active(self, key):
        return bool(self.values(key))

    def get(self, key, tag):
        x = self.d.get(key, {}).get(tag)
        if x and x[1] > self.engine.t:
            return x[0]
        return None


class Accum:
    """Deterministic Bernoulli: returns how many of n trials succeed so the long-run rate is exactly p."""

    __slots__ = ("x", "rng")

    def __init__(self, rng=None, phase=0.5):
        self.x = phase   # start half-way so a 50% event fires on the first trial, not the second
        self.rng = rng

    def take(self, p, n=1):
        if p <= 0 or n <= 0:
            return 0
        if self.rng is not None:
            return sum(1 for _ in range(n) if self.rng.random() < p)
        self.x += p * n
        k = int(self.x)
        self.x -= k
        return k


FIGHT_GAP = 60.0   # assumed seconds between hero fights (counterplay mode); items with shorter cooldowns are ready


def long_cooldowns_spent(f):
    for fx in f.items_fx:
        it = getattr(fx, "item", None)
        if it is None or it.activation == "passive" or not hasattr(fx, "cd"):
            continue
        c = fx.cd()
        if c > FIGHT_GAP and f.skill.fight_phase >= FIGHT_GAP / c:
            fx.ready_at = max(fx.ready_at, c - FIGHT_GAP)


@dataclass
class Skill:
    accuracy: float = 0.26      # fraction of bullets that hit the target hero (ranked median, data/skill_defaults.json)
    headshot: float = 0.157     # fraction of hits that are headshots (ranked median)
    spirit_accuracy: float = 1.0  # fraction of skillshot abilities that land
    # per-ability damage landing factor, keyed by ability name (see data/landing_rates.json): multiplies all
    # damage booked under that ability's name. Fitted from real damage shares, so it folds in misses, partial
    # AoE/DoT uptime and target movement that the hero file doesn't model.
    ability_landing: dict = field(default_factory=dict)
    # the same fitted with deadsim.mechanics on (data/landing_rates_mech.json); used instead when mechanics are on
    ability_landing_mech: dict = field(default_factory=dict)
    use_abilities: bool = True
    use_actives: bool = True
    melee: bool = False         # deprecated, use melee_rate
    # landed melee hits per second of fight (light and heavy, HEAVY_SHARE heavy). Fitted per hero from real
    # damage (data/melee_rates.json, loaded by accuracy.hero_default_skill); 0 = no melee.
    melee_rate: float = 0.0
    heavy_share: float = HEAVY_SHARE  # share of rotation melees that are heavy
    # multiplier on melee_rate by melee items in the build (0, 1, 2+ of MELEE_ITEMS), applied at fight start, since
    # players who buy melee items melee more (accuracy.melee_item_mults). None = melee_rate as is.
    melee_item_mult: tuple | None = None
    # follow an ability that sets up a free hit with a guaranteed heavy melee (Abrams: Shoulder Charge hit). These
    # come on top of melee_rate; the fitted rates already account for them.
    combo_melee: bool = True
    # seconds an enemy DoT (Decay etc.) runs before Dispel Magic cleanses it: about two 1 s ticks, as high-rank
    # players do (Tyler, Eternus). None = cleanse a DoT only below 50% health.
    dot_cleanse_delay: float | None = 1.5
    # share of enemy DoTs Dispel Magic is spent on at all (accuracy.dot_cleanse_share, fitted to real Decay damage
    # on Dispel holders); the rest run out. None = every one.
    dot_cleanse_share: float | None = None
    # the same for build-up DoTs (Afterburn, Toxic Bullets: re-applied by the enemy's gun), which real holders
    # cleanse far more often (accuracy.dot_cleanse_share_buildup). None = every one.
    dot_cleanse_share_buildup: float | None = None
    engage_margin: float = 5.0  # meters a player will close to land an ability that is just out of reach
    # meters beyond engage_margin a player walks in (shooting on the way) before casting a short-range ability; the
    # walk costs gap / move speed seconds of delay. Range items only shorten that walk, so they never decide
    # whether an ability is used at all (Mystic Expansion on Mina's Rake at her 16.3 m median distance).
    walk_in: float = 5.0
    # Used only with deadsim.mechanics on (see that module for the fits):
    parry_rate: float = 0.15       # share of incoming heavy melees parried
    # Counterspell: share of enemy aimed non-ultimate casts a spell parry is timed against (hero_default_skill sets
    # the real-data fit, accuracy.spell_parry_rates: 0)
    spell_parry_rate: float = 0.05
    # the same for enemy ultimates (telegraphed, the cast players buy Counterspell for); None = spell_parry_rate
    spell_parry_rate_ult: float | None = None
    # share of trigger pulls spent on a living enemy summon; None = the per-kind share fitted to Phantom+ replays
    # (data/summon_targeting.json)
    summon_focus: float | None = None
    flee_hp: float = 0.15          # run when below this health share and losing (fit, deadsim.mechanics)
    # Counterplay (off by default; accuracy.hero_default_skill(counterplay=True) turns it on):
    # seconds THIS fighter stays inside an avoidable ground zone (Alchemical Fire) before walking out.
    # None = stands in it for the whole duration, like a training dummy.
    zone_exit_s: float | None = None
    # where this fight falls in the match (0-1, None = every item cooldown ready, as before). An active item whose
    # cooldown C is longer than FIGHT_GAP was spent in an earlier fight unless phase < FIGHT_GAP / C, so over a pool
    # of fights with spread phases a Refresher (300 s) is ready in ~20% of them instead of all.
    fight_phase: float | None = None
    # per-item damage factor keyed by item name, fitted from real damage (data/item_landing.json, factors < 1
    # only): procs spent on creeps, charges used outside fights. Multiplies damage booked under that item.
    item_landing: dict = field(default_factory=dict)
    # per-hero fight pattern (data/fight_patterns.json, deadsim.patterns): combo cast order, setup before the
    # ultimate, abilities used before the fight (Mo & Krill arrive under Burrow). False = cast in slot order.
    fight_pattern: bool = True


@dataclass
class Hit:
    """Info passed to on-hit hooks."""
    kind: str            # bullet | spirit | melee | pure
    source: str
    amount: float        # final damage dealt to health+barrier
    raw: float
    is_ability: bool = False
    ability: object = None
    headshots: int = 0
    hits: int = 0        # bullets that hit (for bullet instances)
    is_dot: bool = False
    is_item: bool = False
    is_ult: bool = False


# ---------------------------------------------------------------------------------------------------
# Fighter
# ---------------------------------------------------------------------------------------------------
class Fighter:
    def __init__(self, engine, name, stats: Stats, skill: Skill, build_opts=None):
        self.e = engine
        self.name = name
        self.st = stats
        self.skill = skill
        self.opts = build_opts or {}
        self.max_hp_base = stats.max_health
        self.hp = stats.max_health
        self.mods = Mods(engine)
        self.barriers = []          # [amount, expire]
        self.enemy: Fighter = None
        self.alive = True
        self.death_time = None
        self.dmg_out = {}           # source -> damage dealt
        self.dmg_in = {}
        self.healed = 0.0
        self.items_fx = []
        self.abilities = []         # AbilityState
        self.plan = None            # deadsim.patterns.Plan (hero fight pattern), None = slot order
        self.cast_order = None      # abilities in cast priority (plan.order)
        self.clip = stats.clip
        self.bonus_ammo = 0
        self.reload_until = 0.0
        self.shooting_since = 0.0   # start of continuous fire (Intensifying Magazine)
        self.hit_acc = Accum(engine.rng, 0.5)
        self.head_acc = Accum(engine.rng, 0.5)
        self.misc_acc = {}
        self.gun_locked_until = 0.0
        self.stat_hooks = []        # callables (fighter) -> dict of dynamic modifiers
        self.counters = {}          # free-form per-fight state for items/abilities
        self.shots_fired = 0
        self.bullets_hit = 0
        self.headshots_hit = 0

    # ---- helpers -----------------------------------------------------------------------------------
    def acc(self, key, phase=0.5):
        a = self.misc_acc.get(key)
        if a is None:
            a = self.misc_acc[key] = Accum(self.e.rng, phase)
        return a

    def mark_debuff(self, key, tag):
        """Remember an enemy-applied timed modifier so a cleanse (Dispel Magic) can remove it."""
        self.counters.setdefault("debuffs", set()).add((key, tag))

    def afflicted(self, min_left=0.0, keys=None):
        """True if an enemy DoT has at least min_left seconds to run, or an enemy debuff (of `keys`, if given)
        is active."""
        t = self.e.t
        if any(end - t >= min_left for end in self.counters.get("dot_until", {}).values()):
            return True
        return any(self.mods.get(k, tg) is not None for k, tg in self.counters.get("debuffs", ())
                   if keys is None or k in keys)

    def buildup_dot(self, min_left=0.0):
        """True if a running enemy DoT with at least min_left seconds left is a build-up DoT (re-applied by the
        enemy's gun: Afterburn, Toxic Bullets), which Dispel holders cleanse far more often than others."""
        t = self.e.t
        bu = self.counters.get("buildup_dots", ())
        return any(end - t >= min_left for tag, end in self.counters.get("dot_until", {}).items() if tag in bu)

    def dispel(self):
        """Purge enemy debuffs and DoTs (Engine.dot ticks stop; ad-hoc item DoTs check dispel_epoch)."""
        for k, tg in self.counters.pop("debuffs", set()):
            self.mods.remove(k, tg)
        for k in [k for k in self.counters if isinstance(k, tuple) and k[0] == "dot"]:
            del self.counters[k]
        self.counters.pop("dot_until", None)
        self.counters.pop("buildup_dots", None)
        self.counters["dispel_epoch"] = self.counters.get("dispel_epoch", 0) + 1

    @property
    def max_hp(self):
        return max(1.0, self.max_hp_base + self.mods.sum("max_health"))

    @property
    def hp_frac(self):
        return self.hp / self.max_hp

    def dyn(self, key):
        """Dynamic (conditional) modifiers from items, e.g. +18% weapon damage while above 65% health."""
        tot = 0.0
        for h in self.stat_hooks:
            v = h(self).get(key)
            if v:
                tot += v
        return tot

    def stat(self, key):
        return self.mods.sum(key) + self.dyn(key)

    # ---- derived live stats --------------------------------------------------------------------------
    def spirit_power(self, extra=0.0):
        return self.st.spirit_power + self.stat("spirit_power") + extra

    def weapon_pct(self):
        return self.st.weapon_pct + self.stat("weapon_pct")

    def fire_rate(self):
        return self.st.fire_rate_pct + self.stat("fire_rate") - self.stat("fire_rate_slow")

    def bullet_resists(self):
        extra = self.mods.values("bullet_resist") + [v for h in self.stat_hooks for k, v in h(self).items() if k == "bullet_resist" and v]
        return list(self.st.bullet_resist) + list(extra)

    def spirit_resists(self):
        extra = self.mods.values("spirit_resist") + [v for h in self.stat_hooks for k, v in h(self).items() if k == "spirit_resist" and v]
        return list(self.st.spirit_resist) + list(extra)

    def can_shoot(self):
        t = self.e.t
        return self.alive and not (self.mods.active("stun") or self.mods.active("disarm")) and t >= self.gun_locked_until

    def can_cast(self):
        return self.alive and not (self.mods.active("stun") or self.mods.active("silence"))

    def can_use_items(self):
        return self.alive and not (self.mods.active("stun") or self.mods.active("item_silence"))

    # ---- healing / barrier -----------------------------------------------------------------------
    def heal(self, amount, source="heal", kind="regen"):
        if not self.alive or amount <= 0:
            return 0.0
        # regen is amped by regen amp; heals the fighter casts on itself (abilities, lifesteal, items) by outgoing
        # healing amp (Healing Booster). healbane etc. are negative heal_received.
        amp = self.st.heal_amp if kind == "regen" else self.st.heal_amp_cast
        mult = 1.0 + amp + self.stat("heal_received")
        amt = min(self.max_hp - self.hp, amount * max(0.0, mult))
        self.hp += amt
        self.healed += amt
        return amt

    def add_barrier(self, amount, duration):
        self.barriers.append([amount, self.e.t + duration])

    def barrier_total(self):
        now = self.e.t
        self.barriers = [b for b in self.barriers if b[1] > now and b[0] > 0]
        return sum(b[0] for b in self.barriers)


def kill_hooks(killer, dead):
    """killer's on-kill item effects (Healbane's heal). Also called when an immortal target refills instead of
    dying (survival / overall score), which counts as a kill there."""
    if killer is None or not killer.alive:
        return
    for fx in killer.items_fx:
        f = getattr(fx, "on_kill", None)
        if f:
            f(killer, dead)


# ---------------------------------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------------------------------
@dataclass
class FightResult:
    winner: str | None
    time: float
    a_hp: float
    b_hp: float
    a_dmg: dict
    b_dmg: dict
    a_name: str = "A"
    b_name: str = "B"
    log: list = field(default_factory=list)
    escaped: str | None = None     # name of the fighter who ran out of the fight (mechanics.movement)
    a_splash: dict = field(default_factory=dict)   # damage to other nearby enemy heroes (mechanics.extra_targets)
    b_splash: dict = field(default_factory=dict)
    a_summon: dict = field(default_factory=dict)   # damage to enemy summons (mechanics.summons)
    b_summon: dict = field(default_factory=dict)
    # per summon kind, [gun, other]: damage to the enemy's summons, and damage taken while one's own summons were out
    a_summon_kind: dict = field(default_factory=dict)
    b_summon_kind: dict = field(default_factory=dict)
    a_hit_while_summon: dict = field(default_factory=dict)
    b_hit_while_summon: dict = field(default_factory=dict)
    a_summons_out: dict = field(default_factory=dict)   # kind -> [summons spawned, killed by the enemy]
    b_summons_out: dict = field(default_factory=dict)

    def summary(self):
        def top(d):
            return ", ".join(f"{k} {v:.0f}" for k, v in sorted(d.items(), key=lambda x: -x[1])[:6])
        return (f"winner={self.winner} t={self.time:.2f}s  {self.a_name} hp={self.a_hp:.0f} [{top(self.a_dmg)}]  "
                f"{self.b_name} hp={self.b_hp:.0f} [{top(self.b_dmg)}]")


_UNSET = object()


class Engine:
    def __init__(self, distance=15.0, max_time=30.0, rng=None, log=False, mech=_UNSET):
        self.t = 0.0
        self.q = []
        self.seq = itertools.count()
        self.distance = distance       # meters between fighters
        self.max_time = max_time
        self.rng = rng
        self.logging = log
        self.log = []
        self.fighters = []
        self.over = False
        if mech is _UNSET:
            from . import mechanics
            mech = mechanics.DEFAULT
        self.mech = mech               # deadsim.mechanics.Mechanics or None (earlier model)
        self.escaped = None
        self.mover = None
        # range spread: real fights don't hold one distance. With mechanics range_drift the distance is lognormal
        # around self.distance (log sd `spread`, drifting with time constant `spread_tau`), and distance effects are
        # taken as expectations over it (p_within, spread_mean, reach_ready), so results stay deterministic and an
        # item's value doesn't hinge on one random path.
        self.spread, self.spread_tau = 0.0, 2.0
        self._fall, self._d0 = {}, distance
        if mech is not None and getattr(mech, "range_drift", False):
            from .mechanics import drift_params
            self.spread, self.spread_tau = drift_params()

    # ---- range spread -------------------------------------------------------------------------------
    def p_within(self, r):
        """Share of fight time the target is within r meters."""
        d = self.distance
        if self.spread <= 0:
            return 1.0 if d <= r else 0.0
        from .mechanics import DRIFT_MAX, DRIFT_MIN
        if r >= DRIFT_MAX:
            return 1.0
        if r < DRIFT_MIN:
            return 0.0
        return 0.5 * (1.0 + math.erf(math.log(r / d) / (self.spread * math.sqrt(2.0))))

    def spread_mean(self, fn, d=None):
        """fn(distance) averaged over the fight's distance spread (around d, default the current distance)."""
        d = self.distance if d is None else d
        if self.spread <= 0:
            return fn(d)
        from .mechanics import DRIFT_MAX, DRIFT_MIN
        k = self.spread * math.sqrt(2.0)
        return sum(w * fn(min(DRIFT_MAX, max(DRIFT_MIN, d * math.exp(k * x)))) for x, w in _GH)

    def reach_ready(self, state, reach, f, walk_in=0.0, mean_field=False):
        """Gate for a cast or active that needs the target within `reach` m. Without spread: now if in reach, after
        gap / move speed if the gap is up to walk_in (the caster walks in), else never. With spread: after the
        expected wait (walking in when the target is in the walk band, waiting for the drift to bring it back when it
        is further), which is smooth in reach, so range items shorten waits instead of switching casts on.
        The timer (state["_walk_in_at"]) starts the first time the cast is wanted and clears on cast.
        mean_field (abilities): with spread, cast now and leave the expected wait in state["_reach_delay"]; the
        cast turns it into a damage factor cooldown / (cooldown + wait) (AbilityState.cast). A real delay would make
        a 30 s fight gain or lose a whole cast from a fraction of a second, so item values would jump."""
        d = self.distance
        st = f.st
        speed = max(1.0, st.hero.base.get("max_move_speed", 7.0)
                    + st.extra.get("MODIFIER_VALUE_MOVEMENT_SPEED_MAX", 0) + f.stat("move_speed"))
        if self.spread <= 0:
            gap = d - reach
            if gap <= 0:
                state.pop("_walk_in_at", None)   # in reach: a later walk-in starts fresh
                return True
            if gap > walk_in:
                state.pop("_walk_in_at", None)
                return False
            delay = gap / speed
        else:
            p_now, p_walk = self.p_within(reach), self.p_within(reach + walk_in)
            delay = ((p_walk - p_now) * walk_in / 2 / speed
                     + (1.0 - p_walk) * (self.spread_tau / max(p_walk, REACH_P_FLOOR) + walk_in / speed))
            if mean_field:
                state["_reach_delay"] = delay
                return True
            if delay <= 1e-9:
                state.pop("_walk_in_at", None)
                return True
        t0 = state.setdefault("_walk_in_at", self.t)
        return self.t - t0 >= delay

    # ---- scheduling -------------------------------------------------------------------------------
    def at(self, time, fn, *args):
        heapq.heappush(self.q, (time, next(self.seq), fn, args))

    def after(self, delay, fn, *args):
        self.at(self.t + max(0.0, delay), fn, *args)

    def note(self, msg):
        if self.logging:
            self.log.append(f"{self.t:6.2f} {msg}")

    # ---- damage -------------------------------------------------------------------------------------
    def damage(self, src: Fighter, dst: Fighter, raw: float, kind: str, source: str, *,
               ignore_resist=False, is_ability=False, ability=None, is_dot=False, is_item=False,
               headshots=0, hits=0, procs=True, is_ult=False, nonlethal=False, pure=False, landed=False):
        """pure=True: raw is already final damage (e.g. Focus Lens re-dealing stored damage), so no outgoing or
        target amps, no resists and no target-side reducers (all already counted in raw). The realistic-mode item
        landing factor still applies on purpose: for Focus Lens it is the real/sim ratio of the item's own damage,
        i.e. how much less real players fit into the silence window. landed=True: the ability already applied its
        landing factor some other way (Bullet Dance shortens its channel), so it is not applied again here."""
        if self.over or not dst.alive or raw <= 0:
            return 0.0
        amt = raw if pure else raw * src.st.outgoing_mult * (1.0 - src.stat("outgoing_penalty")) * (1.0 + src.stat("damage_amp"))
        if is_ability and src.skill.ability_landing and not landed:
            # a sub-source of an ability ("Setup Bishop squares", "Ira Domini (blessed)") uses its ability's factor,
            # as landing_rates.py fits one factor per ability over all of its sources; an ability can also name the
            # factor it uses (Sinclair's copied ultimate uses Audience Participation's)
            fac = src.skill.ability_landing.get(source)
            if fac is None and ability is not None:
                fac = src.skill.ability_landing.get(getattr(ability.ab, "landing_key", None) or ability.ab.name)
            if fac is not None:
                amt *= fac
        if is_ability and ability is not None:
            amt *= ability.scratch.get("_avail", 1.0)   # expected wait for the target to be in reach (spread)
        if is_item and src.skill.item_landing:
            amt *= src.skill.item_landing.get(source, 1.0)
        if pure:
            pass
        elif kind == "spirit":
            amt *= (1.0 - src.stat("spirit_outgoing_penalty"))
            amt *= (1.0 + dst.stat("spirit_amp_taken"))
        elif kind == "bullet":
            amt *= (1.0 + dst.stat("bullet_amp_taken"))
        if not pure:
            amt *= (1.0 + dst.stat("damage_taken_amp"))
        if not (ignore_resist or pure):
            if kind == "bullet":
                res = combine_resist(dst.bullet_resists(), list(src.st.bullet_shred) + dst.mods.values("bullet_shred"))
                amt *= (1.0 - res)
            elif kind == "spirit":
                res = combine_resist(dst.spirit_resists(), list(src.st.spirit_shred) + dst.mods.values("spirit_shred"))
                amt *= (1.0 - res)
            elif kind == "melee":
                res = combine_resist(dst.st.melee_resist + dst.mods.values("melee_resist"), ())
                amt *= (1.0 - res)
        if dst.mods.active("invulnerable") or (kind == "bullet" and dst.mods.active("bullet_immune")):
            return 0.0
        if self.mech is not None and (is_ability or is_item) and "spell_parry" in dst.counters:
            from .mechanics import spell_blocked
            if spell_blocked(self, src, dst, ability):
                return 0.0
        # target-side reductions (Spellbreaker, Plated Armor, ...)
        for fx in () if pure else dst.items_fx:
            f = getattr(fx, "reduce_incoming", None)
            if f:
                amt = f(dst, src, amt, kind, is_dot)
                if amt <= 0:
                    return 0.0
        hit = Hit(kind, source, 0.0, raw, is_ability, ability, headshots, hits, is_dot, is_item, is_ult)
        # barrier then health
        left = amt
        for b in dst.barriers:
            if b[1] > self.t and b[0] > 0 and left > 0:
                take = min(b[0], left)
                b[0] -= take
                left -= take
        if nonlethal:
            left = min(left, max(0.0, dst.hp - 1.0))
        dst.hp -= left
        hit.amount = amt
        src.dmg_out[source] = src.dmg_out.get(source, 0.0) + amt
        dst.dmg_in[source] = dst.dmg_in.get(source, 0.0) + amt
        if "summons" in dst.counters and amt > 0:
            from .mechanics import note_hit_while_summoned
            note_hit_while_summoned(src, dst, amt, source)
        if dst.hp <= 0 and dst.mods.active("death_immune"):
            dst.hp = 1.0
        if dst.hp <= 0:
            saved = False
            for fx in dst.items_fx:
                f = getattr(fx, "on_lethal", None)
                if f and f(dst, src):
                    saved = True
                    break
            if not saved:
                dst.hp = 0.0
                dst.alive = False
                dst.death_time = self.t
                self.note(f"{dst.name} dies to {source}")
                kill_hooks(src, dst)
                self.on_death(dst, src)
        # lifesteal
        if src.alive and amt > 0:
            if kind == "bullet":
                ls = src.st.bullet_lifesteal + src.stat("bullet_lifesteal")
                if ls:
                    src.heal(amt * ls, "bullet_lifesteal", "lifesteal")
            elif kind == "spirit":
                ls = src.st.spirit_lifesteal + src.stat("spirit_lifesteal")
                if ls:
                    src.heal(amt * ls, "spirit_lifesteal", "lifesteal")
        # hooks
        if procs:
            for fx in src.items_fx:
                f = getattr(fx, "on_damage_dealt", None)
                if f:
                    f(src, dst, hit)
            for ab in src.abilities:
                f = getattr(ab.impl, "on_damage_dealt", None) if ab.unlocked else None
                if f:
                    f(ab.ctx, dst, hit)
        for ab in src.abilities:   # every hit, procs or not (DoT ticks wake a Sleep Dagger target)
            f = getattr(ab.impl, "on_any_damage_dealt", None) if ab.unlocked else None
            if f:
                f(ab.ctx, dst, hit)
        for fx in dst.items_fx:
            f = getattr(fx, "on_damage_taken", None)
            if f:
                f(dst, src, hit)
        for ab in dst.abilities:
            f = getattr(ab.impl, "on_damage_taken", None) if ab.unlocked else None
            if f:
                f(ab.ctx, src, hit)
        return amt

    def on_death(self, dead, killer):
        """A fighter just died. 1v1: the fight is over (team.TeamEngine retargets instead)."""
        self.over = True

    # ---- DoT --------------------------------------------------------------------------------------
    def dot(self, src, dst, dps, duration, source, kind="spirit", tick=0.5, tag=None, **kw):
        """Damage over time; refreshing with the same tag replaces the running DoT."""
        if duration <= 0 or dps <= 0:
            return
        guard = kw.pop("guard", None)   # a summon: its DoT stops when it dies
        buildup = kw.pop("buildup", False)   # re-applied by the enemy's gun (Fighter.buildup_dot)
        if self.mech is not None and (kw.get("is_ability") or kw.get("is_item")) and "spell_parry" in dst.counters:
            from .mechanics import spell_blocked
            if spell_blocked(self, src, dst, kw.get("ability")):
                return
        tag = tag or source
        key = ("dot", tag)
        token = object()
        dst.counters[key] = token
        dst.counters.setdefault("dot_until", {})[tag] = self.t + duration
        if buildup:
            dst.counters.setdefault("buildup_dots", set()).add(tag)
        n = max(1, int(round(duration / tick)))
        per = dps * duration / n

        def tick_fn(i):
            if dst.counters.get(key) is not token or not dst.alive or (
                    guard is not None and not (guard.alive and guard.until > self.t)):
                return
            self.damage(src, dst, per, kind, source, is_dot=True, **kw)
            if i + 1 < n:
                self.after(tick, tick_fn, i + 1)
        self.after(tick, tick_fn, 0)

    # ---- gun ----------------------------------------------------------------------------------------
    def bullet_damage(self, f: Fighter, extra_pct=0.0):
        st = f.st
        d = self.distance
        pct = f.weapon_pct() + extra_pct
        if self.spread <= 0:
            return st.bullet_damage * (1.0 + pct) * st.falloff(d), st.crit_mult(d)
        d = self._dkey()
        key = (id(st), d)
        fc = self._fall.get(key)
        if fc is None:   # E[falloff] and E[falloff x crit] over the spread (headshots get the joint one)
            fall = self.spread_mean(st.falloff, d)
            fc = self._fall[key] = (fall, self.spread_mean(lambda x: st.falloff(x) * st.crit_mult(x), d) / max(fall, 1e-9))
        for fx in f.items_fx:   # close/long range bonuses pay where falloff is high/low, not at its average
            g = getattr(fx, "range_band", None)
            if g:
                r, bonus, close = g()
                pct += bonus * self.band_corr(st, r, close, d)
        return st.bullet_damage * (1.0 + pct) * fc[0], fc[1]

    def _dkey(self):
        """Distance for the spread caches: exact at the fight's starting distance (the usual fight), else 0.25 m
        buckets, so a chase that moves the distance every step keeps the caches small."""
        d = self.distance
        return d if d == self._d0 else round(d * 4) / 4

    def band_corr(self, st, r, close, d=None):
        """E[falloff x in band] / E[falloff] - P(in band), band = within r (close) or beyond r: added to the p x bonus a
        close/long range item puts in weapon_pct, it turns E[falloff] x (1 + p x bonus) into the joint expectation."""
        d = self._dkey() if d is None else d
        key = (id(st), d, r, close)
        c = self._fall.get(key)
        if c is None:
            from .mechanics import DRIFT_MAX, DRIFT_MIN
            num = den = pin = wsum = 0.0
            for i in range(161):   # fine grid: the band edge is a step, too sharp for the 7 Gauss-Hermite nodes
                z = -4.0 + i * 0.05
                w = math.exp(-0.5 * z * z)
                x = min(DRIFT_MAX, max(DRIFT_MIN, d * math.exp(self.spread * z)))
                inb = (x <= r) if close else (x >= r)
                fl = st.falloff(x)
                wsum += w
                den += w * fl
                if inb:
                    num += w * fl
                    pin += w
            c = self._fall[key] = num / max(den, 1e-12) - pin / wsum
        return c

    def gun_tick(self, f: Fighter):
        if self.over or not f.alive:
            return
        t = self.t
        st = f.st
        if not f.can_shoot():
            # wake at least every GUN_POLL s: a channel cut short (stun, target dead) pulls gun_locked_until back
            nxt = max(t + 0.05, min(f.gun_locked_until, t + GUN_POLL))
            f.shooting_since = None
            self.at(nxt, self.gun_tick, f)
            return
        if f.clip + f.bonus_ammo <= 0:
            if f.reload_until <= t:
                rt = st.reload_time * max(0.1, 1.0 + f.stat("reload_mult"))
                f.reload_until = t + rt
                f.shooting_since = None
                for fx in f.items_fx:
                    g = getattr(fx, "on_reload", None)
                    if g:
                        g(f)
                self.at(f.reload_until, self.finish_reload, f)
            return
        if f.shooting_since is None:
            f.shooting_since = t
        self.fire(f)
        cycle = st.cycle_time
        if st.spin_cycle:
            # spin fraction rises while firing, decays while not (reloads, locks); cycle time interpolates
            last = getattr(f, "spin_t", t)
            gap = max(0.0, t - last - cycle)
            spin = max(0.0, getattr(f, "spin", 0.0) - gap * st.spin_decay_rate)
            spin = min(1.0, spin + (t - last - gap) * st.spin_up_rate)
            f.spin, f.spin_t = spin, t
            cycle = st.cycle_time + (st.spin_cycle - st.cycle_time) * spin
        if st.burst_count > 1:
            cycle += st.burst_count * st.burst_interval
        interval = cycle / max(0.05, 1.0 + f.fire_rate())
        self.after(interval, self.gun_tick, f)

    def finish_reload(self, f):
        if not f.alive or self.over:
            return
        f.clip = f.st.clip
        self.after(0.0, self.gun_tick, f)

    def fire(self, f: Fighter):
        """One trigger pull: burst_count shots of `pellets` bullets each."""
        e = f.enemy
        st = f.st
        if f.bonus_ammo > 0:
            f.bonus_ammo -= 1
        else:
            f.clip -= 1
        f.shots_fired += 1
        ctx = {"extra_pct": 0.0, "bonus_flat_head": 0.0, "pellet_mult": 1.0, "ignore_resist_frac": 0.0,
               "bonus_spirit": [], "dmg_mult": 1.0}
        for fx in f.items_fx:
            g = getattr(fx, "on_shot", None)
            if g:
                g(f, ctx)
        for ab in f.abilities:
            g = getattr(ab.impl, "on_shot", None) if ab.unlocked else None
            if g:
                g(ab.ctx, ctx)
        n_bullets = int(st.pellets * st.burst_count * ctx["pellet_mult"])
        if self.mech is not None and self.mech.summons and "summons" in e.counters:
            from .mechanics import pick_summon, shoot_summon
            s = pick_summon(f, e)
            if s is not None:
                shoot_summon(self, f, s, n_bullets)
                return
        p_hit = f.skill.accuracy * (1.0 - e.stat("evasion"))
        hits = f.hit_acc.take(p_hit, n_bullets)
        if hits <= 0:
            return
        heads = f.head_acc.take(f.skill.headshot, hits)
        f.bullets_hit += hits
        f.headshots_hit += heads
        per, crit = self.bullet_damage(f, ctx["extra_pct"])
        per *= ctx["dmg_mult"]
        f.counters["bullet_per"] = per
        f.counters["_last_hits"] = hits
        crit_eff = 1.0 + (crit - 1.0) * e.st.crit_received_scale * (1.0 + e.stat("crit_taken"))
        raw = per * (hits - heads) + per * crit_eff * heads + ctx["bonus_flat_head"] * min(heads, 1)
        frac_ign = ctx["ignore_resist_frac"]
        if frac_ign > 0:
            ign_hits = f.acc("armor_piercer").take(frac_ign, hits)
            if ign_hits:
                share = ign_hits / hits
                self.damage(f, e, raw * share, "bullet", "gun", ignore_resist=True, headshots=0, hits=ign_hits, procs=False)
                raw *= (1 - share)
        self.damage(f, e, raw, "bullet", "gun", headshots=heads, hits=hits)
        for kind_src in ctx["bonus_spirit"]:
            amount, name = kind_src
            self.damage(f, e, amount * hits, "spirit", name, is_item=True)

    # ---- run ----------------------------------------------------------------------------------------
    def run(self, a: Fighter, b: Fighter, one_way=False):
        a.enemy, b.enemy = b, a
        self.fighters = [a, b]
        for f in (a, b):
            for fx in f.items_fx:
                g = getattr(fx, "on_start", None)
                if g:
                    g(f)
            if f.skill.fight_phase is not None:
                long_cooldowns_spent(f)
            for ab in f.abilities:
                ab.start()
        for f in (a, b):
            fight_start(f)
        self.at(0.0, self.gun_tick, a)
        if not one_way:
            self.at(0.0, self.gun_tick, b)
        self.at(0.0, self.think, a)
        if not one_way:
            self.at(0.0, self.think, b)
        for f in ((a,) if one_way else (a, b)):
            if f.skill.melee_rate > 0:
                self.at(0.5 / max(f.skill.melee_rate, MELEE_MIN_RATE), self.melee_tick, f)
        self.at(0.0, self.regen_tick)
        if self.mech is not None and self.mech.movement:
            from .mechanics import Mover
            self.mover = Mover(self)
        while self.q and not self.over:
            t, _, fn, args = heapq.heappop(self.q)
            if t > self.max_time:
                self.t = self.max_time
                break
            self.t = t
            fn(*args)
        winner = None
        if not a.alive and b.alive:
            winner = b.name
        elif not b.alive and a.alive:
            winner = a.name
        r = FightResult(winner, self.t, a.hp, b.hp, a.dmg_out, b.dmg_out, a.name, b.name, self.log)
        if self.mech is not None:
            r.escaped = self.escaped
            r.a_splash, r.b_splash = a.counters.get("splash", {}), b.counters.get("splash", {})
            r.a_summon, r.b_summon = a.counters.get("summon_dmg", {}), b.counters.get("summon_dmg", {})
            r.a_summon_kind, r.b_summon_kind = a.counters.get("summon_dmg_kind", {}), b.counters.get("summon_dmg_kind", {})
            r.a_hit_while_summon = a.counters.get("hit_while_summon", {})
            r.b_hit_while_summon = b.counters.get("hit_while_summon", {})
            for f, out in ((a, r.a_summons_out), (b, r.b_summons_out)):
                for x in f.counters.get("summons", ()):
                    row = out.setdefault(x.kind, [0, 0])
                    row[0] += 1
                    row[1] += not x.alive
        return r

    # ---- melee ------------------------------------------------------------------------------------
    def melee_tick(self, f: Fighter):
        """One landed melee hit every 1 / melee_rate seconds (weighted events below MELEE_MIN_RATE). A light melee
        takes MELEE_LIGHT_TIME and a heavy MELEE_HEAVY_TIME of not shooting. Postponed while stunned or busy
        (gun locked by a cast or channel)."""
        if self.over or not f.alive or f.skill.melee_rate <= 0:
            return
        t = self.t
        if f.mods.active("stun") or t < f.gun_locked_until:
            self.at(max(t + 0.1, f.gun_locked_until), self.melee_tick, f)
            return
        heavy = f.acc("melee_heavy").take(f.skill.heavy_share, 1) > 0
        rate = f.skill.melee_rate
        if self.mech is not None and self.mech.parry:
            # parried heavies don't land: swing more often so landed melee stays at the fitted rate
            rate /= max(0.5, 1.0 - f.enemy.skill.parry_rate * f.skill.heavy_share)
        interval = 1.0 / max(rate, MELEE_MIN_RATE)
        if self.mover is None or f.counters.get("fleeing") is not True and self.distance <= self.mover.start + \
                self.mover.melee_reach(f, heavy):
            self.melee_hit(f, heavy, min(1.0, rate * interval))
        self.after(interval, self.melee_tick, f)

    def melee_hit(self, f: Fighter, heavy: bool, w: float = 1.0):
        """Land one basic melee (weight w = expected fraction of a hit) and stop the gun for its swing."""
        t = self.t
        st = f.st
        light = st.hero.base.get("light_melee_damage", 0.0)
        heavy_base = st.hero.base.get("heavy_melee_damage", 0.0) or 2.32 * light
        grow = st.boons * st.hero.per_boon.get("MODIFIER_VALUE_BASE_MELEE_DAMAGE_FROM_LEVEL", 0.0)
        if heavy:
            raw = heavy_base + grow * (heavy_base / light if light else 1.0)
        else:
            raw = light + grow
        raw *= (1.0 + st.melee_pct + f.stat("melee_pct")) * w
        f.counters["melee_heavy"] = heavy
        f.counters["melee_weight"] = w
        f.gun_locked_until = max(f.gun_locked_until, t + (MELEE_HEAVY_TIME if heavy else MELEE_LIGHT_TIME) * w)
        if heavy and self.mech is not None and self.mech.parry:
            from .mechanics import parry_check
            raw *= parry_check(self, f, f.enemy, raw, w)
            if raw <= 0:
                return
        self.damage(f, f.enemy, raw, "melee", "melee", hits=1)

    def regen_tick(self):
        if self.over:
            return
        for f in self.fighters:
            if f.alive:
                r = f.st.health_regen + f.stat("regen")
                if r > 0:
                    f.heal(r * 0.5, "regen")
                drain = f.stat("health_drain")
                if drain > 0:
                    f.hp = max(1.0, f.hp - drain * 0.5)
        self.after(0.5, self.regen_tick)

    def think(self, f: Fighter):
        """Ability / active item decisions, re-evaluated every 0.1 s."""
        if self.over or not f.alive:
            return
        if f.skill.use_abilities and f.can_cast():
            for ab in f.cast_order or f.abilities:
                if ab.try_cast():
                    break   # one cast per think step
        if f.skill.use_actives and f.can_use_items():
            for fx in f.items_fx:
                g = getattr(fx, "try_active", None)
                if g and g(f):
                    break
        self.after(0.1, self.think, f)
