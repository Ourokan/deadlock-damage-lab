"""Paige's Plot Armor on a teammate (2026-11-07, Mechanics.plot_armor_self, opt-in): each cast stays on Paige with
that chance when the fight draws (phase or rng), else her bonuses are scaled by it; 1.0 (default) self-casts all."""
import dataclasses
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from deadsim.heroes import bookworm  # noqa: E402
from deadsim.mechanics import DEFAULT  # noqa: E402


def fake(share, phase=None, rng=None):
    me = type("F", (), {"name": "Paige", "skill": type("S", (), {"fight_phase": phase})(),
                        "e": type("E", (), {"rng": rng})()})()
    return type("C", (), {"engine": type("E", (), {"mech": dataclasses.replace(DEFAULT, plot_armor_self=share)})(),
                          "me": me})()


class PlotArmorSelf(unittest.TestCase):
    def ab(self):
        a = bookworm.PlotArmor.__new__(bookworm.PlotArmor)
        a.s = type("St", (), {"casts": 0})()
        return a

    def test_default_off(self):
        self.assertEqual(DEFAULT.plot_armor_self, 1.0)
        self.assertEqual(self.ab().on_self(fake(1.0, rng=random.Random(1))), 1.0)

    def test_deterministic_scales(self):
        self.assertAlmostEqual(self.ab().on_self(fake(0.52)), 0.52)

    def test_draws_share(self):
        a, rng = self.ab(), random.Random(7)
        c = fake(0.52, rng=rng)
        draws = [a.on_self(c) for _ in range(4000)]
        self.assertTrue(set(draws) <= {0.0, 1.0})
        self.assertAlmostEqual(sum(draws) / len(draws), 0.52, delta=0.03)

    def test_phase_draws_vary_by_cast(self):
        a = self.ab()
        out = []
        for n in range(200):
            a.s.casts = n
            out.append(a.on_self(fake(0.52, phase=0.3)))
        self.assertAlmostEqual(sum(out) / len(out), 0.52, delta=0.1)


if __name__ == "__main__":
    unittest.main()
