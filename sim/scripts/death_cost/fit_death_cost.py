"""What a death costs in real Phantom+ games, for the overall score's death cost (damage/scripts/overall_search.py
death_value).

The overall score is damage per fight; a build that dies more often also spends more of the game dead: respawn
(grows from ~9 s at 0-5k net worth to ~85 s from 40k), the walk back, and the souls its team gives away. Measured:

- respawn_s by net worth, made non-decreasing (deaths of 600 Phantom+ matches, metadata death_details[].death_duration_s, fetched by
  fetch_deaths.py; the victim's net worth at the death from its stats snapshots, linear between them);
- soul rate (own net worth gain per s) and kill bounty (the killing team's net worth gain per death of the other
  team), by the net worth bin at a stats window's start: least squares over 180 / 300 s stats windows of the gain on
  the deaths in the window, with game-time bins and net worth as controls (the victim's own loss per death is ~its
  soul rate x respawn: no souls lost besides the farm missed);
- per phase (as overall_search.game_phase), from the 260 Phantom+ replays of sim/scripts/fight_length (hero-vs-hero
  DamageEvent): engagements (a fighter's pair fights of >= 4 hits both ways, merged when they overlap or follow
  within 5 s, as fit_item_use.py), deaths per engagement, alive seconds per engagement (the fight cycle) and the
  walk back (mean time from respawn to the next engagement minus the mean wait to the next engagement from a random
  moment between two engagements, E[g^2] / 2 E[g]);
- per hero deaths per engagement over all phases relative to the pool's (same phase mix), shrunk toward 1 with
  SHRINK engagements of pool rate.

usage: python3 -I fit_death_cost.py [--raw DIR] [--deaths FILE] [--write]
"""
import argparse
import collections
import glob
import gzip
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(HERE, "..", "fight_length"))
import fit_length as FL  # noqa: E402

import numpy as np  # noqa: E402

PHASES = (("lane", 0, 10000), ("mid", 10000, 27001), ("late", 27001, float("inf")))   # overall_search.game_phase
NW_STEP = 2500
NW_BINS = (0, 5000, 10000, 18000, 27000, 37000)    # soul rate / bounty bins (lower bounds)
SHRINK = 300   # engagements


def phase(nw):
    return next(n for n, lo, hi in PHASES if lo <= nw < hi)


