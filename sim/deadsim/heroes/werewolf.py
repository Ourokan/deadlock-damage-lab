"""Silver (hero_werewolf).

Human form:
- Slam Fire: cast when the clip is down to its last shell, or at once for a first cast held to real cast timing
  (it reloads instantly, and refilling the clip mid-reload
  isn't modeled). The next MaxShots trigger pulls within AbilityDuration get +BonusFireRate% fire rate (T1: +15%
  weapon damage). Each pull that hits adds CurrentHealthDamagePercentage% of the target's current health as bullet
  damage, times (1 + AccuracyPercentage/100) for the accuracy penalty. T3: if all MaxShots pulls hit, +7% current
  health. The listed "Damage = 40" has no label or scaling and isn't used (guess: a trooper/neutral value).
- Boot Kick: a dash kick (skillshot) for 0.9x light melee as melee damage (Damage, only in raw/items.json,
  scales x0.9 ELightMeleeDamage; read through `alt`). It marks the target for MarkDuration, and the next gun hit on him deals BonusDamage spirit.
  T3: the kicked enemy deals -35% damage for DebuffDuration.
- Entangling Bola: skillshot spirit damage. The slow and the stamina lock are movement-only.

Lycan Curse (ult):
- Bloodlust: RagePerDamage per point of damage dealt (+LowHealthRageBonus% below LowHealthFraction hp) plus
  RagePercentagePerSecondInCombat% of MaxRage per second (the whole fight counts as combat). At MaxRage it is cast
  at once (the game auto-casts after ReadyDuration). MaxRage, BonusHealth and LowHealthRageBonus scale per boon.
  Fights on real timing (WOLF_TIMING, with Mechanics.execute_timing): rage and the cooldown carry over from earlier
  fights, which a duel starting at 0 rage missed (it transformed 7-12 s into nearly every duel, never at the start).
  Each fight draws its first transform from Phantom+ replays (data/wolf_timing.json, scripts/mechanics/
  wolf_timing.py): already in wolf form at the start (cast at t=0) in 12% of fights, else at a real time or not at
  all (on cooldown or held: ~40% of fights by 20 s); later casts follow the rage rule.
- Transform: +BonusHealth max health (current health goes up too), heal MissingHealthPercentHeal% of missing health,
  T1 +15% bullet/spirit resist, and the gun becomes Lycan Claws (raw weapon data; per-boon bullet damage from
  the hero's ALT_FIRE per-boon value; clip scaled like the rifle's clip items). Each claw hit adds a stack of
  BonusFireRate / MaxStacks fire rate (all stacks refresh to StackDuration), and adds BonusDurationOnBullet s to the
  form. Each 1% of health lost adds BonusDurationPerHealthPercentLost s. HeadshotResist and the T3 kill refresh are
  ignored. The claws (6 m) are assumed to reach: Silver closes in during the form.
- While transformed, each slot casts its wolf ability (slot mapping is a guess; the wolf abilities are not in
  abilities.json, so `alt` reads them from raw/items.json into an Ability and evaluates them with the slot's
  CastCtx rules: its upgrade tier, spirit power, light melee and duration bonuses):
    slot 1 -> Go For The Throat: 1.5x light melee + MissingHealthDamagePercentage% of the target's missing health
              as melee damage, healing LifeStealPercentOnHit% of the damage dealt.
    slot 2 -> Mauling Leap: 1.5x light melee as melee damage, -BulletArmorReduction% bullet resist (modeled as
              bullet shred) and DPS spirit DoT for DebuffDuration. Lands at spirit_accuracy.
    slot 3 -> Tail Whack: spirit Damage in a 10 m radius + disarm for DisarmDuration.
  Human and wolf versions keep separate cooldowns, both scaled by the slot's cooldown reduction.
"""
import dataclasses
import json
import math
import os
from functools import lru_cache

from deadsim.abilities import AbilityImpl, CastCtx, register
from deadsim.data import Ability, _load, _num

