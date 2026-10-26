"""Baba's abilities (deadsim/heroes/baba.py): Threadsap's stolen spirit and per-bullet damage, Granny Long Legs' ground
pound, Feed The Birds' hex. Run from sim/:
    python3 -m unittest discover -s tests
"""
import heapq
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


class BabaCase(unittest.TestCase):
    def setUp(self):
        self.e = Engine(distance=8, max_time=30)
        sk = Skill(accuracy=1.0, headshot=0.0)
        sk.spirit_accuracy = 1.0
        self.f = make_fighter(self.e, Loadout("Baba", [], souls=20000, skill=sk, tiers=[0, 0, 0, 0],
                                              unlocked=[True] * 4))
        self.g = make_fighter(self.e, Loadout("Abrams", [], souls=20000))
        self.f.enemy, self.g.enemy = self.g, self.f
        for s in self.f.abilities + self.g.abilities:
            s.start()
        self.ab = {s.ab.class_name: s for s in self.f.abilities}

    def run_queue(self, until):
        while self.e.q and self.e.q[0][0] <= until:
            t, _, fn, args = heapq.heappop(self.e.q)
            self.e.t = t
            fn(*args)
        self.e.t = until

    def test_threadsap_steals_spirit_and_powers_bullets(self):
        sp0, foe0 = self.f.spirit_power(), self.g.spirit_power()
        self.ab["ability_baba_bubbling_brew"].cast()
        self.run_queue(1.5)
        self.assertGreater(self.f.spirit_power(), sp0)
        self.assertLess(self.g.spirit_power(), foe0)
        self.e.damage(self.f, self.g, 10.0, "bullet", "gun", hits=3)
        self.assertGreater(self.f.dmg_out.get("Threadsap (gun)", 0), 0)

    def test_ground_pound_only_during_granny_long_legs(self):
        self.f.counters["melee_heavy"] = True
        self.e.melee_hit(self.f, True)
        self.assertEqual(self.f.dmg_out.get("Granny Long Legs", 0), 0)
        self.ab["ability_baba_bench_run"].cast()
        self.e.melee_hit(self.f, True)
        self.assertGreater(self.f.dmg_out.get("Granny Long Legs", 0), 0)

    def test_granny_long_legs_turns_heavies_up(self):
        from deadsim.heroes import baba
        self.ab["ability_baba_bench_run"].cast()
        share, until = self.f.counters["heavy_share"]
        self.assertEqual(share, baba.GLL_HEAVY_SHARE)
        self.assertAlmostEqual(until, self.e.t + self.ab["ability_baba_bench_run"].ctx.dur("AbilityDuration"))

    def test_melee_tick_uses_the_heavy_share_only_while_up(self):
        heavies = []
        self.e.melee_hit = lambda f, heavy, w=1.0: heavies.append(heavy)
        self.e.after = lambda *a, **k: None
        self.f.gun_locked_until = -1.0
        self.f.skill.melee_rate = 1.0
        self.f.counters["heavy_share"] = (0.71, 50.0)
        for _ in range(100):
            self.e.melee_tick(self.f)
        self.assertEqual(sum(heavies), 71)
        heavies.clear()
        self.e.t = 50.0
        for _ in range(100):
            self.e.melee_tick(self.f)
        self.assertAlmostEqual(sum(heavies), 100 * self.f.skill.heavy_share, delta=1)

    def test_melee_bunches_into_granny_long_legs(self):
        from deadsim.heroes import baba
        landed = []
        self.e.melee_hit = lambda f, heavy, w=1.0: landed.append(w)
        self.e.after = lambda *a, **k: None
        self.f.gun_locked_until = -1.0
        self.f.skill.melee_rate = 0.1
        self.g.skill.parry_rate = 0.0   # parried heavies swing more: not this test
        self.e.melee_tick(self.f)
        off = landed.pop()
        self.ab["ability_baba_bench_run"].cast()
        self.e.melee_tick(self.f)
        on = landed.pop()
        self.assertAlmostEqual(on / off, baba.GLL_MELEE_RATIO)
        # the fitted rate is kept on average at the real bench uptime
        u = baba.GLL_UPTIME
        self.assertAlmostEqual(u * on + (1 - u) * off, 0.1 * 0.5)
        self.e.t = self.f.counters["melee_focus"][2]   # the bench is down: back to the off rate
        self.e.melee_tick(self.f)
        self.assertAlmostEqual(landed.pop(), off)

    def test_first_brew_is_prebrewed(self):
        br = self.ab["ability_baba_hexing_brew"]
        br.cast()
        self.run_queue(br.ctx.raw("FireLockTime") - 0.5)        # a brewed throw would not land yet
        first = self.f.dmg_out.get("Baba's Brew", 0)
        self.assertGreater(first, 0)                             # the first throw needs no brewing
        self.assertTrue(br.scratch["thrown"])

    def test_repeat_brew_waits_the_brew_time(self):
        br = self.ab["ability_baba_hexing_brew"]
        br.cast()
        self.run_queue(20.0)
        first = self.f.dmg_out["Baba's Brew"]
        br.cast()
        self.run_queue(20.0 + br.ctx.raw("FireLockTime") - 0.5)
        self.assertAlmostEqual(self.f.dmg_out["Baba's Brew"], first)

    def test_brew_t3_multiplies_burn_and_shred_once(self):
        f = make_fighter(self.e, Loadout("Baba", [], souls=20000, tiers=[0, 0, 3, 0], unlocked=[True] * 4))
        br = next(s for s in f.abilities if s.ab.class_name == "ability_baba_hexing_brew")
        base = self.ab["ability_baba_hexing_brew"].ctx
        self.assertAlmostEqual(br.ctx.raw("SpiritResistReduction"), base.raw("SpiritResistReduction") * 4 / 3, places=2)
        self.assertAlmostEqual(br.ctx.raw("DamagePerSecond"), base.raw("DamagePerSecond") * 4 / 3, places=2)

    def test_feed_the_birds_hexes(self):
        self.ab["ability_baba_ultimate_2"].cast()
        self.run_queue(5.5)
        self.assertGreater(self.f.dmg_out.get("Feed The Birds", 0), 0)
        self.assertTrue(self.g.mods.active("stun"))


if __name__ == "__main__":
    unittest.main()
