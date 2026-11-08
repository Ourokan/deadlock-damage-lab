"""Landed share of an ability's casts by game phase, from the pair-fight replays (2026-11-08).

An ability's landing factor (data/landing_rates_mech.json) is one number over the whole match. Paige's Captivating
Read and Bookwyrm land on an enemy hero less often in the lane: in Phantom+ pair fights (casts_by_build.py's real rows:
a cast landed if that ability hit an enemy hero within LAG_MAX s and before its next cast) Captivating Read lands 0.83x
its whole-match share below 5k souls and ~1.1x late, Bookwyrm 0.85x / ~1.05x (both halves of the replays agree; lane
casts also go at the wave). Most heroes' abilities land MORE often in the lane (0.69 vs 0.61 of casts), so rows are
only for HEROES' abilities that held the split-half damage audit.

rel(bin) = (landed + K x pooled) / (casts + K) / pooled per caster net-worth bin; the sim multiplies the ability's damage
by rel at the duel's net worth (Mechanics.landing_phase, mechanics.landing_phase_mult: linear in ln net worth between
bins' mean net worths, flat outside).

usage: CASTS_WORK=dir python3 -I casts_by_build.py real   (the real rows), then
       CASTS_WORK=dir python3 -I landing_phase.py [--half 0|1] [--write]   (writes data/landing_phase.json)
"""
import json
import os
import pickle
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "fight_length"))
import casts_by_build as CB  # noqa: E402
from deadsim import game  # noqa: E402

HEROES = {"Paige": ("ability_bookworm_aoemagic", "ability_bookworm_dragonfire"),
          "Vyper": ("ability_viper_debuffdagger",)}
BINS = (0, 5000, 10000, 15000, 22000, 30000, 10 ** 9)
K = 50   # casts of shrinkage toward the pooled share
# lane-only rows: bins from this net worth on are held at rel 1.0. Vyper's Screwjab Dagger lands 1.19x its match share
# below 5k and ~0.87x late (both replay halves); the full row split sim_vs_win_raw (with the Vyper refit 27k +0.007/
# -0.006, 37k -0.002/-0.013; without it 27k +0.007/-0.007, 37k +0.001/-0.011); the lane part sits below the svw
# budgets (2026-11-08, validation/README.md "Lane gaps after the melee point")
LANE_ONLY = {"ability_viper_debuffdagger": 10000}
OUT = os.path.join(ROOT, "data", "landing_phase.json")


def curves(rows, half=None):
    G = game()
    out = {}
    for hero, classes in HEROES.items():
        hid = G.hero(hero).id
        for cls in classes:
            # real rows: (hero id, cls, ult, casts, landed, fight s, cooldown, spirit souls, net worth, cdr, match, ...)
            r = [x for x in rows if x[0] == hid and x[1] == cls and x[3] > 0 and (half is None or x[10] % 2 == half)]
            c, l = sum(x[3] for x in r), sum(x[4] for x in r)
            pooled = l / c
            bins = []
            for lo, hi in zip(BINS, BINS[1:]):
                rb = [x for x in r if lo <= x[8] < hi]
                cb, lb = sum(x[3] for x in rb), sum(x[4] for x in rb)
                if cb:
                    nw = sum(x[8] * x[3] for x in rb) / cb
                    rel = (lb + K * pooled) / (cb + K) / pooled
                    if cls in LANE_ONLY and nw >= LANE_ONLY[cls]:
                        rel = 1.0
                    bins.append({"net_worth": round(nw), "landed": round(lb / cb, 3), "casts": cb, "rel": round(rel, 4)})
            out[cls] = {"name": f"{hero}: " + next(a.name for a in G.hero(hero).abilities if a.class_name == cls),
                        "pooled": round(pooled, 4), "casts": c, "bins": bins}
    return out


def main():
    args = sys.argv[1:]
    half = int(args[args.index("--half") + 1]) if "--half" in args else None
    rows = pickle.load(open(CB.REAL_OUT, "rb"))
    out = curves(rows, half)
    for cls, v in out.items():
        print(v["name"], v["pooled"], " ".join(f"{b['net_worth']}:{b['rel']:.2f}({b['casts']})" for b in v["bins"]))
    if "--write" in args:
        json.dump({"source": "scripts/cast_timing/landing_phase.py (casts_by_build.py real rows: Phantom+ pair fights)",
                   "note": "ability damage x rel(nw) at the caster's net worth, linear in ln nw between bins, flat "
                           "outside (Mechanics.landing_phase)", "abilities": out}, open(OUT, "w"), indent=1)
        print("->", OUT)


if __name__ == "__main__":
    main()
