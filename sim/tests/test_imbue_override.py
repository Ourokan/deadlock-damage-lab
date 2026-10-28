"""Duration Extender goes on the ult for the heroes (Nurse, Graves) whose real holders gain there (fight.IMBUE_OVERRIDE), once the
ult is unlocked; before that the usual slot. Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, game  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import IMBUE_OVERRIDE, make_fighter  # noqa: E402


def fighter(hero, unlocked=None):
    return make_fighter(Engine(mech=None), Loadout(hero, ["Duration Extender"], souls=20000, unlocked=unlocked))


def imbued(f):
    return [s.ab.class_name for s in f.abilities if any(i.name == "Duration Extender" for i in s.imbues)]


class ImbueOverride(unittest.TestCase):
    def test_nurse_ult_takes_duration_extender(self):
        f = fighter("Nurse Harrow")
        self.assertEqual(imbued(f), ["ability_nurse_fear"])
        ult = next(s for s in f.abilities if s.ab.ultimate)
        bonus = game().item("Duration Extender").p("BonusAbilityDurationPercent") / 100
        self.assertAlmostEqual(ult.duration_pct(), f.st.duration_pct + bonus)

    def test_every_override_names_a_real_ability(self):
        G = game()
        for (hero, item), ab in IMBUE_OVERRIDE.items():
            h = next(x for x in G.heroes.values() if x.class_name == hero)
            self.assertIn(ab, [a.class_name for a in h.abilities], (hero, item))
            self.assertTrue(any(i.class_name == item for i in G.items.values()), item)

    def test_locked_ult_keeps_usual_slot(self):
        out = imbued(fighter("Nurse Harrow", unlocked=[True, True, True, False]))
        self.assertTrue(out)
        self.assertNotEqual(out, ["ability_nurse_fear"])


if __name__ == "__main__":
    unittest.main()
