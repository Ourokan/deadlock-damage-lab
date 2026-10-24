"""Fit hero-only gun accuracy for heroes whose gun records none in the match stats (Graves, Deadman Danny) from
replay shots and hits (gun_stats.py output), using every other hero in the same matches as the reference.

The sim's Skill.accuracy is the API's hero accuracy (Enemy Hero Accuracy Hits / Shots), so the replay numbers are
mapped onto that scale with the reference heroes (one-bullet guns), whose API accuracy is known:

- shots (used): API hero-aimed shots = a x replay shots in a window (all shots, shots within W s of the player's own
  gun hit on an enemy hero, or of any hero-vs-hero damage involving the player); a = median over references, the
  fight window with the smallest spread wins (all shots spread about as little). accuracy = gun hits / (a x replay shots).
- time (cross-check only): gun damage on heroes with weapon power taken out, per second of hero fighting, over the
  gun's base damage per second = x; references y = API accuracy x (1 + headshot share x 0.65); c = median y / x.
  Its per-hero c runs 0.5-2.3 (how much of a fight each hero spends shooting), so it is too loose to fit with.

Charged gun (Danny): a replay hit deals charge_factor x the base bullet damage of a reference hit (weapon power,
headshots and resists taken out), and Danny fires about 1 shot a second instead of the data's 4. The sim keeps the
gun's damage per second and fires charge_factor x bigger shots charge_factor x less often (build.py).
Tethered gun (Graves): The Teacher only fires through a tether that attaches within MaxRange (20 m); beyond it the
sim's gun deals nothing (tether_range_m, build.Stats.falloff).

usage: python3 fit_guns.py <gun_stats.json> [sample.jsonl.gz for the distance] [--write]
--write stores the result in data/gun_calibration.json (read by deadsim.accuracy.hero_default_skill).
"""
import gzip
import json
import math
import os
import statistics
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, ROOT)
from deadsim.accuracy import DIST_PREFIX, HEADS, HITS, SHOTS, distance_profile  # noqa: E402
from deadsim.data import game  # noqa: E402

TARGETS = {76: "Graves", 78: "Deadman Danny"}
CHARGED = {78}
TETHERED = {76}
WINDOWS = (1, 2, 3, 4)
MIN_API_SHOTS = 300
CRIT_BONUS = 0.65


def pct(xs, q):
    xs = sorted(xs)
    i = (len(xs) - 1) * q
    lo = int(i)
    return xs[lo] + (xs[min(lo + 1, len(xs) - 1)] - xs[lo]) * (i - lo)


def logsd(xs):
    ls = [math.log(x) for x in xs if x > 0]
    return statistics.pstdev(ls) if len(ls) > 1 else float("nan")


def weapon(hid):
    w = game().heroes[hid].weapon
    return w["bullet_damage"], w["shots_per_second_with_reload"], w.get("bullets", 1)


def is_ref(r):
    """A plain one-bullet gun whose replay hits agree with the API's (shotguns count pellets as API shots)."""
    if r["hero_id"] in TARGETS or r["hero_id"] not in game().heroes or r["api_shots"] < MIN_API_SHOTS:
        return False
    if weapon(r["hero_id"])[2] != 1:
        return False
    return 0.8 <= r["hits"] / max(1, r["api_hits"]) <= 1.2


def time_x(r, w):
    bd, sps, _ = weapon(r["hero_id"])
    t = r[f"time_fight{w}"]
    return r["gun_damage_base"] / (bd * sps * t) if t > 0 else 0.0


def ref_y(r):
    acc = r["api_hits"] / r["api_shots"]
    return acc * (1 + CRIT_BONUS * r["api_heads"] / max(1, r["api_hits"]))


def tether_range(hid):
    for x in json.load(open(os.path.join(ROOT, "..", "data", "game", "raw", "items.json"))):
        if x.get("type") == "weapon" and x.get("hero") == hid:
            v = ((x.get("properties") or {}).get("MaxRange") or {}).get("value")
            return float(str(v).rstrip("m")) if v else None
    return None


