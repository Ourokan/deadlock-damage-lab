"""Solomon (2026-11-08, scripts/mechanics/solomon_bishop.py): a Setup Bishop move hits for ImpactDamage and its
squares are separate Damage hits (not a DoT), and Checkmate's execute kills without booking damage.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, duel  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.heroes import chessmaster  # noqa: E402


def bishop_dmg(real):
    old = chessmaster.BISHOP_REAL
    chessmaster.BISHOP_REAL = real
    try:
        r = duel(Loadout("Solomon", ["Extra Spirit"], souls=15000), Loadout("Abrams", ["Extra Health"], souls=15000))
        return r.a_dmg.get("Setup Bishop", 0.0), r.a_dmg.get("Setup Bishop squares", 0.0)
    finally:
        chessmaster.BISHOP_REAL = old


class SolomonBishop(unittest.TestCase):
    def test_moves_hit_harder_and_squares_land(self):
        move_old, sq_old = bishop_dmg(False)
        move_new, sq_new = bishop_dmg(True)
        self.assertGreater(move_new, move_old)   # ImpactDamage (70 + 2.0 x spirit) instead of Damage (25 + 0.85 x)
        self.assertGreater(sq_new, 0.0)

    def test_unbooked_execute_kills_without_damage(self):
        e = Engine()
        a = make_fighter(e, Loadout("Solomon", [], souls=9000))
        b = make_fighter(e, Loadout("Abrams", [], souls=9000))
        a.enemy, b.enemy = b, a
        b.hp = 150.0
        e.damage(a, b, b.hp + 1, "spirit", "Checkmate", ignore_resist=True, unbooked=True, procs=False)
        self.assertFalse(b.alive)
        self.assertNotIn("Checkmate", a.dmg_out)
        self.assertNotIn("Checkmate", b.dmg_in)


if __name__ == "__main__":
    unittest.main()
