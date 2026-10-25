"""Opener timing (2026-10-24): with Mechanics.fight_length and opener_timing, the hits of a source the sim casts on
sight are booked as if its first use came after the real hold (data/opener_timing.json); the fight itself and the
in-full damage are unchanged.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, duel, game  # noqa: E402
from deadsim import mechanics as M  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.accuracy import hero_default_skill  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


class OpenerHold(unittest.TestCase):
    def test_vyper_split_shot_has_a_real_hold(self):
        G = game()
        h = G.hero("Vyper")
        holds = M.opener_holds(h, [G.items_by_name["split shot"]])
        q = holds["Split Shot"]
        self.assertEqual(len(q), 20)
        self.assertTrue(all(a <= b for a, b in zip(q, q[1:])))
        self.assertTrue(0.5 < q[10] < 5.0, q)   # real median first use ~2 s after the sim's

    def test_weight_is_the_mean_over_holds(self):
        e = Engine(mech=dataclasses.replace(M.Mechanics(), fight_length=(1.0, 0.5, 0.0)))
        f = make_fighter(e, Loadout("Vyper", [], souls=5000))
        f.opener_hold = {"Grenade": (0.0, M.LENGTH_STEP)}
        self.assertAlmostEqual(e.length_w(0.0, src=f, source="Grenade"), 0.75)
        self.assertAlmostEqual(e.length_w(0.0, src=f, source="Grenade squares"), 0.75)   # sub-source
        self.assertAlmostEqual(e.length_w(0.0, src=f, source="gun"), 1.0)

    def test_only_with_fight_length_and_the_switch(self):
        lo = Loadout("Vyper", ["Split Shot"], souls=9000, skill=hero_default_skill("Vyper", badge=91, counterplay=True))
        self.assertEqual(make_fighter(Engine(mech=M.Mechanics()), lo).opener_hold, {})
        self.assertFalse(M.Mechanics().opener_timing)   # off by default
        mech = dataclasses.replace(M.Mechanics(), fight_length=M.real_length(9000), opener_timing=True)
        self.assertIn("Split Shot", make_fighter(Engine(mech=mech), lo).opener_hold)
        off = dataclasses.replace(mech, opener_timing=False)
        self.assertEqual(make_fighter(Engine(mech=off), lo).opener_hold, {})
        # a source without a length correction keeps full-length booking (its level would drop)
        bare = Loadout("Vyper", ["Split Shot"], souls=9000)
        self.assertEqual(make_fighter(Engine(mech=mech), bare).opener_hold, {})

    def test_books_openers_lower_and_leaves_the_fight(self):
        a = Loadout("Vyper", ["Split Shot", "Headshot Booster"], souls=9000, skill=hero_default_skill("Vyper", badge=91, counterplay=True))
        b = Loadout("Abrams", ["Extra Health"], souls=9000)
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(9000), opener_timing=True)
        on = duel(a, b, max_time=20, rng=random.Random(3), mechanics=mech)
        off = duel(a, b, max_time=20, rng=random.Random(3), mechanics=dataclasses.replace(mech, opener_timing=False))
        self.assertAlmostEqual(on.time, off.time)
        self.assertEqual({k: round(v, 6) for k, v in on.a_dmg.items()}, {k: round(v, 6) for k, v in off.a_dmg.items()})
        self.assertAlmostEqual(on.a_exp["gun"], off.a_exp["gun"])
        self.assertLess(on.a_exp["Split Shot"], off.a_exp["Split Shot"])


if __name__ == "__main__":
    unittest.main()
