"""Checks of the full game build path logic (damage/scripts/game_path.py). Run from sim/: python3 -m unittest discover -s tests"""
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

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


class FakeEv:
    """Fight value = souls held, so cheaper-per-value pieces still come in a fixed order."""
    def run(self, items, pool="F", detail=False):
        return float(S.cost(list(items)))


class FakeCtx:
    hero = G.hero("Haze").id
    cand = {10000: [ID[n] for n in ("Extra Spirit", "Extra Stamina", "Extra Health", "Rapid Rounds", "Spirit Strike",
                                     "Kinetic Dash", "Decay", "Mystic Burst", "Extra Regen")]}

    def evaluator(self, b):
        return FakeEv()


class BuyOrder(unittest.TestCase):
    def stages(self):
        st, kd, dec, xs = ID["Extra Stamina"], ID["Kinetic Dash"], ID["Decay"], ID["Extra Spirit"]
        return [{"budget": 10000, "items": [st, xs], "sold": [], "waste": 0.0},
                {"budget": 18000, "items": [kd, dec], "sold": [xs], "waste": P.REFUND * G.items[xs].cost}]

    def test_order_ends_holding_each_stage_and_sales_match(self):
        st = self.stages()
        order = P.buy_order(FakeCtx(), st)
        held = []
        for s in order:
            if "sell" in s:
                stage = next(x for x in st if x["budget"] == s["stage"])
                self.assertEqual(sorted(s["sell"]), sorted(stage["sold"]))
                self.assertEqual(s["refund"], round(P.REFUND * S.cost(s["sell"])))
                held = [i for i in held if i not in s["sell"]]
            else:
                held = [i for i in held if i not in s["replaces"]] + [s["item"]]
                self.assertLessEqual(s["net_worth"], s["stage"])
            stage = next(x for x in st if x["budget"] == s["stage"])
            if s is order[-1] or order[order.index(s) + 1]["stage"] != s["stage"]:
                self.assertEqual(sorted(held), sorted(stage["items"]))

    def test_each_threshold_is_listed_once(self):
        order = P.buy_order(FakeCtx(), self.stages())
        seen = [(x["slot"], x["at"]) for s in order for x in s.get("spikes", [])]
        self.assertEqual(len(seen), len(set(seen)))


class StageSearch(unittest.TestCase):
    def test_stage_builds_fit_and_keep_or_sell_the_kept_items(self):
        kept = [ID["Extra Spirit"], ID["Extra Stamina"]]
        res = P.stage_search(FakeCtx(), 10000, kept, 400.0, kept)
        self.assertGreater(len(res), 0)
        for adj, sc, items, sold, waste in res:
            self.assertTrue(S.valid(items, P.item_budget(10000)))
            self.assertLessEqual(S.cost(items) + waste, P.item_budget(10000))
            self.assertAlmostEqual(waste, 400.0 + P.REFUND * S.cost(sold))
            self.assertEqual(sold, P.sold_items(kept, items))
            self.assertAlmostEqual(adj, sc - P.SELL_MARGIN * len(sold))


class Export(unittest.TestCase):
    def test_rerun_keeps_other_brackets_and_unfinished_heroes(self):
        import export_path as E
        with tempfile.TemporaryDirectory() as d:
            out, jobs = os.path.join(d, "out"), lambda br: os.path.join(d, "jobs_" + br)
            os.makedirs(os.path.join(out, "heroes"))
            old = {"brackets": [{"id": "phantom", "label": "x", "patch": "old", "generated": "t0"},
                                {"id": "eternus", "label": "y", "patch": "old", "generated": "t0"}],
                   "heroes": {"1": {"name": "Infernus", "brackets": {"phantom": {"path_score": 1.1}, "eternus": {"path_score": 1.2}}},
                              "13": {"name": "Haze", "brackets": {"phantom": {"path_score": 1.3}}}}}
            with open(os.path.join(out, "index.json"), "w") as f:
                json.dump(old, f)
            os.makedirs(jobs("phantom"))
            with open(os.path.join(jobs("phantom"), "13.json"), "w") as f:
                json.dump({"hero_id": 13, "hero": "Haze", "path_score": 2.0, "stage_scores": [2.0], "start": "best_10k"}, f)
            with mock.patch.object(E, "OUT", out), mock.patch.object(E, "jobs_dir", jobs), \
                    mock.patch.object(E.patch_state, "load", lambda: {"patch": "new"}):
                E.main()
            with open(os.path.join(out, "index.json")) as f:
                idx = json.load(f)
            self.assertEqual(idx["heroes"]["13"]["brackets"]["phantom"]["path_score"], 2.0)
            self.assertEqual(idx["heroes"]["1"]["brackets"]["phantom"]["path_score"], 1.1)   # unfinished: kept
            self.assertEqual(idx["heroes"]["1"]["brackets"]["phantom"]["patch"], "old")
            self.assertEqual(idx["heroes"]["1"]["brackets"]["eternus"]["path_score"], 1.2)   # other tier: kept
            self.assertEqual({b["id"]: b["patch"] for b in idx["brackets"]}, {"phantom": "new", "eternus": "old"})
            self.assertTrue(os.path.exists(os.path.join(out, "heroes", "13_phantom.json")))


if __name__ == "__main__":
    unittest.main()
