"""Viscous' item procs (2026-10-28, validation/README.md "Viscous: Express Shot on the alt fire"): Express Shot's proc
shot is his alt-fire goo shot (its base damage, with the item's alt-fire bonus), and a landed Puddle Punch procs
on-melee items in full rather than in its landing factor's share.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import types
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, game  # noqa: E402
from deadsim import items_fx  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def proc_over_gun(hero):
    """First trigger pull (the proc shot, booked under Express Shot) over the next one (a plain gun shot)."""
    e = Engine(distance=10.0)
    a = make_fighter(e, Loadout(hero, ["Express Shot"], souls=20000))
    b = make_fighter(e, Loadout("Abrams", [], souls=20000))
    a.enemy, b.enemy = b, a
    a.skill = a.skill.__class__(accuracy=1.0, headshot=0.0)
    e.fire(a)
    es = a.dmg_out.get("Express Shot", 0.0)
    e.fire(a)
    return es / a.dmg_out["gun"]


class ExpressShotAltFire(unittest.TestCase):
    def test_alt_ratio_from_data(self):
        self.assertAlmostEqual(items_fx.alt_bullet_ratio(game().hero("Viscous").id), 42.0 / 10.34, delta=1.0)
        self.assertIsNone(items_fx.alt_bullet_ratio(game().hero("Haze").id))

    def test_viscous_proc_is_the_alt_shot(self):
        # two alt shots at ~4x a primary bullet each, against two primary bullets with +125% for a one-bullet gun
        self.assertGreater(proc_over_gun("Viscous"), 1.8 * proc_over_gun("Seven"))


class PuddlePunchProcs(unittest.TestCase):
    def test_full_weight_despite_landing(self):
        e = Engine()
        a = make_fighter(e, Loadout("Viscous", ["Spirit Snatch"], souls=9000))
        fx = next(x for x in a.items_fx if x.item.name == "Spirit Snatch")
        ab = types.SimpleNamespace(ab=types.SimpleNamespace(class_name="viscous_telepunch"))
        hit = types.SimpleNamespace(source="Puddle Punch", ability=ab, landing=0.3)
        self.assertTrue(all(items_fx._melee_proc(fx, a, hit) for _ in range(5)))
        other = types.SimpleNamespace(source="Rend", ability=types.SimpleNamespace(ab=types.SimpleNamespace(
            class_name="drifter_blood_blast")), landing=0.3)
        self.assertLess(sum(items_fx._melee_proc(fx, a, other) for _ in range(10)), 10)


if __name__ == "__main__":
    unittest.main()
