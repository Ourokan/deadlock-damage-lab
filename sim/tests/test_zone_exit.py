"""Alchemical Fire walk-out: targets leave the fire after zone_exit_s unless stunned, immobilized or slowed.
Run from sim/: python3 -m unittest discover -s tests"""
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "damage")]

from deadsim.items_fx import held_share  # noqa: E402
from dummy import Dummy, damage_test  # noqa: E402


class _Mods:
    def __init__(self, **v):
        self.v = v

    def active(self, key):
        return bool(self.v.get(key))

    def values(self, key):
        return self.v.get(key, [])


class _Target:
    def __init__(self, **v):
        self.mods = _Mods(**v)


def fire(hero, zone_exit_s):
    r = damage_test(hero, ["Alchemical Fire"], souls=27000, aim="p75", marks=(15.0,),
                    dummy=Dummy(hp=3000, bullet_resist=0, spirit_resist=0, melee_resist=0, zone_exit_s=zone_exit_s))
    return r["sources"].get("Alchemical Fire", 0.0)


class ZoneExit(unittest.TestCase):
    def test_held_share(self):
        self.assertEqual(held_share(_Target()), 0.0)
        self.assertEqual(held_share(_Target(stun=[1])), 1.0)
        self.assertEqual(held_share(_Target(immobilize=[1])), 1.0)
        self.assertAlmostEqual(held_share(_Target(move_slow=[0.4])), 0.4)
        self.assertAlmostEqual(held_share(_Target(move_slow=[0.99])), 0.9)

    def test_no_hold_hero_only_gets_the_walk_out(self):
        """Calico doesn't hold the target in this fight: the fire deals well under half of its full 5 s once the
        target walks out. (Haze was the example until 2026-10-21; with her gun back after a short Bullet Dance her
        Sleep Dagger now lands while the fire burns, and the T3 wake-up slow keeps the target in it a bit longer.)"""
        stay, walk = fire("Calico", None), fire("Calico", 2.0)
        self.assertGreater(stay, 0)
        self.assertLess(walk, 0.45 * stay)

    def test_holds_keep_more_of_the_fire(self):
        """A hero with stuns and slows keeps a larger share of the fire than one without."""
        calico = fire("Calico", 2.0) / fire("Calico", None)
        kelvin = fire("Kelvin", 2.0) / fire("Kelvin", None)
        self.assertGreater(kelvin, calico)


if __name__ == "__main__":
    unittest.main()
