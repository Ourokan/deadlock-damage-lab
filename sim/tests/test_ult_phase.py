"""Ult casts by game phase (Mechanics.ult_phase, data/ult_phase.json, scripts/cast_timing/ult_phase.py)."""
import json
import math
import os
import sys
import types
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from deadsim import mechanics as M  # noqa: E402

DATA = json.load(open(os.path.join(ROOT, "data", "ult_phase.json")))


def fake(key, souls):
    hid, cls = key.split(":", 1)
    return types.SimpleNamespace(st=types.SimpleNamespace(hero=types.SimpleNamespace(id=int(hid)), souls=souls)), \
        types.SimpleNamespace(ab=types.SimpleNamespace(class_name=cls, ultimate=True))


class UltPhaseTest(unittest.TestCase):
    def test_multiplier_follows_the_fitted_points(self):
        key, row = next(iter(DATA["sources"].items()))
        pts = row["points"]
        self.assertAlmostEqual(M.ult_phase_mult(key, pts[1][0]), pts[1][1], places=6)
        nw = math.sqrt(pts[0][0] * pts[1][0])   # halfway in ln net worth
        self.assertAlmostEqual(M.ult_phase_mult(key, nw), (pts[0][1] + pts[1][1]) / 2, places=6)
        self.assertAlmostEqual(M.ult_phase_mult(key, 100), pts[0][1], places=6)   # flat outside
        self.assertAlmostEqual(M.ult_phase_mult(key, 1e6), pts[-1][1], places=6)

    def test_early_ults_cast_less_pooled(self):
        p = DATA["pooled"]
        self.assertLess(p[0], 1.0)
        self.assertLess(p[0], p[1])

    def test_no_row_no_change(self):
        self.assertEqual(M.ult_phase_mult("999999:x", 30000), 1.0)
        f, ab = fake("999999:x", 30000)
        q = [1.0] * 10 + [None] * 10
        for u in (0.0, 0.3, 0.7, 0.99):
            self.assertEqual(M.ult_phase_u(f, ab, q, u), u)

    def test_cast_share_scales(self):
        key, row = next((k, v) for k, v in DATA["sources"].items() if abs(v["points"][0][1] - 1.0) > 0.03)
        nw, m = row["points"][0]
        f, ab = fake(key, nw)
        q = [float(k) for k in range(8)] + [None] * 12   # cast share 0.4
        us = [(k + 0.5) / 1000 for k in range(1000)]
        mapped = [M.ult_phase_u(f, ab, q, u) for u in us]
        self.assertTrue(all(a <= b for a, b in zip(mapped, mapped[1:])))   # still a quantile map
        self.assertTrue(all(0.0 <= x < 1.0 for x in mapped))
        cast = sum(q[min(len(q) - 1, int(x * len(q)))] is not None for x in mapped) / len(us)
        self.assertAlmostEqual(cast, 0.4 * m, delta=0.01)

    def test_nurse_ult_matched_to_real_fights(self):
        # scripts/cast_timing/ult_rate_match.py: real Nurses cast Lurking Terrors in 16% of lane fights, ~27% later
        row = DATA["sources"]["87:ability_nurse_fear"]
        self.assertIn("matched", row)
        self.assertLess(M.ult_phase_mult("87:ability_nurse_fear", 5000), 0.75)
        self.assertGreater(M.ult_phase_mult("87:ability_nurse_fear", 30000), 1.0)


if __name__ == "__main__":
    unittest.main()
