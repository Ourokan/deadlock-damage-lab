"""Per player: replay shots, gun hits on enemy heroes and the API's hero accuracy (fetch_guns.py output).

usage: python3 gun_stats.py <work dir> [out.json]
For every player: shots (one per m_nShotNumber step of the hero's main weapon), gun hit events on enemy heroes
(DamageEvent with the hero's weapon ability id), headshots (crit_damage > 0), gun damage, and for windows
W = 1..4 s the shots fired within W s of the player's own gun hit on an enemy hero ("hit" windows) or of any
damage between the player and an enemy hero ("fight" windows) and the seconds those windows cover;
gun_damage_base = gun damage on heroes with weapon power taken out (API stats snapshots, interpolated).
"""
import bisect
import collections
import glob
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
TICK = 1 / 64
WINDOWS = (1, 2, 3, 4)
OFFHAND = ("HealingNeedle", "WeaponSwap", "AltWeapon", "ShivWeapon", "ClawWeapon")


def gun_ids():
    out = {}
    for x in json.load(open(os.path.join(ROOT, "data", "game", "raw", "items.json"))):
        if x.get("type") == "weapon" and x.get("hero"):
            out[x["hero"]] = x["id"]
    return out


def near(ts, t, w):
    i = bisect.bisect_left(ts, t - w)
    return i < len(ts) and ts[i] <= t + w


def wp_at(series, t):
    """Weapon power (%) at match time t: linear between the API's stats snapshots (replay time is close enough)."""
    if not series:
        return 0.0
    i = bisect.bisect_left(series, (t, -1e9))
    if i == 0:
        return series[0][1] * t / max(1, series[0][0])
    if i >= len(series):
        return series[-1][1]
    (t0, a), (t1, b) = series[i - 1], series[i]
    return a + (b - a) * (t - t0) / max(1e-9, t1 - t0)


def covered(ts, w):
    """Seconds covered by the union of [t - w, t + w] over sorted ts."""
    tot, end = 0.0, -1e9
    for t in ts:
        a, b = max(t - w, end), t + w
        if b > a:
            tot += b - a
        end = max(end, b)
    return tot


def match_stats(raw, meta, guns):
    rows = [json.loads(line) for line in open(raw)]
    hero_of = {r["a"]: int(r["s"]) for r in rows if r["k"] == "ctl" and r["a"] < 16383 and r["s"] != "0"}
    team_of = {r["a"]: r["s"] for r in rows if r["k"] == "pawn"}
    shots = collections.defaultdict(lambda: collections.defaultdict(list))
    tether = collections.Counter()
    for r in rows:
        if r["k"] == "shot" and not any(o in r["s"] for o in OFFHAND):
            shots[r["a"]][r["s"]].append(r["tick"] * TICK)
            if r["v"]:
                tether[r["a"]] += 1
    hits = collections.defaultdict(list)
    heads, dmg, pellets = collections.Counter(), collections.Counter(), collections.Counter()
    hit_dmg = collections.defaultdict(list)
    fight = collections.defaultdict(list)
    for r in rows:
        if r["k"] != "dmg":
            continue
        att, vic = divmod(r["a"], 100000)
        if att not in team_of or vic not in team_of or team_of[att] == team_of[vic]:
            continue
        t = r["tick"] * TICK
        fight[att].append(t)
        fight[vic].append(t)
        aid, nh, crit = ((r.get("s") or "").split("|") + ["", ""])[:3]
        if att in hero_of and aid == str(guns.get(hero_of[att])):
            hits[att].append(t)
            hit_dmg[att].append((t, r["v"]))
            dmg[att] += r["v"]
            pellets[att] += int(nh or 1)
            heads[att] += float(crit or 0) > 0
    api = {p["hero_id"]: p for p in meta["players"]}
    wp_of = {p["hero_id"]: sorted((st["time_stamp_s"], st.get("weapon_power", 0)) for st in p.get("stats") or [])
             for p in meta["players"]}
    out = []
    for pawn, hid in hero_of.items():
        if hid not in api or not shots[pawn]:
            continue
        tab, st = max(shots[pawn].items(), key=lambda kv: len(kv[1]))
        st.sort()
        h, f = sorted(hits[pawn]), sorted(fight[pawn])
        fs = api[hid].get("final_stats") or {}
        c = fs.get("custom_user_stats") or {}
        base = sum(v / (1 + wp_at(wp_of.get(hid, []), t) / 100) for t, v in hit_dmg[pawn])
        row = {"match_id": meta["match_id"], "hero_id": hid, "weapon_table": tab, "shots": len(st), "hits": len(h),
               "pellets": pellets[pawn], "headshots": heads[pawn], "gun_damage": round(dmg[pawn]),
               "gun_damage_base": round(base),
               "tether_shots": tether[pawn], "duration_s": meta["duration_s"], "weapon_power": fs.get("weapon_power"),
               "api_shots": c.get("Enemy Hero Accuracy##Shots", 0), "api_hits": c.get("Enemy Hero Accuracy##Hits", 0),
               "api_heads": c.get("Enemy Hero Accuracy##Headshots", 0), "hero_bullets_hit": fs.get("hero_bullets_hit")}
        for w in WINDOWS:
            row[f"shots_hit{w}"] = sum(near(h, t, w) for t in st)
            row[f"shots_fight{w}"] = sum(near(f, t, w) for t in st)
            row[f"time_fight{w}"] = round(covered(f, w), 1)
        out.append(row)
    return out


def main():
    work = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(work, "gun_stats.json")
    guns = gun_ids()
    res = []
    for raw in sorted(glob.glob(os.path.join(work, "raw", "*.ndjson"))):
        mid = os.path.basename(raw).split(".")[0]
        meta = json.load(open(os.path.join(work, "meta", f"{mid}.json")))
        res += match_stats(raw, meta, guns)
    json.dump(res, open(out, "w"), indent=0)
    print(len(res), "player rows ->", out)


if __name__ == "__main__":
    main()
