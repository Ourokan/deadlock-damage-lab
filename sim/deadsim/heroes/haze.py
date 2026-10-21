"""Haze (hero_haze).

Assumptions:
- Sleep Dagger: sleep = stun that breaks SleepWakeUpDelay after the next damage Haze deals once
  MinimumSleepTime has passed. Haze throws it while reloading (or when her clip is empty), so the sleep
  covers her reload. T1 bullet-resist shred applies on wake-up; T2 adds FixationStacks Fixation stacks.
- Smoke Bomb: invisibility has no 1v1 combat value, so it is only cast with T3 (fight start, then whenever
  ready below SMOKE_HP): Haze breaks invisibility at once by shooting, getting the post-invis bullet
  lifesteal for PostInvisBuffDuration and dispelling her debuffs.
- Fixation: +DamageBonusFixedPerStack flat bullet damage per hit per stack (1 stack per hit, HeadshotStacks per
  headshot), stacks refresh to AbilityDuration on each hit and drop all at once when it expires. The bonus is
  booked as its own bullet damage under "Fixation" (the game's damage report lists it apart from the gun), gets
  the headshot multiplier and falloff, does not trigger on-hit procs (the bullet already did), and does not
  scale with weapon damage until T3 (T3: +0.11 per stack and an EBaseWeaponDamageIncrease scale of 0.00035 from
  the data, applied as is by c.val; doubt: that factor makes the weapon scaling negligible).
  T1 proc: every ProcDamageStackCount stacks gained, ProcDamage (40 + 0.8 x spirit) spirit damage.
- Bullet Dance: after AbilityCastDelay Haze fires at BonusFireRate extra fire rate for AbilityDuration with
  perfect accuracy, no headshots, without spending ammo, each bullet getting +WeaponDamageBonus flat damage
  (data: FLAT_BULLET_DAMAGE_POST_SCALE, so not multiplied by weapon damage); Fixation books its stack bonus. She gains EvasionPercent evasion for the duration.
  Its landing factor (data/landing_rates*.json, low because the ult is up in few real fights) shortens the channel
  rather than scaling its bullets, so the gun lock shrinks with it.
"""
from deadsim.abilities import AbilityImpl, register

SMOKE_HP = 0.6
ENEMY_DEBUFFS = ("stun", "silence", "disarm", "item_silence", "damage_taken_amp", "spirit_amp_taken",
                 "bullet_amp_taken", "bullet_shred", "spirit_shred", "fire_rate_slow", "outgoing_penalty",
                 "spirit_outgoing_penalty", "crit_taken")


def fixation(f):
    for ab in f.abilities:
        if ab.ab.class_name == "ability_stacking_damage" and ab.unlocked:
            return ab
    return None


@register("ability_sleep_dagger")
class SleepDagger(AbilityImpl):
    kind = "skillshot"
    TAG = ("haze_sleep", "stun")

    def should_cast(self, c):
        return c.me.reload_until > c.now or c.me.clip <= 2

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        if c.me.acc("sleep_dagger").take(c.me.skill.spirit_accuracy) == 0:
            return
        c.spirit_hit(c.val("Damage"), delay=delay, hit_chance=1.0)
        c.debuff("stun", 1, c.dur("SleepDuration"), tag=self.TAG, delay=delay)
        c.state["asleep_from"] = c.now + delay
        c.after(delay, self._mark, c)
        fx = fixation(c.me)
        if c.tier >= 2 and fx:
            c.after(delay, fx.impl.add_stacks, fx.ctx, c.raw("FixationStacks"))

    def _mark(self, c):
        c.state["sleeping"] = True

    def on_any_damage_dealt(self, c, target, hit):   # any damage wakes, DoT ticks (Alchemical Fire) included
        st = c.state
        if not st.get("sleeping") or hit.source == self.s.ab.name:
            return
        if c.now - st["asleep_from"] < c.raw("MinimumSleepTime", 0.2):
            return
        st["sleeping"] = False
        c.after(c.val("SleepWakeUpDelay", 0.1), self._wake, c)

    def _wake(self, c):
        if c.foe.mods.get("stun", self.TAG) is None:
            return
        c.foe.mods.remove("stun", self.TAG)
        if c.tier >= 1:
            c.debuff("bullet_shred", abs(c.raw("BulletResistReduction")) / 100, c.dur("BulletResistReductionDuration"))


