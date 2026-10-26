"""The damage audit's item denominators (scripts/damage_audit.py ITEM_NORM): all of the holder's damage while the item
was owned (real: landing_rates.held_gun(gun_only=False)), or gun damage only (AUDIT_NORM=gun, as before 2026-10-26).
Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from deadsim import game  # noqa: E402
import landing_rates as L  # noqa: E402

ITEM = 2010028405   # an item id from the Phantom+ sample


def fake_match():
    # one Holliday: cumulative damage at 100 s and 200 s; "Bullet" is a per-type total (landing_rates.CATEGORY)
    p = {"hero_id": 14, "slot": 0, "items": [[ITEM, 100, 0, 1]],
         "damage_series": {"citadel_weapon_astro_set": [50, 150], "Bullet": [50, 150],
                           "ability_explosive_barrel": [20, 40], "upgrade_headshot_booster": [0, 30]}}
    return {"duration_s": 200, "damage_times": [100, 200], "players": [p]}, p


class AuditItemNorm(unittest.TestCase):
    def test_held_damage_gun_and_total(self):
        m, p = fake_match()
        c = game().items[ITEM].class_name
        self.assertAlmostEqual(L.held_gun(m, p)[c], 100.0)                   # gun only: 150 - 50
        self.assertAlmostEqual(L.held_gun(m, p, gun_only=False)[c], 150.0)   # 220 - 70, the Bullet total left out

    def test_no_series(self):
        m, p = fake_match()
        del p["damage_series"]
        self.assertIsNone(L.held_gun(m, p, gun_only=False))

    def test_length_factors_keeps_gun(self):
        old = os.environ.pop("AUDIT_NORM", None)
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "fight_length"))
            import importlib
            import damage_audit
            import length_factors  # noqa: F401
            self.assertEqual(os.environ.get("AUDIT_NORM"), "gun")
            self.assertEqual(importlib.reload(damage_audit).ITEM_NORM, "gun")
        finally:
            if old is None:
                os.environ.pop("AUDIT_NORM", None)
            else:
                os.environ["AUDIT_NORM"] = old
            import damage_audit
            importlib.reload(damage_audit)


if __name__ == "__main__":
    unittest.main()
