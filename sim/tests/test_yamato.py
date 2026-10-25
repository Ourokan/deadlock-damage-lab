"""Yamato's Shadow Transformation hold (2026-10-25): cast once all the other unlocked abilities are on cooldown.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill, duel  # noqa: E402

DUMMY = Skill(accuracy=0.0, use_abilities=False, use_actives=False, melee_rate=0.0)


def first_shadow(unlocked):
    a = Loadout("Yamato", [], souls=20000, skill=Skill(accuracy=0.3, use_actives=False), unlocked=unlocked)
    r = duel(a, Loadout("Abrams", [], souls=20000, skill=DUMMY), distance=5.0, max_time=20.0, mechanics=None, log=True)
    casts = [float(x.split()[0]) for x in r.log if "casts Shadow Transformation" in x]
    others = {x.split("casts ")[1] for x in r.log if "casts " in x and "Yamato" in x.split("casts")[0]}
    return (casts[0] if casts else None), others


class ShadowTransformationHold(unittest.TestCase):
    def test_waits_for_the_other_three(self):
        t, others = first_shadow(None)
        self.assertIsNotNone(t)
        self.assertTrue({"Power Slash", "Flying Slash", "Crimson Slash"} <= others, others)

    def test_fewer_abilities_unlocked_still_casts(self):
        # only Crimson Slash and the ult unlocked: waiting for three on cooldown would hold it forever
        t, _ = first_shadow([False, False, True, True])
        self.assertIsNotNone(t)

    def test_casts_by_the_time_fallback(self):
        # the cooldown condition switched off (need 0) and a target that never hurts Yamato: only the time is left
        from deadsim.heroes import yamato
        a = Loadout("Yamato", [], souls=20000, skill=Skill(accuracy=0.3, use_actives=False))
        b = Loadout("Abrams", [], souls=20000, skill=DUMMY)
        old = yamato.ST_ON_CD
        yamato.ST_ON_CD = 0
        try:
            r = duel(a, b, distance=5.0, max_time=20.0, mechanics=None, log=True)
        finally:
            yamato.ST_ON_CD = old
        casts = [float(x.split()[0]) for x in r.log if "casts Shadow Transformation" in x]
        self.assertTrue(casts)
        self.assertGreaterEqual(casts[0], yamato.ST_WAIT - 0.01)
        self.assertLessEqual(casts[0], yamato.ST_WAIT + 2.5)   # (after a slash or channel in progress)


if __name__ == "__main__":
    unittest.main()
