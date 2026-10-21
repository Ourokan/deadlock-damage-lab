"""web/bridge.py maker(): the build maker's fights (you vs each enemy, both fighting back, both refilling)."""
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
sys.path[:0] = [os.path.join(HERE, ".."), os.path.join(HERE, "..", "..", "damage"), os.path.join(HERE, "..", "..", "web")]

import bridge  # noqa: E402

UTILITY = os.path.join(HERE, "..", "..", "web", "maker_utility.json")


class TestMaker(unittest.TestCase):
    def run_maker(self, variants, enemies):
        req = {"hero": "Haze", "souls": 18000, "enemies": enemies, "variants": variants}
        return json.loads(bridge.maker(json.dumps(req)))["variants"]

    def test_fights_each_enemy_and_is_repeatable(self):
        enemies = [{"hero": "Abrams", "items": ["Extra Health"], "souls": 18000}, {"hero": "Seven", "items": [], "souls": 18000}]
        a = self.run_maker([["Extra Spirit"], ["Extra Spirit"]], enemies)
        self.assertEqual(len(a), 2)
        self.assertEqual(len(a[0]), 2)
        self.assertEqual(a[0], a[1])
        for r in a[0]:
            self.assertGreater(r["dealt"], 0)
            self.assertGreater(r["taken"], 0)
            self.assertGreater(r["ttk"], 0)
            self.assertGreater(r["ttd"], 0)

    def test_health_makes_you_last_longer(self):
        enemies = [{"hero": "Haze", "items": ["Rapid Rounds"], "souls": 18000}]
        base, tank = self.run_maker([[], ["Extra Health", "Bullet Resilience"]], enemies)
        self.assertGreater(tank[0]["ttd"], base[0]["ttd"])

    def test_kill_time_extrapolates_from_hp_lost(self):
        # an empty early Haze can't kill a tanky Abrams in 15 s: the time comes from the HP it really took off
        enemies = [{"hero": "Abrams", "items": ["Extra Health", "Bullet Resilience", "Spirit Resilience"], "souls": 18000}]
        r = self.run_maker([[]], enemies)[0][0]
        self.assertGreater(r["ttk"], 15)
        self.assertLessEqual(r["ttk"], 999)
        # never faster than the raw damage alone could do it
        self.assertGreaterEqual(r["ttk"], 15 * r["enemy_hp"] / r["dealt"] - 1e-6)

    def test_lethal_fight_reports_first_kill(self):
        enemies = [{"hero": "Haze", "items": [], "souls": 1}]
        r = self.run_maker([["Mercurial Magnum", "Toxic Bullets", "Burst Fire", "Tesla Bullets"]], enemies)[0][0]
        self.assertLess(r["ttk"], 15)

    def test_utility_names_are_items(self):
        from deadsim.data import game
        names = {i.name for i in game().items.values()}
        tags = {"cc", "slow", "mobility", "escape", "team", "aoe", "antiheal", "cleanse", "stealth", "reach", "farm"}
        names |= {x["name"] for x in json.load(open(os.path.join(HERE, "..", "..", "data", "game", "shop_items.json")))}
        for name, t in json.load(open(UTILITY)).items():
            if name.startswith("_"):
                continue
            self.assertIn(name, names)
            self.assertTrue(set(t) <= tags, name)


class TestMakerData(unittest.TestCase):
    def test_export_usage(self):
        sys.path[:0] = [os.path.join(HERE, "..", "..", "search", "scripts"), os.path.join(HERE, "..", "..", "data")]
        import export
        from deadsim.data import game
        g = game()
        hero, item = sorted(g.heroes)[0], next(i for i in g.items.values() if i.cost > 0).id
        tmp = tempfile.mkdtemp()
        old = export.ROOT, export.OUT
        try:
            export.ROOT, export.OUT = tmp, os.path.join(tmp, "out")
            os.makedirs(os.path.join(tmp, "work")); os.makedirs(export.OUT)
            json.dump({"27000": {str(hero): {"_n": 100, str(item): 40, "1": 90}}},
                      open(os.path.join(tmp, "work", "item_usage_phantom.json"), "w"))
            self.assertEqual(export.export_usage(g), ["phantom"])
            cell = json.load(open(os.path.join(export.OUT, "usage.json")))["phantom"]["27000"]
            self.assertEqual(cell["heroes"][str(hero)]["items"], {str(item): 0.4})   # unknown item id dropped
            self.assertTrue(cell["caps"])
        finally:
            export.ROOT, export.OUT = old
            shutil.rmtree(tmp)

    def test_maker_data_skips_unknown_utility_names(self):
        import build
        tmp = tempfile.mkdtemp()
        old = build.WEB
        try:
            os.makedirs(os.path.join(tmp, "data"))
            json.dump({"Extra Stamina": {"mobility": 1}, "No Such Item": {"cc": 1}}, open(os.path.join(tmp, "maker_utility.json"), "w"))
            build.WEB = tmp
            build.maker_data()
            d = json.load(open(os.path.join(tmp, "data", "maker.json")))
            self.assertEqual(list(d["utility"].values()), [{"mobility": 1}])
            self.assertTrue(d["components"])
            self.assertIn("6", d["hero_cc"])   # Abrams: Shoulder Charge
        finally:
            build.WEB = old
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