WOLF_KEY = "silver_wolf_until"
CLAWS = "citadel_weapon_werewolf_claws"
WOLF_TIMING = True
PLAN_HORIZON = 20.0   # s, the replay holds' horizon (null = not transformed by then)


@lru_cache(maxsize=1)
def wolf_timing():
    with open(os.path.join(os.path.dirname(__file__), "..", "..", "data", "wolf_timing.json")) as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def _raw():
    return {x["class_name"]: x for x in _load("raw/items.json") if x.get("class_name")}


@lru_cache(maxsize=None)
def raw_ability(class_name):
    """An Ability built from raw/items.json, for the wolf-form abilities (absent from abilities.json) and the
    Boot Kick damage (abilities.json drops it). Upgrades are split like deadsim.data does."""
    r = _raw().get(class_name, {})
    props, scale = {}, {}
    for k, v in (r.get("properties") or {}).items():
        if not isinstance(v, dict):
            continue
        props[k] = _num(v.get("value"))
        sf = v.get("scale_function") or {}
        if sf.get("stat_scale") is not None:
            scale[k] = (sf.get("class_name"), sf.get("specific_stat_scale_type"), _num(sf.get("stat_scale")) or 0.0)
    flat, special = [], []
    for u in r.get("upgrades") or []:
        fd, sd = {}, {}
        for pu in u.get("property_upgrades") or []:
            b = _num(pu.get("bonus"))
            if b is None:
                continue
            t = pu.get("upgrade_type")
            if t in (None, "EAddToBase"):
                fd[pu["name"]] = fd.get(pu["name"], 0.0) + b
            else:
                sd.setdefault(pu["name"], []).append((t, pu.get("scale_stat_filter"), b))
        flat.append(fd)
        special.append(sd)
    return Ability(r.get("id", 0), r.get("name", class_name), class_name, 0, "", False, props, scale, flat, {},
                   special)


class _AltState:
    """The slot's AbilityState (tier, spirit power, duration / range bonuses) seen through another Ability."""
    def __init__(self, s, ab):
        self._s, self.ab = s, ab

    def __getattr__(self, k):
        return getattr(self._s, k)


def alt(c, class_name):
    """CastCtx for class_name's raw data with the slot's tier and stats: alt(c, W).val("Damage") etc."""
    key = "_alt_" + class_name
    if key not in c.state:
        c.state[key] = CastCtx(_AltState(c.s, raw_ability(class_name)))
    return c.state[key]


def wolf(c):
    return c.me.counters.get(WOLF_KEY, -1.0) > c.now


def melee(c, amount, name):
    """Melee damage that returns what was dealt (for lifesteal)."""
    amount *= c.me.melee_mult()
    return c.engine.damage(c.me, c.foe, amount, "melee", name, is_ability=True, ability=c.s)


class WolfSlot(AbilityImpl):
    """A basic ability that is replaced by WOLF while Lycan Curse is active."""
    WOLF = ""
    WOLF_RANGE = "AbilityCastRange"

    def start(self, c):
        c.state.update(base_ready=0.0, wolf_ready=0.0)

    def should_cast(self, c):
        st = c.state
        if wolf(c):
            r = alt(c, self.WOLF).rng(self.WOLF_RANGE)
            return c.now >= st["wolf_ready"] and (r <= 0 or c.reach(r + c.me.skill.engage_margin))
        return c.now >= st["base_ready"] and self.base_ok(c)

    def base_ok(self, c):
        return self.in_range(c)

    def cast(self, c):
        st = c.state
        base_cd = c.raw("AbilityCooldown")
        keep = self.s.cooldown() / base_cd if base_cd else 1.0
        if wolf(c):
            st["wolf_ready"] = c.now + alt(c, self.WOLF).raw("AbilityCooldown") * keep
            self.wolf_cast(c)
        else:
            st["base_ready"] = c.now + self.s.cooldown()
            self.base_cast(c)
        self.s.reset_cooldown()   # cooldowns are tracked per form in scratch


