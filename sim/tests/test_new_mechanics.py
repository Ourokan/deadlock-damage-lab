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


def _split_main(hero):
    """Split Shot copies on the main target per landed gun bullet for the hero (Mechanics.split_range on)."""
    from deadsim.accuracy import default_distance
    return M.SPLIT_PRIMARY_HIT * M.SPLIT_REF_M / max(M.SPLIT_MIN_M, default_distance(hero))


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

    MECH = Mechanics(movement=False, parry=False, range_drift=False)

    def graves(self, focus, targeting=None):
        a = Loadout("Graves", [], souls=25000, skill=Skill(accuracy=0.0, use_actives=False))
        b = Loadout("Haze", ["Extra Health", "Bullet Resilience"], souls=25000,
                    skill=Skill(accuracy=0.9, summon_focus=focus, use_abilities=False))
        saved = M._TARGETING
        if targeting is not None:
            M._TARGETING = targeting
        try:
            return duel(a, b, max_time=10, mechanics=self.MECH)   # nobody dies in 10 s
        finally:
            M._TARGETING = saved

    def test_graves_summons_can_be_killed(self):
        shot, ignored = self.graves(1.0), self.graves(0.0)
        self.assertGreater(shot.b_summon.get("Deadhead", 0.0) + shot.b_summon.get("Zombie", 0.0), 0.0)
        self.assertGreater(shot.a_summons_out["graves_skull"][1], 0)    # some Deadheads shot down
        self.assertLess(shot.a_dmg["Jar of Dead"], ignored.a_dmg["Jar of Dead"])   # dead Deadheads stop biting
        self.assertNotIn("Gravestone", shot.b_summon)                     # bullets don't hurt the gravestone

    def test_gravestone_kill_stops_zombies(self):
        rows = {k: dict(v) for k, v in M.summon_targeting().items()}
        for v in rows.values():
            v.update(focus=0.0, splash=0.0)
        standing = self.graves(None, rows)
        rows["graves_stone"].update(splash=50.0)    # broken by the first area hit on Graves
        broken = self.graves(None, rows)
        self.assertEqual(broken.a_summons_out["graves_stone"][1], 1)
        self.assertLess(broken.a_dmg.get("Borrowed Decree (zombie)", 0.0), standing.a_dmg.get("Borrowed Decree (zombie)", 0.0))

    def test_gravestone_break_is_expected_value(self):
        rows = {k: dict(v) for k, v in M.summon_targeting().items()}
        for v in rows.values():
            v.update(focus=0.0, splash=0.0)
        out = []
        for p in (0.0, 0.5, 1.0):
            rows["graves_stone"].update(break_p=p, break_s=3.0)
            r = self.graves(None, rows)
            out.append((r.a_dmg.get("Borrowed Decree (zombie)", 0.0), r.a_dmg.get("Jar of Dead", 0.0)))
        (z0, _), (z5, _), (z1, _) = out
        self.assertGreater(z1, 0.0)                              # zombies from before the break still bite
        self.assertAlmostEqual(z5, (z0 + z1) / 2, delta=0.02 * z0)   # p = 0.5 is half way, no rounding
        # the aura's spirit shred is scaled the same way: Deadheads biting after the break hit softer
        j0, j5, j1 = (x[1] for x in out)
        self.assertGreater(j0, j1)
        self.assertAlmostEqual(j5, (j0 + j1) / 2, delta=0.1 * (j0 - j1))

    def test_splash_hits_summons(self):
        a = Loadout("McGinnis", [], souls=15000, skill=Skill(accuracy=0.0, use_actives=False),
                    unlocked=[True, False, False, False])
        b = Loadout("Infernus", [], souls=15000, skill=Skill(accuracy=0.0, summon_focus=0.0))
        r = duel(a, b, max_time=20, mechanics=self.MECH)
        self.assertGreater(r.b_summon_kind["mcginnis_turret"][1], 0.0)   # abilities only, no gun damage
        self.assertEqual(r.b_summon_kind["mcginnis_turret"][0], 0.0)

    def test_assistant_cannot_be_shot(self):
        # Sinclair's Spectral Assistant has no health in replays: nothing to shoot
        a = Loadout("Sinclair", [], souls=25000, skill=Skill(accuracy=0.3))
        b = Loadout("Haze", [], souls=25000, skill=Skill(accuracy=0.5, summon_focus=1.0, use_abilities=False))
        self.assertEqual(duel(a, b, max_time=20, mechanics=self.MECH).b_summon, {})


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

    def test_split_shot_main_copies_follow_landed_bullets(self):
        """Replays: 0.73 Split Shot hits on the main target per landed gun bullet during the active."""
        a = Loadout("Haze", ["Split Shot"], souls=15000, skill=Skill(accuracy=0.5, use_abilities=False))
        b = Loadout("Abrams", [], souls=15000, skill=Skill(accuracy=0.0, **OFF))
        r = duel(a, b, max_time=4, mechanics=Mechanics(movement=False, parry=False))
        ratio = r.a_dmg["Split Shot"] / r.a_dmg["gun"]
        self.assertAlmostEqual(ratio, _split_main("Haze"), delta=0.15)

    def test_split_shot_main_copies_fall_with_distance(self):
        """Mechanics.split_range: the fan's copies on the main target scale with 1 / the holder's median distance
        (replays: Yamato 1.10 at 8 m, Vyper 0.76 at 11, Wraith 0.59 at 16); off, everyone gets SPLIT_PRIMARY_HIT."""
        def ratio(hero, **kw):
            a = Loadout(hero, ["Split Shot"], souls=15000, skill=Skill(accuracy=0.5, use_abilities=False))
            b = Loadout("Abrams", [], souls=15000, skill=Skill(accuracy=0.0, **OFF))
            r = duel(a, b, max_time=4, mechanics=Mechanics(movement=False, parry=False, **kw))
            return r.a_dmg["Split Shot"] / r.a_dmg["gun"]
        self.assertAlmostEqual(_split_main("Vyper"), 0.77, delta=0.02)
        self.assertAlmostEqual(_split_main("Vindicta"), 0.33, delta=0.02)
        self.assertLess(ratio("Vindicta"), 0.6 * ratio("Vyper"))
        self.assertAlmostEqual(ratio("Vindicta", split_range=False), M.SPLIT_PRIMARY_HIT, delta=0.15)

    def test_split_shot_waits_for_a_target_it_can_hurt(self):
        from deadsim.engine import Engine
        from deadsim.fight import make_fighter
        e = Engine(distance=10, max_time=5, mech=Mechanics(movement=False))
        f = make_fighter(e, Loadout("Haze", ["Split Shot"], souls=15000))
        g = make_fighter(e, Loadout("Abrams", [], souls=15000))
        f.enemy, g.enemy = g, f
        fx = next(x for x in f.items_fx if x.name == "Split Shot")
        g.mods.add("invulnerable", 1, 2.0, "test")
        self.assertFalse(fx.try_active(f))
        g.mods.remove("invulnerable", "test")
        self.assertTrue(fx.try_active(f))

    def test_split_shot_side_hits_capped_in_team_fights(self):
        """The fit covers ~0.3 nearby enemies; with a team fight's 5 at most one side copy lands per bullet."""
        a = Loadout("Haze", ["Split Shot"], souls=15000, skill=Skill(accuracy=0.5, use_abilities=False))
        b = Loadout("Abrams", [], souls=15000, skill=Skill(accuracy=0.0, **OFF))
        r = duel(a, b, max_time=4, mechanics=Mechanics(movement=False, parry=False, extra_targets=5.0))
        main = r.a_dmg["Split Shot"] / _split_main("Haze")
        self.assertLessEqual(r.a_splash["Split Shot"], main * 1.6)

    def test_real_nearby_interpolates_the_position_table(self):
        import json
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "team_value.json")) as fh:
            pos = json.load(fh)["positions"]
        b = sorted(int(k) for k in pos["budgets"] if k != "all")
        tab = pos["budgets"][str(b[0])]["extra"]
        self.assertAlmostEqual(M.real_nearby("extra", 12, b[0]), tab["12"])
        self.assertAlmostEqual(M.real_nearby("extra", 13, b[0]), tab["12"] + (tab["15"] - tab["12"]) / 3)
        self.assertAlmostEqual(M.real_nearby("extra", 12, 1), tab["12"])     # clamped to the lowest budget


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
