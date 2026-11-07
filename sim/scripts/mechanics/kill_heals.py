"""Real Healbane kill heals per second of hero combat, by net worth (validation/kill_heals.md, data/kill_heals.json).

Healbane heals its holder HealOnKill (170 + 3 per boon) whenever an enemy hero dies under its anti-heal, whoever
killed it. The 1v1 duel only has its own kills (the immortal enemy's refills), so it gave the heal a few times less
often than real holders get it.

fetch: full metadata of post-hotfix Phantom+ matches with a Healbane holder (match ids from the fight_rate_post stat
timelines), keeping the Healbane rows of the damage matrix, items and stat timelines (~4 matches/s).
measure: every damage-matrix sample window (180 s) the holder held Healbane for: its Healbane self-heal (stat type 1)
/ the boon-scaled HealOnKill at the window's net worth = kill heals, per minute held, / the game phase's real combat
share (sim/data/sustain.json combat_share, the same convention as healbane_prevented_per_combat_s) = kill heals per
combat second. Per 10k net worth bin, both match-id halves and pooled, with the holder's own kills and the enemy
team's deaths for context. Writes data/kill_heals.json with --write.

usage: python3 -I kill_heals.py fetch <out dir> [n]
       python3 -I kill_heals.py measure [match dir] [--write]
       (default dir: project folder analysis/work/kill_heals)
"""
import collections
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
SIM = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, SIM)
from deadsim.data import game  # noqa: E402
from deadsim.dmatrix import win  # noqa: E402

HB = 2603935618
DIR = "/mnt/project-files/analysis/work/kill_heals"
TIMELINES = "/mnt/project-files/analysis/work/fight_rate_post"
STAT_KEYS = ("time_stamp_s", "net_worth", "kills", "deaths", "assists")
PHASES = (("lane", 540), ("mid", 1500), ("late", 1e9))   # fit_sustain.py PHASES
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}
OUT = os.path.join(SIM, "data", "kill_heals.json")


def fetch(out, n):
    os.makedirs(out, exist_ok=True)
    ids = []
    for path in sorted(glob.glob(os.path.join(TIMELINES, "*.jsonl.gz"))):
        for line in gzip.open(path, "rt"):
            m = json.loads(line)
            if any(it[0] == HB for p in m["players"] for it in p["items"]):
                ids.append(m["match_id"])
    random.seed(7)
    random.shuffle(ids)

    def get(mid):
        fn = os.path.join(out, f"{mid}.json.gz")
        if os.path.exists(fn):
            return 1
        for i in range(4):
            try:
                url = f"https://api.deadlock-api.com/v1/matches/{mid}/metadata"
                with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                    m = json.load(r)["match_info"]
                break
            except Exception:
                time.sleep(3 * (i + 1))
        else:
            return 0
        dm = m.get("damage_matrix") or {}
        names = dm.get("source_details", {}).get("source_name", [])
        stypes = dm.get("source_details", {}).get("stat_type", [])
        heal = {}
        for d in dm.get("damage_dealers", []):
            for s in d["damage_sources"]:
                i = s["source_details_index"]
                if i < len(names) and names[i] == "upgrade_healbane":
                    for tp in s["damage_to_players"]:
                        heal.setdefault(str(d["dealer_player_slot"]), []).append(
                            [stypes[i], tp["target_player_slot"], tp["damage"]])
        slim = {"match_id": mid, "duration_s": m["duration_s"], "times": dm.get("sample_time_s", []), "heal": heal,
                "players": [{"slot": p["player_slot"], "team": p["team"], "hero": p["hero_id"],
                             "items": [[it["item_id"], it["game_time_s"], it.get("sold_time_s", 0)]
                                       for it in p.get("items", [])],
                             "stats": [[s.get(k) or 0 for k in STAT_KEYS] for s in p.get("stats") or []]}
                            for p in m["players"]]}
        with gzip.open(fn, "wt") as f:
            json.dump(slim, f)
        return 1

    with cf.ThreadPoolExecutor(4) as ex:
        ok = sum(ex.map(get, ids[:n]))
    print(f"{ok} of {min(n, len(ids))} matches")


