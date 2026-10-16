"""Refit ability landing factors for some heroes only and update them in place.

Runs scripts/landing_rates.py --hero for each named hero (all of that hero's sample players) and writes the new
factors into data/landing_rates.json (mechanics off) and data/landing_rates_mech.json (mechanics on), leaving
every other hero as it is. Use it after changing how a few heroes fight (hero files, data/fight_patterns.json).

usage: python3 scripts/refit_landing_heroes.py "Mo & Krill" Lash ...
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


def fit(hero, mech):
    M.DEFAULT = M.Mechanics() if mech else None
    sys.argv = ["landing_rates.py", "1000000000", str(os.cpu_count()), "--hero", hero]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        L.main()
    return {m.group(1).strip(): float(m.group(2)) for m in LINE.finditer(buf.getvalue())}


def main(heroes):
    for mech, fn in ((False, "landing_rates.json"), (True, "landing_rates_mech.json")):
        path = os.path.join(ROOT, "data", fn)
        d = json.load(open(path))
        for h in heroes:
            new = fit(h, mech)
            rows = d["heroes"].setdefault(L.game().hero(h).name, {})
            for ab, v in new.items():
                if ab in rows:
                    print(f"{fn} {h} {ab}: {rows[ab]['landing']} -> {v}")
                    rows[ab]["landing"] = v
        json.dump(d, open(path, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
