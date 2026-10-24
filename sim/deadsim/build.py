"""A hero + items + souls -> the hero's static combat stats.

Formulas (checked against 38k real stat snapshots from 400 ranked matches, see validation/README.md):
- Level comes from (net worth - 600) via the hero's level table; boons = level - 1.
- Max health = (base + boons * health_per_boon) * (1 + vitality invest bonus% + base health% items)
               + flat item health, then * (1 + max health% items, e.g. Glass Cannon).
- Spirit power = boons * spirit_per_boon + spirit invest bonus (flat) + item spirit, then * (1 + spirit%).
- Weapon damage % = weapon invest bonus% + sum of item weapon damage% (additive).
- Invest bonus thresholds use the summed cost of owned items in that slot.
Only "innate" item stats (always on) are summed here; conditional, proc and active effects live in items_fx.py.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from .data import game, gun_calibration, Hero, Item, UNITS_PER_METER


def gun_quirks(hero_id):
    """(charge_factor, tether_range_m) from data/gun_calibration.json (replay fit, scripts/gun_calib), or (1, None).
    Deadman Danny's charged shot lands charge_factor x the base bullet damage of an ordinary hit and fires about
    that much less often; Graves' tether gun only fires within tether_range_m."""
    row = gun_calibration().get(str(hero_id)) or {}
    return row.get("charge_factor") or 1.0, row.get("tether_range_m")

# passive-section stats that are unconditional in practice (the tooltip lists them under "passive")
ALWAYS_ON_PASSIVE = {
    "upgrade_cooldown_reduction": ["CooldownReduction"],
    "upgrade_transcendent_cooldown": ["CooldownReduction", "ItemCooldownReduction"],
    "upgrade_imbued_duration_extender": ["BonusAbilityDurationPercent"],
    "upgrade_tech_range": ["TechRangeMultiplier"],
    "upgrade_debuff_reducer": ["StatusResistancePercent"],
    "upgrade_healing_booster": ["HealAmpCastPercent", "HealAmpRegenPercent"],
    "upgrade_absorbing_armor": ["CooldownReduction"],  # Witchmail
}
# stats that only apply to one imbued ability (handled by the ability layer, not summed globally)
IMBUE_ITEMS = {
    "upgrade_magic_reach": {"range": "TechRangeMultiplier"},
    "upgrade_magic_tempo": {"cdr": "CooldownReduction"},
    "upgrade_arcane_extension": {"duration": "BonusAbilityDurationPercent"},
    "upgrade_magic_storm": {"spirit": "ImbuedTechPower"},
    "upgrade_quick_silver": {},
    "upgrade_ethereal_bullets": {},
    "upgrade_mystic_reverb": {},
    "upgrade_bulletshredimbue": {"range": "TechRangeMultiplier"},
    "upgrade_ability_power_shard": {},
    "upgrade_frostbite_charm": {},
}


def combine_resist(sources, reductions=()):
    """Deadlock resist stacking: positives stack multiplicatively, reductions stack multiplicatively
    among themselves and are then subtracted (deadlock.wiki/Damage_Resistance). Values are fractions."""
    keep = 1.0
    for r in sources:
        keep *= (1.0 - r)
    red_keep = 1.0
    for r in reductions:
        red_keep *= (1.0 - abs(r))
    return (1.0 - keep) - (1.0 - red_keep)


def stack_cdr(values):
    """Cooldown reductions stack multiplicatively (assumption; matches in-game tooltip totals we've seen)."""
    keep = 1.0
    for v in values:
        keep *= (1.0 - v)
    return 1.0 - keep


def invest_bonus(hero: Hero, slot: str, spent: float) -> float:
    b = 0.0
    for th, v in hero.invest.get(slot, []):
        if spent >= th:
            b = v
    return b


