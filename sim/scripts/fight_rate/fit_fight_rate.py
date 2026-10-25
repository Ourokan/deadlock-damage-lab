"""Fit how tank items' extra health is used in real Phantom+ games, for the overall score
(damage/scripts/overall_search.py death_rate_value, and the opt-in fight_value).

Question (2026-10-25, after the death cost thread): real tank-item holders die about as often per match as
non-holders, so where does their extra health go? Each player's stat interval (fetch_rates.py, ~180-300 s
snapshots) gives damage dealt to heroes, damage taken, deaths and kills + assists per minute, the net worth and max
health at its start and the items held through it.

1. hp_elasticity per game phase (overall_search.game_phase: lane < 10k, mid 10-27k, late > 27k net worth): within a
   stratum (hero, net worth // 2500, start time // 300 s), the least squares slope of each rate / stratum mean on
   log max health, pooled over strata; SE by jackknife over 10 match groups (match_id % 10).
2. Item tables per search budget (BUDGETS, intervals starting at 0.75-1.35x the budget's net worth): holders vs
   non-holders of each item at the same stratum (real_rates.Strata), ratios and z.

Writes sim/data/fight_rate.json and sim/validation/fight_rate.md. Static snapshot (the timelines live in the shared
folder, CI can't refit it). ~10 min, ~3 GB.

usage: python3 -I fit_fight_rate.py [--src DIR]
"""
import argparse
import glob
import gzip
import json
import math
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import real_rates as R  # noqa: E402

ROOT = R.ROOT
OUT = os.path.join(ROOT, "sim", "data", "fight_rate.json")
MD = os.path.join(ROOT, "sim", "validation", "fight_rate.md")
PHASES = {"lane": (0, 10000), "mid": (10000, 27001), "late": (27001, 10 ** 9)}
KEYS = ("taken", "dealt", "deaths", "ka")
GROUPS = 10
BUDGETS = (10000, 18000, 27000, 37000, 50000)
BAND = (0.75, 1.35)
MIN_HOLDERS = 300


def phase_of(nw):
    return next(p for p, (lo, hi) in PHASES.items() if lo <= nw < hi)


