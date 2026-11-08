"""Nurse's Quicksilver Reload follows her Leech Therapy casts (2026-11-08, validation/README.md "Nurse's Quicksilver
Reload follows her Leech Therapy casts"): Leech Therapy's landing factor above 1 stands for more real casts, each
spending a charge, so the imbued charge damage scales by it (items_fx.LANDING_PROCS, IMBUE_LANDING_PROCS); Leech
ticks are DoTs, so Mystic Burst / Tankbuster (which skip DoT hits) are not touched.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import types
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim import items_fx  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def charge(cls, landing, item="Quicksilver Reload", is_dot=True):
    """Spirit damage the item deals off one hit of ability cls at this landing factor, the charge pending."""
    e = Engine()
    a = make_fighter(e, Loadout("Nurse Harrow", [item], souls=15000))
    b = make_fighter(e, Loadout("Abrams", [], souls=15000))
    a.enemy, b.enemy = b, a
    fx = next(x for x in a.items_fx if x.item.name == item)
    got = []
    fx.spirit = lambda t, dmg, **kw: got.append(dmg)
    e.damage = lambda src, dst, raw, kind, source, **kw: got.append(raw) or raw
    ab = types.SimpleNamespace(ab=types.SimpleNamespace(class_name=cls), impl=None)
    if isinstance(fx, items_fx.ImbueCharge):
        fx.pending = ab
    hit = types.SimpleNamespace(is_ability=True, is_dot=is_dot, kind="spirit", ability=ab, landing=landing,
                                amount=200.0 * landing, pre_mit=200.0, gun_bullet=lambda: False)
    fx.on_damage_dealt(a, b, hit)
    return sum(got)


class QuicksilverOnLeech(unittest.TestCase):
    def test_charge_follows_leech_landing_above_one(self):
        full = charge("ability_nurse_leech_therapy", 1.0)
        self.assertGreater(full, 0)
        self.assertAlmostEqual(charge("ability_nurse_leech_therapy", 2.26), 2.26 * full, delta=1e-6)
        self.assertAlmostEqual(charge("ability_nurse_leech_therapy", 0.6), full, delta=1e-6)   # below 1: whole
        self.assertAlmostEqual(charge("ability_nurse_fear", 2.0), full, delta=1e-6)            # not listed

    def test_switch_off_restores_one_charge(self):
        full = charge("ability_nurse_leech_therapy", 1.0)
        old = items_fx.IMBUE_LANDING_PROCS
        items_fx.IMBUE_LANDING_PROCS = False
        try:
            self.assertAlmostEqual(charge("ability_nurse_leech_therapy", 2.26), full, delta=1e-6)
        finally:
            items_fx.IMBUE_LANDING_PROCS = old

    def test_leech_ticks_release_no_mystic_burst(self):
        self.assertEqual(charge("ability_nurse_leech_therapy", 2.26, item="Mystic Burst"), 0)


if __name__ == "__main__":
    unittest.main()
