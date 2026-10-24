"""Combat mechanics (added 2026-10-15, on by default since 2026-10-16): parry, enemy summons that can be shot, other enemies near the target
(multi-target items), and movement (escape and chase, slows, dashes, mobility items).

An Engine built without a mechanics value uses DEFAULT (Mechanics(): all on, no extra nearby enemies):

    from deadsim.mechanics import Mechanics
    duel(a, b)                                              # parry, summons and movement on
    duel(a, b, mechanics=None)                              # the earlier model
    duel(a, b, mechanics=Mechanics(movement=False))
    duel(a, b, mechanics=Mechanics(extra_targets=1.0))      # a team fight with one more enemy hero next to the target
    import deadsim.mechanics; deadsim.mechanics.DEFAULT = None   # off for every Engine built without one

time_to_kill's dummy never runs, parries or times Counterspell; survival/survival.py turns movement off (an
escape would count as surviving).

Settings fitted to real ranked matches (validation/README.md, "New mechanics"):
- Parry: Skill.parry_rate = share of incoming heavy melees the defender parries (0.15: 5% of all hero melees, from
  team parry counts vs enemy melee hits). A parry cancels the melee and stuns the attacker for ParriedStunTime
  (2.75 s), during which he takes VictimDamageTakenScale (25%) more damage. Light melees are not parried
  (assumption). With parry on, the melee rotation runs 1 / (1 - parry_rate x heavy_share) faster so landed melee
  damage stays at the fitted rate. Missed parries (as common as successes in real games) cost nothing here.
- Counterspell: when the enemy casts an aimed ability (skillshot / target / aoe) and Counterspell is ready, the
  holder times a spell parry with Skill.spell_parry_rate; for SpellParryDuration it blocks the damage, DoTs and
  debuffs of that cast (and of any other enemy ability or item hit). Real holders' ability damage taken drops ~0-3%
  after buying it (same-player before/after vs teammates), so the default is low.
- Summons (Mechanics.summons): McGinnis turrets and Graves' zombies, ghouls, Deadheads and gravestone have health
  (from the data, + boons) and the enemy spends a share of its trigger pulls on each living kind, at acc_mult x its
  hero accuracy. Shares and accuracy multipliers per kind are in data/summon_targeting.json: the shares are fitted
  so the sim's share of enemy gun damage that hits summons instead of the owner matches Phantom+ replays
  (scripts/summons/). Skill.summon_focus overrides every kind's share. Non-gun damage the owner takes (area
  abilities, items, melee) also hits every living summon: x its kind's splash share, fitted the same way (in the replays
  60-70% of what enemies deal to zombies and turrets is not gun damage). A kind with break_p (the gravestone) is
  broken outright by the enemy break_s after it lands with that probability (real share of gravestones that took
  hero damage and were destroyed by a hero; real median time to break). A dead summon stops attacking. Damage to
  summons is not hero damage (`FightResult.*_summon`). A summon lives at most life_other_s (real median life of
  summons no hero killed). Every other hero summon (Sinclair's Assistant, Grey Talon's
  owl, Solomon's pieces, Rat King's rats and banner, Medicinal Specter) has no health in the replays: it can't be shot.
- Other enemies (Mechanics.extra_targets): expected number of other enemy heroes close to the target. Ricochet
  bounces and Split Shot pellets that hit them are booked apart (`FightResult.*_splash`), they never kill anyone.
  Real Ricochet damage is 15% of its holders' gun damage, which is 0.23 bounces per hit, so a fair team-fight
  value is about 0.25, not 1-2.
- Split Shot also hits the main target: during the active each landed shot lands SPLIT_PRIMARY_HIT more copies
  (fit: real Split Shot damage is 27% of its holders' gun damage; the tooltip's "each target hit once per
  multishot" would allow at most 1, so the game's rule is looser than it reads).
- Movement (Mechanics.movement): fighters hold their distance (the step 2 calibration) until one is losing and below
  Skill.flee_hp; he stops shooting and runs, the other chases and keeps shooting. Speed = hero max_move_speed +
  move speed items and buffs, times (1 - slows x (1 - slow resist)); stunned / immobilized = 0. Both dash
  (ground_dash_distance over ground_dash_duration) while stamina lasts; stamina items add charges and regen. The
  runner escapes when the gap reaches Mechanics.escape_dist: the fight ends with no winner (`FightResult.escaped`).
  Slows come from abilities with a SlowPercent-type property (applied on cast at spirit accuracy, a generic
  approximation) and from items: Slowing Hex, Mystic Slow, Slowing Bullets, Cold Front, Arctic Blast, Phantom
  Strike, Lifestrike. Escape tools: Warp Stone, Ethereal Shift, Fleetfoot, Dispel Magic, Counterspell,
  Magic Carpet, Enduring Speed, stamina items. Phantom Strike closes the gap on a runner. Hero mobility abilities
  (grapples, teleports, flight) are NOT modeled: only items, base speed, sprint and stamina. Majestic Leap gets no
  escape value: real holders escape less often, not more (it is an engage tool), so it keeps its step 2 barrier only.
- Range spread (Mechanics.range_drift): the distance is lognormal around the fight distance (log sd and drift time from
  real Phantom+ 1v1 positions, data/fight_range.json), and the engine takes distance effects as expectations over it
  (Engine.p_within / spread_mean / reach_ready). See validation/README.md "Range spread".
"""
from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass

