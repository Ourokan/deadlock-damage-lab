"""Checks of the laning phase test (damage/scripts/overall_search.py lane_fight, used by game_path's early stages):
health carries between trades and regen / out-of-combat regen / Fortitude heal in the gaps.
Run from sim/: python3 -m unittest discover -s tests"""
import os
import sys
import unittest
from unittest import mock

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "damage", "survival")]

import overall_search as O  # noqa: E402
from deadsim.build import compute_stats  # noqa: E402
from survival import survive  # noqa: E402

S = O.S
G = S.G()
ID = {it.name: it.id for it in G.items.values()}
HAZE, ABRAMS = G.hero("Haze").id, G.hero("Abrams").id


class Stats(unittest.TestCase):
    def test_out_of_combat_regen_comes_from_items(self):
        base = compute_stats(G.hero("Haze"), [], souls=3000).ooc_regen
        st = compute_stats(G.hero("Haze"), [G.items[ID["Extra Regen"]]], souls=3000)
        self.assertAlmostEqual(st.ooc_regen - base, 1.5)
        self.assertAlmostEqual(st.health_regen - compute_stats(G.hero("Haze"), [], souls=3000).health_regen, 2.5)


class StartHealth(unittest.TestCase):
    def test_fight_starts_at_the_given_health(self):
        full = survive(HAZE, [], 3000, ABRAMS, [], max_time=30.0)
        hurt = survive(HAZE, [], 3000, ABRAMS, [], max_time=30.0, start_hp=100.0)
        self.assertLess(hurt["time_alive"], full["time_alive"])


class GapHeal(unittest.TestCase):
    r = {"regen": 2.0, "ooc_regen": 1.5, "regen_amp": 0.0, "max_hp": 1000}

    def test_regen_all_gap_ooc_after_delay(self):
        self.assertAlmostEqual(O.gap_heal(self.r, [], gap=25.0), 2.0 * 25 + 1.5 * (25 - O.OOC_DELAY))

    def test_regen_amp_and_fortitude(self):
        fort = G.items[ID["Fortitude"]]
        got = O.gap_heal(self.r | {"regen_amp": 0.2}, [ID["Fortitude"]], gap=25.0)
        want = (2.0 * 25 + 1.5 * (25 - O.OOC_DELAY)
                + 1000 * fort.props["HealLifePercentOutOfCombat"] / 100 * (25 - fort.props["RestoreDelay"])) * 1.2
        self.assertAlmostEqual(got, want)


def fake_survive(lost):
    """Each trade loses `lost` health and deals 100 damage; no regen."""
    calls = []

    def f(h, items, souls, oh, oitems, start_hp=None, **kw):
        hp = 1000.0 if start_hp is None else start_hp
        calls.append(hp)
        end = hp - lost
        return {"damage_dealt": 100.0, "time_alive": kw["max_time"] if end > 0 else 1.0, "survived": end > 0,
                "max_hp": 1000, "final_hp": max(0.0, end), "regen": 0.0, "ooc_regen": 0.0, "regen_amp": 0.0}
    return f, calls


class Lane(unittest.TestCase):
    def setUp(self):
        O.set_bracket(O.PRIMARY)

    def test_health_carries_and_low_health_backs(self):
        f, calls = fake_survive(300.0)
        with mock.patch.object(O, "survive", f):
            dmg, t, share = O.lane_fight(HAZE, [], ABRAMS, [], 3000)
        self.assertEqual(calls, [1000.0, 700.0, 400.0])   # 100 left after the third: backs (< BACK_FRAC)
        self.assertEqual((dmg, share), (300.0, 3 / O.LANE_TRADES))

    def test_death_ends_the_lane(self):
        f, calls = fake_survive(600.0)
        with mock.patch.object(O, "survive", f):
            dmg, t, share = O.lane_fight(HAZE, [], ABRAMS, [], 3000)
        self.assertEqual(len(calls), 2)
        self.assertEqual(share, 1 / O.LANE_TRADES)

    def test_full_lane(self):
        f, calls = fake_survive(10.0)
        with mock.patch.object(O, "survive", f):
            dmg, t, share = O.lane_fight(HAZE, [], ABRAMS, [], 3000)
        self.assertEqual((len(calls), share), (O.LANE_TRADES, 1.0))


class Mix(unittest.TestCase):
    def test_mix_weights_lane_and_fight(self):
        m = O.MixEvaluator.__new__(O.MixEvaluator)
        m.lane, m.fight, m.w = mock.Mock(), mock.Mock(), 0.25
        m.lane.run.return_value, m.fight.run.return_value = 2.0, 1.0
        self.assertAlmostEqual(m.run([]), 0.25 * 2.0 + 0.75 * 1.0)


if __name__ == "__main__":
    unittest.main()
