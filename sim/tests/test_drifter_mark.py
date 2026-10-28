"""Stalker's Mark bleeds a share of the target's current health (2026-10-28): replays show each tick at ~1.05% of the
health the target had before it at every health level, and a bleed almost never kills. Engine.dot(cur_health=True)
takes dps as a share of current health per second and ticks nonlethal.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import heapq
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def bleed(start_hp, share=0.02, duration=5.0, gap=0.0, **kw):
    e = Engine()
    a = make_fighter(e, Loadout("Drifter", [], souls=0))
    b = make_fighter(e, Loadout("Abrams", [], souls=0))
    a.enemy, b.enemy = b, a
    e.fighters = [a, b]
    b.hp = start_hp
    if gap:   # the real fight's entry deficit, as Mechanics.target_health draws it (Fighter.item_hp)
        b.item_assist, b.item_gap, b.item_dmg0 = 0.35, gap, sum(b.dmg_in.values())
    ticks = []
    e.dot(a, b, share, duration, "Stalker's Mark", cur_health=True, is_ability=True, **kw)
    while e.q:
        t, _, fn, args = heapq.heappop(e.q)
        e.t = t
        before = b.hp
        fn(*args)
        ticks.append(before - b.hp)
    return b, ticks


class StalkersMarkCurrentHealth(unittest.TestCase):
    def test_ticks_follow_current_health(self):
        b, ticks = bleed(1000.0)
        self.assertEqual(len(ticks), 10)
        self.assertTrue(all(x > 0 for x in ticks))
        self.assertTrue(all(y < x for x, y in zip(ticks, ticks[1:])))   # each tick smaller: health went down
        b2, half = bleed(500.0)
        self.assertAlmostEqual(half[0] / ticks[0], 0.5, places=6)        # half the health, half the tick

    def test_follows_item_hp(self):
        """With the real entry deficit drawn, ticks come from Fighter.item_hp, not plain health."""
        _, plain = bleed(1000.0)
        b, short = bleed(1000.0, gap=0.2)
        self.assertAlmostEqual(short[0] / plain[0], (1000.0 - 0.2 * b.max_hp) / 1000.0, places=6)
        _, empty = bleed(1000.0, gap=2.0)   # item_hp clamps to 0: the bleed deals nothing
        self.assertTrue(all(x == 0 for x in empty))

    def test_nonlethal(self):
        b, _ = bleed(5.0, share=0.5, nonlethal=True)
        self.assertTrue(b.alive)
        self.assertGreater(b.hp, 0)


if __name__ == "__main__":
    unittest.main()
