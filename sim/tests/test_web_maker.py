"""web/bridge.py maker(): the build maker's fights (you vs each enemy, both fighting back, both refilling)."""
import json
import os
import sys
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

    def test_utility_names_are_items(self):
        from deadsim.data import game
        names = {i.name for i in game().items.values()}
        tags = {"cc", "slow", "mobility", "escape", "team", "aoe", "antiheal", "cleanse", "stealth", "reach", "farm"}
        for name, t in json.load(open(UTILITY)).items():
            if name.startswith("_"):
                continue
            self.assertIn(name, names)
            self.assertTrue(set(t) <= tags, name)


if __name__ == "__main__":
    unittest.main()
