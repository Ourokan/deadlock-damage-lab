"""Checks of the item tier caps (search/scripts/build_pool.py TIER_STEPS): builds hold no more expensive items than
real players of the bracket do at that net worth. Run from sim/: python3 -m unittest discover -s tests"""
import os
import sys
import unittest
from collections import Counter

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "damage")]

import build_pool as P  # noqa: E402
import buy_order as B  # noqa: E402
import search as S  # noqa: E402

G = S.G()
ID = {it.name: it.id for it in G.items.values()}


class Caps(unittest.TestCase):
    def setUp(self):
        self.saved = dict(P._caps)
        for br in (P.PRIMARY, S.BRACKET):
            P._caps[br] = P.DEFAULT_TIER_CAPS

    def tearDown(self):
        P._caps.clear()
        P._caps.update(self.saved)

    def test_quantile_cap(self):
        self.assertEqual(P.quantile_cap(Counter({0: 91, 1: 9})), 0)
        self.assertEqual(P.quantile_cap(Counter({0: 89, 1: 11})), 1)
        self.assertEqual(P.quantile_cap(Counter({2: 5})), 2)

    def test_caps_follow_the_budget(self):
        self.assertEqual(P.caps_for_limit(P.item_budget(18000)), P.DEFAULT_TIER_CAPS[18000])
        self.assertEqual(P.caps_for_limit(P.item_budget(27000) + 100), P.DEFAULT_TIER_CAPS[27000])
        self.assertEqual(P.caps_for_limit(500), P.DEFAULT_TIER_CAPS[10000])
        self.assertIsNone(P.caps_for_limit(10 ** 9))

    def test_no_tier4_item_at_18k(self):
        mm, lim = ID["Mercurial Magnum"], P.item_budget(18000)
        self.assertEqual(G.items[mm].cost, 6400)
        self.assertFalse(S.valid([mm], lim))
        self.assertTrue(S.valid([mm], P.item_budget(27000)))
        self.assertTrue(S.valid([mm], 10 ** 9))   # the search's uncapped item value scan
        self.assertNotIn(mm, S.candidates(lim, {}))

    def test_tier3_count_capped(self):
        t3 = [it.id for it in G.items.values() if it.cost == 3200 and not it.components][:4]
        lim = P.item_budget(18000)
        self.assertTrue(S.valid(t3[:3], lim))
        self.assertFalse(S.valid(t3, lim))

    def test_buy_order_waits_for_the_caps(self):
        mm, es = ID["Mercurial Magnum"], ID["Extra Spirit"]
        self.assertEqual(B.cap_net_worth([es]), 0)
        self.assertEqual(B.cap_net_worth([mm]), 27000)

        class Stub:
            def dmg(self, items, nw):   # Magnum is worth far more per soul, but can't be held before 27k
                v = sum(1000.0 if i == mm else 10.0 for i in items)
                return {o: v for o in ("burst_5s", "fight_15s", "sustained_30s")}

        steps = B.plan(Stub(), [mm, es], "fight_15s")
        self.assertEqual([s["item"] for s in steps][-1], mm)
        self.assertGreaterEqual(steps[-1]["net_worth"], 27000)
        self.assertEqual([s["net_worth"] for s in steps], sorted(s["net_worth"] for s in steps))


if __name__ == "__main__":
    unittest.main()
