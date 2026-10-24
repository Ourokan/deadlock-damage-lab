"""Dispel Magic cleanses only Skill.dot_cleanse_share of enemy DoTs (fitted, sim/scripts/fit_dispel.py).
Run from sim/: python3 -m unittest discover -s tests"""
import dataclasses
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from deadsim import Loadout, duel  # noqa: E402
from deadsim.accuracy import _dispel_fit, dot_cleanse_delay, dot_cleanse_share, hero_default_skill  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.items_fx import DispelMagic  # noqa: E402


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
        self.assertIn(cleansed, (3, 4, 5))

    def test_reaction_by_rank(self):
        self.assertEqual(dot_cleanse_delay(111), 1.5)
        self.assertEqual(dot_cleanse_delay(91), 3.0)
        self.assertEqual(dot_cleanse_delay(None), 3.0)

    def test_missing_fit_raises(self):
        with self.assertRaises(OSError):
            _dispel_fit(-1)

    def test_unphased_phase_spreads(self):
        # no fight_phase, no rng: the pick starts at a hash of both loadouts, spread over 0-1 across opponents
        names = ["Extra Health", "Extra Regen", "Extra Stamina", "Healing Rite", "Close Quarters", "Headshot Booster",
                 "Rapid Rounds", "Spirit Strike", "Monster Rounds", "Sprint Boots", "Spirit Lifesteal",
                 "Bullet Lifesteal", "Extra Charge", "Hollow Point", "Mystic Burst", "Toxic Bullets"]
        phases = []
        for a in names:
            for b in names[:8]:
                e = Engine()
                fa = make_fighter(e, Loadout("Seven", [a, "Decay"], souls=10000))
                fb = make_fighter(e, Loadout("Haze", [b, "Dispel Magic"], souls=10000))
                fa.enemy, fb.enemy = fb, fa
                phases.append(DispelMagic.loadout_phase(fb))
        below = sum(p < 0.5 for p in phases) / len(phases)
        self.assertTrue(0.35 < below < 0.65, below)
        self.assertGreater(len(set(round(p, 6) for p in phases)), len(phases) // 4)

if __name__ == "__main__":
    unittest.main()
