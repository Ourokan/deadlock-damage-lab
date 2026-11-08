"""Paige (hero_bookworm).

Assumptions:
- Bookwyrm: the dragon hits once (Damage after StartupDelay), then the target stands in the burning trail for
  TRAIL_UPTIME of GroundFlameDuration plus the DebuffDuration linger. Reach is DragonTravelRange. With
  Mechanics.bookwyrm_burn (on) the burn is GroundFlameDuration x the real share of it a victim takes ticks for at
  Paige's net worth (burn_uptime: 0.20 in the lane, ~0.30 late; replays, scripts/mechanics/bookwyrm_burn.py), no linger.
- Plot Armor: a 1v1 has no ally, so the sim used to self-cast every one. Real Paiges give it to a teammate on a share
  of casts (Mechanics.plot_armor_self, replays): with fight draws (phase or rng) each cast is on Paige with that
  chance, else on an ally (cooldown spent, nothing for Paige); deterministic fights give her the bonuses x that share.
  On Paige: weapon bonus (BaseAttackDamagePercent) and the T1 fire rate (14% + 0.16 x spirit) last while the barrier
  holds. BonusSpiritDamagePercent is not in the
  description and is ignored. The shove is skipped.
- Captivating Read: skillshot (target can walk out during DetonationDelay); immobilize applied as a state with
  no movement effect. T3 spirit resist reduction modeled as spirit shred.
- Rallying Charge: the target is hit by one knight (not both waves). Amp grows with travelled distance; we
  assume the knights travel the fight distance, so amp = MaxAmp * dist / MaxAmpDistance. Allied heal ignored.
"""
import json
import math
import os

from deadsim.abilities import AbilityImpl, register
from deadsim.mechanics import _interp_ln, self_cast_share

TRAIL_UPTIME = 0.5
_BURN = None


def burn_uptime(souls):
    """Real share of GroundFlameDuration a Bookwyrm victim burns for at net worth souls (data/bookwyrm_burn.json,
    linear in ln net worth between bins, flat outside), None without the file."""
    global _BURN
    if _BURN is None:
        fn = os.path.join(os.path.dirname(__file__), "..", "..", "data", "bookwyrm_burn.json")
        _BURN = []
        if os.path.exists(fn):
            with open(fn) as fh:
                _BURN = [(math.log(b["net_worth"]), b["uptime"]) for b in json.load(fh)["bins"]]
    return _interp_ln(_BURN, souls) if _BURN else None


@register("ability_bookworm_dragonfire")
class Bookwyrm(AbilityImpl):
    kind = "skillshot"
    range_props = ("DragonTravelRange",)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay") + c.raw("StartupDelay")
        c.lock_gun(c.raw("AbilityCastDelay"))
        c.spirit_hit(c.val("Damage"), delay=delay)
        burn = c.dur("GroundFlameDuration") * TRAIL_UPTIME + c.dur("DebuffDuration")
        mech = c.engine.mech
        up = burn_uptime(c.me.st.souls) if mech is not None and getattr(mech, "bookwyrm_burn", False) else None
        if up is not None and c.me.st.souls:
            burn = c.dur("GroundFlameDuration") * up   # Mechanics.bookwyrm_burn: real ticks per victim
        c.dot(c.val("DPS"), burn, delay=delay, tick=c.raw("TickRate", 0.3), hit_chance=c.me.skill.spirit_accuracy)


@register("ability_bookworm_knightbarrier")
class PlotArmor(AbilityImpl):
    kind = "self"

    def should_cast(self, c):
        return c.reach(40)     # in combat

    def on_self(self, c):
        """Share of this cast's bonuses Paige keeps (Mechanics.plot_armor_self)."""
        return self_cast_share(c, "plot_armor_self", "plot_armor", self.s.casts)

    def cast(self, c):
        share = self.on_self(c)
        if share <= 0:
            return      # on a teammate (Mechanics.plot_armor_self): nothing for Paige
        d = c.dur("AbilityDuration")
        c.barrier(c.val("CombatBarrier"), d)
        b = c.me.barriers[-1]
        wpn = c.val("BaseAttackDamagePercent") / 100 * share
        fr = c.val("BonusFireRate") / 100 * share
        end = c.now + d

        def hook(f):
            if f.e.t < end and b[0] > 0:
                return {"weapon_pct": wpn, "fire_rate": fr}
            return {}
        if "plot_hook" in c.state:
            c.me.stat_hooks.remove(c.state["plot_hook"])
        c.state["plot_hook"] = hook
        c.me.stat_hooks.append(hook)


@register("ability_bookworm_aoemagic")
class CaptivatingRead(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        cd = c.raw("AbilityCastDelay")
        c.lock_gun(cd)
        delay = cd + c.raw("DetonationDelay", 1.25)
        acc = c.me.skill.spirit_accuracy
        c.spirit_hit(c.val("Damage"), delay=delay)
        c.debuff("immobilize", 1, c.dur("ImmobilizeDuration") * acc, delay=delay)
        if c.tier >= 3:
            c.debuff("spirit_shred", abs(c.raw("TechArmorDamageReduction")) / 100 * acc, c.dur("DebuffDuration"),
                     delay=delay)


@register("ability_bookworm_knightcharge")
class RallyingCharge(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        ch = c.raw("AbilityChannelTime", 0.7)
        c.lock_gun(ch)
        amp = c.raw("MaxAmp") / 100 * min(1.0, c.dist / max(1.0, c.raw("MaxAmpDistance", 250)))
        c.spirit_hit(c.val("Damage") * (1.0 + amp), delay=ch)
        c.debuff("stun", 1, c.dur("StunDuration") * c.me.skill.spirit_accuracy, delay=ch)