from .build import combine_resist
from .data import GAME
from .items_fx import BuildUp, FX, CC_KEYS, _basic_melee


SUMMON_ACC_MAX = 0.9        # cap on accuracy against a summon (acc_mult x hero accuracy)
SPLIT_PRIMARY_HIT = 2.8     # Split Shot copies landing on the main target per landed shot (fit to real, see README)
SPLIT_SECONDARY_COVER = 0.5  # share of nearby enemies inside the 45 degree fan (assumption)
WARP_AWAY = 0.3             # share of Warp Stone's teleport range that ends up as extra gap when running (fit)
MELEE_REACH = 6.0           # beyond this gap (+ start distance) rotation melees don't land
FLEE_RECOVER = 0.25         # stop running once health is this much above flee_hp (heals)
SPRINT_DELAY = 2.0          # a runner sprints (hero sprint_speed + Sprint Boots) after this long (assumption)
CHASE_PROB = 0.85           # share of runs the other side chases (full speed, dashing); else he stands and shoots (fit)


@dataclass
class Mechanics:
    parry: bool = True
    summons: bool = True
    movement: bool = True
    range_drift: bool = True     # distance spreads around the start distance (Engine.p_within etc., fight_range.json)
    extra_targets: float = 0.0   # expected other enemy heroes near the target (multi-target items)
    escape_dist: float = 40.0    # gap (m) at which a runner is out of the fight


DRIFT_MIN, DRIFT_MAX = 1.5, 40.0   # meters; 40 = the fit's "nearest enemy" cut
_DRIFT = None


def drift_params():
    """(log_sd, tau_s) of real 1v1 fight distance around its median: data/fight_range.json (Phantom+ match_paths,
    scripts/range/fit_range.py)."""
    global _DRIFT
    if _DRIFT is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "fight_range.json")) as fh:
            a = json.load(fh)["duel"]["all"]
        _DRIFT = (a["log_sd"], a["tau_s"])
    return _DRIFT


DEFAULT = Mechanics()   # None turns the new mechanics off for every Engine built without an explicit value


_RAW = None


def raw_props(class_name):
    """Properties of any entry in raw/items.json (parry etc. are not shop items), as floats where possible."""
    global _RAW
    if _RAW is None:
        with open(os.path.join(GAME, "raw", "items.json")) as f:
            _RAW = {x.get("class_name"): x for x in json.load(f)}
    out = {}
    for k, v in ((_RAW.get(class_name) or {}).get("properties") or {}).items():
        v = v.get("value") if isinstance(v, dict) else v
        try:
            out[k] = float(str(v).rstrip("msx%"))
        except (TypeError, ValueError):
            pass
    return out


def _debuff(target, key, value, duration, tag):
    dur = duration * max(0.0, 1.0 - target.st.status_resist - target.stat("status_resist"))
    if dur <= 0:
        return
    target.mods.add(key, value, dur, tag)
    target.mark_debuff(key, tag)
    if key in CC_KEYS:
        for fx in target.items_fx:
            g = getattr(fx, "on_cc", None)
            if g:
                g(target, key)


def nearby_enemies(f):
    """Expected other enemy heroes near f's target: Mechanics.extra_targets in a duel, the living ones in a team fight."""
    g = getattr(f.e, "nearby_enemies", None)
    return g(f) if g is not None else f.e.mech.extra_targets


def _splash(f, amount, kind, source):
    """Damage to other enemy heroes near the target, mitigated like a hit on the target (its resists stand in for
    theirs), booked in f.counters["splash"]."""
    if amount <= 0:
        return 0.0
    team_splash = getattr(f.e, "team_splash", None)
    if team_splash is not None:          # team fight: the other enemies are real fighters
        return team_splash(f, amount, kind, source)
    e = f.enemy
    amt = amount * f.st.outgoing_mult * (1.0 + f.stat("damage_amp"))
    if kind == "bullet":
        amt *= 1.0 - combine_resist(e.st.bullet_resist, f.st.bullet_shred)
    elif kind == "spirit":
        amt *= 1.0 - combine_resist(e.st.spirit_resist, f.st.spirit_shred)
    d = f.counters.setdefault("splash", {})
    d[source] = d.get(source, 0.0) + amt
    return amt


