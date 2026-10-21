"""Range-only items (Mystic Expansion, Greater Expansion) must not decide whether an ability is used at all: players
walk a little closer instead, and with range spread (mechanics range_drift) range shortens the expected wait for the
target to be in reach. Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.mechanics import Mechanics  # noqa: E402

FIXED = Mechanics(range_drift=False)
SPREAD = Mechanics(range_drift=True)


def rake_damage(items, distance=16.3, mech=FIXED):
    """Mina's Rake damage on an idle, refilled Abrams in 30 s at her median fight distance (Rake reaches 10 m)."""
    e = Engine(distance=distance, max_time=30, mech=mech)
    a = make_fighter(e, Loadout("Mina", items, souls=27000, skill=Skill(use_actives=False)), "a")
    d = make_fighter(e, Loadout("Abrams", [], souls=27000, skill=Skill(accuracy=0, use_abilities=False)), "d")
    d.abilities = []
    d.max_hp_base = d.hp = 1e7   # never dies: every run lasts the full 30 s
    e.run(a, d, one_way=True)
    return a.dmg_out.get("Rake", 0.0)


class TestRangeItems(unittest.TestCase):
    def test_rake_cast_without_range_item(self):
        """16.3 m is past Rake's 10 m + 5 m engage margin: Mina walks in instead of never casting it."""
        self.assertGreater(rake_damage([]), 0.0)

    def test_range_item_adds_little_rake_damage(self):
        """Greater Expansion only shortens the walk in, so Rake damage barely moves (it used to unlock Rake)."""
        base, more = rake_damage([]), rake_damage(["Greater Expansion"])
        self.assertLess(abs(more - base), 0.15 * base)

    def test_out_of_walk_in_reach_not_cast(self):
        self.assertEqual(rake_damage([], distance=25.0), 0.0)

    def test_mina_imbues_mystic_expansion_on_retreat(self):
        e = Engine(distance=15, max_time=5)
        f = make_fighter(e, Loadout("Mina", ["Mystic Expansion"], souls=27000))
        held = {s.ab.class_name: [it.name for it in s.imbues] for s in f.abilities}
        self.assertEqual(held["ability_vampirebat_batblink"], ["Mystic Expansion"])


