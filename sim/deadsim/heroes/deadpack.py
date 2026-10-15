"""Deadman Danny (hero_deadpack). New hero (2026-10-13); modeled from tooltip text and data.

Assumptions:
- "Weapon damage" abilities (EBaseWeaponDamageIncrease scaling, applied by c.val as x (1 + k x weapon %)) are
  dealt as bullet damage without item procs.
- Strix Salvo: MarksTotal missiles (T3 +2) lodge along the line; MISSILE_HIT_FRAC of them (x spirit
  accuracy) detonate on the target, each dealing Damage and leaving a mark. Danny consumes one mark per charged
  shot every CHARGED_SHOT_INTERVAL s while marks last (CoatedDuration), each for CoatedDamage. Charged shots are
  not otherwise modeled (the gun keeps its normal cycle). Mark damage is booked as "Strix Salvo (mark)".
- Chimera Mk1: fly in (reach CHIMERA_REACH), dive DIVE_TIME s after cast (players dive early). Danny can shoot
  while flying. The dive hits at spirit accuracy for ExplosionDamage (spirit) + ExplosionBulletDamage (weapon).
  On a miss he self-stuns OverheatStunDurationSelf. He takes MaxHealthSelfDamagePercent of max health unless T2
  and a hero was hit; T2 heals HealOnHit (150 + 1.0 x spirit) on hit instead. Cooldown shrinks
  0.25 s per boon (ELevelUpBoons tag); T3 -40% cooldown on hit.
- Jettison Fuel: spray for AbilityDuration (gun locked) dealing DPS weapon damage and shredding bullet resist
  for DebuffDuration; the backblast at the end deals ScorchDamage. T2 fire-rate buff on backblast hit; T3 adds
  one Strix mark.
- Close The Deal: cast when target is at or below CTD_HP. Grab, rise for RISE_TIME, then fall FALL_TIME taking
  DamagePerMeter over MaxHeight (units -> m) as a DoT, then impact Damage; +BonusDamagePercent when the target is
  below 50%. Both are out of the fight during the flight (target stunned, Danny's gun locked); Danny takes
  SelfDamagePercent of the damage dealt as spirit self-damage (can't kill him). Stun on landing.
"""
from deadsim.abilities import AbilityImpl, register

UNITS_PER_METER = 39.37
MISSILE_HIT_FRAC = 0.67
CHARGED_SHOT_INTERVAL = 1.5
CHIMERA_REACH = 20.0
DIVE_TIME = 1.5
CTD_HP = 0.65
RISE_TIME = 1.0
FALL_TIME = 1.0


def find(c, class_name):
    for ab in c.me.abilities:
        if ab.ab.class_name == class_name:
            return ab
    return None


@register("ability_deadpack_chargeblast")
class StrixSalvo(AbilityImpl):
    kind = "skillshot"
    range_props = ("Range",)

    def start(self, c):
        c.state["marks"] = 0
        c.state["marks_until"] = -1.0
        c.state["consuming"] = False

    def add_marks(self, c, n):
        if c.now > c.state["marks_until"]:
            c.state["marks"] = 0
        c.state["marks"] += n
        c.state["marks_until"] = c.now + c.val("CoatedDuration")
        if not c.state["consuming"]:
            c.state["consuming"] = True
            c.after(CHARGED_SHOT_INTERVAL, self.consume, c)

    def consume(self, c):
        st = c.state
        if st["marks"] <= 0 or c.now > st["marks_until"] or not c.me.alive or not c.foe.alive:
            st["consuming"] = False
            return
        if c.me.can_shoot():
            st["marks"] -= 1
            c.spirit_hit(c.val("CoatedDamage"), name=self.s.ab.name + " (mark)", hit_chance=1.0)
        c.after(CHARGED_SHOT_INTERVAL, self.consume, c)

    def cast(self, c):
        n = int(c.raw("MarksTotal", 3))
        hits = c.me.acc("strix").take(MISSILE_HIT_FRAC * c.me.skill.spirit_accuracy, n)
        if hits <= 0:
            return
        arm = c.raw("MineArmTime", 0.3) + 0.3
        c.spirit_hit(c.val("Damage") * hits, delay=arm, hit_chance=1.0)
        c.after(arm, self.add_marks, c, hits)


