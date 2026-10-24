"""Graves (hero_necro).

Assumptions:
- Jar of Dead: charges come from collected deaths (ResourceCost per jar), which a 1v1 doesn't produce, so
  Graves starts with JARS_AT_START stored jars and gains none. Throws are AbilityCooldownBetweenCharge apart,
  reach JAR_RANGE. Each Deadhead hits once per SKULL_INTERVAL (DelayBeforeRespawning + mean target-search delay)
  for SkullLifetime. With deadsim.mechanics summons on, each Deadhead has SummonHealth (+ boons) and the enemy
  can shoot it down (targeting fitted to replays, data/summon_targeting.json).
- Grasping Hands: the wall is placed on the target: one Damage hit (skillshot) + immobilize after
  ZombieWallDeployTime. Each Ghoul (SummonCount) melees for the Borrowed Decree SummonMeleeDamage (base values
  from the ult's data if the ult isn't known) every GHOUL_INTERVAL s for AbilityDuration x GHOUL_UPTIME. With
  summons on each Ghoul has the zombie SummonHealth and can be killed.
- Essence Theft: progress builds with time spent hitting the target (ShootDurationForMax s to max) and drains at
  ProgressLossPerSecond x ProgressLossMultiplier after DelayBeforeLoss without a hit. At progress p Graves gains
  p x MaxStolenAttackDamage % weapon damage and p x MaxStolenSpiritResist % spirit resist; the target loses the
  same. T3: Deadhead hits add SkullBuildUp s of progress, Ghoul hits ZombieMeleeBuildUp s.
- Borrowed Decree: gravestone lands on the target (Damage, always hits). Zombies spawn every SummonFrequency
  (SummonBurstCount each) for AbilityDuration and attack every GHOUL_INTERVAL s; at most ZOMBIE_CAP attack at
  once. Without summons a zombie lives ZOMBIE_LIFE s (a stand-in for being killed). With summons on it has
  SummonHealth (+ boons) and lives until the enemy kills it, SummonLifetime ends or the zombie row's life_other_s
  in data/summon_targeting.json (median life of real zombies no hero killed: troopers, other heroes), and the gravestone has GravestoneHealth: once it is
  destroyed (by splash, or by the enemy's break: an expected value that scales later spawns and the aura) no
  more zombies spawn and the aura ends (bullets don't damage it in the replays: only area damage
  splashing off Graves breaks it) (replays: zombie spawns drop from 0.46/s to 0.14/s once a
  gravestone is gone). The aura stacks TechArmorDamageReductionPerStack every StackingDebuffTickRate up to
  MaxStacks while the ult lasts (target assumed inside). T3: each zombie death deals CurrentHealthDamagePercentage %
  of current health. Summon melee is spirit damage.
- Summon damage is booked under the summoning ability ("Grasping Hands (ghoul)", "Borrowed Decree (zombie)").
"""
from deadsim.abilities import AbilityImpl, register
from deadsim.mechanics import add_summon, alive

JARS_AT_START = 2
JAR_RANGE = 25.0
GHOUL_INTERVAL = 1.5
GHOUL_UPTIME = 0.6
ZOMBIE_LIFE = 4.5
ZOMBIE_CAP = 2
SUMMON_MELEE_FALLBACK = (40.0, 0.5)   # Borrowed Decree SummonMeleeDamage base / spirit scaling
SUMMON_HEALTH_FALLBACK = (180.0, 8.0)  # Borrowed Decree SummonHealth base / per boon


def find(c, class_name):
    for ab in c.me.abilities:
        if ab.ab.class_name == class_name:
            return ab
    return None


def summon_melee(c):
    ult = find(c, "ability_necro_gravestone")
    if ult is not None:
        return ult.ctx.val("SummonMeleeDamage")
    return SUMMON_MELEE_FALLBACK[0] + SUMMON_MELEE_FALLBACK[1] * c.sp


