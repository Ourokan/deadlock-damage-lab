"""Sinclair's copied ultimate scales with her net worth (Mechanics.copy_ult_phase, data/copy_ult_phase.json, 2026-11-12)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from deadsim import mechanics as M  # noqa: E402


class CopyUltPhaseTest(unittest.TestCase):
    def test_copy_curve_rises_with_net_worth(self):
        early, mid, late = (M.copy_ult_phase_mult(nw) for nw in (5000, 15000, 40000))
        self.assertLess(early, 0.7)
        self.assertGreater(late, 1.2)
        self.assertLess(early, mid)
        self.assertLess(mid, late)

    def test_on_by_default_and_flat_without_souls(self):
        self.assertTrue(M.Mechanics().copy_ult_phase)
        self.assertEqual(M.copy_ult_phase_mult(None), 1.0)


if __name__ == "__main__":
    unittest.main()
