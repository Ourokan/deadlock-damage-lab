"""Victor's revive history (data/victor_revive.json, scripts/mechanics/victor_revive.py). Run from sim/:
    python3 -m unittest discover -s tests
"""
import json
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts", "mechanics"))

import victor_revive as V  # noqa: E402


class VictorReviveCase(unittest.TestCase):
    def test_phase_by_net_worth(self):
        stats = [{"time_stamp_s": 0, "net_worth": 0}, {"time_stamp_s": 600, "net_worth": 12000},
                 {"time_stamp_s": 1800, "net_worth": 36000}]
        off = lambda t: 20.0   # replay s - game s
        self.assertEqual(V.phase(320.0, stats, off), "lane")    # game 300 s: 6k
        self.assertEqual(V.phase(620.0, stats, off), "mid")     # 12k
        self.assertEqual(V.phase(1500.0, stats, off), "late")   # 28.5k
        self.assertEqual(V.phase(1500.0), "late")               # no clock: by minutes

    def test_data(self):
        with open(os.path.join(ROOT, "data", "victor_revive.json")) as fh:
            d = json.load(fh)
        for ph in ("lane", "mid", "late"):
            q = d["phases"][ph]
            self.assertEqual(len(q), V.QBINS)
            v = [x for x in q if x is not None]
            self.assertEqual(v, sorted(v))
            # the rest of a fight he revived in starts REVIVE_S after the cast: on cooldown at any tier
            self.assertLessEqual(v[0], 145.0)
            self.assertTrue(0.0 <= d["in_fight"][ph]["p"] <= 1.0)
        # real Victors are on cooldown at the start of more mid / late fights than lane ones
        on = {ph: sum(1 for x in d["phases"][ph] if x is not None and x < 145) for ph in d["phases"]}
        self.assertLess(on["lane"], on["mid"])
        self.assertLess(on["lane"], on["late"])


if __name__ == "__main__":
    unittest.main()
