"""web/bridge.py replay(): a real fight replayed in the team sim (web/replay.js), and team_fight(start_hp=)."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..", "..")
sys.path[:0] = [os.path.join(HERE, ".."), os.path.join(ROOT, "damage"), os.path.join(ROOT, "web")]

import bridge  # noqa: E402
from deadsim import Loadout, Skill  # noqa: E402
from deadsim.data import game  # noqa: E402
from deadsim.team import team_fight  # noqa: E402


def member(hero, items=(), **kw):
    return dict(hero=hero, items=list(items), souls=20000, **kw)


def replay(a, b, **kw):
    return json.loads(bridge.replay(json.dumps(dict(a=a, b=b, distance=15, max_time=15, **kw))))


class TestReplay(unittest.TestCase):
    def test_start_health(self):
        r = replay([member("Haze", hp=0.4)], [member("Abrams")])
        haze, abrams = r["fighters"]
        self.assertAlmostEqual(haze["start_hp"], 0.4 * haze["max_hp"], delta=1)
        self.assertEqual(abrams["start_hp"], abrams["max_hp"])
        self.assertLessEqual(haze["hp"], haze["start_hp"])

    def test_hurt_hero_dies_sooner(self):
        full = replay([member("Haze")], [member("Infernus", ["Mystic Burst"])])["fighters"][0]
        hurt = replay([member("Haze", hp=0.3)], [member("Infernus", ["Mystic Burst"])])["fighters"][0]
        self.assertFalse(hurt["alive"])
        self.assertTrue(full["alive"] or full["death_time"] > hurt["death_time"])

    def test_start_health_follows_team_order(self):
        # start_hp lists team A then team B: hurting the second B hero hurts only that hero
        r = replay([member("Haze"), member("Abrams")], [member("Infernus"), member("Seven", hp=0.5)])
        starts = [x["start_hp"] / x["max_hp"] for x in r["fighters"]]
        self.assertEqual([round(v, 2) for v in starts], [1.0, 1.0, 1.0, 0.5])

    def test_start_hp_default_leaves_team_fight_unchanged(self):
        a = [Loadout("Haze", ["Rapid Rounds"], souls=20000, skill=Skill(accuracy=0.3))]
        b = [Loadout("Seven", ["Extra Spirit"], souls=20000, skill=Skill(accuracy=0.3))]
        self.assertEqual(team_fight(a, b).to_dict(), team_fight(a, b, start_hp=[None, 1.0]).to_dict())

    def test_real_ability_upgrades(self):
        hero = game().hero("Haze")
        ids = [ab.id for ab in hero.abilities]
        # unlock 1 and 2, upgrade 1 twice; ids of other heroes' abilities are ignored
        tiers, unlocked = bridge._real_abilities(hero, [ids[0], ids[1], ids[0], 123, ids[0]])
        self.assertEqual(unlocked, [True, True, False, False])
        self.assertEqual(tiers, [2, 0, 0, 0])
        locked = replay([member("Haze", abilities=[ids[0]])], [member("Abrams")])["fighters"][0]
        full = replay([member("Haze", abilities=[i for i in ids for _ in range(4)])], [member("Abrams")])["fighters"][0]
        self.assertGreater(full["damage"], locked["damage"])

    def test_own_aim_counts(self):
        lo = replay([member("Haze", accuracy=0.15)], [member("Abrams")])["fighters"][0]
        hi = replay([member("Haze", accuracy=0.5)], [member("Abrams")])["fighters"][0]
        self.assertGreater(hi["damage_by_source"]["gun"], lo["damage_by_source"]["gun"])

    def test_items_change_the_fight(self):
        base = replay([member("Haze"), member("Abrams")], [member("Infernus"), member("Seven")])
        more = replay([member("Haze", ["Toxic Bullets", "Rapid Rounds"]), member("Abrams")], [member("Infernus"), member("Seven")])
        self.assertEqual(len(base["fighters"]), 4)
        self.assertGreater(more["fighters"][0]["damage"], base["fighters"][0]["damage"])

    def test_late_joiner_takes_no_damage_before_arriving(self):
        on = replay([member("Haze"), member("Abrams")], [member("Infernus")])["fighters"]
        late = replay([member("Haze"), member("Abrams", join=10)], [member("Infernus")])["fighters"]
        self.assertGreater(on[1]["damage"], late[1]["damage"])
        self.assertTrue(late[1]["alive"])

    def test_side_with_nobody_yet_waits(self):
        # B arrives at 5 s: nobody shoots before, so A's lone hero takes nothing until then
        r = replay([member("Haze")], [member("Abrams", join=5)])
        self.assertTrue(all(x["alive"] for x in r["fighters"]))
        never = replay([member("Haze")], [member("Abrams", join=30)])["fighters"]   # past max_time (15)
        self.assertEqual(never[0]["damage"], 0)
        self.assertEqual(never[1]["damage_taken"], 0)

    def test_leaver_walks_out_alive(self):
        stay = replay([member("Haze", hp=0.3)], [member("Infernus", ["Mystic Burst"])])["fighters"][0]
        out = replay([member("Haze", hp=0.3, leave=1)], [member("Infernus", ["Mystic Burst"])])["fighters"][0]
        self.assertFalse(stay["alive"])
        self.assertTrue(out["alive"])
        self.assertGreater(out["hp"], 0)

    def test_target_plan(self):
        # everyone on A shoots B's second hero, not the weakest (B's first, at 20%)
        a = [member("Haze", targets=[1] * 15), member("Wraith", targets=[1] * 15)]
        b = [member("Abrams", hp=0.2), member("Seven")]
        planned = replay(a, b)["fighters"]
        focus = replay([member("Haze"), member("Wraith")], b)["fighters"]
        self.assertGreater(planned[3]["damage_taken"], focus[3]["damage_taken"])
        self.assertLess(planned[2]["damage_taken"], focus[2]["damage_taken"])

    def test_whole_side_walking_out_ends_the_fight(self):
        r = replay([member("Haze", leave=2), member("Wraith", leave=3)], [member("Abrams"), member("Seven")])
        self.assertLess(r["time"], 4)
        self.assertTrue(all(x["alive"] for x in r["fighters"]))
        self.assertIsNone(r["winner"])

    def test_dead_planned_target_falls_back_to_focus(self):
        # A plans to shoot B's first hero all fight; it starts at 1 HP and dies at once, then A keeps fighting the other
        r = replay([member("Haze", targets=[0] * 15), member("Wraith", targets=[0] * 15)],
                   [member("Abrams", hp=0.001), member("Seven")])["fighters"]
        self.assertFalse(r[2]["alive"])
        self.assertGreater(r[3]["damage_taken"], 500)

    def test_timing_default_leaves_team_fight_unchanged(self):
        a = [Loadout("Haze", ["Rapid Rounds"], souls=20000, skill=Skill(accuracy=0.3))]
        b = [Loadout("Seven", ["Extra Spirit"], souls=20000, skill=Skill(accuracy=0.3))]
        self.assertEqual(team_fight(a, b).to_dict(),
                         team_fight(a, b, join=[0, None], leave=[None, None], targets=[None, [None]]).to_dict())
        # 3v3 with deaths mid-fight, both focus rules (checked identical to the code before join/leave/targets)
        a3 = [Loadout("Haze", ["Rapid Rounds", "Toxic Bullets"], souls=25000), Loadout("Dynamo", ["Healing Nova"], souls=20000),
              Loadout("Infernus", ["Extra Spirit"], souls=15000)]
        b3 = [Loadout("Abrams", ["Extra Health"], souls=12000), Loadout("Seven", ["Mystic Burst"], souls=30000),
              Loadout("Wraith", ["Rapid Rounds"], souls=18000)]
        for focus in ("focus", "spread"):
            base = team_fight(a3, b3, focus=focus).to_dict()
            self.assertTrue(any(not x["alive"] for x in base["fighters"]))
            self.assertEqual(base, team_fight(a3, b3, focus=focus, join=[None] * 6, leave=[None] * 6,
                                              targets=[None] * 6).to_dict())


@unittest.skipUnless(shutil.which("node"), "needs node")
class TestDetect(unittest.TestCase):
    """web/replay.js finds a made-up fight in made-up match paths (sim/scripts/fight_replay/detect.cjs)."""

    def test_finds_the_fight(self):
        n = 400
        paths, players = [], []
        for slot in range(1, 5):
            far = 9000 + 2000 * slot   # everyone far apart (units; 2000 = 51 m)
            x, hp, c = [far] * n, [100] * n, [0] * n
            if slot in (1, 2):   # slot 1 (team 0) and 2 (team 1) fight from 100 s to 112 s, 2 dies
                for t in range(100, 113):
                    x[t] = 5000 + (0 if slot == 1 else 600)   # ~15 m apart
                    c[t] = 1
                    if slot == 2:
                        hp[t] = max(0, 100 - 9 * (t - 99))
                    elif t % 3 == 0:
                        hp[t] = hp[t - 1] - 5
                    else:
                        hp[t] = hp[t - 1]
                if slot == 2:
                    for t in range(113, 125):
                        hp[t] = 0
                else:
                    for t in range(113, n):
                        hp[t] = hp[112]
            paths.append(dict(player_slot=str(slot), x_min="0", x_max="16383", y_min="0", y_max="16383",
                              x_pos=x, y_pos=[0] * n, health=hp, combat_type=c))
            deaths = [dict(game_time_s=112, killer_player_slot=1, time_to_kill_s=10.0)] if slot == 2 else []
            players.append(dict(player_slot=slot, team=f"Team{(slot + 1) % 2}", death_details=deaths))
        meta = dict(match_info=dict(match_paths=dict(x_resolution=16383, y_resolution=16383, paths=paths), players=players))
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(meta, f)
        try:
            out = subprocess.run(["node", os.path.join(HERE, "..", "scripts", "fight_replay", "detect.cjs"),
                                  os.path.join(ROOT, "web", "replay.js"), f.name], capture_output=True, text=True, check=True)
        finally:
            os.remove(f.name)
        fights = json.loads(out.stdout)["fights"]
        self.assertEqual(len(fights), 1)
        F = fights[0]
        self.assertEqual(sorted(F["players"]), [1, 2])
        self.assertLessEqual(F["t0"], 101)
        self.assertGreaterEqual(F["t1"], 111)
        self.assertEqual([d["slot"] for d in F["deaths"]], [2])
        self.assertEqual(F["hp0"]["2"], 1.0)
        self.assertEqual(F["hp1"]["2"], 0)
        self.assertAlmostEqual(F["dist"], 600 / 39.37, delta=1)
        self.assertEqual(F["join"], {"1": 0, "2": 0})
        self.assertGreaterEqual(F["last"]["1"], F["t1"] - F["t0"] - 1)
        self.assertEqual(set(F["near"]["1"][:5]), {2})   # slot 1's nearest enemy each second


if __name__ == "__main__":
    unittest.main()
