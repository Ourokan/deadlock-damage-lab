"""Checks of the overall score's buy value (damage/scripts/overall_search.py buy_value): items the hero's players
seldom buy (share of same-slot same-tier holdings below BUY_KNEE) count slightly less.
Run from sim/: python3 -m unittest discover -s tests"""
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "survival")]

import overall_search as O  # noqa: E402
import search as S  # noqa: E402


def item(name):
    return next(i for i, it in S.G().items.items() if it.name == name)


class BuyValue(unittest.TestCase):
    def setUp(self):
        self.was = O.BUY_GAMMA

    def tearDown(self):
        O.BUY_GAMMA = self.was

    def test_shares(self):
        g = S.G()
        a = item("Split Shot")
        b = next(i for i, it in g.items.items() if i != a and (it.slot, it.tier) == (g.items[a].slot, g.items[a].tier))
        c = next(i for i, it in g.items.items() if (it.slot, it.tier) != (g.items[a].slot, g.items[a].tier))
        sh = O.buy_shares(7, {"7": {"_n": 100, str(a): 30, str(b): 10, str(c): 5}})
        self.assertAlmostEqual(sh[a], 0.75)   # of the same slot and tier holdings
        self.assertAlmostEqual(sh[c], 1.0)
        self.assertEqual(O.buy_shares(8, {"7": {}}), {})

    def test_value(self):
        a, b = item("Split Shot"), item("Mystic Shot")
        shares = {a: 0.5, b: 0.01}
        self.assertEqual(O.buy_value([a], shares), 1.0)   # common pick: no change
        self.assertAlmostEqual(O.buy_value([b], shares), (0.01 / O.BUY_KNEE) ** O.BUY_GAMMA)
        self.assertAlmostEqual(O.buy_value([b, b], shares), O.buy_value([b], shares))   # held items count once
        never = O.buy_value([item("Decay")], shares)
        self.assertAlmostEqual(never, (O.BUY_FLOOR / O.BUY_KNEE) ** O.BUY_GAMMA)
        self.assertGreater(never, 0.98)   # mild: damage efficiency stays the main function
        self.assertEqual(O.buy_value([b], None), 1.0)
        O.BUY_GAMMA = 0
        self.assertEqual(O.buy_value([b], shares), 1.0)


if __name__ == "__main__":
    unittest.main()
