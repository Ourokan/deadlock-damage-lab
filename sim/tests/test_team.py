"""Tests for deadsim.team (2v2 / 3v3 fights). Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.mechanics import Mechanics  # noqa: E402
from deadsim.team import team_fight, team_item_value  # noqa: E402

S = 20000


def lo(hero, items=(), **kw):
    return Loadout(hero, list(items), souls=S, skill=Skill(accuracy=0.3, **kw))


# duel results pinned from main before team fights (Engine.on_death and the cast notice must not change them),
# with hero fight patterns off (they change cast order on purpose; see tests/test_patterns.py):
# (hero, items, enemy, items, winner, time, damage dealt, damage taken)
DUELS = [   # re-pinned 2026-10-21 for range spread (mechanics range_drift, all hero range checks)
    ("Haze", ["Rapid Rounds", "Toxic Bullets", "Restorative Locket"], "Infernus",
     ["Extra Spirit", "Mystic Burst", "Healing Nova"], "Infernus (B)", 26.59, 2378.6, 2243.3),
    ("Abrams", ["Extra Health", "Ricochet"], "Seven", ["Mystic Burst", "Split Shot", "Rescue Beam"], "Seven (B)", 25.0, 1709.3, 3194.0),
    ("Ivy", ["Extra Spirit", "Divine Barrier"], "Dynamo", ["Hunter's Aura", "Extra Health"], None, 30.0, 1734.4, 1347.1),
]


class TestDuelsUnchanged(unittest.TestCase):
    def test_pinned_duels(self):
        for a, ai, b, bi, win, t, da, db in DUELS:
            r = duel(Loadout(a, ai, souls=S, skill=Skill(accuracy=0.3, melee_rate=0.1, fight_pattern=False)),
                     Loadout(b, bi, souls=S, skill=Skill(accuracy=0.3, fight_pattern=False)))
            got = (r.winner, round(r.time, 3), round(sum(r.a_dmg.values()), 1), round(sum(r.b_dmg.values()), 1))
            self.assertEqual(got, (win, t, da, db), a + " vs " + b)


class TestOneVsOne(unittest.TestCase):
    def test_matches_duel_without_movement(self):
        a, b = lo("Haze", ["Rapid Rounds", "Toxic Bullets"]), lo("Infernus", ["Extra Spirit", "Mystic Burst"])
        d = duel(a, b, max_time=40, mechanics=Mechanics(movement=False))
        t = team_fight([a], [b], max_time=40)
        side = None if d.winner is None else "A" if d.winner == d.a_name else "B"
        self.assertEqual(t.winner, side)
        self.assertAlmostEqual(t.time, d.time, delta=1.0)
        self.assertAlmostEqual(t.fighters[0]["damage"], sum(d.a_dmg.values()), delta=0.05 * sum(d.a_dmg.values()))


class TestTeams(unittest.TestCase):
    def test_fight_ends_when_a_team_is_dead(self):
        a = [lo("Haze", ["Rapid Rounds", "Toxic Bullets"]), lo("Wraith", ["Rapid Rounds"])]
        b = [lo("Haze"), lo("Wraith")]
        r = team_fight(a, b, max_time=90)
        self.assertEqual(r.winner, "A")
        self.assertTrue(all(not x["alive"] for x in r.team("B")))
        self.assertEqual(r.total("A", "kills"), 2)

    def test_two_beat_one(self):
        r = team_fight([lo("Haze"), lo("Haze")], [lo("Haze")], max_time=90)
        self.assertEqual(r.winner, "A")

    def test_focus_and_spread(self):
        a = [lo("Haze"), lo("Wraith"), lo("Abrams")]
        b = [lo("Seven"), lo("Infernus"), lo("Lash")]
        for focus in ("focus", "spread"):
            r = team_fight(a, b, focus=focus)
            self.assertEqual(len(r.fighters), 6)
            self.assertGreater(r.total("A", "damage"), 0)
        guns = dict(use_abilities=False, use_actives=False)   # area abilities would splash the others
        f = team_fight([lo(x.hero, **guns) for x in a], [lo(x.hero, **guns) for x in b], focus="focus", max_time=3)
        hit = [x for x in f.team("B") if x["damage_taken"] > 0]
        self.assertEqual(len(hit), 1)     # everyone shoots the same target at the start


class TestSupport(unittest.TestCase):
    def test_healing_nova_heals_teammate(self):
        a = [lo("Haze"), lo("Dynamo", ["Healing Nova"])]
        b = [lo("Haze", ["Rapid Rounds"]), lo("Wraith", ["Rapid Rounds"])]
        r = team_fight(a, b)
        sup = r.team("A")[1]
        self.assertGreater(sup["healing_given_by_source"].get("Healing Nova", 0), 0)

    def test_rescue_beam_heals_the_teammate(self):
        a = [lo("Haze"), lo("Dynamo", ["Rescue Beam"])]
        b = [lo("Haze", ["Rapid Rounds"]), lo("Wraith", ["Rapid Rounds"])]
        r = team_fight(a, b)
        self.assertGreater(r.team("A")[1]["healing_given_by_source"].get("Rescue Beam", 0), 0)

    def test_divine_barrier_on_teammate(self):
        a = [lo("Haze"), lo("Abrams", ["Divine Barrier"])]
        b = [lo("Haze", ["Rapid Rounds"]), lo("Wraith", ["Rapid Rounds"])]
        r = team_fight(a, b)
        self.assertGreater(r.team("A")[1]["barrier_given"], 0)

    def test_item_value(self):
        a = [lo("Haze"), lo("Dynamo", ["Healing Nova"])]
        b = [lo("Haze", ["Rapid Rounds"]), lo("Wraith", ["Rapid Rounds"])]
        v = team_item_value(a, b, 1, "Healing Nova")
        self.assertGreater(v["delta"]["healing_given"], 0)
        self.assertEqual(set(v["delta"]), {"damage", "damage_taken", "healing_given", "kills", "deaths", "swing", "win", "time"})


class TestTether(unittest.TestCase):
    def test_lone_ivy_matches_duel(self):
        a, b = lo("Ivy", ["Extra Spirit"]), lo("Haze", ["Rapid Rounds"])
        d = duel(a, b, max_time=40, mechanics=Mechanics(movement=False))
        t = team_fight([a], [b], max_time=40)
        self.assertAlmostEqual(t.fighters[0]["damage"], sum(d.a_dmg.values()), delta=0.05 * sum(d.a_dmg.values()))


class TestArea(unittest.TestCase):
    def test_area_abilities_hit_other_enemies(self):
        a = [lo("Dynamo")]
        b = [lo("Haze"), lo("Wraith")]
        on = team_fight(a, b, max_time=20)
        off = team_fight(a, b, max_time=20, aoe_share=0.0)
        self.assertGreater(on.team("A")[0]["damage"], off.team("A")[0]["damage"])

    def test_ricochet_hits_real_teammates(self):
        a = [lo("Haze", ["Ricochet"])]
        b = [lo("Abrams"), lo("Wraith")]
        r = team_fight(a, b, max_time=10)
        self.assertGreater(r.team("A")[0]["damage_by_source"].get("Ricochet", 0), 0)


def fighters(a, b, **kw):
    """Run a team fight and return the two teams' Fighter objects (to inspect buffs and debuffs)."""
    import deadsim.team as T
    seen = {}
    orig = T.TeamEngine.run_team

    def spy(self, ta, tb):
        seen["a"], seen["b"] = ta, tb
        return orig(self, ta, tb)
    T.TeamEngine.run_team = spy
    try:
        team_fight(a, b, **kw)
    finally:
        T.TeamEngine.run_team = orig
    return seen["a"], seen["b"]


