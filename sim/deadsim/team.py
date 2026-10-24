"""Team fights: 2v2, 3v3 (any N v M) on the same engine as duels, so heals, barriers, auras and area damage on
teammates get credit.

    from deadsim import Loadout
    from deadsim.team import team_fight, team_item_value
    a = [Loadout("Haze", ["Rapid Rounds", "Toxic Bullets"], souls=20000),
         Loadout("Dynamo", ["Healing Nova", "Rescue Beam"], souls=20000)]
    b = [Loadout("Abrams", ["Extra Health"], souls=20000), Loadout("Infernus", ["Extra Spirit"], souls=20000)]
    r = team_fight(a, b)
    print(r.summary())                       # winner team, time, one row per hero (damage, heals given, kills)
    team_item_value(a, b, 1, "Healing Nova")  # what one item is worth to the whole team

How a team fight differs from a duel (everything else is the duel model, see engine.py):
- Every hero shoots and casts at one target. focus="focus" (default): each team picks the living enemy with the
  least health and everyone shoots it, then the next when it dies. focus="spread": hero i takes enemy i (lanes),
  and falls back to focus when its own target dies. The fight ends when one team is dead or at max_time.
- Area damage: area abilities (AbilityImpl.kind "aoe") and area items (AOE_ITEMS) also hit each other living
  enemy for aoe_share of the damage (expected share of the other enemies standing inside the area; assumption).
  Ricochet and Split Shot bounces hit the real other enemies (huddle x others stand near the target).
- Support: items and abilities that reach teammates (TEAM_ITEMS, ALLY_ABILITIES below) heal, shield and buff the
  teammate who needs it. Area heals and auras reach each teammate in range for `huddle` of the value (expected
  share of teammates standing close; assumption). Heals and barriers given to teammates are booked per hero.
- Movement (escape and chase) is off: running is a 1v1 decision. Parry, summons and Counterspell stay on.
Known gaps: one shared distance for every pair; crowd control and debuffs from area abilities only land on the
main target; Mystic Conduit, Tag Along and Plot Armor still behave as in a duel.
"""
from __future__ import annotations

import dataclasses
import heapq
from dataclasses import dataclass, field

from .data import game
from .engine import Engine, Fighter, _UNSET, MELEE_MIN_RATE, long_cooldowns_spent
from .patterns import fight_start
from . import items_fx

AOE_SHARE = 0.35   # share of an area hit that also lands on each other enemy (assumption)
HUDDLE = 0.75      # share of an area heal / aura that reaches each teammate (assumption)
AOE_ITEMS = {"Scourge"}
ALLY_HEAL_HP = 0.5   # heal a teammate below this health share
ALLY_BARRIER_HP = 0.6


# ---------------------------------------------------------------------------------------------------------------
# Support helpers
# ---------------------------------------------------------------------------------------------------------------
def heal_ally(src: Fighter, dst: Fighter, amount, source):
    """src heals teammate dst: src's outgoing heal amp, dst's heal received (Healbane etc.). Booked on src."""
    if not dst.alive or amount <= 0:
        return 0.0
    if dst is src:
        return src.heal(amount, source, "item")
    mult = 1.0 + src.st.heal_amp_cast + dst.stat("heal_received")
    amt = min(dst.max_hp - dst.hp, amount * max(0.0, mult))
    dst.hp += amt
    dst.healed += amt
    sup = src.counters.setdefault("support", {})
    sup[source] = sup.get(source, 0.0) + amt
    return amt


def barrier_ally(src: Fighter, dst: Fighter, amount, duration, source):
    dst.add_barrier(amount, duration)
    if dst is not src:
        sup = src.counters.setdefault("barrier_given", {})
        sup[source] = sup.get(source, 0.0) + amount


def neediest(f: Fighter, below=1.0, include_self=True, others_only=False):
    """Living teammate (or f) with the lowest health share under `below`, or None."""
    pool = [x for x in f.allies if x.alive and (x is not f or include_self) and not (others_only and x is f)]
    pool = [x for x in pool if x.hp_frac < below]
    return min(pool, key=lambda x: x.hp_frac) if pool else None


# ---------------------------------------------------------------------------------------------------------------
# Items that reach teammates (replace the duel handler in a team fight)
# ---------------------------------------------------------------------------------------------------------------
TEAM_ITEMS = {}


def team_item(class_name):
    def deco(cls):
        TEAM_ITEMS[class_name] = cls
        return cls
    return deco