@register("ability_deadpack_rocketeer")
class ChimeraMk1(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.dist <= CHIMERA_REACH

    def cast(self, c):
        f = c.me
        s = self.s
        cd = max(1.0, s.cooldown() - abs(c.scale("AbilityCooldown")) * f.st.boons)
        s.ready_at = c.now + cd
        delay = c.raw("AbilityCastDelay", 0.7)
        c.lock_gun(delay)
        hit = bool(f.acc("chimera").take(f.skill.spirit_accuracy))
        t = delay + DIVE_TIME
        selfdmg = f.max_hp * c.raw("MaxHealthSelfDamagePercent") / 100
        if hit:
            c.spirit_hit(c.val("ExplosionDamage"), delay=t, hit_chance=1.0)
            c.after(t, lambda: c.foe.alive and c.engine.damage(f, c.foe, c.val("ExplosionBulletDamage"),
                                                              "bullet", s.ab.name, is_ability=True, ability=s,
                                                              procs=False))
            if c.tier >= 2:
                c.after(t, lambda: f.alive and c.heal(c.val("HealOnHit")))
            else:
                c.after(t, c.self_damage, selfdmg)
            if c.tier >= 3:
                s.ready_at = c.now + cd * (1 - c.raw("OverheatLockoutDurationReductionOnPlayerHitPercent") / 100)
        else:
            c.after(t, c.self_damage, selfdmg)
            c.after(t, lambda: f.mods.add("stun", 1, c.raw("OverheatStunDurationSelf"), "chimera_self"))
        s.next_charge = s.ready_at


@register("ability_deadpack_flamethrower")
class JettisonFuel(AbilityImpl):
    kind = "aoe"

    def cast(self, c):
        f = c.me
        s = self.s
        d = c.dur("AbilityDuration")
        c.lock_gun(d)
        shred = abs(c.raw("BulletResistReduction")) / 100
        dd = c.val("DebuffDuration")
        c.debuff("bullet_shred", shred, dd)
        dps = c.val("DPS")
        tick = 0.25
        for i in range(1, int(d / tick) + 1):
            c.after(i * tick, lambda: c.foe.alive and f.alive and c.engine.damage(
                f, c.foe, dps * tick, "bullet", s.ab.name, is_ability=True, ability=s, is_dot=True, procs=False))
        c.spirit_hit(c.val("ScorchDamage"), delay=d, name=s.ab.name + " backblast")
        if c.tier >= 2:
            c.after(d, lambda: c.buff("fire_rate", c.raw("BonusFireRate") / 100, c.raw("BuffDuration")))
        if c.tier >= 3:
            sx = find(c, "ability_deadpack_chargeblast")
            if sx is not None and sx.unlocked:
                c.after(d, sx.impl.add_marks, sx.ctx, int(c.raw("BurstMarkStacks", 1)))


@register("ability_deadpack_ultimate")
class CloseTheDeal(AbilityImpl):
    kind = "target"

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac <= CTD_HP

    def cast(self, c):
        f, foe = c.me, c.foe
        delay = c.raw("AbilityCastDelay", 0.5)
        flight = RISE_TIME + FALL_TIME
        c.lock_gun(delay + flight + c.raw("StunDurationSelf", 0.4))
        meters = c.raw("MaxHeight", 1700) / UNITS_PER_METER
        self_pct = c.raw("SelfDamagePercent") / 100

        def mult():
            low = foe.hp_frac < c.raw("LowHealthEnemyThresholdPct", 50) / 100
            return 1.0 + (c.raw("BonusDamagePercent") / 100 if low else 0.0)

        def deal(amount):
            if not foe.alive or not f.alive:
                return
            dealt = c.engine.damage(f, foe, amount * mult(), "spirit", self.s.ab.name, is_ability=True,
                                    ability=self.s, is_ult=True)
            c.self_damage(dealt * self_pct, kind="spirit")

        def grab():
            if not foe.alive or not f.alive:
                return
            foe.mods.add("stun", 1, flight, "close_the_deal")
            n = 4
            per = c.val("DamagePerMeter") * meters / n
            for i in range(n):
                c.after(RISE_TIME + FALL_TIME * (i + 1) / n, deal, per)
            c.after(flight, deal, c.val("Damage"))
            c.debuff("stun", 1, c.val("StunDuration"), delay=flight)
        c.after(delay, grab)
