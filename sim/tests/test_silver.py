"""Silver's Lycan Curse on real timing (deadsim/heroes/werewolf.py, data/wolf_timing.json): each fight's first
transform is drawn (already in wolf form, at a real time, or not at all), later casts follow the rage rule. Run from
sim/:
    python3 -m unittest discover -s tests
"""
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


if __name__ == "__main__":
    unittest.main()
