"""Rem (hero_familiar).

Assumptions:
- Pillow Toss: skillshot that lands after cast delay + TossDuration. On a hit, Rem's other abilities have
  CDReduceOnPillowHit seconds taken off their cooldown (scaled by spirit_accuracy, as an expected value).
  T2: -FireRateSlow% fire rate for EffectDuration (the fading-slow window). The knockback is ignored.
- Tag Along: it needs an ally (or a trooper with a Helper), which a 1v1 doesn't have, so it is never cast.
  The heal and the T3 spirit power only happen while napping on an ally, which takes Rem out of the duel.
- Lil Helpers: Rem sends a Helper to follow himself ("Follow a hero"), for a short burst of +TechArmorGain%
  spirit resist (+15% at T3) lasting HELPER_BURST (not in data). Each Helper then naps for HelperDowntimeDuration.
  HelperCount Helpers are used in turn. The trooper/box chores don't exist in a 1v1.
- Naptime: Rem channels for AbilityChannelTime (gun locked, -DamageResistPctWhileChanneling% damage taken via
  bullet/spirit resist). The target then sleeps (modeled as a stun) for up to SleepDuration, and takes AwakeDamage
  when he wakes. Damage from Rem past SleepDamageThreshold (100 + 3.1 per boon, Rem's boons) wakes him after
  MinSleepTime. Rem holds fire for the sleep (reloads, lines up) and only his DoTs/items can wake the target
  early. Cast when the target is within Radius (+ engage margin) and not almost dead.
"""
from deadsim.abilities import AbilityImpl, register

HELPER_BURST = 3.0   # s of spirit resist from a Helper following a hero ("short burst", no duration in data)


@register("ability_familiar_ability02")
class PillowToss(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        d = c.raw("AbilityCastDelay")
        land = d + c.raw("TossDuration")
        c.lock_gun(d + c.raw("AbilityPostCastDuration"))
        c.spirit_hit(c.val("Damage"), delay=land)
        acc = c.me.skill.spirit_accuracy
        cdr = c.raw("CDReduceOnPillowHit") * acc
        c.after(land, self.refund, c, cdr)
        if c.raw("FireRateSlow"):
            c.debuff("fire_rate_slow", c.raw("FireRateSlow") / 100 * acc, c.dur("EffectDuration"), delay=land)

    def refund(self, c, secs):
        if not c.me.alive:
            return
        for ab in c.me.abilities:
            if ab is not self.s:
                ab.ready_at = max(c.now, ab.ready_at - secs)
                if ab.next_charge:
                    ab.next_charge = max(c.now, ab.next_charge - secs)


@register("ability_familiar_attach")
class TagAlong(AbilityImpl):
    kind = "passive"   # ally-only; no ally in a 1v1


@register("ability_familiar_helpinghands")
class LilHelpers(AbilityImpl):
    kind = "self"

    def start(self, c):
        c.state["free_at"] = [0.0] * max(1, int(c.raw("HelperCount", 1)))

    def should_cast(self, c):
        st = c.state
        n = max(1, int(c.raw("HelperCount", 1)))
        while len(st["free_at"]) < n:
            st["free_at"].append(0.0)
        busy = c.me.mods.get("spirit_resist", "lil_helper") is not None
        return c.foe.alive and not busy and min(st["free_at"]) <= c.now

    def cast(self, c):
        st = c.state
        i = st["free_at"].index(min(st["free_at"]))
        dur = HELPER_BURST * (1.0 + c.s.duration_pct())
        st["free_at"][i] = c.now + dur + c.raw("HelperDowntimeDuration")
        c.buff("spirit_resist", c.raw("TechArmorGain") / 100, dur, tag="lil_helper")


@register("ability_familiar_ability01")
class Naptime(AbilityImpl):
    kind = "aoe"
    range_props = ("Radius",)

    def start(self, c):
        c.state.update(asleep=False)

    def should_cast(self, c):
        return self.in_range(c) and c.foe.hp_frac > 0.15

    def cast(self, c):
        ch = c.raw("AbilityCastDelay") + c.dur("AbilityChannelTime")
        c.lock_gun(ch)
        red = c.raw("DamageResistPctWhileChanneling") / 100
        c.buff("bullet_resist", red, ch, tag="naptime_dr_b")
        c.buff("spirit_resist", red, ch, tag="naptime_dr_s")
        c.after(ch, self.sleep, c)

    def sleep(self, c):
        if not c.me.alive or not c.foe.alive:
            return
        st = c.state
        dur = c.dur("SleepDuration")
        st.update(asleep=True, since=c.now, taken=0.0, token=object(),
                  threshold=c.val("SleepDamageThreshold"))
        c.debuff("stun", 1, dur, tag="naptime_sleep")
        c.lock_gun(dur)
        c.after(dur, self.wake, c, st["token"])

    def on_damage_dealt(self, c, target, hit):
        st = c.state
        if not st.get("asleep") or hit.source == self.s.ab.name:
            return
        st["taken"] += hit.amount
        if st["taken"] >= st["threshold"]:
            c.after(max(0.0, st["since"] + c.raw("MinSleepTime") - c.now), self.wake, c, st["token"])

    def wake(self, c, token):
        st = c.state
        if not st.get("asleep") or st.get("token") is not token:
            return
        st["asleep"] = False
        c.foe.mods.remove("stun", "naptime_sleep")
        c.me.gun_locked_until = min(c.me.gun_locked_until, c.now)
        if c.me.alive:
            c.spirit_hit(c.val("AwakeDamage"))
