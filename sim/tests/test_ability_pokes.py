"""Ability pokes beside the duel (Mechanics.pokes, fight.add_pokes, data/ability_pokes.json): Paradox's full-charge
Kinetic Carbine pokes add damage and their item procs, and leave the fight itself alone. Run: python3 -m unittest
discover -s tests -v (from sim/)."""
import dataclasses
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.data import game  # noqa: E402
from deadsim.heroes import chrono  # noqa: E402
from deadsim.mechanics import DEFAULT, poke_rows, real_length  # noqa: E402


def fight(pokes):
    mech = dataclasses.replace(DEFAULT, fight_length=real_length(20000), pokes=pokes, range_drift=False)
    aim = Skill(accuracy=0.4, headshot=0.1, spirit_accuracy=1.0, use_abilities=True, use_actives=False)
    return duel(Loadout("Paradox", ["Tankbuster", "Mystic Shot"], souls=20000, skill=aim),
                Loadout("Haze", [], souls=20000, skill=Skill(accuracy=0.3, use_abilities=False)),
                distance=15.0, max_time=20.0, rng=random.Random(3), mechanics=mech)


class AbilityPokes(unittest.TestCase):
    def test_rows(self):
        rows = poke_rows(game().hero("Paradox"))
        self.assertIn("citadel_ability_chrono_kinetic_carbine", rows)
        self.assertGreater(rows["citadel_ability_chrono_kinetic_carbine"], 0.2)
        self.assertEqual(poke_rows(game().hero("Haze")), {})

    def test_pokes_add_damage_not_fight(self):
        off, on = fight(False), fight(True)
        # the duel is the same fight, only the Carbine is the smaller in-fight hit
        self.assertEqual(off.winner, on.winner)
        # the pokes' full hits and their procs come on top
        k = poke_rows(game().hero("Paradox"))["citadel_ability_chrono_kinetic_carbine"]
        carb_off, carb_on = off.a_exp.get("Kinetic Carbine", 0), on.a_exp.get("Kinetic Carbine", 0)
        self.assertGreater(carb_on, carb_off * chrono.CARBINE_FIGHT_HIT, (carb_off, carb_on))
        self.assertGreater(on.a_dmg.get("Tankbuster", 0), off.a_dmg.get("Tankbuster", 0) * 0.9)
        self.assertGreater(k, 0)
        self.assertEqual(off.a_dmg.get("gun", 0) > 0, on.a_dmg.get("gun", 0) > 0)

    def test_no_pokes_without_fight_length(self):
        mech = dataclasses.replace(DEFAULT, fight_length=None, range_drift=False)
        aim = Skill(accuracy=0.4, spirit_accuracy=1.0, use_abilities=True, use_actives=False)
        a = Loadout("Paradox", [], souls=20000, skill=aim)
        b = Loadout("Haze", [], souls=20000, skill=Skill(accuracy=0.3, use_abilities=False))
        r1 = duel(a, b, distance=15.0, max_time=20.0, rng=random.Random(1), mechanics=mech)
        r2 = duel(a, b, distance=15.0, max_time=20.0, rng=random.Random(1),
                  mechanics=dataclasses.replace(mech, pokes=False))
        self.assertEqual(dict(r1.a_dmg), dict(r2.a_dmg))


if __name__ == "__main__":
    unittest.main()