@register("ability_werewolf_unloadgun")
class SlamFire(WolfSlot):
    kind = "self"
    held_opens = True   # a held first cast skips its gate (fit_cast_timing.py measures it with PROBE_HELD)
    WOLF = "ability_werewolf_frenzy"

    def start(self, c):
        super().start(c)
        c.state.update(shots=0, until=-1.0, armed=False, landed=0)

    def base_ok(self, c):
        # a first cast held to real cast timing (mechanics.cast_timing) opens with it whatever the clip
        return c.foe.alive and (c.me.clip == 1 or self.s.held_opener()) and c.me.reload_until <= c.now

    def base_cast(self, c):
        st = c.state
        d = c.raw("AbilityCastDelay")
        c.lock_gun(d)
        c.me.clip = c.me.st.clip
        dur = c.dur("AbilityDuration")
        st.update(shots=int(c.raw("MaxShots", 3)), until=c.now + d + dur, armed=False, landed=0)
        c.buff("fire_rate", c.raw("BonusFireRate") / 100, d + dur, tag="slam_fire_fr")

    def on_shot(self, c, ctx):
        st = c.state
        if st["shots"] <= 0 or c.now > st["until"]:
            return
        st["shots"] -= 1
        st["armed"] = True
        ctx["extra_pct"] += c.raw("BaseAttackDamagePercent") / 100
        if st["shots"] == 0:
            c.me.mods.remove("fire_rate", "slam_fire_fr")

    def on_damage_dealt(self, c, target, hit):
        st = c.state
        if not st["armed"] or hit.source != "gun" or hit.kind != "bullet" or not hit.hits:
            return
        st["armed"] = False
        st["landed"] += 1
        acc = max(0.0, 1.0 + c.raw("AccuracyPercentage") / 100)
        c.bullet_hit(c.raw("CurrentHealthDamagePercentage") / 100 * c.foe.hp * acc)
        if st["shots"] == 0 and st["landed"] >= c.raw("MaxShots", 3) and c.raw("BonusCurrentHealthDamagePercentage"):
            c.bullet_hit(c.raw("BonusCurrentHealthDamagePercentage") / 100 * c.foe.hp)

    def wolf_cast(self, c):   # Go For The Throat
        w = alt(c, self.WOLF)
        d = w.raw("AbilityCastDelay", 0.2)
        c.lock_gun(d + w.raw("AbilityPostCastDuration", 0.5))
        c.after(d, self._throat, c)

    def _throat(self, c):
        if not c.me.alive or not c.foe.alive:
            return
        w = alt(c, self.WOLF)
        missing = c.foe.max_hp - c.foe.hp
        dmg = w.val("Damage") + w.val("MissingHealthDamagePercentage") / 100 * missing
        dealt = melee(c, dmg, "Go For The Throat")
        if dealt:
            c.heal(dealt * w.val("LifeStealPercentOnHit") / 100)


