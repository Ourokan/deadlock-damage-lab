"""Vindicta (hero_hornet).

Assumptions:
- Stake: Damage on capture; the tether itself is movement-only.
- Flight: while flying every gun bullet that hits adds MagicDamagePerBullet spirit damage. T1's +50% ammo is
  given as bonus ammo on cast (removed when Flight ends). Accuracy while flying is unchanged.
- Crow Familiar: landing rate = spirit_accuracy. Bleed deals DotHealthPercent of the target's *current* health
  per TickRate as spirit damage for DebuffDuration. Resist reductions applied as bullet/spirit shred.
  Replays (2026-11-07, 49 Phantom+ matches, 1,750 crow hits; scratch crow scripts, ability id 2048438176): each tick
  is ~2.4% of the health the target has, and the target sits at 0.61 / 0.57 / 0.52 of max health at the ticks in
  lane / mid / late, where the sim's duel target sat at 0.76 (it opens on a full-health foe). BLEED_CURRENT ticks on
  Fighter.item_hp (the real entry deficit and third parties' damage, as Tankbuster/Decay and Stalker's Mark).
  Real bleeds also end early without a kill (BLEED_BREAK, opt-in OFF: it lowered sim_vs_win_raw on all four day/budget
  splits, mostly by taking value from spirit items whose real edge is high): after the impact and after each tick the bleed is gone
  with a per-tick chance of 0.037 in lane, 0.099 mid, 0.130 late (16% / 36% / 43% of hits cut short; mostly on
  mobile targets: Vyper, Mina, Rat King, Pocket, Calico cut 0.7-0.9 of bleeds; Bebop, Kelvin, Billy ~0.1). The sim
  books that as an expected value: tick k is weighted by (1 - hazard)^(k + 1). Real ticks per hit 4.2 / 3.6 / 3.3,
  sim 4.6 (3.5 with it on). BLEED_CURRENT alone: Vindicta mix 0.020 -> 0.013 (halves 0.016 -> 0.009, 0.025 -> 0.017),
  Crow real/sim 0.77 -> 0.82, sim_vs_win_raw flat-up; a Vindicta corr refit on top failed the split-half mix (not kept).
- Assassinate: spirit damage (as in game); scoping for TimeToFullCharge locks the gun and the shot is always
  full charge. HeadshotBonus (+20%) is applied at the caster's headshot rate. Used as an execute: only when the
  target is under LowHealthEnemyThresholdPct or the shot would kill. Both checks and the low-health bonus use the
  target's gate health (Mechanics.entry_gate: short by its real entry deficit).
"""
from deadsim.abilities import AbilityImpl, register

BLEED_CURRENT = True   # Crow bleed ticks on Fighter.item_hp (real-like current health); False = plain duel health (old)
BLEED_BREAK = False    # opt-in: real bleeds end early without a kill (per-tick hazard by phase); off: lowered sim_vs_win_raw
BREAK_HAZARD = ((10000, 0.037), (27000, 0.099), (float("inf"), 0.130))   # (net worth below, chance per tick)


def break_hazard(souls):
    return next(h for hi, h in BREAK_HAZARD if souls < hi) if BLEED_BREAK else 0.0

@register("citadel_ability_hornet_chain")
class Stake(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(25 + c.me.skill.engage_margin)   # thrown projectile, ~25 m practical range

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        c.spirit_hit(c.val("Damage"), delay=delay)


@register("citadel_ability_hornet_leap")
class Flight(AbilityImpl):
    kind = "self"

    def in_range(self, c):
        return True

    def cast(self, c):
        d = c.dur("AbilityDuration")
        c.lock_gun(c.raw("AbilityChannelTime"))
        c.state["until"] = c.now + d
        if c.tier >= 1:
            extra = int(c.me.st.clip * c.raw("BonusClipSizePercent") / 100)
            c.me.bonus_ammo += extra
            c.after(d, self.end_ammo, c)

    def end_ammo(self, c):
        c.me.bonus_ammo = 0

    def on_damage_dealt(self, c, target, hit):
        if hit.kind == "bullet" and hit.source == "gun" and hit.hits and c.now <= c.state.get("until", -1):
            c.spirit_hit(c.val("MagicDamagePerBullet") * hit.hits, hit_chance=1.0)


@register("citadel_ability_hornet_sting")
class CrowFamiliar(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(30 + c.me.skill.engage_margin)

    def cast(self, c):
        c.lock_gun(c.raw("AbilityPostCastDuration"))
        acc = c.me.skill.spirit_accuracy
        if not c.me.acc("crow_land").take(acc):
            return
        d = c.dur("DebuffDuration")
        c.spirit_hit(c.val("ImpactDamage"), hit_chance=1.0)
        c.debuff("bullet_shred", abs(c.raw("BulletResistReduction")) / 100, d)
        c.debuff("spirit_shred", abs(c.raw("TechArmorDamageReduction")) / 100, d)
        if c.tier >= 1:
            c.debuff("heal_received", c.raw("HealAmpReceivePenaltyPercent") / 100, d)
        token = object()
        c.state["bleed"] = token
        tick = c.raw("TickRate", 1.0)
        n = max(1, int(round(d / tick)))
        epoch = c.dot_track("crow_bleed", c.now + n * tick)
        keep = 1.0 - break_hazard(c.me.st.souls)
        c.after(tick, self.bleed, c, token, n, epoch, keep, keep)

    def bleed(self, c, token, n, epoch, w=1.0, keep=1.0):
        if c.state.get("bleed") is not token or not c.foe.alive or not c.me.alive or n <= 0 or not c.dot_live(epoch):
            return
        hp = c.foe.item_hp if BLEED_CURRENT else c.foe.hp
        amt = hp * c.raw("DotHealthPercent") / 100 * w
        if amt > 0:
            c.engine.damage(c.me, c.foe, amt, "spirit", self.s.ab.name, is_ability=True, ability=self.s, is_dot=True)
        c.after(c.raw("TickRate", 1.0), self.bleed, c, token, n - 1, epoch, w * keep, keep)


@register("citadel_ability_hornet_snipe")
class Assassinate(AbilityImpl):
    kind = "skillshot"

    def damage(self, c, low):
        dmg = c.val("Damage") + (c.val("LowHealthEnemyDamageBonus") if low else 0.0)
        return dmg * (1 + c.me.skill.headshot * c.raw("HeadshotBonus") / 100)

    def should_cast(self, c):
        thr = c.raw("LowHealthEnemyThresholdPct", 50) / 100
        if c.foe.gate_frac < thr:
            return True
        res = 1 - sum(c.foe.st.spirit_resist) if c.foe.st.spirit_resist else 1.0
        return self.damage(c, False) * c.me.skill.spirit_accuracy * res >= c.foe.gate_hp

    def cast(self, c):
        charge = c.raw("TimeToFullCharge", 1.0)
        c.lock_gun(charge)
        c.after(charge, self.shoot, c)

    def shoot(self, c):
        if not c.me.alive or not c.foe.alive:
            return
        low = c.foe.gate_frac < c.raw("LowHealthEnemyThresholdPct", 50) / 100
        c.spirit_hit(self.damage(c, low))
