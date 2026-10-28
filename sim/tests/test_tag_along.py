"""Rem's Tag Along (2026-10-28, Mechanics.tag_along): real Rems ride an ally for 5-14% of their combat time (replays),
with no gun, melee or Pillow Toss then and almost no damage taken. With fight draws the duel puts Rem on an ally for
windows whose share matches data/tag_along.json at his net worth.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, duel  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.mechanics import DEFAULT, Mechanics, _interp_ln, real_length, tag_along_windows  # noqa: E402
import deadsim.mechanics as M  # noqa: E402


def rem(souls, rng=None, mech=None):
    e = Engine(rng=rng, mech=mech or dataclasses.replace(Mechanics(), fight_length=real_length(souls)))
    f = make_fighter(e, Loadout("Rem", [], souls=souls))
    return f


class TagAlongWindows(unittest.TestCase):
    def test_share_matches_data(self):
        for souls in (2000, 30000):
            tot, horizon = 0.0, 60.0
            for i in range(400):
                f = rem(souls, rng=random.Random(i))
                tot += sum(min(horizon, t + n) - t for t, n in tag_along_windows(f, "x", horizon))
            M.tag_along_windows(f, "x")   # loads the table
            want = _interp_ln(M._TAG[0], souls)
            self.assertAlmostEqual(tot / 400 / horizon, want, delta=0.35 * want)

    def test_off_and_deterministic_fights_have_none(self):
        self.assertEqual(tag_along_windows(rem(20000), "x"), [])   # no rng, no phase
        off = dataclasses.replace(Mechanics(), tag_along=False, fight_length=real_length(20000))
        self.assertEqual(tag_along_windows(rem(20000, random.Random(1), off), "x"), [])

    def test_less_gun_when_on(self):
        gun = {}
        for on in (False, True):
            g = 0.0
            for i in range(150):
                mech = dataclasses.replace(DEFAULT, tag_along=on, fight_length=real_length(30000))
                r = duel(Loadout("Rem", [], souls=30000), Loadout("Haze", [], souls=30000), max_time=20,
                         rng=random.Random(i), mechanics=mech)
                g += r.a_exp.get("gun", 0.0) / max(1e-9, sum(r.a_exp.values()))
            gun[on] = g
        self.assertLess(gun[True], gun[False])


if __name__ == "__main__":
    unittest.main()
