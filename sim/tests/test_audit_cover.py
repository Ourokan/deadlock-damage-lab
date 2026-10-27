"""The damage audit's whole-match cover (scripts/damage_audit.py AUDIT_COVER): duel times drawn from the player's real
damage over the match, and the real damage in each fifth of the match that weighs the sim mix of that fifth.
Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import damage_audit as D  # noqa: E402


def fake_match():
    # one Holliday: 100 damage in the first half of a 1000 s match, 900 in the second
    p = {"hero_id": 14, "slot": 0, "items": [],
         "damage_series": {"citadel_weapon_astro_set": [100, 1000], "Bullet": [100, 1000]}}
    return {"match_id": 1, "duration_s": 1000, "damage_times": [500, 1000], "players": [p]}, p


class AuditCover(unittest.TestCase):
    def test_fracs_follow_real_damage(self):
        m, p = fake_match()
        fr = D.cover_fracs(m, p)
        self.assertEqual(len(fr), D.COVER_DUELS)
        self.assertEqual(fr, sorted(fr))
        # one duel per fifth of the real damage: 10% of it is in the first half, so at most one duel there
        self.assertLessEqual(sum(f < 0.5 for f in fr), 1)
        self.assertTrue(all(0.0 <= f <= 1.0 for f in fr))

    def test_real_bins(self):
        m, p = fake_match()
        rb = D.real_bins(m, p)
        self.assertEqual(len(rb), D.COVER_BINS)
        self.assertAlmostEqual(sum(rb), 1000.0)
        self.assertAlmostEqual(rb[0], 40.0)    # 0-200 s of the first 100 over 500 s
        self.assertAlmostEqual(rb[4], 360.0)   # 800-1000 s of the 900 over 500 s

    def test_no_series(self):
        m, p = fake_match()
        del p["damage_series"]
        self.assertIsNone(D.cover_fracs(m, p))
        self.assertIsNone(D.real_bins(m, p))

    def test_bins(self):
        self.assertEqual(D.cover_bin(0.0), 0)
        self.assertEqual(D.cover_bin(0.39), 1)
        self.assertEqual(D.cover_bin(1.0), D.COVER_BINS - 1)


if __name__ == "__main__":
    unittest.main()