@dataclass
class Stats:
    hero: Hero
    items: list
    souls: float
    level: int
    boons: int
    # vitality
    max_health: float = 0.0
    health_regen: float = 0.0
    ooc_regen: float = 0.0        # out-of-combat health regen per s (only between lane trades, game_path)
    bullet_resist: list = field(default_factory=list)   # fractions
    spirit_resist: list = field(default_factory=list)
    melee_resist: list = field(default_factory=list)
    status_resist: float = 0.0
    crit_received_scale: float = 1.0
    heal_amp: float = 0.0          # incoming regen/heal amp from own items
    heal_amp_cast: float = 0.0     # outgoing healing amp: own ability heals, lifesteal, item heals
    # spirit
    spirit_power: float = 0.0
    cdr: float = 0.0               # global ability cooldown reduction (fraction)
    item_cdr: float = 0.0
    ult_cdr: float = 0.0
    duration_pct: float = 0.0
    range_pct: float = 0.0
    bonus_charges: int = 0
    charged_spirit: float = 0.0    # Extra Charge / Rapid Recharge spirit for charged abilities
    charged_cdr: float = 0.0
    charge_delay_red: float = 0.0
    spirit_lifesteal: float = 0.0
    spirit_shred: list = field(default_factory=list)      # always-on enemy spirit resist reduction (fractions)
    # weapon
    weapon_pct: float = 0.0        # additive weapon damage bonus (fraction)
    fire_rate_pct: float = 0.0
    bullet_damage: float = 0.0     # per bullet, before % bonuses
    pellets: int = 1
    cycle_time: float = 1.0
    burst_count: int = 1
    burst_interval: float = 0.0
    spin_cycle: float | None = None   # fully spun-up cycle time (None = no spin-up)
    spin_up_rate: float = 0.5         # spin fraction gained per second of firing
    spin_decay_rate: float = 0.25     # spin fraction lost per second not firing
    clip: int = 1
    gun_range_m: float | None = None   # beyond it the gun deals nothing (Graves' tether)
    reload_time: float = 1.0
    reload_mult: float = 1.0
    bullet_lifesteal: float = 0.0
    bullet_shred: list = field(default_factory=list)
    melee_pct: float = 0.0
    outgoing_mult: float = 1.0     # all-damage multiplier (Golden Goose Egg)
    extra: dict = field(default_factory=dict)

    @property
    def weapon(self):
        return self.hero.weapon

    def falloff(self, meters: float) -> float:
        if self.gun_range_m is not None and meters > self.gun_range_m:
            return 0.0
        w = self.hero.weapon
        d = meters * UNITS_PER_METER
        s, e = w.get("damage_falloff_start_range", 0), w.get("damage_falloff_end_range", 0)
        lo = w.get("damage_falloff_start_scale", 1.0)
        hi = w.get("damage_falloff_end_scale", 1.0)
        if e <= s or d <= s:
            return lo
        if d >= e:
            return hi
        x = (d - s) / (e - s)
        b = w.get("damage_falloff_bias", 0.5) or 0.5
        if b != 0.5:  # Valve Bias(): x ^ (log(b) / log(0.5))
            import math
            x = x ** (math.log(b) / math.log(0.5))
        return lo + (hi - lo) * x

    def crit_mult(self, meters: float) -> float:
        w = self.hero.weapon
        d = meters * UNITS_PER_METER
        s, e = w.get("crit_bonus_start_range", 0), w.get("crit_bonus_end_range", 0)
        a, b = w.get("crit_bonus_start", 1.0), w.get("crit_bonus_end", 1.0)
        if e <= s or d <= s:
            return a
        if d >= e:
            return b
        return a + (b - a) * (d - s) / (e - s)

    def shot_interval(self, extra_fire_rate=0.0) -> float:
        """Seconds between trigger pulls (a burst counts as one pull). Burst guns: cycle_time + burst_count x
        intra-burst time per pull, which matches the weapon data's bullets_per_second."""
        base = self.cycle_time + (self.burst_count * self.burst_interval if self.burst_count > 1 else 0.0)
        return base / max(0.05, 1.0 + self.fire_rate_pct + extra_fire_rate)

    def bullet_resist_total(self, reductions=()):
        return combine_resist(self.bullet_resist, reductions)

    def spirit_resist_total(self, reductions=()):
        return combine_resist(self.spirit_resist, reductions)