# ---------------------------------------------------------------------------------------------------------------
# Parry
# ---------------------------------------------------------------------------------------------------------------
def parry_check(eng, att, dfd, raw, w):
    """Called for every rotation heavy melee. Returns the share of `raw` that lands (0 if parried)."""
    if not dfd.alive or dfd.mods.active("stun") or dfd.skill.parry_rate <= 0:
        return 1.0
    p = dfd.skill.parry_rate * dfd.counters.get("parry_mult", 1.0)
    k = dfd.acc("parry").take(min(1.0, p) * min(1.0, w))
    if k:
        parried(eng, att, dfd, raw / max(w, 1e-9))
    if w >= 1.0:
        return 0.0 if k else 1.0
    return 1.0 - min(1.0, p)


def parried(eng, att, dfd, full):
    pp = raw_props("citadel_ability_melee_parry")
    d = pp.get("ParriedStunTime", 2.75)
    _debuff(att, "stun", 1, d, ("parry", "stun"))
    _debuff(att, "damage_taken_amp", pp.get("VictimDamageTakenScale", 25) / 100, d, ("parry", "amp"))
    dfd.counters["parries"] = dfd.counters.get("parries", 0) + 1
    eng.note(f"{dfd.name} parries {att.name}")
    for fx in dfd.items_fx:
        g = getattr(fx, "on_parry", None)
        if g:
            g(dfd, att, full)


# ---------------------------------------------------------------------------------------------------------------
# Spell parry (Counterspell)
# ---------------------------------------------------------------------------------------------------------------
def spell_blocked(eng, src, dst, ability=None):
    """True if dst's open spell-parry window blocks this ability / item hit from src."""
    sp = dst.counters.get("spell_parry")
    if not sp:
        return False
    t = eng.t
    until, ab, ab_until, fx = sp
    if t <= until or (ability is not None and ability is ab and t <= ab_until):
        fx.success(dst)
        return True
    if t > max(until, ab_until):
        dst.counters.pop("spell_parry", None)
    return False


# ---------------------------------------------------------------------------------------------------------------
# Summons
# ---------------------------------------------------------------------------------------------------------------
_TARGETING = None


def summon_targeting():
    """{kind: {"focus": share of trigger pulls, "acc_mult": accuracy vs on a hero}} from data/summon_targeting.json."""
    global _TARGETING
    if _TARGETING is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "summon_targeting.json")) as fh:
            _TARGETING = json.load(fh)["kinds"]
    return _TARGETING


class Summon:
    def __init__(self, owner, name, hp, spirit_resist=0.0, bullet_resist=0.0, until=math.inf, kind="turret",
                 on_death=None):
        self.owner, self.name, self.hp = owner, name, hp
        self.bullet_resist, self.spirit_resist = bullet_resist, spirit_resist
        self.until = until
        self.kind = kind
        t = summon_targeting().get(kind, {})
        self.focus, self.acc_mult, self.splash = t.get("focus", 0.0), t.get("acc_mult", 1.0), t.get("splash", 0.0)
        self.on_death = on_death
        self.alive = True

    def hurt(self, amount, kind="bullet"):
        res = self.bullet_resist if kind == "bullet" else self.spirit_resist if kind == "spirit" else 0.0
        amt = min(self.hp, amount * (1.0 - res))
        self.hp -= amt
        if self.hp <= 0:
            self.alive = False
            self.owner.e.note(f"{self.name} of {self.owner.name} destroyed")
            if self.on_death:
                self.on_death()
        return amt


def add_summon(owner, name, hp, spirit_resist=0.0, bullet_resist=0.0, life=math.inf, delay=0.0, kind="turret",
               on_death=None):
    """A summon the enemy can shoot, or None if summons are off. Give it to Engine.dot as guard= so its damage
    stops when it dies. kind picks its row in data/summon_targeting.json; on_death runs if it is killed. Its life
    is capped at the row's life_other_s: the median real life of summons no enemy hero killed (troopers, other
    heroes, left behind), which a 1v1 doesn't have."""
    m = owner.e.mech
    if m is None or not m.summons:
        return None
    life = min(life, summon_targeting().get(kind, {}).get("life_other_s", math.inf))
    s = Summon(owner, name, hp, spirit_resist, bullet_resist, owner.e.t + delay + life, kind, on_death)
    owner.counters.setdefault("summons", []).append(s)
    row = summon_targeting().get(kind, {})
    if row.get("break_p"):
        owner.e.after(delay + row["break_s"], _break, s, row["break_p"])
    return s


