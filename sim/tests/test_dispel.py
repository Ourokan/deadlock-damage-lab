"""Dispel Magic cleanses only Skill.dot_cleanse_share of enemy DoTs (fitted, sim/scripts/fit_dispel.py).
Run from sim/: python3 -m unittest discover -s tests"""
import dataclasses
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from deadsim import Loadout, duel  # noqa: E402
from deadsim.accuracy import dot_cleanse_share, hero_default_skill  # noqa: E402


def decay_taken(share, phase=None):
    a = Loadout("Seven", ["Extra Spirit", "Mystic Burst", "Decay"], souls=20000,
                skill=hero_default_skill("Seven", badge=91, counterplay=True))
    sk = dataclasses.replace(hero_default_skill("Haze", badge=91, counterplay=True), dot_cleanse_share=share,
                             fight_phase=phase)
    b = Loadout("Haze", ["Rapid Rounds", "Swift Striker", "Dispel Magic"], souls=20000, skill=sk)
    return duel(a, b).a_dmg.get("Decay", 0.0)


class DispelShare(unittest.TestCase):
    def test_fitted_share_loaded(self):
        for badge in (None, 91, 111):
            s = dot_cleanse_share(badge)
            self.assertIsNotNone(s)
            self.assertTrue(0.0 < s < 1.0)
        self.assertEqual(dot_cleanse_share(111), dot_cleanse_share(91))

    def test_share_gates_cleanse(self):
        never, always = decay_taken(0.0), decay_taken(1.0)
        self.assertGreater(never, 0.0)
        self.assertLess(always, 0.6 * never)

    def test_phase_picks_share_of_fights(self):
        # the first DoT is cleansed when phase + share crosses 1: in about `share` of evenly spread phases
        never = decay_taken(0.0)
        cleansed = sum(decay_taken(0.4, phase=k / 10) < 0.6 * never for k in range(10))
        self.assertEqual(cleansed, 4)

    def test_unphased_fight_rounds_share(self):
        # no fight_phase, no rng: all or nothing, the first DoT is cleansed only from share 0.5 up
        never = decay_taken(0.0)
        self.assertAlmostEqual(decay_taken(0.26), never)
        self.assertLess(decay_taken(0.5), 0.6 * never)


if __name__ == "__main__":
    unittest.main()
