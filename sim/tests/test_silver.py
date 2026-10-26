"""Silver's Lycan Curse on real timing (deadsim/heroes/werewolf.py, data/wolf_timing.json): each fight's first
transform is drawn (already in wolf form, at a real time, or not at all), later casts follow the rage rule. Wolf
abilities skip the human slot's first-cast hold; Tail Whack also hits others near the target. Run from sim/:
    python3 -m unittest discover -s tests
"""
import heapq
import math
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.heroes import werewolf  # noqa: E402
from deadsim.mechanics import DEFAULT as MECH, real_length  # noqa: E402

ULT = "ability_werewolf_transformation"


class SilverCase(unittest.TestCase):
    def setUp(self):
        self.e = Engine(distance=8, max_time=30)
        self.f = make_fighter(self.e, Loadout("Silver", [], souls=20000, skill=Skill(), unlocked=[True] * 4))
        self.g = make_fighter(self.e, Loadout("Abrams", [], souls=20000))
        self.f.enemy, self.g.enemy = self.g, self.f
        for s in self.f.abilities + self.g.abilities:
            s.start()
        self.ult = next(s for s in self.f.abilities if s.ab.class_name == ULT)

    def test_draw_plan_start_time_or_none(self):
        d = werewolf.wolf_timing()
        p0 = d["start_wolf"]
        c = self.ult.ctx
        self.ult.impl.draw_plan(c, p0 / 2)          # already in wolf form: on sight
        self.assertTrue(self.ult.impl.should_cast(c))
        self.ult.impl.draw_plan(c, 0.999)           # the last bin: not transformed by 20 s
        self.assertEqual(c.state["plan_at"], math.inf)
        self.assertFalse(self.ult.impl.should_cast(c))
        c.state["rage"] = 1e9                       # a full rage bar doesn't override the drawn plan
        self.assertFalse(self.ult.impl.should_cast(c))
        self.e.t += werewolf.PLAN_HORIZON           # past the data's horizon: the rage rule again
        self.assertTrue(self.ult.impl.should_cast(c))
        self.e.t = 0.0
        h = d["holds"][0]
        self.ult.impl.draw_plan(c, p0 + 1e-6)       # first real bin
        self.assertAlmostEqual(c.state["plan_at"], self.e.t + h)

    def test_cast_clears_plan_then_rage_rule(self):
        c = self.ult.ctx
        self.ult.impl.draw_plan(c, 0.0)
        self.ult.cast()
        self.assertNotIn("plan_at", c.state)
        self.e.t += 30.0
        self.f.counters[werewolf.WOLF_KEY] = -1.0
        c.state["rage"] = 0.0
        self.assertFalse(self.ult.impl.should_cast(c))
        c.state["rage"] = self.ult.impl.max_rage(c)
        self.assertTrue(self.ult.impl.should_cast(c))

    def test_some_duels_start_in_wolf_form(self):
        mech = MECH.__class__(**{**MECH.__dict__, "fight_length": real_length(20000)})
        starts = 0
        for k in range(60):
            r = duel(Loadout("Silver", [], souls=20000), Loadout("Abrams", [], souls=20000), distance=8,
                     max_time=20, rng=random.Random(k), mechanics=mech, log=True)
            first = next((ln for ln in r.log if "casts Lycan Curse" in ln), None)
            if first is not None and float(first.split()[0]) < 0.6:
                starts += 1
        self.assertGreater(starts, 0)
        self.assertLess(starts, 30)

    def test_wolf_ability_skips_human_hold(self):
        bola = next(s for s in self.f.abilities if s.ab.class_name == "ability_werewolf_netshot")
        bola.held_until = math.inf                  # the Bola's real first-cast hold
        self.assertFalse(bola.try_cast())
        self.ult.cast()                             # wolf form: Tail Whack is not held by it
        self.e.t += 0.5
        casts = bola.casts
        self.assertTrue(bola.try_cast())
        self.assertEqual(bola.casts, casts)         # nor counted as the Bola's first cast
        self.f.counters[werewolf.WOLF_KEY] = -1.0   # back in human form: the hold stands
        self.e.t += 30.0
        self.assertFalse(bola.try_cast())

    def test_tail_whack_hits_others(self):
        bola = next(s for s in self.f.abilities if s.ab.class_name == "ability_werewolf_netshot")
        self.ult.cast()
        self.e.t += 0.5
        self.assertTrue(bola.try_cast())
        end = self.e.t + 1.0
        while self.e.q and self.e.q[0][0] <= end:   # run the cast's delayed hit
            t, _, fn, args = heapq.heappop(self.e.q)
            self.e.t = t
            fn(*args)
        self.assertGreater(self.f.counters.get("splash", {}).get("Tail Whack", 0.0), 0.0)

    def test_wolf_ability_timing_opt_in(self):
        c = self.ult.ctx
        self.ult.impl.draw_plan(c, 0.5)
        self.ult.cast()                             # off (default): wolf abilities start ready
        wolves = [s for s in self.f.abilities if isinstance(s.impl, werewolf.WolfSlot)]
        self.assertTrue(all(s.scratch["wolf_ready"] == 0.0 for s in wolves))
        werewolf.WOLF_ABILITY_TIMING = True
        try:
            q = werewolf.wolf_timing()["abilities"]
            for s in wolves:                        # on: each first cast at a real run's time, or not this run
                h = self.ult.impl.wolf_hold(c, s.impl.WOLF)
                self.assertTrue(h == math.inf or any(abs(h - self.e.t - x) < 1e-9 for x in q[s.impl.WOLF] if x is not None))
            self.assertEqual(self.ult.impl.wolf_hold(c, "x"), 0.0)
        finally:
            werewolf.WOLF_ABILITY_TIMING = False


if __name__ == "__main__":
    unittest.main()
