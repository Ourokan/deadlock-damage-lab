"""Uncut items' fight-length correction (accuracy.CAP_AFTER_LENGTH, 2026-10-27): an item with landing >= 1 and
length_corr < 1 gets min(1, landing x length_corr); corrections above 1, cut items, small samples and Return Fire
(LENGTH_CAP_SKIP) keep the old factor; item_landing_heroes.fit_pooled refits a lifted row on the combined factor.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from deadsim import accuracy  # noqa: E402
import item_landing_heroes as ILH  # noqa: E402

ROWS = {
    "a": {"name": "Phantom Strike", "holders": 100, "landing": 1.205, "length_corr": 0.482},
    "b": {"name": "Arctic Blast", "holders": 100, "landing": 2.5, "length_corr": 0.536},
    "c": {"name": "Spirit Burn", "holders": 100, "landing": 1.2, "length_corr": 1.528},
    "d": {"name": "Toxic Bullets", "holders": 100, "landing": 0.53, "length_corr": 0.8},
    "e": {"name": "Return Fire", "holders": 100, "landing": 3.754, "length_corr": 0.622},
    "f": {"name": "Rare Item", "holders": 10, "landing": 1.5, "length_corr": 0.5},
}


HEROES = {"Vyper": {"Toxic Bullets": {"holders": 50, "real_over_sim": 1.2, "landing": 1.1},
                    "Return Fire": {"holders": 50, "real_over_sim": 1.2, "landing": 1.5}},
          "Wraith": {"Toxic Bullets": {"holders": 50, "real_over_sim": 1.2, "landing": 2.0}},
          "Ivy": {"Toxic Bullets": {"holders": 50, "real_over_sim": 0.9, "landing": 0.9}}}


class Lift(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump({"items": ROWS, "heroes": HEROES, "meta": {}}, self.tmp)
        self.tmp.close()
        self.old = accuracy.ITEM_LANDING, accuracy.CAP_AFTER_LENGTH
        accuracy.ITEM_LANDING, accuracy.CAP_AFTER_LENGTH = self.tmp.name, True

    def tearDown(self):
        accuracy.ITEM_LANDING, accuracy.CAP_AFTER_LENGTH = self.old
        os.unlink(self.tmp.name)

    def test_lifted_rows_get_the_capped_product(self):
        c = accuracy.item_length_corr()
        self.assertAlmostEqual(c["Phantom Strike"], 1.205 * 0.482)
        self.assertEqual(c["Arctic Blast"], 1.0)

    def test_others_keep_their_correction(self):
        c = accuracy.item_length_corr()
        self.assertEqual(c["Spirit Burn"], 1.528)   # lifts above 1 stay
        self.assertEqual(c["Toxic Bullets"], 0.8)   # cut item: landing x corr in fight.py, not here
        self.assertEqual(c["Return Fire"], 0.622)   # LENGTH_CAP_SKIP
        self.assertNotIn("Rare Item", c)
        self.assertFalse(accuracy.lifted(ROWS["f"]))
        self.assertEqual(accuracy.item_landing()["Toxic Bullets"], 0.53)
        self.assertNotIn("Phantom Strike", accuracy.item_landing())

    def test_off_restores_the_old_factor(self):
        accuracy.CAP_AFTER_LENGTH = False
        self.assertEqual(accuracy.item_length_corr()["Phantom Strike"], 0.482)

    def test_fit_pooled_refits_lifted_rows_on_the_product(self):
        def audit(r):
            return {"items": {"a": {"name": "Phantom Strike", "holders": 10 ** 6, "real_over_sim": r}}}
        d = ILH.fit_pooled(audit(0.8), {"Phantom Strike"})
        self.assertAlmostEqual(d["items"]["a"]["landing"], round(1.205 * 0.8, 3), places=2)   # below 1: a cut
        d = ILH.fit_pooled(audit(1.5), {"Phantom Strike"})
        self.assertAlmostEqual(d["items"]["a"]["landing"], round(1.205 * 1.5, 3), places=2)   # stays above 1
        d = ILH.fit_pooled(audit(9.0), {"Phantom Strike"})
        self.assertAlmostEqual(d["items"]["a"]["landing"], round(1 / 0.482, 3), places=3)     # product capped at 1


    def test_hero_rows_above_one_lift_past_the_pooled_correction(self):
        # accuracy.HERO_LENGTH_LIFT (2026-11-08): a hero row above 1 gives min(1, landing x pooled length_corr)
        self.assertAlmostEqual(accuracy.item_length_corr("Vyper")["Toxic Bullets"], 1.1 * 0.8)
        self.assertEqual(accuracy.item_length_corr("Wraith")["Toxic Bullets"], 1.0)
        self.assertEqual(accuracy.item_length_corr("Ivy")["Toxic Bullets"], 0.8)     # row below 1: a plain cut
        self.assertEqual(accuracy.item_length_corr("Vyper")["Return Fire"], 0.622)   # LENGTH_CAP_SKIP
        self.assertEqual(accuracy.item_length_corr()["Toxic Bullets"], 0.8)
        self.assertEqual(accuracy.item_landing("Vyper")["Toxic Bullets"], 1.0)
        old = accuracy.HERO_LENGTH_LIFT
        try:
            accuracy.HERO_LENGTH_LIFT = False
            self.assertEqual(accuracy.item_length_corr("Wraith")["Toxic Bullets"], 0.8)
        finally:
            accuracy.HERO_LENGTH_LIFT = old

    def test_hero_fit_goes_up_to_one_over_the_correction(self):
        def audit(hero, r):
            return {"meta": {"sample": "t"}, "hero_items": [{"hero": hero, "item": "Toxic Bullets", "holders": 10 ** 6,
                                                            "real_over_sim": r}]}
        d = ILH.fit(audit("Vyper", 1.1), items={"Toxic Bullets"})
        self.assertAlmostEqual(d["heroes"]["Vyper"]["Toxic Bullets"]["landing"], round(1.1 * 1.1, 3), places=2)
        d = ILH.fit(audit("Vyper", 9.0), items={"Toxic Bullets"})
        self.assertAlmostEqual(d["heroes"]["Vyper"]["Toxic Bullets"]["landing"], round(1 / 0.8, 3), places=3)
        d = ILH.fit(audit("Wraith", 0.5), items={"Toxic Bullets"})   # the audit saw the capped product 1 / 0.8
        self.assertAlmostEqual(d["heroes"]["Wraith"]["Toxic Bullets"]["landing"], round(0.5 / 0.8, 3), places=2)
        d = ILH.fit(audit("Ivy", 0.5), items={"Toxic Bullets"})      # below 1 stays a plain landing
        self.assertAlmostEqual(d["heroes"]["Ivy"]["Toxic Bullets"]["landing"], 0.45, places=2)


    def test_hero_fit_without_a_row_starts_from_the_pooled_factor(self):
        def audit(r):
            return {"meta": {"sample": "t"}, "hero_items": [{"hero": "Shiv", "item": "Phantom Strike", "holders": 10 ** 6,
                                                            "real_over_sim": r}]}
        d = ILH.fit(audit(1.1), items={"Phantom Strike"})   # lifted pooled row: 1.205 x 0.482 = 0.581 seen
        self.assertAlmostEqual(d["heroes"]["Shiv"]["Phantom Strike"]["landing"], round(1.205 * 1.1, 3), places=2)
        d = ILH.fit(audit(0.9), items={"Phantom Strike"})
        self.assertAlmostEqual(d["heroes"]["Shiv"]["Phantom Strike"]["landing"], round(1.205 * 0.9, 3), places=2)

    def test_hero_and_item_keep_other_heroes_rows(self):
        a = {"meta": {"sample": "t"}, "hero_items": [{"hero": "Vyper", "item": "Toxic Bullets", "holders": 10 ** 6,
                                                      "real_over_sim": 1.0}]}
        d = ILH.fit(a, only={"Vyper"}, items={"Toxic Bullets"})
        self.assertEqual(d["heroes"]["Wraith"]["Toxic Bullets"]["landing"], 2.0)
        self.assertEqual(d["heroes"]["Ivy"]["Toxic Bullets"]["landing"], 0.9)


if __name__ == "__main__":
    unittest.main()
