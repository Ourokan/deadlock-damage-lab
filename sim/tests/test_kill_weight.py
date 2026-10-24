"""Checks of the overall score's kill weight (damage/scripts/overall_search.py kill_cut, sim/data/kill_weight.json):
items' own damage counts x how often real damage of that item is followed by a kill.
Run from sim/: python3 -m unittest discover -s tests"""
import json
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "survival")]

import overall_search as O  # noqa: E402

with open(os.path.join(ROOT, "sim", "data", "kill_weight.json")) as _fh:
    KW = json.load(_fh)["items"]


class KillWeight(unittest.TestCase):
    def setUp(self):
        self.was = O.KILL_WEIGHT
        O.KILL_WEIGHT = True

    def tearDown(self):
        O.KILL_WEIGHT = self.was

    def test_file_is_sane(self):
        self.assertIn("Decay", KW)
        for n, r in KW.items():
            self.assertTrue(0.2 < r["weight"] < 2.0, n)
            self.assertGreater(r["holders"], 0, n)
            # shrinkage pulls toward 1, never past the raw estimate
            self.assertLessEqual(abs(r["weight"] - 1), abs(r["raw"] - 1) + 1e-9, n)

    def test_decay_counts_less_than_its_damage(self):
        self.assertLess(KW["Decay"]["weight"], 0.7)

    def test_cut_only_touches_items(self):
        by = {"gun": 1000.0, "Decay": 300.0, "Some Ability": 200.0}
        self.assertAlmostEqual(O.kill_cut(by), (1 - KW["Decay"]["weight"]) * 300.0)
        r = {"damage_dealt": 1500.0, "damage_by_source": by, "enemy_healed": 100.0}
        self.assertAlmostEqual(O.net_damage(r), 1400.0 - O.kill_cut(by))

    def test_switch_off(self):
        O.KILL_WEIGHT = False
        self.assertEqual(O.kill_cut({"Decay": 300.0}), 0.0)
        r = {"damage_dealt": 1500.0, "damage_by_source": {"Decay": 300.0}}
        self.assertEqual(O.net_damage(r), 1500.0)

    def test_area_and_splash_are_weighted(self):
        r = {"damage_by_source": {"Mystic Reverb": 100.0}, "splash_dealt": 50.0,
             "splash_by_source": {"Ricochet": 50.0}}
        on = O.area_damage(r, 27000)
        O.KILL_WEIGHT = False
        off = O.area_damage(r, 27000)
        k = O.area_extra("Mystic Reverb", 27000)
        self.assertAlmostEqual(off - on, 100.0 * k * (1 - KW["Mystic Reverb"]["weight"])
                               + 50.0 * (1 - KW["Ricochet"]["weight"]), places=6)


if __name__ == "__main__":
    unittest.main()
