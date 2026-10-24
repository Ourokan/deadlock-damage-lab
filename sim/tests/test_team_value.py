"""Checks of the overall score's team value (damage/scripts/overall_search.py): real teammates / other enemies in
reach from data/team_value.json, area items' hits on the other enemies, ally items' multiplier.
Run from sim/: python3 -m unittest discover -s tests"""
import json
import math
import os
import sys
import types
import unittest
from unittest import mock

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "sim/scripts", "search/scripts", "damage/scripts", "damage",
                                                 "survival")]

import damage_audit  # noqa: E402
from team import area_hits  # noqa: E402
import overall_search as O  # noqa: E402
from survival import survive  # noqa: E402

G = O.S.G()
with open(os.path.join(ROOT, "sim", "data", "area_hits.json")) as _fh:
    AREA_HITS = json.load(_fh)
ID = {it.name: it.id for it in G.items.values()}


class Near(unittest.TestCase):
    def test_counts_grow_with_radius(self):
        for kind in ("allies", "any_ally", "extra", "extra_self"):
            self.assertLess(O.near(kind, 8, 27000), O.near(kind, 30, 27000))

    def test_clamps_at_the_table_edges(self):
        self.assertEqual(O.near("allies", 100, 27000), O.near("allies", 40, 27000))
        self.assertEqual(O.near("allies", 1, 27000), O.near("allies", 5, 27000))
        self.assertEqual(O.near("allies", 35, 80000), O.near("allies", 35, 50000))
        self.assertEqual(O.near("allies", 35, 3000), O.near("allies", 35, 10000))

    def test_interpolates_between_bins(self):
        lo, hi = O.near("allies", 35, 18000), O.near("allies", 35, 27000)
        self.assertTrue(min(lo, hi) <= O.near("allies", 35, 22000) <= max(lo, hi))
        self.assertAlmostEqual(O.near("extra", 15.5, 27000),
                               (O.near("extra", 15, 27000) + O.near("extra", 16, 27000)) / 2, places=6)


class AreaDamage(unittest.TestCase):
    # raw extra hits; the kill weight on top of them is checked in test_kill_weight.py
    def setUp(self):
        self.kill, O.KILL_WEIGHT = O.KILL_WEIGHT, False

    def tearDown(self):
        O.KILL_WEIGHT = self.kill

    def test_area_item_damage_counts_on_the_other_enemies(self):
        # replay values read straight from data/area_hits.json (not through area_extra), so a refit keeps this passing
        r = {"damage_by_source": {"gun": 1000.0, "Mystic Reverb": 200.0, "Scourge": 100.0}, "splash_dealt": 30.0}
        x, bins = AREA_HITS["items"], AREA_HITS["phase"]["bins"]
        lo, hi = max((b for b in bins if b["net_worth"] <= 27000), key=lambda b: b["net_worth"]), \
            min((b for b in bins if b["net_worth"] > 27000), key=lambda b: b["net_worth"])
        u = math.log(27000 / lo["net_worth"]) / math.log(hi["net_worth"] / lo["net_worth"])
        k = lo["fit"] + (hi["fit"] - lo["fit"]) * u
        want = (200 * x["Mystic Reverb"]["extra_per_main"] + 100 * x["Scourge"]["extra_per_main"]) * k + 30
        self.assertAlmostEqual(O.area_damage(r, 27000), want, places=6)

    def test_extra_hits_grow_with_net_worth(self):
        # lane trades early, team fights late: an early build's area items get less of the pooled value
        pooled = O.area_extra("Cold Front")
        early, mid, late = (O.area_extra("Cold Front", s) for s in (6000, 18000, 50000))
        self.assertLess(early, mid)
        self.assertLessEqual(mid, late)
        self.assertLess(early, pooled)
        self.assertGreater(late, pooled)
        self.assertEqual(O.area_extra("Cold Front", 1000), O.area_extra("Cold Front", 3000))     # flat outside the fit
        self.assertEqual(O.area_extra("Cold Front", 80000), O.area_extra("Cold Front", 120000))
        self.assertIsNone(O.area_extra("Toxic Bullets", 27000))

    def test_position_count_is_the_fallback(self):
        r = {"damage_by_source": {"Mystic Reverb": 200.0, "Scourge": 100.0}}
        old = O.area_extra
        O.area_extra = lambda name, souls=None: None
        try:
            got = O.area_damage(r, 27000)
        finally:
            O.area_extra = old
        self.assertAlmostEqual(got, 200 * O.near("extra", 16, 27000) + 100 * O.near("extra_self", 10, 27000), places=6)

    def test_replay_area_hits_cover_the_area_items(self):
        # data/area_hits.json is looked up by item name: a renamed item would silently fall back to positions
        for name in O.AREA_ITEMS:
            x = O.area_extra(name)
            self.assertIsNotNone(x, name)
            self.assertTrue(0.0 <= x < 2.0, name)

    def test_area_items_book_damage_under_their_names(self):
        # area_damage reads damage_by_source by item name: a different label would silently count 0
        h = G.hero("Paradox").id
        for name in O.AREA_ITEMS:
            r = survive(h, [ID[name]], 27000, G.hero("Abrams").id, [], max_time=30.0, focus=2.0, skill=O.skill(h))
            self.assertGreater(r["damage_by_source"].get(name, 0.0), 0.0, name)

    def test_ricochet_bounces_in_the_overall_fight(self):
        h, e = G.hero("Haze").id, G.hero("Abrams").id
        with_ = O.fight(h, [ID["Ricochet"]], e, [], 27000)[0]
        without = O.fight(h, [], e, [], 27000)[0]
        self.assertGreater(with_, without)