class Elasticity:
    """Sufficient sums per (stratum, match group) for the within-stratum slope of rate / stratum mean on log hp."""

    def __init__(self):
        self.s = defaultdict(lambda: [[0, 0.0, 0.0] + [0.0, 0.0] * len(KEYS) for _ in range(GROUPS)])
        self.n = 0

    def add(self, stratum, group, x, v):
        self.n += 1
        a = self.s[stratum][group]
        a[0] += 1
        a[1] += x
        a[2] += x * x
        for q, k in enumerate(KEYS):
            a[3 + 2 * q] += v[k]
            a[4 + 2 * q] += x * v[k]

    def slope(self, q, skip=None):
        num = den = 0.0
        for gs in self.s.values():
            t = [sum(g[j] for k, g in enumerate(gs) if k != skip) for j in range(len(gs[0]))]
            n = t[0]
            if n < 5:
                continue
            my = t[3 + 2 * q] / n
            if my <= 0:
                continue
            mx = t[1] / n
            den += t[2] - n * mx * mx
            num += (t[4 + 2 * q] - n * mx * my) / my
        return num / den if den else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=R.SRC)
    a = ap.parse_args()
    items = R.shop_items()
    el = {p: Elasticity() for p in PHASES}
    bands = {b: R.Strata() for b in BUDGETS}
    n_m = 0
    for p in sorted(glob.glob(os.path.join(a.src, "*.jsonl.gz"))):
        with gzip.open(p, "rt") as f:
            for line in f:
                m = json.loads(line)
                if m.get("mode") not in (None, "Normal", 1):
                    continue
                n_m += 1
                grp = m["match_id"] % GROUPS
                for pl in m["players"]:
                    ab = pl.get("abandon_s") or 0
                    st = pl["stats"]
                    for s0, s1 in zip(st, st[1:]):
                        mins = (s1[0] - s0[0]) / 60
                        if mins < R.MIN_MIN or (ab and ab < s1[0]) or s0[7] <= 0:
                            continue
                        v = {"dealt": (s1[2] - s0[2]) / mins, "taken": (s1[3] - s0[3]) / mins,
                             "deaths": (s1[5] - s0[5]) / mins, "ka": (s1[4] + s1[6] - s0[4] - s0[6]) / mins}
                        el[phase_of(s0[1])].add((pl["hero_id"], s0[1] // R.NW_BIN, s0[0] // R.T_BIN), grp,
                                                math.log(s0[7]), v)
                        held, part = R.held_sets(pl["items"], items, s0[0], s1[0])
                        for b, strata in bands.items():
                            if BAND[0] * b <= s0[1] < BAND[1] * b:
                                strata.add((pl["hero_id"], s0[1], s0[0], mins, v, held, part))
    elas = {}
    for ph, e in el.items():
        elas[ph] = {"intervals": e.n}
        for q, k in enumerate(KEYS):
            full = e.slope(q)
            jk = [e.slope(q, g) for g in range(GROUPS)]
            mj = sum(jk) / GROUPS
            elas[ph][k] = [round(full, 4), round(math.sqrt((GROUPS - 1) / GROUPS * sum((x - mj) ** 2 for x in jk)), 4)]
    tables = {}
    for b, strata in bands.items():
        t = {}
        for i, c in strata.count.items():
            if c < MIN_HOLDERS:
                continue
            e = strata.compare(i)
            if e and e["n"] >= MIN_HOLDERS:
                t[items[i]["name"]] = {"slot": items[i].get("slot"), "holders": e["n"],
                                       **{k: [round(e[k]["ratio"], 4), round(e[k]["z"], 1)] for k in KEYS}}
        tables[str(b)] = {"nw": [int(BAND[0] * b), int(BAND[1] * b)], "intervals": strata.n, "items": t}
    res = {
        "_note": ("Real Phantom+ stat timelines (sim/scripts/fight_rate/fetch_rates.py), patch 09-29-2026. "
                  "hp_elasticity: d log(damage taken per minute) / d log(max health) at the same hero, net worth "
                  "and game time, per game phase (overall_search.game_phase; opt-in fight_value). items[budget]: "
                  "holders / non-holders ratio [ratio, z] of each per-minute rate at the same hero, net worth and "
                  "game time (deaths used by overall_search.death_rate_value). Static snapshot: refit with "
                  "sim/scripts/fight_rate/fit_fight_rate.py after fetching new timelines."),
        "matches": n_m,
        "hp_elasticity": {ph: elas[ph]["taken"][0] for ph in PHASES},
        "elasticities": elas,
        "items": tables,
    }
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    write_md(res)
    print(json.dumps(elas, indent=1))


def write_md(res):
    L = ["# Fight rate: where tank items' extra health goes (Phantom+)", "",
         f"{res['matches']:,} Phantom+ matches (patch 09-29-2026, 2026-09-30 to 2026-10-24), each player's stat "
         "snapshots every ~3-5 min (sim/scripts/fight_rate/fetch_rates.py, fit_fight_rate.py). Per interval: damage "
         "dealt to heroes, damage taken, deaths and kills + assists per minute.", "",
         "## Max health elasticity", "",
         "Within (hero, net worth // 2500, game time // 300 s): % change of each rate per % more max health "
         "(SE: jackknife over 10 match groups).", "",
         "| Phase | Intervals | Damage taken / min | Damage dealt / min | Deaths / min | Kills + assists / min |",
         "|---|---|---|---|---|---|"]
    for ph, e in res["elasticities"].items():
        L.append(f"| {ph} | {e['intervals']:,} | " + " | ".join(f"{e[k][0]:+.2f} ± {e[k][1]:.2f}" for k in KEYS) + " |")
    L += ["", "More max health is spent, not banked: players with more health take more damage per minute (more or "
          "longer fights) and join more kills, while dealing about the same damage per minute at the same net worth "
          "(the souls went into health instead of damage).", ""]
    for b, t in res["items"].items():
        L += [f"## Item holders vs non-holders, {t['nw'][0]:,}-{t['nw'][1]:,} net worth (budget {int(b):,})", "",
              f"{t['intervals']:,} intervals; ratio holders / non-holders at the same hero, net worth and game time "
              f"(z in brackets), items held through the whole interval by >= {MIN_HOLDERS}. Sorted by deaths.", "",
              "| Item | Slot | Holders | Damage taken | Damage dealt | Deaths | Kills + assists |",
              "|---|---|---|---|---|---|---|"]
        for n, e in sorted(t["items"].items(), key=lambda x: x[1]["deaths"][0]):
            L.append(f"| {n} | {e['slot']} | {e['holders']:,} | " +
                     " | ".join(f"{e[k][0]:.3f} ({e[k][1]:+.1f})" for k in KEYS) + " |")
        L.append("")
    with open(MD, "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
