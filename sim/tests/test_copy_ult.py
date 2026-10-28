"""Sinclair's copied ultimates (2026-10-28, opt-in): with Mechanics.copy_ult, Audience Participation's copy books its damage
with its own landing factor x the copied ultimate's factor (data/copy_ult.json), so ultimates real Sinclairs get
little from (Combo) count less than ones they get a lot from (Lurking Terrors).
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim import mechanics as M  # noqa: E402
from deadsim.accuracy import hero_default_skill  # noqa: E402
from deadsim.fight import duel  # noqa: E402
from deadsim.heroes import magician  # noqa: E402


def copy_damage(foe, mech, n=30):
    tot = 0.0
    for s in range(n):
        a = Loadout("Sinclair", [], souls=27000, skill=hero_default_skill("Sinclair", counterplay=True))
        b = Loadout(foe, [], souls=27000, skill=hero_default_skill(foe, counterplay=True))
        r = duel(a, b, max_time=20, rng=random.Random(s), mechanics=mech)
        tot += sum(v for k, v in r.a_dmg.items() if k.startswith("Audience Participation ("))
    return tot


class CopyUlt(unittest.TestCase):
    def test_factors_loaded(self):
        f = magician.copy_ult_factors()
        self.assertLess(f["ability_ult_combo"], 1.0)
        self.assertGreater(f["ability_nurse_fear"], 1.0)

    def test_copy_scaled_by_its_ultimate(self):
        on, off = (dataclasses.replace(M.DEFAULT, copy_ult=x) for x in (True, False))
        f = magician.copy_ult_factors()["ability_ult_combo"]
        on_d, off_d = copy_damage("Mo & Krill", on), copy_damage("Mo & Krill", off)
        self.assertGreater(off_d, 0)
        self.assertLess(on_d, off_d)
        self.assertAlmostEqual(on_d / off_d, f, delta=0.35 * f)


if __name__ == "__main__":
    unittest.main()
