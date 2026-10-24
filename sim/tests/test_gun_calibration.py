"""Replay-calibrated guns (data/gun_calibration.json): Danny's charged shot, Graves' tether range and their aim.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import compute_stats, game  # noqa: E402
from deadsim.accuracy import default_distance, gun_calibrated, gun_calibration, hero_default_skill  # noqa: E402
from deadsim.build import gun_quirks  # noqa: E402

G = game()


class GunCalibration(unittest.TestCase):
    def test_danny_charged_shot_keeps_damage_per_second(self):
        h = G.hero("Deadman Danny")
        cf, _ = gun_quirks(h.id)
        self.assertGreater(cf, 1.5)
        st = compute_stats(h.name, souls=0)
        self.assertAlmostEqual(st.bullet_damage, h.weapon["bullet_damage"] * cf)
        self.assertAlmostEqual(st.cycle_time, h.weapon["cycle_time"] * cf)
        self.assertAlmostEqual(st.bullet_damage / st.cycle_time, h.weapon["bullet_damage"] / h.weapon["cycle_time"])

    def test_graves_tether_range(self):
        st = compute_stats("Graves", souls=0)
        self.assertEqual(st.gun_range_m, 20.0)
        self.assertGreater(st.falloff(19.9), 0.0)
        self.assertEqual(st.falloff(20.1), 0.0)
        self.assertIsNone(compute_stats("Haze", souls=0).gun_range_m)

    def test_calibrated_aim_is_the_default(self):
        for name in ("Graves", "Deadman Danny"):
            h = G.hero(name)
            self.assertTrue(gun_calibrated(h.id))
            row = gun_calibration()[str(h.id)]
            sk = hero_default_skill(name)
            self.assertEqual(sk.accuracy, row["accuracy"]["p50"])
            self.assertEqual(sk.headshot, 0.0)
            self.assertEqual(default_distance(name), row["median_distance_m"])
        self.assertFalse(gun_calibrated(G.hero("Haze").id))


if __name__ == "__main__":
    unittest.main()
