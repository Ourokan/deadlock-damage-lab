"""Violet's abilities (deadsim/heroes/artist.py): Living Ink booking and cooldown cuts, Still Life's sketch, Abstract
Landscape's hits. Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.heroes import artist  # noqa: E402

ALL = [True] * 4


class VioletCase(unittest.TestCase):
    tiers = [0, 0, 0, 0]

    def setUp(self):
        self.e = Engine(distance=10, max_time=30)
        sk = Skill(accuracy=1.0, headshot=0.0)
        sk.spirit_accuracy = 1.0
        self.f = make_fighter(self.e, Loadout("Violet", [], souls=20000, skill=sk, tiers=list(self.tiers),
                                              unlocked=ALL))
        self.g = make_fighter(self.e, Loadout("Abrams", [], souls=20000))
        self.f.enemy, self.g.enemy = self.g, self.f
        for s in self.f.abilities + self.g.abilities:
            s.start()
        self.ab = {s.ab.class_name: s for s in self.f.abilities}

    def run_queue(self, until):
        import heapq
        while self.e.q and self.e.q[0][0] <= until:
            t, _, fn, args = heapq.heappop(self.e.q)
            self.e.t = t
            fn(*args)
        self.e.t = until


class TestLivingInk(VioletCase):
    def shoot(self):
        ctx = {"extra_pct": 0.0, "bonus_flat_head": 0.0, "pellet_mult": 1.0, "ignore_resist_frac": 0.0,
               "bonus_spirit": [], "dmg_mult": 1.0}
        li = self.ab["ability_artist_homingbrush"]
        li.impl.on_shot(li.ctx, ctx)
        return ctx

    def test_three_empowered_shots_book_gun_and_splash(self):
        li = self.ab["ability_artist_homingbrush"]
        li.cast()
        for _ in range(3):
            self.assertEqual(self.shoot()["pellet_mult"], 0.0)   # the steered bullet replaces the gun shot
        self.assertEqual(self.shoot()["pellet_mult"], 1.0)       # the 4th is a plain shot
        out = self.f.dmg_out
        self.assertGreater(out.get("gun", 0), 0)
        self.assertGreater(out.get("Living Ink", 0), 0)          # only the splash is booked under the ability

    def test_hits_cut_other_cooldowns_not_its_own(self):
        li, sl = self.ab["ability_artist_homingbrush"], self.ab["ability_artist_tether"]
        self.e.t = 1.0
        li.ready_at = sl.ready_at = 20.0
        artist.cut_cooldowns(li.ctx, 1.5)
        self.assertEqual(li.ready_at, 20.0)
        self.assertAlmostEqual(sl.ready_at, 18.5)

    def test_cuts_skip_effects_without_an_item(self):
        """survival.py's immortal refill (and hero pseudo effects) sit in items_fx with no item: Violet as the
        survival or overall search's enemy crashed every fight on it (rerun 73, 2026-10-25)."""
        import types
        li = self.ab["ability_artist_homingbrush"]
        none, missing = types.SimpleNamespace(item=None, ready_at=5.0), types.SimpleNamespace(ready_at=5.0)
        self.f.items_fx += [none, missing]
        self.e.t = 1.0
        artist.cut_cooldowns(li.ctx, 1.5)
        self.assertEqual((none.ready_at, missing.ready_at), (5.0, 5.0))

    def test_survival_fight_with_violet_as_enemy(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "survival"))
        from survival import survive
        r = survive("Abrams", [], 20000, "Violet", [])
        self.assertGreater(r["damage_taken"], 0)


class TestStillLife(VioletCase):
    def test_sketch_completes_and_stuns(self):
        sl = self.ab["ability_artist_tether"]
        sl.cast()
        self.run_queue(artist.SKETCH_MAX)
        self.assertFalse(sl.scratch["active"])
        self.assertGreaterEqual(sl.scratch["meter"], 100)
        self.assertGreater(self.f.dmg_out.get("Still Life", 0), 0)

    def test_living_ink_hit_fills_the_sketch_once(self):
        sl, li = self.ab["ability_artist_tether"], self.ab["ability_artist_homingbrush"]
        sl.cast()
        before = sl.scratch["meter"]
        li.cast()
        TestLivingInk.shoot(self)
        self.assertAlmostEqual(sl.scratch["meter"] - before, sl.ctx.raw("BuildUpPerShot"))


class TestStillLifeT1(VioletCase):
    tiers = [0, 0, 1, 0]

    def test_t1_regen_is_hp_per_second(self):
        sl = self.ab["ability_artist_tether"]
        sl.cast()
        self.assertGreaterEqual(self.f.stat("regen"), 15.0)


class TestAbstractLandscape(VioletCase):
    def test_hits_damage_times_grove_hits(self):
        al = self.ab["ability_artist_bamboogrove"]
        al.cast()
        self.run_queue(artist.GROVE_FIRST_HIT + 0.01)
        first = self.f.dmg_out.get("Abstract Landscape", 0)
        self.assertGreater(first, 0)
        self.assertTrue(self.g.mods.active("silence"))
        self.run_queue(artist.GROVE_FIRST_HIT + artist.GROVE_REHIT_GAP + 0.01)
        self.assertAlmostEqual(self.f.dmg_out["Abstract Landscape"] / first, artist.GROVE_HITS, places=2)


if __name__ == "__main__":
    unittest.main()
