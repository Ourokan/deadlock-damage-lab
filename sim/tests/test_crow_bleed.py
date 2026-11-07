"""Vindicta's Crow Familiar bleed (2026-11-07): replays show each tick as a share of the health the target has
then, on targets well below full health (Fighter.item_hp: real entry deficit and third parties' damage), and real
bleeds often end early without a kill (opt-in BLEED_BREAK: a per-tick break chance by game phase, booked as an
expected value).
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, duel  # noqa: E402
from deadsim.heroes import hornet  # noqa: E402


def crow(souls=20000, current=True, brk=True):
    old = hornet.BLEED_CURRENT, hornet.BLEED_BREAK
    hornet.BLEED_CURRENT, hornet.BLEED_BREAK = current, brk
    try:
        r = duel(Loadout("Vindicta", ["Extra Spirit", "Mystic Burst"], souls=souls),
                 Loadout("Abrams", ["Extra Health"], souls=souls))
        return r.a_dmg.get("Crow Familiar", 0.0)
    finally:
        hornet.BLEED_CURRENT, hornet.BLEED_BREAK = old


class CrowBleed(unittest.TestCase):
    def test_hazard_by_phase(self):
        old = hornet.BLEED_BREAK
        try:
            hornet.BLEED_BREAK = True   # opt-in
            self.assertLess(hornet.break_hazard(5000), hornet.break_hazard(20000))
            self.assertLess(hornet.break_hazard(20000), hornet.break_hazard(40000))
            hornet.BLEED_BREAK = False
            self.assertEqual(hornet.break_hazard(40000), 0.0)
        finally:
            hornet.BLEED_BREAK = old

    def test_break_lowers_bleed(self):
        full, cut = crow(brk=False), crow(brk=True)
        self.assertGreater(cut, 0.0)
        self.assertLess(cut, full)

    def test_plain_duel_health_without_mechanics(self):
        # a plain duel draws no entry deficit, so item_hp is plain health: BLEED_CURRENT changes nothing there
        self.assertAlmostEqual(crow(current=True, brk=False), crow(current=False, brk=False), places=6)


if __name__ == "__main__":
    unittest.main()
