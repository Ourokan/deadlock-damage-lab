"""Conditional, proc and active item effects. Always-on stats are summed in build.py instead.

Each handler is a small class keyed by the item's class_name. Hooks the engine calls (all optional):
    on_start(f)                         fight begins
    on_shot(f, ctx)                     before a trigger pull resolves; may edit ctx (extra_pct, pellet_mult, ...)
    on_damage_dealt(f, target, hit)     after f damages target
    on_damage_taken(f, attacker, hit)   after f takes damage
    reduce_incoming(f, attacker, amount, kind, is_dot) -> amount
    on_lethal(f, attacker) -> bool      return True if death was prevented
    on_kill(f, target)                  f killed target (or an immortal target refilled, engine.kill_hooks)
    on_cast(f, ability_state)           f cast an ability
    on_enemy_cast(f, ability_state)     the enemy cast an ability
    on_cc(f, key)                       f just received stun / silence / disarm / immobilize
    on_reload(f)
    try_active(f) -> bool               use an active item now if it makes sense (called every 0.1 s)
    stat(f) -> dict                     dynamic modifiers (e.g. {"weapon_pct": .18} while above 65% hp)
Items not listed here only contribute their always-on stats; `MODELED` lets reports flag that.
"""
from __future__ import annotations

from .abilities import CastCtx

HANDLERS = {}


def _duration_scaled():
    import json
    import os
    path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "game", "shop_items.json")
    out = set()
    try:
        for it in json.load(open(path)):
            for k, v in it["properties"].items():
                sc = v.get("scale") or {}
                if sc.get("specific_stat_scale_type") == "ETechDuration" or sc.get("class_name") == "scale_function_tech_duration":
                    out.add((it["class_name"], k))
    except (OSError, ValueError, KeyError):
        pass
    return out


DURATION_SCALED = _duration_scaled()
CC_KEYS = ("stun", "silence", "disarm", "immobilize")


def held_share(t):
    """How much of a ground zone's tick a target that wants to walk out still takes: all of it while stunned or
    immobilized, the slowed share while slowed (a 40% slow keeps it in 40% as long), none otherwise. So a hero with
    no hold (Haze) only gets the first zone_exit_s of Alchemical Fire, and one with stuns or slows gets more."""
    if t.mods.active("stun") or t.mods.active("immobilize"):
        return 1.0
    slow = 1.0
    for v in t.mods.values("move_slow"):
        slow *= 1.0 - v
    return min(0.9, 1.0 - slow)


def handler(*class_names):
    def deco(cls):
        for n in class_names:
            HANDLERS[n] = cls
        return cls
    return deco


def item_value(item, prop, f, default=0.0):
    """Item property with its scaling: spirit power, boons, healing scales."""
    v = item.props.get(prop)
    v = default if v is None else v
    sc = item.scale.get(prop)
    if sc:
        cls, stype, k = sc
        if stype == "ELevelUpBoons" or cls == "scale_function_healing_boon_scale":
            v += k * f.st.boons
        elif cls == "scale_function_tech_damage" or stype == "ETechPower" or cls == "scale_function_healing_spirit_scale":
            v += k * f.spirit_power()
    return v


def shots_hit(f, hit):
    """Shot-equivalents that hit: pellets / pellets per shot. Flat per-bullet bonuses and proc chances are per shot,
    so a 9-pellet shotgun gets them once per full shot, not 9 times."""
    return hit.hits / max(1, f.st.pellets)


class FX:
    def __init__(self, item, f):
        self.item = item
        self.f = f
        self.ready_at = 0.0

    def v(self, prop, default=0.0):
        return item_value(self.item, prop, self.f, default)

    @property
    def name(self):
        return self.item.name

    @property
    def now(self):
        return self.f.e.t

    def cd(self, prop="AbilityCooldown"):
        base = self.item.p(prop)
        if self.item.activation != "passive":
            return base * (1.0 - self.f.st.item_cdr)
        return base

    def ready(self):
        return self.now >= self.ready_at

    def dur(self, prop, default=0.0):
        """Duration property, lengthened by bonus duration (Superior Duration etc.) when the game scales it with
        ETechDuration (e.g. Decay's 12 s)."""
        v = self.item.p(prop, default)
        if (self.item.class_name, prop) in DURATION_SCALED:
            v *= 1.0 + self.f.st.duration_pct
        return v

    def use(self, prop="AbilityCooldown"):
        self.ready_at = self.now + self.cd(prop)

    def debuff(self, target, key, value, duration, tag=None):
        dur = duration * max(0.0, 1.0 - target.st.status_resist - target.stat("status_resist"))
        target.mods.add(key, value, dur, tag or (self.item.class_name, key))
        target.mark_debuff(key, tag or (self.item.class_name, key))
        if key in CC_KEYS:
            for fx in target.items_fx:
                g = getattr(fx, "on_cc", None)
                if g:
                    g(target, key)

    def buff(self, key, value, duration, tag=None):
        self.f.mods.add(key, value, duration, tag or (self.item.class_name, key))

    def spirit(self, target, amount, name=None, **kw):
        return self.f.e.damage(self.f, target, amount, "spirit", name or self.item.name, is_item=True, **kw)

    def in_range(self, meters):
        return self.f.e.distance <= meters + 0.5

    def reach_p(self, meters):
        """Share of fight time the target is within `meters` (1 / 0 without range spread)."""
        return self.f.e.p_within(meters + 0.5)

    def ready_in(self, meters):
        """Gate for an active that needs the target within `meters`: now / never without range spread, after the
        expected wait for the drift to bring the target in with it (Engine.reach_ready)."""
        st = self.__dict__.setdefault("_reach_state", {})
        if self.f.e.reach_ready(st, meters + 0.5, self.f):
            st.pop("_walk_in_at", None)
            return True
        return False


class BuildUp(FX):
    """Bullets build a % meter; at 100% the effect procs. Meter decays after BuildUpDuration without hits.

    Build-up per bullet is hero-specific in the game: proportional to the gun's base damage per bullet
    (deadlock.wiki lists Toxic Bullets at 47% per full Abrams shotgun shot, 8.2% Ivy, 17.6% Lash, 10.3% Wraith,
    which is BuildUpPerShot x base bullet damage x 1.13-1.63, about 1.4), and reduced by distance falloff the
    same way as bullet damage. Headshots don't add more."""
    per_prop = "BuildUpPerShot"
    scale = 1.4  # wiki fit, see above

    def per_hit(self, f):
        # a charged shot (Danny) is gun_charge base bullets' worth of damage, and builds up as much
        base = ((f.st.weapon or {}).get("bullet_damage", 0.0) or 1.0) * f.st.gun_charge
        return self.item.p(self.per_prop) * self.scale * base * f.e.hit_falloff(f.st)

    def __init__(self, item, f):
        super().__init__(item, f)
        self.meter = 0.0
        self.last = -99.0
        self.immune_until = 0.0

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "bullet" or not hit.hits or hit.is_ability:
            return
        if self.now < self.immune_until:
            return
        if self.now - self.last > self.dur("BuildUpDuration", 5.0):
            self.meter = 0.0
        self.last = self.now
        self.meter += self.per_hit(f) * hit.hits
        if self.meter >= 100.0:
            self.meter = 0.0
            self.proc(f, t)

    def proc(self, f, t):
        pass


# ---------------------------------------------------------------------------------------------------
# Weapon items
# ---------------------------------------------------------------------------------------------------
@handler("upgrade_pristine_emblem")
class OpeningRounds(FX):
    def stat(self, f):
        return {"weapon_pct": self.item.p("BaseAttackDamagePercentBonus") / 100} if f.enemy and f.enemy.hp_frac > 0.5 else {}


@handler("upgrade_close_range", "upgrade_close_quarter_combat")
class CloseRange(FX):
    def stat(self, f):
        p = f.e.p_within(self.item.p("CloseRangeBonusDamageRange", 15))
        return {"weapon_pct": p * self.item.p("CloseRangeBonusWeaponPower") / 100} if p > 0 else {}

    def range_band(self):
        return self.item.p("CloseRangeBonusDamageRange", 15), self.item.p("CloseRangeBonusWeaponPower") / 100, True


