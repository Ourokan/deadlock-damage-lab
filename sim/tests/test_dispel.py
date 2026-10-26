"""Dispel Magic cleanses only Skill.dot_cleanse_share of enemy DoTs (fitted, sim/scripts/fit_dispel.py).
Run from sim/: python3 -m unittest discover -s tests"""
import dataclasses
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from deadsim import Loadout, duel  # noqa: E402
from deadsim.accuracy import _dispel_fit, dot_cleanse_delay, dot_cleanse_share, hero_default_skill  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.items_fx import DispelMagic  # noqa: E402


def decay_taken(share, phase=None):
    a = Loadout("Seven", ["Extra Spirit", "Mystic Burst", "Decay"], souls=20000,
                skill=hero_default_skill("Seven", badge=91, counterplay=True))
    sk = dataclasses.replace(hero_default_skill("Haze", badge=91, counterplay=True), dot_cleanse_share=share,
                             fight_phase=phase)
    b = Loadout("Haze", ["Rapid Rounds", "Swift Striker", "Dispel Magic"], souls=20000, skill=sk)
    return duel(a, b).a_dmg.get("Decay", 0.0)


class DispelShare(unittest.TestCase):
    def test_fitted_share_loaded(self):
        for badge in (None, 91, 111):
            s = dot_cleanse_share(badge)
            self.assertIsNotNone(s)
            self.assertTrue(0.0 < s < 1.0)
        self.assertEqual(dot_cleanse_share(111), dot_cleanse_share(91))

    def test_share_gates_cleanse(self):
        never, always = decay_taken(0.0), decay_taken(1.0)
        self.assertGreater(never, 0.0)
        self.assertLess(always, 0.6 * never)

    def test_phase_picks_share_of_fights(self):
        # the first DoT is cleansed when phase + share crosses 1: in about `share` of evenly spread phases
        never = decay_taken(0.0)
        cleansed = sum(decay_taken(0.4, phase=k / 10) < 0.6 * never for k in range(10))
        self.assertIn(cleansed, (3, 4, 5))

    def test_reaction_by_rank(self):
        self.assertEqual(dot_cleanse_delay(111), 1.5)
        self.assertEqual(dot_cleanse_delay(91), 3.0)
        self.assertEqual(dot_cleanse_delay(None), 3.0)

    def test_missing_fit_raises(self):
        with self.assertRaises(OSError):
            _dispel_fit(-1)

    def test_unphased_phase_spreads(self):
        # no fight_phase, no rng: the pick starts at a hash of both loadouts, spread over 0-1 across opponents
        names = ["Extra Health", "Extra Regen", "Extra Stamina", "Healing Rite", "Close Quarters", "Headshot Booster",
                 "Rapid Rounds", "Spirit Strike", "Monster Rounds", "Sprint Boots", "Spirit Lifesteal",
                 "Bullet Lifesteal", "Extra Charge", "Hollow Point", "Mystic Burst", "Toxic Bullets"]
        phases = []
        for a in names:
            for b in names[:8]:
                e = Engine()
                fa = make_fighter(e, Loadout("Seven", [a, "Decay"], souls=10000))
                fb = make_fighter(e, Loadout("Haze", [b, "Dispel Magic"], souls=10000))
                fa.enemy, fb.enemy = fb, fa
                phases.append(DispelMagic.loadout_phase(fb))
        below = sum(p < 0.5 for p in phases) / len(phases)
        self.assertTrue(0.35 < below < 0.65, below)
        self.assertGreater(len(set(round(p, 6) for p in phases)), len(phases) // 4)

    def test_buildup_share_loaded(self):
        from deadsim.accuracy import dot_cleanse_share_buildup
        # real holders cleanse Afterburn far more than Decay
        self.assertGreater(dot_cleanse_share_buildup(91), dot_cleanse_share(91))
        self.assertLessEqual(dot_cleanse_share_buildup(91), 1.0)
        self.assertIsNotNone(hero_default_skill("Haze", badge=91).dot_cleanse_share_buildup)


def afterburn_taken(share_buildup, items=("Rapid Rounds", "Swift Striker", "Dispel Magic")):
    a = Loadout("Infernus", ["Extra Spirit", "Mystic Burst", "Rapid Rounds"], souls=20000,
                skill=hero_default_skill("Infernus", badge=91, counterplay=True))
    sk = dataclasses.replace(hero_default_skill("Haze", badge=91, counterplay=True), dot_cleanse_share=0.0,
                             dot_cleanse_share_buildup=share_buildup)
    return duel(a, Loadout("Haze", list(items), souls=20000, skill=sk)).a_dmg.get("Afterburn", 0.0)


class DispelAfterburn(unittest.TestCase):
    def test_afterburn_is_purged(self):
        # Afterburn ticks on its own schedule (not Engine.dot): it must still show to Dispel and stop on a purge
        never, always = afterburn_taken(0.0), afterburn_taken(1.0)
        self.assertGreater(never, 0.0)
        self.assertLess(always, 0.85 * never)

    def test_buildup_share_only_for_buildup(self):
        # Decay is not a build-up DoT: the build-up share must not cleanse it, while its own share does
        def decay(share, share_buildup):
            a = Loadout("Seven", ["Extra Spirit", "Mystic Burst", "Decay"], souls=20000,
                        skill=hero_default_skill("Seven", badge=91, counterplay=True))
            sk = dataclasses.replace(hero_default_skill("Haze", badge=91, counterplay=True), dot_cleanse_share=share,
                                     dot_cleanse_share_buildup=share_buildup)
            return duel(a, Loadout("Haze", ["Rapid Rounds", "Swift Striker", "Dispel Magic"], souls=20000,
                                   skill=sk)).a_dmg.get("Decay", 0.0)
        base = decay(0.0, 0.0)
        self.assertGreater(base, 0.0)
        self.assertAlmostEqual(decay(0.0, 1.0), base, places=6)
        self.assertLess(decay(1.0, 0.0), 0.6 * base)

    def test_buildup_joins_running_episode(self):
        # a Decay episode drawn "no" (share 0) must not keep Dispel off Afterburn that starts during it
        a = Loadout("Infernus", ["Extra Spirit", "Mystic Burst", "Rapid Rounds", "Decay"], souls=25000,
                    skill=hero_default_skill("Infernus", badge=91, counterplay=True))

        def burn(share_buildup):
            sk = dataclasses.replace(hero_default_skill("Haze", badge=91, counterplay=True), dot_cleanse_share=0.0,
                                     dot_cleanse_share_buildup=share_buildup)
            r = duel(a, Loadout("Haze", ["Rapid Rounds", "Swift Striker", "Dispel Magic"], souls=25000, skill=sk))
            return r.a_dmg.get("Afterburn", 0.0) / r.time   # per second: the two duels can end at different times
        self.assertLess(burn(1.0), 0.9 * burn(0.0))


def own_dot_taken(hero, items, source, share):
    a = Loadout(hero, items, souls=20000, skill=hero_default_skill(hero, badge=91, counterplay=True))
    sk = dataclasses.replace(hero_default_skill("Haze", badge=91, counterplay=True), dot_cleanse_share=share,
                             dot_cleanse_delay=0.5)
    return duel(a, Loadout("Haze", ["Rapid Rounds", "Swift Striker", "Dispel Magic"], souls=20000,
                           skill=sk)).a_dmg.get(source, 0.0)


class SelfTickingDots(unittest.TestCase):
    def test_crow_bleed_and_scarabs_purged(self):
        for hero, src in (("Vindicta", "Crow Familiar"), ("Mirage", "Fire Scarabs")):
            items = ["Extra Spirit", "Mystic Burst", "Rapid Rounds"]
            never, always = own_dot_taken(hero, items, src, 0.0), own_dot_taken(hero, items, src, 1.0)
            self.assertGreater(never, 0.0, hero)
            self.assertLess(always, never, hero)


class CounterspellUlt(unittest.TestCase):
    def test_ult_rate_blocks_death_slam(self):
        def slam(rate_ult):
            a = Loadout("Lash", ["Extra Spirit", "Mystic Burst"], souls=20000,
                        skill=hero_default_skill("Lash", badge=91, counterplay=True))
            sk = dataclasses.replace(hero_default_skill("Haze", badge=91, counterplay=True), spell_parry_rate=0.0,
                                     spell_parry_rate_ult=rate_ult)
            r = duel(a, Loadout("Haze", ["Rapid Rounds", "Counterspell"], souls=20000, skill=sk))
            return r.a_dmg.get("Death Slam", 0.0)
        self.assertGreater(slam(0.0), 0.0)
        self.assertLess(slam(1.0), 0.6 * slam(0.0))   # later slams can come while it is on cooldown

    def test_ult_falls_back_to_rate(self):
        # spell_parry_rate_ult None: ultimates use spell_parry_rate (same fight as setting both to it)
        a = Loadout("Lash", ["Extra Spirit", "Mystic Burst"], souls=20000,
                    skill=hero_default_skill("Lash", badge=91, counterplay=True))

        def taken(rate, rate_ult):
            sk = dataclasses.replace(hero_default_skill("Haze", badge=91, counterplay=True), spell_parry_rate=rate,
                                     spell_parry_rate_ult=rate_ult)
            return duel(a, Loadout("Haze", ["Rapid Rounds", "Counterspell"], souls=20000, skill=sk)).a_dmg
        self.assertEqual(taken(0.0, None), taken(0.0, 0.0))
        self.assertEqual(taken(1.0, None), taken(1.0, 1.0))

    def test_fitted_rates_loaded(self):
        from deadsim.accuracy import spell_parry_rates
        r, u = spell_parry_rates(91)
        self.assertTrue(0.0 <= r <= 0.05 and 0.0 <= u <= 0.05, (r, u))   # real holders block ~nothing
        sk = hero_default_skill("Haze", badge=91)
        self.assertEqual((sk.spell_parry_rate, sk.spell_parry_rate_ult), (r, u))

if __name__ == "__main__":
    unittest.main()
