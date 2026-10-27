"""Checks of the overall score's focus cost (damage/scripts/overall_search.py focus_value): real holders' damage-taken
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


class FocusCost(unittest.TestCase):
    def setUp(self):
        self.was = O.FOCUS_GAMMA

    def tearDown(self):
        O.FOCUS_GAMMA = self.was

    def test_value(self):
        self.assertAlmostEqual(O.focus_value([], 27000), 1.0)
        rates = O.taken_rates(27000)
        rf, reb = item("Return Fire"), item("Rebuttal")
        self.assertGreater(rates[reb], 1.0)    # Rebuttal holders take more damage per minute
        self.assertAlmostEqual(O.focus_value([rf, reb], 27000), (rates[rf] * rates[reb]) ** -O.FOCUS_GAMMA)
        lo, hi = O.DEATH_RATE_CLAMP
        self.assertAlmostEqual(O.focus_value(list(rates), 27000),
                               max(lo, min(hi, math.prod(rates.values()))) ** -O.FOCUS_GAMMA)
        O.FOCUS_GAMMA = 0
        self.assertEqual(O.focus_value([reb], 27000), 1.0)

    def test_skipped(self):
        rates = O.taken_rates(27000)
        names = {it.name for i, it in S.G().items.items() if i in rates}
        self.assertFalse(names & O.HEAL_ITEMS)
        self.assertFalse(names & O.FOCUS_SKIP)
        for n in O.FOCUS_SKIP:    # the skip list names real items
            item(n)


if __name__ == "__main__":
    unittest.main()