@team_item("upgrade_health_nova")
class TeamHealingNova(items_fx.FX):
    """Heals the user and teammates in AuraRadius (huddle each) when anyone in range drops below half health."""

    def try_active(self, f):
        if not self.ready() or neediest(f, ALLY_HEAL_HP) is None:
            return False
        self.use()
        tot, d = self.v("TotalHealthRegen"), self.dur("RegenDuration", 2)
        hud = f.e.huddle
        for i in range(4):
            for x in f.allies:
                f.e.after(d / 4 * (i + 1), heal_ally, f, x, tot / 4 * (1.0 if x is f else hud), self.name)
        return True


@team_item("upgrade_rescue_beam")
class TeamRescueBeam(items_fx.FX):
    """Channel a heal of HealPercentAmount% of the target's max health on the teammate in most need (itself when
    alone, as in a duel)."""

    def try_active(self, f):
        if not self.ready():
            return False
        x = neediest(f, ALLY_HEAL_HP, others_only=True)
        if x is None:
            if any(a.alive and a is not f for a in f.allies) or f.hp_frac > ALLY_HEAL_HP:
                return False
            x = f
        self.use()
        d = self.item.p("AbilityChannelTime", 2.5)
        amt = x.max_hp * self.item.p("HealPercentAmount") / 100
        f.gun_locked_until = max(f.gun_locked_until, f.e.t + d)
        n = int(d / 0.25)
        for i in range(n):
            f.e.after(0.25 * (i + 1), heal_ally, f, x, amt / n, self.name)
        return True


class TeamBarrier(items_fx.FX):
    prop = "CombatBarrier"
    dur_prop = "BuffDuration"

    def try_active(self, f):
        if not self.ready():
            return False
        x = neediest(f, ALLY_BARRIER_HP)
        if x is None:
            return False
        self.use()
        barrier_ally(f, x, self.v(self.prop), self.item.p(self.dur_prop, 6), self.name)
        return True


@team_item("upgrade_divine_barrier")
class TeamDivineBarrier(TeamBarrier):
    pass


@team_item("upgrade_guardian_ward")
class TeamGuardianWard(TeamBarrier):
    prop = "GuardianWardCombatBarrier"


@team_item("upgrade_restorative_locket")
class TeamRestorativeLocket(items_fx.FX):
    """Stacks from every enemy cast in Radius; the heal goes to the teammate (or self) in most need."""

    def on_enemy_cast(self, f, ab):
        if f.e.distance <= self.item.p("Radius", 32):
            f.counters["locket"] = min(self.item.p("MaxStacks", 25), f.counters.get("locket", 0) + 1)

    def try_active(self, f):
        n = f.counters.get("locket", 0)
        x = neediest(f, ALLY_HEAL_HP)
        if not self.ready() or x is None or n <= 0:
            return False
        self.use()
        f.counters["locket"] = 0
        heal_ally(f, x, n * self.v("HealPerStack"), self.name)
        return True


@team_item("upgrade_dps_aura")
class TeamHeroicAura(items_fx.FX):
    """Passive aura: BulletResist to teammates in Radius (huddle each; the user's own comes with the item's stats)
    while the user lives. Active: BonusFireRate for AbilityDuration to the user and teammates in Radius."""

    def on_start(self, f):
        br = self.item.p("BulletResist") / 100
        for x in f.allies:
            if x is not f:
                x.mods.add("bullet_resist", br * f.e.huddle, 1e9, ("heroic_aura_passive", f.name))

    def on_death_any(self, f):
        if not f.alive:
            for x in f.allies:
                x.mods.remove("bullet_resist", ("heroic_aura_passive", f.name))

    def try_active(self, f):
        if not self.ready():
            return False
        self.use()
        d, fr = self.dur("AbilityDuration", 7), self.item.p("BonusFireRate") / 100
        for x in f.allies:
            if x.alive:
                x.mods.add("fire_rate", fr * (1.0 if x is f else f.e.huddle), d, ("heroic_aura", f.name))
        return True


