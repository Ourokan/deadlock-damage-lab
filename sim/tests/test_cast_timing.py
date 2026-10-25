"""Cast timing (2026-10-25): with Mechanics.fight_length and cast_timing (on by default), each ability the sim casts on
sight gets its first cast held to the real Phantom+ cast timing (data/cast_timing.json,
scripts/cast_timing/fit_cast_timing.py), so a duel no longer opens with every ability and the ultimate at t=0.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import math
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, duel, game  # noqa: E402
from deadsim import engine  # noqa: E402
from deadsim import mechanics as M  # noqa: E402
from deadsim.accuracy import hero_default_skill  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def ult_key(name):
    h = game().hero(name)
    return f"{h.id}:{h.abilities[3].class_name}"


class CastHolds(unittest.TestCase):
    def test_ults_are_held_and_mostly_not_cast(self):
        holds = M.cast_holds()
        q = holds[ult_key("McGinnis")]
        self.assertEqual(len(q), 20)
        timed = [h for h in q if h is not None]
        self.assertTrue(all(a <= b for a, b in zip(timed, timed[1:])))
        self.assertEqual(q[:len(timed)], timed)    # the not-cast values come last
        self.assertLess(len(timed), 12)            # real players cast the ult in well under 60% of fights

    def test_apollo_basic_abilities_are_held(self):
        """Apollo's slow gun kept his players out of the fit until landing_rates.SLOW_GUNS: his three basic
        abilities (cast on sight in the sim, 3-5 s in real fights) now have holds; his ult keeps its health gate."""
        holds = M.cast_holds()
        h = game().hero("Apollo")
        for ab in h.abilities[:3]:
            q = holds[f"{h.id}:{ab.class_name}"]
            self.assertEqual(len(q), 20)
            self.assertGreater(sorted(x for x in q if x is not None)[len(q) // 2 - 1], 1.0)
        self.assertNotIn(ult_key("Apollo"), holds)

    def test_other_slow_guns_are_held(self):
        """Violet, The Doorman and Solomon joined the fits with Apollo's slow-gun limits: their on-sight abilities are
        held to real cast times. Kelvin joined without holds (they made his held-out damage mix worse both ways)."""
        holds = M.cast_holds()
        for name, held in (("Violet", 4), ("The Doorman", 3), ("Solomon", 3)):
            h = game().hero(name)
            rows = [k for k in holds if k.startswith(f"{h.id}:")]
            self.assertEqual(len(rows), held, name)
            self.assertTrue(all(len(holds[k]) == 20 for k in rows))
        self.assertFalse([k for k in holds if k.startswith(f"{game().hero('Kelvin').id}:")])

    def test_hold_moves_the_ready_time(self):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
        e = Engine(mech=mech, rng=random.Random(1))
        f = make_fighter(e, Loadout("McGinnis", [], souls=27000))
        for ab in f.abilities:
            ab.start()
        M.hold_first_casts(f)
        ult = f.abilities[3]
        q = M.cast_holds()[ult_key("McGinnis")]
        self.assertTrue(ult.held_until == math.inf or ult.held_until in q)
        self.assertEqual(ult.ready_at, 0.0)   # not a cooldown

    def test_phase_draw_spreads_over_the_holds(self):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
        q = M.cast_holds()[ult_key("McGinnis")]
        never = 0
        for k in range(40):
            e = Engine(mech=mech)
            lo = Loadout("McGinnis", [], souls=27000)
            lo.skill = dataclasses.replace(lo.skill, fight_phase=k / 40)
            f = make_fighter(e, lo)
            for ab in f.abilities:
                ab.start()
            M.hold_first_casts(f)
            never += f.abilities[3].held_until == math.inf
        # 40 evenly spaced phases (shifted by the hash) give each of the 20 bins 2, give or take one at the edges
        self.assertLessEqual(abs(never - 2 * sum(h is None for h in q)), 1)

    def test_deterministic_and_full_length_fights_cast_on_sight(self):
        a, b = Loadout("McGinnis", [], souls=27000), Loadout("Abrams", [], souls=27000)
        # no fight length: as before
        r0 = duel(a, b, max_time=10, rng=random.Random(2))
        r1 = duel(a, b, max_time=10, rng=random.Random(2), mechanics=dataclasses.replace(M.DEFAULT, cast_timing=False))
        self.assertEqual(r0.a_dmg, r1.a_dmg)
        # fight length but no rng and no phase: nothing to draw from, cast on sight
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
        r2 = duel(a, b, max_time=10, mechanics=mech)
        r3 = duel(a, b, max_time=10, mechanics=dataclasses.replace(mech, cast_timing=False))
        self.assertEqual(r2.a_dmg, r3.a_dmg)

    def test_held_ult_frees_the_gun_early(self):
        """McGinnis' Heavy Barrage channel at t=0 kept her gun quiet for the first seconds of most duels."""
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
        on = off = 0.0
        for k in range(20):
            a = Loadout("McGinnis", [], souls=27000)
            a.skill = dataclasses.replace(a.skill, fight_phase=k / 20)
            b = Loadout("Abrams", [], souls=27000)
            for m, acc in ((mech, "on"), (dataclasses.replace(mech, cast_timing=False), "off")):
                r = duel(a, b, max_time=4, mechanics=m)
                if acc == "on":
                    on += r.a_dmg.get("gun", 0.0)
                else:
                    off += r.a_dmg.get("gun", 0.0)
        self.assertGreater(on, off)

    def held_mcginnis(self, items=()):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
        e = Engine(mech=mech, rng=random.Random(1))
        f = make_fighter(e, Loadout("McGinnis", list(items), souls=27000))
        for ab in f.abilities:
            ab.start()
        for ab in f.abilities:
            ab.held_until = math.inf    # a "not cast in this fight" draw for every ability
        return f

    def test_held_never_casts_and_is_not_on_cooldown(self):
        f = self.held_mcginnis()
        self.assertFalse(any(ab.try_cast() for ab in f.abilities))
        self.assertTrue(all(ab.ready_at <= f.e.t for ab in f.abilities))

    def test_refresher_does_not_release_a_held_ability(self):
        f = self.held_mcginnis(["Refresher"])
        fx = next(x for x in f.items_fx if x.item.name == "Refresher")
        fx.try_active(f)   # nothing is on cooldown: no reset, and a reset would leave the hold anyway
        self.assertFalse(any(ab.try_cast() for ab in f.abilities))

    def test_prefight_ability_keeps_its_timing(self):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
        e = Engine(mech=mech, rng=random.Random(1))
        f = make_fighter(e, Loadout("Mo & Krill", [], souls=27000))
        for ab in f.abilities:
            ab.start()
        M.hold_first_casts(f)
        if f.plan is not None and f.plan.prefight is not None:
            self.assertEqual(f.plan.prefight.held_until, 0.0)


