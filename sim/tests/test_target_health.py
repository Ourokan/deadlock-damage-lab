"""Target health for health-conditional items (2026-10-26).

- Mechanics.target_health (on): in fights booked over real lengths, a fighter facing an Opening Rounds holder is seen
  by that item short by a real entry deficit and by TARGET_ASSIST x the damage it takes (the real fight's third
  parties, Fighter.item_hp_frac); its health, the fight's length and execute gates stay. An immortal enemy's refill
  starts a new life the item sees full.
- Tankbuster and Decay deal their current-health damage from that health (Fighter.item_hp), with the third parties at
  CURRENT_HEALTH_ASSIST instead.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim import mechanics as M  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def pair(items, seed=1):
    mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
    e = Engine(distance=10, mech=mech, rng=random.Random(seed))
    f = make_fighter(e, Loadout("Haze", items, souls=27000))
    g = make_fighter(e, Loadout("Abrams", [], souls=27000))
    f.enemy, g.enemy = g, f
    return e, f, g


class TargetHealth(unittest.TestCase):
    def test_on_by_default(self):
        self.assertTrue(M.DEFAULT.target_health)

    def test_only_against_a_holder(self):
        e, f, g = pair([])
        M.target_health(g)
        self.assertEqual(g.item_assist, 0.0)
        self.assertEqual(g.item_hp_frac, g.hp_frac)
        gaps = []
        for s in range(200):
            e, f, g = pair(["Opening Rounds"], seed=s)
            M.target_health(g)
            M.target_health(f)
            self.assertEqual(f.item_assist, 0.0)   # Abrams holds no such item
            self.assertEqual(g.item_assist, M.TARGET_ASSIST)
            self.assertEqual(g.hp, g.max_hp)       # health stays
            self.assertEqual(g.gate_frac, 1.0 - g.entry_gap)
            gaps.append(g.item_gap)
        self.assertTrue(any(x > 0.05 for x in gaps))
        self.assertGreater(sum(x == 0 for x in gaps), 0.3 * len(gaps))   # many fights start full

    def test_opening_rounds_sees_it(self):
        e, f, g = pair(["Opening Rounds"])
        fx = next(x for x in f.items_fx if x.item.class_name == "upgrade_pristine_emblem")
        g.item_assist, g.item_gap = 0.5, 0.0
        g.hp = 0.7 * g.max_hp
        g.dmg_in["gun"] = 0.3 * g.max_hp
        self.assertAlmostEqual(g.item_hp_frac, 0.55)
        self.assertTrue(fx.stat(f))
        g.item_gap = 0.1
        self.assertAlmostEqual(g.item_hp_frac, 0.45)
        self.assertFalse(fx.stat(f))

    def test_engine_run_wires_it(self):
        seen = {}
        probe = type("Probe", (), {"item": None, "on_start": lambda self, x: seen.setdefault(x.name, x.item_assist)})
        for flag, length, want in ((True, True, M.TARGET_ASSIST), (False, True, 0.0), (True, False, 0.0)):
            mech = dataclasses.replace(M.DEFAULT, target_health=flag,
                                       fight_length=M.real_length(27000) if length else None)
            e = Engine(distance=10, mech=mech, rng=random.Random(3))
            f = make_fighter(e, Loadout("Haze", ["Opening Rounds"], souls=27000))
            g = make_fighter(e, Loadout("Abrams", [], souls=27000))
            seen.clear()
            g.items_fx.append(probe())
            e.run(f, g)
            self.assertEqual(seen[g.name], want)

    def test_refill_is_a_new_life(self):
        e, f, g = pair(["Opening Rounds"])
        g.item_assist, g.item_gap = 0.5, 0.2
        g.dmg_in["gun"] = g.max_hp
        refill = type("Refill", (), {"on_lethal": lambda self, x, a: setattr(x, "hp", x.max_hp) or True})()
        g.items_fx.append(refill)
        e.fighters = [f, g]
        g.hp = 10.0
        e.damage(f, g, 1000.0, "bullet", "gun", ignore_resist=True)
        self.assertEqual(g.hp, g.max_hp)
        self.assertAlmostEqual(g.item_hp_frac, 1.0)

    def test_current_health_items_see_it(self):
        for name in ("Tankbuster", "Decay"):
            e, f, g = pair([name])
            M.target_health(g)
            self.assertEqual(g.item_assist, M.TARGET_ASSIST)
        g.item_gap = 0.1
        g.hp = 0.7 * g.max_hp
        g.dmg_in["gun"] = 0.3 * g.max_hp
        self.assertAlmostEqual(g.item_hp / g.max_hp, 0.7 - 0.1 - M.CURRENT_HEALTH_ASSIST * 0.3)
        g.item_assist = 0.0   # no draw: the real health
        self.assertAlmostEqual(g.item_hp, g.hp)

    def test_tankbuster_damage_from_seen_health(self):
        out = []
        for gap in (0.0, 0.5):
            e, f, g = pair(["Tankbuster"])
            e.fighters = [f, g]
            g.item_assist, g.item_gap = M.TARGET_ASSIST, gap
            fx = next(x for x in f.items_fx if x.item.class_name == "upgrade_magic_shock")
            fx.charged_at = -100.0
            before = g.hp
            fx.on_damage_dealt(f, g, type("Hit", (), {"is_ability": True, "is_dot": False, "kind": "spirit", "ability": None,
                                                     "pre_mit": 500.0, "amount": 500.0, "landing": 1.0})())
            out.append(before - g.hp)
        pct = fx.item.p("CurrentHealthDamage") / 100
        self.assertAlmostEqual(out[0] - out[1], 0.5 * g.max_hp * pct * f.skill.item_landing.get("Tankbuster", 1.0),
                               delta=1.0)

    def test_decay_ticks_from_seen_health(self):
        import heapq
        ticks = []
        for gap in (0.0, 0.5):
            e, f, g = pair(["Decay"])
            e.fighters = [f, g]
            g.item_assist, g.item_gap = M.TARGET_ASSIST, gap
            fx = next(x for x in f.items_fx if x.item.class_name == "upgrade_rupture")
            fx.extra(f, g)
            before = g.hp
            t, _, fn, args = heapq.heappop(e.q)
            e.t = t
            fn(*args)
            ticks.append(before - g.hp)
        self.assertGreater(ticks[1], 0)
        self.assertAlmostEqual(ticks[1] / ticks[0], 0.5, delta=0.01)


if __name__ == "__main__":
    unittest.main()