@register("ability_smoke_bomb")
class SmokeBomb(AbilityImpl):
    kind = "self"

    def in_range(self, c):
        return True

    def should_cast(self, c):
        return c.tier >= 3 and (c.now < 0.2 or c.me.hp_frac < SMOKE_HP)

    def cast(self, c):
        for key in ENEMY_DEBUFFS:
            c.me.mods.d.pop(key, None)
        c.buff("bullet_lifesteal", c.raw("BulletLifesteal") / 100, c.dur("PostInvisBuffDuration"))


@register("ability_stacking_damage")
class Fixation(AbilityImpl):
    kind = "passive"

    def start(self, c):
        c.state.update(stacks=0.0, expire=-1.0, gained=0.0)

    def stacks(self, c):
        return c.state["stacks"] if c.now < c.state["expire"] else 0.0

    def flat(self, c):
        """Flat bonus damage per bullet hit at the current stack count."""
        return c.val("DamageBonusFixedPerStack") * self.stacks(c)

    def add_stacks(self, c, n):
        if c.now >= c.state["expire"]:
            c.state["stacks"] = 0.0
        c.state["stacks"] = min(c.raw("MaxStacks"), c.state["stacks"] + n)
        c.state["expire"] = c.now + c.dur("AbilityDuration")
        if c.tier >= 1:
            c.state["gained"] += n
            every = c.raw("ProcDamageStackCount", 20)
            while c.state["gained"] >= every:
                c.state["gained"] -= every
                c.spirit_hit(c.val("ProcDamage"), name="Fixation proc", hit_chance=1.0)

    def on_damage_dealt(self, c, target, hit):
        if hit.kind != "bullet" or not hit.hits or hit.source == self.s.ab.name:
            return
        f, e = c.me, c.foe
        bonus = self.flat(c)
        if bonus > 0:   # the stack bonus is its own damage source in the game's damage report
            _, crit = c.engine.bullet_damage(f)
            crit_eff = 1.0 + (crit - 1.0) * e.st.crit_received_scale * (1.0 + e.stat("crit_taken"))
            body = hit.hits - hit.headshots
            amt = bonus * f.st.falloff(c.dist) * (body + hit.headshots * crit_eff)
            c.engine.damage(f, e, amt, "bullet", self.s.ab.name, is_ability=True, ability=self.s,
                            hits=hit.hits, headshots=hit.headshots, procs=False)
        self.add_stacks(c, hit.hits - hit.headshots + hit.headshots * c.raw("HeadshotStacks", 3))


@register("ability_bullet_flurry")
class BulletDance(AbilityImpl):
    kind = "aoe"

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.2

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        # the landing factor shortens the channel instead of scaling its bullets: the factor mostly says how
        # rarely the ult is up in a real fight, and scaling damage alone kept the full gun lock, so casting it
        # cost Haze more gun damage than it dealt (0.11 landing = 0.4 s of Bullet Dance, then the gun again)
        T = c.val("AbilityDuration") * min(1.0, c.me.skill.ability_landing.get(self.s.ab.name, 1.0))
        c.lock_gun(delay + T)
        c.buff("evasion", c.raw("EvasionPercent") / 100, delay + T)
        c.state["end"] = c.now + delay + T
        c.after(delay, self.shoot, c)

    def shoot(self, c):
        f = c.me
        if not f.alive or not c.foe.alive or c.now > c.state["end"] + 1e-9:
            return
        if f.mods.active("stun"):
            f.gun_locked_until = c.now
            return
        base, _ = c.engine.bullet_damage(f)
        per = base + c.raw("WeaponDamageBonus")    # flat bonus is post-scale; Fixation books its own bonus
        c.gun_volley(f.st.pellets, per, accuracy=1.0, headshots=False, landed=True)
        rate = 1.0 + f.fire_rate() + c.raw("BonusFireRate") / 100
        c.after(f.st.cycle_time / max(0.05, rate), self.shoot, c)
