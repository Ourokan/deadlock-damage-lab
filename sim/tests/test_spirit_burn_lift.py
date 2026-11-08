"""Spirit Burn hero rows above 1 (2026-11-08, accuracy.ROW_ABOVE_ONE): in length-weighted fights a hero row's landing
multiplies the pooled length_corr; the plain 1v1 keeps min(1, landing).
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import accuracy  # noqa: E402


class SpiritBurnLift(unittest.TestCase):
    def test_lifted_row(self):
        rows = accuracy.item_landing("Solomon")
        self.assertLessEqual(rows.get("Spirit Burn", 1.0), 1.0)
        old = accuracy.ROW_ABOVE_ONE_ON
        try:
            accuracy.ROW_ABOVE_ONE_ON = False
            off = accuracy.item_length_corr("Solomon").get("Spirit Burn", 1.0)
            accuracy.ROW_ABOVE_ONE_ON = True
            on = accuracy.item_length_corr("Solomon").get("Spirit Burn", 1.0)
        finally:
            accuracy.ROW_ABOVE_ONE_ON = old
        self.assertGreater(on, off)


if __name__ == "__main__":
    unittest.main()
