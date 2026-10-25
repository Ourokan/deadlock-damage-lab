"""Vyper's Petrifying Bola timing (replays: lands a median 4.1 s into a fight). Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.heroes import viper  # noqa: E402


class TestBola(unittest.TestCase):
    def setUp(self):
        self.e = Engine(distance=10, max_time=30)
        self.f = make_fighter(self.e, Loadout("Vyper", [], souls=30000))
        self.g = make_fighter(self.e, Loadout("Abrams", [], souls=30000))
        self.f.enemy, self.g.enemy = self.g, self.f
        for s in self.f.abilities + self.g.abilities:
            s.start()
        self.bola = next(s for s in self.f.abilities if s.ab.class_name == "ability_viper_petrifybola")

    def wants(self):
        return self.bola.impl.should_cast(self.bola.ctx)

    def test_held_at_full_health(self):
        self.assertFalse(self.wants())

    def test_thrown_once_the_target_is_hurt(self):
        self.g.hp = self.g.max_hp * (viper.BOLA_CAST_HP - 0.05)
        self.assertTrue(self.wants())

    def test_thrown_anyway_late_in_the_fight(self):
        self.e.t = viper.BOLA_MAX_WAIT
        self.assertTrue(self.wants())


if __name__ == "__main__":
    unittest.main()