class Precast(unittest.TestCase):
    """A negative hold (mechanics.precast): the ability went out before the fight so its hit opens it."""

    def paradox(self, seed=1):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
        e = Engine(mech=mech, rng=random.Random(seed))
        f = make_fighter(e, Loadout("Paradox", [], souls=27000))
        for ab in f.abilities:
            ab.start()
        return e, f, next(ab for ab in f.abilities if ab.ab.name == "Kinetic Carbine")

    def test_holds_on_due_time_floor_at_the_hit_lag(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "cast_timing"))
        import fit_cast_timing as FCT
        n = len(FCT.GRID)
        sim = {"cast_by": [1.0] * n, "hit_lag_s": 2.5}            # casts on sight, hits 2.5 s later
        real = {"cast_by": [0.0] * 4 + [0.5] * (n - 4),          # real casts: half by 2 s
                "due_by": [0.4] + [0.6] * (n - 1)}               # but 40% of the damage opens the fight
        q = FCT.holds(real, sim)
        self.assertEqual(q[:8], [-2.5] * 8)                        # cast 2.5 s before t=0, the hit at 0
        self.assertTrue(all(h is None for h in q[12:]))           # 60% landed by 20 s
        del sim["hit_lag_s"]                                       # no damage lag: the old cast-curve holds
        self.assertTrue(all(h is None or h >= 0 for h in FCT.holds(real, sim)))

    def test_carbine_has_precast_holds(self):
        q = M.cast_holds()[f"{game().hero('Paradox').id}:citadel_ability_chrono_kinetic_carbine"]
        self.assertLess(min(h for h in q if h is not None), -1.0)   # real openers land with the fight's first hit

    def test_precast_casts_before_the_start(self):
        e, f, kc = self.paradox()
        kc.precast_at = -2.0
        M.precast(f)
        self.assertEqual(kc.casts, 1)
        self.assertEqual(e.t, 0.0)
        self.assertGreater(kc.ready_at, 0.0)   # the cooldown counts from the precast
        self.assertIsNone(kc.precast_at)

    def test_precast_skips_an_ability_on_cooldown(self):
        e, f, kc = self.paradox()
        kc.ready_at = 5.0
        kc.precast_at = -2.0
        M.precast(f)
        self.assertEqual(kc.casts, 0)
        self.assertEqual(kc.ready_at, 5.0)

    def test_refused_precast_restores_the_ability(self):
        e, f, kc = self.paradox()
        kc.precast_at = -2.0
        kc.impl.should_cast = lambda c: False   # its rule turns it down before the fight
        M.precast(f)
        self.assertEqual(kc.casts, 0)
        self.assertEqual((kc.ready_at, kc.held_until), (0.0, 0.0))   # waits for the first chance in the fight

    def test_refused_precast_restores_the_gun_lock(self):
        e, f, kc = self.paradox()
        f.gun_locked_until = -0.5   # free at t=0, but locked at the precast time
        kc.precast_at = -2.0
        kc.impl.should_cast = lambda c: False
        M.precast(f)
        self.assertEqual(f.gun_locked_until, -0.5)

    def test_damage_before_the_start_books_in_slice_0(self):
        e, f, kc = self.paradox()
        g = make_fighter(e, Loadout("Abrams", [], souls=27000))
        f.enemy, g.enemy = g, f
        e.t = -0.4
        e.damage(f, g, 100.0, "spirit", "Kinetic Carbine", is_ability=True)
        e.t = 0.0
        self.assertEqual(set(f.dmg_by_2s), {0})
        self.assertAlmostEqual(f.dmg_exp["Kinetic Carbine"], f.dmg_out["Kinetic Carbine"])   # P(going) at t<0 is 1

    def test_precast_sees_a_free_gun_and_goes_earliest_first(self):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
        e = Engine(distance=8, mech=mech, rng=random.Random(1))
        f = make_fighter(e, Loadout("Lash", [], souls=27000))
        g = make_fighter(e, Loadout("Abrams", [], souls=27000))
        f.enemy, g.enemy = g, f
        for ab in f.abilities:
            ab.start()
        by = {ab.ab.name: ab for ab in f.abilities}
        by["Ground Strike"].precast_at = -0.4   # listed first, cast later
        by["Death Slam"].precast_at = -2.9      # gated on "not busy": t=0's gun state must not turn it down
        M.precast(f)
        self.assertEqual(by["Death Slam"].casts, 1)


    def test_carbine_opener_lands_early(self):
        engine.PROFILE_SOURCES = True
        try:
            early = 0
            for s in range(60):
                mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
                e = Engine(distance=15, max_time=10, rng=random.Random(s), mech=mech)
                a = make_fighter(e, Loadout("Paradox", [], souls=27000))
                b = make_fighter(e, Loadout("Abrams", [], souls=27000))
                e.run(a, b)
                early += a.dmg_first.get("Kinetic Carbine", math.inf) < 1.0
        finally:
            engine.PROFILE_SOURCES = False
        self.assertGreater(early, 6)   # the 2.5 s charge alone kept every Carbine hit past 2.5 s


