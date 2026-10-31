"""Checks of the overall score's real death rate value (damage/scripts/overall_search.py death_rate_value) and the
opt-in fight rate (fight_value), both from sim/data/fight_rate.json.
Run from sim/: python3 -m unittest discover -s tests"""
import math
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "survival")]

import overall_search as O  # noqa: E402
import search as S  # noqa: E402


def item(name):
    return next(i for i, it in S.G().items.items() if it.name == name)


class DeathRate(unittest.TestCase):
    def setUp(self):
        self.was = O.DEATH_RATE, O.FIGHT_RATE
        O.DEATH_RATE = True

    def tearDown(self):
        O.DEATH_RATE, O.FIGHT_RATE = self.was

    def test_file_is_sane(self):
        d = O.fight_rate_data()
        for ph in ("lane", "mid", "late"):
            self.assertTrue(0.3 < d["hp_elasticity"][ph] < 1.0, ph)
        for b, t in d["items"].items():
            self.assertGreater(t["intervals"], 100000, b)
            for n, e in t["items"].items():
                self.assertTrue(0.3 < e["deaths"][0] < 2.0, (b, n))

    def test_value(self):
        hero = S.G().hero("Abrams").id
        self.assertAlmostEqual(O.death_rate_value([], hero, 27000), 1.0)
        rates = O.death_rates(27000)
        cd = item("Cheat Death")
        self.assertLess(rates[cd], 0.8)           # Cheat Death holders die far less
        self.assertGreater(O.death_rate_value([cd], hero, 27000), 1.0)
        worse = [i for i, r in rates.items() if r > 1.0]
        self.assertTrue(worse)
        self.assertLess(O.death_rate_value(worse[:1], hero, 27000), 1.0)
        # exact form: ((c + d L) / (c + d x ratio x L)) ^ DEATH_RATE_GAMMA
        dd = O.death_data()
        row = dd["phases"][O.game_phase(27000)]
        d = row["deaths_per_engagement"] * dd["heroes"].get(str(hero), {}).get("ratio", 1.0)
        c, L = row["alive_s_per_engagement"], O.death_seconds(27000)
        k = O.DEATH_RATE_GAMMA
        self.assertAlmostEqual(O.death_rate_value([cd], hero, 27000), ((c + d * L) / (c + d * rates[cd] * L)) ** k)
        # the product of many items is clamped
        self.assertAlmostEqual(O.death_rate_value(list(rates), hero, 27000),
                               ((c + d * L) / (c + d * max(O.DEATH_RATE_CLAMP[0], min(O.DEATH_RATE_CLAMP[1],
                                   math.prod(rates.values()))) * L)) ** k)
        O.DEATH_RATE = False
        self.assertEqual(O.death_rate_value([cd], hero, 27000), 1.0)

    def test_per_kills_assists(self):
        """DEATH_PER_KA divides each item's deaths ratio by its kills + assists ratio (deaths per engagement)."""
        e = O.fight_rate_data()["items"]["27000"]["items"]["Spirit Shielding"]
        em = item("Spirit Shielding")   # tier 2: tier-1 items are left out at 27k (DEATH_RATE_T1_FROM)
        was = O.DEATH_PER_KA
        try:
            O.DEATH_PER_KA = True
            self.assertAlmostEqual(O.death_rates(27000)[em], e["deaths"][0] / e["ka"][0])
            O.DEATH_PER_KA = False
            self.assertAlmostEqual(O.death_rates(27000)[em], e["deaths"][0])
        finally:
            O.DEATH_PER_KA = was

    def test_through_the_evaluator(self):
        """The popular build scores 1 (its own death rate value is divided out), Cheat Death raises a build's score
        by exactly its death rate value when damage is unchanged; the lane score gets it too."""
        hero = S.G().hero("Abrams").id
        pop = [item("Extra Health"), item("Headshot Booster")]
        cd = item("Cheat Death")
        was = S.popular_build
        S.popular_build = lambda *a: pop

        class Ev(O.Evaluator):
            def _rows(self, items, pool):
                return [(1, 1.0, 900.0, 12.0, False, 0.2, 800.0)]

        class Lane(O.LaneEvaluator):
            def _rows(self, items, pool):
                return [(1, 1.0, 900.0, 12.0, False)]
        try:
            for cls in (Ev, Lane):
                ev = cls(hero, 27000, {})
                self.assertAlmostEqual(ev.run(pop), 1.0)
                gain = ev.run(pop + [cd]) / (O.movement_value(pop + [cd], hero) * ev._map(pop + [cd])
                                             * O.win_value(pop + [cd], hero) * O.team_value(pop + [cd], 27000)
                                             / (O.movement_value(pop, hero) * O.win_value(pop, hero)
                                                * O.team_value(pop, 27000)))
                want = O.death_rate_value(pop + [cd], hero, 27000) / O.death_rate_value(pop, hero, 27000)
                self.assertGreater(want, 1.0)
                self.assertAlmostEqual(gain, want, places=6)
        finally:
            S.popular_build = was

    def test_movement_items_left_out(self):
        # movement_value already counts their deaths (escape)
        self.assertNotIn(item("Warp Stone"), O.death_rates(27000))

    def test_healing_items_left_out(self):
        # their holders die less without winning more (heal_deaths.py); HEAL_DEATHS = True keeps their ratios
        was = O.HEAL_DEATHS
        try:
            O.HEAL_DEATHS = False
            self.assertNotIn(item("Radiant Regeneration"), O.death_rates(27000))
            self.assertNotIn(item("Spirit Lifesteal"), O.death_rates(27000))
            self.assertIn(item("Cheat Death"), O.death_rates(27000))
            O.HEAL_DEATHS = True
            self.assertIn(item("Radiant Regeneration"), O.death_rates(27000))
            self.assertIn(item("Spirit Lifesteal"), O.death_rates(27000))
        finally:
            O.HEAL_DEATHS = was
        names = {it.name for it in S.G().items.values()}
        self.assertFalse(O.HEAL_ITEMS - names)    # renamed by a patch: fix the list

    def test_death_price(self):
        # a death is priced above the time it takes (real win edges, death_price.py): gamma 1 = time dead only
        was = O.DEATH_RATE_GAMMA
        hero, cd = S.G().hero("Abrams").id, item("Cheat Death")
        try:
            O.DEATH_RATE_GAMMA = 1.0
            one = O.death_rate_value([cd], hero, 27000)
            O.DEATH_RATE_GAMMA = 2.0
            self.assertAlmostEqual(O.death_rate_value([cd], hero, 27000), one ** 2)
        finally:
            O.DEATH_RATE_GAMMA = was
        self.assertGreaterEqual(O.DEATH_RATE_GAMMA, 1.0)

    def test_tier1_left_out_late(self):
        # leftover tier-1 holders' kills + assists come from the team's lead (validation/tier1_death_rate.md)
        was = O.DEATH_RATE_T1_FROM
        tier1 = {i for i, it in S.G().items.items() if it.tier == 1}
        try:
            O.DEATH_RATE_T1_FROM = 27000
            self.assertFalse(tier1 & set(O.death_rates(27000)))
            self.assertFalse(tier1 & set(O.death_rates(37000)))
            self.assertTrue(tier1 & set(O.death_rates(10000)))     # still core items early
            self.assertIn(item("Cheat Death"), O.death_rates(27000))
            O.DEATH_RATE_T1_FROM = None
            self.assertIn(item("Extra Charge"), O.death_rates(27000))
        finally:
            O.DEATH_RATE_T1_FROM = was

    def test_fight_value(self):
        O.FIGHT_RATE = False
        self.assertEqual(O.fight_value(500, 1000, 3000, 2000, 27000), 1.0)
        O.FIGHT_RATE = True
        self.assertAlmostEqual(O.fight_value(1000, 1000, 2000, 2000, 27000), 1.0)
        self.assertGreater(O.fight_value(1000, 1000, 2400, 2000, 27000), 1.0)   # more health: more fights
        self.assertGreater(O.fight_value(800, 1000, 2000, 2000, 27000), 1.0)    # less health lost per fight
        self.assertEqual(O.fight_value(0, 0, 2400, 2000, 5000), 1.0)            # lane: no health lost booked
        self.assertLessEqual(O.fight_value(1, 1000, 9000, 2000, 27000), O.FIGHT_CLAMP[1])


if __name__ == "__main__":
    unittest.main()