def _break(s, p):
    """The enemy walks up and breaks summon s (melee) with probability p: Graves' gravestone, which bullets can't hurt."""
    f = s.owner.enemy
    if f is not None and f.alive and alive(s) and s.alive and f.acc("summon_break:" + s.kind).take(p):
        d = f.counters.setdefault("summon_dmg", {})   # not in summon_dmg_kind: that is the gun / splash fit
        d[s.name] = d.get(s.name, 0.0) + s.hurt(s.hp, "pure")


def alive(s):
    """True for a summon still standing (or no summon: summons off)."""
    return s is None or (s.alive and s.until > s.owner.e.t)


def live_summons(f):
    """The first (oldest) living summon of each kind f has out, in spawn order: the one the enemy shoots."""
    t = f.e.t
    out, seen = [], set()
    for s in f.counters.get("summons", ()):
        if s.alive and s.until > t and s.kind not in seen:
            seen.add(s.kind)
            out.append(s)
    return out


def live_summon(f):
    s = live_summons(f)
    return s[0] if s else None


def pick_summon(f, e):
    """The enemy summon f spends this trigger pull on, or None (shoot the hero)."""
    for s in live_summons(e):
        if s.bullet_resist >= 1.0:   # bullets can't hurt it (Graves' gravestone)
            continue
        focus = s.focus if f.skill.summon_focus is None else f.skill.summon_focus
        if focus > 0 and f.acc("summon_focus:" + s.kind).take(focus):
            return s
    return None


def note_hit_while_summoned(src, dst, amount, source):
    """dst took amount of hero damage while it has summons out. Books it per kind as [gun, other] (the fit compares
    it with damage to the summons) and splashes non-gun damage (area abilities, items, melee) onto every living
    summon: amount x its kind's splash share (fitted to replays against the damage all of a kind's summons take,
    see data/summon_targeting.json). Gun pulls go to one summon at a time (pick_summon: the oldest of each kind)."""
    d = dst.counters.setdefault("hit_while_summon", {})
    gun = source == "gun"
    for s in live_summons(dst):
        row = d.setdefault(s.kind, [0.0, 0.0])
        row[0 if gun else 1] += amount
    if gun:
        return
    t = dst.e.t
    for s in list(dst.counters.get("summons", ())):
        if s.alive and s.until > t and s.splash > 0:
            _book(src, s, s.hurt(amount * s.splash, "pure"), 1)


def _book(f, s, amt, i):
    d = f.counters.setdefault("summon_dmg", {})
    d[s.name] = d.get(s.name, 0.0) + amt
    k = f.counters.setdefault("summon_dmg_kind", {}).setdefault(s.kind, [0.0, 0.0])
    k[i] += amt


def shoot_summon(eng, f, s, n_bullets):
    """f spends this trigger pull on enemy summon s. Returns True (the pull is used)."""
    hits = f.acc("summon_hit").take(min(SUMMON_ACC_MAX, f.skill.accuracy * s.acc_mult), n_bullets)
    if hits:
        per, _ = eng.bullet_damage(f)
        _book(f, s, s.hurt(per * hits, "bullet"), 0)
    return True


# ---------------------------------------------------------------------------------------------------------------
# Movement
# ---------------------------------------------------------------------------------------------------------------
SLOW_PROPS = ("SlowPercent", "MovementSlowPct", "MoveSlowPercent", "MovementSlow", "MoveSpeedSlowPct",
              "MoveSpeedAndDashSlowPct", "MovementSpeedSlow")
SLOW_DUR_PROPS = ("SlowDuration", "MovementSlowDuration", "DebuffDuration", "AbilityDuration")


def after_cast(state):
    """Hook from AbilityState.cast: generic ability slow on the enemy (movement mode)."""
    f = state.f
    m = f.e.mech
    if not m.movement or state.impl.kind in ("self", "passive"):
        return
    c = state.ctx
    pct = next((c.raw(p) for p in SLOW_PROPS if c.raw(p)), 0.0)
    if pct <= 0 or f.enemy is None:
        return
    dur = next((c.dur(p) for p in SLOW_DUR_PROPS if c.raw(p)), 2.0)
    land = f.skill.spirit_accuracy if state.impl.kind == "skillshot" else 1.0
    delay = c.raw("AbilityCastDelay")
    e = f.enemy
    f.e.after(delay, lambda: e.alive and _debuff(e, "move_slow", min(0.9, pct / 100) * land, dur,
                                                 ("ab_slow", state.ab.class_name)))