# Net worth runs 600 souls ahead of the souls that count toward level (fits 97% of 32k in-game snapshots,
# where true level = ability points + 4 and boons = level - 1).
NET_WORTH_OFFSET = 600


def compute_stats(hero, items=(), souls=None, level=None) -> Stats:
    G = game()
    hero = G.hero(hero)
    items = [G.item(i) for i in items]
    if souls is None:
        souls = sum(i.cost for i in items)
    if level is None:
        level = G.level_for_souls(hero, max(0.0, souls - NET_WORTH_OFFSET))
    boons = max(0, level - 1)   # every level after 1 is a standard level-up (one boon)
    pb = hero.per_boon
    st = Stats(hero=hero, items=items, souls=souls, level=level, boons=boons)

    spent = {"weapon": 0, "vitality": 0, "spirit": 0}
    for it in items:
        spent[it.slot] = spent.get(it.slot, 0) + it.cost

    agg = {}
    lists = {"bullet_res": [], "spirit_res": [], "melee_res": [], "cdr": [], "spirit_shred": [], "bullet_shred": []}

    def add(stat, k, v):
        if stat in ("MODIFIER_VALUE_BULLET_ARMOR_DAMAGE_RESIST",):
            lists["bullet_res"].append(v / 100)
        elif stat == "MODIFIER_VALUE_TECH_RESIST":
            lists["spirit_res"].append(v / 100)
        elif stat == "MODIFIER_VALUE_MELEE_RESIST":
            lists["melee_res"].append(v / 100)
        elif stat == "MODIFIER_VALUE_COOLDOWN_REDUCTION_PERCENTAGE":
            if "Charged" in k:
                agg["charged_cdr"] = agg.get("charged_cdr", 0) + v
            else:
                lists["cdr"].append(v / 100)
        elif stat == "MODIFIER_VALUE_TECH_RESIST_REDUCTION":
            lists["spirit_shred"].append(abs(v) / 100)
        elif stat == "MODIFIER_VALUE_BULLET_AND_MELEE_RESIST_REDUCTION":
            lists["bullet_shred"].append(abs(v) / 100)
        elif stat == "MODIFIER_VALUE_TECH_POWER" and "Charged" in k:
            agg["charged_spirit"] = agg.get("charged_spirit", 0) + v
        else:
            agg[stat] = agg.get(stat, 0) + v

    for it in items:
        for k, v in it.innate.items():
            add(it.stat_type[k], k, v)
        for k in ALWAYS_ON_PASSIVE.get(it.class_name, []):
            v = it.props.get(k)
            if v and k in it.stat_type:
                add(it.stat_type[k], k, v)

    A = lambda key: agg.get("MODIFIER_VALUE_" + key, 0.0)

    # vitality
    base_hp = hero.base["max_health"] + boons * pb.get("MODIFIER_VALUE_BASE_HEALTH_FROM_LEVEL", 0)
    vit = invest_bonus(hero, "vitality", spent["vitality"]) / 100
    st.max_health = (base_hp * (1 + vit + A("BASE_HEALTH_PERCENT") / 100) + A("HEALTH_MAX")) * (1 + A("HEALTH_MAX_PERCENT") / 100)
    st.health_regen = hero.base.get("base_health_regen", 0) + A("HEALTH_REGEN_PER_SECOND")
    st.ooc_regen = (hero.base.get("ooc_health_regen", 0) or 0) \
        + boons * pb.get("MODIFIER_VALUE_OUT_OF_COMBAT_HEALTH_REGEN", 0) + A("OUT_OF_COMBAT_HEALTH_REGEN")
    base_br = pb.get("MODIFIER_VALUE_BULLET_ARMOR_DAMAGE_RESIST", 0) * boons
    base_sr = hero.base.get("tech_armor_damage_reduction", 0) or 0
    base_sr += pb.get("MODIFIER_VALUE_TECH_RESIST", 0) * boons
    st.bullet_resist = ([base_br / 100] if base_br else []) + lists["bullet_res"]
    st.spirit_resist = ([base_sr / 100] if base_sr else []) + lists["spirit_res"]
    st.melee_resist = lists["melee_res"]
    st.status_resist = A("STATUS_RESISTANCE") / 100
    st.crit_received_scale = hero.base.get("crit_damage_received_scale", 1.0)
    st.heal_amp = A("HEAL_AMP_REGEN_PERCENT") / 100
    st.heal_amp_cast = A("HEAL_AMP_CAST_PERCENT") / 100

    # spirit
    sp = boons * pb.get("MODIFIER_VALUE_TECH_POWER", 0) + invest_bonus(hero, "spirit", spent["spirit"]) + A("TECH_POWER")
    st.spirit_power = sp * (1 + A("TECH_POWER_PERCENT") / 100)
    st.cdr = stack_cdr(lists["cdr"])
    st.item_cdr = A("ITEM_COOLDOWN_REDUCTION_PERCENTAGE") / 100
    st.ult_cdr = A("ULTIMATE_COOLDOWN_REDUCTION_PERCENTAGE") / 100
    st.duration_pct = A("BONUS_ABILITY_DURATION_PERCENTAGE") / 100
    st.range_pct = A("TECH_RANGE_PERCENT") / 100
    st.bonus_charges = int(A("BONUS_ABILITY_CHARGES"))
    st.charged_spirit = agg.get("charged_spirit", 0.0)
    st.charged_cdr = agg.get("charged_cdr", 0.0) / 100
    st.charge_delay_red = A("COOLDOWN_BETWEEN_CHARGE_REDUCTION_PERCENTAGE") / 100
    st.spirit_lifesteal = A("TECH_LIFESTEAL") / 100
    st.spirit_shred = lists["spirit_shred"]

    # weapon
    w = hero.weapon
    st.weapon_pct = (invest_bonus(hero, "weapon", spent["weapon"]) + A("WEAPON_DAMAGE_INCREASE")) / 100
    st.fire_rate_pct = A("FIRE_RATE") / 100
    st.bullet_damage = w.get("bullet_damage", 0) + boons * pb.get("MODIFIER_VALUE_BASE_BULLET_DAMAGE_FROM_LEVEL", 0)
    st.pellets = int(w.get("bullets", 1) or 1)
    st.cycle_time = w.get("cycle_time", 1.0)
    charge, st.gun_range_m = gun_quirks(hero.id)
    st.bullet_damage *= charge   # same damage per second as the data's gun, in fewer, bigger (charged) shots
    st.cycle_time *= charge
    st.burst_count = int(w.get("burst_shot_count", 1) or 1)
    st.burst_interval = w.get("intra_burst_cycle_time", 0.0) or 0.0
    # spin-up guns (McGinnis, Victor): cycle time falls toward max_spin_cycle_time while firing
    st.spin_cycle = w.get("max_spin_cycle_time") if w.get("spins_up") else None
    st.spin_up_rate = w.get("spin_increase_rate", 0.5) or 0.5
    st.spin_decay_rate = w.get("spin_decay_rate", 0.25) or 0.25
    st.clip = max(1, int(round(w.get("clip_size", 1) * (1 + A("AMMO_CLIP_SIZE_PERCENT") / 100) + A("AMMO_CLIP_SIZE"))))
    # a charged shot spends charge_factor rounds (Danny's replays: about 6 shots between reloads of a 14 clip), so
    # reload downtime per second of fire stays the data gun's
    st.clip = max(1, int(round(st.clip / charge)))
    st.reload_mult = 1.0 + A("RELOAD_SPEED") / 100
    st.reload_time = w.get("reload_duration", 1.0) * st.reload_mult
    st.bullet_lifesteal = A("BULLET_LIFESTEAL") / 100
    st.bullet_shred = lists["bullet_shred"]
    st.melee_pct = A("MELEE_DAMAGE_INCREASE") / 100
    st.outgoing_mult = 1 + A("ALL_DAMAGE_MULTIPLIER") / 100
    st.extra = {k: v for k, v in agg.items() if k.startswith("MODIFIER_VALUE_") and not k.endswith(("HEALTH_MAX",))}
    return st
