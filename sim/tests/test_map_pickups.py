"""Permanent map pickups by net worth (Mechanics.map_pickups, data/map_pickups.json from
scripts/mechanics/map_pickups.py, 2026-11-11). Run from sim/: python3 -m unittest tests.test_map_pickups"""
import dataclasses
import os
import random
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
from deadsim.build import compute_stats  # noqa: E402
from deadsim.mechanics import DEFAULT as MECH, apply_map_pickups, map_pickups_at  # noqa: E402

load_heroes()


class MapPickups(unittest.TestCase):
    def test_curve_grows_with_net_worth(self):
        lo, hi = map_pickups_at(5000), map_pickups_at(37000)
        for k in ("weapon_pct", "fire_rate_pct", "spirit", "health"):
            self.assertGreater(hi[k], 3 * lo[k])
        self.assertTrue(8 < hi["weapon_pct"] < 14)   # real Phantom+: +10.6% weapon damage at 37k
        self.assertTrue(80 < hi["health"] < 140)

    def test_apply_adds_to_stats(self):
        st = compute_stats("Haze", [], 37000)
        hp, sp, wp, fr = st.max_health, st.spirit_power, st.weapon_pct, st.fire_rate_pct
        pk = map_pickups_at(37000)
        apply_map_pickups(st, pk)
        self.assertAlmostEqual(st.max_health - hp, pk["health"])
        self.assertAlmostEqual(st.spirit_power - sp, pk["spirit"])
        self.assertAlmostEqual(st.weapon_pct - wp, pk["weapon_pct"] / 100)
        self.assertAlmostEqual(st.fire_rate_pct - fr, pk["fire_rate_pct"] / 100)

    def test_duel_gun_damage_up(self):
        def gun(on):
            sk = Skill(accuracy=0.5, use_abilities=False)
            foe = Loadout("Abrams", [], souls=37000, skill=Skill(accuracy=0.0, use_abilities=False))
            r = duel(Loadout("Haze", [], souls=37000, skill=sk), foe, max_time=4.0, rng=random.Random(3),
                     mechanics=dataclasses.replace(MECH, map_pickups=on))
            return sum(v for k, v in r.a_dmg.items() if "gun" in k.lower() or k == "Gun")
        on, off = gun(True), gun(False)
        self.assertGreater(off, 0.0)
        self.assertGreater(on, off * 1.03)


if __name__ == "__main__":
    unittest.main()
