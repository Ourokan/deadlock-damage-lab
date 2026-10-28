"""CC lands like the ability (deadsim Mechanics.cc_landing): an ability's stun / silence / disarm / immobilize lasts x
the ability's landing (skillshot spirit accuracy x landing factor x reach wait, at most 1); off, it lands in full.
Run from sim/: python3 -m unittest discover -s tests"""
import dataclasses
import os
import random
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, duel, mechanics  # noqa: E402
from deadsim.engine import Mods  # noqa: E402


def cc_given(flag, hero="Warden", mech=None):
    """Seconds of CC hero's abilities put on the foe in one 20 s duel (before status resist, which the foe lacks)."""
    seen = []
    add = Mods.add

    def spy(self, key, value, duration, tag=None):
        if key in ("stun", "silence", "disarm", "immobilize") and isinstance(tag, tuple) and str(tag[0]).startswith("ability_"):
            seen.append(duration)
        return add(self, key, value, duration, tag)
    mech = mech or dataclasses.replace(mechanics.DEFAULT, cc_landing=flag)
    with mock.patch.object(Mods, "add", spy):
        duel(Loadout(hero, [], souls=20000), Loadout("Abrams", [], souls=20000), max_time=20.0,
             rng=random.Random(1), mechanics=mech)
    return seen


class CCLanding(unittest.TestCase):
    def test_cc_shorter_when_on(self):
        off, on = cc_given(False), cc_given(True)
        self.assertTrue(off)
        self.assertTrue(on)
        self.assertLess(max(on), max(off) + 1e-9)
        self.assertLess(sum(on) / len(on), sum(off) / len(off))

    def test_off_is_the_default_and_unchanged(self):
        # the default (off) leaves every CC duration as it was before the flag existed
        self.assertFalse(mechanics.DEFAULT.cc_landing)
        self.assertEqual(cc_given(False), cc_given(None, mech=mechanics.DEFAULT))


if __name__ == "__main__":
    unittest.main()