@team_item("upgrade_bullet_armor_reduction_aura")
class TeamHuntersAura(items_fx.FX):
    """Bullet resist shred and fire rate slow on every enemy in Radius (the single-target x2 only when one enemy
    is left)."""

    def on_start(self, f):
        radius = self.item.p("Radius", 15)
        base_shred = abs(self.item.p("BulletArmorReduction")) / 100
        base_slow = self.item.p("FireRateSlow") / 100
        mult = self.item.p("SingleTargetPlayerMultiplier", 2)

        def k(x):
            return mult if sum(1 for e in f.foes if e.alive) == 1 else 1.0

        for e in f.foes:
            e.stat_hooks.append(lambda x, e=e: {"fire_rate_slow": base_slow * k(x)}
                                if f.alive and x.e.distance <= radius else {})
            if f.e.distance <= radius:
                e.mods.add("bullet_shred", base_shred, 1e9, ("hunters", f.name))
        self.base_shred, self.mult = base_shred, mult

    def on_death_any(self, f):
        """Refresh the shred when the enemy team is down to one (single-target bonus) or f died (aura gone)."""
        alive = [e for e in f.foes if e.alive]
        for e in f.foes:
            e.mods.remove("bullet_shred", ("hunters", f.name))
            if f.alive and e.alive:
                e.mods.add("bullet_shred", self.base_shred * (self.mult if len(alive) == 1 else 1.0), 1e9,
                           ("hunters", f.name))


# ---------------------------------------------------------------------------------------------------------------
# Abilities that reach teammates
# ---------------------------------------------------------------------------------------------------------------
# heal: the caster's heals from this ability also heal each teammate (x huddle); buffs: these buff keys are shared
# the same way; tether: buffs go full strength to the caster and one teammate (Kudzu's 1v1 half factor undone);
# need: cast when any teammate (not just the caster) is below the ability's health threshold.
ALLY_ABILITIES = {
    "citadel_ability_nikuman": {"heal": True, "need": True},        # Dynamo: Rejuvenating Aurora
    "ability_ice_grenade": {"heal": True},                          # Kelvin: Frost Grenade
    "ability_ice_dome": {"buffs": ("regen",)},                      # Kelvin: Frozen Shelter
    "citadel_ability_tangotether": {"tether": 2.0},                # Ivy: Kudzu Connection (1v1 runs at 0.5)
}


def _share_ability(st):
    spec = ALLY_ABILITIES.get(st.ab.class_name)
    if not spec:
        return
    c, f = st.ctx, st.f
    eng = f.e
    if spec.get("heal"):
        own = c.heal

        def heal(amount, own=own):
            got = own(amount)
            for x in f.allies:
                if x is not f and x.alive:
                    heal_ally(f, x, amount * eng.huddle, st.ab.name)
            return got
        c.heal = heal
    keys = spec.get("buffs", ())
    tether = spec.get("tether")
    if keys or tether:
        own_buff = c.buff

        def buff(key, value, duration, tag=None, own=own_buff):
            v = value
            if tether:
                mates = [x for x in f.allies if x is not f and x.alive][:1]
                k = 1.0
                if mates:            # alone, Kudzu keeps the duel's no-tether value
                    v = value * tether
            else:
                mates = [x for x in f.allies if x is not f and x.alive] if key in keys else []
                k = eng.huddle
            own(key, v, duration, tag)
            for x in mates:
                x.mods.add(key, v * k, duration, (st.ab.class_name, key, f.name, tag))
        c.buff = buff
    if spec.get("need"):
        impl = st.impl
        own_should = impl.should_cast

        def should_cast(cc, own=own_should):
            if own(cc):
                return True
            low = neediest(f, 1.0, others_only=True)
            if low is None:
                return False
            hp, f.hp = f.hp, f.max_hp * low.hp_frac   # ask the ability as if the caster were that hurt
            try:
                return own(cc)
            finally:
                f.hp = hp
        impl.should_cast = should_cast