class TestRangeSpread(unittest.TestCase):
    """Range spread: the distance is lognormal around the fight distance (data/fight_range.json)."""

    def test_spread_on_by_default(self):
        e = Engine(distance=16.3, mech=SPREAD)
        self.assertTrue(Mechanics().range_drift)
        self.assertGreater(e.spread, 0.3)
        self.assertAlmostEqual(e.p_within(16.3), 0.5, places=6)
        self.assertEqual(Engine(distance=16.3, mech=FIXED).p_within(16.3), 1.0)

    def test_spread_mean_is_lognormal(self):
        """spread_mean averages over ln(distance / median) ~ N(0, spread^2) (caps lifted for the check)."""
        import math
        import deadsim.mechanics as M
        lo, hi = M.DRIFT_MIN, M.DRIFT_MAX
        M.DRIFT_MIN, M.DRIFT_MAX = 1e-6, 1e6
        try:
            e = Engine(distance=12.0, mech=SPREAD)
            m = e.spread_mean(lambda x: math.log(x / 12.0))
            v = e.spread_mean(lambda x: math.log(x / 12.0) ** 2) - m * m
        finally:
            M.DRIFT_MIN, M.DRIFT_MAX = lo, hi
        self.assertAlmostEqual(m, 0.0, delta=0.03)
        self.assertAlmostEqual(v, e.spread ** 2, delta=0.01 * e.spread ** 2)

    def test_rake_smooth_in_distance_and_range(self):
        """Rake damage falls smoothly with distance (no cliff at reach + margin + walk-in) and a range item adds a
        little at every distance instead of switching Rake on."""
        prev = None
        for dist in (10.0, 13.0, 16.3, 20.0, 25.0):
            base, more = rake_damage([], dist, SPREAD), rake_damage(["Greater Expansion"], dist, SPREAD)
            self.assertGreater(base, 0.0)
            self.assertGreater(more, base)
            self.assertLess(more - base, 0.2 * base)
            if prev is not None:
                self.assertLessEqual(base, prev * 1.02)   # missing-health damage wiggles a little
            prev = base

    def test_close_quarters_partial(self):
        """Close Quarters (bonus within 15 m) pays part of the time at 16.3 m instead of never."""
        from deadsim.items_fx import CloseRange
        e = Engine(distance=16.3, mech=SPREAD)
        f = make_fighter(e, Loadout("Mina", ["Close Quarters"], souls=27000), "a")
        g = make_fighter(e, Loadout("Abrams", [], souls=27000), "d")
        f.enemy, g.enemy = g, f
        fx = next(x for x in f.items_fx if isinstance(x, CloseRange))
        full = fx.item.p("CloseRangeBonusWeaponPower") / 100
        got = fx.stat(f)["weapon_pct"]
        self.assertGreater(got, 0.3 * full)
        self.assertLess(got, 0.7 * full)

    def test_close_quarters_joint_with_falloff(self):
        """The bonus pays where the target is close, where falloff is highest: bullet damage gains more than
        p x bonus x E[falloff] (Engine.band_corr), and Long Range gains less."""
        e = Engine(distance=16.3, mech=SPREAD)
        st = make_fighter(e, Loadout("Haze", [], souls=27000), "a").st
        self.assertGreater(e.band_corr(st, 15, True), 0.0)
        self.assertLess(e.band_corr(st, 15, False), 0.0)

    def test_avail_per_cast(self):
        """The expected-wait damage factor is set on every cast: 1 for a cast that skipped the reach gate, so a
        wait from an earlier, blocked attempt can't carry over."""
        e = Engine(distance=16.3, mech=SPREAD)
        f = make_fighter(e, Loadout("Mina", [], souls=27000), "a")
        g = make_fighter(e, Loadout("Abrams", [], souls=27000), "d")
        f.enemy, g.enemy = g, f
        ab = f.abilities[0]
        cd = ab.charge_delay() if ab.max_charges() > 1 else ab.cooldown()
        ab.scratch["_reach_delay"] = cd
        ab.cast()
        self.assertAlmostEqual(ab.scratch["_avail"], 0.5)
        ab.cast()
        self.assertEqual(ab.scratch["_avail"], 1.0)

    def test_moving_distance_cache_stays_small(self):
        """A chase moves the distance every step: the spread caches bucket it instead of growing per step."""
        e = Engine(distance=16.3, mech=SPREAD)
        f = make_fighter(e, Loadout("Haze", ["Close Quarters", "Long Range"], souls=27000), "a")
        g = make_fighter(e, Loadout("Abrams", [], souls=27000), "d")
        f.enemy, g.enemy = g, f
        still = e.bullet_damage(f)
        for i in range(2000):
            e.distance = 10.0 + i * 0.005
            e.bullet_damage(f)
        self.assertLess(len(e._fall), 200)
        e.distance = 16.3
        self.assertEqual(e.bullet_damage(f), still)   # the starting distance stays exact
        for d in (8.0, 12.3, 21.7, 30.1):   # buckets: same value whatever came before, close to exact
            e.distance = d
            got = e.bullet_damage(f)[0]
            exact = Engine(distance=d, mech=SPREAD)
            h = make_fighter(exact, Loadout("Haze", ["Close Quarters", "Long Range"], souls=27000), "a")
            k = make_fighter(exact, Loadout("Abrams", [], souls=27000), "d")
            h.enemy, k.enemy = k, h
            self.assertAlmostEqual(got, exact.bullet_damage(h)[0], delta=0.01 * got)

    def test_hard_reach_gate_smooth(self):
        """CastCtx.reach (heroes without walk-in, here Vindicta's 25 m stake) follows the spread: Stake damage fades
        as the fight distance grows past the reach (30 m with the engage margin) instead of dropping to nothing."""
        def dmg(distance):
            e = Engine(distance=distance, max_time=30, mech=SPREAD)
            a = make_fighter(e, Loadout("Vindicta", [], souls=27000, skill=Skill(use_actives=False)), "a")
            d = make_fighter(e, Loadout("Abrams", [], souls=27000, skill=Skill(accuracy=0, use_abilities=False)), "d")
            d.abilities = []
            d.max_hp_base = d.hp = 1e7
            e.run(a, d, one_way=True)
            return a.dmg_out.get("Stake", 0.0)
        near, edge, far = dmg(20.0), dmg(32.0), dmg(36.0)
        self.assertGreater(edge, 0.0)
        self.assertGreater(far, 0.0)
        self.assertLess(far, near)



def ability_damage(hero, mech, distance=12.0, p=None):
    """Damage by source on an idle 1e7 HP Abrams in 30 s; p pins Engine.p_within (the share inside any radius)."""
    e = Engine(distance=distance, max_time=30, mech=mech)
    if p is not None:
        e.p_within = lambda r: p
    a = make_fighter(e, Loadout(hero, [], souls=27000, skill=Skill(use_actives=False)), "a")
    d = make_fighter(e, Loadout("Abrams", [], souls=27000, skill=Skill(accuracy=0, use_abilities=False)), "d")
    d.abilities = []
    d.max_hp_base = d.hp = 1e7
    e.run(a, d, one_way=True)
    return a.dmg_out