@register("ability_werewolf_kickflip")
class BootKick(WolfSlot):
    kind = "skillshot"
    WOLF = "ability_werewolf_maulingleap"

    def start(self, c):
        super().start(c)
        c.state["mark_until"] = -1.0

    def base_cast(self, c):
        d = c.raw("AbilityCastDelay") + c.raw("AbilityChannelTime")
        c.lock_gun(d + c.raw("AbilityPostCastDuration"))
        acc = c.me.skill.spirit_accuracy
        kick = alt(c, self.s.ab.class_name).val("Damage")
        c.after(d, self._kick, c, kick * acc, acc)

    def _kick(self, c, dmg, acc):
        if not c.me.alive:
            return
        melee(c, dmg, self.s.ab.name)
        c.state["mark_until"] = c.now + c.dur("MarkDuration")
        c.state["mark_acc"] = acc
        if c.raw("OutgoingDamagePercent"):
            c.debuff("outgoing_penalty", abs(c.raw("OutgoingDamagePercent")) / 100 * acc, c.dur("DebuffDuration"))

    def on_damage_dealt(self, c, target, hit):
        st = c.state
        if hit.source == "gun" and hit.kind == "bullet" and hit.hits and c.now < st["mark_until"]:
            st["mark_until"] = -1.0
            c.spirit_hit(c.val("BonusDamage") * st.get("mark_acc", 1.0), hit_chance=1.0)

    def wolf_cast(self, c):   # Mauling Leap
        w = alt(c, self.WOLF)
        d = w.raw("AbilityCastDelay", 0.35) + w.raw("AbilityChannelTime", 0.55)
        c.lock_gun(d)
        c.after(d, self._maul, c, c.me.skill.spirit_accuracy)

    def _maul(self, c, acc):
        if not c.me.alive or not c.foe.alive:
            return
        w = alt(c, self.WOLF)
        melee(c, w.val("Damage") * acc, "Mauling Leap")
        dur = w.dur("DebuffDuration", 6.0)
        c.debuff("bullet_shred", abs(w.val("BulletArmorReduction")) / 100 * acc, dur, tag="mauling_leap")
        c.dot(w.val("DPS"), dur, tick=w.raw("TickRate", 0.5), name="Mauling Leap", hit_chance=acc)


@register("ability_werewolf_netshot")
class EntanglingBola(WolfSlot):
    kind = "skillshot"
    WOLF = "ability_werewolf_cripplingslash"
    WOLF_RANGE = "SlashRadius"

    def base_ok(self, c):
        return c.reach(25.0 + c.me.skill.engage_margin)   # thrown projectile, no cast range in data

    def base_cast(self, c):
        d = c.raw("AbilityCastDelay")
        c.lock_gun(d)
        c.spirit_hit(c.val("Damage"), delay=d)

    def wolf_cast(self, c):   # Tail Whack
        w = alt(c, self.WOLF)
        d = w.raw("AbilityCastDelay", 0.15)
        c.lock_gun(d)
        c.spirit_hit(w.val("Damage"), delay=d, name="Tail Whack", hit_chance=1.0)
        c.debuff("disarm", 1, w.dur("DisarmDuration", 2.0), delay=d)