# ---------------------------------------------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------------------------------------------
class TeamEngine(Engine):
    def __init__(self, *a, focus="focus", huddle=HUDDLE, aoe_share=AOE_SHARE, **kw):
        super().__init__(*a, **kw)
        if self.mech is not None and self.mech.movement:
            self.mech = dataclasses.replace(self.mech, movement=False)
        self.focus = focus
        self.huddle = huddle
        self.aoe_share = aoe_share
        self.teams = ([], [])

    # ---- targeting ----------------------------------------------------------------------------------------------
    def pick_target(self, f):
        foes = [e for e in f.foes if e.alive]
        if not foes:
            return None
        if self.focus == "spread" and f.counters.get("lane") is not None:
            lane = f.foes[f.counters["lane"] % len(f.foes)]
            if lane.alive:
                return lane
        return min(foes, key=lambda e: (e.hp + e.barrier_total(), e.name))

    def retarget(self):
        picks = {}
        for f in self.fighters:
            if not f.alive:
                continue
            if f.enemy is None or not f.enemy.alive:
                if self.focus == "focus":
                    side = id(f.foes)
                    if side not in picks:
                        picks[side] = self.pick_target(f)
                    f.enemy = picks[side]
                else:
                    f.enemy = self.pick_target(f)

    def on_death(self, dead, killer):
        if killer is not None and killer is not dead:
            killer.counters["kills"] = killer.counters.get("kills", 0) + 1
        if not any(x.alive for x in dead.allies):
            self.over = True
            return
        self.retarget()
        for f in self.fighters:
            for fx in f.items_fx:
                g = getattr(fx, "on_death_any", None)
                if g:
                    g(f)

    # ---- multi-target damage ---------------------------------------------------------------------------------------
    def nearby_enemies(self, f):
        return self.huddle * max(0, sum(1 for e in f.foes if e.alive and e is not f.enemy))

    def team_splash(self, f, amount, kind, source):
        """Bounce damage (Ricochet, Split Shot) on the other living enemies, split evenly."""
        others = [e for e in f.foes if e.alive and e is not f.enemy]
        if not others:
            return 0.0
        return sum(self.damage(f, e, amount / len(others), kind, source, is_item=True, procs=False, _echo=True)
                   for e in others)

    def damage(self, src, dst, raw, kind, source, *, _echo=False, **kw):
        amt = super().damage(src, dst, raw, kind, source, **kw)
        if _echo or self.aoe_share <= 0 or raw <= 0 or getattr(src, "foes", None) is None:
            return amt
        ab = kw.get("ability")
        area = (kw.get("is_ability") and ab is not None and getattr(ab.impl, "kind", "") == "aoe") \
            or (kw.get("is_item") and source in AOE_ITEMS)
        if area:
            kw = dict(kw, procs=False)
            for e in src.foes:
                if e is not dst and e.alive and not self.over:
                    super().damage(src, e, raw * self.aoe_share, kind, source, **kw)
        return amt

    # ---- run ------------------------------------------------------------------------------------------------------
    def run_team(self, team_a, team_b):
        self.teams = (team_a, team_b)
        self.fighters = list(team_a) + list(team_b)
        for mine, theirs in ((team_a, team_b), (team_b, team_a)):
            for i, f in enumerate(mine):
                f.allies, f.foes = mine, theirs
                f.counters["lane"] = i
                f.enemy = None
        self.retarget()
        for f in self.fighters:
            for fx in f.items_fx:
                g = getattr(fx, "on_start", None)
                if g:
                    g(f)
            if f.skill.fight_phase is not None:
                long_cooldowns_spent(f)
            for ab in f.abilities:
                ab.start()
        for f in self.fighters:
            fight_start(f)
        for f in self.fighters:
            self.at(0.0, self.gun_tick, f)
            self.at(0.0, self.think, f)
            if f.skill.melee_rate > 0:
                self.at(0.5 / max(f.skill.melee_rate, MELEE_MIN_RATE), self.melee_tick, f)
        self.at(0.0, self.regen_tick)
        while self.q and not self.over:
            t, _, fn, args = heapq.heappop(self.q)
            if t > self.max_time:
                self.t = self.max_time
                break
            self.t = t
            fn(*args)
        alive_a = any(f.alive for f in team_a)
        alive_b = any(f.alive for f in team_b)
        winner = "A" if alive_a and not alive_b else "B" if alive_b and not alive_a else None
        return TeamResult(winner, self.t, [_row(f, "A") for f in team_a] + [_row(f, "B") for f in team_b])


def _row(f, team):
    sup = f.counters.get("support", {})
    bar = f.counters.get("barrier_given", {})
    return {
        "name": f.name, "team": team, "hero": f.st.hero.name, "alive": f.alive,
        "hp": round(f.hp, 1), "max_hp": round(f.max_hp, 1), "death_time": f.death_time,
        "damage": sum(f.dmg_out.values()), "damage_by_source": dict(f.dmg_out),
        "damage_taken": sum(f.dmg_in.values()), "healed": f.healed,
        "healing_given": sum(sup.values()), "healing_given_by_source": dict(sup),
        "barrier_given": sum(bar.values()), "kills": f.counters.get("kills", 0),
    }


