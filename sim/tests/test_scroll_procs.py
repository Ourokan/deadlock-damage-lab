"""Lightning Scroll procs per ult damage (items_fx.SCROLL_PER_ULT_DMG, 2026-11-08, scripts/mechanics/scroll_procs.py):
real procs hit each enemy hero the ult damages, so a hero with a replay rate gets a share of a proc per point of ult
damage dealt; the others keep one proc per cast, 3 s after its first ult hit. Run: python3 -m unittest discover -s tests
-v (from sim/)."""
import os
import sys
import types
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import items_fx  # noqa: E402
from deadsim.engine import Hit  # noqa: E402
from test_imbue_items import pair  # noqa: E402


def ult_hit(amount):
    return Hit("spirit", "ult", amount, amount, is_ability=True, ability=types.SimpleNamespace(scratch={}), is_ult=True)


class ScrollProcs(unittest.TestCase):
    def setUp(self):
        self.old = items_fx.SCROLL_ULT_DMG
        items_fx.SCROLL_ULT_DMG = True

    def tearDown(self):
        items_fx.SCROLL_ULT_DMG = self.old

    def setup(self, hero):
        e, f, g = pair(["Lightning Scroll"], hero=hero)
        e.max_time = 30
        g.hp = g.max_hp_base = 1e12
        fx = next(x for x in f.items_fx if x.name == "Lightning Scroll")
        return e, f, g, fx

    def test_rate_hero_gets_procs_per_ult_damage(self):
        e, f, g, fx = self.setup("McGinnis")
        h = ult_hit(1000.0)
        fx.on_damage_dealt(f, g, h)
        fx.on_damage_dealt(f, g, ult_hit(1000.0))
        got = f.dmg_out.get("Lightning Scroll", 0.0)
        one = fx.v("Damage")
        self.assertGreater(got, 0)   # booked with the hit
        self.assertAlmostEqual(got / one, 2000 * items_fx.SCROLL_PER_ULT_DMG["McGinnis"], delta=0.6)

    def test_other_heroes_keep_one_proc_per_cast(self):
        e, f, g, fx = self.setup("Graves")
        a = types.SimpleNamespace(scratch={})
        for _ in range(3):
            fx.on_damage_dealt(f, g, Hit("spirit", "ult", 500.0, 500.0, is_ability=True, ability=a, is_ult=True))
        self.assertEqual(f.dmg_out.get("Lightning Scroll", 0.0), 0.0)   # 3 s later
        calls = []
        e.after = lambda d, fn, *a: calls.append((d, fn))
        fx.on_damage_dealt(f, g, Hit("spirit", "ult", 500.0, 500.0, is_ability=True, ability=types.SimpleNamespace(scratch={}),
                                     is_ult=True))
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0], fx.item.p("DelayBeforeStun", 3))
        calls[0][1]()
        self.assertAlmostEqual(f.dmg_out["Lightning Scroll"] / fx.v("Damage"), 1.0, delta=0.5)


if __name__ == "__main__":
    unittest.main()