class Mover:
    """Distance control, escape and chase. Ticks every DT seconds."""
    DT = 0.1

    def __init__(self, eng):
        self.e = eng
        self.start = eng.distance
        for f in eng.fighters:
            b = f.st.hero.base
            x = f.st.extra
            f.counters["stamina"] = b.get("stamina", 3) + x.get("MODIFIER_VALUE_STAMINA", 0)
            f.counters["stamina_max"] = f.counters["stamina"]
            f.counters["stamina_regen"] = b.get("stamina_regen_per_second", 0.222) * (
                1 + x.get("MODIFIER_VALUE_STAMINA_REGEN_PER_SECOND_PERCENTAGE", 0) / 100)
            f.counters["dash_until"] = -1.0
        eng.after(self.DT, self.tick)

    # -- speeds --------------------------------------------------------------------------------------------
    def speed(self, f):
        if not f.alive or f.mods.active("immobilize"):
            return 0.0
        eth = None
        if f.mods.active("stun"):
            eth = f.mods.get("stun", "ethereal")
            if eth is None:
                return 0.0
        b = f.st.hero.base
        v = b.get("max_move_speed", 7.0) + f.st.extra.get("MODIFIER_VALUE_MOVEMENT_SPEED_MAX", 0) + f.stat("move_speed")
        for fx in f.items_fx:
            g = getattr(fx, "move_speed", None)
            if g:
                v += g(f)
        if f.counters.get("fleeing") and self.e.t - f.counters.get("flee_t", 0.0) >= SPRINT_DELAY:
            v += b.get("sprint_speed", 1.6) + f.st.extra.get("MODIFIER_VALUE_SPRINT_SPEED_BONUS", 0)
        if eth is not None:
            v = f.counters.get("float_speed", 2.5)
        slow = combine_resist(f.mods.values("move_slow"), ())
        sres = min(1.0, f.counters.get("slow_resist", 0.0) + f.stat("slow_resist"))
        v *= 1.0 - slow * (1.0 - sres)
        t = self.e.t
        if t < f.counters["dash_until"]:
            dash = b.get("ground_dash_distance_in_meters", 10.0) / max(0.2, b.get("ground_dash_duration", 0.68))
            dash *= 1.0 - min(0.9, f.stat("dash_slow")) * (1.0 - sres)
            v = max(v, dash)
        return max(0.0, v)

    def melee_reach(self, f, heavy):
        return melee_reach(f, heavy)

    def try_dash(self, f):
        if f.counters["stamina"] >= 1 and self.e.t >= f.counters["dash_until"] and f.alive \
                and not f.mods.active("stun") and not f.mods.active("immobilize"):
            f.counters["stamina"] -= 1
            f.counters["dash_until"] = self.e.t + f.st.hero.base.get("ground_dash_duration", 0.68)

    def draw(self, f):
        """A uniform [0, 1) draw: engine rng if sampling, else a hash of the matchup so a single fight stays
        deterministic while a population of fights gets the right mix (a one-off decision has no Accum)."""
        if self.e.rng is not None:
            return self.e.rng.random()
        h = hash((round(f.st.max_health, 1), f.st.souls, round(f.enemy.st.max_health, 1), f.enemy.st.souls,
                  round(self.e.t, 1), f.st.hero.id, f.enemy.st.hero.id))
        return (h % 1000003) / 1000003

    # -- loop -----------------------------------------------------------------------------------------------
    def tick(self):
        e = self.e
        if e.over:
            return
        a, b = e.fighters
        for f in (a, b):
            f.counters["stamina"] = min(f.counters["stamina_max"], f.counters["stamina"] + f.counters["stamina_regen"] * self.DT)
            fl = f.counters.get("fleeing")
            if not fl and f.alive and f.enemy.alive and not f.enemy.counters.get("fleeing") \
                    and f.hp_frac < f.skill.flee_hp and f.hp_frac < f.enemy.hp_frac and f.skill.use_actives:
                f.counters["fleeing"] = True
                f.counters["flee_t"] = e.t
                e.note(f"{f.name} runs")
                for fx in f.items_fx:
                    g = getattr(fx, "on_flee", None)
                    if g:
                        g(f)
                f.enemy.counters["chasing"] = self.draw(f) < CHASE_PROB
                for fx in f.enemy.items_fx:
                    g = getattr(fx, "on_enemy_flee", None)
                    if g:
                        g(f.enemy)
            elif fl and f.hp_frac > f.skill.flee_hp + FLEE_RECOVER:
                f.counters["fleeing"] = False
                e.note(f"{f.name} turns back")
        runner = a if a.counters.get("fleeing") else b if b.counters.get("fleeing") else None
        if runner is not None:
            chaser = runner.enemy
            runner.gun_locked_until = max(runner.gun_locked_until, e.t + self.DT + 0.01)
            self.try_dash(runner)
            for fx in chaser.items_fx:
                g = getattr(fx, "chase", None)
                if g and chaser.counters.get("chasing"):
                    g(chaser)
            vr = self.speed(runner)
            vc = 0.0
            if chaser.counters.get("chasing"):
                vc = self.speed(chaser)
                if vc < vr:
                    self.try_dash(chaser)
                    vc = self.speed(chaser)
            e.distance = max(1.0, e.distance + (vr - vc) * self.DT)
            if e.distance >= e.mech.escape_dist:
                e.escaped = runner.name
                e.note(f"{runner.name} escapes at {e.distance:.0f} m")
                e.over = True
                return
        elif e.distance > self.start:
            # nobody running: the chaser walks back into his fighting distance
            e.distance = max(self.start, e.distance - max(self.speed(a), self.speed(b)) * self.DT)
        e.after(self.DT, self.tick)


