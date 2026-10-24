"""Replay-calibrated guns (data/gun_calibration.json): Danny's charged shot, Graves' tether range and their aim.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill, compute_stats, duel, game  # noqa: E402
from deadsim.mechanics import Mechanics  # noqa: E402
from unittest import mock  # noqa: E402

import deadsim.accuracy as acc  # noqa: E402
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
        self.assertEqual(st.clip, max(1, round(h.weapon["clip_size"] / cf)))   # a clip lasts as long as the data's

    def test_graves_tether_range(self):
        st = compute_stats("Graves", souls=0)
        r = gun_calibration()[str(G.hero("Graves").id)]["tether_range_m"]
        self.assertEqual(st.gun_range_m, r)
        self.assertGreater(st.falloff(r - 0.1), 0.0)
        self.assertEqual(st.falloff(r + 0.1), 0.0)
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

    def test_graves_duel_beyond_tether_has_no_gun_damage(self):
        aim = Skill(accuracy=0.5, headshot=0.0, use_abilities=False, use_actives=False)
        fixed = Mechanics(range_drift=False)
        for dist, expect_gun in ((10.0, True), (30.0, False)):
            r = duel(Loadout("Graves", [], souls=5000, skill=aim), Loadout("Haze", [], souls=5000, skill=aim),
                     distance=dist, max_time=10.0, mechanics=fixed)
            gun = sum(v for k, v in r.a_dmg.items() if k in ("gun", "Gun", "GUN") or "weapon" in k.lower())
            self.assertEqual(gun > 0, expect_gun, (dist, dict(r.a_dmg)))

    def test_gun_drift_warns_instead_of_failing(self):
        """A patch that moves either gun keeps the old fit running (patch reruns can't refit: that needs live replay
        queries) but warns once per hero, naming the refit (scripts/gun_calib)."""
        import warnings
        import deadsim.build as B
        h = G.hero("Deadman Danny")
        with mock.patch.dict(h.weapon, {"bullet_damage": h.weapon["bullet_damage"] + 1}), \
                mock.patch.object(B, "_warned", set()), warnings.catch_warnings(record=True) as got:
            warnings.simplefilter("always")
            cf, _ = B.gun_quirks(h.id)
            B.gun_quirks(h.id)
        self.assertEqual(cf, gun_calibration()[str(h.id)]["charge_factor"])
        self.assertEqual(len([x for x in got if "gun_calib" in str(x.message)]), 1)

    def test_calibrated_players_are_fitted(self):
        """landing_rates.gun_known keeps Graves/Danny players (no API hero hits) in the ability, item and audit fits."""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
        import landing_rates as L
        no_hits = {acc.HITS: 0}
        self.assertTrue(L.gun_known({"hero_id": G.hero("Graves").id, "custom": no_hits}))
        self.assertFalse(L.gun_known({"hero_id": G.hero("Haze").id, "custom": no_hits}))
        self.assertTrue(L.gun_known({"hero_id": G.hero("Haze").id, "custom": {acc.HITS: L.MIN_HITS}}))
        sk = L.skill_of({"hero_id": G.hero("Deadman Danny").id, "custom": {acc.SHOTS: 400, acc.HITS: 200}})
        self.assertEqual(sk.accuracy, gun_calibration()[str(G.hero("Deadman Danny").id)]["accuracy"]["p50"])

    def test_player_skill_uses_the_replay_fit_without_a_lookup(self):
        """No per-player gun stats exist for these heroes: player_skill returns the replay median, never calls the
        API, and reports zero matches (callers must not divide by it)."""
        with mock.patch.object(acc, "_get", side_effect=AssertionError("no API call expected")):
            sk, info = acc.player_skill(1, hero="Graves")
        row = gun_calibration()[str(G.hero("Graves").id)]
        self.assertEqual((sk.accuracy, sk.headshot), (row["accuracy"]["p50"], 0.0))
        self.assertEqual(info["matches"], 0)
        self.assertEqual(info["median_distance_m"], row["median_distance_m"])


if __name__ == "__main__":
    unittest.main()
