"""Target health for health-conditional items (2026-10-26).

- Mechanics.target_health (on): in fights booked over real lengths, a fighter facing an Opening Rounds holder is seen
  by that item short by a real entry deficit and by TARGET_ASSIST x the damage it takes (the real fight's third
  parties, Fighter.item_hp_frac); its health, the fight's length and execute gates stay. An immortal enemy's refill
  starts a new life the item sees full.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim import mechanics as M  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def pair(items, seed=1):
    mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
    e = Engine(distance=10, mech=mech, rng=random.Random(seed))
    f = make_fighter(e, Loadout("Haze", items, souls=27000))
    g = make_fighter(e, Loadout("Abrams", [], souls=27000))
    f.enemy, g.enemy = g, f
    return e, f, g


class TargetHealth(unittest.TestCase):
    def test_on_by_default(self):
        self.assertTrue(M.DEFAULT.target_health)

    def test_only_against_a_holder(self):
        e, f, g = pair([])
        M.target_health(g)
        self.assertEqual(g.item_assist, 0.0)
        self.assertEqual(g.item_hp_frac, g.hp_frac)
        gaps = []
        for s in range(200):
            e, f, g = pair(["Opening Rounds"], seed=s)
            M.target_health(g)
            M.target_health(f)
            self.assertEqual(f.item_assist, 0.0)   # Abrams holds no such item
            self.assertEqual(g.item_assist, M.TARGET_ASSIST)
            self.assertEqual(g.hp, g.max_hp)       # health stays
            self.assertEqual(g.gate_frac, 1.0 - g.entry_gap)
            gaps.append(g.item_gap)
        self.assertTrue(any(x > 0.05 for x in gaps))
        self.assertGreater(sum(x == 0 for x in gaps), 0.3 * len(gaps))   # many fights start full

    def test_opening_rounds_sees_it(self):
        e, f, g = pair(["Opening Rounds"])
        fx = next(x for x in f.items_fx if x.item.class_name == "upgrade_pristine_emblem")
        g.item_assist, g.item_gap = 0.5, 0.0
        g.hp = 0.7 * g.max_hp
        g.dmg_in["gun"] = 0.3 * g.max_hp
        self.assertAlmostEqual(g.item_hp_frac, 0.55)
        self.assertTrue(fx.stat(f))
        g.item_gap = 0.1
        self.assertAlmostEqual(g.item_hp_frac, 0.45)
        self.assertFalse(fx.stat(f))

    def test_refill_is_a_new_life(self):
        e, f, g = pair(["Opening Rounds"])
        g.item_assist, g.item_gap = 0.5, 0.2
        g.dmg_in["gun"] = g.max_hp
        refill = type("Refill", (), {"on_lethal": lambda self, x, a: setattr(x, "hp", x.max_hp) or True})()
        g.items_fx.append(refill)
        e.fighters = [f, g]
        g.hp = 10.0
        e.damage(f, g, 1000.0, "bullet", "gun", ignore_resist=True)
        self.assertEqual(g.hp, g.max_hp)
        self.assertAlmostEqual(g.item_hp_frac, 1.0)


if __name__ == "__main__":
    unittest.main()
