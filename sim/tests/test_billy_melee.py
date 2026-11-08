"""Billy's basic melee feeds Blasted (2026-11-08, validation/README.md "Billy's basic melee feeds Blasted"): the
engine's melee rotation hits reload BulletsReloadedPer{Light,Heavy}MeleePct of the clip and, while Blasted is
active, extend its window, as Bashdown's melee already did (punkgoat.ROTATION_MELEE).
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.heroes import punkgoat  # noqa: E402


def setup():
    e = Engine()
    a = make_fighter(e, Loadout("Billy", [], souls=15000, tiers=[1, 1, 1, 1]))
    b = make_fighter(e, Loadout("Abrams", [], souls=15000))
    a.enemy, b.enemy = b, a
    e.fighters = [a, b]
    bl = next(x for x in a.abilities if x.ab.class_name == "ability_punkgoat_blasted")
    bl.impl.start(bl.ctx)
    return e, a, bl


class RotationMelee(unittest.TestCase):
    def test_light_melee_reloads_and_extends(self):
        e, a, bl = setup()
        a.clip = 0
        bl.ctx.state["active_until"] = e.t + 5.0
        e.melee_hit(a, False, 1.0)
        want = int(a.st.clip * bl.ctx.raw("BulletsReloadedPerLightMeleePct") / 100 + 0.5)
        self.assertEqual(a.clip, want)
        self.assertGreater(bl.ctx.state["active_until"], e.t + 5.0)

    def test_fractional_hits_add_up(self):
        e, a, bl = setup()
        a.clip = 0
        for _ in range(10):
            e.melee_hit(a, False, 0.1)
        full = a.st.clip * bl.ctx.raw("BulletsReloadedPerLightMeleePct") / 100
        self.assertTrue(int(full) - 1 <= a.clip <= int(full) + 1, (a.clip, full))

    def test_switch_off(self):
        old = punkgoat.ROTATION_MELEE
        punkgoat.ROTATION_MELEE = False
        try:
            e, a, bl = setup()
            a.clip = 0
            e.melee_hit(a, False, 1.0)
            self.assertEqual(a.clip, 0)
        finally:
            punkgoat.ROTATION_MELEE = old


if __name__ == "__main__":
    unittest.main()