def theft_feed(c, prop):
    et = find(c, "ability_necro_fear")
    if et is not None and et.unlocked and et.tier >= 3:
        et.impl.feed(et.ctx, et.ctx.raw(prop))


def summon_health(c):
    ult = find(c, "ability_necro_gravestone")
    if ult is not None:
        return ult.ctx.val("SummonHealth")
    return SUMMON_HEALTH_FALLBACK[0] + SUMMON_HEALTH_FALLBACK[1] * c.me.st.boons


def summon_hit(c, amount, name, buildup_prop, guard=None):
    if c.me.alive and c.foe.alive and alive(guard):
        c.spirit_hit(amount, name=name, hit_chance=1.0)
        theft_feed(c, buildup_prop)


@register("ability_necro_hauntingskull")
class JarOfDead(AbilityImpl):
    kind = "skillshot"

    def start(self, c):
        c.state["jars"] = JARS_AT_START

    def should_cast(self, c):
        return c.state.get("jars", 0) > 0 and c.reach(JAR_RANGE)

    def cast(self, c):
        c.state["jars"] -= 1
        delay = c.raw("AbilityCastDelay")
        c.lock_gun(delay)
        if not c.me.acc("jar_hit").take(c.me.skill.spirit_accuracy):
            return
        life = c.val("SkullLifetime")
        every = c.raw("DelayBeforeRespawning", 1.0) + (c.raw("TargetSearchDelayMin") + c.raw("TargetSearchDelayMax")) / 2
        dmg = c.val("Damage")
        for k in range(int(c.raw("SkullCount"))):
            s = add_summon(c.me, "Deadhead", c.val("SummonHealth"), life=life, delay=delay, kind="graves_skull")
            t = delay + c.raw("TargetSearchInitialDelayMin") + k * c.raw("TargetSearchInitialStagger")
            while t < delay + life:
                c.after(t, summon_hit, c, dmg, self.s.ab.name, "SkullBuildUp", s)
                t += every


@register("ability_necro_zombiewall")
class GraspingHands(AbilityImpl):
    kind = "skillshot"

    def cast(self, c):
        delay = c.raw("ZombieWallDeployTime", 0.6)
        c.spirit_hit(c.val("Damage"), delay=delay)
        c.debuff("immobilize", 1, c.dur("ImmobilizeDuration") * c.me.skill.spirit_accuracy, delay=delay)
        dmg = summon_melee(c)
        life = c.dur("AbilityDuration") * GHOUL_UPTIME
        for g in range(int(c.raw("SummonCount", 1))):
            s = add_summon(c.me, "Ghoul", summon_health(c), life=life, delay=delay, kind="graves_zombie")
            t = delay + 0.5 + 0.2 * g
            while t < delay + life:
                c.after(t, summon_hit, c, dmg, self.s.ab.name + " (ghoul)", "ZombieMeleeBuildUp", s)
                t += GHOUL_INTERVAL


@register("ability_necro_fear")
class EssenceTheft(AbilityImpl):
    kind = "passive"

    def start(self, c):
        c.state.update(prog=0.0, last=-99.0)
        c.me.stat_hooks.append(lambda f: self.mods(c, +1))
        c.foe.stat_hooks.append(lambda f: self.mods(c, -1))

    def progress(self, c):
        st = c.state
        idle = c.now - st["last"] - c.raw("DelayBeforeLoss", 0.5)
        p = st["prog"]
        if idle > 0:
            p -= idle * c.raw("ProgressLossPerSecond", 1) * c.raw("ProgressLossMultiplier", 1)
        return max(0.0, p)

    def feed(self, c, seconds):
        st = c.state
        st["prog"] = min(c.raw("ShootDurationForMax", 4), self.progress(c) + seconds)
        st["last"] = c.now

    def mods(self, c, sign):
        if not c.foe or not c.foe.alive:
            return {}
        frac = self.progress(c) / max(0.1, c.raw("ShootDurationForMax", 4))
        if frac <= 0:
            return {}
        # spirit power without dynamic hooks (calling c.val here would recurse through stat hooks)
        sp = c.me.st.spirit_power + c.me.mods.sum("spirit_power")
        steal = c.raw("MaxStolenAttackDamage") + c.scale("MaxStolenAttackDamage") * sp
        return {"weapon_pct": sign * frac * steal / 100,
                "spirit_resist": sign * frac * c.raw("MaxStolenSpiritResist") / 100}

    def on_damage_dealt(self, c, target, hit):
        if hit.kind != "bullet" or not hit.hits or hit.is_ability:
            return
        gap = c.now - c.state["last"]
        self.feed(c, min(gap, 0.5))


