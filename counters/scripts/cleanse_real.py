"""What Counterspell and Dispel Magic block in real ranked matches, per enemy ability, from the damage matrix.

Same pairing as damage/scripts/decay_vs_dispel.py, for every enemy damage source: inside one 3-minute damage-matrix
window, from one enemy dealer, compare the damage (normalised by each target's max HP) taken by targets holding the
item for the whole window with teammates who have not bought it yet. ratio = holders / non-holders; 1 - ratio is
the share the item removed (blocked by a spell parry, cleansed by Dispel, or avoided some other way). Kills by that
dealer are paired the same way (deaths per target-window), for kill-avoidance.

Sources are grouped per dealer hero ability (ultimate or not), "gun", "melee", "item" and "all". Damage matrix
values are before resists (sim-mechanics memory), so the items' own resists don't show here; their HP is
normalised away.

usage: python3 cleanse_real.py ITEM_NAME [n_matches] [min_badge] [days] [focus_hero] [n_focus]
  e.g. cleanse_real.py Counterspell 1200 91 5 Lash 600
writes counters/work/cleanse_<item>_<badge>.json (match ids cached in counters/work/cache_<item>_<badge>/)
"""
import concurrent.futures as cf
import glob
import gzip
import json
import os
import random
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(ROOT, "sim"))
from deadsim import game  # noqa: E402
from deadsim.dmatrix import win  # noqa: E402

UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}
G = game()
BUILDS = os.environ.get("PLAYER_BUILDS", "/mnt/project-files/data/builds/player_builds")


def get(mid, cache):
    fn = os.path.join(cache, f"{mid}.json.gz")
    if os.path.exists(fn):
        return json.load(gzip.open(fn, "rt"))
    url = f"https://api.deadlock-api.com/v1/matches/{mid}/metadata"
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                m = json.load(r)["match_info"]
            keep = {k: m[k] for k in ("match_id", "duration_s", "damage_matrix")}
            keep["players"] = [{k: p.get(k) for k in ("player_slot", "team", "hero_id", "items", "death_details")}
                               | {"max_hp": {s["time_stamp_s"]: s["max_health"] for s in p.get("stats", [])}}
                               for p in m["players"]]
            json.dump(keep, gzip.open(fn, "wt"))
            return keep
        except Exception:  # noqa: BLE001
            time.sleep(3 * (i + 1))
    return None


def held(items, item_id, t0, t1):
    return any(x["item_id"] == item_id and x["game_time_s"] <= t0 and (not x.get("sold_time_s") or x["sold_time_s"] >= t1)
               for x in items)


def bought_by(items, item_id, t1):
    return any(x["item_id"] == item_id and x["game_time_s"] <= t1 for x in items)


_GROUPS = {}


def group(hero_id, name):
    """Source name -> (group, is_ult) for a dealer hero: an ability class name, gun, melee, item or other."""
    key = (hero_id, name)
    if key in _GROUPS:
        return _GROUPS[key]
    g = None
    h = G.heroes.get(hero_id)
    if name.startswith("upgrade_"):
        g = ("item:" + name, False)
    elif name.startswith("citadel_weapon") or name == "Bullet":
        g = ("gun", False)
    elif "melee" in name.lower():
        g = ("melee", False)
    elif h is not None:
        # exact class name, else the longest prefix (Lash's ult citadel_ability_lash_ultimate also starts with
        # Grapple's citadel_ability_lash)
        best = None
        for a in h.abilities:
            if name == a.class_name:
                best = a
                break
            if name.startswith(a.class_name + "_") and (best is None or len(a.class_name) > len(best.class_name)):
                best = a
        if best is not None:
            g = (best.name, bool(best.ultimate))
    _GROUPS[key] = g
    return g


def analyse(m, item_id, acc):
    dm = m.get("damage_matrix") or {}
    names = dm.get("source_details", {}).get("source_name", [])
    stypes = dm.get("source_details", {}).get("stat_type", [])
    times = dm.get("sample_time_s") or []
    n = len(times)
    P = {p["player_slot"]: p for p in m["players"]}

    def hp(p, t):
        return p["max_hp"].get(t) or p["max_hp"].get(str(t)) or (list(p["max_hp"].values())[-1] if p["max_hp"] else None)

    for d in dm.get("damage_dealers", []):
        me = P.get(d["dealer_player_slot"])
        if not me:
            continue
        hid = me["hero_id"]
        # per target slot: {group: cumulative array}
        per = {}
        for s in d["damage_sources"]:
            i = s["source_details_index"]
            if i >= len(names) or stypes[i] != 0:
                continue
            g = group(hid, names[i])
            if g is None:
                continue
            for tp in s["damage_to_players"]:
                tgt = P.get(tp["target_player_slot"])
                if tgt and tgt["team"] != me["team"]:
                    per.setdefault(tgt["player_slot"], []).append((g, tp["damage"]))
        for k in range(1, n):
            t0, t1 = times[k - 1], times[k]
            sides = {True: [], False: []}
            for slot, tgt in P.items():
                if tgt["team"] == me["team"]:
                    continue
                h = hp(tgt, t1)
                if not h:
                    continue
                if held(tgt["items"], item_id, t0, t1):
                    side = True
                elif not bought_by(tgt["items"], item_id, t1):
                    side = False
                else:
                    continue
                row = {}
                for (g, ult), arr in per.get(slot, ()):
                    v = win(arr, k, n) / h
                    row[g] = row.get(g, 0.0) + v
                    row["all"] = row.get("all", 0.0) + v
                    if g.startswith("item:"):
                        row["items"] = row.get("items", 0.0) + v
                    elif g not in ("gun", "melee"):
                        tag = "abilities:ult" if ult else "abilities:non-ult"
                        row[tag] = row.get(tag, 0.0) + v
                        row["abilities"] = row.get("abilities", 0.0) + v
                kills = sum(1 for x in (tgt.get("death_details") or [])
                            if x.get("killer_player_slot") == me["player_slot"] and t0 < x["game_time_s"] <= t1)
                sides[side].append((row, kills))
            if not sides[True] or not sides[False]:
                continue
            for key in (hid, "any"):
                a = acc.setdefault(str(key), {"windows": 0, "pairs": {}, "kills": [0.0, 0.0]})
                a["windows"] += 1
                a["kills"][0] += sum(x for _, x in sides[True]) / len(sides[True])
                a["kills"][1] += sum(x for _, x in sides[False]) / len(sides[False])
                gs = set()
                for r, _ in sides[True] + sides[False]:
                    gs.update(r)
                for g in gs:
                    w = sum(r.get(g, 0.0) for r, _ in sides[True]) / len(sides[True])
                    wo = sum(r.get(g, 0.0) for r, _ in sides[False]) / len(sides[False])
                    a["pairs"].setdefault(g, []).append((w, wo))


