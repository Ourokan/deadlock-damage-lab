"""Checks of the laning phase test (damage/scripts/overall_search.py lane_fight, used by game_path's early stages):
health carries between trades and regen / out-of-combat regen / Fortitude / heal pickups / farm-heal items heal in
the gaps; plus the sustain parts of the fight score (net damage, fight entry health, Healbane's kill heal).
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


NO_PICKUPS = {"pickup_hp_per_min": {"lane": 0.0, "mid": 0.0, "late": 0.0}, "farm_heal_hp_per_min": {},
              "entry_hp": {"lane": 1.0, "mid": 1.0, "late": 1.0}, "gap_s": {"lane": 20, "mid": 25, "late": 25}}


class GapHeal(unittest.TestCase):
    r = {"regen": 2.0, "ooc_regen": 1.5, "regen_amp": 0.0, "max_hp": 1000}

    def setUp(self):
        p = mock.patch.object(O, "sustain", lambda: NO_PICKUPS)
        p.start()
        self.addCleanup(p.stop)

    def test_regen_all_gap_ooc_after_delay(self):
        self.assertAlmostEqual(O.gap_heal(self.r, [], gap=25.0), 2.0 * 25 + 1.5 * (25 - O.OOC_DELAY))

    def test_regen_amp_and_fortitude(self):
        fort = G.items[ID["Fortitude"]]
        got = O.gap_heal(self.r | {"regen_amp": 0.2}, [ID["Fortitude"]], gap=25.0)
        want = (2.0 * 25 + 1.5 * (25 - O.OOC_DELAY)
                + 1000 * fort.props["HealLifePercentOutOfCombat"] / 100 * (25 - fort.props["RestoreDelay"])) * 1.2
        self.assertAlmostEqual(got, want)

    def test_pickups_amped_by_regen_amp_and_farm_items_by_cast_amp(self):
        sus = dict(NO_PICKUPS, pickup_hp_per_min={"lane": 120.0, "mid": 60.0, "late": 60.0},
                   farm_heal_hp_per_min={"Restorative Shot": {"lane": 60.0, "mid": 30.0, "late": 30.0}})
        r = self.r | {"regen": 0.0, "ooc_regen": 0.0, "regen_amp": 0.5, "heal_amp_cast": 0.2}
        with mock.patch.object(O, "sustain", lambda: sus):
            self.assertAlmostEqual(O.gap_heal(r, [], gap=30.0), 60.0 * 1.5)
            self.assertAlmostEqual(O.gap_heal(r, [ID["Restorative Shot"]], gap=30.0), 60.0 * 1.5 + 30.0 * 1.2)
            self.assertAlmostEqual(O.gap_heal(r, [ID["Restorative Shot"]], gap=30.0, phase="mid"), 45.0 + 18.0)

    def test_healbane_cuts_enemy_gap_heal(self):
        hb = G.items[ID["Healbane"]]
        want = 1 - abs(hb.props["HealAmpReceivePenaltyPercent"]) / 100 * hb.props["AbilityDuration"] / 25.0
        self.assertAlmostEqual(O.healbane_gap_share([ID["Healbane"]], gap=25.0), want)
        self.assertEqual(O.healbane_gap_share([]), 1.0)


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


def fake_survive_enemy(enemy_left):
    """Each trade deals 100 damage, the enemy heals 20 of it and ends at enemy_left health (max 1000)."""
    def f(h, items, souls, oh, oitems, start_hp=None, enemy_start_hp=None, **kw):
        return {"damage_dealt": 100.0, "enemy_healed": 20.0, "time_alive": kw["max_time"], "survived": True,
                "max_hp": 1000, "final_hp": 1000.0, "regen": 0.0, "ooc_regen": 0.0, "regen_amp": 0.0,
                "enemy_final_hp": enemy_left, "enemy_max_hp": 1000, "enemy_kills": 0,
                "enemy": {"regen": 0.0, "ooc_regen": 0.0, "regen_amp": 0.0, "max_hp": 1000}}
    return f


class Lane(unittest.TestCase):
    def setUp(self):
        O.set_bracket(O.PRIMARY)
        p = mock.patch.object(O, "sustain", lambda: NO_PICKUPS)
        p.start()
        self.addCleanup(p.stop)

    def test_net_damage_and_enemy_backing_frees_the_lane(self):
        with mock.patch.object(O, "survive", fake_survive_enemy(900.0)):
            dmg, t, share = O.lane_fight(HAZE, [], ABRAMS, [], 3000)
        self.assertAlmostEqual(dmg, 80.0 * O.LANE_TRADES)   # enemy healing undoes damage
        with mock.patch.object(O, "survive", fake_survive_enemy(100.0)):
            dmg, t, share = O.lane_fight(HAZE, [], ABRAMS, [], 3000)
        # enemy below BACK_FRAC after the first trade: backs, the rest of the lane counts at the mean trade
        self.assertAlmostEqual(dmg, 80.0 * O.LANE_TRADES)
        self.assertEqual(share, 1.0)

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


class RealSim(unittest.TestCase):
    def setUp(self):
        O.set_bracket(O.PRIMARY)

    def test_lane_on_the_real_sim(self):
        # survive() result keys used by lane_fight / gap_heal
        r = survive(HAZE, [ID["Extra Regen"]], 3000, ABRAMS, [], max_time=O.TRADE_S, start_hp=500.0)
        for k in ("regen", "ooc_regen", "regen_amp", "max_hp", "final_hp", "survived", "damage_dealt"):
            self.assertIn(k, r)
        self.assertGreater(O.gap_heal(r, [ID["Extra Regen"]]), O.gap_heal(r | {"ooc_regen": 0.0}, []))
        dmg, t, share = O.lane_fight(HAZE, [ID["Extra Regen"]], ABRAMS, [], 3000)
        self.assertGreater(dmg, 0)
        self.assertTrue(0 <= share <= 1)
        self.assertLessEqual(t, O.LANE_TRADES * O.TRADE_S + 1e-6)


class FightSustain(unittest.TestCase):
    def setUp(self):
        O.set_bracket(O.PRIMARY)

    def test_net_damage(self):
        self.assertEqual(O.net_damage({"damage_dealt": 500.0, "enemy_healed": 120.0}), 380.0)
        self.assertEqual(O.net_damage({"damage_dealt": 50.0, "enemy_healed": 120.0}), 0.0)

    def test_popular_build_enters_at_real_health_and_healing_builds_enter_fuller(self):
        pop = [ID["Extra Health"]]
        d = O.entry_deficit(HAZE, pop, 18000)
        r = O.build_stats(HAZE, pop, 18000)
        want = O.sustain()["entry_hp"]["mid"] * r["max_hp"]
        self.assertAlmostEqual(O.entry_hp_start(HAZE, pop, 18000, d), want, places=6)
        heal = pop + [ID["Radiant Regeneration"]]
        rh = O.build_stats(HAZE, heal, 18000)
        self.assertGreater(O.entry_hp_start(HAZE, heal, 18000, d) / rh["max_hp"], want / r["max_hp"])

    def test_healbane_heals_on_a_refill_kill(self):
        hb = G.items[ID["Healbane"]]
        r = survive(HAZE, [ID["Healbane"]], 18000, ABRAMS, [], max_time=30.0, start_hp=600.0)
        self.assertIn("enemy_kills", r)
        self.assertIn("enemy_healed", r)
        from deadsim.engine import kill_hooks
        healed = []
        killer = mock.Mock(alive=True)
        handler = __import__("deadsim.items_fx", fromlist=["HANDLERS"]).HANDLERS["upgrade_healbane"](hb, killer)
        killer.items_fx = [handler]
        killer.heal = lambda amt, *a: healed.append(amt)
        target = mock.Mock()
        target.mods.get.return_value = -0.35
        kill_hooks(killer, target)
        self.assertEqual(healed, [hb.props["HealOnKill"]])
        target.mods.get.return_value = None
        kill_hooks(killer, target)
        self.assertEqual(len(healed), 1)


class Calibration(unittest.TestCase):
    def setUp(self):
        O.set_bracket(O.PRIMARY)

    def test_healbane_runs_at_the_real_rate(self):
        # a refit of fit_sustain.py without fit_healbane.py drops the key; this KeyError is the guard
        su = O.sustain()
        k = su["healbane_landing"]
        self.assertEqual(su["healbane_landing_real"], su["healbane_prevented_per_combat_s"])   # fitted on today's real rate
        self.assertTrue(0 < k < 1)   # the sim overshoots the real rate, so the cut is scaled down
        self.assertEqual(O.skill(HAZE).item_landing["Healbane"], k)
        hb = G.items[ID["Healbane"]]
        want = 1 - abs(hb.props["HealAmpReceivePenaltyPercent"]) / 100 * k * hb.props["AbilityDuration"] / 25.0
        self.assertAlmostEqual(O.healbane_gap_share([ID["Healbane"]], gap=25.0), want)

    def test_field_heal_items_save_heal_trips(self):
        pop = [ID["Extra Health"]]
        base = O.map_time(HAZE, pop, 18000, pop)
        self.assertAlmostEqual(base, 1 - O.sustain()["heal_trips_per_min"]["mid"] * O.TRIP_S / 60)
        self.assertGreater(O.map_time(HAZE, pop + [ID["Radiant Regeneration"]], 18000, pop), base)
        self.assertEqual(O.map_time(HAZE, pop, 6000, pop), 1.0)   # lane: scored by the lane test


class StageEvaluators(unittest.TestCase):
    def test_lane_stages_use_the_lane_test(self):
        import game_path as P
        with mock.patch.object(O, "LaneEvaluator", lambda *a: "lane"), \
                mock.patch.object(O, "MixEvaluator", lambda *a: ("mix", a[-1])), \
                mock.patch.object(O, "Evaluator", lambda *a: "fight"):
            got = {b: P.make_evaluator(HAZE, b, None) for b in P.STAGES}
        self.assertEqual(got[3000], "lane")
        self.assertEqual(got[6000], "lane")
        self.assertEqual(got[10000], ("mix", 0.5))
        self.assertTrue(all(got[b] == "fight" for b in P.STAGES if b > 10000))


class Mix(unittest.TestCase):
    def test_mix_weights_lane_and_fight(self):
        m = O.MixEvaluator.__new__(O.MixEvaluator)
        m.lane, m.fight, m.w = mock.Mock(), mock.Mock(), 0.25
        m.lane.run.return_value, m.fight.run.return_value = 2.0, 1.0
        self.assertAlmostEqual(m.run([]), 0.25 * 2.0 + 0.75 * 1.0)


if __name__ == "__main__":
    unittest.main()
