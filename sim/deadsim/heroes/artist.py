"""Violet (hero_artist).

Assumptions:
- Living Ink: a charge empowers the next MaxShots gun shots for AbilityDuration. Steered bullets hit at the
  better of the caster's gun and spirit accuracy (they home in), deal BulletDamageMultiplier % of a gun bullet
  plus Damage spirit splash. As in the game's damage events, the bullet is a gun hit (same tick as the splash,
  booked under the weapon) and only the splash is booked under Living Ink. Each landed shot cuts the other abilities' cooldowns by
  CooldownReductionPerHit and active item cooldowns by half of it (replays: the other cooldown starts step back
  1.5 s per hit, Living Ink's own never does). While empowered the gun fires FireRateSlow %
  slower. T2: each empower adds a +BonusFireRatePerStack % fire rate stack (MaxStacks, StackDuration).
  Draw (alt fire: an ink wall) is movement/blocking only and not modeled.
- Living Ink passive ("casting any other ability refreshes the cooldown of Flow State") is not a cooldown reset:
  in Phantom+ replays Flow State casts are at least ~21 s apart (p10 of 44 gaps, cooldown 23 s), so it is left out.
- Flow State: the brush travels at DashSpeed m/s (no brush speed in the data; assumed the same) and is flicked
  when it reaches the target: damage grows from MinDamage to MaxDamage over MaxDamageTime of travel. Trail damage
  and the slow are folded into that one hit (the landing factor fits the real total). T3 damage amp is taken at
  its full OutgoingDamagePercent for DamageAmpDuration once half of DamageAmpBuildDuration has passed (it builds
  while sliding on the trail). T1 stamina is movement only.
- Still Life: lock-on within AbilityCastRange. The sketch fills BuildUpPerSecond per s, BuildUpPerShot per landed
  gun shot and BuildUpPerAbility per ability hit (a Living Ink hit counts once, as its gun shot); it deals DPS every
  TickInterval while drawing and at 100 deals Damage and stuns for StunDuration. Violet keeps shooting meanwhile.
  The draw gives up after SKETCH_MAX s (no limit in the data). T1 regen (HealthRegen, spirit scaled) on cast and
  again on pickup (the sketch is assumed picked up), T2 the subject deals OutgoingDamagePercent less while drawn.
  The permanent per-sketch stats are not modeled (they depend on how many sketches were taken earlier in the game).
- Abstract Landscape: cast when the target is within GroveRadius. Violet stands inside for AbilityDuration and
  gains TechPower spirit power (T2 also spirit lifesteal). The target walks out through the ink at GROVE_FIRST_HIT
  s, taking Damage and Silence (the slow is skipped), and crosses it again GROVE_HITS - 1 times on average (replay
  numbers at the constants). Each crossing is assumed to hit; T3 (ink not destroyed) is not modeled beyond that.
  Vision blocking is not modeled.
"""
from deadsim.abilities import AbilityImpl, register

LIVING_INK = "Living Ink"
SKETCH_MAX = 6.0     # s a Still Life draw keeps going before it is given up (no limit in the data)
# Abstract Landscape, from Phantom+ replays (97 casts): an enemy that takes its damage first does at 3.7 s after the
# cast (median; channel included), and is hit 1.71 times on average (it crosses the ink again 1.3 s later)
GROVE_FIRST_HIT = 3.7
GROVE_HITS = 1.71
GROVE_REHIT_GAP = 1.3


def cut_cooldowns(c, secs):
    """Living Ink hit: every other ability cooldown - secs, active item cooldowns - secs / 2."""
    now = c.now
    for ab in c.me.abilities:
        if ab is c.s:
            continue
        if ab.ready_at > now:
            ab.ready_at = max(now, ab.ready_at - secs)
        if ab.next_charge:
            ab.next_charge = max(now, ab.next_charge - secs)
    for fx in c.me.items_fx:
        it = getattr(fx, "item", None)   # hero effects (parry, revive, ...) sit in items_fx without an item
        if it is not None and it.activation != "passive" and fx.ready_at > now:
            fx.ready_at = max(now, fx.ready_at - secs / 2)


@register("ability_artist_homingbrush")
class LivingInk(AbilityImpl):
    kind = "self"

    def start(self, c):
        c.state.update(shots=0, until=-1.0, stacks=0, stacks_until=-1.0)

    def in_range(self, c):
        return c.engine.hit_reach(c.me.st) > 0

    def should_cast(self, c):
        st = c.state
        return c.foe.alive and (st["shots"] <= 0 or c.now >= st["until"]) and self.in_range(c)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay + c.raw("AbilityPostCastDuration"))
        st = c.state
        d = c.dur("AbilityDuration")
        st["shots"], st["until"] = int(c.raw("MaxShots", 3)), c.now + delay + d
        if c.raw("FireRateSlow"):
            c.buff("fire_rate", -c.raw("FireRateSlow") / 100, delay + d, tag="living_ink_slow")
        if c.raw("BonusFireRatePerStack"):
            if c.now >= st["stacks_until"]:
                st["stacks"] = 0
            st["stacks"] = min(int(c.raw("MaxStacks", 5)), st["stacks"] + 1)
            sd = c.dur("StackDuration", 10)
            st["stacks_until"] = c.now + sd
            c.buff("fire_rate", c.raw("BonusFireRatePerStack") / 100 * st["stacks"], sd, tag="living_ink_stacks")

    def on_shot(self, c, ctx):
        st = c.state
        if st["shots"] <= 0:
            return
        if c.now >= st["until"]:
            st["shots"] = 0
            c.me.mods.remove("fire_rate", "living_ink_slow")
            return
        st["shots"] -= 1
        if st["shots"] <= 0:
            c.me.mods.remove("fire_rate", "living_ink_slow")
        ctx["pellet_mult"] = 0.0   # this shot is the steered bullet below, not a gun shot
        f, e, eng = c.me, c.foe, c.engine
        sk = f.skill
        p = min(1.0, max(sk.accuracy, sk.spirit_accuracy) * (1.0 - e.stat("evasion")) * eng.hit_reach(f.st))
        if f.acc("living_ink").take(p, 1) <= 0:
            return
        heads = f.head_acc.take(sk.headshot, 1)
        per, crit = eng.bullet_damage(f, ctx["extra_pct"])
        per *= ctx["dmg_mult"] * c.raw("BulletDamageMultiplier", 100) / 100
        crit_eff = 1.0 + (crit - 1.0) * e.st.crit_received_scale * (1.0 + e.stat("crit_taken"))
        f.bullets_hit += 1
        f.headshots_hit += heads
        eng.damage(f, e, per * (crit_eff if heads else 1.0), "bullet", "gun", headshots=heads, hits=1)
        eng.damage(f, e, c.val("Damage"), "spirit", self.s.ab.name, is_ability=True, ability=self.s)
        cut_cooldowns(c, c.raw("CooldownReductionPerHit"))


