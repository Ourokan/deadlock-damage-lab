"""Items changed by the 10-30 hotfix (validation/hotfix_items.md): Shadow Weave's ambush can give +50% weapon damage
(opt-in ShadowWeave.AMBUSH_WEAPON; it used to be +25% fire rate, a property the game data no longer has); Rebuttal holders parry 1.62x as often.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.items_fx import ShadowWeave  # noqa: E402
from deadsim.mechanics import Rebuttal  # noqa: E402


class ShadowWeaveAmbush(unittest.TestCase):
    def test_ambush_buffs_weapon_damage(self):
        e = Engine()
        a = make_fighter(e, Loadout("Haze", ["Shadow Weave"], souls=15000))
        b = make_fighter(e, Loadout("Abrams", [], souls=15000))
        a.enemy, b.enemy = b, a
        fx = next(x for x in a.items_fx if isinstance(x, ShadowWeave))
        self.assertFalse(ShadowWeave.AMBUSH_WEAPON)   # opt-in, off by default
        ShadowWeave.AMBUSH_WEAPON = True
        self.addCleanup(setattr, ShadowWeave, "AMBUSH_WEAPON", False)
        before = a.weapon_pct()
        if not a.skill.use_actives:
            self.skipTest("default skill does not use actives")
        fx.on_start(a)
        bonus = fx.item.p("AmbushBonusWeaponDamage") / 100
        self.assertGreater(bonus, 0)
        self.assertAlmostEqual(a.weapon_pct() - before, bonus, places=6)


class RebuttalParries(unittest.TestCase):
    def test_post_hotfix_parry_multiplier(self):
        self.assertAlmostEqual(Rebuttal.REBUTTAL_PARRY_MULT, 1.62)


if __name__ == "__main__":
    unittest.main()
