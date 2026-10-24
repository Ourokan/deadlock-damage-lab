"""Kinetic Carbine procs Mystic Shot like a gun hit (replays: 73% of Paradox's Mystic Shot procs on heroes land with
a Kinetic Carbine hit). Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.engine import Hit  # noqa: E402
from deadsim.mechanics import Mechanics  # noqa: E402


class ParadoxMysticShot(unittest.TestCase):
    def test_weapon_proc_hit_flag(self):
        self.assertFalse(Hit("spirit", "x", 0.0, 0.0).weapon_proc)

    def test_carbine_procs_mystic_shot_without_gun_hits(self):
        """A Paradox who never lands a bullet (accuracy 0) still procs Mystic Shot through Kinetic Carbine."""
        aim = Skill(accuracy=0.0, headshot=0.0, spirit_accuracy=1.0, use_abilities=True, use_actives=False)
        r = duel(Loadout("Paradox", ["Mystic Shot"], souls=20000, skill=aim),
                 Loadout("Haze", [], souls=20000, skill=Skill(accuracy=0.0, use_abilities=False)),
                 distance=10.0, max_time=30.0, mechanics=Mechanics(range_drift=False))
        self.assertGreater(r.a_dmg.get("Kinetic Carbine", 0), 0, dict(r.a_dmg))
        self.assertGreater(r.a_dmg.get("Mystic Shot", 0), 0, dict(r.a_dmg))


if __name__ == "__main__":
    unittest.main()
