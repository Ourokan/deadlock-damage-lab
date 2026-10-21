"""Range-only items (Mystic Expansion, Greater Expansion) must not decide whether an ability is used at all: players
walk a little closer instead. Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def rake_damage(items, distance=16.3):
    """Mina's Rake damage on an idle Abrams in 30 s at her median fight distance (Rake reaches 10 m)."""
    e = Engine(distance=distance, max_time=30)
    a = make_fighter(e, Loadout("Mina", items, souls=27000, skill=Skill(use_actives=False)), "a")
    d = make_fighter(e, Loadout("Abrams", [], souls=27000, skill=Skill(accuracy=0, use_abilities=False)), "d")
    d.abilities = []
    e.run(a, d, one_way=True)
    return a.dmg_out.get("Rake", 0.0)


class TestRangeItems(unittest.TestCase):
    def test_rake_cast_without_range_item(self):
        """16.3 m is past Rake's 10 m + 5 m engage margin: Mina walks in instead of never casting it."""
        self.assertGreater(rake_damage([]), 0.0)

    def test_range_item_adds_little_rake_damage(self):
        """Greater Expansion only shortens the walk in, so Rake damage barely moves (it used to unlock Rake)."""
        base, more = rake_damage([]), rake_damage(["Greater Expansion"])
        self.assertLess(abs(more - base), 0.15 * base)

    def test_out_of_walk_in_reach_not_cast(self):
        self.assertEqual(rake_damage([], distance=25.0), 0.0)

    def test_mina_imbues_mystic_expansion_on_retreat(self):
        e = Engine(distance=15, max_time=5)
        f = make_fighter(e, Loadout("Mina", ["Mystic Expansion"], souls=27000))
        held = {s.ab.class_name: [it.name for it in s.imbues] for s in f.abilities}
        self.assertEqual(held["ability_vampirebat_batblink"], ["Mystic Expansion"])


if __name__ == "__main__":
    unittest.main()
