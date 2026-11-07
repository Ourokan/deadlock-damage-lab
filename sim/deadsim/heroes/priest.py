"""Venator (hero_priest).

Assumptions:
- Weapon-damage abilities (EBaseWeaponDamageIncrease scaling, applied by c.val) are bullet damage (bullet
  resist, procs).
- Consecrating Grenade: skillshot (throw reach GRENADE_RANGE) dealing Damage, then a burn on the target for
  BurnDuration dealing DPS as pure damage (the description's "pure damage to enemies in the area" is read as
  the burn hurting the burning hero; doubtful) and HealAmpReceivePenaltyPercent healing reduction.
- Gutshot: cone blast (AbilityCastRange) for Damage, hits its target. A wall is close behind the target
  WALL_CHANCE of the time: BonusDamage and StunDuration stun. Knockback is movement. T3 blessed heavy melee is
  not modeled (no melee in the default rotation).
- Hex-Lined Snap Trap: kicked under the target, which trips it SNAP_TRAP_TRIGGER after the cast (scaled by
  spirit accuracy): Damage spirit damage; immobilize is movement-only. T3: +IncomingDamagePercentFromCaster
  damage-taken amp for RevealDuration.
- Ira Domini: replaces the gun with StakeCount crossbow stakes fired STAKE_INTERVAL apart; each lands with the
  caster's spirit (skillshot) accuracy since they are single aimed shots, no headshots. Each stake: Damage (weapon
  scaled) bullet damage that procs like a gun bullet. The game books stakes under their own weapon
  (citadel_weapon_priest_crossbow, not the gun citadel_weapon_priest_set), so they are "Ira Domini (stakes)" with a
  landing factor of their own: replays land 1.6 stakes on heroes per cast (of 3) for 1.4 blessed hits, and booked as
  gun they hid a plain gun share of 0.16 vs real 0.38 behind stakes at 0.27-0.33 of damage vs real 0.10. The final stake (all of them at T3) is blessed: +BonusDamage pure damage and executes a target left below ExecuteThreshold % health. Cast once the target is below
  ULT_CAST_HP so the execute matters.
  Booking (BOOK_UNBLESSED, 2026-11-07): the game books an unblessed stake under the ult's own class
  (ability_priest_weaponswap) and only a blessed one under the crossbow. In post-hotfix replays a cast before T3 has
  ~1.4 stake hits with only an Ira Domini event (~0.6 with crossbow + blessed); at T3 0.03. The sim booked every stake
  as crossbow, so early stakes read 1.5x over and early Ira 1.7x under, and the whole-match fit split the two wrongly.
  Unblessed stakes are now booked as "Ira Domini" with the stakes' own landing factor (Engine.damage book_only).
  The 10-30 hotfix (Bonus Damage 115 -> 95, per boon 3.0 -> 3.6) left real blessed hits as big as before.
"""
from deadsim.abilities import AbilityImpl, register

GRENADE_RANGE = 25.0      # m, grenade throw reach (no range in data)
WALL_CHANCE = 0.5         # share of Gutshots that wall-stun (no walls in the model)
SNAP_TRAP_TRIGGER = 1.0   # s from kick to the target stepping on the armed trap
STAKE_INTERVAL = 0.8      # s between crossbow stakes (not in data)
ULT_CAST_HP = 0.7
STAKES_AS_ULT = True      # stakes booked under Ira Domini (with its landing), not gun
BOOK_UNBLESSED = True     # an unblessed stake (before T3) is booked under the ult's own class, as the game does


