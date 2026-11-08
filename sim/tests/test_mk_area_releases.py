"""Mo & Krill (2026-11-08, scripts/mechanics/mk_area_releases.py): Mystic Burst releases on every hero a Scorn hit
lands on, so the duel's one release per cast stands for the ability's real heroes per cast (items_fx.AREA_RELEASES).
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, duel  # noqa: E402
from deadsim import items_fx  # noqa: E402


def burst(on):
    old = items_fx.AREA_RELEASES_ON
    items_fx.AREA_RELEASES_ON = on
    try:
        r = duel(Loadout("Mo & Krill", ["Mystic Burst", "Extra Spirit"], souls=15000),
                 Loadout("Abrams", ["Extra Health"], souls=15000))
        return r.a_dmg.get("Mystic Burst", 0.0)
    finally:
        items_fx.AREA_RELEASES_ON = old


class AreaReleases(unittest.TestCase):
    def test_scorn_releases_scale_with_heroes_per_cast(self):
        off, on = burst(False), burst(True)
        self.assertGreater(off, 0.0)
        self.assertGreater(on, off)


if __name__ == "__main__":
    unittest.main()
