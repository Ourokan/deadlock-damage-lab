"""Cooldown items at the fight start (2026-10-27): with Mechanics.cast_timing and cdr_ready, a build whose items cut an
ability's cooldown starts more fights with it ready (data/cdr_ready.json, scripts/cast_timing/cdr_ready.py): the
first-cast hold draw moves toward the early end of the real holds by the real holders' measured gain.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, game  # noqa: E402
from deadsim import mechanics as M  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def fighter(items):
    ids = {it.name: i for i, it in game().items.items()}
    return make_fighter(Engine(mech=None), Loadout("Seven", [ids[n] for n in items], souls=27000))


def ult(f):
    return next(ab for ab in f.abilities if ab.ab.ultimate)


class CdrReady(unittest.TestCase):
    def test_curves_fall_with_the_cooldown(self):
        d = M.cdr_ready_rows()
        self.assertEqual(len(d["k_grid"]), len(d["pooled"]["ult"]))
        for c in [d["pooled"]["ult"], d["pooled"]["ability"]] + list(d["sources"].values()):
            self.assertTrue(all(a >= b for a, b in zip(c, c[1:])))
        for tag in ("ult", "ability"):
            self.assertTrue(0.0 < d["rho"][tag]["rho"] < 1.0)

    def test_no_cooldown_items_keeps_the_draw(self):
        f = fighter([])
        for ab in f.abilities:
            for u in (0.0, 0.3, 0.7, 0.99):
                self.assertEqual(M.cdr_ready_u(f, ab, u), u)

    def test_cooldown_items_draw_earlier_holds(self):
        f1, f2 = fighter(["Superior Cooldown"]), fighter(["Superior Cooldown", "Transcendent Cooldown"])
        us = [k / 20 for k in range(20)]
        a = [M.cdr_ready_u(f1, ult(f1), u) for u in us]
        b = [M.cdr_ready_u(f2, ult(f2), u) for u in us]
        self.assertTrue(all(x <= u for x, u in zip(a, us)))
        self.assertTrue(all(y <= x for x, y in zip(a, b)))
        self.assertLess(b[10], a[10])
        self.assertTrue(all(x <= y for x, y in zip(a, a[1:])))   # still a quantile map
        self.assertLess(a[-1], 1.0)


if __name__ == "__main__":
    unittest.main()
