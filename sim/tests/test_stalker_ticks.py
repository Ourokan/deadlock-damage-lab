import dataclasses
import os
import sys
import unittest
from types import SimpleNamespace as NS

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from deadsim import Loadout  # noqa: E402
from deadsim.data import game  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.items_fx import Stalker  # noqa: E402
from deadsim.mechanics import Mechanics, stalker_ticks_mult  # noqa: E402


class StalkerTicks(unittest.TestCase):
    def test_curve(self):
        lo, hi = stalker_ticks_mult(5000), stalker_ticks_mult(40000)
        self.assertTrue(0.9 < lo <= 1.0)
        self.assertTrue(0.6 < hi < 0.72)
        self.assertGreater(lo, stalker_ticks_mult(16000))
        self.assertEqual(stalker_ticks_mult(0), 1.0)

    def proc(self, on, souls):
        e = Engine(mech=dataclasses.replace(Mechanics(), stalker_ticks=on))
        a = make_fighter(e, Loadout("Haze", [], souls=souls))
        b = make_fighter(e, Loadout("Abrams", [], souls=souls))
        a.enemy, b.enemy = b, a
        it = next(i for i in game().items.values() if i.class_name == "upgrade_weapon_backstabber")
        fx = Stalker(it, a)
        fx.reach_share = lambda m: 1.0
        got = {}
        e.dot = lambda f, t, dps, d, name, **k: got.__setitem__("dps", dps)
        fx.debuff = lambda t, key, v, d: got.__setitem__("shred", v)
        fx.on_damage_dealt(a, b, NS(kind="bullet", hits=1))
        return got

    def test_handler(self):
        off, on = self.proc(False, 40000), self.proc(True, 40000)
        self.assertAlmostEqual(on["dps"], off["dps"] * stalker_ticks_mult(40000), places=6)
        self.assertAlmostEqual(on["shred"], off["shred"], places=9)   # the shred is not scaled


if __name__ == "__main__":
    unittest.main()
