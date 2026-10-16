"""Game data access: heroes, guns, abilities, shop items, with indexes the model needs.

Everything is loaded once (lru_cache) from /mnt/project-files/data/game (override with DEADSIM_DATA).
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from functools import lru_cache

DATA_DIR = os.environ.get("DEADSIM_DATA", os.path.join(os.path.dirname(__file__), "..", "..", "data"))
GAME = os.path.join(DATA_DIR, "game")

UNITS_PER_METER = 39.37  # game units ("inches") per meter; falloff ranges are stored in units


def _load(name):
    with open(os.path.join(GAME, name)) as f:
        return json.load(f)


def _num(v):
    """Property values come as numbers, numeric strings or strings like '8m'. Returns float or None."""
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().rstrip("m").rstrip("%")
    try:
        return float(s)
    except ValueError:
        return None


@dataclass
class Item:
    id: int
    name: str
    class_name: str
    slot: str          # weapon | vitality | spirit
    tier: int
    cost: int
    activation: str    # passive | instant_cast | press | instant_cast_toggle
    components: list
    props: dict        # property name -> float value
    innate: dict       # unconditional stats: property name -> float (only those with a provided stat type)
    stat_type: dict    # property name -> MODIFIER_VALUE_* (for any property that names one)
    sections: list     # [(section_type, [property names])]
    scale: dict        # property name -> (scale class, stat type, stat_scale) for spirit-scaled values

    def p(self, key, default=0.0):
        v = self.props.get(key)
        return default if v is None else v


@dataclass
class Ability:
    id: int
    name: str
    class_name: str
    hero_id: int
    slot: str          # signature1..4
    ultimate: bool
    props: dict        # name -> float
    scale: dict        # name -> (class, stat type, stat_scale)
    upgrades: list     # [ {prop: flat delta}, x3 ]  (plain / EAddToBase upgrades only)
    description: dict
    # [ {prop: [(upgrade_type, scale_stat_filter, bonus), ...]}, x3 ] for EAddToScale / EMultiplyScale /
    # EMultiplyBase upgrades (e.g. "+0.2 spirit scaling"). abilities.json merges these into `upgrades` and loses
    # the flat part when a tier has both, so both lists are rebuilt from raw/items.json.
    scale_upgrades: list = field(default_factory=list)


@dataclass
class Hero:
    id: int
    name: str
    class_name: str
    base: dict
    per_boon: dict
    level_gold: list           # cumulative souls required for level 1..N
    invest: dict               # slot -> [(threshold, bonus)]
    weapon: dict               # weapon_info of primary gun
    abilities: list = field(default_factory=list)  # [Ability] in slot order
    level_bonus: list = field(default_factory=list)  # per level 1..N: "unlock" (an ability unlock), "point" (an ability point) or None


@lru_cache(maxsize=1)
def game():
    return Game()


class Game:
    def __init__(self):
        raw_items = {i["id"]: i for i in _load("raw/items.json")}
        self.items: dict[int, Item] = {}
        for s in _load("shop_items.json"):
            r = raw_items.get(s["id"], {})
            sections, innate_names = [], set()
            for sec in r.get("tooltip_sections") or []:
                names = []
                for a in sec.get("section_attributes", []):
                    names += a.get("properties", []) + a.get("important_properties", []) + a.get("elevated_properties", [])
                sections.append((sec.get("section_type"), names))
                if sec.get("section_type") == "innate":
                    innate_names |= set(names)
            props, stat_type, scale, innate = {}, {}, {}, {}
            for k, v in s["properties"].items():
                if not isinstance(v, dict):
                    continue
                val = _num(v.get("value"))
                props[k] = val
                if v.get("provided_property_type"):
                    stat_type[k] = v["provided_property_type"]
                    if k in innate_names and val:
                        innate[k] = val
                rs = (r.get("properties") or {}).get(k, {}).get("scale_function") or {}
                if rs.get("class_name") == "scale_function_tech_damage" or rs.get("stat_scale"):
                    scale[k] = (rs.get("class_name"), rs.get("specific_stat_scale_type"), _num(rs.get("stat_scale")) or 0.0)
            self.items[s["id"]] = Item(s["id"], s["name"], s["class_name"], s["slot"], s["tier"], s["cost"],
                                       s["activation"], s.get("components") or [], props, innate, stat_type,
                                       sections, scale)
        self.items_by_class = {i.class_name: i for i in self.items.values()}
        self.items_by_name = {i.name.lower(): i for i in self.items.values()}

        raw_ups = {}
        for x in _load("raw/items.json"):
            if x.get("type") == "ability" or str(x.get("class_name", "")).startswith(("ability", "citadel_ability")) \
                    or x.get("upgrades"):
                raw_ups[x["class_name"]] = x.get("upgrades") or []

        def split_upgrades(cls, merged):
            if cls not in raw_ups:
                return merged, [{} for _ in merged]
            flat, special = [], []
            for u in raw_ups[cls]:
                fd, sd = {}, {}
                for pu in u.get("property_upgrades") or []:
                    b = _num(pu.get("bonus"))
                    if b is None:
                        continue
                    t = pu.get("upgrade_type")
                    if t in (None, "EAddToBase"):
                        fd[pu["name"]] = fd.get(pu["name"], 0.0) + b
                    else:
                        sd.setdefault(pu["name"], []).append((t, pu.get("scale_stat_filter"), b))
                flat.append(fd)
                special.append(sd)
            return flat, special

        abil = {}
        for a in _load("abilities.json"):
            props, scale = {}, {}
            for k, v in a["properties"].items():
                if not isinstance(v, dict):
                    continue
                props[k] = _num(v.get("value"))
                sc = v.get("scale") or {}
                if sc:
                    scale[k] = (sc.get("class_name"), sc.get("specific_stat_scale_type"), _num(sc.get("stat_scale")) or 0.0)
            flat, special = split_upgrades(
                a["class_name"], [{k: _num(x) for k, x in u.items()} for u in (a.get("upgrades") or [])])
            abil[a["id"]] = Ability(a["id"], a["name"], a["class_name"], a["hero_id"], a["slot"],
                                    a["ability_type"] == "ultimate", props, scale, flat,
                                    a.get("description") or {}, special)
        self.abilities = abil
        self.abilities_by_class = {a.class_name: a for a in abil.values()}

        weapons = {w["hero_id"]: w["weapon_info"] for w in _load("weapons.json")}
        self.heroes: dict[int, Hero] = {}
        for h in _load("heroes.json"):
            lv = sorted(((int(k), v["required_gold"]) for k, v in h["level_info"].items()))
            inv = {slot: [(b["gold_threshold"], b["bonus"]) for b in rows]
                   for slot, rows in h["souls_invested_bonuses"].items()}
            hero = Hero(h["id"], h["name"], h["class_name"], h["starting_stats"], h["level_up_per_boon"],
                        [g for _, g in lv], inv, weapons.get(h["id"], {}))
            for k, _ in lv:
                cur = h["level_info"][str(k)].get("bonus_currencies") or []
                hero.level_bonus.append("unlock" if "EAbilityUnlocks" in cur else "point" if "EAbilityPoints" in cur else None)
            for slot in ("signature1", "signature2", "signature3", "signature4"):
                ref = h["abilities"].get(slot)
                if ref and ref["id"] in abil:
                    hero.abilities.append(abil[ref["id"]])
            self.heroes[h["id"]] = hero
        self.heroes_by_name = {h.name.lower(): h for h in self.heroes.values()}

    # lookups -----------------------------------------------------------------
    def hero(self, key) -> Hero:
        if isinstance(key, Hero):
            return key
        if isinstance(key, int):
            return self.heroes[key]
        k = str(key).lower()
        if k in self.heroes_by_name:
            return self.heroes_by_name[k]
        for h in self.heroes.values():
            if h.class_name == k or h.class_name == "hero_" + k:
                return h
        raise KeyError(key)

    def item(self, key) -> Item:
        if isinstance(key, Item):
            return key
        if isinstance(key, int):
            return self.items[key]
        k = str(key).lower()
        if k in self.items_by_name:
            return self.items_by_name[k]
        if k in self.items_by_class:
            return self.items_by_class[k]
        if "upgrade_" + k in self.items_by_class:
            return self.items_by_class["upgrade_" + k]
        raise KeyError(key)

    def level_for_souls(self, hero: Hero, souls: float) -> int:
        lvl = 0
        for i, g in enumerate(hero.level_gold):
            if souls >= g:
                lvl = i + 1
        return max(lvl, 1)
