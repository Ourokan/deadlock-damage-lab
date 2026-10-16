"""Item effects added in the coverage pass (Witchmail, Unstoppable, Haunting Shot, Runed Gauntlets, Restorative
Shot, Fortitude). Same handler API as items_fx; imported by items_fx before MODELED is built.

Still not modeled (no value in a fixed-distance 1v1 or no data): movement items (Slowing Hex, Mystic Slow,
Enduring Speed, Magic Carpet, Electric Slippers, Seraphim Wings, Shadow Strike), parry items (Rebuttal,
Counterspell), multi-target (Split Shot, Ricochet), team or economy items (Healing Rite, Celestial Blessing,
Golden Goose Egg, Trophy Collector, Glass Cannon stacks, Eternal Gift), and the legendaries Frostbite Charm, Omnicharge Signet, Mystical Piano, Prism Blast,
Unstable Concoction, Nullification Burst, Shrink Ray, Vortex Web, Cloak of Opportunity.
"""
from __future__ import annotations

from .items_fx import CC_KEYS, FX, _basic_melee, _melee_proc, handler

# ability properties that mark a crowd-control cast (Unstoppable is popped in answer to these)
CC_PROPS = ("StunDuration", "SleepDuration", "ImmobilizeDuration", "SilenceDuration", "DisarmDuration",
            "ChainDuration")


def _cut_cooldown(ab, now, seconds):
    if ab.ready_at > now:
        ab.ready_at = max(now, ab.ready_at - seconds)


@handler("upgrade_absorbing_armor")
class Witchmail(FX):
    """A spirit hit of at least DamageThreshold cuts a random ability cooldown by CooldownReductionPerHit
    (internal cooldown AbilityCooldown)."""

    def on_damage_taken(self, f, src, hit):
        if hit.kind != "spirit" or hit.amount < self.item.p("DamageThreshold", 75) or not self.ready():
            return
        cooling = [ab for ab in f.abilities if ab.ready_at > self.now]
        if not cooling:
            return
        self.use()
        rng = f.e.rng
        ab = rng.choice(cooling) if rng is not None else max(cooling, key=lambda a: a.ready_at)
        _cut_cooldown(ab, self.now, self.item.p("CooldownReductionPerHit", 4))


@handler("upgrade_unstoppable")
class Unstoppable(FX):
    """Active: CC immunity for AbilityDuration (modeled as 100% status resist, which also shortens slows and
    heal reduction applied meanwhile) and cleanses current silence / disarm / immobilize. Used when the enemy
    casts a crowd-control ability, or when already silenced or disarmed. Not usable while stunned."""

    def _go(self, f):
        self.use()
        dur = self.dur("AbilityDuration", 5.5)
        self.buff("status_resist", 1.0, dur)
        for k in CC_KEYS:
            if k != "stun":
                f.mods.d.pop(k, None)

    def _usable(self, f):
        return self.ready() and f.skill.use_actives and f.alive and not f.mods.active("stun")

    def on_enemy_cast(self, f, ab_state):
        if self._usable(f) and any(k in ab_state.ab.props and "Self" not in k for k in CC_PROPS):
            self._go(f)

    def try_active(self, f):
        if self._usable(f) and (f.mods.active("silence") or f.mods.active("disarm") or f.mods.active("immobilize")):
            self._go(f)
            return True
        return False


@handler("upgrade_eldritch_shot")
class HauntingShot(FX):
    """Next bullet hit: HealthPctDamage% of current health as spirit damage, and for DebuffDuration the target
    deals OutgoingDamagePenaltyPercent less damage and receives HealAmpReceivePenaltyPercent less healing."""

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "bullet" or not hit.hits or hit.is_item or not self.ready():
            return
        self.use()
        d = self.dur("DebuffDuration", 4)
        self.spirit(t, t.hp * self.item.p("HealthPctDamage") / 100, procs=False)
        self.debuff(t, "outgoing_penalty", abs(self.item.p("OutgoingDamagePenaltyPercent")) / 100, d)
        self.debuff(t, "heal_received", -abs(self.item.p("HealAmpReceivePenaltyPercent")) / 100, d)


@handler("upgrade_runed_gauntlets")
class RunedGauntlets(FX):
    """Landed heavy melee off cooldown: every ability on cooldown loses CooldownReductionOnHitPct% of its remaining
    time, at least CooldownReductionOnHitMin seconds."""

    def on_damage_dealt(self, f, t, hit):
        if not _basic_melee(hit) or not f.counters.get("melee_heavy") or not _melee_proc(self, f):
            return
        self.use()
        now = self.now
        for ab in f.abilities:
            left = ab.ready_at - now
            if left > 0:
                _cut_cooldown(ab, now, max(self.item.p("CooldownReductionOnHitMin", 4),
                                           left * self.item.p("CooldownReductionOnHitPct", 16) / 100))


@handler("upgrade_medic_bullets")
class RestorativeShot(FX):
    """Bullet hit on a hero off cooldown heals HealFromHero."""

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "bullet" or not hit.hits or not self.ready():
            return
        self.use()
        f.heal(self.v("HealFromHero"), self.name, "item")


@handler("upgrade_chonky")
class Fortitude(FX):
    """After RestoreDelay s without taking damage, regenerate HealLifePercentOutOfCombat% of max health per second.
    Fights start with the fighter rested (regen on until the first hit)."""

    def on_start(self, f):
        self.last_hit = -1e9
        f.e.after(0.5, self.tick)

    def on_damage_taken(self, f, src, hit):
        if hit.amount > 0:
            self.last_hit = self.now

    def tick(self):
        f = self.f
        if not f.alive or f.e.over:
            return
        if self.now - self.last_hit >= self.item.p("RestoreDelay", 10) and f.hp < f.max_hp:
            f.heal(f.max_hp * self.item.p("HealLifePercentOutOfCombat") / 100 * 0.5, self.name, "regen")
        f.e.after(0.5, self.tick)
