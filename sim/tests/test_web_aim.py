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


def node(expr, routes=None):
    """Evaluate expr with aim.js loaded. fetch is stubbed: routes maps an API path to a JSON body, a number to
    that HTTP status, anything else is a 404, so the tests never touch the network."""
    stub = (f"const ROUTES = {json.dumps(routes or {})};\n"
            "global.fetch = async (url) => { const r = ROUTES[url.replace('https://api.deadlock-api.com', '')];"
            " return typeof r === 'number' ? { ok: false, status: r } : r === undefined ? { ok: false, status: 404 }"
            " : { ok: true, status: 200, json: async () => r }; };\n")
    js = stub + f"const Aim = require({json.dumps(os.path.abspath(AIM_JS))});\n(async () => console.log(JSON.stringify(await ({expr}))))();"
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

    def test_resolve_id_formats(self):
        got = node("Promise.all(['[U:1:34500250]', '34500250', '76561197994765978',"
                   " 'https://steamcommunity.com/profiles/76561197994765978/'].map(Aim.resolve))")
        self.assertEqual([r["id"] for r in got], [34500250] * 4)

    def test_held_at(self):
        # net worth 0 -> 10k at 600 s -> 20k at 1200 s; item 2 is built from 1, item 4 sold at 700 s, 9 not a shop item
        b = {"items": [[1, 100, 0], [2, 500, 0], [3, 650, 0], [4, 200, 700], [9, 50, 0], [5, 1100, 0]],
             "nw": [[600, 10000], [1200, 20000]], "net_worth": 21000}
        known, comps = "(id) => id !== 9", "(id) => (id === 2 ? [1] : [])"
        at = node(f"Aim.heldAt({json.dumps(b)}, 12000, {known}, {comps})")   # 12k reached at 720 s
        self.assertAlmostEqual(at["t"], 720)
        self.assertEqual(at["items"], [2, 3])           # 4 sold at 700, 5 bought later, 1 inside 2, 9 unknown
        end = node(f"Aim.heldAt({json.dumps(b)}, 99999, {known})")             # never reached: the end build
        self.assertIsNone(end["t"])
        self.assertEqual(end["items"], [1, 2, 3, 5])     # no comps given: components stay

    def test_from_matches(self):
        def meta(shots, hits, heads):
            m = json.loads(json.dumps(META))
            m["match_info"]["players"][0]["stats"][-1]["custom_user_stats"][:3] = [
                {"id": 1, "value": shots}, {"id": 2, "value": hits}, {"id": 3, "value": heads}]
            return m
        hist = [{"match_id": i, "hero_id": 1 if i < 5 else 2, "game_mode": 1, "start_time": 100 - i} for i in range(8)]
        hist.append({"match_id": 99, "hero_id": 1, "game_mode": 4, "start_time": 200})  # not a normal match
        routes = {"/v1/players/7/match-history": hist, "/v1/matches/99/metadata": meta(1000, 1000, 1000),
                  "/v1/matches/0/metadata": meta(100, 30, 6), "/v1/matches/1/metadata": 429,
                  "/v1/matches/2/metadata": meta(300, 60, 6), "/v1/matches/5/metadata": meta(50, 50, 50)}
        r = node("Aim.fromMatches(7, 1, { n: 10 })", routes)  # 5 hero-1 matches: 0 and 2 readable, 1 rate-limited
        self.assertEqual((r["scope"], r["matches"], r["failed"], r["shots"], r["hits"], r["headshots"]),
                         ("hero", 2, 1, 400, 90, 12))
        self.assertAlmostEqual(r["accuracy"], 90 / 400)
        r = node("Aim.fromMatches(7, 3, { n: 1 })", routes)  # no hero-3 matches: all heroes, newest readable first
        self.assertEqual((r["scope"], r["matches"], r["shots"]), ("all", 1, 100))

    def test_percentile(self):
        q = {"p25": 0.2, "p50": 0.26, "p75": 0.32, "p90": 0.39}
        got = node(f"[0.1, 0.2, 0.23, 0.30, 0.39, 0.5].map((v) => Aim.percentile(v, {json.dumps(q)}))")
        self.assertEqual(got, [{"below": True, "p": 25}, {"below": False, "p": 25}, {"p": 38}, {"p": 67},
                               {"above": False, "p": 90}, {"above": True, "p": 90}])


if __name__ == "__main__":
    unittest.main()