def melee_reach(f, heavy):
    """Gap beyond the start distance a rotation melee still lands from. Items with MeleeDistanceScale make heavy
    melees lunge that % farther (game data: Melee Charge 50, Crushing Fists 60, Runed Gauntlets 150; the largest
    held counts), so a chaser lands them on a runner sooner."""
    if not heavy:
        return MELEE_REACH
    return MELEE_REACH * (1.0 + max((fx.item.p("MeleeDistanceScale", 0.0) for fx in f.items_fx
                                      if getattr(fx, "item", None) is not None), default=0.0) / 100)


def melee_reachable(eng):
    mv = getattr(eng, "mover", None)
    return mv is None or eng.distance <= mv.start + MELEE_REACH


# ---------------------------------------------------------------------------------------------------------------
# Item handlers that only exist with mechanics on (attached by fight.make_fighter). `MECH_HANDLERS` is separate
# from items_fx.HANDLERS so items_fx.MODELED (search candidates) is unchanged.
# ---------------------------------------------------------------------------------------------------------------
MECH_HANDLERS = {}


def mech_handler(*class_names, need="parry"):
    def deco(cls):
        cls.need = need
        for n in class_names:
            MECH_HANDLERS.setdefault(n, []).append(cls)
        return cls
    return deco


def _base_fx(f, item, me):
    return next((fx for fx in f.items_fx if fx.item is item and fx is not me and not getattr(fx, "need", None)), None)


def _used_within(base, seconds):
    """The base handler's active was used within `seconds` (its ready_at minus its cooldown)."""
    if base is None or base.ready_at <= 0:
        return False
    return base.now < base.ready_at - base.cd() + seconds


@mech_handler("upgrade_melee_rebuttal", need="parry")
class Rebuttal(FX):
    """On a parry: heal ParrySuccessHealPercentage% of the parried damage, deal it back to the attacker, and
    +BonusDamagePercent% damage for BuffDuration. Holders parry REBUTTAL_PARRY_MULT x as often (real holders log
    0.88 parry successes per 3 min vs 0.47 for everyone else)."""
    REBUTTAL_PARRY_MULT = 1.9

    def on_start(self, f):
        f.counters["parry_mult"] = self.REBUTTAL_PARRY_MULT

    def on_parry(self, f, att, full):
        f.heal(full * self.item.p("ParrySuccessHealPercentage", 100) / 100, self.name, "item")
        f.e.damage(f, att, full, "melee", self.name, is_item=True, procs=False)
        self.buff("damage_amp", self.item.p("BonusDamagePercent", 30) / 100, self.item.p("BuffDuration", 6))


@mech_handler("upgrade_counterspell", need="parry")
class Counterspell(FX):
    """Spell parry timed against an enemy aimed cast (Skill.spell_parry_rate) when off cooldown; see module doc."""

    def on_enemy_cast(self, f, ab):
        if not self.ready() or not f.alive or f.mods.active("stun") or ab.impl.kind not in ("skillshot", "target", "aoe"):
            return
        if not f.acc("spell_parry").take(f.skill.spell_parry_rate):
            return
        self.use()
        win = self.item.p("SpellParryDuration", 0.8)
        lead = ab.ctx.raw("AbilityCastDelay")
        f.counters["spell_parry"] = [self.now + win, ab, self.now + lead + win, self]
        self.done = False

    def success(self, f):
        if getattr(self, "done", True):
            return
        self.done = True
        f.counters["spell_parries"] = f.counters.get("spell_parries", 0) + 1
        f.heal(self.v("HealOnSuccess"), self.name, "item")
        d = self.item.p("BuffDuration", 6)
        self.buff("spirit_power", self.item.p("SpiritPower"), d)
        self.buff("move_speed", self.item.p("BonusMoveSpeed"), d)


@mech_handler("upgrade_ricochet", need="splash")
class Ricochet(FX):
    """Each gun hit bounces RicochetDamagePercent% to min(RicochetTargets, nearby enemies) other heroes."""

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "bullet" or hit.source != "gun" or not hit.hits:
            return
        n = nearby_enemies(f)
        k = f.acc("ricochet").take(min(1.0, n), 1) if n < 1 else min(int(self.item.p("RicochetTargets", 2)), int(n))
        if k:
            _splash(f, hit.raw * k * self.item.p("RicochetDamagePercent", 65) / 100, "bullet", self.name)


