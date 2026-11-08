import os
import random
import sys
import unittest
from types import SimpleNamespace as NS

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from deadsim.items_fx import random_start  # noqa: E402
from deadsim.mechanics import Mechanics  # noqa: E402


class FakeFx:
    def __init__(self):
        self.ready_at, self.now, self.item = 0.0, 0.0, NS(name="Spirit Shielding")

    def cd(self):
        return 40.0


def fighter(p, rng=None, phase=None):
    return NS(e=NS(mech=Mechanics(barrier_start_random=p), rng=rng), skill=NS(fight_phase=phase), name="A")


class BarrierStart(unittest.TestCase):
    def test_off(self):
        fx = FakeFx()
        random_start(fx, fighter(0.0, random.Random(1)))
        self.assertEqual(fx.ready_at, 0.0)

    def test_always_spent(self):
        for s in range(20):
            fx = FakeFx()
            random_start(fx, fighter(1.0, random.Random(s)))
            self.assertTrue(0.0 <= fx.ready_at < 40.0)

    def test_share_spent(self):
        rng, spent = random.Random(3), 0
        for _ in range(4000):
            fx = FakeFx()
            random_start(fx, fighter(0.5, rng))
            spent += fx.ready_at > 0
        self.assertAlmostEqual(spent / 4000, 0.5, delta=0.03)

    def test_deterministic(self):
        fx = FakeFx()
        random_start(fx, fighter(0.5))             # no rng, no phase: ready as before
        self.assertEqual(fx.ready_at, 0.0)
        spent = 0
        for i in range(200):                       # no rng, phase pool: spent in about half the fights
            fx = FakeFx()
            random_start(fx, fighter(0.5, phase=(i + 0.5) / 200))
            spent += fx.ready_at > 0
        self.assertAlmostEqual(spent / 200, 0.5, delta=0.02)


class AllyCast(unittest.TestCase):
    def run_duel(self, share):
        import dataclasses
        from deadsim.engine import Engine
        from deadsim.items_fx import DivineBarrier
        from deadsim.data import game
        sys.path.insert(0, os.path.dirname(__file__))
        from test_shred_uptime import pair
        e = Engine(mech=dataclasses.replace(Mechanics(), barrier_ally_cast={"Divine Barrier": share}))
        e.rng = random.Random(0)
        a, b = pair(e)
        it = next(i for i in game().items.values() if i.name == "Divine Barrier")
        fx = DivineBarrier(it, b)
        b.hp = b.max_hp * 0.5
        self.assertTrue(fx.try_active(b))
        return b.barrier_total(), fx.ready_at

    def test_ally_cast(self):
        bar, ready = self.run_duel(0.0)
        self.assertGreater(bar, 0)
        bar, ready = self.run_duel(1.0)        # always on a teammate: cooldown spent, no barrier here
        self.assertEqual(bar, 0.0)
        self.assertGreater(ready, 0)


if __name__ == "__main__":
    unittest.main()
