"""Checks of the overall score's death cost (damage/scripts/overall_search.py death_value, sim/data/death_cost.json)
and Healing Tempo's heal buff (deadsim items_fx.HealingTempo).
Run from sim/: python3 -m unittest discover -s tests"""
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "survival")]

import overall_search as O  # noqa: E402
from deadsim import items_fx  # noqa: E402


class DeathCost(unittest.TestCase):
    def setUp(self):
        self.was = O.DEATH_COST, O.DEATH_BOUNTY
        O.DEATH_COST = True

    def tearDown(self):
        O.DEATH_COST, O.DEATH_BOUNTY = self.was

    def test_file_is_sane(self):
        d = O.death_data()
        rs = [r for _, r in d["respawn_s"]]
        self.assertEqual(rs, sorted(rs))          # respawn grows with net worth
        self.assertTrue(5 < rs[0] < 15 and 70 < rs[-1] < 100)
        for ph in ("lane", "mid", "late"):
            row = d["phases"][ph]
            self.assertTrue(0.05 < row["deaths_per_engagement"] < 0.5, ph)
            self.assertTrue(20 < row["alive_s_per_engagement"] < 150, ph)
        for h, row in d["heroes"].items():
            self.assertTrue(0.6 < row["ratio"] < 1.6, h)

    def test_death_costs_more_late(self):
        self.assertLess(O.death_seconds(3000), O.death_seconds(27000))
        O.DEATH_BOUNTY = 0.0
        self.assertAlmostEqual(O.death_seconds(200000), O.death_data()["respawn_s"][-1][1]
                               + O.death_data()["phases"]["late"]["walk_back_s"])

    def test_value(self):
        self.assertAlmostEqual(O.death_value(0.3, 0.3, 1, 27000), 1.0)
        self.assertGreater(O.death_value(0.1, 0.3, 1, 27000), 1.0)
        self.assertLess(O.death_value(0.5, 0.3, 1, 27000), 1.0)
        # never dying is worth at most the whole real death share of the game
        row = O.death_data()["phases"]["late"]
        cap = 1 + row["deaths_per_engagement"] * 2 * O.death_seconds(30000) / row["alive_s_per_engagement"]
        self.assertLess(O.death_value(0.0, 0.3, 1, 30000), cap)
        # lane fights have no death chance: neutral
        self.assertAlmostEqual(O.death_value(0.0, 0.0, 1, 5000), 1.0)
        O.DEATH_COST = False
        self.assertEqual(O.death_value(0.1, 0.3, 1, 27000), 1.0)

    def test_chance_follows_real_fight_length(self):
        self.assertEqual(O.death_chance({"survived": True, "time_alive": 30.0}, 27000), 0.0)
        early = O.death_chance({"survived": False, "time_alive": 3.0}, 27000)
        late = O.death_chance({"survived": False, "time_alive": 20.0}, 27000)
        self.assertTrue(0.8 < early <= 1.0 and late < 0.2, (early, late))


class HealingTempo(unittest.TestCase):
    def test_heal_grants_the_buff_and_regen_does_not(self):
        g = O.S.G()
        it = g.items_by_name["healing tempo"]

        class Mods:
            def __init__(self):
                self.added = []

            def add(self, key, value, duration, tag):
                self.added.append((key, value, duration))

        class E:
            t = 0.0

        class St:
            item_cdr = duration_pct = 0.0

        class F:
            def __init__(self):
                self.e, self.mods, self.st = E(), Mods(), St()

        f = F()
        fx = items_fx.HealingTempo(it, f)
        fx.on_healed(f, 0.5)                      # below MinimumHealAmount
        self.assertEqual(f.mods.added, [])
        fx.on_healed(f, 50.0)
        keys = {k: v for k, v, _ in f.mods.added}
        self.assertAlmostEqual(keys["fire_rate"], it.p("BonusFireRate") / 100)
        self.assertGreater(keys["move_speed"], 0)
        fx.on_healed(f, 50.0)                     # on cooldown
        self.assertEqual(len(f.mods.added), 2)
        from deadsim.engine import NOT_HEALS
        self.assertIn("regen", NOT_HEALS)


if __name__ == "__main__":
    unittest.main()