class TestHeroRangeChecks(unittest.TestCase):
    def test_reach_matches_fixed_gate(self):
        """At a fixed distance CastCtx.reach(r) is the old `dist <= r` gate: no walk-in, no expected-wait factor."""
        for d in (10.0, 20.0, 20.5, 30.0):
            e = Engine(distance=d, mech=FIXED)
            f = make_fighter(e, Loadout("Seven", [], souls=27000), "a")
            state = {}
            self.assertEqual(e.reach_ready(state, 20.0, f, mean_field=True), d <= 20.0, d)
            self.assertNotIn("_reach_delay", state)

    def test_cast_ctx_reach_and_p_in_at_fixed_distance(self):
        """Through a hero's CastCtx: reach(r) is the old `dist <= r` gate and p_in(r) is 1 or 0 at a fixed distance."""
        for d in (10.0, 20.0, 20.5, 30.0):
            e = Engine(distance=d, mech=FIXED)
            f = make_fighter(e, Loadout("Seven", [], souls=27000), "a")
            g = make_fighter(e, Loadout("Abrams", [], souls=27000), "d")
            f.enemy, g.enemy = g, f
            c = f.abilities[0].ctx
            self.assertEqual(c.reach(20.0), d <= 20.0, d)
            self.assertNotIn("_reach_delay", c.state)
            self.assertEqual(c.p_in(20.0), 1.0 if d <= 20.0 else 0.0)

    def test_stun_and_silence_flip_at_median(self):
        """Victor's revive blast stuns and Celeste's barrier pop silences only while p_in >= 0.5 (the target inside
        the radius at the median distance)."""
        from unittest import mock
        import deadsim.abilities as AB
        from deadsim.fight import duel
        seen = []
        orig = AB.CastCtx.debuff

        def debuff(c, kind, *a, **k):
            seen.append((c.s.ab.name, kind))
            return orig(c, kind, *a, **k)

        def effects(a, b, p):
            seen.clear()
            with mock.patch.object(AB.CastCtx, "debuff", debuff), \
                    mock.patch.object(Engine, "p_within", lambda self, r: p):
                duel(Loadout(a, [], souls=27000, skill=Skill(accuracy=0.5)),
                     Loadout(b, [], souls=27000, skill=Skill(accuracy=0.5)), mechanics=FIXED, max_time=60)
            return set(seen)
        for a, b, src, kind in (("Victor", "Haze", "Shocking Reanimation", "stun"),
                                ("Celeste", "Haze", "Dazzling Trick", "silence")):
            self.assertIn((src, kind), effects(a, b, 0.6))
            self.assertNotIn((src, kind), effects(a, b, 0.4))

    def test_p_in_scales_radius_damage(self):
        """Seven's Storm Cloud deals about p x its damage when the target is inside the storm a share p of the time."""
        full = ability_damage("Seven", FIXED, p=1.0)["Storm Cloud"]
        part = ability_damage("Seven", FIXED, p=0.4)["Storm Cloud"]
        self.assertGreater(part, 0.35 * full)
        self.assertLess(part, 0.45 * full)

    def test_tether_scales_then_breaks_at_median(self):
        """Lady Geist's Life Drain drains p x per tick while p >= 0.5 and breaks below (the median-distance check)."""
        full = ability_damage("Lady Geist", FIXED, p=1.0)["Life Drain"]
        self.assertAlmostEqual(ability_damage("Lady Geist", FIXED, p=0.6)["Life Drain"], 0.6 * full, delta=0.01 * full)
        self.assertNotIn("Life Drain", ability_damage("Lady Geist", FIXED, p=0.4))

    def test_haze_fixation_falloff_matches_gun(self):
        """Haze's Fixation bonus uses the same spread-averaged falloff as her bullets, so its share of gun damage
        doesn't change with the spread."""
        for d in (8.0, 16.0):
            f, s = ability_damage("Haze", FIXED, d), ability_damage("Haze", SPREAD, d)
            self.assertAlmostEqual(f["Fixation"] / f["gun"], s["Fixation"] / s["gun"], places=6)

    def test_turret_falloff_averaged(self):
        """McGinnis' Mini Turret falloff averages over the spread: some of the time the target is past falloff start
        even when the median distance isn't."""
        self.assertLess(ability_damage("McGinnis", SPREAD, 8.0)["Mini Turret"],
                        ability_damage("McGinnis", FIXED, 8.0)["Mini Turret"])


if __name__ == "__main__":
    unittest.main()
