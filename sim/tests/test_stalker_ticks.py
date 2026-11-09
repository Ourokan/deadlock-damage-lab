import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from deadsim.mechanics import stalker_ticks_mult  # noqa: E402


class StalkerTicks(unittest.TestCase):
    def test_curve(self):
        lo, hi = stalker_ticks_mult(5000), stalker_ticks_mult(40000)
        self.assertTrue(0.9 < lo <= 1.0)
        self.assertTrue(0.6 < hi < 0.72)
        self.assertGreater(lo, stalker_ticks_mult(16000))
        self.assertEqual(stalker_ticks_mult(0), 1.0)


if __name__ == "__main__":
    unittest.main()
