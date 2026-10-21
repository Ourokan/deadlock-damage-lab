"""Checks of the full game build path logic (damage/scripts/game_path.py). Run from sim/: python3 -m unittest discover -s tests"""
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "damage")]

import game_path as P  # noqa: E402

S = P.S
G = S.G()
ID = {it.name: it.id for it in G.items.values()}


class Ownership(unittest.TestCase):
    def test_upgrading_a_held_component_is_not_a_sale(self):
        qr, mm = ID["Quicksilver Reload"], ID["Mercurial Magnum"]
        self.assertEqual(P.with_item([qr], mm), [mm])
        self.assertEqual(P.sold_items([qr], [mm]), [])

    def test_dropping_an_item_is_a_sale(self):
        qr, dec = ID["Quicksilver Reload"], ID["Decay"]
        self.assertEqual(P.sold_items([qr, dec], [dec]), [qr])


class Score(unittest.TestCase):
    def test_weakest_stage_counts_twice(self):
        self.assertAlmostEqual(P.path_score([1.0, 1.0, 1.0]), 1.0)
        # same mean, but the even path wins over one with a weak stage
        self.assertGreater(P.path_score([1.2, 1.2, 1.2]), P.path_score([0.9, 1.3, 1.4]))


class Spikes(unittest.TestCase):
    def test_threshold_crossings(self):
        h = G.hero("Haze")
        got = P.crossed(h, {"weapon": 3200, "vitality": 0, "spirit": 0}, {"weapon": 4800, "vitality": 800, "spirit": 0})
        self.assertIn({"slot": "weapon", "at": 4800, "bonus": dict(h.invest["weapon"])[4800]}, got)
        self.assertIn("vitality", {x["slot"] for x in got})
        self.assertNotIn(3200, [x["at"] for x in got if x["slot"] == "weapon"])

    def test_slot_spend_counts_item_costs(self):
        qr = ID["Quicksilver Reload"]
        inv = P.invest([qr])
        self.assertEqual(inv[G.items[qr].slot], G.items[qr].cost)


if __name__ == "__main__":
    unittest.main()
