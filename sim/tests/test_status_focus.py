"""Status resist under focus (deadsim Mechanics.status_focus): survive(focus=) makes the focused fighter's status
resist count x focus on every debuff duration, and leaves it alone with the flag off or at focus 1.
Run from sim/: python3 -m unittest discover -s tests"""
import dataclasses
import os
import sys
import unittest
from unittest import mock

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "survival")]

import survival  # noqa: E402
from deadsim import Loadout, mechanics  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def focus_seen(focus, flag=True):
    """status_focus of the survive() holder when the fight starts."""
    seen = []
    run = Engine.run

    def spy(e, me, foe):
        seen.append(me.status_focus)
        return run(e, me, foe)
    mech = dataclasses.replace(mechanics.DEFAULT, status_focus=flag)
    with mock.patch.object(Engine, "run", spy), mock.patch.object(mechanics, "DEFAULT", mech):
        survival.survive("Abrams", [], 9000, "Haze", [], max_time=2.0, focus=focus)
    return seen[0]


class StatusFocus(unittest.TestCase):
    def test_survive_sets_the_holders_status_focus(self):
        self.assertEqual(focus_seen(2.0), 2.0)
        self.assertEqual(focus_seen(1.0), 1.0)
        self.assertEqual(focus_seen(2.0, flag=False), 1.0)

    def test_debuff_duration_shortened_x_focus(self):
        e = Engine(distance=10)
        a = make_fighter(e, Loadout("Abrams", ["Debuff Reducer"], souls=27000))
        r = a.st.status_resist
        mechanics._debuff(a, "slow", 0.3, 4.0, "t1")
        a.status_focus = 2.0
        mechanics._debuff(a, "slow", 0.3, 4.0, "t2")
        self.assertAlmostEqual(a.mods.d["slow"]["t1"][1] - e.t, 4.0 * (1 - r))
        self.assertAlmostEqual(a.mods.d["slow"]["t2"][1] - e.t, 4.0 * (1 - 2 * r))


if __name__ == "__main__":
    unittest.main()