@dataclass
class TeamResult:
    winner: str | None          # "A", "B" or None (time ran out with both teams standing)
    time: float
    fighters: list = field(default_factory=list)   # one dict per hero, see _row

    def team(self, side):
        return [r for r in self.fighters if r["team"] == side]

    def total(self, side, key):
        return sum(r[key] for r in self.team(side))

    def hp_lost(self, side):
        """Health the side is down at the end (a dead hero counts its whole max health)."""
        return sum(r["max_hp"] - (r["hp"] if r["alive"] else 0.0) for r in self.team(side))

    def summary(self):
        lines = [f"winner={self.winner} t={self.time:.2f}s"]
        for r in self.fighters:
            state = f"hp={r['hp']:.0f}" if r["alive"] else f"died {r['death_time']:.1f}s"
            sup = f"  heals given {r['healing_given']:.0f}" if r["healing_given"] else ""
            sup += f"  barrier given {r['barrier_given']:.0f}" if r["barrier_given"] else ""
            lines.append(f"  [{r['team']}] {r['name']:<22} dmg {r['damage']:6.0f}  taken {r['damage_taken']:6.0f}  "
                         f"kills {r['kills']}  {state}{sup}")
        return "\n".join(lines)

    def to_dict(self):
        return {"winner": self.winner, "time": round(self.time, 2),
                "fighters": [{k: (round(v, 1) if isinstance(v, float) else
                                  {s: round(x, 1) for s, x in v.items()} if isinstance(v, dict) else v)
                              for k, v in r.items()} for r in self.fighters]}


# ---------------------------------------------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------------------------------------------
def team_fight(team_a, team_b, distance=15.0, max_time=40.0, focus="focus", huddle=HUDDLE, aoe_share=AOE_SHARE,
               rng=None, log=False, mechanics=_UNSET, allies=True):
    """team_a, team_b: lists of Loadout (1-6 each). Returns TeamResult.
    allies=False turns everything that reaches teammates off (duel item handlers, no ally abilities, huddle 0), so
    a fight with and without it isolates what items give teammates (scripts/team/team_value.py)."""
    if not allies:
        huddle = 0.0
    from .fight import make_fighter
    from .abilities import load_heroes
    load_heroes()
    if not team_a or not team_b:
        raise ValueError("each team needs at least one hero")
    e = TeamEngine(distance=distance, max_time=max_time, rng=rng, log=log, mech=mechanics,
                   focus=focus, huddle=huddle, aoe_share=aoe_share)
    sides = []
    for tag, team in (("A", team_a), ("B", team_b)):
        fs = []
        for lo in team:
            f = make_fighter(e, lo, f"{lo.name or game().hero(lo.hero).name} ({tag}{len(fs) + 1})")
            if allies:
                _team_items(f, lo)
            fs.append(f)
        sides.append(fs)
    for f in sides[0] + sides[1] if allies else ():
        for st in f.abilities:
            _share_ability(st)
    return e.run_team(*sides)


def _team_items(f, lo):
    """Swap duel item handlers for their team versions."""
    _, items = lo.resolve()
    by_class = {it.class_name: it for it in items}
    for i, fx in enumerate(list(f.items_fx)):
        it = getattr(fx, "item", None)
        cls = TEAM_ITEMS.get(getattr(it, "class_name", None))
        if cls is None or type(fx) is cls or type(fx).__module__ != items_fx.__name__:
            continue
        new = cls(by_class[it.class_name], f)
        f.items_fx[i] = new
        if hasattr(fx, "stat") and fx.stat in f.stat_hooks:
            f.stat_hooks.remove(fx.stat)
        if hasattr(new, "stat"):
            f.stat_hooks.append(new.stat)


def team_item_value(team_a, team_b, index, item, replace=None, **kw):
    """What one item on team_a[index] is worth to the whole team: fight with and without it (or with `replace`
    in its slot). Returns deltas for team A: damage dealt, damage taken, heals given, enemy kills, deaths, swing
    (health the enemy team lost minus health team A lost, so heals count), win."""
    def strip(lo, add):
        items = [i for i in lo.items if i != item] + ([add] if add else [])
        return dataclasses.replace(lo, items=items)
    with_ = list(team_a)
    if item not in with_[index].items:
        with_[index] = dataclasses.replace(with_[index], items=list(with_[index].items) + [item])
    without = list(with_)
    without[index] = strip(with_[index], replace)
    r1, r0 = team_fight(with_, team_b, **kw), team_fight(without, team_b, **kw)

    def stats(r):
        return {"damage": r.total("A", "damage"), "damage_taken": r.total("A", "damage_taken"),
                "healing_given": r.total("A", "healing_given") + r.total("A", "barrier_given"),
                "kills": r.total("A", "kills"), "deaths": sum(1 for x in r.team("A") if not x["alive"]),
                "swing": r.hp_lost("B") - r.hp_lost("A"),
                "win": 1 if r.winner == "A" else 0 if r.winner is None else -1, "time": r.time}
    s1, s0 = stats(r1), stats(r0)
    return {"with": s1, "without": s0, "delta": {k: s1[k] - s0[k] for k in s1}}
