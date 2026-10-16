"""Seven's Storm Cloud: no stacked clouds on a Refresher reset, and the gun-vs-cloud check uses landing rates.
Run from sim/: python3 -m unittest discover -s tests"""
import dataclasses
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "damage")]

from deadsim import Loadout  # noqa: E402
from deadsim.accuracy import hero_default_skill  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.heroes import gigawatt  # noqa: E402
from dummy import Dummy, damage_test  # noqa: E402

ITEMS = ["Improved Spirit", "Refresher", "Superior Duration", "Escalating Exposure"]


class StormCloud(unittest.TestCase):
    def test_refresher_mid_channel_does_not_stack_a_second_cloud(self):
        casts = []
        cast = gigawatt.StormCloud.cast

        def spy(self, c):
            casts.append((c.now, c.now + c.dur("AbilityChannelTime")))
            return cast(self, c)

        gigawatt.StormCloud.cast = spy
        try:
            r = damage_test("Seven", ITEMS, souls=27000, aim="p75", tiers=[3, 3, 0, 3], dummy=Dummy(hp=3000))
        finally:
            gigawatt.StormCloud.cast = cast
        self.assertTrue(casts and r["sources"].get("Storm Cloud", 0) > 0)
        for (_, end), (start, _) in zip(casts, casts[1:]):
            self.assertGreaterEqual(start, end - 1e-9)

    def test_gun_check_scales_power_surge_by_its_landing_rate(self):
        def gun_dps(landing):
            sk = hero_default_skill("Seven", "p75")
            sk = dataclasses.replace(sk, ability_landing={**sk.ability_landing, "Power Surge": landing},
                                     ability_landing_mech={**sk.ability_landing_mech, "Power Surge": landing})
            f = make_fighter(Engine(distance=15), Loadout("Seven", ITEMS, souls=27000, skill=sk, tiers=[3, 3, 3, 3]))
            ps = next(a for a in f.abilities if a.ab.class_name == "ability_power_surge")
            ps.scratch["until"] = 1e9
            return gigawatt.gun_dps(ps.ctx)

        full, half, none = gun_dps(1.0), gun_dps(0.5), gun_dps(0.0)
        self.assertGreater(full, none)
        self.assertAlmostEqual(half - none, (full - none) / 2, places=6)


if __name__ == "__main__":
    unittest.main()
