"""Vyper's Lethal Venom misses (heroes/viper.py VENOM_MISS, 2026-11-08): with fight draws a cast venom misses a living
target at the real rate (15% of in-fight casts in Phantom+ replays); without draws, or switched off (the default),
every cast lands.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import random
import sys
import types
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim.heroes import viper  # noqa: E402


def ctx(phase=None, rng=None):
    f = types.SimpleNamespace(skill=types.SimpleNamespace(fight_phase=phase), e=types.SimpleNamespace(rng=rng),
                              name="Vyper")
    return types.SimpleNamespace(me=f, state={})


def venom():
    return viper.LethalVenom.__new__(viper.LethalVenom)


class VenomMiss(unittest.TestCase):
    def setUp(self):
        self.old = viper.VENOM_MISS
        viper.VENOM_MISS = 0.152   # opt-in (off by default)

    def tearDown(self):
        viper.VENOM_MISS = self.old

    def test_no_draws_always_lands(self):
        c = ctx()
        self.assertFalse(any(venom().missed(c) for _ in range(100)))

    def test_rng_miss_rate(self):
        c, v = ctx(rng=random.Random(3)), venom()
        n = 20000
        self.assertAlmostEqual(sum(v.missed(c) for _ in range(n)) / n, 0.152, delta=0.01)

    def test_phase_draws_spread_over_casts(self):
        n = 4000
        rate = sum(venom().missed(c) for c in [ctx(phase=k / n) for k in range(n)] for _ in range(3)) / (3 * n)
        self.assertAlmostEqual(rate, 0.152, delta=0.02)

    def test_switch_off(self):
        viper.VENOM_MISS = 0.0
        c = ctx(rng=random.Random(1))
        self.assertFalse(any(venom().missed(c) for _ in range(100)))


if __name__ == "__main__":
    unittest.main()
