"""Per-hero ability length corrections straight from the damage audit, for heroes whose landing factors were refit.

refit_landing_heroes.py fits each ability's landing factor with every hit of a 20 s duel in full and the casts on
sight (what the dummy page runs). The searches and the audit book damage over real fight lengths with first casts
held to real cast times (Mechanics.fight_length + cast_timing), through landing x length_corr. length_factors.py
can't redo length_corr for a refit hero any more: its keep mode refuses factors already scaled for cast timing, and
its --refit target (the in-full ratio in duels with held casts) is not what the landing fit saw (held-out audit
0.040 -> 0.063 for 13 refit heroes).

So for each named hero's ability rows in data/landing_rates_mech.json, from the audit's per-hero sources
(validation/damage_audit.json, real/sim of source damage over gun damage):

    length_corr = length_corr x (real/sim) ^ (players / (players + PRIOR))

clipped to KEEP_RANGE. Note the heroes in the file's meta "audit_corr_heroes". Run the audit, then this, a few rounds (each audit reads the new factors). Abilities the
audit does not see on a hero (never cast, no real damage) keep their correction.

usage: python3 scripts/ability_corr_heroes.py [--audit PATH] [--prior N] --hero NAME [--hero NAME ...] [--write]
"""
import json
import math
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PATH = os.path.join(ROOT, "data", "landing_rates_mech.json")
PRIOR = 20
KEEP_RANGE = (0.1, 10.0)   # as length_factors.py's keep mode


def fit(audit, heroes, prior=PRIOR):
    data = json.load(open(PATH))
    for h in heroes:
        a = audit["heroes"].get(h)
        rows = data["heroes"].get(h)
        if not a or not rows:
            print(f"{h}: not in the audit or the landing file")
            continue
        w = a["players"] / (a["players"] + prior)
        for name, r in rows.items():
            src = a["sources"].get(r.get("class") or "")
            x = src and src.get("real_over_sim")
            if not x or x <= 0:
                continue
            old = r.get("length_corr", 1.0)
            new = max(KEEP_RANGE[0], min(KEEP_RANGE[1], old * math.exp(w * math.log(x))))
            r["length_corr"] = round(new, 3)
            print(f"{h:15s} {name:28s} real/sim {x:5.2f}  length_corr {old:.3f} -> {new:.3f}")
    return data


def main():
    args = sys.argv[1:]
    path = os.path.join(ROOT, "validation", "damage_audit.json")
    prior = PRIOR
    if "--audit" in args:
        path = args[args.index("--audit") + 1]
    if "--prior" in args:
        prior = float(args[args.index("--prior") + 1])
    heroes = [args[i + 1] for i, a in enumerate(args) if a == "--hero"]
    data = fit(json.load(open(path)), heroes, prior)
    if "--write" in args:
        json.dump(data, open(PATH, "w"), indent=1)


if __name__ == "__main__":
    main()
