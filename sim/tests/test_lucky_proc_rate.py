"""Lucky Shot procs at the replay rate (2026-11-08, scripts/mechanics/item_ticks.py): holders' procs per gun hit on
heroes are 0.296 against the listed 25%, at normal size. Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import items_fx  # noqa: E402
from test_imbue_items import pair  # noqa: E402


class LuckyProcRate(unittest.TestCase):
    def test_procs_per_gun_hit_follow_replays(self):
        e, f, g = pair(["Lucky Shot"], hero="Venator")
        g.hp = g.max_hp_base = 1e12
        f.counters["bullet_per"] = 10.0
        for _ in range(2000):
            e.damage(f, g, 10.0, "bullet", "gun", hits=1)
        got = f.dmg_out.get("Lucky Shot", 0.0) / f.dmg_out["gun"]
        self.assertAlmostEqual(items_fx.LUCKY_PROC_MULT * 0.25, 0.296, places=3)
        self.assertGreater(got, 0.27)    # the listed 25% would read ~0.25
        self.assertLess(got, 0.33)


if __name__ == "__main__":
    unittest.main()
