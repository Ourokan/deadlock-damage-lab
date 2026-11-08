"""Lash's Flog factor above 1 stands for more real casts (2026-11-08, validation/README.md "Lash's Quicksilver Reload
follows his Flog casts"): each cast spends a Quicksilver charge, and Flog hits (not DoTs) release Mystic Burst /
Tankbuster charge, so both scale by the factor (items_fx.LANDING_PROCS).
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from test_nurse_quicksilver import charge  # noqa: E402


class FlogProcs(unittest.TestCase):
    def test_quicksilver_follows_flog_landing(self):
        full = charge("ability_lash_flog", 1.0, is_dot=False)
        self.assertGreater(full, 0)
        self.assertAlmostEqual(charge("ability_lash_flog", 1.37, is_dot=False), 1.37 * full, delta=1e-6)

    def test_mystic_burst_release_follows_flog_landing(self):
        full = charge("ability_lash_flog", 1.0, item="Mystic Burst", is_dot=False)
        self.assertGreater(full, 0)
        self.assertAlmostEqual(charge("ability_lash_flog", 1.37, item="Mystic Burst", is_dot=False), 1.37 * full,
                               delta=1e-6)

    def test_ground_strike_not_listed(self):
        full = charge("citadel_ability_lash_down_strike", 1.0, is_dot=False)
        self.assertAlmostEqual(charge("citadel_ability_lash_down_strike", 1.6, is_dot=False), full, delta=1e-6)


if __name__ == "__main__":
    unittest.main()
