"""Checks of the overall score's farm value (damage/scripts/overall_search.py farm_value): real holders' jungle-souls
ratios from sim/data/fight_rate.json.
Run from sim/: python3 -m unittest discover -s tests"""
import math
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "survival")]

import overall_search as O  # noqa: E402
import search as S  # noqa: E402


def item(name):
    return next(i for i, it in S.G().items.items() if it.name == name)


class FarmValue(unittest.TestCase):
    def setUp(self):
        self.was = O.FARM_GAMMA

    def tearDown(self):
        O.FARM_GAMMA = self.was

    def test_value(self):
        self.assertAlmostEqual(O.farm_value([], 27000), 1.0)
        rates = O.jungle_rates(27000)
        ric, decay = item("Ricochet"), item("Decay")
        self.assertGreater(rates[ric], 1.0)    # Ricochet holders clear camps faster
        self.assertLess(rates[decay], 1.0)
        self.assertAlmostEqual(O.farm_value([ric, decay], 27000), (rates[ric] * rates[decay]) ** O.FARM_GAMMA)
        lo, hi = O.DEATH_RATE_CLAMP
        self.assertAlmostEqual(O.farm_value(list(rates), 27000),
                               max(lo, min(hi, math.prod(rates.values()))) ** O.FARM_GAMMA)
        O.FARM_GAMMA = 0
        self.assertEqual(O.farm_value([ric], 27000), 1.0)

    def test_every_budget(self):
        for b in (10000, 18000, 27000, 37000, 50000):
            self.assertTrue(O.jungle_rates(b))

    def test_movement_skipped(self):
        O.movement_value(())
        moving = O._move[2]
        self.assertFalse(set(O.jungle_rates(27000)) & moving)


if __name__ == "__main__":
    unittest.main()
