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


class Lift(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump({"items": ROWS, "heroes": {}}, self.tmp)
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


if __name__ == "__main__":
    unittest.main()
