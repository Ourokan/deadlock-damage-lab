"""Bullet resist shred in fights (2026-10-27): in-fight bullet_shred debuffs count x Mechanics.shred_uptime; damage a
barrier soaks is booked as dealt unless Mechanics.unbook_absorbed (opt-in).
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.mechanics import Mechanics  # noqa: E402


def pair(e):
    a = make_fighter(e, Loadout("Haze", [], souls=800))
    b = make_fighter(e, Loadout("Abrams", [], souls=800))
    a.enemy, b.enemy = b, a
    b.st.bullet_resist = [0.3]
    return a, b


class ShredUptime(unittest.TestCase):
    def hit(self, mech, shred):
        e = Engine(mech=mech)
        a, b = pair(e)
        if shred:
            b.mods.add("bullet_shred", shred, 10.0)
        e.damage(a, b, 100, "bullet", "gun")
        return a.dmg_out["gun"] / a.st.outgoing_mult

    def test_shred_scaled(self):
        m = dataclasses.replace(Mechanics(), shred_uptime=0.5)
        self.assertAlmostEqual(self.hit(m, 0.0), 70.0, places=4)
        self.assertAlmostEqual(self.hit(m, 0.2), 80.0, places=4)          # 0.3 resist - 0.5 x 0.2 shred
        full = dataclasses.replace(Mechanics(), shred_uptime=1.0)
        self.assertAlmostEqual(self.hit(full, 0.2), 90.0, places=4)
        self.assertAlmostEqual(self.hit(None, 0.2), 90.0, places=4)       # no mechanics: as before

    def test_absorbed_booking(self):
        for unbook, want in ((False, 70.0), (True, 30.0)):
            e = Engine(mech=dataclasses.replace(Mechanics(), unbook_absorbed=unbook))
            a, b = pair(e)
            b.add_barrier(40.0, 10.0)
            e.damage(a, b, 100, "bullet", "gun")
            self.assertAlmostEqual(a.dmg_out["gun"] / a.st.outgoing_mult, want, places=4)
            self.assertAlmostEqual(sum(b.dmg_in.values()) / a.st.outgoing_mult, 70.0, places=4)


if __name__ == "__main__":
    unittest.main()