@mech_handler("upgrade_split_shot", need="any")
class SplitShot(FX):
    """Active for BonusShotsDuration: every trigger pull also throws a fan of BulletSplitShot bullets; each target is
    hit at most once per fan. The main target takes SPLIT_PRIMARY_HIT more copies of each landed shot; other
    nearby heroes (Mechanics.extra_targets) are hit at accuracy x SPLIT_SECONDARY_COVER and each such shot adds a
    WeaponDamagePerStack% weapon damage stack (MaxStacks, WeaponDamageBonusDuration). Booked as Split Shot."""

    def try_active(self, f):
        if not self.ready() or f.e.distance > 35:
            return False
        self.use()
        self.until = self.now + self.item.p("BonusShotsDuration", 5)
        return True

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "bullet" or hit.source != "gun" or self.now >= getattr(self, "until", -1):
            return
        st = f.st
        n = st.pellets * st.burst_count
        k = f.acc("split_main").take(f.skill.accuracy * (1.0 - t.stat("evasion")), n)
        per = f.counters.get("bullet_per", 0.0)
        if k and per:
            f.e.damage(f, t, per * k * SPLIT_PRIMARY_HIT, "bullet", self.name, is_item=True, procs=False, hits=k)
        x = nearby_enemies(f)
        if x > 0 and per:
            k2 = f.acc("split_side").take(min(1.0, f.skill.accuracy * SPLIT_SECONDARY_COVER * x), 1)
            if k2:
                _splash(f, per * n * f.skill.accuracy, "bullet", self.name)
                j = f.counters.get("split_stack", 0)
                f.counters["split_stack"] = j + 1
                self.buff("weapon_pct", self.item.p("WeaponDamagePerStack", 8) / 100,
                          self.item.p("WeaponDamageBonusDuration", 12), tag=("split", j % int(self.item.p("MaxStacks", 5))))


# -- movement items ---------------------------------------------------------------------------------------------
class _MoveFX(FX):
    pass


@mech_handler("upgrade_cardio_calibrator", need="movement")
class EnduringSpeed(_MoveFX):
    """Passive move speed is in the static stats; this adds SlowResistancePercent."""

    def on_start(self, f):
        f.counters["slow_resist"] = f.counters.get("slow_resist", 0.0) + self.item.p("SlowResistancePercent") / 100


@mech_handler("upgrade_fleetfoot_boots", need="movement")
class Fleetfoot(_MoveFX):
    """Active: +ActiveBonusMoveSpeed and SlowResistancePercent for AbilityDuration, used to run or to chase."""

    def _go(self, f):
        if not self.ready():
            return
        self.use()
        d = self.item.p("AbilityDuration", 5)
        self.buff("move_speed", self.item.p("ActiveBonusMoveSpeed", 3), d)
        self.buff("slow_resist", self.item.p("SlowResistancePercent", 40) / 100, d)

    def on_flee(self, f):
        self._go(f)

    def chase(self, f):
        self._go(f)


@mech_handler("upgrade_reduce_debuff_duration", need="movement")
class DispelSpeed(_MoveFX):
    """Dispel Magic's active also gives +ActiveBonusMoveSpeed for BuffDuration."""

    def move_speed(self, f):
        base = getattr(self, "_b", None) or _base_fx(f, self.item, self)
        self._b = base
        return self.item.p("ActiveBonusMoveSpeed", 2) if _used_within(base, self.item.p("BuffDuration", 3)) else 0.0


@mech_handler("upgrade_self_bubble", need="movement")
class EtherealMove(_MoveFX):
    """Ethereal Shift: float at FloatMoveSpeed while in the void, then +BonusMoveSpeed for BuffDuration."""

    def on_start(self, f):
        f.counters["float_speed"] = self.item.p("FloatMoveSpeed", 2.5)

    def move_speed(self, f):
        return self.item.p("BonusMoveSpeed", 3) if f.mods.get("spirit_power", "eth") is not None else 0.0


@mech_handler("upgrade_magic_carpet", need="movement")
class MagicCarpet(_MoveFX):
    """Used to run: assumed +FlyMoveSpeed m/s for AbilityDuration (flying likely also breaks line of sight, not
    modeled)."""

    def on_flee(self, f):
        if self.ready():
            self.use()
            self.buff("move_speed", self.item.p("FlyMoveSpeed", 7), self.item.p("AbilityDuration", 12))


