"""Melee by game phase (Mechanics.melee_phase, data/melee_phase.json)."""
import dataclasses
import json
import math
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.mechanics import DEFAULT as MECH, melee_phase_mult  # noqa: E402

DATA = json.load(open(os.path.join(ROOT, "data", "melee_phase.json")))
CALICO = "16"


class MeleePhaseTest(unittest.TestCase):
    def test_multiplier_follows_the_fitted_points(self):
        # values read straight from the data file, so a refit keeps this passing
        pts = DATA["heroes"][CALICO]["points"]
        self.assertAlmostEqual(melee_phase_mult(16, pts[1][0]), pts[1][1], places=6)
        nw = math.sqrt(pts[0][0] * pts[1][0])   # halfway in ln net worth
        self.assertAlmostEqual(melee_phase_mult(16, nw), (pts[0][1] + pts[1][1]) / 2, places=6)
        self.assertAlmostEqual(melee_phase_mult(16, 100), pts[0][1], places=6)   # flat outside
        self.assertAlmostEqual(melee_phase_mult(16, 1e6), pts[-1][1], places=6)

    def test_lane_melee_above_late_pooled(self):
        p = DATA["pooled"]
        self.assertGreater(p["0.3"], p["0.9"])

    def test_no_row_no_change(self):
        self.assertEqual(melee_phase_mult(999999, 30000), 1.0)
        self.assertEqual(melee_phase_mult(16, None), 1.0)

    def test_engine_scales_the_melee_rate(self):
        # melee only, deterministic duel: melee damage with the term = without x the multiplier at the duel's souls
        souls = DATA["heroes"][CALICO]["points"][0][0]
        sk = Skill(accuracy=0.0, use_abilities=False, melee_rate=0.5)
        foe = Loadout("Abrams", [], souls=souls, skill=Skill(accuracy=0.0, use_abilities=False))
        got = {}
        for on in (False, True):
            mech = dataclasses.replace(MECH, melee_phase=on, movement=False, parry=False, range_drift=False)
            r = duel(Loadout("Calico", [], souls=souls, skill=sk), foe, distance=2.0, max_time=10.0, mechanics=mech)
            got[on] = r.a_dmg.get("melee", 0.0)
        self.assertGreater(got[False], 0.0)
        self.assertAlmostEqual(got[True] / got[False], melee_phase_mult(16, souls), delta=0.15)


if __name__ == "__main__":
    unittest.main()