@register("ability_priest_flashbang")
class ConsecratingGrenade(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(GRENADE_RANGE)

    def cast(self, c):
        delay = c.raw("AbilityCastDelay") + 0.5   # bounce before exploding
        c.lock_gun(c.raw("AbilityCastDelay") + c.raw("AbilityPostCastDuration"))
        acc = c.me.skill.spirit_accuracy
        c.bullet_hit(c.val("Damage") * acc, delay=delay)
        d = c.dur("BurnDuration")
        c.dot(c.val("DPS"), d, delay=delay, tick=c.raw("TickRate", 0.2), kind="pure", hit_chance=acc)
        c.debuff("heal_received", c.raw("HealAmpReceivePenaltyPercent") / 100 * acc, d, delay=delay)


@register("ability_priest_knockback")
class Gutshot(AbilityImpl):
    kind = "aoe"

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        dmg = c.val("Damage")
        wall = c.me.acc("gutshot_wall").take(WALL_CHANCE, 1) > 0
        if wall:
            dmg += c.val("BonusDamage")
            c.debuff("stun", 1, c.raw("StunDuration"), delay=delay)
        c.bullet_hit(dmg, delay=delay)


@register("ability_priest_beartrap")
class SnapTrap(AbilityImpl):
    kind = "skillshot"

    def in_range(self, c):
        return c.reach(15.0 + c.me.skill.engage_margin)   # kick reach ~15 m

    def cast(self, c):
        c.lock_gun(c.raw("AbilityCastDelay"))
        t = c.raw("AbilityCastDelay") + max(c.raw("ArmTime"), SNAP_TRAP_TRIGGER)
        c.spirit_hit(c.val("Damage"), delay=t)
        if c.raw("IncomingDamagePercentFromCaster"):
            c.debuff("damage_taken_amp", c.raw("IncomingDamagePercentFromCaster") / 100 * c.me.skill.spirit_accuracy,
                     c.dur("RevealDuration"), delay=t)


@register("ability_priest_weaponswap")
class IraDomini(AbilityImpl):
    kind = "self"

    def should_cast(self, c):
        return c.foe.hp_frac <= ULT_CAST_HP

    def cast(self, c):
        delay = c.raw("AbilityCastDelay")
        n = int(c.raw("StakeCount", 3))
        c.lock_gun(delay + n * STAKE_INTERVAL + c.raw("SwapEndDelay"))
        for i in range(n):
            blessed = i == n - 1 or bool(c.raw("AllStakesBlessed"))
            c.after(delay + i * STAKE_INTERVAL, self.stake, c, blessed)

    def stake(self, c, blessed):
        f, e = c.me, c.foe
        if not (f.alive and e.alive):
            return
        p = f.skill.spirit_accuracy   # single aimed stakes land like skillshots, not like spray
        # stakes are crossbow (weapon) bullets that proc like gun bullets; the game books them under their own weapon
        # (citadel_weapon_priest_crossbow), which the audit counts as Ira Domini, so they take the ult's landing
        if STAKES_AS_ULT:
            # the game books an unblessed stake under ability_priest_weaponswap and a blessed one under the crossbow
            # (replays: before T3 ~1.4 stake hits a cast carry only an Ira Domini event, the final stake both)
            book = self.s.ab.name if BOOK_UNBLESSED and not blessed else None
            c.engine.damage(f, e, c.val("Damage") * p, "bullet", self.s.ab.name + " (stakes)", is_ability=True,
                            ability=self.s, hits=1, is_ult=True, weapon_proc=True, book=book, book_only=True)
        else:
            c.engine.damage(f, e, c.val("Damage") * p, "bullet", "gun", ability=self.s, hits=1, is_ult=True)
        if blessed and e.alive:
            c.engine.damage(f, e, c.val("BonusDamage") * p, "pure", self.s.ab.name + " (blessed)", is_ability=True,
                            ability=self.s, is_ult=True)
            if p >= 0.5 and e.alive and e.hp_frac * 100 < c.raw("ExecuteThreshold"):
                c.engine.damage(f, e, e.hp + e.barrier_total() + 1.0, "pure", self.s.ab.name + " (execute)",
                                is_ability=True, ability=self.s, is_ult=True, ignore_resist=True)
