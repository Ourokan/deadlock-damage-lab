"""Fight length (2026-10-24): with Mechanics.fight_length every hit is also booked x P(a real fight is still going),
the booking alone leaves the fight unchanged; landing corrections (which do move the fight) apply only to such fights; Mystic Burst's MinimumDamage checks the
hit's size when it lands, not after the landing factor.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import dataclasses
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim import mechanics as M  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


class LengthWeight(unittest.TestCase):
    def test_interpolates_and_holds_the_last_point(self):
        e = Engine(mech=dataclasses.replace(M.Mechanics(), fight_length=(1.0, 0.5, 0.2)))
        self.assertAlmostEqual(e.length_w(0.0), 1.0)
        self.assertAlmostEqual(e.length_w(M.LENGTH_STEP / 2), 0.75)
        self.assertAlmostEqual(e.length_w(100.0), 0.2)
        self.assertEqual(Engine(mech=M.Mechanics()).length_w(5.0), 1.0)
        self.assertEqual(Engine(mech=None).length_w(5.0), 1.0)

    def test_real_curve_falls_and_has_phases(self):
        c = M.real_length()
        self.assertAlmostEqual(c[0], 1.0)
        self.assertTrue(all(a >= b for a, b in zip(c, c[1:])))
        s10 = c[int(10 / M.LENGTH_STEP)]
        self.assertTrue(0.15 < s10 < 0.6, s10)
        self.assertIsNot(M.real_length(5000), M.real_length(40000))

    def test_booking_leaves_the_fight_unchanged(self):
        a = Loadout("Haze", ["Headshot Booster", "Monster Rounds"], souls=8000)
        b = Loadout("Abrams", ["Extra Health"], souls=8000)
        full = duel(a, b, max_time=20, rng=random.Random(3))
        # cast_timing, recast_timing and entry_hp off: held casts and short entry health do move the fight, the
        # booking alone does not
        mech = dataclasses.replace(M.DEFAULT, fight_length=M.real_length(8000), cast_timing=False,
                                  recast_timing=False, entry_hp=False)
        exp = duel(a, b, max_time=20, rng=random.Random(3), mechanics=mech)
        self.assertEqual(full.winner, exp.winner)
        self.assertAlmostEqual(full.time, exp.time)
        self.assertEqual({k: round(v, 6) for k, v in full.a_dmg.items()}, {k: round(v, 6) for k, v in exp.a_dmg.items()})
        self.assertEqual({k: round(v, 6) for k, v in full.a_exp.items()}, {k: round(v, 6) for k, v in full.a_dmg.items()})
        self.assertLess(sum(exp.a_exp.values()), 0.8 * sum(exp.a_dmg.values()))
        self.assertGreater(sum(exp.a_exp.values()), 0.0)


class LengthCorrections(unittest.TestCase):
    def skill(self):
        return Skill(ability_landing={"Grenade": 0.5}, ability_length_corr={"Grenade": 0.6},
                     item_landing={"Toxic Bullets": 0.5}, item_length_corr={"Toxic Bullets": 2.0, "Split Shot": 0.5})

    def test_only_fights_with_a_length_use_them(self):
        lo = Loadout("Haze", [], souls=5000, skill=self.skill())
        f = make_fighter(Engine(mech=None), lo)
        self.assertAlmostEqual(f.skill.ability_landing["Grenade"], 0.5)
        self.assertNotIn("Split Shot", f.skill.item_landing)
        f = make_fighter(Engine(mech=dataclasses.replace(M.Mechanics(), fight_length=(1.0, 0.5))), lo)
        self.assertAlmostEqual(f.skill.ability_landing["Grenade"], 0.3)
        self.assertAlmostEqual(f.skill.item_landing["Toxic Bullets"], 1.0)
        self.assertAlmostEqual(f.skill.item_landing["Split Shot"], 0.5)   # uncut item: the correction alone

    def test_no_item_corrections_outside_realistic_mode(self):
        sk = dataclasses.replace(self.skill(), item_landing={})
        f = make_fighter(Engine(mech=dataclasses.replace(M.Mechanics(), fight_length=(1.0, 0.5))),
                         Loadout("Haze", [], souls=5000, skill=sk))
        self.assertEqual(f.skill.item_landing, {})


class Survive(unittest.TestCase):
    def test_expected_damage_below_full(self):
        import importlib.util
        path = os.path.join(os.path.dirname(__file__), "..", "..", "survival", "survival.py")
        spec = importlib.util.spec_from_file_location("survival_mod", path)
        S = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(S)
        args = ("Haze", ["Headshot Booster"], 8000, "Abrams", ["Extra Health"])
        full = S.survive(*args, max_time=20)
        exp = S.survive(*args, max_time=20, fight_length=(1.0, 0.5, 0.2))
        self.assertAlmostEqual(full["damage_dealt_full"], full["damage_dealt"])   # (the corrections move exp's fight)
        self.assertLess(exp["damage_dealt"], exp["damage_dealt_full"])
        self.assertGreater(exp["damage_dealt"], 0.0)


class ItemActiveCC(unittest.TestCase):
    def silence(self, skill, mech=None):
        e = Engine(mech=mech)
        a = make_fighter(e, Loadout("Haze", ["Silence Wave"], souls=8000, skill=skill))
        b = make_fighter(e, Loadout("Abrams", [], souls=8000))
        a.enemy, b.enemy = b, a
        fx = next(x for x in a.items_fx if x.name == "Silence Wave")
        return fx.cc(3.0)

    def test_silence_follows_the_fitted_factor_without_the_length_correction(self):
        self.assertAlmostEqual(self.silence(Skill()), 3.0)
        self.assertAlmostEqual(self.silence(Skill(item_landing={"Silence Wave": 0.5})), 1.5)
        sk = Skill(item_landing={"Silence Wave": 0.5}, item_length_corr={"Silence Wave": 0.4})
        self.assertAlmostEqual(self.silence(sk, dataclasses.replace(M.Mechanics(), fight_length=(1.0, 0.5))), 1.5)
        self.assertAlmostEqual(self.silence(Skill(item_landing={"Silence Wave": 1.3})), 3.0)


class MinimumDamage(unittest.TestCase):
    def test_threshold_checks_the_landed_hit_size(self):
        e = Engine(mech=None)
        a = make_fighter(e, Loadout("Infernus", ["Mystic Burst"], souls=800,
                                    skill=Skill(ability_landing={"big": 0.5})))
        b = make_fighter(e, Loadout("Abrams", [], souls=800))
        a.enemy, b.enemy = b, a
        e.damage(a, b, 120, "spirit", "big", is_ability=True)   # 60 after the factor, 120 when it lands
        self.assertGreater(a.dmg_out.get("Mystic Burst", 0.0), 0.0)

    def test_witchmail_threshold_checks_the_landed_hit_size(self):
        e = Engine(mech=None)
        a = make_fighter(e, Loadout("Infernus", [], souls=8000, skill=Skill(ability_landing={"big": 0.5})))
        b = make_fighter(e, Loadout("Abrams", ["Witchmail"], souls=8000))
        a.enemy, b.enemy = b, a
        ab = b.abilities[0]
        ab.ready_at = e.t + 30.0
        e.damage(a, b, 100, "spirit", "big", is_ability=True)   # 50 after the factor, 100 (>= 75) when it lands
        self.assertLess(ab.ready_at, e.t + 30.0)


if __name__ == "__main__":
    unittest.main()
