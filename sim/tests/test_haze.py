"""Haze duel fixes (2026-10-21). Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill, duel, game  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402

G = game()
load_heroes()
GUN_ONLY = Skill(accuracy=1.0, headshot=0.0, use_abilities=False, use_actives=False)


class GunAfterShortenedLock(unittest.TestCase):
    def test_gun_resumes_when_a_lock_is_cut_short(self):
        # a channel locks the gun for 4 s and is interrupted at 0.5 s (Bullet Dance stunned): the gun must
        # fire again right away, not sleep until the old 4 s lock end
        e = Engine(distance=10.0, max_time=3.0, mech=None)
        a = make_fighter(e, Loadout("Haze", [], souls=5000, skill=GUN_ONLY), "A")
        b = make_fighter(e, Loadout("Abrams", [], souls=5000, skill=GUN_ONLY), "B")
        a.gun_locked_until = 4.0

        def cut(f):
            f.gun_locked_until = e.t
        e.at(0.5, cut, a)
        shots = []
        orig = e.fire
        e.fire = lambda f: (shots.append(e.t) if f is a else None, orig(f))[1]
        e.run(a, b, one_way=True)
        self.assertTrue(shots, "gun never fired after the lock was cut")
        self.assertLess(shots[0], 0.5 + 0.11)


class BulletDanceLanding(unittest.TestCase):
    def fight(self, landing):
        sk = Skill(accuracy=0.3, headshot=0.15, use_actives=False,
                   ability_landing={"Bullet Dance": landing}, ability_landing_mech={"Bullet Dance": landing})
        a = Loadout("Haze", [], souls=20000, skill=sk)
        b = Loadout("Abrams", [], souls=20000, skill=Skill(accuracy=0.0, use_abilities=False, use_actives=False,
                                                           melee_rate=0.0))
        return duel(a, b, distance=8.0, max_time=6.0, mechanics=None)

    def test_landing_shortens_the_channel_not_the_bullets(self):
        full, part = self.fight(1.0), self.fight(0.25)
        bd_full, bd_part = full.a_dmg.get("Bullet Dance", 0), part.a_dmg.get("Bullet Dance", 0)
        self.assertGreater(bd_full, 0)
        # about a quarter of the channel's damage
        self.assertAlmostEqual(bd_part / bd_full, 0.25, delta=0.08)
        # the gun gets the rest of the channel back
        self.assertGreater(part.a_dmg.get("gun", 0), full.a_dmg.get("gun", 0))


class SleepWakesOnAnyDamage(unittest.TestCase):
    def sleep_then_dot(self, at):
        """Haze sleeps the target at t=0 (no other damage), then a no-proc DoT tick hits it at `at` s."""
        idle = Skill(accuracy=0.0, use_abilities=False, use_actives=False, melee_rate=0.0)
        e = Engine(distance=10.0, max_time=4.0, mech=None)
        a = make_fighter(e, Loadout("Haze", [], souls=20000, skill=idle), "A")
        b = make_fighter(e, Loadout("Abrams", [], souls=20000, skill=idle), "B")
        dagger = next(ab for ab in a.abilities if ab.ab.name == "Sleep Dagger")
        e.at(0.0, lambda: dagger.cast())
        e.at(at, lambda: e.damage(a, b, 10.0, "spirit", "Alchemical Fire", is_dot=True, is_item=True, procs=False))
        seen = {}
        e.at(at + 0.5, lambda: seen.update(asleep=b.mods.active("stun")))
        e.run(a, b)
        return seen["asleep"]

    def test_dot_tick_wakes_the_target(self):
        self.assertFalse(self.sleep_then_dot(1.0))

    def test_minimum_sleep_time_holds(self):
        # a tick before MinimumSleepTime (0.2 s after the 0.2 s throw) does not wake
        self.assertTrue(self.sleep_then_dot(0.25))


if __name__ == "__main__":
    unittest.main()
