"""Billy (hero_punkgoat).

Assumptions:
- Melee damage = hero light (heavy) melee base + per-boon growth, x melee % items. Bashdown's slam lands
  PlaceDistanceInFrontOfCaster ahead with a shockwave of WaveEndRadius: the spirit wave reaches that far; the
  melee pull-down only lands within AbilityCastRange + PullDownRange (+ engage margin). T3 swaps light melee for
  the HeavyMeleeDamage scale (50%) of heavy melee (heavy grows with boons in proportion to light). Knockup / pull are skipped.
- Rising Ram: reach = ChargeSpeed x AbilityDuration (units -> m). Lands at spirit accuracy; on impact the
  cooldown is halved. T1 weapon burst, T3 max-health buff (health gained too).
- Blasted (passive): light melee hits restore BulletsReloadedPerLightMeleePct of the clip and wreck the
  target. Active: for AbilityDuration bullets inflict wrecked too (BlastedRateOnBulletPct), so the target takes
  BulletDamageAmp % more bullet damage for the whole window (the extra is booked as its own unresisted "Blasted"
  hit after each bullet hit, as the game's damage report does); melee hits during it add MaxHealthMelee (x
  LightMeleeScalePct for light melee) max health for HealthBoostDuration and extend the window. T2 gives
  Bashdown a charge on use. No melee is woven between abilities
  (the engine has no melee rotation), so only Bashdown's melee counts.
- Chain Gang: target chained for AbilityDuration taking DPS, then yanked for Damage. T1 resists last for the
  chain duration (assumed).
"""
from deadsim.abilities import AbilityImpl, register

UNITS_PER_METER = 39.37


def find(c, class_name):
    for ab in c.me.abilities:
        if ab.ab.class_name == class_name:
            return ab
    return None


def melee_base(c, heavy=False):
    """Light melee (base + boon growth); heavy melee grows with boons in proportion to light."""
    light = c.light_melee()
    if not heavy:
        return light
    base = c.me.st.hero.base
    return base.get("heavy_melee_damage", 0.0) * light / max(1.0, base.get("light_melee_damage", 1.0))


def on_melee(c, heavy=False):
    """Blasted's melee effects, called by Billy's ability melee hits."""
    bl = find(c, "ability_punkgoat_blasted")
    if bl is not None and bl.unlocked:
        bl.impl.melee(bl.ctx, heavy)


@register("ability_punkgoat_ult")
class Bashdown(AbilityImpl):
    kind = "aoe"

    def in_range(self, c):
        return c.reach(c.raw("PlaceDistanceInFrontOfCaster") + c.val("WaveEndRadius") + 0.5)

    def cast(self, c):
        ch = c.raw("AbilityChannelTime", 0.3)
        c.lock_gun(ch + c.raw("AbilityPostCastDuration"))
        reach = c.rng("AbilityCastRange") + c.raw("PullDownRange") + c.me.skill.engage_margin
        if c.dist <= reach:
            heavy = c.tier >= 3
            dmg = melee_base(c, heavy) * (c.scale("HeavyMeleeDamage") if heavy else 1.0)
            c.melee_hit(dmg, delay=ch)
            c.after(ch, on_melee, c, heavy)
        c.spirit_hit(c.val("Damage"), delay=ch + c.raw("ExplodeDelay", 0.5), hit_chance=1.0)


@register("ability_punkgoat_goatflip")
class RisingRam(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        reach = c.raw("ChargeSpeed") * c.dur("AbilityDuration") / UNITS_PER_METER
        return c.reach(reach + c.me.skill.engage_margin)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay + c.dur("AbilityDuration"))
        if not c.me.acc("ram_hit").take(c.me.skill.spirit_accuracy):
            return
        c.spirit_hit(c.val("Damage"), delay=delay + 0.2, hit_chance=1.0)
        s = self.s
        s.ready_at = c.now + s.cooldown() * (1 - c.raw("ReduceCooldownOnHitPct") / 100)
        s.next_charge = s.ready_at
        if c.tier >= 1:
            c.buff("weapon_pct", c.raw("WeaponDamageBurst") / 100, c.raw("WeaponDamageBurstDuration"))
        if c.tier >= 3:
            hp = c.me.max_hp_base * c.raw("MaxHealthBuffPct") / 100
            c.buff("max_health", hp, c.raw("MaxHealthBuffDuration"))
            c.me.hp += hp


@register("ability_punkgoat_blasted")
class Blasted(AbilityImpl):
    kind = "self"

    def start(self, c):
        c.state["active_until"] = -1.0

    def should_cast(self, c):
        return c.reach(30)

    def cast(self, c):
        d = c.dur("AbilityDuration")
        c.state["active_until"] = c.now + d
        self.amp(c)
        if c.tier >= 2:
            bd = find(c, "ability_punkgoat_ult")
            if bd is not None and bd.unlocked:
                bd.charges = min(bd.max_charges(), bd.charges + 1)
                bd.ready_at = min(bd.ready_at, c.now)

    def amp(self, c):
        pass   # the window is c.state["active_until"]; the amp itself is booked in on_damage_dealt

    def on_damage_dealt(self, c, target, hit):
        """Wrecked: bullets deal BulletDamageAmp % more, booked under Blasted as the game reports it."""
        if hit.kind != "bullet" or hit.amount <= 0 or c.now >= c.state["active_until"] or not target.alive:
            return
        f = c.me
        mult = (f.st.outgoing_mult * (1.0 - f.stat("outgoing_penalty")) * (1.0 + f.stat("damage_amp"))
                * (1.0 + target.stat("damage_taken_amp")))
        extra = hit.amount * c.raw("BulletDamageAmp") / 100 / max(1e-6, mult)
        c.engine.damage(f, target, extra, "pure", self.s.ab.name, is_ability=True, ability=self.s, procs=False)

    def melee(self, c, heavy):
        f = c.me
        pct = c.raw("BulletsReloadedPerHeavyMeleePct" if heavy else "BulletsReloadedPerLightMeleePct") / 100
        f.clip = min(f.st.clip, f.clip + int(round(f.st.clip * pct)))
        if c.now < c.state["active_until"]:
            scale = 1.0 if heavy else c.raw("LightMeleeScalePct", 40) / 100
            ext = c.val("DurationPerHeavyMelee" if heavy else "DurationPerLightMelee") * scale
            c.state["active_until"] = min(c.state["active_until"] + ext, c.now + c.raw("MaxDuration", 35))
            hp = c.val("MaxHealthMelee") * scale
            f.mods.add("max_health", hp, c.dur("HealthBoostDuration"))
            f.hp += hp
            self.amp(c)


@register("ability_punkgoat_tether")
class ChainGang(AbilityImpl):
    kind = "target"

    def cast(self, c):
        d = c.dur("AbilityDuration")
        c.lock_gun(c.raw("AbilityPostCastDuration"))
        c.dot(c.val("DPS"), d, tick=c.raw("TickRate", 0.25))
        c.spirit_hit(c.val("Damage"), delay=d)
        if c.tier >= 1:
            c.buff("bullet_resist", c.raw("BulletResist") / 100, d)
            c.buff("spirit_resist", c.raw("TechResist") / 100, d)
