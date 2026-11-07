"""Kill stack items: Glass Cannon, Trophy Collector (build.KILL_STACKS, validation/kill_stacks.md). Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import build as B  # noqa: E402
from deadsim.data import game  # noqa: E402


def item(class_name):
    return next(i for i, it in game().items.items() if it.class_name == class_name)


def glass_cannon():
    return item("upgrade_glass_cannon")


class TestKillStacks(unittest.TestCase):
    def setUp(self):
        self.was = B.KILL_STACKS

    def tearDown(self):
        B.KILL_STACKS = self.was

    def test_stacks_rise_with_net_worth(self):
        self.assertAlmostEqual(B.kill_stacks(10000), 0.36)
        self.assertAlmostEqual(B.kill_stacks(30000), 0.78)
        self.assertAlmostEqual(B.kill_stacks(90000), 2.70)

    def test_fire_rate_and_clip_from_real_stacks(self):
        gc = glass_cannon()
        per = game().item(gc).props.get("FireRatePerKill", 0)
        B.KILL_STACKS = False
        off = B.compute_stats("Wraith", [gc], souls=35000)
        B.KILL_STACKS = True
        on = B.compute_stats("Wraith", [gc], souls=35000)
        self.assertAlmostEqual(on.fire_rate_pct - off.fire_rate_pct, 0.98 * per / 100)
        self.assertEqual(on.clip - off.clip, 2)   # ~0.98 stacks x BonusClipPerKill 2

    def test_stacks_capped_at_max_stacks(self):
        gc = glass_cannon()
        per = game().item(gc).props.get("FireRatePerKill", 0)
        cap = game().item(gc).props.get("MaxStacks", 8)
        B.KILL_STACKS, was = True, B.KILL_STACKS_BY_NW["upgrade_glass_cannon"]
        B.KILL_STACKS_BY_NW["upgrade_glass_cannon"] = ((0, 50.0),)
        try:
            on = B.compute_stats("Wraith", [gc], souls=35000)
        finally:
            B.KILL_STACKS_BY_NW["upgrade_glass_cannon"] = was
        B.KILL_STACKS = False
        off = B.compute_stats("Wraith", [gc], souls=35000)
        self.assertAlmostEqual(on.fire_rate_pct - off.fire_rate_pct, cap * per / 100)

    def test_trophy_range_opt_in(self):
        tc = item("upgrade_trophy_collector")
        per = game().item(tc).props.get("StackingTechRangeMultiplier", 0)
        B.KILL_STACKS = False
        off = B.compute_stats("Wraith", [tc], souls=25000)
        B.KILL_STACKS, was = True, B.KILL_STACK_ITEMS
        B.KILL_STACK_ITEMS = was + ("upgrade_trophy_collector",)
        try:
            on = B.compute_stats("Wraith", [tc], souls=25000)
        finally:
            B.KILL_STACK_ITEMS = was
        shipped = B.compute_stats("Wraith", [tc], souls=25000)
        self.assertEqual(shipped.range_pct, off.range_pct)   # measured, not applied
        self.assertAlmostEqual(on.range_pct - off.range_pct, 8.96 * per / 100)
        self.assertEqual(on.fire_rate_pct, off.fire_rate_pct)
        self.assertLessEqual(B.kill_stacks(99000, "upgrade_trophy_collector"), 16)

    def test_other_items_untouched(self):
        other = next(i for i, it in game().items.items() if it.class_name == "upgrade_rapid_rounds")
        B.KILL_STACKS = True
        on = B.compute_stats("Wraith", [other], souls=35000)
        B.KILL_STACKS = False
        off = B.compute_stats("Wraith", [other], souls=35000)
        self.assertEqual((on.fire_rate_pct, on.clip), (off.fire_rate_pct, off.clip))


if __name__ == "__main__":
    unittest.main()
