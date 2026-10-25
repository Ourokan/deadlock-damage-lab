"""Bebop's Grapple Arm hit and Victor's Shocking Reanimation carried over from earlier fights
(deadsim/heroes/bebop.py, frank.py). Run from sim/:
    python3 -m unittest discover -s tests
"""
import dataclasses
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.mechanics import DEFAULT, real_length  # noqa: E402
import deadsim.heroes.frank as frank  # noqa: E402


class BebopHook(unittest.TestCase):
    def test_grapple_arm_deals_melee_damage(self):
        sk = Skill(accuracy=0.5, headshot=0.0)
        r = duel(Loadout("Bebop", [], souls=15000, skill=sk), Loadout("Abrams", [], souls=15000), distance=10,
                 max_time=10, mechanics=None)
        self.assertGreater(r.a_dmg.get("Grapple Arm", 0.0), 0.0)


class VictorCarry(unittest.TestCase):
    def starts(self, mech, rng):
        seen = []
        orig = frank.carried_cooldown

        def spy(c, s):
            v = orig(c, s)
            seen.append(v)
            return v
        frank.carried_cooldown = spy
        try:
            for i in range(30):
                duel(Loadout("Victor", [], souls=30000), Loadout("Haze", [], souls=30000), max_time=5,
                     rng=random.Random(i) if rng else None, mechanics=mech)
        finally:
            frank.carried_cooldown = orig
        return seen

    def test_ready_without_fight_length_or_rng(self):
        self.assertTrue(all(v == 0 for v in self.starts(DEFAULT, True)))
        mech = dataclasses.replace(DEFAULT, fight_length=real_length(30000))
        self.assertTrue(all(v == 0 for v in self.starts(mech, False)))

    def test_some_fights_start_on_cooldown(self):
        mech = dataclasses.replace(DEFAULT, fight_length=real_length(30000))
        seen = self.starts(mech, True)
        on = sum(1 for v in seen if v > 0) / len(seen)
        self.assertTrue(0.1 < on < 0.8, on)


if __name__ == "__main__":
    unittest.main()
