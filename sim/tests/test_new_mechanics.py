"""Tests for deadsim.mechanics (parry, Counterspell, summons, nearby enemies, movement). Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.mechanics import Mechanics  # noqa: E402
import deadsim.mechanics as M  # noqa: E402

OFF = dict(use_abilities=False, use_actives=False)


class TestOff(unittest.TestCase):
    def test_none_matches_earlier_model(self):
        a = Loadout("Abrams", ["Extra Health", "Rebuttal"], souls=15000, skill=Skill(accuracy=0.3, melee_rate=0.3))
        b = Loadout("McGinnis", ["Extra Spirit", "Split Shot"], souls=15000, skill=Skill(accuracy=0.3))
        r1 = duel(a, b, mechanics=None)
        saved, M.DEFAULT = M.DEFAULT, None
        try:
            r2 = duel(a, b)   # unset -> DEFAULT
        finally:
            M.DEFAULT = saved
        self.assertEqual((r1.winner, round(r1.time, 3), round(r1.a_hp, 3)), (r2.winner, round(r2.time, 3), round(r2.a_hp, 3)))
        self.assertIsNone(r1.escaped)
        self.assertEqual(r1.b_summon, {})

    def test_default_is_on(self):
        self.assertIsInstance(M.DEFAULT, Mechanics)
        a = Loadout("Abrams", [], souls=15000, skill=Skill(accuracy=0.3, melee_rate=0.3))
        b = Loadout("McGinnis", [], souls=15000, skill=Skill(accuracy=0.3))
        r = duel(a, b)
        self.assertGreater(sum(r.a_summon.values()), 0.0)   # Abrams shoots the turret


class TestParry(unittest.TestCase):
    def fight(self, items=(), parry=1.0):
        a = Loadout("Abrams", [], souls=15000, skill=Skill(accuracy=0.0, melee_rate=1.0, heavy_share=1.0, **OFF))
        b = Loadout("Haze", list(items), souls=15000, skill=Skill(accuracy=0.0, parry_rate=parry, **OFF))
        return duel(a, b, max_time=10, mechanics=Mechanics(movement=False), log=True)

    def test_parry_blocks_heavy_and_stuns(self):
        r = self.fight(parry=1.0)
        self.assertEqual(r.a_dmg.get("melee", 0.0), 0.0)
        self.assertTrue(any("parries" in x for x in r.log))
        self.assertGreater(self.fight(parry=0.0).a_dmg.get("melee", 0.0), 0.0)

    def test_rebuttal_returns_damage(self):
        r = self.fight(["Rebuttal"], parry=1.0)
        self.assertGreater(r.b_dmg.get("Rebuttal", 0.0), 0.0)


class TestCounterspell(unittest.TestCase):
    def test_blocks_aimed_cast(self):
        def run(rate):
            a = Loadout("Infernus", [], souls=15000, skill=Skill(accuracy=0.0, use_actives=False))
            b = Loadout("Haze", ["Counterspell"], souls=15000, skill=Skill(accuracy=0.0, spell_parry_rate=rate, **OFF))
            r = duel(a, b, max_time=1.0, mechanics=Mechanics(movement=False))
            return sum(r.a_dmg.values())
        self.assertLess(run(1.0), run(0.0))


class TestSummons(unittest.TestCase):
    def test_turret_can_be_killed(self):
        a = Loadout("McGinnis", [], souls=15000, skill=Skill(accuracy=0.0, use_actives=False),
                    unlocked=[True, False, False, False])
        b = Loadout("Haze", [], souls=15000, skill=Skill(accuracy=0.5, summon_focus=1.0, use_abilities=False))
        on = duel(a, b, max_time=20, mechanics=Mechanics(movement=False, parry=False, range_drift=False))
        off = duel(a, b, max_time=20, mechanics=None)
        self.assertGreater(sum(on.b_summon.values()), 0.0)
        self.assertLess(on.a_dmg.get("Mini Turret", 0.0), off.a_dmg.get("Mini Turret", 0.0))


class TestNearby(unittest.TestCase):
    def test_ricochet_splash_only_with_nearby_enemies(self):
        a = Loadout("Haze", ["Ricochet"], souls=30000, skill=Skill(accuracy=0.5, **OFF))
        b = Loadout("Abrams", [], souls=30000, skill=Skill(accuracy=0.0, **OFF))
        self.assertEqual(duel(a, b, max_time=5, mechanics=Mechanics(movement=False)).a_splash, {})
        r = duel(a, b, max_time=5, mechanics=Mechanics(movement=False, extra_targets=1.0))
        self.assertGreater(r.a_splash.get("Ricochet", 0.0), 0.0)

    def test_split_shot_hits_main_target(self):
        a = Loadout("Haze", ["Split Shot"], souls=15000, skill=Skill(accuracy=0.5, use_abilities=False))
        b = Loadout("Abrams", [], souls=15000, skill=Skill(accuracy=0.0, **OFF))
        r = duel(a, b, max_time=5, mechanics=Mechanics(movement=False))
        self.assertGreater(r.a_dmg.get("Split Shot", 0.0), 0.0)


class TestMovement(unittest.TestCase):
    def setUp(self):
        self.p = M.CHASE_PROB

    def tearDown(self):
        M.CHASE_PROB = self.p

    def fight(self, a_items=(), b_items=(), chase=0.0):
        M.CHASE_PROB = chase
        a = Loadout("Haze", list(a_items), souls=20000, skill=Skill(accuracy=0.2, use_abilities=False, flee_hp=0.5))
        b = Loadout("Haze", list(b_items), souls=20000, skill=Skill(accuracy=0.6, use_abilities=False))
        return duel(a, b, distance=15, max_time=40, mechanics=Mechanics(parry=False))

    def test_runner_escapes_a_stander(self):
        r = self.fight(chase=0.0)
        self.assertEqual(r.escaped, "Haze (A)")
        self.assertIsNone(r.winner)

    def test_chaser_with_slow_catches(self):
        free = self.fight(chase=1.0)
        slowed = self.fight(b_items=["Slowing Hex", "Phantom Strike"], chase=1.0)
        self.assertNotEqual(slowed.escaped, "Haze (A)")
        self.assertTrue(free.escaped == "Haze (A)" or free.winner is not None)

    def test_warp_stone_helps(self):
        base = self.fight(chase=1.0)
        warp = self.fight(a_items=["Warp Stone", "Enduring Speed", "Fleetfoot"], chase=1.0)
        self.assertTrue(warp.escaped == "Haze (A)" or (warp.winner is None and base.winner is not None)
                        or warp.time > base.time)


if __name__ == "__main__":
    unittest.main()
