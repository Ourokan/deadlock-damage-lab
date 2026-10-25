"""Turn raw deadlock-api asset dumps into compact tables for the combat model."""
import json, re, sys, os, shutil
RAW, OUT = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(OUT, "raw"), exist_ok=True)
for f in os.listdir(RAW):
    if f.startswith("assets_") or f in ("patches.json", "info.json"):
        shutil.copy(os.path.join(RAW, f), os.path.join(OUT, "raw", f.replace("assets_", "")))
heroes = json.load(open(os.path.join(RAW, "assets_heroes.json")))
items = json.load(open(os.path.join(RAW, "assets_items.json")))
by_class = {x["class_name"]: x for x in items}

def text(s):
    if not isinstance(s, str): return s
    s = re.sub(r"<svg.*?</svg>", "", s, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

def num(v):
    if isinstance(v, (int, float)): return v
    m = re.fullmatch(r"\s*(-?[\d.]+)\s*([a-z%]*)\s*", str(v))
    return float(m.group(1)) if m else v

def props(p, keep_zero=False):
    out = {}
    for k, v in (p or {}).items():
        val = v.get("value")
        if val is None or (not keep_zero and str(val) in ("0", "0.0", "-1", "-1.0")): continue
        d = {"value": num(val)}
        if isinstance(val, str) and re.search(r"[a-z%]$", val): d["raw"] = val
        for key in ("label", "postfix", "provided_property_type", "conditional", "usage_flags", "street_brawl_value", "negative_attribute"):
            if v.get(key) not in (None, ""): d[key] = v[key]
        sf = v.get("scale_function")
        if sf and sf.get("class_name"):
            d["scale"] = {k2: sf[k2] for k2 in ("class_name", "subclass_name", "specific_stat_scale_type", "stat_scale", "scaling_stats") if sf.get(k2) is not None}
        out[k] = d
    return out

def upgrades(u):
    return [{pu["name"]: num(pu["bonus"]) for pu in t.get("property_upgrades", [])} for t in (u or [])]

def desc(x):
    d = x.get("description")
    if isinstance(d, dict): return {k: text(v) for k, v in d.items() if v}
    return text(d)

# In-development heroes (Violet, Baba) are pickable in real matches. Keep one once the sim has a model for it
# (sim/deadsim/heroes/<class without hero_>.py), so a new hero never runs on generic abilities.
MODELED = {f[:-3] for f in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sim", "deadsim", "heroes"))
           if f.endswith(".py")}
release = [h for h in heroes if h["player_selectable"] and not h["disabled"]
           and (not h["in_development"] or h["class_name"].removeprefix("hero_") in MODELED)]
H, A, W = [], [], []
for h in release:
    sig = {k: h["items"].get(k) for k in ("signature1", "signature2", "signature3", "signature4")}
    wpn = by_class.get(h["items"].get("weapon_primary"), {})
    H.append({"id": h["id"], "name": h["name"], "class_name": h["class_name"], "hero_type": h.get("hero_type"),
              "gun_tag": h.get("gun_tag"), "complexity": h.get("complexity"),
              "starting_stats": {k: v["value"] for k, v in h["starting_stats"].items()},
              "level_up_per_boon": h.get("standard_level_up_upgrades"), "level_info": h.get("level_info"),
              "souls_invested_bonuses": h.get("cost_bonuses"), "purchase_bonuses": h.get("purchase_bonuses"),
              "scaling_stats": h.get("scaling_stats"), "item_slot_info": h.get("item_slot_info"),
              "weapon": {"id": wpn.get("id"), "class_name": wpn.get("class_name"), "name": wpn.get("name")},
              "abilities": {k: {"class_name": v, "id": by_class.get(v, {}).get("id"), "name": by_class.get(v, {}).get("name")} for k, v in sig.items()}})
    if wpn:
        W.append({"hero_id": h["id"], "hero": h["name"], "id": wpn["id"], "class_name": wpn["class_name"], "name": wpn["name"],
                  "weapon_info": wpn.get("weapon_info"), "properties": props(wpn.get("properties"))})
    for slot, cn in sig.items():
        a = by_class.get(cn)
        if not a: continue
        A.append({"hero_id": h["id"], "hero": h["name"], "slot": slot, "id": a["id"], "class_name": cn, "name": a.get("name"),
                  "ability_type": a.get("ability_type"), "boss_damage_scale": a.get("boss_damage_scale"),
                  "description": desc(a), "properties": props(a.get("properties")), "upgrades": upgrades(a.get("upgrades")),
                  "weapon_info": a.get("weapon_info") or None})
S = []
for x in items:
    if x.get("type") != "upgrade" or not x.get("shopable"): continue
    S.append({"id": x["id"], "class_name": x["class_name"], "name": x.get("name"), "slot": x.get("item_slot_type"),
              "tier": x.get("item_tier"), "cost": x.get("cost"), "activation": x.get("activation"),
              "is_active": x.get("is_active_item"), "components": x.get("component_items") or [],
              "description": desc(x), "properties": props(x.get("properties")), "upgrades": upgrades(x.get("upgrades"))})
S.sort(key=lambda s: (s["slot"] or "", s["tier"] or 0, s["name"] or ""))
for name, data in (("heroes", H), ("abilities", A), ("weapons", W), ("shop_items", S)):
    json.dump(data, open(os.path.join(OUT, f"{name}.json"), "w"), indent=1)
    print(name, len(data))
