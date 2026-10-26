"""McGinnis's Mini Turret pacing (forge.TURRET_PACING, data/turret_gaps.json). Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, duel  # noqa: E402
from deadsim.heroes import forge  # noqa: E402
from deadsim.mechanics import DEFAULT as MECH, real_length  # noqa: E402


def turrets_by(t, pacing, n=40):
    """Mean Mini Turrets McGinnis (tier 2: three charges) casts by t s into 20 s duels on real fight lengths."""
    mech = MECH.__class__(**{**MECH.__dict__, "fight_length": real_length(20000)})
    saved, forge.TURRET_PACING = forge.TURRET_PACING, pacing
    try:
        total = 0
        for k in range(n):
            r = duel(Loadout("McGinnis", [], souls=20000, tiers=[2, 0, 0, 0]), Loadout("Abrams", [], souls=20000),
                     max_time=20, rng=random.Random(k), mechanics=mech, log=True)
            total += sum(1 for ln in r.log if "McGinnis" in ln.split("casts")[0] and "casts Mini Turret" in ln
                         and float(ln.split()[0]) <= t)
        return total / n
    finally:
        forge.TURRET_PACING = saved


class TestTurretPacing(unittest.TestCase):
    def test_gaps_per_phase(self):
        for souls in (5000, 20000, 40000):
            q = forge.turret_gaps(souls)
            self.assertEqual(len(q), 20)
            vals = [x for x in q if x is not None]
            self.assertEqual(vals, sorted(vals))
            self.assertGreater(vals[len(vals) // 2], 3.0)   # real players spread turrets wider than the 3 s charge gap

    def test_fewer_turrets_early_in_a_fight(self):
        off, on = turrets_by(10, False), turrets_by(10, True)
        self.assertGreater(off, 2.0)     # every charge on sight
        self.assertLess(on, 1.6)         # real 0.9-1.1 placed by 10 s
        self.assertGreater(on, 0.5)

    def test_deterministic_fights_unchanged(self):
        a = Loadout("McGinnis", [], souls=20000, tiers=[2, 0, 0, 0])
        b = Loadout("Abrams", [], souls=20000)
        r1 = duel(a, b)
        saved, forge.TURRET_PACING = forge.TURRET_PACING, False
        try:
            r2 = duel(a, b)
        finally:
            forge.TURRET_PACING = saved
        self.assertEqual(r1.a_dmg.get("Mini Turret"), r2.a_dmg.get("Mini Turret"))


if __name__ == "__main__":
    unittest.main()
