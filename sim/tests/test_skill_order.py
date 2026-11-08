"""Checks of the ability point model (deadsim.fight) and the ability order search (damage/scripts/skill_order.py).
Run from sim/: python3 -m unittest discover -s tests"""
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "damage")]

from deadsim.data import game  # noqa: E402
from deadsim.fight import (LANE_ORDER_HEROES, LANE_ORDER_SOULS, ORDER_HEROES, _auto_abilities, abilities_for_order, ability_budget,  # noqa: E402
                           default_ability_order, median_ability_order, popular_ability_order)
import skill_order as K  # noqa: E402

G = game()
HAZE = G.hero("Haze")
IDS = [a.id for a in HAZE.abilities]


class Points(unittest.TestCase):
    def test_four_unlocks_and_32_points_by_level_36(self):
        self.assertEqual(ability_budget(HAZE, 0), (1, 0))
        self.assertEqual(ability_budget(HAZE, 50000), (4, 32))

    def test_popular_order_is_maxed_at_50k(self):
        tiers, unlocked = abilities_for_order(HAZE, popular_ability_order(HAZE.id), 50000)
        self.assertEqual(tiers, [3, 3, 3, 3])
        self.assertTrue(all(unlocked))

    def test_order_waits_for_a_tier_3_instead_of_skipping_ahead(self):
        a, b = IDS[0], IDS[1]
        order = [a, b, IDS[2], IDS[3], a, a, a, b]   # unlocks, then a to tier 3 (8 points), then b
        for souls in range(4000, 12000, 500):
            pts = ability_budget(HAZE, souls)[1]
            tiers, _ = abilities_for_order(HAZE, order, souls)
            want = 3 if pts >= 8 else 2 if pts >= 3 else 1 if pts >= 1 else 0
            self.assertEqual(tiers[0], want, souls)
            self.assertEqual(tiers[1], 1 if pts >= 9 else 0, souls)


class Search(unittest.TestCase):
    def test_stop_rule(self):
        self.assertTrue(K.stops_at((3, 3, 3, 3), 32))
        self.assertTrue(K.stops_at((2, 0, 0, 0), 4, toward=(3, 0, 0, 0)))    # 1 left, tier 3 costs 5
        self.assertFalse(K.stops_at((2, 0, 0, 0), 4, toward=(2, 1, 0, 0)))   # 1 left buys the next tier 1

    def test_full_order_follows_the_upgrade_sequence(self):
        seq = [2, 2, 2, 0, 0, 0, 1, 1, 1, 3, 3, 3]
        order, steps = K.full_order(HAZE, popular_ability_order(HAZE.id), seq)
        self.assertEqual(len(order), 16)
        ups = [IDS.index(s["ability"]) for s in steps if s["tier"]]
        self.assertEqual(ups, seq)
        self.assertEqual(abilities_for_order(HAZE, order, 50000)[0], [3, 3, 3, 3])
        levels = [s["level"] for s in steps]
        self.assertEqual(levels, sorted(levels))


def _auto_abilities_with(hero, souls, order):
    """_auto_abilities on a given order (the fight's event count per net worth)."""
    from deadsim.fight import ability_events_for_souls
    ids = [a.id for a in hero.abilities]
    tiers, unlocked = [0] * len(ids), [False] * len(ids)
    for aid in order[:ability_events_for_souls(souls)]:
        i = ids.index(aid)
        if unlocked[i]:
            tiers[i] = min(3, tiers[i] + 1)
        unlocked[i] = True
    return tiers, unlocked


class MedianOrder(unittest.TestCase):
    def test_lane_order_heroes_switch_back_after_the_lane(self):
        # LANE_ORDER_HEROES follow the median order below LANE_ORDER_SOULS only: the 27k / 37k builds the win check
        # scores keep the popular order (and the corr fitted on it)
        self.assertLess(LANE_ORDER_SOULS, 27000)
        self.assertFalse(set(LANE_ORDER_HEROES) & set(ORDER_HEROES))
        for name in LANE_ORDER_HEROES:
            h = G.hero(name)
            self.assertEqual(default_ability_order(h, LANE_ORDER_SOULS - 1), median_ability_order(h.id))
            self.assertEqual(default_ability_order(h, LANE_ORDER_SOULS), popular_ability_order(h.id))
            self.assertEqual(default_ability_order(h), popular_ability_order(h.id))
            for souls in (27000, 37000):
                self.assertEqual(_auto_abilities(h, souls), _auto_abilities_with(h, souls, popular_ability_order(h.id)))

    def test_order_heroes_follow_the_median_order(self):
        for name in ORDER_HEROES:
            h = G.hero(name)
            order = default_ability_order(h)
            self.assertEqual(order, median_ability_order(h.id))
            ids = [a.id for a in h.abilities]
            self.assertEqual(sorted(order), sorted(ids * 4))   # 4 unlocks + 12 upgrades, each ability 1 + 3
        self.assertEqual(default_ability_order(HAZE), popular_ability_order(HAZE.id))

    def test_celeste_upgrades_her_ult_by_mid_game(self):
        # real Celeste players have Shining Wonder at tier 1.6 at 60% of the match (scripts/ability_order.py)
        h = G.hero("Celeste")
        ult = next(i for i, a in enumerate(h.abilities) if a.ultimate)
        self.assertGreaterEqual(_auto_abilities(h, 34000)[0][ult], 1)

    def test_ivy_levels_kudzu_early(self):
        # Ivy's popular order leaves Kudzu Connection at tier 0 by mid game, real players have it at 2.1
        h = G.hero("Ivy")
        kudzu = next(i for i, a in enumerate(h.abilities) if a.name == "Kudzu Connection")
        self.assertGreaterEqual(_auto_abilities(h, 14000)[0][kudzu], 2)

    def test_geist_takes_essence_bomb_tier_3(self):
        # since the 10-30 Essence Bomb buff real Geists level it to tier 2.6 late (popular order: 2.0, no puddle)
        h = G.hero("Lady Geist")
        self.assertIn("Lady Geist", ORDER_HEROES)
        self.assertEqual(_auto_abilities(h, 27000)[0][0], 3)

    def test_paige_unlocks_her_ult_in_lane(self):
        # Paige's popular order maxes Bookwyrm first and has Rallying Charge locked at 8k souls; the median order has
        # it unlocked and Bookwyrm at tier 1
        h = G.hero("Paige")
        ult = next(i for i, a in enumerate(h.abilities) if a.ultimate)
        book = next(i for i, a in enumerate(h.abilities) if a.name == "Bookwyrm")
        tiers, unlocked = _auto_abilities(h, 8000)
        self.assertTrue(unlocked[ult])
        self.assertLessEqual(tiers[book], 1)

    def test_graves_maxes_jar_by_mid_game(self):
        # Graves' popular order maxes Grasping Hands first and has Jar of Dead at tier 2 until 26k souls; the median
        # order has Jar at tier 3 by 18k (real Graves: 39% at T3 by 60% of the match)
        h = G.hero("Graves")
        jar = next(i for i, a in enumerate(h.abilities) if a.name == "Jar of Dead")
        tiers, _ = _auto_abilities(h, 18000)
        self.assertEqual(tiers[jar], 3)


if __name__ == "__main__":
    unittest.main()
