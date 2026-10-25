"""Fight entry health (2026-10-25): with Mechanics.fight_length and entry_hp (on by default), a fighter whose start
health wasn't set starts short by a deficit drawn from the real Phantom+ entry health spread (data/sustain.json), so
health-gated abilities meet their threshold as early as in real fights; Pain Battery starts charged by it, and a held
first Slam Fire opens whatever the clip.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim import abilities  # noqa: E402
from deadsim import mechanics as M  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def pair(hero, seed=1, mech=None):
    mech = mech or dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
    e = Engine(distance=10, mech=mech, rng=random.Random(seed))
    f = make_fighter(e, Loadout(hero, [], souls=27000))
    g = make_fighter(e, Loadout("Abrams", [], souls=27000))
    f.enemy, g.enemy = g, f
    return e, f, g


class EntryHealth(unittest.TestCase):
    def test_spread_matches_the_real_deficits(self):
        q = M.entry_deficits(27000)
        short = []
        for s in range(400):
            e, f, g = pair("Haze", s)
            M.entry_health(g)
            short.append(1 - g.hp / g.max_hp)
        self.assertAlmostEqual(sum(short) / len(short), sum(q) / len(q), delta=0.02)
        self.assertGreater(sum(d == 0 for d in short), 0.3 * len(short))   # many fights start full

    def test_set_start_and_deterministic_fights_stay(self):
        e, f, g = pair("Haze")
        g.entry_set = True
        M.entry_health(g)
        self.assertEqual(g.hp, g.max_hp)
        e = Engine(distance=10, mech=dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000)))
        h = make_fighter(e, Loadout("Haze", [], souls=27000))
        M.entry_health(h)
        self.assertEqual(h.hp, h.max_hp)   # no rng, no phase: full

    def test_pain_battery_starts_charged_by_missing_health(self):
        e, f, g = pair("Victor")
        pb = next(a for a in f.abilities if a.ab.name == "Pain Battery")
        f.hp = 0.5 * f.max_hp
        pb.start()
        self.assertGreater(pb.ctx.state["stored"], 0.4 * f.max_hp)
        self.assertTrue(pb.impl.full(pb.ctx))


class SlamFireOpener(unittest.TestCase):
    def test_held_first_cast_opens_with_a_full_clip(self):
        e, f, g = pair("Silver")
        for ab in f.abilities:
            ab.start()
        sf = next(a for a in f.abilities if a.ab.name == "Slam Fire")
        self.assertFalse(sf.impl.base_ok(sf.ctx))   # full clip: the gate holds
        sf.timed = True
        self.assertTrue(sf.impl.base_ok(sf.ctx))
        sf.casts = 1
        self.assertFalse(sf.impl.base_ok(sf.ctx))   # later casts wait for the last shell

    def test_probe_acts_as_held(self):
        e, f, g = pair("Silver")
        sf = next(a for a in f.abilities if a.ab.name == "Slam Fire")
        abilities.PROBE_HELD = True
        try:
            self.assertTrue(sf.held_opener())
        finally:
            abilities.PROBE_HELD = False
        self.assertFalse(sf.held_opener())


if __name__ == "__main__":
    unittest.main()
