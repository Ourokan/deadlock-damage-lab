"""Area abilities' extra heroes by game phase (Mechanics.ability_area_phase, data/ability_area_phase.json)."""
import dataclasses
import json
import math
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.mechanics import DEFAULT as MECH, ability_area_mult  # noqa: E402

DATA = json.load(open(os.path.join(ROOT, "data", "ability_area_phase.json")))
TERRORS = "ability_nurse_fear"


class AbilityAreaPhaseTest(unittest.TestCase):
    def test_multiplier_follows_the_fitted_bins(self):
        # values read straight from the data file, so a refit keeps this passing
        row = DATA["abilities"][TERRORS]
        b = row["bins"]
        self.assertAlmostEqual(ability_area_mult(TERRORS, b[1]["net_worth"]), b[1]["rel"] / row["pooled"], places=6)
        lo, hi = b[1], b[2]
        nw = math.sqrt(lo["net_worth"] * hi["net_worth"])   # halfway in ln net worth
        self.assertAlmostEqual(ability_area_mult(TERRORS, nw), (lo["rel"] + hi["rel"]) / 2 / row["pooled"], places=6)
        self.assertAlmostEqual(ability_area_mult(TERRORS, 100), b[0]["rel"] / row["pooled"], places=6)   # flat outside
        self.assertAlmostEqual(ability_area_mult(TERRORS, 1e6), b[-1]["rel"] / row["pooled"], places=6)

    def test_lane_below_late_and_mean_one(self):
        # non-decreasing in net worth, and the curve's mean (weighted as fitted) is the pooled level
        for cls, row in DATA["abilities"].items():
            rel = [b["rel"] for b in row["bins"]]
            self.assertEqual(rel, sorted(rel), cls)
            self.assertLessEqual(rel[0], row["pooled"] + 1e-6, cls)
            self.assertGreaterEqual(rel[-1], row["pooled"] - 1e-6, cls)

    def test_no_row_no_change(self):
        self.assertEqual(ability_area_mult("ability_not_there", 30000), 1.0)
        self.assertEqual(ability_area_mult(TERRORS, None), 1.0)

    def test_engine_scales_the_ability_damage(self):
        # Lurking Terrors alone, deterministic duel: damage with the term = without x the multiplier at the duel's souls
        souls = 40000
        sk = Skill(accuracy=0.0, ability_landing={"Lurking Terrors": 1.0})
        foe = Loadout("Abrams", [], souls=souls, skill=Skill(accuracy=0.0, use_abilities=False))
        got = {}
        for on in (False, True):
            r = duel(Loadout("Nurse Harrow", [], souls=souls, skill=sk, unlocked=[False, False, False, True]), foe,
                     max_time=8.0, mechanics=dataclasses.replace(MECH, ability_area_phase=on, cast_timing=False))
            got[on] = r.a_dmg.get("Lurking Terrors", 0.0)
        self.assertGreater(got[False], 0.0)
        self.assertAlmostEqual(got[True] / got[False], ability_area_mult(TERRORS, souls), places=3)


if __name__ == "__main__":
    unittest.main()
