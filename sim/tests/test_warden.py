"""Warden's Last Stand (deadsim/heroes/warden.py, PULSE_FREE): the gun lock and resists last for the 2 s charge only,
and a stun in the charge cancels the pulses. Run from sim/:
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
from deadsim.heroes import warden  # noqa: E402


class LastStandCase(unittest.TestCase):
    def setUp(self):
        self.e = Engine(distance=8, max_time=30)
        self.f = make_fighter(self.e, Loadout("Warden", [], souls=20000, skill=Skill(accuracy=1.0),
                                              tiers=[0, 0, 0, 0], unlocked=[True] * 4))
        self.g = make_fighter(self.e, Loadout("Abrams", [], souls=20000))
        self.f.enemy, self.g.enemy = self.g, self.f
        for s in self.f.abilities + self.g.abilities:
            s.start()
        self.ls = next(s for s in self.f.abilities if s.ab.class_name == "ability_warden_riot_protocol")

    def run_queue(self, until):
        while self.e.q and self.e.q[0][0] <= until:
            t, _, fn, args = heapq.heappop(self.e.q)
            self.e.t = t
            fn(*args)
        self.e.t = until

    def test_gun_and_resists_free_after_charge(self):
        self.assertTrue(warden.PULSE_FREE)
        charge = self.ls.ctx.raw("AbilityCastDelay")
        self.ls.impl.cast(self.ls.ctx)
        self.assertGreaterEqual(self.f.gun_locked_until, charge - 1e-9)
        self.assertLess(self.f.gun_locked_until, charge + 0.1)
        self.assertTrue(self.f.mods.active("bullet_resist"))
        self.run_queue(charge + 1.6)
        self.assertFalse(self.f.mods.active("bullet_resist"))
        self.assertGreater(self.f.dmg_out.get("Last Stand", 0), 0)

    def test_stun_in_charge_cancels(self):
        """A 0.3 s stun inside the charge, gone before the first pulse, still cancels it."""
        self.ls.impl.cast(self.ls.ctx)
        self.run_queue(0.8)
        self.f.mods.add("stun", 1, 0.3, "test")
        self.run_queue(4.0)
        self.assertEqual(self.f.dmg_out.get("Last Stand", 0), 0)
        self.assertFalse(self.f.mods.active("bullet_resist"))
        self.assertLessEqual(self.f.gun_locked_until, 1.1)

    def test_stun_while_pulsing_does_not_cancel(self):
        charge = self.ls.ctx.raw("AbilityCastDelay")
        self.ls.impl.cast(self.ls.ctx)
        self.run_queue(charge + 1.2)
        before = self.f.dmg_out.get("Last Stand", 0)
        self.f.mods.add("stun", 1, 1.0, "test")
        self.run_queue(charge + 3.0)
        self.assertGreater(self.f.dmg_out.get("Last Stand", 0), before)


if __name__ == "__main__":
    unittest.main()
