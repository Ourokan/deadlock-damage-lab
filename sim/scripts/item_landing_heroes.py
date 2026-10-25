"""Per-hero item damage factors from the damage audit's holders-only hero x item table.

The pooled factors (scripts/item_landing.py) are one fit over every holder, so they follow the heroes that buy an item
most; how much of an item's damage real players land differs a lot by hero (Torment Pulse real/sim from 0.57 on
Graves to 1.74 on Shiv in the 2026-10-25 audit). Fight distance does not explain it: making item radii follow each
hero's real Phantom+ fight distance (match_paths) left the per-hero gaps as wide (validation/README.md "Per-hero item
factors").

For each hero x item row of validation/damage_audit.json (at least damage_audit.HERO_ITEM_MIN holders):

    landing = current factor x (real/sim) ^ (holders / (holders + PRIOR))

where the current factor is what that hero's duels used in the audit (its own row if it has one, else the pooled
factor, else 1 for an uncut item) and the exponent shrinks small samples toward no change. Same cap as the pooled
factors: at most 1 (an item real players get more from stays uncut; that excess is mostly team fights), at least
0.25. Rows that would stay exactly at the pooled factor are left out. Run the audit, then this, then the audit again;
it starts from the audit's residuals, so a second pass refines the first. PRIOR = 20 holders from a split-half check
(fit on one half of the sample's matches, audited on the other: held-out hero x item error 0.338 -> 0.249 with no
shrinkage, 0.250 at 20, 0.260 at 40, 0.277 at 80; 20 hedges rows near the 20-holder floor at almost no cost).

With --hero NAME (repeatable) only that hero's rows are refit and the other heroes' rows are kept, for a hero whose
ability factors were just refit (scripts/refit_landing_heroes.py): its old item rows made up for the old abilities.

usage: python3 scripts/item_landing_heroes.py [--audit PATH] [--prior N] [--hero NAME ...] [--write]
"""
import json
import math
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from deadsim import accuracy  # noqa: E402

PRIOR = 20


def fit(audit, prior=PRIOR, only=None):
    """only: refit just these heroes' rows (after refitting their abilities) and keep every other hero's."""
    data = json.load(open(accuracy.ITEM_LANDING))
    heroes = {h: v for h, v in data.get("heroes", {}).items() if only and h not in only}
    for r in audit["hero_items"]:
        if only and r["hero"] not in only:
            continue
        x = r.get("real_over_sim")
        if not x or x <= 0:
            continue
        cur = accuracy.item_landing(r["hero"]).get(r["item"], 1.0)
        new = cur * math.exp(r["holders"] / (r["holders"] + prior) * math.log(x))
        new = max(0.25, min(1.0, new))
        pooled = accuracy.item_landing().get(r["item"], 1.0)
        if abs(new - pooled) < 1e-3:
            continue
        heroes.setdefault(r["hero"], {})[r["item"]] = {"holders": r["holders"], "real_over_sim": x,
                                                       "landing": round(new, 3)}
    data["heroes"] = {h: dict(sorted(v.items())) for h, v in sorted(heroes.items())}
    data["meta"]["heroes"] = (f"per-hero factors from the damage audit's hero x item rows ({audit['meta']['sample']}, "
                              f">= 20 holders): current factor x (real/sim)^(n/(n+{prior})), capped 0.25-1; replace "
                              "the pooled factor for that hero (scripts/item_landing_heroes.py)")
    return data


def main():
    args = sys.argv[1:]
    path = os.path.join(ROOT, "validation", "damage_audit.json")
    prior = PRIOR
    if "--audit" in args:
        path = args[args.index("--audit") + 1]
    if "--prior" in args:
        prior = float(args[args.index("--prior") + 1])
    only = {args[i + 1] for i, a in enumerate(args) if a == "--hero"}
    data = fit(json.load(open(path)), prior, only)
    n = sum(len(v) for v in data["heroes"].values())
    for h, v in data["heroes"].items():
        if only and h not in only:
            continue
        for it, r in v.items():
            print(f"{h:15s} {it:22s} n={r['holders']:4d} real/sim {r['real_over_sim']:.2f} -> {r['landing']:.3f}")
    print(f"{n} hero x item factors")
    if "--write" in args:
        json.dump(data, open(accuracy.ITEM_LANDING, "w"), indent=1)


if __name__ == "__main__":
    main()