@register("ability_werewolf_transformation")
class LycanCurse(AbilityImpl):
    kind = "self"

    def start(self, c):
        c.state.update(rage=0.0, stacks=0, orig=None)
        c.after(0.5, self.tick, c)

    def max_rage(self, c):
        return c.val("MaxRage")

    def tick(self, c):
        if not c.me.alive or c.engine.over:
            return
        if not wolf(c):
            c.state["rage"] += self.max_rage(c) * c.raw("RagePercentagePerSecondInCombat") / 100 * 0.5
        c.after(0.5, self.tick, c)

    def draw_plan(self, c, u):
        """Mechanics.execute_timing: this fight's first transform from draw u (mechanics.execute_plans): at the start
        (already in wolf form), at a real time, or not (inf)."""
        if not WOLF_TIMING:
            return
        d = wolf_timing()
        p0 = d["start_wolf"]
        if u < p0:
            c.state["plan_at"] = c.now
            return
        q = d["holds"]
        h = q[min(len(q) - 1, int((u - p0) / (1.0 - p0) * len(q)))]
        c.state["plan_at"] = math.inf if h is None else c.now + h
        c.state["plan_end"] = c.now + PLAN_HORIZON   # past the data's horizon, the rage rule again

    def should_cast(self, c):
        if not c.foe.alive or wolf(c):
            return False
        at = c.state.get("plan_at")
        if at is not None and c.now >= c.state.get("plan_end", math.inf):
            c.state.pop("plan_at")
            at = None
        if at is not None:   # first transform on real timing (draw_plan)
            return c.now >= at
        return c.state["rage"] >= self.max_rage(c)

    def on_damage_dealt(self, c, target, hit):
        st = c.state
        if not wolf(c):
            g = hit.amount * c.raw("RagePerDamage")
            if c.me.hp_frac < c.raw("LowHealthFraction") / 100:
                g *= 1.0 + c.val("LowHealthRageBonus") / 100
            st["rage"] += g
        elif hit.source == "gun" and hit.kind == "bullet" and hit.hits:
            c.me.counters[WOLF_KEY] += c.raw("BonusDurationOnBullet") * hit.hits
            st["stacks"] = min(int(c.raw("MaxStacks", 15)), st["stacks"] + hit.hits)
            per = c.val("BonusFireRate") / 100 / c.raw("MaxStacks", 15)
            c.buff("fire_rate", per * st["stacks"], c.raw("StackDuration", 5), tag="lycan_fr")

    def on_damage_taken(self, c, src, hit):
        if wolf(c) and hit.amount > 0:
            pct = hit.amount / c.me.max_hp * 100
            c.me.counters[WOLF_KEY] += c.raw("BonusDurationPerHealthPercentLost") * pct

    def cast(self, c):
        f = c.me
        st = c.state
        c.lock_gun(c.raw("AbilityCastDelay"))
        st.update(rage=0.0, stacks=0)
        st.pop("plan_at", None)
        f.counters[WOLF_KEY] = c.now + c.dur("AbilityDuration")
        bonus = c.val("BonusHealth")
        f.mods.add("max_health", bonus, 1e9, "lycan_hp")
        f.hp += bonus
        c.heal((f.max_hp - f.hp) * c.raw("MissingHealthPercentHeal") / 100)
        if c.raw("BulletResist"):
            f.mods.add("bullet_resist", c.raw("BulletResist") / 100, 1e9, "lycan_br")
            f.mods.add("spirit_resist", c.raw("TechResist") / 100, 1e9, "lycan_sr")
        # weapon swap to Lycan Claws
        orig = f.st
        cw = _raw().get(CLAWS, {}).get("weapon_info") or {}
        rifle = orig.hero.weapon
        clip_scale = orig.clip / max(1, rifle.get("clip_size", orig.clip))
        f.st = dataclasses.replace(
            orig, hero=dataclasses.replace(orig.hero, weapon=cw),
            bullet_damage=cw.get("bullet_damage", 25.0)
            + orig.boons * orig.hero.per_boon.get("MODIFIER_VALUE_BASE_BULLET_DAMAGE_FROM_LEVEL_ALT_FIRE", 0.0),
            pellets=int(cw.get("bullets", 1) or 1), cycle_time=cw.get("cycle_time", 0.5),
            burst_count=int(cw.get("burst_shot_count", 1) or 1),
            burst_interval=cw.get("intra_burst_cycle_time", 0.0) or 0.0,
            clip=max(1, int(round(cw.get("clip_size", 12) * clip_scale))),
            reload_time=cw.get("reload_duration", 1.5) * orig.reload_mult)
        f.clip = f.st.clip
        st["orig"] = orig
        for ab in f.abilities:   # wolf abilities start ready
            if isinstance(ab.impl, WolfSlot):
                ab.scratch["wolf_ready"] = 0.0
        c.after(0.25, self.watch, c)

    def watch(self, c):
        f = c.me
        if not f.alive or c.engine.over:
            return
        if wolf(c):
            c.after(0.25, self.watch, c)
            return
        st = c.state
        for key, tag in (("max_health", "lycan_hp"), ("bullet_resist", "lycan_br"), ("spirit_resist", "lycan_sr"),
                         ("fire_rate", "lycan_fr")):
            f.mods.remove(key, tag)
        f.hp = min(f.hp, f.max_hp)
        if st.get("orig") is not None:
            f.st = st["orig"]
            st["orig"] = None
            f.clip = min(f.clip, f.st.clip) if f.clip > 0 else f.clip
        st["rage"] = 0.0