def interp(st, t):
    """Stat row linearly interpolated at time t (timelines step 180 s, then 300 s; damage-matrix samples 180 s)."""
    if t == 0:
        return [0.0] * len(STAT_KEYS)
    for a, b in zip(st, st[1:]):
        if a[0] <= t <= b[0]:
            f = (t - a[0]) / max(1, b[0] - a[0])
            return [x + f * (y - x) for x, y in zip(a, b)]
    return None


def measure(d, write):
    G = game()
    with open(os.path.join(SIM, "data", "sustain.json")) as f:
        share = json.load(f)["combat_share"]
    # (net worth bin, half) -> kill heals, heal HP, minutes held, combat minutes, holder kills, enemy deaths
    acc = collections.defaultdict(lambda: [0.0] * 6)
    n_match, holders = 0, 0
    for fn in sorted(glob.glob(os.path.join(d, "*.json.gz"))):
        m = json.load(gzip.open(fn, "rt"))
        times = m["times"]
        if not times:
            continue
        n_match += 1
        half = m["match_id"] % 2
        for p in m["players"]:
            iv = [(t0, ts or 1e9) for iid, t0, ts in p["items"] if iid == HB and t0 > 0]
            if not iv:
                continue
            holders += 1
            slot = str(p["slot"])
            rows = [r for r in m["heal"].get(slot, []) if r[0] == 1 and str(r[1]) == slot]
            enemies = [q for q in m["players"] if q["team"] != p["team"]]
            hero = G.hero(p["hero"])
            for k, t1 in enumerate(times):
                t0 = times[k - 1] if k else 0
                if not any(a <= t0 and b >= t1 for a, b in iv):
                    continue
                a, b = interp(p["stats"], t0), interp(p["stats"], t1)
                if a is None or b is None:
                    continue
                nw = (a[1] + b[1]) / 2
                boons = max(0, G.level_for_souls(hero, max(0.0, nw - 600)) - 1)
                hp = sum(win(r[2], k, len(times)) for r in rows)
                ed = 0.0
                for q in enemies:
                    qa, qb = interp(q["stats"], t0), interp(q["stats"], t1)
                    if qa is not None and qb is not None:
                        ed += qb[3] - qa[3]
                mins = (t1 - t0) / 60
                ph = next(n for n, hi in PHASES if t0 < hi)
                r = acc[(int(min(60000, nw // 10000 * 10000)), half)]
                r[0] += hp / (170 + 3 * boons)
                r[1] += hp
                r[2] += mins
                r[3] += mins * share[ph]
                r[4] += b[2] - a[2]
                r[5] += ed
    pooled = collections.defaultdict(lambda: [0.0] * 6)
    for (nb, _), r in acc.items():
        pooled[nb] = [x + y for x, y in zip(pooled[nb], r)]
    print(f"{n_match} matches, {holders} Healbane holders")
    print("net worth  kill heals/combat s  (half A / half B)  per min held  HP/min  own kills/min  enemy deaths/min  "
          "heals per enemy death  minutes")
    curve = []
    for nb, r in sorted(pooled.items()):
        if r[2] < 100:
            continue
        rate = r[0] / (r[3] * 60)
        ha, hb_ = (acc[(nb, h)][0] / max(1e-9, acc[(nb, h)][3] * 60) for h in (0, 1))
        print(f"  {nb:>6}+  {rate:.4f}  ({ha:.4f} / {hb_:.4f})  {r[0] / r[2]:.3f}  {r[1] / r[2]:6.1f}  "
              f"{r[4] / r[2]:.3f}  {r[5] / r[2]:.3f}  {r[0] / max(1, r[5]):.3f}  {r[2]:.0f}")
        curve.append([nb + 5000, round(rate, 4)])
    if write:
        with open(OUT, "w") as f:
            json.dump({"source": f"{n_match} post-hotfix Phantom+ matches, {holders} Healbane holders "
                                 "(sim/scripts/mechanics/kill_heals.py)",
                       "note": "kill heals per second of hero combat by net worth (bin centre, rate); Healbane's "
                               "self-heal / boon-scaled HealOnKill, per minute held / sustain.json combat_share",
                       "upgrade_healbane": curve}, f, indent=1)
        print(f"wrote {OUT}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "fetch":
        fetch(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 800)
        return
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    measure(args[0] if args else DIR, "--write" in sys.argv)


if __name__ == "__main__":
    main()
