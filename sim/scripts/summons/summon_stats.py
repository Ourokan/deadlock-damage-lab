"""Real summon numbers from fetch_summons.py output: health, lifetime, how often enemy heroes kill them, and the share
of enemy hero damage that goes to a summon instead of its owner while it is alive.

usage: python3 -I summon_stats.py <work dir> [out.json]

Per summon kind (label in fetch_summons.TABLES):
- n, hp (median max health at spawn) and hp_by_min (median per 5 game minutes: it grows with the owner's boons),
- life_s (median seconds alive), life_s_not_hero_killed / life_s_hero_killed (same, split by whether an enemy hero
  killed it), killed (share whose health reached 0), hero_killed (last hit by an enemy hero),
- engaged (share that took any enemy hero damage) and hero_killed_engaged (share of those an enemy hero killed:
  closer to a duel, where every summon is in the fight),
- focus_share = enemy hero damage to summons of that kind / (that + enemy hero damage to the owner), counted only
  while at least one summon of that kind is alive. Damage to a summon is capped at its health (overkill dropped).
- gun_focus_share: the same with gun damage only (what the sim's focus moves: only bullets hit summons there),
  gun_part: share of enemy hero damage to the summons that is gun damage, splash_ratio: non-gun enemy damage to
  the summons / non-gun enemy damage to the owner in the same windows.
- by_ability: top enemy ability ids by damage dealt to the summons (bullets and abilities are both counted).
"""
import collections
import glob
import json
import os
import statistics
import sys

TICKS = 60.0
INVALID = 16777215
ITEMS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "data", "game", "raw", "items.json")
GUN_IDS = {str(x["id"]) for x in json.load(open(ITEMS)) if str(x.get("class_name", "")).startswith("citadel_weapon")}


def load(fn):
    rows = collections.defaultdict(list)
    for line in open(fn):
        r = json.loads(line)
        rows[r["k"]].append(r)
    return rows


def instances(rows, hero_of, team_of):
    """(label, team, owner pawn, max hp, t0, t1) per summon, pairing create/delete by entity index."""
    ev = collections.defaultdict(list)
    for r in rows["ent"]:
        s = (r.get("s") or "").split("|")
        if len(s) < 5:
            continue
        ev[r["a"]].append((r["tick"], s, r.get("v")))
    out = []
    last_tick = max([r["tick"] for r in rows["dmg"]] + [0])
    for idx, es in ev.items():
        es.sort(key=lambda x: (x[0], x[1][1] != "delete"))
        cur = None
        for tick, s, v in es:
            label, kind = s[0], s[1]
            if kind == "create":
                if cur:
                    out.append(cur + [tick])
                owner = int(s[2]) % 16384 if s[2] and int(s[2]) != INVALID else None
                team = int(s[3]) if s[3] else None
                cur = [label, team, owner, v or (float(s[4]) if s[4] else None), idx, tick]
            elif kind == "delete" and cur:
                out.append(cur + [tick])
                cur = None
        if cur:
            out.append(cur + [last_tick])
    res = []
    for label, team, owner, hp, idx, t0, t1 in out:
        hero_label = label.split("_")[0]
        if owner not in hero_of:
            owner = None
        if owner is None and team is not None:
            # owner = the hero on that team whose summon this is
            want = OWNER_HERO.get(hero_label)
            owner = next((p for p, h in hero_of.items() if h == want and team_of.get(p) == team), None)
        if team is None and owner is not None:
            team = team_of.get(owner)
        res.append(dict(label=label, team=team, owner=owner, hp=hp, idx=idx, t0=t0, t1=t1))
    return res


OWNER_HERO = {"graves": 76, "sinclair": 60, "mcginnis": 8, "talon": 17, "rem": 79, "calico": 16, "solomon": 85,
              "ratking": 84, "viscous": 35, "nurse": 87}


def merge(iv):
    iv = sorted(iv)
    out = []
    for a, b in iv:
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def inside(iv, t):
    lo, hi = 0, len(iv)
    while lo < hi:
        m = (lo + hi) // 2
        if iv[m][1] < t:
            lo = m + 1
        else:
            hi = m
    return lo < len(iv) and iv[lo][0] <= t <= iv[lo][1]


