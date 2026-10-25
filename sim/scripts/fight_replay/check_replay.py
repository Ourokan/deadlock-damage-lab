"""How close the site's fight replay (web/replay.js + bridge.replay) comes to the real fights.

Fetches recent Phantom+ matches (or reads saved /v1/matches/{id}/metadata JSONs), finds their fights with the site's
own detection (detect.cjs, needs node), replays each with everyone's real items, souls, ability upgrades, aim,
starting health and distance, and compares with what really happened: deaths, health lost, and which side came out
ahead.

usage: python3 -I check_replay.py <repo dir> <metadata dir> [n_fetch=0] [mode=site]
mode: site (what the page sends: real arrival, survivors leave after their last fighting second, each hero shoots its
nearest enemy), all0 (everyone from the start to the end, focus the weakest: the first version), join (arrival only),
leave (arrival and leaving, focus the weakest), hazard (as site but leaving at the fitted flat rate, not real times)
"""
import concurrent.futures as cf
import json
import os
import statistics as st
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.abspath(sys.argv[1])
sys.path[:0] = [os.path.join(ROOT, "sim"), os.path.join(ROOT, "damage"), os.path.join(ROOT, "web")]
import bridge  # noqa: E402
from deadsim.data import game  # noqa: E402

API = "https://api.deadlock-api.com/v1/matches"
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}
HERE = os.path.dirname(os.path.abspath(__file__))
RNG = __import__("random").Random(7)
LEAVE_RATE = 0.016   # real early leaves per hero-second of fighting, flat across health (fit_disengage.py)


def fetch(out, n):
    now = int(time.time())
    url = (f"{API}/metadata?limit={n}&min_average_badge=91&min_duration_s=1200&order_by=match_id&order_direction=desc"
           f"&min_unix_timestamp={now - 3 * 86400}&max_unix_timestamp={now - 7200}")
    ids = [m["match_id"] for m in json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))]

    def one(mid):
        fn = os.path.join(out, f"{mid}.json")
        if not os.path.exists(fn):
            body = urllib.request.urlopen(urllib.request.Request(f"{API}/{mid}/metadata", headers=UA), timeout=120).read()
            open(fn, "wb").write(body)
    with cf.ThreadPoolExecutor(6) as ex:
        list(ex.map(one, ids))


def corr(x, y):
    mx, my = st.mean(x), st.mean(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y)) ** .5


