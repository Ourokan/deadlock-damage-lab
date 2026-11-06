"""Apollo's Riposte immobilizes since the late-October 2026 hotfix (deadsim/heroes/fencer.py RIPOSTE_CC). Run from sim/:
    python3 -m unittest discover -s tests
"""
import heapq
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


class TestRiposte(unittest.TestCase):
    def test_counter_immobilizes_not_stuns(self):
        e = Engine(distance=5, max_time=60, mech=None)
        f = make_fighter(e, Loadout("Apollo", [], souls=20000))
        g = make_fighter(e, Loadout("Abrams", [], souls=20000))
        f.enemy, g.enemy = g, f
        for s in f.abilities + g.abilities:
            s.start()
        rip = {s.ab.class_name: s for s in f.abilities}["ability_fencer_riposte"]
        rip.cast()
        rip.impl.counter(rip.ctx)
        self.assertTrue(g.mods.active("immobilize"))
        self.assertFalse(g.mods.active("stun"))
        self.assertTrue(g.can_shoot() or g.clip == 0)


if __name__ == "__main__":
    unittest.main()
