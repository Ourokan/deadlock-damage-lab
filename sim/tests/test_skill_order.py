"""Checks of the ability point model (deadsim.fight) and the ability order search (damage/scripts/skill_order.py).
Run from sim/: python3 -m unittest discover -s tests"""
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "damage")]

from deadsim.data import game  # noqa: E402
from deadsim.fight import abilities_for_order, ability_budget, popular_ability_order  # noqa: E402
import skill_order as K  # noqa: E402

G = game()
HAZE = G.hero("Haze")
IDS = [a.id for a in HAZE.abilities]


class Points(unittest.TestCase):
    def test_four_unlocks_and_32_points_by_level_36(self):
        self.assertEqual(ability_budget(HAZE, 0), (1, 0))
        self.assertEqual(ability_budget(HAZE, 50000), (4, 32))

    def test_popular_order_is_maxed_at_50k(self):
        tiers, unlocked = abilities_for_order(HAZE, popular_ability_order(HAZE.id), 50000)
        self.assertEqual(tiers, [3, 3, 3, 3])
        self.assertTrue(all(unlocked))

    def test_order_waits_for_a_tier_3_instead_of_skipping_ahead(self):
        a, b = IDS[0], IDS[1]
        order = [a, b, IDS[2], IDS[3], a, a, a, b]   # unlocks, then a to tier 3 (8 points), then b
        for souls in range(4000, 12000, 500):
            pts = ability_budget(HAZE, souls)[1]
            tiers, _ = abilities_for_order(HAZE, order, souls)
            want = 3 if pts >= 8 else 2 if pts >= 3 else 1 if pts >= 1 else 0
            self.assertEqual(tiers[0], want, souls)
            self.assertEqual(tiers[1], 1 if pts >= 9 else 0, souls)


class Search(unittest.TestCase):
    def test_stop_rule(self):
        self.assertTrue(K.stops_at((3, 3, 3, 3), 32))
        self.assertTrue(K.stops_at((2, 0, 0, 0), 4, toward=(3, 0, 0, 0)))    # 1 left, tier 3 costs 5
        self.assertFalse(K.stops_at((2, 0, 0, 0), 4, toward=(2, 1, 0, 0)))   # 1 left buys the next tier 1

    def test_full_order_follows_the_upgrade_sequence(self):
        seq = [2, 2, 2, 0, 0, 0, 1, 1, 1, 3, 3, 3]
        order, steps = K.full_order(HAZE, popular_ability_order(HAZE.id), seq)
        self.assertEqual(len(order), 16)
        ups = [IDS.index(s["ability"]) for s in steps if s["tier"]]
        self.assertEqual(ups, seq)
        self.assertEqual(abilities_for_order(HAZE, order, 50000)[0], [3, 3, 3, 3])
        levels = [s["level"] for s in steps]
        self.assertEqual(levels, sorted(levels))


if __name__ == "__main__":
    unittest.main()
