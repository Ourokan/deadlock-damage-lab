"""Ability pokes beside the duel (Mechanics.pokes, fight.add_pokes, data/ability_pokes.json): Paradox's full-charge
Kinetic Carbine pokes add damage and their item procs, and leave the fight itself alone. Run: python3 -m unittest
discover -s tests -v (from sim/)."""
import dataclasses
import os
import random
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "..", "survival"))

from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.data import game  # noqa: E402
from deadsim.fight import add_pokes  # noqa: E402
from deadsim.heroes import chrono  # noqa: E402
from deadsim.mechanics import DEFAULT, poke_rows, real_length  # noqa: E402

CARBINE = "citadel_ability_chrono_kinetic_carbine"


def mech(pokes=True):
    return dataclasses.replace(DEFAULT, fight_length=real_length(20000), pokes=pokes, range_drift=False)


def paradox(spirit_accuracy=1.0, items=("Tankbuster", "Mystic Shot")):
    aim = Skill(accuracy=0.4, headshot=0.0, spirit_accuracy=spirit_accuracy, use_abilities=True, use_actives=False)
    return Loadout("Paradox", list(items), souls=20000, skill=aim)


HAZE = Loadout("Haze", [], souls=20000, skill=Skill(accuracy=0.3, use_abilities=False))


def pokes(lo, rng=None):
    dmg, exp = {}, {}
    add_pokes(dmg, exp, lo, HAZE, 15.0, rng, mech())
    return dmg, exp


class AbilityPokes(unittest.TestCase):
    def test_rows(self):
        rows = poke_rows(game().hero("Paradox"))
        self.assertGreater(rows[CARBINE], 0.2)
        self.assertEqual(poke_rows(game().hero("Haze")), {})

    def test_pokes_leave_the_fight(self):
        off = duel(paradox(), HAZE, distance=15.0, max_time=20.0, rng=random.Random(3), mechanics=mech(False))
        on = duel(paradox(), HAZE, distance=15.0, max_time=20.0, rng=random.Random(3), mechanics=mech(True))
        self.assertEqual(off.winner, on.winner)
        self.assertGreater(on.a_dmg.get("Tankbuster", 0), off.a_dmg.get("Tankbuster", 0) * 0.9)

    def test_poke_is_k_full_hits_and_fight_hit_is_scaled(self):
        """A poke adds pokes_per_fight full Carbine hits; a cast in the fight is CARBINE_FIGHT_HIT of one."""
        k = poke_rows(game().hero("Paradox"))[CARBINE]
        only = [a.class_name == CARBINE for a in game().hero("Paradox").abilities]
        dmg, exp = pokes(dataclasses.replace(paradox(items=()), unlocked=only))
        self.assertAlmostEqual(dmg["Kinetic Carbine"], exp["Kinetic Carbine"])
        full = dmg["Kinetic Carbine"] / k
        # one fight cast (no gun, no other casts): the same hit x CARBINE_FIGHT_HIT
        lo = paradox(items=())
        only = [a.class_name == CARBINE for a in game().hero("Paradox").abilities]   # no Pulse Grenade amp
        no_gun = dataclasses.replace(lo, skill=dataclasses.replace(lo.skill, accuracy=0.0), unlocked=only)
        r = duel(no_gun, dataclasses.replace(HAZE, skill=Skill(accuracy=0.0, use_abilities=False)), distance=15.0,
                 max_time=3.0, mechanics=dataclasses.replace(mech(), cast_timing=False))
        self.assertAlmostEqual(r.a_dmg["Kinetic Carbine"] - dmg["Kinetic Carbine"],  # duel = fight cast + pokes
                               chrono.CARBINE_FIGHT_HIT * full, delta=0.05 * full)

    def test_poke_scales_with_spirit_accuracy_without_rng(self):
        """rng None (survival.survive): the expected hit, not one all-or-nothing roll."""
        hi, _ = pokes(paradox(1.0))
        lo, _ = pokes(paradox(0.4))
        self.assertGreater(lo["Kinetic Carbine"], 0)
        self.assertAlmostEqual(lo["Kinetic Carbine"], 0.4 * hi["Kinetic Carbine"], delta=0.01 * hi["Kinetic Carbine"])

    def test_survive_adds_own_pokes(self):
        import survival
        kw = dict(max_time=20.0, fight_length=real_length(20000))
        r = survival.survive("Paradox", ["Tankbuster"], 20000, "Haze", [], **kw)
        old = DEFAULT.pokes
        try:
            DEFAULT.pokes = False
            r0 = survival.survive("Paradox", ["Tankbuster"], 20000, "Haze", [], **kw)
        finally:
            DEFAULT.pokes = old
        self.assertGreater(r["damage_dealt"], r0["damage_dealt"])
        self.assertEqual(r["time_alive"], r0["time_alive"])

    def test_no_pokes_without_fight_length(self):
        m = dataclasses.replace(DEFAULT, fight_length=None, range_drift=False)
        r1 = duel(paradox(), HAZE, distance=15.0, max_time=20.0, rng=random.Random(1), mechanics=m)
        r2 = duel(paradox(), HAZE, distance=15.0, max_time=20.0, rng=random.Random(1),
                  mechanics=dataclasses.replace(m, pokes=False))
        self.assertEqual(dict(r1.a_dmg), dict(r2.a_dmg))


if __name__ == "__main__":
    unittest.main()
