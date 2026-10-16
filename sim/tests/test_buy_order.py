"""Checks of the item buy order logic (damage/scripts/buy_order.py). Run from sim/: python3 -m unittest discover -s tests"""
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "damage")]

import buy_order as B  # noqa: E402
import search as S  # noqa: E402
from build_pool import BUDGETS, item_budget  # noqa: E402

G = S.G()
ID = {it.name: it.id for it in G.items.values()}


class NetWorth(unittest.TestCase):
    def test_lowest_net_worth_that_covers_the_spend(self):
        for spend in (800, 3200, 15600, 30000, item_budget(50000)):
            nw = B.net_worth_for(spend)
            self.assertEqual(nw % B.NW_STEP, 0)
            self.assertGreaterEqual(item_budget(nw), spend)
            self.assertLess(item_budget(nw - B.NW_STEP), spend)

    def test_milestone_budgets_map_back_to_themselves(self):
        for b in BUDGETS:
            self.assertLessEqual(B.net_worth_for(item_budget(b)), b)


class Upgrades(unittest.TestCase):
    def test_upgrade_credits_the_held_component(self):
        qr, mm = ID["Quicksilver Reload"], ID["Mercurial Magnum"]
        new, paid = B.after_buy([qr], mm)
        self.assertEqual(new, [mm])
        self.assertEqual(paid, G.items[mm].cost - G.items[qr].cost)

    def test_buying_without_the_component_pays_full_price(self):
        mm, dec = ID["Mercurial Magnum"], ID["Decay"]
        new, paid = B.after_buy([dec], mm)
        self.assertEqual(sorted(new), sorted([dec, mm]))
        self.assertEqual(paid, G.items[mm].cost)


class Milestones(unittest.TestCase):
    def test_holdings_follow_the_steps_and_upgrades(self):
        qr, mm, dec = ID["Quicksilver Reload"], ID["Mercurial Magnum"], ID["Decay"]

        class FakePath:
            def dmg(self, items, nw):
                return {o: float(len(items)) for o in ("burst_5s", "fight_15s", "sustained_30s")}

        steps = [{"item": qr, "replaces": [], "spent": 1600},
                 {"item": dec, "replaces": [], "spent": 4800},
                 {"item": mm, "replaces": [qr], "spent": 9600},
                 {"item": ID["Focus Lens"], "replaces": [], "spent": item_budget(50000)}]
        m = B.milestones(FakePath(), {}, steps, "fight_15s")
        self.assertEqual(sorted(m["10000"]["items"]), sorted([qr, dec]))   # 9600 > 8350 item budget at 10k
        self.assertEqual(sorted(m["18000"]["items"]), sorted([mm, dec]))
        self.assertEqual(len(m["50000"]["items"]), 3)
        self.assertIsNone(m["10000"]["share_of_best"])


if __name__ == "__main__":
    unittest.main()