class TestSupportMore(unittest.TestCase):
    def setUp(self):
        self.b = [lo("Haze", ["Rapid Rounds"]), lo("Wraith", ["Rapid Rounds"])]

    def test_locket_heals_teammate(self):
        a = [lo("Haze"), lo("Abrams", ["Restorative Locket"])]
        b = [lo("Infernus", ["Extra Spirit"]), lo("Seven", ["Extra Spirit"])]   # casters fill the locket
        r = team_fight(a, b)
        self.assertGreater(r.team("A")[1]["healing_given_by_source"].get("Restorative Locket", 0), 0)

    def test_heroic_aura_speeds_up_teammate(self):
        a = [lo("Haze"), lo("Abrams", ["Heroic Aura"])]
        with_ = team_fight(a, self.b, max_time=8, huddle=1.0)
        without = team_fight([a[0], lo("Abrams")], self.b, max_time=8, huddle=1.0)
        self.assertGreater(with_.team("A")[0]["damage"], without.team("A")[0]["damage"])

    def test_hunters_aura_shreds_every_enemy(self):
        guns = dict(use_abilities=False, use_actives=False)
        a = [lo("Abrams", ["Hunter's Aura"], **guns)]
        b = [lo("Haze", **guns), lo("Wraith", **guns)]
        _, fb = fighters(a, b, max_time=1)
        self.assertTrue(all(sum(e.mods.values("bullet_shred")) > 0 for e in fb))   # not just the target

    def test_rejuvenating_aurora_heals_teammate(self):
        a = [lo("Haze"), lo("Dynamo")]
        r = team_fight(a, self.b)
        self.assertGreater(r.team("A")[1]["healing_given_by_source"].get("Rejuvenating Aurora", 0), 0)

    def test_kudzu_buffs_teammate(self):
        fa, _ = fighters([lo("Haze", use_abilities=False), lo("Ivy")], self.b, max_time=3)
        haze = fa[0]
        self.assertTrue(any(k[0] == "citadel_ability_tangotether" for k in haze.mods.d.get("fire_rate", {})
                            if isinstance(k, tuple)))


class TestBridge(unittest.TestCase):
    def test_web_bridge_team(self):
        import json
        root = os.path.join(os.path.dirname(__file__), "..", "..")
        sys.path[:0] = [os.path.join(root, "web"), os.path.join(root, "damage")]
        import bridge
        r = json.loads(bridge.team(json.dumps({"a": [{"hero": "Haze", "items": ["Rapid Rounds"]},
                                                     {"hero": "Dynamo", "items": ["Healing Nova"]}],
                                               "b": [{"hero": "Abrams"}, {"hero": "Seven"}], "souls": 20000})))
        self.assertEqual(len(r["fighters"]), 4)
        self.assertIn(r["winner"], ("A", "B", None))


if __name__ == "__main__":
    unittest.main()