def main():
    meta = sys.argv[2]
    mode = sys.argv[4] if len(sys.argv) > 4 else "site"
    os.makedirs(meta, exist_ok=True)
    if len(sys.argv) > 3 and int(sys.argv[3]):
        fetch(meta, int(sys.argv[3]))
    G = game()
    T = dict(fights=0, heroes=0, real_deaths=0, sim_deaths=0, both_dead=0, one_sided=0, same_side=0, other_side=0)
    sw, lost, hero = [], [], []
    for fn in sorted(f for f in os.listdir(meta) if f.endswith(".json")):
        mi = json.load(open(os.path.join(meta, fn))).get("match_info") or {}
        if not mi.get("match_paths"):
            continue
        det = json.loads(subprocess.run(["node", os.path.join(HERE, "detect.cjs"), os.path.join(ROOT, "web/replay.js"),
                                         os.path.join(meta, fn)], capture_output=True, text=True, check=True).stdout)
        P = {p["player_slot"]: p for p in mi["players"]}
        names = {c["id"]: c["name"] for c in mi.get("custom_user_stats") or []}

        def aim(p):
            c = {names.get(x["id"], x["id"]): x["value"] for x in (p["stats"][-1].get("custom_user_stats") or [])}
            sh, h = c.get("Enemy Hero Accuracy##Shots", 0), c.get("Enemy Hero Accuracy##Hits", 0)
            return (h / sh, c.get("Enemy Hero Accuracy##Headshots", 0) / h) if sh >= 100 and h > 0 else (None, None)

        def nw(p, t):   # as match.js netWorthAt
            pts = [(0, 0)] + [(s["time_stamp_s"], s["net_worth"]) for s in p["stats"]]
            for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
                if t1 >= t:
                    return v0 + (v1 - v0) * (t - t0) / max(1, t1 - t0)
            return p["net_worth"]

        def member(s, F):   # as replay.js rpMember
            p, items, ab = P[s], [], []
            for x in p["items"]:
                if x["game_time_s"] > F["t0"]:
                    continue
                it = G.items.get(x["item_id"]) if isinstance(G.items, dict) else None
                if it is not None and getattr(it, "cost", 0):
                    if (not x["sold_time_s"] or x["sold_time_s"] > F["t0"]) and x["item_id"] not in items:
                        items.append(x["item_id"])
                else:
                    ab.append(x["item_id"])
            a, h = aim(p)
            return dict(hero=p["hero_id"], items=items, souls=nw(p, F["t0"]), hp=F["hp0"][str(s)], abilities=ab,
                        accuracy=a, headshot=h)

        for F in det["fights"]:
            ok = [s for s in F["players"] if P[s]["hero_id"] in G.heroes]
            A = [s for s in ok if ok and P[s]["team"] == P[ok[0]]["team"]]
            B = [s for s in ok if s not in A]
            if not A or not B:
                continue
            dead = {d["slot"] for d in F["deaths"]}
            mem = {s: member(s, F) for s in A + B}
            for s in A + B:   # timing, as replay.js rpMember in mode "site"
                foes = B if s in A else A
                if mode in ("site", "join", "leave", "hazard"):
                    mem[s]["join"] = F["join"][str(s)]
                if mode in ("site", "leave") and s not in dead:
                    mem[s]["leave"] = F["last"][str(s)] + 1
                if mode == "hazard":   # fitted flat early-leave rate (fit_disengage.py) instead of the real leave times
                    mem[s]["leave"] = mem[s]["join"] + RNG.expovariate(LEAVE_RATE)
                if mode in ("site", "hazard"):
                    mem[s]["targets"] = [foes.index(x) if x in foes else None for x in F["near"][str(s)]]
            req = dict(a=[mem[s] for s in A], b=[mem[s] for s in B], distance=max(3, F["dist"]),
                       max_time=min(45, max(4, F["t1"] - F["t0"] + 1)))
            r = json.loads(bridge.replay(json.dumps(req)))
            rows = dict(zip(A + B, r["fighters"]))
            real = {d["slot"] for d in F["deaths"]} & set(A + B)
            sim = {s for s, x in rows.items() if not x["alive"]}
            T["fights"] += 1
            T["heroes"] += len(rows)
            T["real_deaths"] += len(real)
            T["sim_deaths"] += len(sim)
            T["both_dead"] += len(real & sim)
            rl = {s: (F["hp0"][str(s)] - F["hp1"][str(s)]) * x["max_hp"] for s, x in rows.items()}
            sl = {s: x["start_hp"] - (x["hp"] if x["alive"] else 0) for s, x in rows.items()}
            sw.append((sum(rl[s] for s in B) - sum(rl[s] for s in A), sum(sl[s] for s in B) - sum(sl[s] for s in A)))
            lost.append((sum(rl.values()), sum(sl.values())))
            hero.extend((rl[s], sl[s]) for s in rows)
            ra, rb = len(real & set(A)), len(real & set(B))
            if (ra > 0) != (rb > 0):
                sa, sb = len(sim & set(A)), len(sim & set(B))
                T["one_sided"] += 1
                T["same_side"] += (sa - sb) * (ra - rb) > 0
                T["other_side"] += (sa - sb) * (ra - rb) < 0
    print(json.dumps(T))
    print(f"sim deaths / real {T['sim_deaths'] / max(1, T['real_deaths']):.2f}; real deaths the sim also has "
          f"{T['both_dead'] / max(1, T['real_deaths']):.2f}; sim deaths that are real {T['both_dead'] / max(1, T['sim_deaths']):.2f}; "
          f"F1 {2 * T['both_dead'] / max(1, T['sim_deaths'] + T['real_deaths']):.3f}")
    print(f"fights where only one side lost heroes: sim kills more on the same side {T['same_side']}, on the other "
          f"{T['other_side']}, even {T['one_sided'] - T['same_side'] - T['other_side']}")
    print(f"health lost real / sim {sum(x[0] for x in lost) / sum(x[1] for x in lost):.2f}; correlation per fight "
          f"{corr(*zip(*lost)):.2f}, per hero {corr(*zip(*hero)):.2f}; HP swing correlation {corr(*zip(*sw)):.2f}, "
          f"same sign {sum((a > 0) == (b > 0) for a, b in sw) / len(sw):.2f}")


if __name__ == "__main__":
    main()
