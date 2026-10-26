"""Execute gates on real entry health and Djinn's Mark timing (2026-10-26).

- Mechanics.entry_gate (on): in fights booked over real lengths, a fighter facing an execute (Killing Blow,
  Assassinate, Close The Deal, Lethal Venom) gets a real entry deficit draw that only those gates see
  (Fighter.gate_hp); its health and the fight's length stay.
- Djinn's Mark: after each mark, a real chance (data/djinn_gaps.json) that Mirage lands no mark until they expire;
  a first cast held to real cast timing pops the marks there are.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim import mechanics as M  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.heroes import mirage  # noqa: E402


def pair(hero, enemy="Abrams", seed=1, mech=None, rng=True):
    mech = mech or dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
    e = Engine(distance=10, mech=mech, rng=random.Random(seed) if rng else None)
    f = make_fighter(e, Loadout(hero, [], souls=27000))
    g = make_fighter(e, Loadout(enemy, [], souls=27000))
    f.enemy, g.enemy = g, f
    return e, f, g


class EntryGate(unittest.TestCase):
    def test_on_by_default_and_not_with_entry_hp(self):
        self.assertTrue(M.DEFAULT.entry_gate)
        self.assertFalse(M.DEFAULT.entry_hp)

    def test_drawn_only_against_an_execute(self):
        gaps = []
        for s in range(300):
            e, f, g = pair("Shiv", seed=s)
            M.entry_gate(g)
            M.entry_gate(f)
            self.assertEqual(f.entry_gap, 0.0)   # Abrams has no execute: Shiv's health is seen as it is
            self.assertEqual(g.hp, g.max_hp)     # health stays
            gaps.append(g.entry_gap)
        q = M.entry_deficits(27000)
        self.assertAlmostEqual(sum(gaps) / len(gaps), sum(q) / len(q), delta=0.02)
        self.assertGreater(sum(x == 0 for x in gaps), 0.3 * len(gaps))   # many fights start full

    def test_set_start_and_deterministic_fights_stay(self):
        e, f, g = pair("Shiv")
        g.entry_set = True
        M.entry_gate(g)
        self.assertEqual(g.entry_gap, 0.0)
        e, f, g = pair("Shiv", rng=False)
        M.entry_gate(g)
        self.assertEqual(g.entry_gap, 0.0)   # no rng, no phase

    def test_gates_see_the_gap(self):
        e, f, g = pair("Shiv")
        for ab in f.abilities:
            ab.start()
        kb = next(a for a in f.abilities if a.ab.name == "Killing Blow")
        thr = kb.ctx.raw("EnemyHealthPercent") / 100
        g.hp = (thr + 0.1) * g.max_hp
        self.assertFalse(kb.impl.should_cast(kb.ctx))
        g.entry_gap = 0.2
        self.assertAlmostEqual(g.gate_frac, thr - 0.1)
        self.assertTrue(kb.impl.should_cast(kb.ctx))

    def test_engine_run_draws_it(self):
        e, f, g = pair("Shiv", seed=5)
        seen = []
        g.items_fx.append(type("Probe", (), {"on_start": lambda self, x: seen.append(x.entry_gap)})())
        e.run(f, g)
        gaps = [seen[0]]
        for s in range(6, 30):
            e, f, g = pair("Shiv", seed=s)
            seen = []
            g.items_fx.append(type("Probe", (), {"on_start": lambda self, x: seen.append(x.entry_gap)})())
            e.run(f, g)
            gaps.append(seen[0])
        self.assertTrue(any(x > 0.05 for x in gaps))


class DjinnsMark(unittest.TestCase):
    def setup(self, rng=True):
        e, f, g = pair("Mirage", rng=rng)
        for ab in f.abilities:
            ab.start()
        dm = next(a for a in f.abilities if a.ab.class_name == "mirage_sand_phantom")
        return e, f, g, dm

    def test_gap_chance_reads_the_data(self):
        self.assertGreater(mirage.gap_chance(5.0), mirage.gap_chance(8.0))
        self.assertTrue(0.2 < mirage.gap_chance(5.0) < 0.8)
        self.assertAlmostEqual(mirage.gap_chance(5.5), (mirage.gap_chance(5.0) + mirage.gap_chance(6.0)) / 2)

    def test_gaps_block_marks_until_expiry(self):
        blocked = 0
        for s in range(60):
            e, f, g = pair("Mirage", seed=s)
            for ab in f.abilities:
                ab.start()
            dm = next(a for a in f.abilities if a.ab.class_name == "mirage_sand_phantom")
            hit = type("Hit", (), {"kind": "bullet", "source": "gun", "hits": 1.0})()
            dm.impl.on_damage_dealt(dm.ctx, g, hit)
            self.assertEqual(dm.ctx.state["stacks"], 1)
            if dm.ctx.state["gap_until"] > 0:
                self.assertEqual(dm.ctx.state["gap_until"], dm.ctx.state["expire"])
                blocked += 1
        d = dm.ctx.dur("VictimStackDuration")
        self.assertAlmostEqual(blocked / 60, mirage.gap_chance(d), delta=0.2)

    def test_deterministic_fights_keep_marking(self):
        e, f, g, dm = self.setup(rng=False)
        hit = type("Hit", (), {"kind": "bullet", "source": "gun", "hits": 1.0})()
        dm.impl.on_damage_dealt(dm.ctx, g, hit)
        self.assertEqual(dm.ctx.state["gap_until"], -1.0)

    def test_held_first_cast_pops_what_there_is(self):
        e, f, g, dm = self.setup()
        dm.ctx.state["stacks"] = 1
        self.assertFalse(dm.impl.should_cast(dm.ctx))   # waits for max marks
        dm.timed = True
        self.assertTrue(dm.impl.should_cast(dm.ctx))
        dm.ctx.state["stacks"] = 0
        self.assertFalse(dm.impl.should_cast(dm.ctx))   # nothing to pop


if __name__ == "__main__":
    unittest.main()
