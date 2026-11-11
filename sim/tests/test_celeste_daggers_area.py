"""Celeste's Radiant Daggers hits more heroes as the game goes on (Mechanics.ability_area_phase, 2026-11-10)."""
import json
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from deadsim.mechanics import ability_area_mult  # noqa: E402

DATA = json.load(open(os.path.join(ROOT, "data", "ability_area_phase.json")))
DAGGERS = "ability_unicorn_luminousstrike"


class CelesteDaggersAreaTest(unittest.TestCase):
    def test_daggers_row_lane_under_late_over(self):
        self.assertIn(DAGGERS, DATA["abilities"])
        self.assertLess(ability_area_mult(DAGGERS, 3000), 0.9)
        self.assertGreater(ability_area_mult(DAGGERS, 45000), 1.1)

    def test_only_the_daggers_row(self):
        # Dazzling Trick and Shining Wonder rows cut sim_vs_win_raw (ability_area_phase.ONLY)
        for cls in ("ability_unicorn_prismaticguard", "ability_unicorn_dazzlingorb", "ability_unicorn_radiantblast"):
            self.assertNotIn(cls, DATA["abilities"])
            self.assertEqual(ability_area_mult(cls, 45000), 1.0)


if __name__ == "__main__":
    unittest.main()