def distance(sample, hid):
    if not sample:
        return None
    meds = []
    for line in gzip.open(sample):
        for p in json.loads(line)["players"]:
            if p["hero_id"] == hid:
                med, _ = distance_profile({k: v for k, v in p["custom"].items() if k.startswith(DIST_PREFIX)})
                if med is not None:
                    meds.append(med)
    return (round(statistics.median(meds), 1), len(meds)) if meds else None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    rows = json.load(open(args[0]))
    sample = args[1] if len(args) > 1 else None
    refs = [r for r in rows if is_ref(r)]
    print(f"{len(rows)} player rows, {len(refs)} reference players on {len({r['hero_id'] for r in refs})} heroes")

    # shots method: which replay shot count tracks the API's hero-aimed shots best
    keys = ["shots"] + [f"shots_hit{w}" for w in WINDOWS] + [f"shots_fight{w}" for w in WINDOWS]
    shot_fit = {}
    for k in keys:
        ratios = [r["api_shots"] / r[k] for r in refs if r[k] > 0]
        shot_fit[k] = (statistics.median(ratios), logsd(ratios))
        print(f"  shots  {k:13s} API shots / replay = {shot_fit[k][0]:.3f}  log sd {shot_fit[k][1]:.3f}")
    # count fight-window shots only: all shots tie on spread but tie the fit to how much a hero farms creeps (Graves
    # tethers creeps a lot), which the API's hero-aimed shots leave out
    sk = min((k for k in shot_fit if k.startswith("shots_fight")), key=lambda k: shot_fit[k][1])
    a = shot_fit[sk][0]

    # time method
    time_fit = {}
    for w in WINDOWS:
        ratios = [ref_y(r) / time_x(r, w) for r in refs if time_x(r, w) > 0]
        time_fit[w] = (statistics.median(ratios), logsd(ratios))
        print(f"  time   fight{w}        y / x = {time_fit[w][0]:.3f}  log sd {time_fit[w][1]:.3f}")
    tw = min(time_fit, key=lambda w: time_fit[w][1])
    c = time_fit[tw][0]
    # how well each method recovers the references' own API accuracy (headshots excluded)
    err_s = [math.log((r["hits"] / (a * r[sk])) / (r["api_hits"] / r["api_shots"])) for r in refs if r[sk] > 0]
    err_t = [math.log(c * time_x(r, tw) / ref_y(r)) for r in refs if time_x(r, tw) > 0]
    print(f"  references: shots method ({sk}) log error sd {statistics.pstdev(err_s):.3f}; "
          f"time method (fight{tw}) {statistics.pstdev(err_t):.3f}")

    # base damage per hit relative to the bullet's base damage, headshots taken out (resists, falloff, conditional
    # weapon bonuses left in): what an ordinary hit lands for, to read Danny's charge against
    q_ref = statistics.median(r["gun_damage_base"] / r["hits"] / weapon(r["hero_id"])[0]
                              / (1 + CRIT_BONUS * r["headshots"] / r["hits"]) for r in refs if r["hits"])
    print(f"  references: base damage per hit / bullet damage (no headshots) {q_ref:.3f}")
    out = {"source": f"{len({r['match_id'] for r in rows})} Phantom+ replays (sim/scripts/gun_calib), "
                     f"{len(refs)} reference players",
           "shots_method": {"count": sk, "api_shots_per_replay_shot": round(a, 4), "log_sd": round(shot_fit[sk][1], 3)},
           "time_method": {"window_s": tw, "c": round(c, 4), "log_sd": round(time_fit[tw][1], 3)},
           "ref_hit_base_ratio": round(q_ref, 4),
           "heroes": {}}
    for hid, name in TARGETS.items():
        mine = [r for r in rows if r["hero_id"] == hid and r[f"time_fight{tw}"] > 0 and r["shots"] > 0]
        if not mine:
            continue
        acc_t = [c * time_x(r, tw) for r in mine]
        acc_s = [r["hits"] / (a * r[sk]) for r in mine if r[sk] > 0]
        acc_s_mean = sum(r["hits"] for r in mine) / sum(a * r[sk] for r in mine)
        hs = [r["headshots"] / max(1, r["hits"]) for r in mine]
        q = {"p25": .25, "p50": .5, "p75": .75, "p90": .9}
        bd, sps, _ = weapon(hid)
        dph = statistics.median(r["gun_damage_base"] / max(1, r["hits"]) for r in mine)
        row = {"name": name, "n": len(mine),
               "accuracy": {k: round(pct(acc_s, v), 4) for k, v in q.items()},
               "headshot": {k: round(pct(hs, v), 4) for k, v in q.items()},
               "accuracy_pooled": round(acc_s_mean, 4),
               "time_method_accuracy_p50": round(pct(acc_t, .5), 4),
               "replay_hit_rate_p50": round(pct([r["hits"] / r["shots"] for r in mine], .5), 4),
               "base_damage_per_hit": round(dph, 1), "sim_base_damage_per_shot": bd,
               "tether_shot_share": round(sum(r["tether_shots"] for r in mine) / sum(r["shots"] for r in mine), 3)}
        if hid in CHARGED:
            row["charge_factor"] = round(dph / bd / q_ref, 3)
        if hid in TETHERED:
            row["tether_range_m"] = tether_range(hid)
        d = distance(sample, hid)
        if d:
            row["median_distance_m"], row["n_distance"] = d
        out["heroes"][str(hid)] = row
        print(f"{name}: n={len(mine)} accuracy p25/p50/p75 {row['accuracy']['p25']:.3f}/{row['accuracy']['p50']:.3f}/"
              f"{row['accuracy']['p75']:.3f} (pooled {acc_s_mean:.3f}; time method {row['time_method_accuracy_p50']:.3f}); "
              f"headshots {row['headshot']['p50']:.3f}; base dmg/hit {dph:.1f} vs sim shot {bd} "
              f"(charge {row.get('charge_factor')}); tether {row.get('tether_range_m')} m; "
              f"distance {row.get('median_distance_m')}")
    if "--write" in sys.argv:
        dst = os.path.join(ROOT, "data", "gun_calibration.json")
        json.dump(out, open(dst, "w"), indent=1)
        print("->", dst)
    else:
        print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
