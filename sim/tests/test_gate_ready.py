"""Gated ults at the fight start (2026-10-27): with Mechanics.cast_timing and gate_ready, an ability in
mechanics.GATE_READY (Apollo's Itani Lo Sahn: no real hold, its own health gate) starts a fight on cooldown past its
real share of fights started ready (data/cdr_ready.json), so it is cast in real-like shares of fights.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import math
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim import mechanics as M  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402

KEY = "77:ability_fencer_ultimate"


def ult_held(seed, mech=M.DEFAULT):
    f = make_fighter(Engine(rng=random.Random(seed), mech=mech), Loadout("Apollo", [], souls=27000))
    ab = next(a for a in f.abilities if a.ab.ultimate)
    M.hold_first_casts(f)
    return ab.held_until == math.inf


class GateReady(unittest.TestCase):
    def test_apollo_ult_listed_without_hold(self):
        self.assertIn(KEY, M.GATE_READY)
        self.assertNotIn(KEY, M.cast_holds())   # its own gate times it once ready

    def test_off_cooldown_at_the_real_ready_share(self):
        ready = M.cdr_ready_rows()["sources"][KEY][-1]
        n = 2000
        held = sum(ult_held(s) for s in range(n)) / n
        self.assertAlmostEqual(held, 1.0 - ready, delta=0.04)

    def test_off_keeps_the_ult_ready(self):
        mech = dataclasses.replace(M.DEFAULT, gate_ready=False)
        self.assertFalse(any(ult_held(s, mech) for s in range(200)))


if __name__ == "__main__":
    unittest.main()