@mech_handler("upgrade_warp_stone", need="movement")
class WarpStoneMove(_MoveFX):
    """With movement on, Warp Stone is saved for running: its bullet resist, and on average WARP_AWAY of its
    AbilityCastRange teleport adds to the gap (fit: the full 11 m gave +23 pts escape share vs +6.5 real)."""

    def on_start(self, f):
        self.base = _base_fx(f, self.item, self)
        if self.base is not None:
            self.base.try_active = lambda f: False

    def on_flee(self, f):
        b = self.base
        if b is None or not b.ready() or f.mods.active("stun"):
            return
        b.use()
        self.buff("bullet_resist", self.item.p("BulletResist") / 100, self.item.p("CasterBuffDuration", 6))
        f.e.distance += self.item.p("AbilityCastRange", 11) * WARP_AWAY


@mech_handler("upgrade_phantom_strike", need="movement")
class PhantomChase(_MoveFX):
    """Phantom Strike on a runner within AbilityCastRange: its normal hit plus teleporting next to him, and its
    SlowPercent slow."""

    def on_start(self, f):
        self.base = _base_fx(f, self.item, self)

    def chase(self, f):
        b = self.base
        if b is None or not b.ready() or f.e.distance > self.item.p("AbilityCastRange", 25) + 0.5:
            return
        if b.try_active(f):
            f.e.distance = 2.0
            _debuff(f.enemy, "move_slow", self.item.p("SlowPercent", 40) / 100, self.item.p("SlowDuration", 3),
                    ("phantom", "slow"))


@mech_handler("upgrade_containment", need="movement")
class SlowingHex(_MoveFX):
    """Active on a runner in AbilityCastRange: SlowPercent slow and GroundDashReductionPercent shorter dashes."""

    def chase(self, f):
        if not self.ready() or f.e.distance > self.item.p("AbilityCastRange", 25) + 0.5:
            return
        self.use()
        d = self.item.p("AbilityDuration", 3.5)
        _debuff(f.enemy, "move_slow", self.item.p("SlowPercent", 16) / 100, d, ("hex", "slow"))
        _debuff(f.enemy, "dash_slow", abs(self.item.p("GroundDashReductionPercent", 26)) / 100, d, ("hex", "dash"))


@mech_handler("upgrade_magic_slow", need="movement")
class MysticSlow(_MoveFX):
    """Spirit damage from abilities / items slows by MovementSpeedSlow% (and dashes) for AbilityDuration."""

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "spirit" or not (hit.is_ability or hit.is_item) or hit.amount <= 0:
            return
        d = self.item.p("AbilityDuration", 2)
        _debuff(t, "move_slow", self.item.p("MovementSpeedSlow", 24) / 100, d, ("mslow", "slow"))
        _debuff(t, "dash_slow", abs(self.item.p("GroundDashReductionPercent", 10)) / 100, d, ("mslow", "dash"))


@mech_handler("upgrade_slowing_bullets", need="movement")
class SlowingBulletsMove(BuildUp):
    def proc(self, f, t):
        d = self.item.p("SlowDuration", 3.5)
        _debuff(t, "move_slow", self.item.p("SlowPercent", 24) / 100, d, ("sbullets", "slow"))
        _debuff(t, "dash_slow", abs(self.item.p("GroundDashReductionPercent", 20)) / 100, d, ("sbullets", "dash"))


SlowingBulletsMove.need = "movement"


@mech_handler("upgrade_cold_front", "upgrade_arctic_blast", need="movement")
class FrostSlow(_MoveFX):
    """Cold Front / Arctic Blast: their hit slows by MovementSpeedSlow / SlowPercent for AbilityDuration /
    SlowDuration."""

    def on_damage_dealt(self, f, t, hit):
        if hit.source != self.name:
            return
        pct = self.item.p("MovementSpeedSlow") or self.item.p("SlowPercent")
        d = self.item.p("SlowDuration") or self.item.p("AbilityDuration", 4)
        _debuff(t, "move_slow", pct / 100, d, ("frost", self.name))


@mech_handler("upgrade_boxing_glove", need="movement")
class LifestrikeSlow(_MoveFX):
    """Lifestrike's melee proc also slows SlowPercent for SlowDuration (same AbilityCooldown)."""

    def on_damage_dealt(self, f, t, hit):
        if not _basic_melee(hit) or not self.ready():
            return
        self.use()
        _debuff(t, "move_slow", self.item.p("SlowPercent", 48) / 100, self.item.p("SlowDuration", 2.5), ("lstrike", "slow"))


def attach(f, items):
    m = f.e.mech
    on = {"parry": m.parry, "splash": True, "any": True, "movement": m.movement}
    for it in items:
        for cls in MECH_HANDLERS.get(it.class_name, ()):
            if not on.get(cls.need, False):
                continue
            fx = cls(it, f)
            f.items_fx.append(fx)
            if hasattr(fx, "stat"):
                f.stat_hooks.append(fx.stat)
