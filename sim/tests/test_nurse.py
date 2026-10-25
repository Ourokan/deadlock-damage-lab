"""Nurse Harrow's ability models (deadsim/heroes/nurse.py). Run from sim/:
    python3 -m unittest discover -s tests
"""
import heapq
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.heroes import nurse  # noqa: E402


class NurseCase(unittest.TestCase):
    def setUp(self):
        self.e = Engine(distance=10, max_time=60, mech=None)
        self.f = make_fighter(self.e, Loadout("Nurse Harrow", [], souls=20000))
        self.g = make_fighter(self.e, Loadout("Abrams", [], souls=20000))
        self.f.enemy, self.g.enemy = self.g, self.f
        for s in self.f.abilities + self.g.abilities:
            s.start()
        self.ab = {s.ab.class_name: s for s in self.f.abilities}

    def run_until(self, t):
        """Run the scheduled events up to t s (no gun or AI: only what the abilities scheduled)."""
        e = self.e
        while e.q and e.q[0][0] <= t:
            e.t, _, fn, args = heapq.heappop(e.q)
            fn(*args)
        e.t = t


class TestLeech(NurseCase):
    def test_fight_starts_with_real_stacks(self):
        self.assertAlmostEqual(nurse.stacks(self.f), nurse.start_stacks(20000), places=6)
        self.assertGreater(self.f.mods.sum("regen"), 0)
        self.assertGreater(self.f.mods.sum("fire_rate"), 0)

    def test_one_leech_then_heal_and_stack_on_pickup(self):
        lt = self.ab["ability_nurse_leech_therapy"]
        c = lt.ctx
        before = nurse.stacks(self.f)
        lt.cast()
        self.run_until(c.raw("AbilityCastDelay") + c.dur("AbilityDuration") + 0.5)
        dealt = self.f.dmg_out.get("Leech Therapy", 0.0)
        self.assertGreater(dealt, 0)
        self.assertLess(dealt, c.val("DPS") * c.dur("AbilityDuration") * 1.01)   # one leech, resists only lower it
        self.f.hp = self.f.max_hp * 0.5
        hp = self.f.hp
        self.run_until(nurse.PICKUP_S + 0.01)
        self.assertGreater(self.f.hp - hp, dealt * 0.99)
        self.assertAlmostEqual(nurse.stacks(self.f), min(lt.impl.max_stacks(c), before + 1))


class TestVapors(NurseCase):
    def test_damage_deferred_then_crash(self):
        wv = self.ab["ability_nurse_adrenaline_rush"]
        wv.cast()
        self.run_until(0.3)
        hp = self.f.hp
        self.e.damage(self.g, self.f, 100.0, "spirit", "test", ignore_resist=True)
        self.assertAlmostEqual(hp - self.f.hp, 100.0 * (1 - nurse.SELF_CAST), places=6)
        pending = wv.scratch["pending"]
        self.assertAlmostEqual(pending, 100.0 * nurse.SELF_CAST, places=6)
        self.run_until(0.2 + wv.ctx.dur("AbilityDuration") + 0.01)
        self.assertAlmostEqual(self.g.dmg_out[nurse.CRASH_SRC], pending * 1.3, delta=1e-6)

    def test_healing_removes_specters_first(self):
        wv = self.ab["ability_nurse_adrenaline_rush"]
        wv.cast()
        self.run_until(0.3)
        self.e.damage(self.g, self.f, 200.0, "spirit", "test", ignore_resist=True)
        pending = wv.scratch["pending"]
        self.f.heal(pending / 2, "test", "ability")
        self.assertLess(wv.scratch["pending"], pending)


class TestTerrors(NurseCase):
    def test_fear_after_buildup_and_gun_locked(self):
        lt = self.ab["ability_nurse_fear"]
        c = lt.ctx
        lt.cast()
        self.assertGreater(self.f.gun_locked_until, c.raw("AbilityCastDelay") + c.dur("AbilityChannelTime") - 0.01)
        self.run_until(c.raw("AbilityCastDelay") + c.raw("BuildupTime") - 0.2)
        self.assertFalse(self.g.mods.active("disarm"))
        self.run_until(c.raw("AbilityCastDelay") + c.raw("BuildupTime") + 0.2)
        self.assertTrue(self.g.mods.active("disarm"))
        self.assertGreater(self.f.dmg_out.get("Lurking Terrors", 0.0), 0)

    def test_stun_breaks_channel(self):
        lt = self.ab["ability_nurse_fear"]
        c = lt.ctx
        lt.cast()
        self.run_until(c.raw("AbilityCastDelay") + 0.5)
        self.f.mods.add("stun", 1, 0.5, "test_stun")
        dealt = self.f.dmg_out.get("Lurking Terrors", 0.0)
        self.run_until(c.raw("AbilityCastDelay") + 3.0)
        self.assertAlmostEqual(self.f.dmg_out.get("Lurking Terrors", 0.0), dealt, delta=c.val("DPS") * 0.2)
        self.assertLess(self.f.gun_locked_until, c.raw("AbilityCastDelay") + 1.0)

    def test_needles_never_cast(self):
        self.assertFalse(self.ab["ability_nurse_healing_needles"].try_cast())


class TestCrashBooking(unittest.TestCase):
    """The game books the crash under the enemy's ability_nurse_adrenaline_rush: not Sinclair's copied ult."""

    def test_crash_maps_to_the_nurse_class(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
        import landing_rates as L
        from deadsim import game
        classes = [ab.class_name for ab in game().hero("Sinclair").abilities]
        self.assertEqual(L.real_key("ability_nurse_adrenaline_rush", classes), "ability_nurse_adrenaline_rush")
        self.assertEqual(L.sim_key(nurse.CRASH_SRC, {}, game()), "ability_nurse_adrenaline_rush")


class TestAimRows(unittest.TestCase):
    """Every hero has its own population aim (skill_defaults.json) or a replay gun calibration (Graves, Danny), so no
    hero silently falls back to the all-hero default aim and fight distance."""

    def test_no_hero_on_the_all_hero_default(self):
        import json
        from deadsim import game
        from deadsim.accuracy import DEFAULTS, gun_calibration
        rows = json.load(open(DEFAULTS))["heroes"]
        G = game()
        heroes = G.heroes.values() if isinstance(G.heroes, dict) else G.heroes
        missing = [h.name for h in heroes if str(h.id) not in rows and str(h.id) not in gun_calibration()]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
