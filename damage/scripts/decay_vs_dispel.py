"""How much of Decay's damage lands on targets that hold Dispel Magic, from real ranked matches.

Decay: 12 s, one tick per second, each tick a % of the target's current HP. Real data has no tick counts, so this
compares Decay damage per target between targets holding Dispel Magic and teammates without it, inside the same
3-minute damage-matrix window from the same Decay owner (same casts, same spirit power), normalised by each
target's max HP in that window. ratio = Dispel holders' Decay damage / non-holders'. Equivalent ticks ~ 12 x ratio
(early ticks are bigger, since they take % of a higher current HP, so a dispel after k ticks removes a bit less than
(12-k)/12 of the damage: read ticks as a lower bound).

usage: python3 scripts/decay_vs_dispel.py [n_matches] [min_badge] [days]
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
sys.path.insert(0, os.path.join(HERE, "..", "..", "sim"))
from deadsim import game  # noqa: E402
from deadsim.dmatrix import at  # noqa: E402

UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}
G = game()
DECAY, DISPEL = G.item("Decay").id, G.item("Dispel Magic").id


def get(mid):
    url = f"https://api.deadlock-api.com/v1/matches/{mid}/metadata"
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return json.load(r)["match_info"]
        except Exception:  # noqa: BLE001
            time.sleep(3 * (i + 1))
    return None


def held(items, item_id, t0, t1):
    """Owned for the whole window [t0, t1]."""
    for x in items:
        if x["item_id"] == item_id and x["game_time_s"] <= t0 and (not x.get("sold_time_s") or x["sold_time_s"] >= t1):
            return True
    return False


def analyse(m, acc):
    dm = m.get("damage_matrix") or {}
    names = dm.get("source_details", {}).get("source_name", [])
    stypes = dm.get("source_details", {}).get("stat_type", [])
    times = dm.get("sample_time_s") or []
    P = {p["player_slot"]: p for p in m["players"]}
    for d in dm.get("damage_dealers", []):
        me = P.get(d["dealer_player_slot"])
        if not me:
            continue
        series = {}
        for s in d["damage_sources"]:
            i = s["source_details_index"]
            if i < len(names) and names[i] == "upgrade_rupture" and stypes[i] == 0:
                for tp in s["damage_to_players"]:
                    tgt = P.get(tp["target_player_slot"])
                    if tgt and tgt["team"] != me["team"]:
                        # right-aligned arrays (deadsim.dmatrix): sum them per sample time, not per index
                        cur = series.setdefault(tgt["player_slot"], [0] * len(times))
                        for k in range(len(times)):
                            cur[k] += at(tp["damage"], k, len(times))
        if not series:
            continue
        for k in range(1, len(times)):
            t0, t1 = times[k - 1], times[k]
            if not held(me["items"], DECAY, t0, t1):
                continue
            grp = {True: [], False: []}
            for slot, tgt in P.items():
                if tgt["team"] == me["team"]:
                    continue
                cum = series.get(slot)
                dmg = (cum[k] - cum[k - 1]) if cum else 0
                hp = next((s["max_health"] for s in tgt["stats"] if s["time_stamp_s"] == t1), None) or \
                    (tgt["stats"][-1]["max_health"] if tgt["stats"] else None)
                if not hp:
                    continue
                if held(tgt["items"], DISPEL, t0, t1):
                    grp[True].append(dmg / hp)
                elif not any(x["item_id"] == DISPEL for x in tgt["items"] if x["game_time_s"] <= t1):
                    grp[False].append(dmg / hp)
            if grp[True] and grp[False]:   # paired window: same Decay owner, both kinds of target
                acc["with"].append(sum(grp[True]) / len(grp[True]))
                acc["without"].append(sum(grp[False]) / len(grp[False]))
                acc["windows"] += 1


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    min_badge = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    files = sorted(glob.glob(os.path.join(HERE, "..", "..", "data", "builds", "player_builds", "*.jsonl.gz")))[-days - 1:-1]
    has_decay, has_dispel = set(), set()
    for fn in files:
        for line in gzip.open(fn, "rt"):
            r = json.loads(line)
            if (r["badge"] or 0) < min_badge:
                continue
            if DECAY in r["final_items"]:
                has_decay.add(r["match_id"])
            if DISPEL in r["final_items"]:
                has_dispel.add(r["match_id"])
    ids = sorted(has_decay & has_dispel)
    random.seed(11)
    ids = random.sample(ids, min(n, len(ids)))
    acc = {"with": [], "without": [], "windows": 0}
    done = 0
    with cf.ThreadPoolExecutor(6) as ex:
        for m in ex.map(get, ids):
            if m:
                analyse(m, acc)
                done += 1
    w, wo = sum(acc["with"]), sum(acc["without"])
    ratio = w / wo if wo else None
    # bootstrap over paired windows
    random.seed(3)
    pairs = list(zip(acc["with"], acc["without"]))
    boots = []
    for _ in range(1000):
        s = [random.choice(pairs) for _ in pairs]
        b = sum(x for _, x in s)
        boots.append(sum(x for x, _ in s) / b if b else 0)
    boots.sort()
    out = {"min_badge": min_badge, "matches": done, "paired_windows": acc["windows"], "ratio": ratio,
           "ratio_90ci": [boots[50], boots[949]] if boots else None,
           "equivalent_ticks_of_12": 12 * ratio if ratio else None,
           "decay_pct_maxhp_per_window_with": w / len(pairs) if pairs else None,
           "decay_pct_maxhp_per_window_without": wo / len(pairs) if pairs else None}
    print(json.dumps(out, indent=1))
    json.dump(out, open(os.path.join(HERE, "..", "work", f"decay_vs_dispel_{min_badge}.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
