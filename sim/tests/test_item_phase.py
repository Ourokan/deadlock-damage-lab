"""Item damage by game phase (Mechanics.item_phase, data/item_phase.json from scripts/mechanics/item_phase.py,
2026-11-12, opt-in). Run from sim/: python3 -m unittest tests.test_item_phase"""
import dataclasses
import os
import random
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
from deadsim.mechanics import DEFAULT as MECH, item_phase_mult, item_phase_rows  # noqa: E402

load_heroes()


class ItemPhase(unittest.TestCase):
    def test_rows(self):
        rows = item_phase_rows()
        self.assertIn("Quicksilver Reload", rows)
        self.assertGreater(item_phase_mult("Quicksilver Reload", 6000), item_phase_mult("Quicksilver Reload", 30000))
        self.assertEqual(item_phase_mult("Extra Health", 20000), 1.0)
        self.assertFalse(MECH.item_phase)   # opt-in

    def test_duel_scaled(self):
        souls = 30000

        def shot(on):
            sk = Skill(accuracy=0.5, use_abilities=False, item_landing={"Mystic Shot": 1.0})
            foe = Loadout("Abrams", [], souls=souls, skill=Skill(accuracy=0.0, use_abilities=False))
            r = duel(Loadout("Haze", ["Mystic Shot"], souls=souls, skill=sk), foe, max_time=6.0, rng=random.Random(4),
                     mechanics=dataclasses.replace(MECH, item_phase=on))
            return r.a_dmg.get("Mystic Shot", 0.0)
        on, off = shot(True), shot(False)
        self.assertGreater(off, 0.0)
        self.assertAlmostEqual(on / off, item_phase_mult("Mystic Shot", souls), places=2)


if __name__ == "__main__":
    unittest.main()
