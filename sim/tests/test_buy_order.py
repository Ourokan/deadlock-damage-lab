"""Checks of the item buy order logic (damage/scripts/buy_order.py). Run from sim/: python3 -m unittest discover -s tests"""
import json
import os
import sys
import tempfile
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


class StubPath:
    """Damage = 100 per target item held plus 10 per component, at any net worth."""
    def __init__(self, target):
        self.target = set(target)

    def dmg(self, items, nw):
        v = sum(100.0 if i in self.target else 10.0 for i in items)
        return {o: v for o in ("burst_5s", "fight_15s", "sustained_30s")}


class Plan(unittest.TestCase):
    def test_ends_with_exactly_the_target_at_its_cost(self):
        target = [ID["Mercurial Magnum"], ID["Decay"], ID["Escalating Exposure"], ID["Extra Spirit"]]
        steps = B.plan(StubPath(target), target, "fight_15s")
        held = []
        for s in steps:
            held = [i for i in held if i not in s["replaces"]] + [s["item"]]
        self.assertEqual(sorted(held), sorted(target))
        self.assertEqual(steps[-1]["spent"], S.cost(target))   # components are credited, never paid twice
        self.assertEqual([s["spent"] for s in steps], sorted(s["spent"] for s in steps))

    def test_item_cap_raises_instead_of_a_partial_order(self):
        target = [ID["Decay"], ID["Extra Spirit"]]
        old, S.MAX_ITEMS = S.MAX_ITEMS, 1
        try:
            with self.assertRaises(RuntimeError):
                B.plan(StubPath(target), target, "fight_15s")
        finally:
            S.MAX_ITEMS = old


class Inputs(unittest.TestCase):
    def test_published_results_only_on_request(self):
        old_root, old_flag = B.ROOT, B.USE_PUBLISHED
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "out", "heroes"))
            with open(os.path.join(d, "out", "heroes", "13.json"), "w") as f:
                json.dump({"budgets": {str(b): {"dummy_hp": 1} for b in BUDGETS}}, f)
            B.ROOT = d
            try:
                B.USE_PUBLISHED = False
                self.assertEqual(B.search_results(13), {})
                B.USE_PUBLISHED = True
                self.assertEqual(sorted(B.search_results(13)), BUDGETS)
            finally:
                B.ROOT, B.USE_PUBLISHED = old_root, old_flag

    def test_dummy_hp_interpolates_between_budgets(self):
        p = B.Path(13, {10000: {"dummy_hp": 1000}, 18000: {"dummy_hp": 2000}})
        self.assertEqual(p.hp(5000), 1000)
        self.assertEqual(p.hp(14000), 1500)
        self.assertEqual(p.hp(60000), 2000)


if __name__ == "__main__":
    unittest.main()
