"""Mina (hero_vampirebat).

Assumptions:
- Rake: one cone hit (range AbilityCastRange) for Damage + MissingHealthDamagePercentage of the target's missing
  health, spirit damage. Damage's EStatsCount scaling is not modeled (unknown stat). Heal-per-kill and trooper
  execute don't apply in a 1v1. Mina can't shoot during cast + post-cast.
- Sanguine Retreat: Mina is untargetable (invulnerable) and can't shoot for AbilityDuration. Without T1 it is an
  escape, cast when below RETREAT_HP; with T1 it is cast on cooldown for +BonusFireRate (BuffDuration) and
  BonusBullets. Recasts (MaxRecasts) are only used when below RECAST_HP.
- Love Bites: every gun hit deals MagicDamagePerBullet spirit damage. Build-up toward the bite: BuildUpPerShot per
  gun hit (x BuildUpHeadshotBonus on headshots), BuildUpPerDagger per Rake hit, BuildUpPerBat per bat hit,
  BuildUpPerShot for other ability damage; resets after BuildUpDuration without build-up. At 100 the bite deals
  BonusDamage, then a PerTargetCooldown starts (cooldown reduction applies). T3: +BonusFireRate for BuffDuration.
  Bullets building up is an assumption (the description only names abilities, but without it the bite almost
  never procs). Each bite adds BonusBatsPerProc bats to Nox Nostra (up to BonusBatsMax).
- Nox Nostra: BatCount (+ bonus bats) bats released at BatPerSecond after the cast delay; all seek the single
  target and hit for Damage, refreshing a DebuffDuration silence. T3 adds CurrentHealthPercent of current health
  per hit. BatEffectiveness / MaxBatTargets are ignored (single target).
"""
from deadsim.abilities import AbilityImpl, register

RETREAT_HP = 0.4     # escape threshold without T1
RECAST_HP = 0.3      # use the recasts only when this low
BATS_KEY = "mina_bonus_bats"


@register("ability_vampirebat_steallife")
class Rake(AbilityImpl):
    kind = "aoe"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay + c.raw("AbilityPostCastDuration"))
        e = c.foe

        def go():
            if c.me.alive and e.alive:
                miss = (e.max_hp - e.hp) * c.raw("MissingHealthDamagePercentage") / 100
                c.spirit_hit(c.raw("Damage") + miss)
        c.after(delay, go)


@register("ability_vampirebat_batblink")
class SanguineRetreat(AbilityImpl):
    kind = "self"

    def should_cast(self, c):
        return c.raw("BonusFireRate") > 0 or c.me.hp_frac < RETREAT_HP

    def cast(self, c):
        d = c.dur("AbilityDuration", 0.65)
        n = 1 + (int(c.raw("MaxRecasts")) if c.me.hp_frac < RECAST_HP else 0)
        c.buff("invulnerable", 1, d * n, tag="bat_blink")
        c.lock_gun(d * n)
        if c.raw("BonusFireRate"):
            c.buff("fire_rate", c.raw("BonusFireRate") / 100, c.dur("BuffDuration"), tag="bat_blink_fr")
            c.me.bonus_ammo += int(c.raw("BonusBullets"))


@register("ability_vampirebat_lovebites")
class LoveBites(AbilityImpl):
    kind = "passive"

    def start(self, c):
        c.state.update(meter=0.0, last=-99.0, ready=0.0)
        c.me.counters[BATS_KEY] = 0

    def on_damage_dealt(self, c, target, hit):
        if hit.source == self.s.ab.name or hit.is_item:
            return
        if hit.kind == "bullet" and hit.source == "gun" and hit.hits:
            c.engine.damage(c.me, target, c.val("MagicDamagePerBullet") * hit.hits, "spirit", self.s.ab.name,
                            is_ability=True, ability=self.s, procs=False)
            hs = hit.headshots * (c.raw("BuildUpHeadshotBonus", 1.5) - 1.0)
            self.build(c, target, c.raw("BuildUpPerShot") * (hit.hits + hs))
        elif hit.is_ability and hit.ability is not None:
            cls = hit.ability.ab.class_name
            if cls == "ability_vampirebat_batswarm":
                self.build(c, target, c.raw("BuildUpPerBat"))
            elif cls == "ability_vampirebat_steallife":
                self.build(c, target, c.raw("BuildUpPerDagger"))
            elif not hit.is_dot:
                self.build(c, target, c.raw("BuildUpPerShot"))

    def build(self, c, target, amount):
        st = c.state
        if c.now < st["ready"] or not target.alive:
            return
        if c.now - st["last"] > c.raw("BuildUpDuration", 5):
            st["meter"] = 0.0
        st["last"] = c.now
        st["meter"] += amount
        if st["meter"] < 100:
            return
        st["meter"] = 0.0
        cdr = 1.0 - max(0.0, min(0.95, c.me.st.cdr + c.me.stat("cdr")))
        st["ready"] = c.now + c.raw("PerTargetCooldown") * cdr
        c.engine.damage(c.me, target, c.val("BonusDamage"), "spirit", self.s.ab.name, is_ability=True,
                        ability=self.s)
        if c.raw("BonusFireRate"):
            c.buff("fire_rate", c.raw("BonusFireRate") / 100, c.dur("BuffDuration"), tag="love_bites_fr")
        nox = next((a for a in c.me.abilities if a.ab.class_name == "ability_vampirebat_batswarm"), None)
        if nox is not None:
            mx = nox.ctx.raw("BonusBatsMax", 50)
            c.me.counters[BATS_KEY] = min(mx, c.me.counters.get(BATS_KEY, 0) + nox.ctx.raw("BonusBatsPerProc", 2))


@register("ability_vampirebat_batswarm")
class NoxNostra(AbilityImpl):
    kind = "target"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        n = int(c.raw("BatCount", 75) + c.me.counters.get(BATS_KEY, 0))
        rate = max(1.0, c.raw("BatPerSecond", 30))
        travel = c.dist / max(1.0, c.raw("JumpSpeed", 17))
        for i in range(n):
            c.after(delay + travel + i / rate, self.bat, c)

    def bat(self, c):
        f, e = c.me, c.foe
        if not (f.alive and e.alive):
            return
        dmg = c.val("Damage") + e.hp * c.raw("CurrentHealthPercent") / 100
        c.engine.damage(f, e, dmg, "spirit", self.s.ab.name, is_ability=True, ability=self.s, is_ult=True)
        c.debuff("silence", 1, c.raw("DebuffDuration", 1.25), tag="nox_silence")
