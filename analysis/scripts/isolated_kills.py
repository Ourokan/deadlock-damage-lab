"""Real 1v1 strength per hero: who wins isolated kills (no other hero death nearby) at equal net worth.

The sim's duels pit two heroes at the same net worth; the closest real thing is a kill with no other hero death
within WINDOW seconds (not a team fight) where killer and victim are within BALANCE of each other's net worth.
Per hero: share = isolated kills / (isolated kills + isolated deaths); per pair the same head to head.
Ganks (2v1 with one death) still count, so shares sit closer to 50% than true duel win rates.

Data: deadlock-api /v1/sql match_player (death times, killer slot, net worth every ~3 min), Phantom+ ranked
(match average badge >= 91), one query per UTC day (the endpoint allows ~20 queries an hour).

usage: python3 analysis/scripts/isolated_kills.py WORK_DIR FIRST_DAY LAST_DAY [--window 15] [--balance 0.1]
Writes WORK_DIR/deaths_<day>.json (cached) and analysis/out/isolated_kills.json.
"""
import argparse
import bisect
import collections
import datetime
import json
import os
import time
import urllib.parse
import urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
Q = ("SELECT match_id, player_slot, hero_id, team, net_worth, \"death_details.game_time_s\" dt, "
     "\"death_details.killer_player_slot\" ks, \"stats.time_stamp_s\" st, \"stats.net_worth\" snw "
     "FROM match_player WHERE start_time >= TIMESTAMP '{d} 00:00:00+00' "
     "AND start_time < TIMESTAMP '{d} 00:00:00+00' + INTERVAL 1 DAY "
     "AND game_mode='Normal' AND match_mode='Ranked' AND average_badge >= 91")
BUDGETS = {"all": (0, 10 ** 9), "10000": (0, 14000), "18000": (14000, 22500), "27000": (22500, 32000),
           "37000": (32000, 43000), "50000": (43000, 10 ** 9)}


def fetch(work, day):
    fn = os.path.join(work, f"deaths_{day}.json")
    if not os.path.exists(fn):
        url = "https://api.deadlock-api.com/v1/sql?" + urllib.parse.urlencode({"query": Q.format(d=day)})
        req = urllib.request.Request(url, headers={"User-Agent": "deadlock-build-sim/0.1 (research)"})
        with urllib.request.urlopen(req, timeout=300) as r:
            rows = json.load(r)
        json.dump(rows, open(fn, "w"))
        time.sleep(5)
    return json.load(open(fn))


def nw_at(p, t):
    i = bisect.bisect_left(p["st"], t)
    return p["snw"][i] if i < len(p["st"]) else p["net_worth"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("work")
    ap.add_argument("first")
    ap.add_argument("last")
    ap.add_argument("--window", type=float, default=15.0)
    ap.add_argument("--balance", type=float, default=0.1)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    day, last = datetime.date.fromisoformat(a.first), datetime.date.fromisoformat(a.last)
    matches = collections.defaultdict(dict)
    while day <= last:
        for r in fetch(a.work, day.isoformat()):
            matches[r["match_id"]].setdefault(r["player_slot"], r)   # match_player repeats some rows
        day += datetime.timedelta(days=1)
    names = {h["id"]: h["name"] for h in json.load(open(os.path.join(ROOT, "data", "game", "heroes.json")))}
    out = {b: {"pair": collections.Counter(), "kills": collections.Counter(), "deaths": collections.Counter()}
           for b in BUDGETS}
    for ps in matches.values():
        if len(ps) < 12:
            continue
        ev = sorted((t, s, k) for s, p in ps.items() for t, k in zip(p["dt"] or [], p["ks"] or []))
        times = [e[0] for e in ev]
        for t, v, k in ev:
            if k not in ps or ps[k]["team"] == ps[v]["team"]:
                continue
            if bisect.bisect_right(times, t + a.window) - bisect.bisect_left(times, t - a.window) > 1:
                continue   # another death nearby: a team fight
            nv, nk = nw_at(ps[v], t), nw_at(ps[k], t)
            if abs(nk - nv) > a.balance * max(nk, nv):
                continue
            kh, vh = ps[k]["hero_id"], ps[v]["hero_id"]
            for b, (lo, hi) in BUDGETS.items():
                if lo <= nv < hi:
                    o = out[b]
                    o["pair"][f"{kh},{vh}"] += 1
                    o["kills"][kh] += 1
                    o["deaths"][vh] += 1
    res = {"meta": {"what": "isolated kills (no other hero death within window s), killer and victim net worth within "
                            "balance of each other, Phantom+ ranked; share = kills / (kills + deaths)",
                    "days": [a.first, a.last], "matches": len(matches), "window_s": a.window, "balance": a.balance,
                    "budgets": "victim net worth band per budget: " + json.dumps(BUDGETS)},
           "budgets": {}}
    for b, o in out.items():
        heroes = {}
        for h in set(o["kills"]) | set(o["deaths"]):
            k, d = o["kills"][h], o["deaths"][h]
            heroes[str(h)] = {"name": names.get(h, str(h)), "kills": k, "deaths": d, "share": round(k / (k + d), 4)}
        res["budgets"][b] = {"heroes": heroes, "pairs": dict(o["pair"])}
    os.makedirs(os.path.join(ROOT, "analysis", "out"), exist_ok=True)
    json.dump(res, open(os.path.join(ROOT, "analysis", "out", "isolated_kills.json"), "w"), indent=1)
    for r in sorted(res["budgets"]["all"]["heroes"].values(), key=lambda r: -r["share"]):
        print(f"{r['name']:15s} {r['share']:.3f}  ({r['kills']} / {r['deaths']})")


if __name__ == "__main__":
    main()