@register("ability_artist_rollingprojectile")
class FlowState(AbilityImpl):
    kind = "skillshot"

    def speed(self, c):
        return max(1.0, c.raw("DashSpeed", 20.0))

    def in_range(self, c):
        return c.within(self.speed(c) * c.raw("MaxDamageTime", 2.0) + c.rng("ExplosionRadius"))

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        travel = c.dist / self.speed(c)
        x = min(1.0, travel / max(0.1, c.raw("MaxDamageTime", 2.0)))
        lo, hi = c.val("MinDamage"), c.val("MaxDamage")
        c.spirit_hit(lo + (hi - lo) * x, delay=delay + travel)
        if c.raw("OutgoingDamagePercent"):
            c.after(delay + c.raw("DamageAmpBuildDuration") / 2, self.amp, c)

    def amp(self, c):
        if c.me.alive:
            c.buff("damage_amp", c.raw("OutgoingDamagePercent") / 100, c.dur("DamageAmpDuration"))


@register("ability_artist_tether")
class StillLife(AbilityImpl):
    kind = "target"

    def start(self, c):
        c.state.update(active=False, meter=0.0)

    def in_range(self, c):
        return c.within(c.rng("AbilityCastRange"))

    def cast(self, c):
        st = c.state
        st.update(active=True, meter=0.0, start=c.now, epoch=st.get("epoch", 0) + 1)
        if c.raw("HealthRegen"):
            c.buff("regen", c.val("HealthRegen"), c.dur("BuffDuration", 4))
        if c.raw("OutgoingDamagePercent"):
            c.debuff("outgoing_penalty", abs(c.raw("OutgoingDamagePercent")) / 100, SKETCH_MAX, tag="still_life_t2")
        c.after(c.raw("TickInterval", 0.15), self.tick, c, st["epoch"])

    def end(self, c):
        c.state["active"] = False
        c.foe.mods.remove("outgoing_penalty", "still_life_t2")

    def tick(self, c, epoch):
        st = c.state
        if not st["active"] or st["epoch"] != epoch:
            return
        if not (c.me.alive and c.foe.alive) or c.now - st["start"] > SKETCH_MAX or c.me.mods.active("stun"):
            self.end(c)
            return
        dt = c.raw("TickInterval", 0.15)
        c.engine.damage(c.me, c.foe, c.val("DPS") * dt, "spirit", self.s.ab.name, is_ability=True, ability=self.s,
                        is_dot=True)
        st["meter"] += c.raw("BuildUpPerSecond") * dt
        if not self.complete(c):
            c.after(dt, self.tick, c, epoch)

    def on_damage_dealt(self, c, target, hit):
        st = c.state
        if not st["active"] or hit.is_dot or hit.source == self.s.ab.name:
            return
        if hit.source == "gun" and hit.hits:
            st["meter"] += c.raw("BuildUpPerShot") * hit.hits / max(1, c.me.st.pellets)
        elif hit.is_ability and hit.source != LIVING_INK:   # an empowered hit counts once, as its gun shot
            st["meter"] += c.raw("BuildUpPerAbility")
        self.complete(c)

    def complete(self, c):
        st = c.state
        if not st["active"] or st["meter"] < 100:
            return False
        self.end(c)
        c.spirit_hit(c.val("Damage"))
        c.debuff("stun", 1, c.raw("StunDuration"))
        if c.raw("HealthRegen"):   # T1: refreshed on pickup
            c.buff("regen", c.val("HealthRegen"), c.dur("BuffDuration", 4))
        return True


@register("ability_artist_bamboogrove")
class AbstractLandscape(AbilityImpl):
    kind = "aoe"
    range_props = ("GroveRadius",)

    def cast(self, c):
        delay = c.raw("AbilityChannelTime")
        c.lock_gun(delay)
        d = c.val("AbilityDuration")
        c.buff("spirit_power", c.raw("TechPower"), delay + d)
        if c.raw("AbilityLifestealPercentHero"):
            c.buff("spirit_lifesteal", c.raw("AbilityLifestealPercentHero") / 100, delay + d)
        out = max(delay, GROVE_FIRST_HIT)
        c.spirit_hit(c.val("Damage"), delay=out)
        c.debuff("silence", 1, c.raw("SilenceDuration"), delay=out)
        c.spirit_hit(c.val("Damage") * (GROVE_HITS - 1), delay=out + GROVE_REHIT_GAP)