@register("ability_necro_gravestone")
class BorrowedDecree(AbilityImpl):
    kind = "target"

    def cast(self, c):
        ch = c.raw("AbilityChannelTime", 0.66)
        c.lock_gun(ch)
        c.spirit_hit(c.val("Damage"), delay=ch + c.raw("GrowTime"))
        dur = c.val("AbilityDuration")
        c.state["alive"] = []          # attacking zombies: (expiry time, summon or None)
        stone = add_summon(c.me, "Gravestone", c.raw("GravestoneHealth"), bullet_resist=1.0, life=dur,
                           delay=ch + c.raw("GrowTime"), kind="graves_stone")   # replays: bullets never damage it
        c.state["stone"] = stone
        # aura stacks: spirit resist reduction
        n_ticks = int(dur / c.raw("StackingDebuffTickRate", 0.25))
        per = abs(c.raw("TechArmorDamageReductionPerStack")) / 100
        for i in range(1, n_ticks + 1):
            stacks = min(c.raw("MaxStacks", 40), i)
            c.after(ch + i * c.raw("StackingDebuffTickRate", 0.25),
                    lambda s=stacks: alive(stone) and c.debuff("spirit_shred", s * per * (stone.weight if stone else 1),
                                                               c.raw("StackingDebuffTickRate", 0.25) + 0.05,
                                                               tag="decree_stacks"))
        t = ch + c.raw("SummonInitialDelay", 0.3)
        freq = c.raw("SummonFrequency", 4)
        while t < ch + dur:
            for b in range(int(c.raw("SummonBurstCount", 1))):
                c.after(t + b * c.raw("SummonBurstFrequency", 0.1), self.spawn, c)
            t += freq

    def spawn(self, c):
        stone = c.state.get("stone")
        if not c.me.alive or not c.foe.alive or not alive(stone):
            return
        if stone is not None and stone.weight < 1 and not c.me.acc("decree_spawn").take(stone.weight):
            return   # the gravestone is broken in this share of fights (mechanics._break)
        now = c.now
        live = [x for x in c.state["alive"] if x[0] > now and alive(x[1])]
        c.state["alive"] = live
        if len(live) >= ZOMBIE_CAP:
            return
        name = self.s.ab.name + " (zombie)"
        pct = c.raw("CurrentHealthDamagePercentage") / 100 if c.tier >= 3 else 0.0
        state = {"done": False}

        def death():   # T3: a zombie's death (killed or expired) hits the target once
            if pct and not state["done"]:
                state["done"] = True
                if c.me.alive and c.foe.alive:
                    c.spirit_hit(c.foe.hp * pct, name=name, hit_chance=1.0)
        spawn_t = c.raw("SpawnDuration", 1.5)
        s = add_summon(c.me, "Zombie", c.val("SummonHealth"), life=c.dur("SummonLifetime"), kind="graves_zombie",
                       on_death=death)
        life = ZOMBIE_LIFE if s is None else s.until - now
        live.append((now + life, s))
        dmg = c.val("SummonMeleeDamage")
        t = spawn_t
        while t < life:
            c.after(t, summon_hit, c, dmg, name, "ZombieMeleeBuildUp", s)
            t += GHOUL_INTERVAL
        if pct:
            c.after(life, death)
