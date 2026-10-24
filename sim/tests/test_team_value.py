"""Checks of the overall score's team value (damage/scripts/overall_search.py): real teammates / other enemies in
reach from data/team_value.json, area items' hits on the other enemies, ally items' multiplier.
Run from sim/: python3 -m unittest discover -s tests"""
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "damage", "survival")]

import overall_search as O  # noqa: E402

G = O.S.G()
ID = {it.name: it.id for it in G.items.values()}


class Near(unittest.TestCase):
    def test_counts_grow_with_radius(self):
        for kind in ("allies", "any_ally", "extra", "extra_self"):
            self.assertLess(O.near(kind, 8, 27000), O.near(kind, 30, 27000))

    def test_interpolates_between_bins(self):
        lo, hi = O.near("allies", 35, 18000), O.near("allies", 35, 27000)
        self.assertTrue(min(lo, hi) <= O.near("allies", 35, 22000) <= max(lo, hi))
        self.assertAlmostEqual(O.near("extra", 15.5, 27000),
                               (O.near("extra", 15, 27000) + O.near("extra", 16, 27000)) / 2, places=6)


class AreaDamage(unittest.TestCase):
    def test_area_item_damage_counts_on_the_other_enemies(self):
        r = {"damage_by_source": {"gun": 1000.0, "Mystic Reverb": 200.0, "Scourge": 100.0}, "splash_dealt": 30.0}
        want = 200 * O.near("extra", 16, 27000) + 100 * O.near("extra_self", 10, 27000) + 30
        self.assertAlmostEqual(O.area_damage(r, 27000), want, places=6)

    def test_ricochet_bounces_in_the_overall_fight(self):
        h, e = G.hero("Haze").id, G.hero("Abrams").id
        with_ = O.fight(h, [ID["Ricochet"]], e, [], 27000)[0]
        without = O.fight(h, [], e, [], 27000)[0]
        self.assertGreater(with_, without)


class AllyItems(unittest.TestCase):
    def test_ally_items_raise_the_score(self):
        self.assertEqual(O.team_value([ID["Extra Health"]], 27000), 1.0)
        for name in ("Healing Nova", "Heroic Aura", "Divine Barrier"):
            self.assertGreater(O.team_value([ID[name]], 27000), 1.0, name)

    def test_values_add(self):
        a, b = ID["Healing Nova"], ID["Heroic Aura"]
        both = O.team_value([a, b], 27000) - 1
        self.assertAlmostEqual(both, O.team_value([a], 27000) - 1 + O.team_value([b], 27000) - 1, places=6)


if __name__ == "__main__":
    unittest.main()
