"""Gun time by build (2026-10-27): with Mechanics.gun_lean, the gun's fire interval and reload are / exp(-gun_lean x
souls in spirit items / 1000), so a spirit build fires fewer bullets in the same time.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, game  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.mechanics import Mechanics, gun_lean_row  # noqa: E402

SPIRIT = ["Mystic Burst", "Improved Spirit"]
WEAPON = ["Headshot Booster"]


class GunLean(unittest.TestCase):
    def fighter(self, mech, items):
        return make_fighter(Engine(mech=mech), Loadout("Haze", items, souls=9000))

    def test_uptime(self):
        G = game()
        m = dataclasses.replace(Mechanics(), gun_lean=0.03, gun_lean_hero=False)
        souls = sum(G.item(n).cost for n in SPIRIT)
        self.assertAlmostEqual(self.fighter(m, SPIRIT + WEAPON).gun_uptime, math.exp(-0.03 * souls / 1000))
        self.assertEqual(self.fighter(m, WEAPON).gun_uptime, 1.0)        # weapon items: no change
        self.assertEqual(self.fighter(None, SPIRIT).gun_uptime, 1.0)     # no mechanics: as before
        off = dataclasses.replace(Mechanics(), gun_lean=0.0, gun_lean_hero=False)
        self.assertEqual(self.fighter(off, SPIRIT).gun_uptime, 1.0)

    def test_fewer_shots(self):
        def shots(lean):
            e = Engine(mech=dataclasses.replace(Mechanics(), gun_lean=lean, gun_lean_hero=False), max_time=4.0)
            a = make_fighter(e, Loadout("Haze", SPIRIT, souls=9000))
            b = make_fighter(e, Loadout("Abrams", [], souls=9000))
            e.run(a, b)
            return a.shots_fired
        full, lean = shots(0.0), shots(0.2)
        self.assertGreater(full, 0)
        self.assertLess(lean, full * 0.75)   # uptime 0.62 here

    def test_hero_k(self):
        """gun_lean_hero (2026-11-07): the hero's own slope k around its center (data/gun_lean_hero.json), at most 1"""
        G = game()
        souls = sum(G.item(n).cost for n in SPIRIT)
        k, c = gun_lean_row(G.hero("Haze").id)
        on = dataclasses.replace(Mechanics(), gun_lean=0.03, gun_lean_hero=True)
        want = min(1.0, math.exp(-0.03 * souls / 1000 - (k - 0.03) * (souls - c) / 1000))
        self.assertAlmostEqual(self.fighter(on, SPIRIT).gun_uptime, want)
        self.assertLessEqual(self.fighter(on, WEAPON).gun_uptime, 1.0)
        self.assertIsNone(gun_lean_row(-1))   # no row: the pooled curve

if __name__ == "__main__":
    unittest.main()
