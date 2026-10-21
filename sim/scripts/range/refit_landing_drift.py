"""Refit every hero's mechanics-on landing factors (data/landing_rates_mech.json) and the mech validation shares with
the current deadsim.mechanics.DEFAULT (range drift on), by running landing_rates.py --iterate over all heroes N times.
landing_rates.py writes the mechanics-off file names, so each round moves its outputs to the _mech names and restores
the mechanics-off files.

usage: python3 refit_landing_drift.py [rounds] [workers]
"""
import os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "scripts"))
import deadsim.mechanics as M  # noqa: E402
import landing_rates as L  # noqa: E402

PAIRS = [("data/landing_rates.json", "data/landing_rates_mech.json"),
         ("validation/damage_shares.json", "validation/damage_shares_mech.json"),
         ("validation/item_shares.json", "validation/item_shares_mech.json")]


def main():
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    workers = sys.argv[2] if len(sys.argv) > 2 else str(os.cpu_count())
    M.DEFAULT = M.Mechanics()
    keep = {off: open(os.path.join(ROOT, off)).read() for off, _ in PAIRS}
    try:
        for r in range(rounds):
            L._landing.clear()
            sys.argv = ["landing_rates.py", "1000000000", workers, "--iterate"]
            L.main()
            for off, mech in PAIRS:
                shutil.copy(os.path.join(ROOT, off), os.path.join(ROOT, mech))
            print("round", r + 1, "done", flush=True)
    finally:
        for off, text in keep.items():
            open(os.path.join(ROOT, off), "w").write(text)


if __name__ == "__main__":
    main()