def respawn(ms):
    """Mean respawn s per NW_STEP net worth bin (bins with >= 30 deaths)."""
    b = collections.defaultdict(list)
    for m in ms:
        for p in m["players"]:
            if not p["stats"]:
                continue
            for d in p["deaths"]:
                if d["respawn_s"]:
                    b[int(FL.nw_at(p["stats"], d["t"]) // NW_STEP)].append(d["respawn_s"])
    out = [[k * NW_STEP + NW_STEP / 2, statistics.mean(v), len(v)] for k, v in sorted(b.items()) if len(v) >= 30]
    # the game's timer only grows with time: pool adjacent bins that dip (pool-adjacent-violators, death-weighted)
    blocks = []
    for x, y, n in out:
        blocks.append([[x], y, n])
        while len(blocks) > 1 and blocks[-2][1] > blocks[-1][1]:
            (xa, ya, na), (xb, yb, nb) = blocks[-2], blocks[-1]
            blocks[-2:] = [[xa + xb, (ya * na + yb * nb) / (na + nb), na + nb]]
    return [[x, round(y, 1), n] for xs, y, n in blocks for x in xs]


def souls(ms):
    """Per net worth bin: own soul rate (per s) and the killing team's gain per death of the other team."""
    own, team = [], []
    for m in ms:
        sides = collections.defaultdict(list)
        for p in m["players"]:
            s = p["stats"]
            sides[p["team"]].append(s)
            for a, b in zip(s, s[1:]):
                dt = b["time_stamp_s"] - a["time_stamp_s"]
                if dt in (180, 300):
                    own.append((a["net_worth"], (b["net_worth"] - a["net_worth"]) / dt, a["time_stamp_s"]))
        if len(sides) != 2 or any(len(v) != 6 for v in sides.values()):
            continue
        n = min(len(s) for v in sides.values() for s in v)
        for t, o in (tuple(sides), tuple(sides)[::-1]):
            for i in range(n - 1):
                a, b = sides[t][0][i]["time_stamp_s"], sides[t][0][i + 1]["time_stamp_s"]
                if b - a not in (180, 300):
                    continue

                def tot(side, j, k):
                    return sum(s[j][k] for s in sides[side])
                team.append((tot(t, i, "net_worth") / 6, (tot(t, i + 1, "net_worth") - tot(t, i, "net_worth")) / (b - a),
                             (tot(o, i + 1, "deaths") - tot(o, i, "deaths")) / (b - a),
                             (tot(t, i + 1, "deaths") - tot(t, i, "deaths")) / (b - a), a))
    own, team = np.array(own), np.array(team)
    out = []
    for k, lo in enumerate(NW_BINS):
        hi = NW_BINS[k + 1] if k + 1 < len(NW_BINS) else 1e9
        rate = own[(own[:, 0] >= lo) & (own[:, 0] < hi), 1].mean()
        r = team[(team[:, 0] >= lo) & (team[:, 0] < hi)]
        tb = np.floor(r[:, 4] / 300)
        x = np.column_stack([np.ones(len(r)), r[:, 2], r[:, 3], r[:, 0] / 1000]
                            + [(tb == v).astype(float) for v in sorted(set(tb))[1:]])
        beta = np.linalg.lstsq(x, r[:, 1], rcond=None)[0]
        out.append({"nw": lo, "soul_rate": round(float(rate), 2), "bounty": round(float(beta[1])),
                    "windows": int(len(r))})
    return out


def replays(raw, deaths_meta):
    files = sorted(glob.glob(os.path.join(raw, "*.ndjson.gz")))
    sample = FL.load_sample(os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz"),
                            {os.path.basename(f).split(".")[0] for f in files})
    agg = collections.defaultdict(lambda: collections.defaultdict(float))
    hero_agg = collections.defaultdict(lambda: collections.defaultdict(float))
    after, gaps = collections.defaultdict(list), collections.defaultdict(list)
    used = 0
    for fn in files:
        mid = os.path.basename(fn).split(".")[0]
        m, md = sample.get(mid), deaths_meta.get(mid)
        if not m or not md:
            continue
        hero, ev = FL.read(fn)
        off = FL.clock_offset(ev, hero, m)
        if off is None:
            continue
        used += 1
        byh = {p["hero_id"]: p for p in m["players"]}
        mdh = {p["hero_id"]: p for p in md["players"]}
        pairs = collections.defaultdict(list)
        deaths, dead = collections.defaultdict(list), set()
        for e in ev:
            t, a, v, hp = e[:4]
            pa, pv = byh.get(hero.get(a)), byh.get(hero.get(v))
            if pa is None or pv is None or pa["team"] == pv["team"]:
                continue
            pairs[min(a, v), max(a, v)].append(e)
            if hp <= 0 and v not in dead:
                dead.add(v)
                deaths[v].append(t)
            elif hp > 0:
                dead.discard(v)
        iv = collections.defaultdict(list)
        for (x, y), es in pairs.items():
            runs = []
            for e in es:
                if not runs or e[0] - runs[-1][-1][0] > FL.GAP_S:
                    runs.append([])
                runs[-1].append(e)
            for f in runs:
                if len(f) < FL.MIN_HITS or len({(e[1], e[2]) for e in f}) < 2:
                    continue
                iv[x].append((f[0][0], f[-1][0]))
                iv[y].append((f[0][0], f[-1][0]))
        for pawn, ivs in iv.items():
            h = hero.get(pawn)
            p, ps = mdh.get(h), byh.get(h)
            if p is None or ps is None or not ps["stats"]:
                continue
            ivs.sort()
            eng = []
            for a, b in ivs:
                if eng and a - eng[-1][1] <= FL.GAP_S:
                    eng[-1][1] = max(eng[-1][1], b)
                else:
                    eng.append([a, b])
            dl = []
            for td in deaths[pawn]:
                g = td - off(td)
                d = min(p["deaths"], key=lambda d: abs(d["t"] - g)) if p["deaths"] else None
                if d and abs(d["t"] - g) < 3 and d["respawn_s"]:
                    dl.append((td, d["respawn_s"], g))
            for a, _ in eng:
                ph = phase(FL.nw_at(ps["stats"], a - off(a)))
                agg[ph]["engagements"] += 1
                hero_agg[h][ph + "_eng"] += 1
            for td, r, g in dl:
                ph = phase(FL.nw_at(ps["stats"], g))
                agg[ph]["deaths"] += 1
                hero_agg[h][ph + "_deaths"] += 1
                nxt = next((a for a, _ in eng if a > td + r), None)
                if nxt is not None:
                    after[ph].append(nxt - td - r)
            dead_iv = [(td, td + r) for td, r, _ in dl]
            for k in range(len(eng) - 1):
                ga, gb = eng[k][1], eng[k + 1][0]
                if not any(ga <= x < gb for x, _ in dead_iv):
                    gaps[phase(FL.nw_at(ps["stats"], ga - off(ga)))].append(gb - ga)
            for gt in range(0, md["duration_s"], 10):
                rt = gt + off(gt + 60)
                if not any(x <= rt < y for x, y in dead_iv):
                    agg[phase(FL.nw_at(ps["stats"], gt))]["alive_s"] += 10
    out = {}
    for ph, _, _ in PHASES:
        a, g = agg[ph], gaps[ph]
        wait = sum(x * x for x in g) / (2 * sum(g))
        out[ph] = {"engagements": int(a["engagements"]), "deaths": int(a["deaths"]),
                   "deaths_per_engagement": round(a["deaths"] / a["engagements"], 4),
                   "alive_s_per_engagement": round(a["alive_s"] / a["engagements"], 1),
                   "respawn_to_engagement_s": round(statistics.mean(after[ph]), 1),
                   "wait_to_engagement_s": round(wait, 1),
                   "walk_back_s": round(max(0.0, statistics.mean(after[ph]) - wait), 1)}
    heroes = {}
    for h, a in hero_agg.items():
        exp = sum(a[ph + "_eng"] * out[ph]["deaths_per_engagement"] for ph, _, _ in PHASES)
        d = sum(a[ph + "_deaths"] for ph, _, _ in PHASES)
        e = sum(a[ph + "_eng"] for ph, _, _ in PHASES)
        rate = exp / max(1, e)
        heroes[str(h)] = {"ratio": round((d + SHRINK * rate) / (exp + SHRINK * rate), 3), "deaths": int(d),
                          "engagements": int(e)}
    return used, out, heroes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="/mnt/project-files/analysis/work/fight_length/raw")
    ap.add_argument("--deaths", default="/mnt/project-files/analysis/work/death_cost/deaths.jsonl.gz")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    ms = [json.loads(line) for line in gzip.open(a.deaths)]
    res = respawn(ms)
    so = souls(ms)
    used, phases, heroes = replays(a.raw, {str(m["match_id"]): m for m in ms})
    print(f"{len(ms)} matches with death details, {used} replays")
    print("respawn s by net worth: " + " ".join(f"{int(nw // 1000)}k {r:.0f}" for nw, r, _ in res[::2]))
    for row in so:
        print(f"from {row['nw']:>5}: soul rate {row['soul_rate']:.1f}/s, kill bounty {row['bounty']} souls "
              f"(= {row['bounty'] / row['soul_rate']:.0f} s of farm), {row['windows']} windows")
    for ph, row in phases.items():
        print(f"{ph:5s} " + ", ".join(f"{k} {v}" for k, v in row.items()))
    hr = sorted(heroes.items(), key=lambda x: x[1]["ratio"])
    print("hero death ratio low: " + ", ".join(f"{h} {v['ratio']}" for h, v in hr[:5])
          + "; high: " + ", ".join(f"{h} {v['ratio']}" for h, v in hr[-5:]))
    if a.write:
        out = {"source": f"{len(ms)} Phantom+ matches' death details (fetch_deaths.py) and {used} of their replays "
                         "(sim/scripts/fight_length raw), scripts/death_cost/fit_death_cost.py",
               "respawn_s": [[nw, r] for nw, r, _ in res], "souls": so, "phases": phases, "heroes": heroes,
               "note": "respawn_s: [net worth, mean respawn s]; souls: per net worth bin (lower bound) own soul gain "
                       "per s and the killing team's net worth gain per death; phases: engagement = a fighter's pair "
                       "fights merged within 5 s; heroes: deaths per engagement / the pool's at the same phase mix, "
                       "shrunk"}
        with open(os.path.join(ROOT, "data", "death_cost.json"), "w") as f:
            json.dump(out, f, indent=1)
            f.write("\n")


if __name__ == "__main__":
    main()