def ratio_ci(pairs, rnd, n_boot=400):
    w, wo = sum(x for x, _ in pairs), sum(y for _, y in pairs)
    if wo <= 0:
        return None, None
    boots = []
    for _ in range(n_boot):
        s = [rnd.choice(pairs) for _ in pairs]
        b = sum(y for _, y in s)
        boots.append(sum(x for x, _ in s) / b if b else 0.0)
    boots.sort()
    return w / wo, [boots[int(0.05 * n_boot)], boots[int(0.95 * n_boot) - 1]]


def main():
    item = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    min_badge = int(sys.argv[3]) if len(sys.argv) > 3 else 91
    days = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    focus = sys.argv[5] if len(sys.argv) > 5 else None
    n_focus = int(sys.argv[6]) if len(sys.argv) > 6 else 600
    item_id = G.item(item).id
    focus_id = G.hero(focus).id if focus else None
    files = sorted(glob.glob(os.path.join(BUILDS, "*.jsonl.gz")))[-days:]
    rows = {}
    for fn in files:
        for line in gzip.open(fn, "rt"):
            r = json.loads(line)
            if (r["badge"] or 0) >= min_badge:
                rows.setdefault(r["match_id"], {})[r["account_id"]] = r
    has, foc = [], []
    for mid, rs in rows.items():
        holders = [r for r in rs.values() if item_id in r["final_items"]]
        if not holders:
            continue
        has.append(mid)
        if focus_id is not None and any(r["hero_id"] == focus_id for r in rs.values()) and len(holders) < len(rs):
            foc.append(mid)
    rnd = random.Random(11)
    ids = set(rnd.sample(sorted(has), min(n, len(has))))
    if foc:
        ids |= set(rnd.sample(sorted(foc), min(n_focus, len(foc))))
    tag = item.lower().replace(" ", "_")
    cache = os.path.join(HERE, "..", "work", f"cache_{tag}_{min_badge}")
    os.makedirs(cache, exist_ok=True)
    acc, done = {}, 0
    with cf.ThreadPoolExecutor(6) as ex:
        for m in ex.map(lambda x: get(x, cache), sorted(ids)):
            if m:
                analyse(m, item_id, acc)
                done += 1
    rnd = random.Random(3)
    out = {"item": item, "min_badge": min_badge, "matches": done, "focus": focus, "by_dealer": {}}
    for key, a in acc.items():
        name = "any" if key == "any" else (G.heroes[int(key)].name if int(key) in G.heroes else f"hero_{key}")
        e = {"windows": a["windows"], "groups": {}}
        k1, k0 = a["kills"]
        e["kill_ratio"] = k1 / k0 if k0 else None
        e["kills_per_window"] = [k1 / a["windows"], k0 / a["windows"]]
        for g, pairs in a["pairs"].items():
            if len(pairs) < 30:
                continue
            r, ci = ratio_ci(pairs, rnd)
            e["groups"][g] = {"ratio": r, "ci90": ci, "windows": len(pairs),
                              "dmg_pct_hp_without": sum(y for _, y in pairs) / len(pairs)}
        out["by_dealer"][name] = e
    path = os.path.join(HERE, "..", "work", f"cleanse_{tag}_{min_badge}.json")
    json.dump(out, open(path, "w"), indent=1)
    show = ["any"] + ([focus] if focus else [])
    for s in show:
        e = out["by_dealer"].get(s)
        if not e:
            continue
        print(s, "windows", e["windows"], "kill ratio", e["kill_ratio"] and round(e["kill_ratio"], 3))
        for g, v in sorted(e["groups"].items(), key=lambda x: -x[1]["dmg_pct_hp_without"])[:14]:
            print(f"  {g:32s} ratio {v['ratio']:.3f} ci {v['ci90'][0]:.3f}-{v['ci90'][1]:.3f}  n {v['windows']}  "
                  f"dmg/hp {v['dmg_pct_hp_without']:.4f}")


if __name__ == "__main__":
    main()
