"""Healing booked by source (2026-10-25, the site's item sheet): lifesteal is keyed by the damage it heals from,
heal_exp adds up to healed_exp, heal_raw keeps what the max health cap cut.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def pair(e, items):
    a = make_fighter(e, Loadout("Haze", items, souls=10000))
    b = make_fighter(e, Loadout("Abrams", [], souls=10000))
    a.enemy, b.enemy = b, a
    return a, b


class HealSources(unittest.TestCase):
    def test_lifesteal_keyed_by_damage_source(self):
        e = Engine()
        a, b = pair(e, ["Spirit Lifesteal"])
        a.hp = a.max_hp / 2
        e.damage(a, b, 200, "spirit", "Sleep Dagger", is_ability=True)
        self.assertGreater(a.heal_exp.get("spirit_lifesteal|Sleep Dagger", 0.0), 0.0)
        self.assertAlmostEqual(sum(a.heal_exp.values()), a.healed_exp, places=6)

    def test_raw_keeps_capped_healing(self):
        e = Engine()
        a, _ = pair(e, [])
        a.hp = a.max_hp - 10
        got = a.heal(50, "Headhunter", "heal")
        self.assertAlmostEqual(got, 10.0, places=6)
        self.assertAlmostEqual(a.heal_exp["Headhunter"], 10.0, places=6)
        self.assertGreaterEqual(a.heal_raw["Headhunter"], 50.0 - 1e-9)
        self.assertEqual(a.heal(5, "Headhunter", "heal"), 0.0)   # full: nothing lands, raw still grows
        self.assertAlmostEqual(a.heal_exp["Headhunter"], 10.0, places=6)


if __name__ == "__main__":
    unittest.main()