class AreaHitsFit(unittest.TestCase):
    def test_mean_net_worth_interpolates_between_snapshots(self):
        curves = [[(100, 1000), (200, 3000)], [(100, 3000), (200, 5000)]]
        self.assertAlmostEqual(area_hits.mean_nw(curves, 150), 3000.0)
        self.assertAlmostEqual(area_hits.mean_nw(curves, 50), 1000.0)     # from 0 before the first snapshot
        self.assertAlmostEqual(area_hits.mean_nw(curves, 900), 4000.0)    # last value after the end

    def test_phase_fit_is_non_decreasing(self):
        # one area item, baseline 0 (no other-hero proc damage): bins observe 0.5, 1.5, 0.9, 1.2 x the pooled 1.0
        rows = [("m", 5000, "Toxic Bullets", 1e6, 0.0)]
        for nw, ratio in ((12000, 0.5), (17000, 1.5), (22000, 0.9), (45000, 1.2)):
            rows += [("m", nw, "Toxic Bullets", 1e6, 0.0), ("m", nw, "Cold Front", 1000.0, 1000.0 * ratio)]
        fit = [b["fit"] for b in area_hits.phase_fit(rows, {"Cold Front": 1.0})]
        self.assertEqual(fit, sorted(fit))
        self.assertAlmostEqual(fit[0], 0.5)
        self.assertAlmostEqual(fit[1], 1.2)    # 1.5 and 0.9 pooled
        self.assertAlmostEqual(fit[3], 1.2)


class AuditSources(unittest.TestCase):
    def test_area_items_and_splash_count_on_other_heroes(self):
        # the damage audit compares with every enemy hero's damage: area items x (1 + replay extra hits), splash as is
        r = types.SimpleNamespace(a_dmg={"gun": 1000.0, "Mystic Reverb": 200.0, "Toxic Bullets": 50.0},
                                  a_splash={"Ricochet": 40.0})
        d = damage_audit.sim_sources(r, lambda k: k, exp=False)
        self.assertAlmostEqual(d["Mystic Reverb"], 200 * (1 + AREA_HITS["items"]["Mystic Reverb"]["extra_per_main"]),
                               places=6)
        self.assertEqual(d["gun"], 1000.0)
        self.assertEqual(d["Toxic Bullets"], 50.0)    # single-target proc: no area value
        self.assertEqual(d["Ricochet"], 40.0)

    def test_expected_booking_reads_the_exp_totals(self):
        r = types.SimpleNamespace(a_dmg={"gun": 1000.0}, a_splash={"Ricochet": 40.0},
                                  a_exp={"gun": 600.0}, a_splash_exp={"Ricochet": 10.0})
        d = damage_audit.sim_sources(r, lambda k: k)
        self.assertEqual(d["gun"], 600.0)
        self.assertEqual(d["Ricochet"], 10.0)


class AllyItems(unittest.TestCase):
    def test_every_fitted_item_is_a_real_item(self):
        # team_value looks items up by name: a renamed item would silently drop to 1.0
        names = {it.name for it in G.items.values()}
        for name in O.team_data()["items"]["values"]:
            self.assertIn(name, names)
        for name in O.AREA_ITEMS:
            self.assertIn(name, names)

    def test_ally_items_raise_the_score(self):
        self.assertEqual(O.team_value([ID["Extra Health"]], 27000), 1.0)
        for name in ("Healing Nova", "Heroic Aura", "Divine Barrier"):
            self.assertGreater(O.team_value([ID[name]], 27000), 1.0, name)

    def test_noisy_fits_count_zero(self):
        # a fit inside its 95% band counts zero, one clear of it counts (synthetic specs: the patch rerun refits
        # team_value.json, so no real item stays noisy for good; Hunter's Aura at 50k was 0.013 +- 0.039)
        def spec(value, se):
            return {"reach": "allies", "radius_m": 20, "reach_sim": 2.0, "budgets": {"50000": {"value": value, "se": se}}}
        data = {"items": {"values": {"Hunter's Aura": spec(0.013, 0.039), "Healing Nova": spec(0.2, 0.02)}}}
        with mock.patch.object(O, "team_data", return_value=data):
            self.assertEqual(O.team_value([ID["Hunter's Aura"]], 50000), 1.0)
            self.assertGreater(O.team_value([ID["Healing Nova"]], 50000), 1.0)

    def test_values_add(self):
        a, b = ID["Healing Nova"], ID["Heroic Aura"]
        both = O.team_value([a, b], 27000) - 1
        self.assertAlmostEqual(both, O.team_value([a], 27000) - 1 + O.team_value([b], 27000) - 1, places=6)


if __name__ == "__main__":
    unittest.main()
