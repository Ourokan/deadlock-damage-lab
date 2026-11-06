"""Apollo's Riposte immobilizes since the late-October 2026 hotfix (deadsim/heroes/fencer.py RIPOSTE_CC). Run from sim/:
    python3 -m unittest discover -s tests
"""
import json
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
        self.assertFalse(g.mods.active("disarm"))
        self.assertTrue(g.can_shoot())

    def test_apollo_follows_the_median_order(self):
        from deadsim.fight import ORDER_HEROES, default_ability_order
        from deadsim import game
        self.assertIn("Apollo", ORDER_HEROES)
        h = game().hero("Apollo")
        order = json.load(open(os.path.join(os.path.dirname(__file__), "..", "data", "ability_order.json")))
        self.assertEqual(list(default_ability_order(h)), order["heroes"][str(h.id)]["order"])


if __name__ == "__main__":
    unittest.main()
