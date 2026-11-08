"""Haze (2026-11-08, scripts/mechanics/haze_lucky.py): Lucky Shot also rolls on Fixation's bonus damage.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, duel  # noqa: E402
from deadsim.heroes import haze  # noqa: E402


def lucky(on):
    old = haze.LUCKY_FIXATION
    haze.LUCKY_FIXATION = on
    try:
        r = duel(Loadout("Haze", ["Lucky Shot", "Extended Magazine"], souls=15000),
                 Loadout("Abrams", ["Extra Health"], souls=15000))
        return r.a_dmg.get("Lucky Shot", 0.0)
    finally:
        haze.LUCKY_FIXATION = old


class HazeLucky(unittest.TestCase):
    def test_fixation_rolls_lucky_shot(self):
        self.assertGreater(lucky(True), lucky(False))


if __name__ == "__main__":
    unittest.main()
