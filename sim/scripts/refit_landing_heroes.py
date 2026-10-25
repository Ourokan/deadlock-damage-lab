"""Refit ability landing factors for some heroes only and update them in place.

Runs scripts/landing_rates.py --hero for each named hero (all of that hero's sample players) and writes the new
factors into data/landing_rates.json (mechanics off) and data/landing_rates_mech.json (mechanics on), leaving
every other hero as it is. Use it after changing how a few heroes fight (hero files, data/fight_patterns.json).

With --iterate N (default 1) each fit runs landing_rates.py --iterate N times, starting from the factors in the
files: needed for heroes whose factors don't scale damage linearly (Haze: Bullet Dance shortens its channel).

With --sample PATH the fits use that sample (e.g. a Phantom+ one from fetch_validation.py --api) instead of
validation/matches_sample.jsonl.gz. Abilities the files don't list yet (a new hero) are added.

usage: python3 scripts/refit_landing_heroes.py [--iterate N] [--sample PATH] "Mo & Krill" Lash ...
"""
import contextlib
import io
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import deadsim.mechanics as M  # noqa: E402
import landing_rates as L  # noqa: E402

LINE = re.compile(r"^\s+landing (.+?)\s+([\d.]+)$", re.M)


SAMPLE = []   # --sample PATH: fit on that sample instead of validation/matches_sample.jsonl.gz


def fit(hero, mech, iterate=False):
    M.DEFAULT = M.Mechanics() if mech else None
    L._landing.clear()
    sys.argv = (["landing_rates.py", "1000000000", str(os.cpu_count())] + (["--iterate"] if iterate else []) + SAMPLE
                + ["--hero", hero])
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        L.main()
    return {m.group(1).strip(): float(m.group(2)) for m in LINE.finditer(buf.getvalue())}


def main(heroes, rounds=0):
    for mech, fn in ((False, "landing_rates.json"), (True, "landing_rates_mech.json")):
        path = os.path.join(ROOT, "data", fn)
        for i in range(max(1, rounds)):
            d = json.load(open(path))
            for h in heroes:
                new = fit(h, mech, iterate=rounds > 0)
                hero = L.game().hero(h)
                classes = {a.name: a.class_name for a in hero.abilities}
                rows = d["heroes"].setdefault(hero.name, {})
                for ab, v in new.items():
                    old = rows.setdefault(ab, {"landing": None})
                    if "class" not in old and ab in classes:   # length_factors.py needs it for a new row
                        old["class"] = classes[ab]
                    print(f"{fn} {h} {ab}: {old['landing']} -> {v}", flush=True)
                    old["landing"] = v
            json.dump(d, open(path, "w"), indent=1)   # the next round's fights read these factors


if __name__ == "__main__":
    args = sys.argv[1:]
    n = 0
    if "--sample" in args:
        i = args.index("--sample")
        SAMPLE[:] = ["--sample", args[i + 1]]
        args = args[:i] + args[i + 2:]
    if "--iterate" in args:
        i = args.index("--iterate")
        n = int(args[i + 1])
        args = args[:i] + args[i + 2:]
    main(args, n)
