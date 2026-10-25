"""Per-hero item damage factors (item_landing.json "heroes", scripts/item_landing_heroes.py) replace the pooled factor
for that hero only, inside the same 0.25-1 cap. Run from sim/:
    python3 -m unittest discover -s tests
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from deadsim import accuracy  # noqa: E402
from deadsim.accuracy import hero_default_skill, item_landing  # noqa: E402
import item_landing_heroes as H  # noqa: E402


class HeroItemLanding(unittest.TestCase):
    def test_hero_rows_override_pooled(self):
        heroes = json.load(open(accuracy.ITEM_LANDING)).get("heroes", {})
        self.assertTrue(heroes)
        pooled = item_landing()
        for hero, rows in heroes.items():
            own = item_landing(hero)
            for name, r in rows.items():
                self.assertAlmostEqual(own[name], max(0.25, min(1.0, r["landing"])))
            for name, v in pooled.items():
                if name not in rows:
                    self.assertEqual(own[name], v)

    def test_skill_uses_hero_rows(self):
        hero, rows = next(iter(json.load(open(accuracy.ITEM_LANDING))["heroes"].items()))
        sk = hero_default_skill(hero, counterplay=True)
        name, r = next(iter(rows.items()))
        self.assertAlmostEqual(sk.item_landing[name], max(0.25, min(1.0, r["landing"])))

    def test_switch_off(self):
        accuracy.HERO_ITEM_LANDING = False
        try:
            self.assertEqual(item_landing("Graves"), item_landing())
        finally:
            accuracy.HERO_ITEM_LANDING = True

    def test_fit_shrinks_and_caps(self):
        cur = item_landing("Graves").get("Torment Pulse", 1.0)
        audit = {"meta": {"sample": "x"}, "hero_items": [
            {"hero": "Graves", "item": "Torment Pulse", "holders": 20, "real_over_sim": 0.5},
            {"hero": "Shiv", "item": "Torment Pulse", "holders": 50, "real_over_sim": 5.0}]}
        d = H.fit(audit, prior=20)
        self.assertAlmostEqual(d["heroes"]["Graves"]["Torment Pulse"]["landing"], round(cur * 0.5 ** 0.5, 3), places=3)
        self.assertEqual(d["heroes"]["Shiv"]["Torment Pulse"]["landing"], 1.0)


if __name__ == "__main__":
    unittest.main()