@handler("upgrade_long_range", "upgrade_sharpshooter")
class LongRange(FX):
    def stat(self, f):
        p = 1.0 - f.e.p_within(self.item.p("LongRangeBonusWeaponPowerMinRange", 15) - 1e-6)
        return {"weapon_pct": p * self.item.p("LongRangeBonusWeaponPower") / 100} if p > 0 else {}

    def range_band(self):
        return self.item.p("LongRangeBonusWeaponPowerMinRange", 15), self.item.p("LongRangeBonusWeaponPower") / 100, False


@handler("upgrade_regenerating_bullet_shield")
class BattleVest(FX):
    def stat(self, f):
        if f.hp_frac > self.item.p("LifeThreshold", 65) / 100:
            return {"weapon_pct": self.item.p("BaseAttackDamagePercent") / 100, "fire_rate": self.item.p("BonusFireRate") / 100}
        return {}


@handler("upgrade_hollow_point_rounds")
class HollowPoint(FX):
    def stat(self, f):
        return {"weapon_pct": self.item.p("BaseAttackDamagePercent") / 100} if f.hp_frac > self.item.p("LifeThreshold", 65) / 100 else {}

    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "bullet" and hit.hits and f.hp_frac > self.item.p("LifeThreshold", 65) / 100:
            self.debuff(t, "bullet_shred", abs(self.item.p("BulletArmorReduction")) / 100, self.dur("DebuffDuration", 8))