def match_stats(fn, acc):
    rows = load(fn)
    hero_of = {r["a"]: int(r["s"]) for r in rows["ctl"] if r.get("s") and r["s"] != "0"}
    team_of = {r["a"]: int(r["s"]) for r in rows["pawn"] if r.get("s")}
    ins = instances(rows, hero_of, team_of)
    by_idx = collections.defaultdict(list)
    for s in ins:
        by_idx[s["idx"]].append(s)
    taken = collections.defaultdict(float)
    for r in rows["sdmg"]:
        att, vic = divmod(r["a"], 100000)
        s = next((x for x in by_idx.get(vic, ()) if x["t0"] <= r["tick"] <= x["t1"]), None)
        if s is None:
            continue
        ab, _, acls = ((r.get("s") or "") + "||").split("|")[:3]
        enemy_hero = att in team_of and team_of[att] != s["team"]
        room = max(0.0, (s["hp"] or 1e9) - taken[id(s)])
        d = min(room, r["v"])
        taken[id(s)] += d
        if enemy_hero:
            s.setdefault("hero_dmg", 0.0)
            s["hero_dmg"] += d
            if ab in GUN_IDS:
                s["gun_dmg"] = s.get("gun_dmg", 0.0) + d
            s.setdefault("by_ab", collections.Counter())[ab] += d
        if s["hp"] and d > 0 and taken[id(s)] >= s["hp"] - 0.5:     # victim_health_new is empty in the extracts
            s["killed"] = True
            s["hero_killed"] = enemy_hero
    # owner damage while each kind is alive
    windows = collections.defaultdict(list)
    for s in ins:
        if s["owner"] is not None:
            windows[(s["owner"], s["label"])].append((s["t0"], s["t1"]))
    windows = {k: merge(v) for k, v in windows.items()}
    owner_dmg = collections.defaultdict(float)
    owner_gun = collections.defaultdict(float)
    for r in rows["dmg"]:
        att, vic = divmod(r["a"], 100000)
        if team_of.get(att) == team_of.get(vic):
            continue
        for (owner, label), iv in windows.items():
            if owner == vic and inside(iv, r["tick"]):
                owner_dmg[label] += r["v"]
                if r.get("s") in GUN_IDS:
                    owner_gun[label] += r["v"]
    for s in ins:
        if s["owner"] is None or s["hp"] is None:
            continue
        a = acc[s["label"]]
        a["n"] += 1
        a["hp"].append(s["hp"])
        a["hp_min"][int(s["t0"] / TICKS / 300)].append(s["hp"])
        a["life"].append((s["t1"] - s["t0"]) / TICKS)
        (a["life_hk"] if s.get("hero_killed") else a["life_other"]).append((s["t1"] - s["t0"]) / TICKS)
        a["killed"] += bool(s.get("killed"))
        a["hero_killed"] += bool(s.get("hero_killed"))
        a["hero_dmg"] += s.get("hero_dmg", 0.0)
        if s.get("hero_dmg", 0.0) > 0:
            a["engaged"] += 1
            a["engaged_killed"] += bool(s.get("hero_killed"))
        a["gun_dmg"] += s.get("gun_dmg", 0.0)
        a["by_ab"].update(s.get("by_ab", {}))
        a["matches"].add(os.path.basename(fn))
    for label, d in owner_dmg.items():
        acc[label]["owner_dmg"] += d
        acc[label]["owner_gun"] += owner_gun[label]


def main():
    work = sys.argv[1]
    acc = collections.defaultdict(lambda: dict(n=0, hp=[], hp_min=collections.defaultdict(list), life=[], life_other=[], life_hk=[], killed=0,
                                               hero_killed=0, engaged=0, engaged_killed=0, hero_dmg=0.0, owner_dmg=0.0, gun_dmg=0.0, owner_gun=0.0,
                                               by_ab=collections.Counter(), matches=set()))
    files = sorted(glob.glob(os.path.join(work, "raw", "*.ndjson")))
    for fn in files:
        match_stats(fn, acc)
    out = {"matches": len(files), "kinds": {}}
    for label, a in sorted(acc.items()):
        if not a["n"]:
            continue
        tot = a["hero_dmg"] + a["owner_dmg"]
        out["kinds"][label] = dict(
            n=a["n"], matches=len(a["matches"]), hp=statistics.median(a["hp"]),
            hp_by_min={f"{k * 5}-{k * 5 + 5}": statistics.median(v) for k, v in sorted(a["hp_min"].items())},
            life_s=round(statistics.median(a["life"]), 2),
            life_p25_p75=[round(x, 2) for x in statistics.quantiles(a["life"], n=4)[::2]] if a["n"] > 2 else None,
            life_s_not_hero_killed=round(statistics.median(a["life_other"]), 2) if a["life_other"] else None,
            life_s_hero_killed=round(statistics.median(a["life_hk"]), 2) if a["life_hk"] else None,
            killed=round(a["killed"] / a["n"], 3), hero_killed=round(a["hero_killed"] / a["n"], 3),
            engaged=round(a["engaged"] / a["n"], 3),
            hero_killed_engaged=round(a["engaged_killed"] / a["engaged"], 3) if a["engaged"] else None,
            hero_dmg_per_summon=round(a["hero_dmg"] / a["n"], 1),
            focus_share=round(a["hero_dmg"] / tot, 3) if tot else None,
            gun_focus_share=round(a["gun_dmg"] / (a["gun_dmg"] + a["owner_gun"]), 3) if a["gun_dmg"] + a["owner_gun"] else None,
            gun_part=round(a["gun_dmg"] / a["hero_dmg"], 3) if a["hero_dmg"] else None,
            splash_ratio=round((a["hero_dmg"] - a["gun_dmg"]) / (a["owner_dmg"] - a["owner_gun"]), 3)
            if a["owner_dmg"] > a["owner_gun"] else None,
            by_ability=dict(a["by_ab"].most_common(6)))
    txt = json.dumps(out, indent=1)
    if len(sys.argv) > 2:
        open(sys.argv[2], "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
