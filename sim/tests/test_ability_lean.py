"""Abilities by build (2026-10-28): with Mechanics.ability_lean, a build's first-cast holds and recast waits are drawn
at hazard ratio exp(ability_lean x (spirit item souls - the hero's center) / 1000) of the hero's real curves, so a
spirit build casts sooner and a gun build later.
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
from deadsim.mechanics import Mechanics, lean_center, lean_u, recast_rows, recast_wait  # noqa: E402

SPIRIT = ["Mystic Burst", "Improved Spirit", "Superior Duration"]
WEAPON = ["Headshot Booster"]


class AbilityLean(unittest.TestCase):
    def fighter(self, mech, items):
        return make_fighter(Engine(mech=mech), Loadout("Haze", items, souls=12000))

    def test_hazard(self):
        G = game()
        m = dataclasses.replace(Mechanics(), ability_lean=0.006)
        souls = sum(G.item(n).cost for n in SPIRIT)
        c = lean_center(G.hero("Haze").id)
        self.assertAlmostEqual(self.fighter(m, SPIRIT).cast_hazard, math.exp(0.006 * (souls - c) / 1000))
        self.assertLess(self.fighter(m, WEAPON).cast_hazard, 1.0)        # under the center: later
        off = dataclasses.replace(Mechanics(), ability_lean=0.0)
        self.assertEqual(self.fighter(off, SPIRIT).cast_hazard, 1.0)

    def test_quantile(self):
        class F:
            cast_hazard = 1.0
        f = F()
        self.assertEqual(lean_u(f, 0.4), 0.4)
        f.cast_hazard = 1.5
        self.assertLess(lean_u(f, 0.4), 0.4)       # sooner on the same curve
        self.assertAlmostEqual(1 - (1 - lean_u(f, 0.4)) ** 1.5, 0.4)   # P(by t) = 1 - (1 - P(t)) ^ hr
        f.cast_hazard = 0.7
        self.assertGreater(lean_u(f, 0.4), 0.4)
        self.assertLess(lean_u(f, 0.999), 1.0)

    def test_default_off(self):
        self.assertEqual(Mechanics().ability_lean, 0.0)   # opt-in: the searches' scores don't move

    def test_recast_wait_uses_hazard(self):
        f = self.fighter(Mechanics(), SPIRIT)
        f.skill = dataclasses.replace(f.skill, fight_phase=0.37)
        ab = next(a for a in f.abilities if a.max_charges() == 1 and not a.ab.ultimate
                  and f"{f.st.hero.id}:{a.ab.class_name}" not in recast_rows()["skip"])
        base = recast_wait(ab)
        f.cast_hazard = 5.0
        self.assertLessEqual(recast_wait(ab), base)
        self.assertLess(recast_wait(ab), max(base, 1e-9) if math.isfinite(base) else math.inf)


if __name__ == "__main__":
    unittest.main()
