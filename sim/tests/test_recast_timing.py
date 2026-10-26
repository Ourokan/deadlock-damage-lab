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

    def test_reset_on_cooldown_draws_a_finite_wait(self):
        """A reset (Refresher, Shadow Transformation) of an ability on cooldown: ready now, cast on a fresh real wait
        from now, never "not again this fight" (the curve's censored share is mostly fights ending)."""
        q = M.recast_rows()["sources"][key("Lady Geist", "Malice")]
        for k in range(12):
            e, ab, castable = self.malice_with_wait(math.inf)
            e.t = ab.ready_at - 0.5 - 0.2 * k   # still on cooldown
            ab.reset_cooldown()
            w = ab.recast_wait
            self.assertNotEqual(w, math.inf)
            self.assertTrue(any(abs(w - max(0.0, h)) < 1e-9 for h in q if h is not None))
            e.t += w
            self.assertTrue(castable(ab))
        e, ab, castable = self.malice_with_wait(5.0)
        ab.reset_cooldown()
        e.t = ab.ready_at - 0.5   # a second reset before a cast draws again
        ab.ready_at = e.t + 1.0
        ab.reset_cooldown()
        self.assertEqual(ab.resets, 2)

    def test_reset_keeps_a_ready_abilitys_wait(self):
        e, ab, castable = self.malice_with_wait(3.0)
        e.t = ab.ready_at + 1.0   # off cooldown, 2 s of its wait left
        ab.reset_cooldown()
        self.assertAlmostEqual(ab.recast_wait, 2.0)
        e, ab, castable = self.malice_with_wait(math.inf)
        e.t = ab.ready_at + 100.0   # not again this fight: a reset of a ready ability doesn't change that
        self.assertFalse(castable(ab))
        self.assertFalse(ab.try_cast())
        ab.reset_cooldown()
        self.assertEqual(ab.recast_wait, math.inf)
        self.assertFalse(castable(ab))
        ab.reset_cooldown(redraw=False)   # no wait at all (Silver's slots keep theirs per form)
        self.assertEqual(ab.recast_wait, 0.0)
        self.assertTrue(castable(ab))

    def test_silver_waits_per_form(self):
        """Silver's slots cast a human or a wolf ability, each on its own cooldown plus its own real recast wait (the
        form swap's cooldown reset used to drop the wait: Boot Kick recast within 0.5 s 89% vs real 3%)."""
        from unittest import mock
        from deadsim.heroes import werewolf as W
        e, f = fighter("Silver")
        ab = next(a for a in f.abilities if a.ab.name == "Boot Kick")
        st = ab.ctx.state
        calls = []

        def fake(a, cls=None, n=None, finite=False):
            calls.append(cls)
            return 2.0 if cls is None else 3.0
        with mock.patch.object(M, "recast_wait", fake):
            ab.cast()   # human form
            self.assertAlmostEqual(st["base_ready"], e.t + ab.cooldown() + 2.0)
            self.assertEqual(ab.recast_wait, 0.0)   # the slot itself isn't held: each form gates on its own
            f.counters[W.WOLF_KEY] = e.t + 100.0
            ab.cast()   # wolf form
            self.assertAlmostEqual(st["wolf_ready"], e.t + ab.impl.wolf_cooldown(ab.ctx) + 3.0)
        self.assertIn(ab.impl.WOLF, calls)   # the wolf ability's own row
        self.assertAlmostEqual(ab.impl.wolf_cooldown(ab.ctx) / ab.cooldown(),
                               W.alt(ab.ctx, ab.impl.WOLF).raw("AbilityCooldown") / ab.ctx.raw("AbilityCooldown"))
        self.assertIn(f"{game().hero('Silver').id}:ability_werewolf_maulingleap", M.recast_rows()["sources"])


class RecastFit(unittest.TestCase):
    """scripts/cast_timing/recast_timing.py fit: which abilities get waits, and from which curve."""

    def fit(self, real_rows, sim_rows):
        import json
        import tempfile
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "cast_timing"))
        import recast_timing as R
        with tempfile.TemporaryDirectory() as d:
            real = os.path.join(d, "real.json")
            with open(real, "w") as fh:
                json.dump({"source": "test", "rows": real_rows}, fh)
            out = os.path.join(d, "out.json")
            with mock_attr(R, "REAL", real), mock_attr(R, "SHRINK", 50.0), mock_attr(R, "MIN_ROW", 40):
                R.fit(real_rows, sim_rows, out)
            with open(out) as fh:
                return json.load(fh)

    def test_skip_shrink_and_rows(self):
        G = list(range(49))
        slow = [min(1.0, 0.02 * k) for k in G]   # 2% by 0.5 s
        fast = [min(1.0, 0.3 + 0.02 * k) for k in G]
        real = {"1:gated": {"chances": 200, "recast_by": slow},       # sim already about real: skipped
                "1:early": {"chances": 200, "recast_by": slow},       # sim gated, but far faster than real: waits
                "1:few": {"chances": 50, "recast_by": slow},          # own row, shrunk toward the pooled curve
                "1:none": {"chances": 30, "recast_by": slow},         # too few: pooled
                "1:big": {"chances": 1000, "recast_by": fast}}
        sim = {"1:gated": (50, [0.0, 0.05]), "1:early": (50, [0.0, 0.4]), "1:few": (50, [0.9, 0.95])}
        d = self.fit(real, sim)
        self.assertEqual(d["skip"], ["1:gated"])
        self.assertIn("1:early", d["sources"])
        self.assertNotIn("1:none", d["sources"])
        self.assertIn("1:few", d["sources"])
        few, own, pooled = d["sources"]["1:few"], d["sources"]["1:early"], d["pooled"]
        fin = lambda q: [h if h is not None else 99.0 for h in q]  # noqa: E731
        # shrunk: between its own curve's waits (slow: long) and the pooled ones (mostly fast)
        self.assertTrue(all(p - 1e-9 <= a <= b + 1e-9 for a, b, p in zip(fin(few), fin(own), fin(pooled))))
        self.assertNotEqual(few, own)


class mock_attr:
    def __init__(self, obj, name, value):
        self.obj, self.name, self.value = obj, name, value

    def __enter__(self):
        self.old = getattr(self.obj, self.name)
        setattr(self.obj, self.name, self.value)

    def __exit__(self, *a):
        setattr(self.obj, self.name, self.old)


class RecastOff(unittest.TestCase):
    def test_off_casts_on_ready(self):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000), recast_timing=False)
        e, f = fighter("Lady Geist", mech=mech)
        ab = next(a for a in f.abilities if a.ab.name == "Malice")
        ab.cast()
        self.assertEqual(ab.recast_wait, 0.0)


if __name__ == "__main__":
    unittest.main()