class UltWait(unittest.TestCase):
    def lash(self):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(27000))
        e = Engine(distance=8, mech=mech, rng=random.Random(1))
        f = make_fighter(e, Loadout("Lash", [], souls=27000))
        g = make_fighter(e, Loadout("Abrams", [], souls=27000))
        f.enemy, g.enemy = g, f
        for ab in f.abilities:
            ab.start()
        by = {ab.ab.name: ab for ab in f.abilities}
        return f, by["Grapple"], by["Death Slam"]

    def test_held_setup_does_not_block_the_ult(self):
        f, grapple, ult = self.lash()
        self.assertFalse(f.plan.allows(ult))   # Death Slam waits for Grapple ...
        grapple.held_until = math.inf
        self.assertTrue(f.plan.allows(ult))    # ... unless Grapple is held out of the fight

    def test_held_first_cast_skips_the_wait(self):
        f, grapple, ult = self.lash()
        ult.timed = True
        self.assertTrue(f.plan.allows(ult))
        ult.casts = 1
        self.assertFalse(f.plan.allows(ult))   # later casts wait as before


class MeleeOpener(unittest.TestCase):
    def duels(self, on, n=80):
        engine.PROFILE_SOURCES = True
        first = []
        try:
            for s in range(n):
                mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(15000), melee_timing=on)
                e = Engine(distance=8, max_time=10, rng=random.Random(s), mech=mech)
                a = make_fighter(e, Loadout("Bebop", ["Spirit Strike"], souls=15000,
                                            skill=hero_default_skill("Bebop")))
                b = make_fighter(e, Loadout("Abrams", [], souls=15000))
                e.run(a, b)
                first.append(a.dmg_first.get("Spirit Strike", math.inf))
        finally:
            engine.PROFILE_SOURCES = False
        return first

    def test_holders_open_with_the_proc(self):
        off, on = self.duels(False), self.duels(True)
        self.assertEqual(sum(t < 1.0 for t in off), 0)   # the steady rate's first melee comes at 2.5 s
        self.assertGreater(sum(t < 1.0 for t in on), 3)

    def test_opener_is_paid_back_by_later_melee(self):
        def ticks(opener):
            mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(15000))
            e = Engine(distance=8, max_time=60, rng=random.Random(3), mech=mech)
            a = make_fighter(e, Loadout("Bebop", ["Spirit Strike"], souls=15000, skill=hero_default_skill("Bebop")))
            b = make_fighter(e, Loadout("Abrams", [], souls=15000))
            a.enemy, b.enemy = b, a
            hits = []
            orig = e.melee_hit
            e.melee_hit = lambda f, heavy, w=1.0: hits.append(w) or orig(f, heavy, w)
            if opener:
                e.melee_open(a, False)
            for k in range(12):
                e.t = 2.5 + 5 * k
                e.melee_tick(a)
            return hits, a.counters.get("melee_debt", 0.0)
        base, _ = ticks(False)
        hits, debt = ticks(True)
        self.assertEqual(hits[0], 1.0)            # the opener is one full hit
        self.assertLess(debt, 1e-9)
        self.assertAlmostEqual(sum(hits), sum(base))   # ... that the later ticks pay back in full

    def test_out_of_reach_tick_keeps_the_debt(self):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(15000))
        e = Engine(distance=30, max_time=60, rng=random.Random(3), mech=mech)
        a = make_fighter(e, Loadout("Bebop", ["Spirit Strike"], souls=15000, skill=hero_default_skill("Bebop")))
        b = make_fighter(e, Loadout("Abrams", [], souls=15000))
        a.enemy, b.enemy = b, a
        a.counters["melee_debt"] = 1.0
        e.mover = type("Far", (), {"start": 0.0, "melee_reach": lambda self, f, heavy: 3.0})()
        e.melee_tick(a)
        self.assertEqual(a.counters["melee_debt"], 1.0)   # no hit landed, nothing paid

    def test_parried_opener_owes_nothing(self):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(15000))
        e = Engine(distance=8, max_time=60, rng=random.Random(3), mech=mech)
        a = make_fighter(e, Loadout("Bebop", ["Melee Charge"], souls=15000, skill=hero_default_skill("Bebop")))
        b = make_fighter(e, Loadout("Abrams", [], souls=15000))
        a.enemy, b.enemy = b, a
        orig = M.parry_check
        M.parry_check = lambda *args: 0.0
        try:
            e.melee_open(a, True)
        finally:
            M.parry_check = orig
        self.assertEqual(a.counters.get("melee_debt"), 0.0)

    def test_no_item_no_opener(self):
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(15000))
        e = Engine(mech=mech, rng=random.Random(1))
        f = make_fighter(e, Loadout("Bebop", [], souls=15000, skill=hero_default_skill("Bebop")))
        self.assertIsNone(M.melee_opener(f))


if __name__ == "__main__":
    unittest.main()
