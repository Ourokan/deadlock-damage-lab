"""Viscous' ability hits and the items riding them (2026-10-28, validation/README.md "Viscous: procs per hit"):
Splatter's landing factor above 1 also multiplies the Mystic Burst / Tankbuster charge its hit releases
(items_fx.LANDING_PROCS), Goo Ball hits each target 1.47 times per cast as in replays (viscous.REAL_HITS), and the
opt-in Mechanics.charge_gaps draws a charged ability's next cast from real gaps.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import random
import sys
import types
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim import items_fx, mechanics  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.heroes import viscous  # noqa: E402


def release(cls, landing):
    """Mystic Burst damage released by one full-charge spirit hit of ability cls at this landing factor."""
    e = Engine()
    a = make_fighter(e, Loadout("Viscous", ["Mystic Burst"], souls=9000))
    b = make_fighter(e, Loadout("Abrams", [], souls=9000))
    a.enemy, b.enemy = b, a
    fx = next(x for x in a.items_fx if x.item.name == "Mystic Burst")
    got = []
    e.damage = lambda src, dst, raw, kind, source, **kw: got.append(raw) or raw
    ab = types.SimpleNamespace(ab=types.SimpleNamespace(class_name=cls), impl=None)
    hit = types.SimpleNamespace(is_ability=True, is_dot=False, kind="spirit", ability=ab, landing=landing,
                                amount=200.0 * landing, pre_mit=200.0)
    fx.on_damage_dealt(a, b, hit)
    return sum(got)


class LandingProcs(unittest.TestCase):
    def test_splatter_release_follows_landing_above_one(self):
        full = release("viscous_goo_grenade", 1.0)
        self.assertGreater(full, 0)
        self.assertAlmostEqual(release("viscous_goo_grenade", 1.5), 1.5 * full, delta=1e-6)
        self.assertAlmostEqual(release("viscous_goo_grenade", 0.5), full, delta=1e-6)   # below 1: a whole hit
        self.assertAlmostEqual(release("viscous_telepunch", 1.5), full, delta=1e-6)     # not in LANDING_PROCS


class GooBallHits(unittest.TestCase):
    def test_hits_per_target_match_replays(self):
        mean, p = 1.0, 1.0
        for x in viscous.REHIT_P:
            p *= x
            mean += p
        self.assertAlmostEqual(mean, 1.47, delta=0.03)


class ChargeGaps(unittest.TestCase):
    def test_punch_gap_drawn_from_replays(self):
        e = Engine(rng=random.Random(3))
        e.mech = mechanics.Mechanics(charge_gaps=True)
        a = make_fighter(e, Loadout("Viscous", [], souls=20000, tiers=[1, 1, 1, 1]))
        ab = next(x for x in a.abilities if x.ab.class_name == "viscous_telepunch")
        self.assertGreater(ab.max_charges(), 1)
        waits = [mechanics.recast_wait(ab) for _ in range(200)]
        self.assertTrue(all(w >= 0 for w in waits))
        # real gaps under 20 s: about half under 6 s (the sim's charge delay alone is 1.7 s)
        share = sum(w + ab.charge_delay() < 6 for w in waits) / len(waits)
        self.assertTrue(0.3 < share < 0.7, share)
        e.mech = mechanics.Mechanics(charge_gaps=False)
        self.assertEqual(mechanics.recast_wait(ab), 0.0)


if __name__ == "__main__":
    unittest.main()
