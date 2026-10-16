"""Tests for deadsim.patterns (per-hero cast order, ult setup, prefight). Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter, time_to_kill  # noqa: E402
from deadsim import patterns  # noqa: E402


def casts(log):
    return [(float(l.split()[0]), l.split(" casts ")[1]) for l in log if " casts " in l]


class TestPatterns(unittest.TestCase):
    def test_every_hero_has_a_valid_row(self):
        from deadsim.data import game
        G = game()
        for hid in G.heroes:
            row = patterns.pattern(hid)
            self.assertIsNotNone(row, G.hero(hid).name)
            names = {a.class_name for a in G.hero(hid).abilities}
            for c in row["order"] + row["ult_after"] + ([row["prefight"]] if row["prefight"] else []):
                self.assertIn(c, names, G.hero(hid).name)

    def test_krill_opens_burrowed(self):
        """Mo emerges on the target at t=0: spin damage starts at once and Burrow is on cooldown."""
        a = Loadout("Mo & Krill", [], souls=15000, skill=Skill(accuracy=0.3))
        r = time_to_kill(a, Loadout("Abrams", [], souls=15000), max_time=3.0, log=True)
        cs = casts(r.log)
        self.assertEqual(cs[0], (0.0, "Burrow"))
        self.assertGreater(r.a_dmg.get("Burrow", 0), 0)
        off = Loadout("Mo & Krill", [], souls=15000, skill=Skill(accuracy=0.3, fight_pattern=False))
        r_off = time_to_kill(off, Loadout("Abrams", [], souls=15000), max_time=3.0)
        self.assertGreater(r.a_dmg.get("Burrow", 0), r_off.a_dmg.get("Burrow", 0))

    def test_prefight_cooldown_counts_from_before_the_fight(self):
        e = Engine(distance=10, max_time=5)
        f = make_fighter(e, Loadout("Mo & Krill", [], souls=15000, skill=Skill(accuracy=0.3)))
        g = make_fighter(e, Loadout("Abrams", [], souls=15000))
        e.run(f, g, one_way=True)
        burrow = next(s for s in f.abilities if s.ab.class_name == "ability_burrow")
        self.assertAlmostEqual(burrow.ready_at, burrow.cooldown() - burrow.impl.prefight_lead(burrow.ctx), places=6)

    def test_off_keeps_slot_order(self):
        e = Engine(distance=10, max_time=1)
        f = make_fighter(e, Loadout("Mo & Krill", [], souls=15000, skill=Skill(fight_pattern=False)))
        self.assertIsNone(f.plan)
        self.assertIsNone(f.cast_order)

    def test_ult_waits_for_setup(self):
        e = Engine(distance=10, max_time=1)
        f = make_fighter(e, Loadout("Warden", [], souls=30000, skill=Skill(accuracy=0.3)))
        ult = next(s for s in f.abilities if s.ab.ultimate)
        setup = next(s for s in f.abilities if s.ab.class_name == "ability_warden_lock_down")
        self.assertFalse(f.plan.allows(ult))
        setup.casts = 1
        self.assertTrue(f.plan.allows(ult))
        setup.casts = 0
        e.t = patterns.SETUP_WAIT
        self.assertTrue(f.plan.allows(ult))


if __name__ == "__main__":
    unittest.main()
