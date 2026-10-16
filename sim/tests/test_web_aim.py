"""web/aim.js must compute aim the same way as deadsim.accuracy (run with node; skipped when node is missing)."""
import json
import os
import shutil
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim.accuracy import DIST_PREFIX, HEADS, HITS, SHOTS, distance_profile  # noqa: E402

AIM_JS = os.path.join(os.path.dirname(__file__), "..", "..", "web", "aim.js")
HISTS = [
    {"10": 120, "20": 300, "30": 80, "50": 10, "Infinite": 2},
    {"10": 5, "20": 5, "30": 5, "40": 5, "50": 5, "75": 5, "100": 5, "Infinite": 5},
    {"10": 900},
    {"30": 1, "Infinite": 3},
]
META = {"match_info": {
    "custom_user_stats": [{"id": 1, "name": SHOTS}, {"id": 2, "name": HITS}, {"id": 3, "name": HEADS},
                          {"id": 9, "name": DIST_PREFIX + "20"}],
    "players": [{"account_id": 7, "stats": [{"custom_user_stats": [{"id": 1, "value": 10}]},
                                            {"custom_user_stats": [{"id": 1, "value": 400}, {"id": 2, "value": 100},
                                                                   {"id": 3, "value": 20}, {"id": 9, "value": 55}]}]},
                {"account_id": 8, "stats": [{"custom_user_stats": [{"id": 2, "value": 3}]}]}]}}


def node(expr):
    js = f"const Aim = require({json.dumps(os.path.abspath(AIM_JS))});\n(async () => console.log(JSON.stringify(await ({expr}))))();"
    return json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout)


@unittest.skipUnless(shutil.which("node"), "node not installed")
class WebAim(unittest.TestCase):
    def test_median_distance_matches_python(self):
        got = node(f"{json.dumps(HISTS)}.map(Aim.medianDistance)")
        for h, js in zip(HISTS, got):
            py, _ = distance_profile({DIST_PREFIX + k: v for k, v in h.items()})
            self.assertAlmostEqual(js, py, places=9, msg=h)
        self.assertIsNone(node("Aim.medianDistance({})"))

    def test_match_stats_reads_last_snapshot(self):
        cs = node(f"Aim.matchStats({json.dumps(META)}, 7)")
        self.assertEqual((cs[SHOTS], cs[HITS], cs[HEADS], cs[DIST_PREFIX + "20"]), (400, 100, 20, 55))
        self.assertIsNone(node(f"Aim.matchStats({json.dumps(META)}, 8)"))  # no shots at heroes
        self.assertIsNone(node(f"Aim.matchStats({json.dumps(META)}, 99)"))

    def test_resolve_ids_without_network(self):
        got = node("Promise.all(['[U:1:34500250]', '34500250', '76561197994765978',"
                   " 'https://steamcommunity.com/profiles/76561197994765978/'].map(Aim.resolve))")
        self.assertEqual([r["id"] for r in got], [34500250] * 4)

    def test_percentile(self):
        q = {"p25": 0.2, "p50": 0.26, "p75": 0.32, "p90": 0.39}
        got = node(f"[0.1, 0.2, 0.23, 0.30, 0.39, 0.5].map((v) => Aim.percentile(v, {json.dumps(q)}))")
        self.assertEqual(got, [{"below": True, "p": 25}, {"below": False, "p": 25}, {"p": 38}, {"p": 67},
                               {"above": False, "p": 90}, {"above": True, "p": 90}])


if __name__ == "__main__":
    unittest.main()