@handler("upgrade_headshot_booster", "upgrade_headhunter")
class HeadshotBonus(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "bullet" and hit.headshots and not hit.is_ability and self.ready():
            self.use()
            f.e.damage(f, t, self.v("HeadShotBonusDamage"), "bullet", self.name, procs=False, is_item=True)
            hp = self.v("HealPercentPerHeadshot")
            if hp:
                f.heal(f.max_hp * hp / 100, self.name)


@handler("upgrade_headshot_booster2")
class WeakeningHeadshot(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "bullet" and hit.headshots:
            self.debuff(t, "bullet_shred", abs(self.item.p("BulletResistReduction")) / 100, self.dur("DebuffDuration", 12))


@handler("upgrade_banshee_slugs")
class CripplingHeadshot(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "bullet" and hit.headshots:
            d = self.dur("DebuffDuration", 12)
            self.debuff(t, "bullet_shred", abs(self.item.p("BulletResistReduction")) / 100, d)
            self.debuff(t, "spirit_shred", abs(self.item.p("MagicResistReduction")) / 100, d)
            self.debuff(t, "heal_received", self.item.p("HealAmpReceivePenaltyPercent") / 100, d)


@handler("upgrade_tech_defense_shredders", "upgrade_spellslinger_headshots")
class SpiritShredder(FX):
    def __init__(self, item, f):
        super().__init__(item, f)
        self.stacks = []

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "bullet" or not hit.hits:
            return
        d = self.dur("DebuffDuration", 8)
        self.debuff(t, "spirit_shred", abs(self.item.p("TechArmorDamageReduction")) / 100, d)
        f.mods.add("spirit_lifesteal", self.item.p("AbilityLifestealPercentHero") / 100, d, (self.item.class_name, "ls"))
        if self.item.class_name == "upgrade_spellslinger_headshots" and hit.headshots and self.ready():
            self.ready_at = self.now + self.item.p("ProcCooldown", 2)
            n = int(self.item.p("MaxStacks", 4))
            k = self.f.counters.get("rend", 0) % n
            self.f.counters["rend"] = k + 1
            self.debuff(t, "spirit_shred", abs(self.item.p("MagicResistReduction")) / 100, d, tag=("rend", k))


@handler("upgrade_toxic_bullets")
class ToxicBullets(BuildUp):
    def proc(self, f, t):
        d = self.dur("DotDuration", 4)
        pct = self.v("DotHealthPercent") / 100
        f.e.dot(f, t, pct * t.max_hp, d, self.name, kind="spirit", tick=self.item.p("TickRate", 0.5), is_item=True,
                buildup=True)
        self.debuff(t, "heal_received", self.item.p("HealAmpReceivePenaltyPercent") / 100, d)


@handler("upgrade_chain_lightning", "upgrade_capacitor")
class TeslaBullets(FX):
    # the shock has its own 0.2 s proc timer: Capacitor's 40 s active cooldown (ready_at) must not switch it off
    # (it did until 2026-10-24: sim Capacitor shock damage per gun damage was 1/4.6 of real Phantom+ holders)
    proc_at = 0.0

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "bullet" or not hit.hits or hit.is_ability or self.now < self.proc_at:
            return
        # proc chance is per shot, not per pellet (shotguns): chance that at least one of the shots that hit procs
        p = 1.0 - (1.0 - self.item.p("ProcChance") / 100) ** shots_hit(f, hit)
        n = f.acc(self.item.class_name).take(p, 1)
        if n:
            self.proc_at = self.now + self.item.p("ProcCooldown", 0.2)
            self.spirit(t, self.v("DamagePerChain"))

    def try_active(self, f):  # Capacitor's projectile
        if self.item.class_name != "upgrade_capacitor" or not self.ready() or not f.skill.use_actives:
            return False
        if self.item.props.get("Damage"):
            self.use()
            self.spirit(f.enemy, self.v("Damage") * f.skill.spirit_accuracy)
            return True
        return False


@handler("upgrade_critshot")
class LuckyShot(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "bullet" or not hit.hits or hit.is_ability:
            return
        n = f.acc("lucky").take(self.item.p("ProcChance") / 100, hit.hits)
        if n:
            per = f.counters.get("bullet_per", 0.0)
            f.e.damage(f, t, per * n * self.item.p("CritDamagePercent") / 100, "bullet", self.name, procs=False, is_item=True)


@handler("upgrade_aprounds")
class ArmorPiercer(FX):
    def on_shot(self, f, ctx):
        ctx["ignore_resist_frac"] = max(ctx["ignore_resist_frac"], self.item.p("ProcChance") / 100)


@handler("upgrade_express_shot")
class ExpressShot(FX):
    def on_shot(self, f, ctx):
        if self.ready():
            self.use()
            ctx["extra_pct"] += self.v("ProcBaseAttackDamagePercent") / 100
            ctx["pellet_mult"] *= 2
            ctx["book"] = self.name   # the game books the whole proc shot under the item (replays: ~2x a gun hit)
            f.clip = max(0, f.clip - int(self.item.p("ProcAmmoConsumed", 2)) + 1)


@handler("upgrade_intensifying_clip")
class IntensifyingMagazine(FX):
    def stat(self, f):
        if f.shooting_since is None:
            return {}
        frac = min(1.0, (f.e.t - f.shooting_since) / self.item.p("ShootDurationForMax", 2.5))
        return {"weapon_pct": frac * self.dur("BaseAttackDamagePercentAtMaxDuration") / 100}


@handler("upgrade_burst_fire")
class BurstFire(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "bullet" and hit.hits and self.ready():
            self.use()
            self.buff("fire_rate", self.item.p("ActivatedFireRate") / 100, self.dur("AbilityDuration", 4.5))


@handler("upgrade_berserker")
class Berserker(FX):
    def __init__(self, item, f):
        super().__init__(item, f)
        self.acc_dmg = 0.0
        self.k = 0

    def on_damage_taken(self, f, src, hit):
        self.acc_dmg += hit.amount
        per = self.item.p("DamageToStack", 120)
        while self.acc_dmg >= per:
            self.acc_dmg -= per
            n = int(self.item.p("MaxStacks", 10))
            self.k = (self.k + 1) % n
            f.mods.add("weapon_pct", self.item.p("WeaponPowerPerStack") / 100, self.dur("DamageDuration", 10), ("bers", self.k))


@handler("upgrade_tech_overflow")
class SpiritualOverflow(BuildUp):
    def proc(self, f, t):
        d = self.dur("AbilityDuration", 15)
        self.buff("fire_rate", self.item.p("BonusFireRate") / 100, d)
        self.buff("spirit_power", self.item.p("BonusSpirit"), d)
        self.buff("spirit_lifesteal", self.item.p("BonusSpiritLifesteal") / 100, d)
        self.immune_until = self.now + d


@handler("upgrade_crackshot")
class MysticShot(FX):
    """Real fights don't open with the proc ready: 62% of Mystic Shot damage lands on creeps and troopers, so the
    cooldown is usually part spent when a hero fight starts. Starting it ready made the sim give 0.45 x gun damage
    vs 0.32 real (126 holders, damage matrix over the held window). The cooldown starts at a random point of its
    cycle (half-way when the engine is deterministic), which gives 0.31. Kinetic Carbine also procs it
    (Hit.weapon_proc)."""

    def on_start(self, f):
        rng = f.e.rng
        self.ready_at = self.now + self.cd() * (rng.random() if rng is not None else 0.5)

    def on_damage_dealt(self, f, t, hit):
        gun_hit = (hit.kind == "bullet" and hit.hits and not hit.is_ability) or hit.weapon_proc
        if gun_hit and self.ready():
            self.use()
            self.spirit(t, self.v("ProcBonusMagicDamage"))


@handler("upgrade_rechargingbullets")
class RechargingRush(FX):
    def __init__(self, item, f):
        super().__init__(item, f)
        self.window = []

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "bullet" or not self.ready():
            return
        now = self.now
        self.window = [(x, a) for x, a in self.window if now - x <= self.item.p("DamageWindow", 3.5)] + [(now, hit.amount)]
        if sum(a for _, a in self.window) >= self.item.p("DamageThreshold", 200):
            self.use()
            self.window = []
            for ab in f.abilities:
                if ab.is_charged() and ab.charges < ab.max_charges():
                    ab.charges += 1


@handler("upgrade_weapon_backstabber")
class Stalker(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "bullet" and hit.hits and self.ready() and \
                f.acc("stalker_reach").take(self.reach_p(self.item.p("ProcRadius", 8)), 1):
            self.use()
            d = self.dur("DebuffDuration", 5)
            f.e.dot(f, t, self.v("DPS"), d, self.name, tick=self.item.p("TickRate", 0.5), is_item=True)
            self.debuff(t, "bullet_shred", abs(self.item.p("BulletResistReduction")) / 100, d)


@handler("upgrade_bullet_armor_reduction_aura")
class HuntersAura(FX):
    def on_start(self, f):
        e = f.enemy
        mult = self.item.p("SingleTargetPlayerMultiplier", 2)  # 1v1: only one hero nearby
        radius = self.item.p("Radius", 15)
        shred = abs(self.item.p("BulletArmorReduction")) / 100 * mult
        slow = self.item.p("FireRateSlow") / 100 * mult
        p = f.e.p_within(radius)   # share of the fight the target stands in the aura
        e.stat_hooks.append(lambda x: {"fire_rate_slow": slow * p} if p > 0 else {})
        if p > 0:
            e.mods.add("bullet_shred", shred * p, 1e9, ("hunters", f.name))


@handler("upgrade_proc_silence")
class Silencer(BuildUp):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "bullet" and hit.hits:
            self.debuff(t, "spirit_outgoing_penalty", abs(self.item.p("TechDamageReduction")) / 100, self.dur("DebuffDuration", 6))
        super().on_damage_dealt(f, t, hit)

    def proc(self, f, t):
        d = self.dur("SilenceDuration", 2.5)
        self.debuff(t, "silence", 1, d)
        self.immune_until = self.now + d + self.dur("ImmunityDuration", 10)


@handler("upgrade_inhibitor")
class Inhibitor(BuildUp):
    def proc(self, f, t):
        d = self.dur("DebuffDuration", 5)
        self.debuff(t, "outgoing_penalty", abs(self.item.p("OutgoingDamagePenaltyPercent")) / 100, d)
        self.debuff(t, "heal_received", self.item.p("HealAmpReceivePenaltyPercent") / 100, d)


@handler("upgrade_slowing_bullets", "upgrade_weighted_shots")
class SlowBullets(BuildUp):
    pass  # movement slow only; no effect on a stand-still duel


@handler("upgrade_siphon_bullets")
class SiphonBullets(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "bullet" and hit.hits and not hit.is_ability and self.ready():
            self.ready_at = self.now + self.item.p("ProcCooldown", 1.2)
            amt = t.max_hp_base * self.item.p("HealthStealPctHero") / 100
            # realistic mode: the real-data factor scales the whole steal (cap drop, health taken, heal) alike, so the
            # damage below is not marked is_item (that would scale only the health taken)
            amt *= (f.skill.item_landing or {}).get(self.name, 1.0)
            d = self.dur("StealDuration", 17)
            k = f.counters.get("siphon", 0) + 1
            f.counters["siphon"] = k
            t.mods.add("max_health", -amt, d, ("siphon", k))
            # the stolen health is taken from current health too: the game books it as Siphon Bullets damage
            # (real Phantom+ holders: 0.24 Siphon damage per gun damage, sim was 0 while it only lowered the cap)
            f.e.damage(f, t, amt, "spirit", self.name, procs=False, pure=True)
            t.hp = min(t.hp, t.max_hp)
            f.mods.add("max_health", amt, d, ("siphon", k))
            f.heal(amt, self.name)


@handler("upgrade_reinforcing_casings")
class EscalatingResilience(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "bullet" and hit.hits:
            k = f.counters.get("escres", 0)
            if k < self.item.p("MaxArmorStacks", 30):
                f.counters["escres"] = k + 1
                f.mods.add("escres_stack", 1, self.dur("BulletResistDuration", 24), ("escres", k))

    def stat(self, f):
        n = len(f.mods.values("escres_stack"))
        return {"bullet_resist": n * self.item.p("BulletResistPerStack", 2) / 100} if n else {}


@handler("upgrade_active_reload")
class ActiveReload(FX):
    success = 0.75   # share of reloads timed right (assumption)

    def on_reload(self, f):
        if self.ready() and f.acc("active_reload").take(self.success):
            self.use()
            f.reload_until = self.now + (f.reload_until - self.now) * 0.55
            self.f.e.at(f.reload_until, lambda: None)
            d = self.dur("AbilityDuration", 7)
            self.buff("fire_rate", self.item.p("BonusFireRate") / 100, d)
            self.buff("bullet_lifesteal", self.item.p("BulletLifestealPercent") / 100, d)


@handler("upgrade_kinetic_sash")
class KineticDash(FX):
    def on_start(self, f):
        if f.skill.use_actives:   # assumes a dash-jump into the fight
            d = self.dur("AbilityDuration", 7)
            self.buff("fire_rate", self.item.p("BonusFireRate") / 100, d, tag="kd")
            f.bonus_ammo += int(self.item.p("BonusClipSize"))

    def on_reload(self, f):
        f.mods.remove("fire_rate", "kd")


@handler("upgrade_enchanted_holsters")
class Spellslinger(FX):
    def on_cast(self, f, ab):
        n = int(self.item.p("MaxStacks", 6))
        k = f.counters.get("sling", 0)
        f.counters["sling"] = k + 1
        d = self.dur("BuffDuration", 18)
        for j in range(min(k + 1, n)):   # each stack refreshes the duration
            f.mods.add("fire_rate", self.item.p("BonusFireRate") / 100, d, ("sling", j))
            f.mods.add("reload_mult", self.item.p("ReloadSpeedMultipler") / 100, d, ("sling", j))


@handler("upgrade_fervor")
class Frenzy(FX):
    def on_damage_taken(self, f, src, hit):
        if f.hp_frac < self.item.p("LowHealthThreshold", 50) / 100 and self.ready():
            self.use()
            d = self.dur("AbilityDuration", 10)
            self.buff("fire_rate", self.item.p("FervorFireRate") / 100, d)
            self.buff("status_resist", self.item.p("FervorStatusResistancePercent") / 100, d)


@handler("upgrade_dps_aura")
class HeroicAura(FX):
    def stat(self, f):
        return {}

    def try_active(self, f):
        if self.ready():
            self.use()
            self.buff("fire_rate", self.item.p("BonusFireRate") / 100, self.dur("AbilityDuration", 7))
            return True
        return False


@handler("upgrade_cloaking_device_active")
class ShadowWeave(FX):
    def on_start(self, f):
        if f.skill.use_actives:   # opens the fight from stealth (ambush)
            d = self.dur("AmbushDuration", 5)
            self.buff("fire_rate", self.item.p("AmbushBonusFireRate") / 100, d)
            self.buff("spirit_power", self.item.p("AmbushBonusTechPower"), d)
            self.ready_at = 1e9


@handler("upgrade_thermal_detonator")
class AlchemicalFire(FX):
    def try_active(self, f):
        r = self.item.p("Radius", 10)
        if not self.ready() or not self.ready_in(r + 5):
            return False
        self.use()
        d = self.dur("AbilityDuration", 5)
        dps, inc, mx = self.v("DPS"), self.v("DPSIncrease"), self.v("DPSMax")
        t = f.enemy
        exit_s = t.skill.zone_exit_s   # counterplay: the target walks out of the fire unless something holds it
        for i in range(int(d / 0.5 + 1e-9)):
            cur = min(mx, dps + inc * (i * 0.5))
            f.e.after(0.5 * (i + 1), lambda c=cur, k=i: self._tick(f, t, c, exit_s is None or 0.5 * (k + 1) <= exit_s + 1e-9))
        self.debuff(t, "bullet_shred", abs(self.v("BulletArmorReduction")) / 100, d if exit_s is None else min(d, exit_s))
        return True

    def _tick(self, f, t, cur, inside):
        share = 1.0 if inside else held_share(t)
        if share > 0:
            self.spirit(t, cur * 0.5 * share * f.skill.spirit_accuracy, is_dot=True)
            if not inside:   # still held in the fire: its bullet shred stays on until the next tick
                self.debuff(t, "bullet_shred", abs(self.v("BulletArmorReduction")) / 100, 0.5 * share + 0.01)


@handler("upgrade_blood_tribute")
class BloodTribute(FX):
    def on_start(self, f):
        if f.skill.use_actives:
            self.buff("fire_rate", self.item.p("BonusFireRate") / 100, 1e9)
            self.buff("status_resist", self.item.p("StatusResistancePercent") / 100, 1e9)
            self.buff("health_drain", self.item.p("HealthDrainedPerSecond"), 1e9)


@handler("upgrade_non_player_bonus_sacrifice")
class CultistSacrifice(FX):
    def on_start(self, f):
        if f.skill.use_actives:   # long buff (160 s) assumed up before the fight
            d = 1e9
            self.buff("weapon_pct", self.v("BaseAttackDamagePercent") / 100, d)
            self.buff("max_health", self.v("BonusHealth"), d)
            f.hp += self.v("BonusHealth")


# ---------------------------------------------------------------------------------------------------
# Vitality items
# ---------------------------------------------------------------------------------------------------
@handler("upgrade_tech_purge")
class SpiritResilience(FX):
    def stat(self, f):
        return {"spirit_resist": self.item.p("TechResistBelowThreshold") / 100} if f.hp_frac < self.item.p("HealthThreshold", 50) / 100 else {}


@handler("upgrade_improved_bullet_armor")
class BulletResilience(FX):
    def stat(self, f):
        return {"bullet_resist": self.item.p("BulletResistBelowThreshold") / 100} if f.hp_frac < self.item.p("HealthThreshold", 50) / 100 else {}


@handler("upgrade_magic_shield")
class EnchantersEmblem(FX):
    def stat(self, f):
        if f.hp_frac > self.item.p("LifeThreshold", 65) / 100:
            return {"spirit_power": self.item.p("TechPower"), "cdr": self.item.p("CooldownReduction") / 100}
        return {}


class ShieldOnDamage(FX):
    kind = "spirit"

    def __init__(self, item, f):
        super().__init__(item, f)
        self.window = []

    def on_damage_taken(self, f, src, hit):
        if hit.kind != self.kind or not self.ready():
            return
        now = self.now
        self.window = [(x, a) for x, a in self.window if now - x <= self.item.p("DamageWindow", 3.5)] + [(now, hit.amount)]
        if sum(a for _, a in self.window) >= self.item.p("DamageThreshold"):
            self.use()
            self.window = []
            f.add_barrier(self.v("CombatBarrier"), self.dur("BarrierDuration", 8))


@handler("upgrade_spirit_bubble")
class SpiritShielding(ShieldOnDamage):
    kind = "spirit"


@handler("upgrade_weapon_shielding")
class WeaponShielding(ShieldOnDamage):
    kind = "bullet"


@handler("upgrade_spellbreaker")
class Spellbreaker(FX):
    def reduce_incoming(self, f, src, amt, kind, is_dot):
        if kind == "spirit" and amt >= self.item.p("DamageThreshold", 175) and self.ready():
            self.use()
            return amt * (1.0 - self.item.p("SpiritDamageReductionProc") / 100)
        return amt


@handler("upgrade_deflecting_armor")
class PlatedArmor(FX):
    def reduce_incoming(self, f, src, amt, kind, is_dot):
        if kind != "bullet" or is_dot:
            return amt
        n = src.counters.get("_last_hits", 1) or 1
        k = f.acc("plated").take(self.item.p("DeflectionPercent") / 100, n)
        return amt * (1.0 - k / n)


@handler("upgrade_cheat_death")
class CheatDeath(FX):
    def on_lethal(self, f, src):
        if not self.ready():
            return False
        self.use()
        f.hp = 1.0
        d = self.dur("DeathImmunityDuration", 4.5)
        f.mods.add("death_immune", 1, d, "cheatdeath")
        f.mods.add("outgoing_penalty", abs(self.item.p("DeathImmunityDamageReduction")) / 100, d, "cheatdeath")
        f.mods.add("heal_received", self.item.p("HealAmpReceivePenaltyPercent") / 100, d, "cheatdeath")
        return True


@handler("upgrade_juggernaut")
class Juggernaut(FX):
    def on_damage_taken(self, f, src, hit):
        if hit.kind == "bullet" and not hit.is_ability:
            self.debuff(src, "fire_rate_slow", self.item.p("FireRateSlow") / 100, self.dur("FireRateSlowDuration", 4))


@handler("upgrade_surging_power")
class VampiricBurst(FX):
    def try_active(self, f):
        if not self.ready() or f.hp_frac > 0.9 and f.e.t > 0.5:
            return False
        self.use()
        d = self.dur("AbilityDuration", 5)
        self.buff("bullet_lifesteal", self.item.p("ActiveBonusLifesteal") / 100, d)
        self.buff("fire_rate", self.item.p("ActiveBonusFireRate") / 100, d)
        f.bonus_ammo += int(f.st.clip * self.item.p("ActiveReloadPercent") / 100)
        return True


@handler("upgrade_infuser")
class Infuser(FX):
    def try_active(self, f):
        if not self.ready():
            return False
        self.use()
        d = self.dur("AbilityDuration", 7)
        self.buff("spirit_lifesteal", self.item.p("AbilityLifestealPercentHero") / 100, d)
        self.buff("spirit_power", self.item.p("BonusSpirit"), d)
        return True


@handler("upgrade_fury_trance")
class FuryTrance(FX):
    def try_active(self, f):
        # silences yourself, so only worth it once abilities are all on cooldown
        if not self.ready() or any(a.unlocked and a.charges > 0 and f.e.t >= a.ready_at for a in f.abilities if a.impl.kind != "passive"):
            return False
        self.use()
        d = self.dur("AbilityDuration", 6.5)
        self.buff("fire_rate", self.item.p("ActiveBonusFireRate") / 100, d)
        self.buff("spirit_resist", self.item.p("TechResist") / 100, d)
        f.mods.add("silence", 1, d, "furytrance")
        return True


@handler("upgrade_colossus")
class Colossus(FX):
    def try_active(self, f):
        if not self.ready() or f.hp_frac > 0.8:
            return False
        self.use()
        d = self.dur("AbilityDuration", 7)
        self.buff("bullet_resist", self.item.p("BuffBulletResist") / 100, d)
        self.buff("spirit_resist", self.item.p("BuffTechResist") / 100, d)
        return True


@handler("upgrade_metal_skin")
class MetalSkin(FX):
    def try_active(self, f):
        if not self.ready() or f.hp_frac > 0.5:
            return False
        self.use()
        self.buff("bullet_immune", 1, self.dur("AbilityDuration", 5))
        return True


@handler("upgrade_warp_stone")
class WarpStone(FX):
    def try_active(self, f):
        if not self.ready() or f.hp_frac > 0.6:
            return False
        self.use()
        self.buff("bullet_resist", self.item.p("BulletResist") / 100, self.dur("CasterBuffDuration", 6))
        return True


@handler("upgrade_self_bubble")
class EtherealShift(FX):
    def try_active(self, f):
        if not self.ready() or f.hp_frac > 0.35:
            return False
        self.use()
        d = self.dur("AbilityDuration", 4)
        self.buff("invulnerable", 1, d)
        f.mods.add("stun", 1, d, "ethereal")   # can't act while in the void
        b = self.dur("BuffDuration", 5)
        f.e.after(d, lambda: (f.mods.add("spirit_power", self.item.p("BonusSpirit"), b, "eth"),
                              f.mods.add("spirit_resist", self.item.p("TechResist") / 100, b, "eth")))
        return True


class BarrierActive(FX):
    prop = "CombatBarrier"
    dur = "BuffDuration"
    hp_below = 0.6

    def try_active(self, f):
        if not self.ready() or f.hp_frac > self.hp_below:
            return False
        self.use()
        f.add_barrier(self.v(self.prop), self.item.p(self.dur, 6))
        return True


@handler("upgrade_grit")
class Grit(BarrierActive):
    dur = "BarrierDuration"


@handler("upgrade_divine_barrier")
class DivineBarrier(BarrierActive):
    pass


@handler("upgrade_guardian_ward")
class GuardianWard(BarrierActive):
    prop = "GuardianWardCombatBarrier"


@handler("upgrade_rocket_booster")
class MajesticLeap(BarrierActive):
    dur = "BarrierDuration"
    hp_below = 0.4


@handler("upgrade_diviners_kevlar")
class DivinersKevlar(FX):
    def on_cast(self, f, ab):
        if ab.ab.ultimate and self.ready():
            self.use()
            d = self.dur("BuffDuration", 20)
            f.add_barrier(self.v("CombatBarrier"), d)
            self.buff("spirit_power", self.item.p("TechPower"), d)


@handler("upgrade_health_nova")
class HealingNova(FX):
    def try_active(self, f):
        if not self.ready() or f.hp_frac > 0.5:
            return False
        self.use()
        tot, d = self.v("TotalHealthRegen"), self.dur("RegenDuration", 2)
        for i in range(4):
            f.e.after(d / 4 * (i + 1), f.heal, tot / 4, self.name, "item")
        return True


@handler("upgrade_rescue_beam")
class RescueBeam(FX):
    def try_active(self, f):
        if not self.ready() or f.hp_frac > 0.5:
            return False
        self.use()
        d = self.item.p("AbilityChannelTime", 2.5)
        amt = f.max_hp * self.item.p("HealPercentAmount") / 100
        f.gun_locked_until = max(f.gun_locked_until, f.e.t + d)
        n = int(d / 0.25)
        for i in range(n):
            f.e.after(0.25 * (i + 1), f.heal, amt / n, self.name, "item")
        return True


@handler("upgrade_restorative_locket")
class RestorativeLocket(FX):
    def on_enemy_cast(self, f, ab):
        if f.acc("locket_reach").take(self.reach_p(self.item.p("Radius", 32)), 1):
            f.counters["locket"] = min(self.item.p("MaxStacks", 25), f.counters.get("locket", 0) + 1)

    def try_active(self, f):
        n = f.counters.get("locket", 0)
        if not self.ready() or f.hp_frac > 0.5 or n <= 0:
            return False
        self.use()
        f.counters["locket"] = 0
        f.heal(n * self.v("HealPerStack"), self.name, "item")
        return True


@handler("upgrade_return_fire")
class ReturnFire(FX):
    def try_active(self, f):
        if not self.ready():
            return False
        self.use()
        self.buff("return_fire", 1, self.dur("AbilityDuration", 6.5))
        return True

    def on_damage_taken(self, f, src, hit):
        if not f.mods.active("return_fire") or hit.source == self.name or hit.is_dot:
            return
        pct = self.item.p("BulletDamageReflectedPct") if hit.kind == "bullet" else self.item.p("SpiritDamageReflectedPct")
        if pct and hit.amount > 0:
            f.e.damage(f, src, hit.amount * pct / 100 * f.skill.accuracy, "bullet", self.name, procs=False, is_item=True)


@handler("upgrade_vex_barrier", "upgrade_auto_cleanse")
class ReactiveBarrier(FX):
    def on_cc(self, f, key):
        if not self.ready():
            return
        self.use()
        f.add_barrier(self.v("VexBarrierCombatBarrier"), self.dur("AbilityDuration", 10))
        if self.item.class_name == "upgrade_auto_cleanse":
            for k in CC_KEYS:
                f.mods.d.pop(k, None)
            for ab in f.abilities:
                ab.ready_at = f.e.t + (ab.ready_at - f.e.t) * (1 - self.item.p("CooldownReductionOnProc", 20) / 100)


@handler("upgrade_reduce_debuff_duration")
class DispelMagic(FX):
    """Active: purge enemy debuffs and DoTs and heal HealOnActivate. Used at once against an enemy silence or disarm.
    Against a DoT with >= 2 s left: only on Skill.dot_cleanse_share of DoT episodes (real players mostly let Decay
    run: on cooldown, saved for a stun, not noticed; accuracy.dot_cleanse_share), and then after
    Skill.dot_cleanse_delay seconds of it (reaction time), or with dot_cleanse_delay=None only once below
    DOT_PANIC_HP of max health. An episode is a stretch with some enemy DoT running, drawn once when it starts while
    Dispel is ready (overlapping DoTs share the draw; the cooldown is simulated too, and the fit uses this same
    code). The draw is an engine.Accum: random when the engine has an rng (fit_dispel.py), else deterministic,
    started at Skill.fight_phase, so over the overall score's spread phases the first DoT is cleansed in exactly
    that share of fights. Without a phase (single duels, the duel-score search) it starts at a hash of both
    fighters' items, so across an opponent pool the first DoT is still cleansed in about that share of fights. The
    +2 m/s move speed does nothing at fixed distance. Assumption: BuffDuration (3 s) is the move-speed buff, not
    debuff immunity."""
    DOT_PANIC_HP = 0.5
    DOT_MIN_LEFT = 2.0   # s: a DoT about to run out is not worth the cooldown

    def __init__(self, item, f):
        super().__init__(item, f)
        self.dot_seen = None
        self.dot_go = False
        self.dot_pick = {}
        self.dot_buildup_drawn = False

    def _draw(self, f, kind):
        """Spend Dispel on this DoT episode? kind "buildup": Skill.dot_cleanse_share_buildup, else dot_cleanse_share
        (None = always). One Accum per kind, both started at the same phase."""
        sk = f.skill
        share = sk.dot_cleanse_share_buildup if kind == "buildup" else sk.dot_cleanse_share
        if share is None:
            return True
        pick = self.dot_pick.get(kind)
        if pick is None:
            from .engine import Accum
            phase = sk.fight_phase
            pick = self.dot_pick[kind] = Accum(f.e.rng, self.loadout_phase(f) if phase is None else phase)
        return pick.take(share) > 0

    @staticmethod
    def loadout_phase(f):
        """Stable 0-1 phase from both fighters' item ids and max health (stat-only items have no handler but change
        health), integers only, so it is the same in every process."""
        x = 0
        for g in (f, f.enemy):
            if g is None:
                continue
            for i in sorted(fx.item.id for fx in g.items_fx if getattr(fx, "item", None) is not None) + [
                    int(round(g.max_hp_base * 10))]:
                x = (x * 1000003 + i) % (1 << 61)
        return (((x * 11400714819323198485) % (1 << 64)) >> 11) / (1 << 53)   # Fibonacci hash, high bits

    def try_active(self, f):
        if not self.ready() or not f.skill.use_actives:
            return False
        cc = f.afflicted(min_left=1e9, keys=("silence", "disarm"))
        dot = f.afflicted(min_left=self.DOT_MIN_LEFT, keys=())
        if not dot:
            self.dot_seen = None
        else:
            buildup = f.buildup_dot(self.DOT_MIN_LEFT)
            if self.dot_seen is None:
                self.dot_seen = self.now
                self.dot_go = self._draw(f, "buildup" if buildup else "other")
                self.dot_buildup_drawn = buildup
            elif buildup and not self.dot_go and not self.dot_buildup_drawn:
                # a build-up DoT (Afterburn, Toxic Bullets) joined a running episode: its own draw
                self.dot_buildup_drawn = True
                self.dot_go = self._draw(f, "buildup")
        delay = f.skill.dot_cleanse_delay
        if not self.dot_go:
            use_on_dot = False
        elif delay is None:
            use_on_dot = dot and f.hp_frac < self.DOT_PANIC_HP
        else:
            use_on_dot = dot and self.now - self.dot_seen >= delay
        if not cc and not use_on_dot:
            return False
        self.use()
        self.dot_seen = None
        f.dispel()
        f.heal(self.v("HealOnActivate"), self.name, "heal")
        return True


@handler("upgrade_healbuff")
class HealingTempo(FX):
    pass


# ---------------------------------------------------------------------------------------------------
# Spirit items
# ---------------------------------------------------------------------------------------------------
@handler("upgrade_magic_burst", "upgrade_magic_shock")
class MysticBurst(FX):
    """Charges up over AbilityChargeUpTime and each qualifying ability hit releases what has charged, not a full proc
    on a cooldown: in replays (70 Phantom+ matches, hero victims) a release's damage grows linearly with the time
    since the last one, up to the full amount at 14 s (Mystic Burst median 2 after <1 s, 20 after 7 s, 39 after 14+;
    Tankbuster 7 / 75 / 188), and releases on the same victim come 0.2-2 s apart, so ReProcLockoutTime is not a
    lockout between releases. Full charge at the fight's start. Hits in the same tick share one charge (the first
    takes it); the total released doesn't depend on their order, except Tankbuster's current-health term."""

    def __init__(self, item, f):
        super().__init__(item, f)
        self.charged_at = -1e9

    def on_start(self, f):
        self.charged_at = -1e9

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "spirit" or not hit.is_ability or hit.is_dot:
            return
        if hit.amount / max(1e-6, hit.landing) < self.item.p("MinimumDamage", 80):
            return
        charge = min(1.0, (self.now - self.charged_at) / max(1e-6, self.cd("AbilityChargeUpTime")))
        self.charged_at = self.now
        if charge <= 0:
            return
        dmg = self.v("Damage")
        if self.item.class_name == "upgrade_magic_shock":   # Tankbuster: + % current health, ignores resist
            dmg += t.hp * self.item.p("CurrentHealthDamage") / 100
            f.e.damage(f, t, dmg * charge, "spirit", self.name, ignore_resist=True, is_item=True, procs=False)
        else:
            f.e.damage(f, t, dmg * charge, "spirit", self.name, is_item=True, procs=False)


@handler("upgrade_magic_vulnerability")
class MysticVulnerability(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "spirit":
            self.debuff(t, "spirit_shred", abs(self.item.p("TechArmorDamageReduction")) / 100, self.dur("AbilityDuration", 7))


@handler("upgrade_escalating_exposure")
class EscalatingExposure(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "spirit" or not self.ready():
            return
        self.ready_at = self.now + self.item.p("ProcCooldown", 0.7)
        n = int(self.item.p("MaxStacks", 12))
        k = min(n, f.counters.get("expo", 0) + 1)
        f.counters["expo"] = k
        d = self.dur("AbilityDuration", 12)
        # all stacks refresh together
        t.mods.add("spirit_amp_taken", k * self.item.p("MagicIncreasePerStack") / 100, d, ("expo", f.name))

    def on_start(self, f):
        f.counters["expo"] = 0


@handler("upgrade_spirit_burn")
class SpiritBurn(FX):
    def __init__(self, item, f):
        super().__init__(item, f)
        self.window = []

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "spirit" or not self.ready() or hit.source == self.name:
            return
        now = self.now
        self.window = [(x, a) for x, a in self.window if now - x <= self.dur("DamageThresholdDuration", 5)] + [(now, hit.amount)]
        if sum(a for _, a in self.window) >= self.item.p("DamageThreshold", 500):
            self.ready_at = now + self.dur("ImmunityDuration", 20)
            self.window = []
            self.spirit(t, self.v("ExplosionDamage"), procs=False)
            d = self.dur("DebuffDuration", 8)
            f.e.dot(f, t, self.v("DPS"), d, self.name, tick=self.item.p("TickRate", 0.5), is_item=True, procs=False)
            self.debuff(t, "heal_received", self.item.p("HealAmpReceivePenaltyPercent") / 100, d)


class ImbueCharge(FX):
    """Quicksilver Reload / Mercurial Magnum: imbued ability cast while charged -> bonus damage, fire rate, reload.
    Mercurial's per-bullet bonus lasts BuffDuration (12 s) with the fire rate."""

    def on_start(self, f):
        self.ready_at = 0.0
        self.pending = None

    def imbued(self, ab):
        return self.item in ab.imbues

    def on_cast(self, f, ab):
        if not self.imbued(ab) or not self.ready():
            return
        self.use("AbilityChargeUpTime")
        self.pending = ab
        d = self.dur("BuffDuration", 12)
        self.buff("fire_rate", self.item.p("BonusFireRate") / 100, d)
        f.clip = f.st.clip
        if self.item.class_name == "upgrade_ethereal_bullets":
            # the bullet bonus lasts the buff, not one clip: in Phantom+ replays 82% of a Vyper holder's gun hits after
            # the first proc carry it (Wraith 79%, Warden 93%) while his clip lasts 1.7 s
            self.buff("mercurial", 1, d)

    def on_damage_dealt(self, f, t, hit):
        if self.pending is not None and hit.ability is self.pending and hit.kind == "spirit":
            self.pending = None
            self.spirit(t, self.v("Damage"), procs=False)
        if hit.kind == "bullet" and hit.hits and not hit.is_ability and f.mods.active("mercurial"):
            # "+X% Base Bullet Damage" per bullet (X = 20 + 0.38 x Spirit Power), not flat damage: in replays each
            # proc is ~0.4-0.55 x the hero's base bullet damage (Wraith median 4, Warden 11, Holliday 31).
            pct = self.v("BulletsBonusMagicDamage") / 100
            self.spirit(t, f.st.bullet_damage * pct * hit.hits, procs=False)



HANDLERS["upgrade_quick_silver"] = ImbueCharge
HANDLERS["upgrade_ethereal_bullets"] = ImbueCharge


@handler("upgrade_magic_storm")
class SurgeOfPower(FX):
    def on_cast(self, f, ab):
        if self.item in ab.imbues and self.ready():
            self.use()
            self.buff("fire_rate", self.item.p("FireRateBonus") / 100, self.dur("MovementSpeedBonusDuration", 8))


@handler("upgrade_mystic_reverb")
class MysticReverb(FX):
    """Imbued ability damage builds up while the item is ready; once it reaches MinimumDamage the item goes on cooldown
    and DelayDuration later the echo deals TechDamagePercent% of that damage plus MaxHealthDamage% of the target's
    current health (the tooltip's "Current Health Bonus Damage", not a cap). Build-up is per target and lasts
    DelayDuration; DoT ticks of the imbued ability count, so a damage-over-time imbue (Flame Dash) triggers it too."""

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "spirit" or hit.ability is None or self.item not in hit.ability.imbues:
            return
        # imbued lifesteal on this hit (engine.damage applies lifesteal before these hooks, so a short spirit_lifesteal
        # mod here would only reach the next hit)
        if not hit.is_dot:   # DoT ticks build up the echo (below) but keep the old no-lifesteal rule
            f.heal(hit.amount * self.item.p("ImbueAbilityLifesteal") / 100, "spirit_lifesteal", "lifesteal")
        if not self.ready():
            return
        # the threshold counts damage dealt (after resist) on this target within DelayDuration; the echo repeats the raw
        # damage (it is mitigated again)
        builds = f.counters.setdefault("reverb_build", {})
        t0, dealt, acc = builds.get(id(t), (f.e.t, 0.0, 0.0))
        if f.e.t - t0 > self.dur("DelayDuration", 3):
            t0, dealt, acc = f.e.t, 0.0, 0.0
        dealt, acc = dealt + hit.amount, acc + hit.raw
        if dealt < self.item.p("MinimumDamage", 0):
            builds[id(t)] = (t0, dealt, acc)
            return
        builds.clear()
        self.use()
        base = acc * self.item.p("TechDamagePercent") / 100
        pct = self.item.p("MaxHealthDamage", 0) / 100

        def echo():
            if t.alive:
                self.spirit(t, base + pct * max(0.0, t.hp), procs=False)
        f.e.after(self.dur("DelayDuration", 3), echo)


@handler("upgrade_bulletshredimbue")
class BallisticEnchantment(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.ability is not None and self.item in hit.ability.imbues:
            self.buff("weapon_pct", self.item.p("WeaponPowerPerStack") / 100, self.dur("AbilityDuration", 20))


@handler("upgrade_ability_power_shard")
class EchoShard(FX):
    def on_cast(self, f, ab):
        if self.item in ab.imbues:
            f.counters["echo_target"] = ab

    def try_active(self, f):
        ab = f.counters.get("echo_target")
        if not self.ready() or ab is None or f.e.t >= ab.ready_at:
            return False
        self.ready_at = self.now + (self.item.p("AbilityCooldown", 30) + ab.cooldown()) * (1 - f.st.item_cdr)
        ab.reset_cooldown()
        f.counters["echo_target"] = None
        return True


@handler("upgrade_ability_refresher")
class Refresher(FX):
    def try_active(self, f):
        if not self.ready():
            return False
        on_cd = [a for a in f.abilities if a.unlocked and a.impl.kind != "passive" and f.e.t < a.ready_at]
        ult_used = any(a.ab.ultimate and a.casts for a in f.abilities)
        if len(on_cd) < 3 or not ult_used:
            return False
        self.use()
        for a in f.abilities:
            a.reset_cooldown()
        return True


@handler("upgrade_suppressor")
class Suppressor(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "spirit":
            self.debuff(t, "fire_rate_slow", self.item.p("FireRateSlow") / 100, self.dur("AbilityDuration", 4.5))


@handler("upgrade_healbane")
class Healbane(FX):
    """Spirit damage cuts the target's healing; a target that dies under it heals the holder HealOnKill. In
    realistic mode the cut is scaled by Skill.item_landing["Healbane"] (real heal prevented per fight second / the
    sim's, sim/scripts/sustain/fit_healbane.py)."""

    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "spirit":
            k = f.skill.item_landing.get(self.name, 1.0) if f.skill.item_landing else 1.0
            self.debuff(t, "heal_received", k * self.item.p("HealAmpReceivePenaltyPercent") / 100,
                        self.dur("AbilityDuration", 8))

    def on_kill(self, f, t):
        if t.mods.get("heal_received", (self.item.class_name, "heal_received")) is not None:
            f.heal(self.item.p("HealOnKill"), self.name, "item")


@handler("upgrade_bullet_resist_shredder")
class BulletResistShredder(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "spirit":
            self.debuff(t, "bullet_shred", abs(self.item.p("BulletArmorReduction")) / 100, self.dur("AbilityDuration", 8))


@handler("upgrade_mystic_regeneration", "upgrade_resonant_healing")
class MysticRegeneration(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.kind == "spirit":
            self.buff("regen", self.v("Regeneration"), self.dur("RegenerationDuration", 7))

    def on_cast(self, f, ab):
        if self.item.class_name == "upgrade_resonant_healing" and self.ready():
            self.use()
            f.heal(self.v("HealingPerCast"), self.name, "item")


@handler("upgrade_tech_damage_pulse")
class TormentPulse(FX):
    def on_start(self, f):
        f.e.after(self.item.p("AbilityCooldown", 1.4), self.pulse)

    def pulse(self):
        f = self.f
        if not f.alive or f.e.over:
            return
        p = self.reach_p(self.item.p("DamagePulseRadius", 9))
        if p > 0:
            self.spirit(f.enemy, self.v("DamagePulseAmount") * p)
        f.e.after(self.item.p("AbilityCooldown", 1.4), self.pulse)


class DamageActive(FX):
    radius_prop = "EndRadius"
    dmg_prop = "Damage"

    def extra(self, f, t):
        pass

    def cc(self, d):
        """CC duration d x the item's real-data factor in realistic mode (accuracy.item_landing, the fitted factor
        without the fight-length correction): the factor stands for casts that miss or come late, and a miss
        misses its stun / silence / disarm too."""
        if not self.f.skill.item_landing:
            return d
        from .accuracy import item_landing
        global _CC_LANDING
        if _CC_LANDING is None:
            _CC_LANDING = item_landing()
        return d * _CC_LANDING.get(self.name, 1.0)

    def try_active(self, f):
        r = self.item.p(self.radius_prop) or self.item.p("AbilityCastRange") or 15
        if not self.ready() or not self.ready_in(r):
            return False
        self.use()
        dmg = self.v(self.dmg_prop) if self.dmg_prop else 0
        if dmg:
            self.spirit(f.enemy, dmg * f.skill.spirit_accuracy)
        self.extra(f, f.enemy)
        return True


_CC_LANDING = None


@handler("upgrade_cold_front")
class ColdFront(DamageActive):
    pass


@handler("upgrade_arctic_blast")
class ArcticBlast(DamageActive):
    def extra(self, f, t):
        self.debuff(t, "stun", 1, self.cc(self.dur("FreezeDuration", 1)))


@handler("upgrade_targeted_silence")
class SilenceWave(DamageActive):
    radius_prop = "AbilityCastRange"

    def extra(self, f, t):
        self.debuff(t, "silence", 1, self.cc(self.dur("AbilityDuration", 3)))


@handler("upgrade_phantom_strike")
class PhantomStrike(DamageActive):
    radius_prop = "AbilityCastRange"
    dmg_prop = "ImpactDamage"

    def extra(self, f, t):
        self.debuff(t, "disarm", 1, self.cc(self.dur("SlowDuration", 3)))


@handler("upgrade_target_stun")
class Knockdown(DamageActive):
    radius_prop = "AbilityCastRange"
    dmg_prop = None

    def extra(self, f, t):
        f.e.after(self.item.p("StunDelay", 2), lambda: self.debuff(t, "stun", 1, self.dur("StunDuration", 0.5)))


@handler("upgrade_spirit_sap")
class SpiritSap(DamageActive):
    radius_prop = "AbilityCastRange"
    dmg_prop = None

    def extra(self, f, t):
        d = self.dur("AbilityDuration", 12)
        self.debuff(t, "spirit_shred", abs(self.item.p("MagicResistReduction")) / 100, d)
        self.debuff(t, "spirit_power", self.item.p("TechPowerReduction"), d)


@handler("upgrade_withering_whip")
class RustedBarrel(DamageActive):
    radius_prop = "AbilityCastRange"
    dmg_prop = None

    def extra(self, f, t):
        d = self.dur("AbilityDuration", 5)
        self.debuff(t, "fire_rate_slow", self.item.p("FireRateSlow") / 100, d)
        self.debuff(t, "bullet_shred", abs(self.item.p("BulletArmorReduction")) / 100, d)


@handler("upgrade_greater_withering_whip")
class DisarmingHex(DamageActive):
    radius_prop = "AbilityCastRange"
    dmg_prop = None

    def extra(self, f, t):
        d = self.dur("AbilityDuration", 4.25)
        self.debuff(t, "disarm", 1, d)
        self.debuff(t, "bullet_shred", abs(self.item.p("BulletArmorReduction")) / 100, d)


@handler("upgrade_glitch")
class CursedRelic(DamageActive):
    radius_prop = "AbilityCastRange"
    dmg_prop = None

    def extra(self, f, t):
        d = self.dur("AbilityDuration", 3.25)
        for k in ("silence", "disarm", "item_silence"):
            self.debuff(t, k, 1, d)
        f.mods.add("outgoing_penalty", abs(self.item.p("OutgoingDamagePenaltyPercent")) / 100, d, "cursed")


@handler("upgrade_focus_lens")
class FocusLens(DamageActive):
    radius_prop = "AbilityCastRange"
    dmg_prop = None

    def extra(self, f, t):
        d = self.dur("AbilityDuration", 4.5)
        self.debuff(t, "silence", 1, d)
        rd = self.dur("ResistReductionDuration", 12)
        self.debuff(t, "spirit_shred", abs(self.item.p("MagicResistReduction")) / 100, rd)
        self.debuff(t, "spirit_power", self.item.p("TechPowerReduction"), rd)
        start = sum(t.dmg_in.values())
        pct = self.item.p("PercentDamage") / 100
        # the stored damage already had amps (Escalating Exposure etc.) and resists applied, so it lands as is
        f.e.after(d, lambda: self.spirit(t, (sum(t.dmg_in.values()) - start) * pct, procs=False, pure=True))


@handler("upgrade_rupture")
class Decay(DamageActive):
    radius_prop = "AbilityCastRange"
    dmg_prop = None

    def extra(self, f, t):
        d = self.dur("AbilityDuration", 12)
        pct = self.v("DotHealthPercent") / 100
        self.debuff(t, "heal_received", self.item.p("HealAmpReceivePenaltyPercent") / 100, d)
        tick = self.item.p("TickRate", 1.0)
        epoch = t.counters.get("dispel_epoch", 0)
        t.counters.setdefault("dot_until", {})[self.item.class_name] = f.e.t + d
        for i in range(int(d / tick)):
            f.e.after(tick * (i + 1), lambda: self.spirit(t, t.hp * pct * tick, procs=False, nonlethal=True, is_dot=True)
                      if t.counters.get("dispel_epoch", 0) == epoch else None)


@handler("upgrade_discord")
class Scourge(DamageActive):
    radius_prop = "AuraRadius"
    dmg_prop = None

    def extra(self, f, t):
        d = self.dur("AbilityDuration", 10)
        self.buff("spirit_resist", self.item.p("TechResist") / 100, d)
        self.buff("status_resist", self.item.p("StatusResistancePercent") / 100, d)
        pct = self.v("MaxHealthPercentAsDPS") / 100
        tick = self.item.p("TickRate", 0.25)
        for i in range(int(d / tick)):
            p = self.reach_p(self.item.p("AuraRadius", 10))
            f.e.after(tick * (i + 1), lambda p=p: self.spirit(t, t.max_hp * pct * tick * p, procs=False, is_dot=True)
                      if p > 0 else None)


@handler("upgrade_ultimate_burst")
class LightningScroll(FX):
    def on_damage_dealt(self, f, t, hit):
        if hit.is_ult and hit.ability is not None and not hit.ability.scratch.get("_scroll"):
            hit.ability.scratch["_scroll"] = True
            f.e.after(self.item.p("DelayBeforeStun", 3), lambda: (self.spirit(t, self.v("Damage"), procs=False),
                                                                  self.debuff(t, "stun", 1, self.dur("StunDuration", 0.75))))

    def on_cast(self, f, ab):
        if ab.ab.ultimate:
            ab.scratch["_scroll"] = False


@handler("upgrade_arcane_surge")
class ArcaneSurge(FX):
    def on_cast(self, f, ab):
        if f.counters.get("arcane_used"):
            return
        f.counters["arcane_used"] = True   # one dash-jump empowered cast per fight
        ab.scratch["_bonus_spirit"] = self.item.p("SpiritPower")
        ab.scratch["_bonus_duration"] = self.item.p("BonusAbilityDurationPercent") / 100


# ---------------------------------------------------------------------------------------------------
# Melee items. They react to the engine's melee rotation (source "melee", Skill.melee_rate); the flag
# f.counters["melee_heavy"] says whether the hit was a heavy melee. Movement parts (charge distance, slows) skipped.
# ---------------------------------------------------------------------------------------------------
def _basic_melee(hit):
    return hit.kind == "melee" and hit.source == "melee"


def _melee_proc(fx, f):
    """Whether a (possibly fractional-weight) melee event triggers this item's on-melee effect."""
    return fx.ready() and f.acc(fx.item.class_name + ":melee").take(f.counters.get("melee_weight", 1.0), 1) > 0


@handler("upgrade_melee_charge", "upgrade_crushing_fists")
class MeleeCharge(FX):
    """Heavy melee off cooldown deals +BonusHeavyMeleeDamage%. Crushing Fists also stuns on it and each light
    melee adds a bullet-resist-reduction stack (MaxStacks, DebuffDuration; a heavy adds HeavyMeleeMultiplier)."""

    def on_damage_dealt(self, f, t, hit):
        if not _basic_melee(hit):
            return
        heavy = f.counters.get("melee_heavy")
        if heavy and _melee_proc(self, f):
            self.use()
            f.e.damage(f, t, hit.raw * self.item.p("BonusHeavyMeleeDamage") / 100, "melee", self.name,
                       is_item=True, procs=False)
            if self.dur("StunDuration"):
                self.debuff(t, "stun", 1, self.dur("StunDuration"))
        red = abs(self.item.p("BulletResistReduction"))
        if red:
            n = int(self.item.p("HeavyMeleeMultiplier", 2) if heavy else self.item.p("LightMeleeStacks", 1))
            for _ in range(n):
                k = f.counters.get("fists", 0)
                f.counters["fists"] = k + 1
                self.debuff(t, "bullet_shred", red / 100, self.dur("DebuffDuration", 8),
                            tag=("fists", k % int(self.item.p("MaxStacks", 6))))


@handler("upgrade_spirit_snatch")
class SpiritSnatch(FX):
    """Melee hit off cooldown: SpiritDamage, and steals spirit power and spirit resist for AbilityDuration."""

    def on_damage_dealt(self, f, t, hit):
        if not _basic_melee(hit) or not _melee_proc(self, f):
            return
        self.use()
        d = self.dur("AbilityDuration", 10)
        self.spirit(t, self.v("SpiritDamage"), procs=False)
        self.debuff(t, "spirit_power", -abs(self.item.p("TechPowerReduction")), d)
        self.debuff(t, "spirit_resist", -abs(self.item.p("TechArmorDamageReduction")) / 100, d)
        self.buff("spirit_power", self.item.p("TechPowerGain"), d)
        self.buff("spirit_resist", self.item.p("TechArmorGain") / 100, d)


@handler("upgrade_acolytes_glove")
class SpiritStrike(FX):
    """Melee hit off cooldown: SpiritDamage and a spirit resist reduction for AbilityDuration."""

    def on_damage_dealt(self, f, t, hit):
        if not _basic_melee(hit) or not _melee_proc(self, f):
            return
        self.use()
        self.spirit(t, self.v("SpiritDamage"), procs=False)
        self.debuff(t, "spirit_shred", abs(self.item.p("TechArmorDamageReduction")) / 100, self.dur("AbilityDuration", 6))


@handler("upgrade_lifestrike_gauntlets", "upgrade_boxing_glove")
class Lifestrike(FX):
    """Melee hit off cooldown heals LifestrikeHeal (Melee Lifesteal) or LifestealHeal + % of the hit (Lifestrike)."""

    def on_damage_dealt(self, f, t, hit):
        if not _basic_melee(hit) or not _melee_proc(self, f):
            return
        self.use()
        amt = self.v("LifestrikeHeal") + self.v("LifestealHeal") + hit.amount * self.item.p("LifestealHealPercent") / 100
        f.heal(amt, self.name, "item")


from . import items_fx_extra  # noqa: E402,F401  (registers more handlers)

MODELED = set(HANDLERS)


def attach(f, items):
    for it in items:
        cls = HANDLERS.get(it.class_name)
        if cls is None:
            continue
        fx = cls(it, f)
        f.items_fx.append(fx)
        if hasattr(fx, "stat"):
            f.stat_hooks.append(fx.stat)
