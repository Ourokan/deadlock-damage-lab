"""Build pool rows: a (match, player) row the build files hold twice counts once (search/scripts/build_pool.py
player_rows). Run from sim/: python3 -m unittest discover -s tests"""
import gzip
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts")]

import build_pool as P  # noqa: E402


class PlayerRows(unittest.TestCase):
    def test_repeats_dropped(self):
        rows = [{"match_id": 1, "account_id": 10}, {"match_id": 1, "account_id": 11},
                {"match_id": 1, "account_id": 10}, {"match_id": 2, "account_id": 10}]
        with tempfile.TemporaryDirectory() as d:
            fn = os.path.join(d, "2026-10-01.jsonl.gz")
            with gzip.open(fn, "wt") as f:
                f.writelines(json.dumps(r) + "\n" for r in rows)
            got = [(r["match_id"], r["account_id"]) for r in P.player_rows([fn])]
        self.assertEqual(got, [(1, 10), (1, 11), (2, 10)])


if __name__ == "__main__":
    unittest.main()
