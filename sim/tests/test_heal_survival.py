"""Checks of the overall score's heal survival (damage/scripts/overall_search.py HEAL_SURVIVAL, Evaluator._heal_surv):
healing items' duel time-alive gain counts ^ HEAL_SURVIVAL. Run from sim/: python3 -m unittest discover -s tests"""
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "survival")]

import overall_search as O  # noqa: E402
import search as S  # noqa: E402


def item(name):
    return next(i for i, it in S.G().items.items() if it.name == name)


class Stub(O.Evaluator):
    """Evaluator without fights: time alive = 10 s + 2 s per healing item held, 1 s per other item."""

    def __init__(self, pop):
        self.pop, self._hg, self.cache = tuple(sorted(pop)), {}, {}

    def _rows(self, items, pool):
        t = 10.0 + sum(2.0 if S.G().items[i].name in O.HEAL_ITEMS else 1.0 for i in items)
        return [(0, 1.0, 0.0, t, 1.0)]


class HealSurvival(unittest.TestCase):
    def setUp(self):
        self.was = O.HEAL_SURVIVAL

    def tearDown(self):
        O.HEAL_SURVIVAL = self.was

    def test_factor(self):
        leech, booster, armor = item("Leech"), item("Healing Booster"), item("Battle Vest")
        ev = Stub([armor])
        a = O.DAMAGE_ELASTICITY
        O.HEAL_SURVIVAL = 0.5
        self.assertEqual(ev._heal_surv([armor], "F"), 1.0)            # no healing item: nothing changes
        self.assertAlmostEqual(ev._heal_surv([armor, leech], "F"), (13 / 11) ** (a * -0.5))
        self.assertAlmostEqual(ev._heal_surv([armor, leech, booster], "F"), ((13 / 11) * (13 / 11)) ** (a * -0.5))
        ev2 = Stub([armor, leech])                                      # held by the popular build: gain = with / without
        self.assertAlmostEqual(ev2._heal_gain(leech, "F"), 13 / 11)
        O.HEAL_SURVIVAL = 1
        self.assertEqual(ev._heal_surv([armor, leech], "F"), 1.0)


if __name__ == "__main__":
    unittest.main()
