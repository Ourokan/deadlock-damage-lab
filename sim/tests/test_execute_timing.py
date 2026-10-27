"""Killing Blow and Soul Exchange on real fight timing (2026-10-26).

- Mechanics.execute_timing (on): Killing Blow's first cast in a fight is drawn from the real outcomes
  (data/execute_timing.json): spent at a real time without an execute, wait for the execute gate, or not cast; Soul
  Exchange's first cast is held to a real first cast time (or not cast), then its gap gate.
- Mechanics.swap_full (on, 2026-10-28): the swap lands whole (no landing factor) on ghost.SWAP_LAND of casts.
- Mechanics.gate_assist (on): Soul Exchange's Geist sees her health short by a real entry deficit and by the real
  third parties' damage per damage she takes (Fighter.self_gate_frac); her health stays.
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


def pair(hero, enemy="Abrams", seed=1, rng=True):
    mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
    e = Engine(distance=5, mech=mech, rng=random.Random(seed) if rng else None)
    f = make_fighter(e, Loadout(hero, [], souls=27000))
    g = make_fighter(e, Loadout(enemy, [], souls=27000))
    f.enemy, g.enemy = g, f
    for x in (f, g):
        for ab in x.abilities:
            ab.start()
    return e, f, g


def ability(f, name):
    return next(a for a in f.abilities if a.ab.name == name)


class Defaults(unittest.TestCase):
    def test_on_by_default(self):
        self.assertTrue(M.DEFAULT.execute_timing)
        self.assertTrue(M.DEFAULT.gate_assist)

    def test_data_rows(self):
        for row in ("all", "even", "odd"):
            M.EXEC_ROW = row
            try:
                d = M.execute_timing_data()
            finally:
                M.EXEC_ROW = "all"
            kb, se = d["killing_blow"], d["soul_exchange"]
            self.assertEqual(len(kb["commit_holds"]), len(se["holds"]))
            self.assertTrue(0 < kb["exec_share"] < 1)
            self.assertTrue(1.0 < d["assist"]["ability_health_swap"] < 1.4)


class KillingBlowPlan(unittest.TestCase):
    def test_draws(self):
        q = M.execute_timing_data()["killing_blow"]
        n = sum(x is not None for x in q["commit_holds"])
        e, f, g = pair("Shiv")
        kb = ability(f, "Killing Blow")
        kb.impl.draw_plan(kb.ctx, 0.0)                      # spent at a real time
        self.assertAlmostEqual(kb.ctx.state["commit_at"], q["commit_holds"][0])
        e, f, g = pair("Shiv")
        kb = ability(f, "Killing Blow")
        kb.impl.draw_plan(kb.ctx, n / len(q["commit_holds"]) + q["exec_share"] / 2)   # waits for the execute
        self.assertNotIn("commit_at", kb.ctx.state)
        self.assertEqual(kb.held_until, 0.0)
        kb.impl.draw_plan(kb.ctx, 0.999)                    # on cooldown
        self.assertEqual(kb.held_until, math.inf)

    def test_spent_cast_is_the_slash_not_an_execute(self):
        e, f, g = pair("Shiv")
        kb = ability(f, "Killing Blow")
        self.assertFalse(kb.impl.should_cast(kb.ctx))        # full health, no commit
        kb.ctx.state["commit_at"] = 0.0
        self.assertTrue(kb.impl.should_cast(kb.ctx))
        hp = g.hp
        kb.cast()
        for _, _, fn, args in list(e.q):   # the slash lands (the cast's delayed hit)
            if getattr(fn, "__name__", "") == "go":
                fn(*args)
        self.assertTrue(g.alive)
        self.assertLess(g.hp, hp)
        self.assertNotIn("commit_at", kb.ctx.state)          # a recast waits for the execute
        self.assertFalse(kb.impl.should_cast(kb.ctx))

    def test_engine_run_draws_plans(self):
        seen = set()
        for s in range(40):
            e, f, g = pair("Shiv", seed=s)
            e.run(f, g)
            kb = ability(f, "Killing Blow")
            seen.add(kb.ctx.state["plan"])
        self.assertEqual(seen, {"spent", "none", "exec"})

    def test_deterministic_fights_keep_the_gate(self):
        e, f, g = pair("Shiv", rng=False)
        e.run(f, g)
        kb = ability(f, "Killing Blow")
        self.assertNotIn("plan", kb.ctx.state)
        self.assertNotEqual(kb.held_until, math.inf)


class SoulExchange(unittest.TestCase):
    def test_gate_assist_only_for_geist(self):
        e, f, g = pair("Lady Geist")
        M.gate_assist(f)
        M.gate_assist(g)
        self.assertGreater(f.gate_assist, 1.0)
        self.assertEqual(g.gate_assist, 0.0)
        self.assertEqual(f.hp, f.max_hp)                     # health stays
        f.entry_gap = 0.0
        f.dmg_in["gun"] = 0.1 * f.max_hp
        f.hp -= 0.1 * f.max_hp
        self.assertAlmostEqual(f.self_gate_frac, 0.9 - 0.1 * f.gate_assist)
        self.assertAlmostEqual(f.gate_frac, 0.9)            # execute gates on Geist don't see the assist

    def test_killing_blow_on_geist_ignores_her_assist(self):
        e, f, g = pair("Shiv", enemy="Lady Geist")
        M.gate_assist(g)
        g.entry_gap = 0.0
        kb = ability(f, "Killing Blow")
        thr = kb.ctx.raw("EnemyHealthPercent") / 100
        g.hp = (thr + 0.05) * g.max_hp
        g.dmg_in["gun"] = 0.9 * g.max_hp
        self.assertLess(g.self_gate_frac, thr)
        self.assertFalse(kb.impl.executes(kb.ctx))

    def test_swap_on_gate_health(self):
        e, f, g = pair("Lady Geist", rng=False)   # no rng: the swap's SWAP_LAND draw lands the first cast
        se = ability(f, "Soul Exchange")
        f.gate_assist, f.entry_gap = 0.0, 0.6
        self.assertTrue(se.impl.should_cast(se.ctx))         # actual health full, gate health 40%
        before = g.hp
        se.impl.swap(se.ctx)
        self.assertAlmostEqual(g.hp, max(0.4, se.ctx.raw("EnemyMinHealthPct") / 100) * g.max_hp, delta=1.0)
        self.assertLess(g.hp, before)

    def test_swap_whole_past_landing_factor(self):
        # Mechanics.swap_full: the swap skips Soul Exchange's landing factor (it is no hit that lands part of the
        # time); off, the factor shrinks it as before
        for whole in (True, False):
            e, f, g = pair("Lady Geist", rng=False)
            e.mech = dataclasses.replace(e.mech, swap_full=whole)
            f.skill = dataclasses.replace(f.skill, ability_landing={"Soul Exchange": 0.5})
            se = ability(f, "Soul Exchange")
            f.gate_assist, f.entry_gap = 0.0, 0.6
            before = g.hp
            floor = max(0.4, se.ctx.raw("EnemyMinHealthPct") / 100) * g.max_hp
            se.impl.swap(se.ctx)
            self.assertAlmostEqual(before - g.hp, (before - floor) * (1.0 if whole else 0.5), delta=1.0)

    def test_hold_draw(self):
        q = M.execute_timing_data()["soul_exchange"]["holds"]
        e, f, g = pair("Lady Geist")
        se = ability(f, "Soul Exchange")
        se.impl.draw_plan(se.ctx, 0.0)
        self.assertAlmostEqual(se.held_until, q[0])
        se.impl.draw_plan(se.ctx, 0.999)
        self.assertEqual(se.held_until, math.inf if q[-1] is None else q[-1])


if __name__ == "__main__":
    unittest.main()
