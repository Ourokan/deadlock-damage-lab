"""Recast timing (2026-10-26): with Mechanics.fight_length and recast_timing, after each cast of a single-charge,
non-ultimate ability the next one waits a delay past the cooldown drawn from the real Phantom+ recast curve
(data/recast_timing.json, scripts/cast_timing/recast_timing.py): real players recast within 0.5 s of ready only
~15-25% of the time, the sim did ~90%.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import math
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, game  # noqa: E402
from deadsim import mechanics as M  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def key(hero, ability):
    h = game().hero(hero)
    return f"{h.id}:{next(a.class_name for a in h.abilities if a.name == ability)}"


def fighter(hero, mech=None, rng=1, phase=None, souls=27000):
    mech = mech or dataclasses.replace(M.DEFAULT, fight_length=M.real_length(souls), recast_timing=True)
    e = Engine(mech=mech, rng=None if rng is None else random.Random(rng))
    lo = Loadout(hero, [], souls=souls)
    if phase is not None:
        lo.skill = dataclasses.replace(lo.skill, fight_phase=phase)
    f = make_fighter(e, lo)
    for ab in f.abilities:
        ab.start()
    return e, f


class RecastRows(unittest.TestCase):
    def test_rows_are_sorted_waits(self):
        rows = M.recast_rows()
        self.assertGreater(len(rows["sources"]), 20)
        for q in list(rows["sources"].values()) + [rows["pooled"]]:
            self.assertEqual(len(q), 20)
            timed = [h for h in q if h is not None]
            self.assertEqual(q[:len(timed)], timed)   # the not-again values come last
            self.assertTrue(all(a <= b for a, b in zip(timed, timed[1:])))
        # real players mostly don't recast the moment the cooldown is up
        self.assertGreater(rows["pooled"][10], 1.0)

    def test_gated_abilities_keep_their_timing(self):
        """Victor's Pain Battery and Aura of Suffering already wait in the sim (a toggle, health): no wait on top."""
        self.assertIn(key("Victor", "Aura of Suffering"), M.recast_rows()["skip"])
        e, f = fighter("Victor")
        ab = next(a for a in f.abilities if a.ab.name == "Aura of Suffering")
        self.assertEqual(M.recast_wait(ab), 0.0)


class RecastWait(unittest.TestCase):
    def test_wait_comes_from_the_row(self):
        e, f = fighter("Lady Geist")
        ab = next(a for a in f.abilities if a.ab.name == "Malice")
        q = M.recast_rows()["sources"][key("Lady Geist", "Malice")]
        for _ in range(10):
            w = M.recast_wait(ab)
            self.assertTrue(w == math.inf or any(abs(w - max(0.0, h)) < 1e-9 for h in q if h is not None))

    def test_no_draw_without_rng_or_phase_or_for_ults(self):
        e, f = fighter("Lady Geist", rng=None)
        self.assertTrue(all(M.recast_wait(ab) == 0.0 for ab in f.abilities))
        e, f = fighter("Lady Geist")
        self.assertEqual(M.recast_wait(f.abilities[3]), 0.0)

    def test_phase_draw_is_fixed_per_cast(self):
        e, f = fighter("Lady Geist", phase=0.3)
        ab = next(a for a in f.abilities if a.ab.name == "Malice")
        ab.cast()
        self.assertEqual(ab.recast_wait, M.recast_wait(ab))

    def malice_with_wait(self, w):
        from deadsim import patterns
        e, f = fighter("Lady Geist")
        ab = next(a for a in f.abilities if a.ab.name == "Malice")
        ab.cast()
        ab.recast_wait = w
        return e, ab, patterns._castable

    def test_try_cast_and_plan_wait_past_the_cooldown(self):
        e, ab, castable = self.malice_with_wait(2.0)
        e.t = ab.ready_at + 1.0   # cooldown up, wait not over
        self.assertFalse(castable(ab))
        self.assertFalse(ab.try_cast())
        e.t = ab.ready_at + 2.0
        self.assertTrue(castable(ab))

    def test_not_again_this_fight_until_a_reset(self):
        e, ab, castable = self.malice_with_wait(math.inf)
        e.t = ab.ready_at + 100.0
        self.assertFalse(castable(ab))
        self.assertFalse(ab.try_cast())
        ab.reset_cooldown()   # a reset (Refresher) lets it go at once
        self.assertEqual(ab.recast_wait, 0.0)
        self.assertTrue(castable(ab))

    def test_off_casts_on_ready(self):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000), recast_timing=False)
        e, f = fighter("Lady Geist", mech=mech)
        ab = next(a for a in f.abilities if a.ab.name == "Malice")
        ab.cast()
        self.assertEqual(ab.recast_wait, 0.0)


if __name__ == "__main__":
    unittest.main()
