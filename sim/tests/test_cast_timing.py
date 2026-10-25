"""Cast timing (2026-10-25): with Mechanics.fight_length and cast_timing (on by default), each ability the sim casts on
sight gets its first cast held to the real Phantom+ cast timing (data/cast_timing.json,
scripts/cast_timing/fit_cast_timing.py), so a duel no longer opens with every ability and the ultimate at t=0.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import math
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, duel, game  # noqa: E402
from deadsim import mechanics as M  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def ult_key(name):
    h = game().hero(name)
    return f"{h.id}:{h.abilities[3].class_name}"


class CastHolds(unittest.TestCase):
    def test_ults_are_held_and_mostly_not_cast(self):
        holds = M.cast_holds()
        q = holds[ult_key("McGinnis")]
        self.assertEqual(len(q), 20)
        timed = [h for h in q if h is not None]
        self.assertTrue(all(a <= b for a, b in zip(timed, timed[1:])))
        self.assertEqual(q[:len(timed)], timed)    # the not-cast values come last
        self.assertLess(len(timed), 12)            # real players cast the ult in well under 60% of fights

    def test_hold_moves_the_ready_time(self):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
        e = Engine(mech=mech, rng=random.Random(1))
        f = make_fighter(e, Loadout("McGinnis", [], souls=27000))
        for ab in f.abilities:
            ab.start()
        M.hold_first_casts(f)
        ult = f.abilities[3]
        q = M.cast_holds()[ult_key("McGinnis")]
        self.assertTrue(ult.ready_at == math.inf or ult.ready_at in q)

    def test_phase_draw_spreads_over_the_holds(self):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
        q = M.cast_holds()[ult_key("McGinnis")]
        never = 0
        for k in range(40):
            e = Engine(mech=mech)
            lo = Loadout("McGinnis", [], souls=27000)
            lo.skill = dataclasses.replace(lo.skill, fight_phase=k / 40)
            f = make_fighter(e, lo)
            for ab in f.abilities:
                ab.start()
            M.hold_first_casts(f)
            never += f.abilities[3].ready_at == math.inf
        self.assertEqual(never, 2 * sum(h is None for h in q))   # 40 phases = 2 per bin

    def test_deterministic_and_full_length_fights_cast_on_sight(self):
        a, b = Loadout("McGinnis", [], souls=27000), Loadout("Abrams", [], souls=27000)
        # no fight length: as before
        r0 = duel(a, b, max_time=10, rng=random.Random(2))
        r1 = duel(a, b, max_time=10, rng=random.Random(2), mechanics=dataclasses.replace(M.DEFAULT, cast_timing=False))
        self.assertEqual(r0.a_dmg, r1.a_dmg)
        # fight length but no rng and no phase: nothing to draw from, cast on sight
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
        r2 = duel(a, b, max_time=10, mechanics=mech)
        r3 = duel(a, b, max_time=10, mechanics=dataclasses.replace(mech, cast_timing=False))
        self.assertEqual(r2.a_dmg, r3.a_dmg)

    def test_held_ult_frees_the_gun_early(self):
        """McGinnis' Heavy Barrage channel at t=0 kept her gun quiet for the first seconds of most duels."""
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
        on = off = 0.0
        for k in range(20):
            a = Loadout("McGinnis", [], souls=27000)
            a.skill = dataclasses.replace(a.skill, fight_phase=k / 20)
            b = Loadout("Abrams", [], souls=27000)
            for m, acc in ((mech, "on"), (dataclasses.replace(mech, cast_timing=False), "off")):
                r = duel(a, b, max_time=4, mechanics=m)
                if acc == "on":
                    on += r.a_dmg.get("gun", 0.0)
                else:
                    off += r.a_dmg.get("gun", 0.0)
        self.assertGreater(on, off)


if __name__ == "__main__":
    unittest.main()
