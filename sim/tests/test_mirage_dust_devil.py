"""Mirage's Dust Devil lands less late (Mechanics.landing_phase, data/landing_phase.json row from
scripts/cast_timing/landing_phase.py, 2026-11-10). Run from sim/: python3 -m unittest tests.test_mirage_dust_devil"""
import dataclasses
import json
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
from deadsim.mechanics import DEFAULT as MECH, landing_phase_mult  # noqa: E402

load_heroes()
DD = "mirage_tornado"
ROW = json.load(open(os.path.join(ROOT, "data", "landing_phase.json")))["abilities"][DD]


def dd_dmg(souls, on):
    sk = Skill(accuracy=0.0, ability_landing={"Dust Devil": 1.0})
    foe = Loadout("Abrams", [], souls=souls, skill=Skill(accuracy=0.0, use_abilities=False))
    r = duel(Loadout("Mirage", [], souls=souls, skill=sk, unlocked=[False, True, False, False]), foe, max_time=6.0,
             mechanics=dataclasses.replace(MECH, cast_timing=False, ability_area_phase=False, landing_phase=on))
    return r.a_dmg.get("Dust Devil", 0.0)


class DustDevilLate(unittest.TestCase):
    def test_row_lands_less_late(self):
        self.assertLess(ROW["bins"][-1]["landed"], 0.5 * ROW["bins"][1]["landed"])   # replays: 0.34 vs 0.82
        self.assertLess(landing_phase_mult(DD, 40000), 0.8)
        self.assertGreater(landing_phase_mult(DD, 7500), 1.1)

    def test_late_duel_damage_scaled(self):
        souls = 40000
        on, off = dd_dmg(souls, True), dd_dmg(souls, False)
        self.assertGreater(off, 0.0)
        self.assertAlmostEqual(on / off, landing_phase_mult(DD, souls), places=3)


if __name__ == "__main__":
    unittest.main()
