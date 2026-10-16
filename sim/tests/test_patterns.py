"""Tests for deadsim.patterns (per-hero cast order, ult setup, prefight). Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill, duel  # noqa: E402
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

    def _warden(self):
        e = Engine(distance=10, max_time=1)
        f = make_fighter(e, Loadout("Warden", [], souls=30000, skill=Skill(accuracy=0.3)))
        g = make_fighter(e, Loadout("Abrams", [], souls=30000))
        f.enemy, g.enemy = g, f
        ult = next(s for s in f.abilities if s.ab.ultimate)
        setup = next(s for s in f.abilities if s.ab.class_name == "ability_warden_lock_down")
        for s in f.abilities:
            s.start()
        return e, f, g, ult, setup

    def test_ult_waits_for_setup(self):
        e, f, g, ult, setup = self._warden()
        self.assertTrue(patterns._castable(setup))
        self.assertFalse(f.plan.allows(ult))
        setup.casts = 1
        self.assertTrue(f.plan.allows(ult))
        setup.casts = 0
        e.t = patterns.SETUP_WAIT
        self.assertTrue(f.plan.allows(ult))

    def test_ult_does_not_wait_for_setup_on_cooldown(self):
        e, f, g, ult, setup = self._warden()
        for s in f.plan.after:          # every setup ability spent before this fight
            s.charges, s.ready_at = 0, 30.0
            self.assertFalse(patterns._castable(s))
        self.assertTrue(f.plan.allows(ult))

    def test_ult_does_not_wait_at_low_health(self):
        e, f, g, ult, setup = self._warden()
        g.hp = g.max_hp * 0.2
        self.assertTrue(f.plan.allows(ult))
        g.hp, f.hp = g.max_hp, f.max_hp * 0.2
        self.assertTrue(f.plan.allows(ult))


# default behaviour (patterns on), pinned so a change to deadsim.patterns or data/fight_patterns.json shows up:
# (hero, enemy, winner, time, damage dealt, damage taken) at 20k souls, accuracy 0.3, no items, mechanics default
PINNED = [
    ("Mo & Krill", "Haze", None, 30.0, 1663.8, 1568.9),
    ("Paradox", "Abrams", None, 30.0, 2490.7, 1404.7),
    ("Venator", "Lash", "Venator (A)", 21.548, 2088.4, 971.5),
    ("Warden", "Seven", "Seven (B)", 17.1, 734.1, 2623.5),
]


class TestPinnedWithPatterns(unittest.TestCase):
    def test_pinned_duels(self):
        for a, b, win, t, da, db in PINNED:
            r = duel(Loadout(a, [], souls=20000, skill=Skill(accuracy=0.3)),
                     Loadout(b, [], souls=20000, skill=Skill(accuracy=0.3)))
            got = (r.winner, round(r.time, 3), round(sum(r.a_dmg.values()), 1), round(sum(r.b_dmg.values()), 1))
            self.assertEqual(got, (win, t, da, db), a + " vs " + b)


if __name__ == "__main__":
    unittest.main()
