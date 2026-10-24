"""Paradox's gun share fixes (2026-10-24): Kinetic Carbine damage grows with level bullet damage and charges for
MaxChargeDuration; Mystic Burst / Tankbuster release what has charged since the last release; Express Shot proc
shots and Escalating Exposure's amp are booked under the item, as the game's damage records do.
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402
from deadsim.mechanics import Mechanics  # noqa: E402


def pair(e, a_hero, a_items, souls=800):
    a = make_fighter(e, Loadout(a_hero, a_items, souls=souls))
    b = make_fighter(e, Loadout("Abrams", [], souls=souls))
    a.enemy, b.enemy = b, a
    return a, b


class MysticBurstCharge(unittest.TestCase):
    def test_release_grows_with_time_since_last(self):
        e = Engine()
        a, b = pair(e, "Infernus", ["Mystic Burst"])
        e.damage(a, b, 120, "spirit", "big", is_ability=True)            # charged before the fight: full 40
        self.assertAlmostEqual(a.dmg_out["Mystic Burst"], 40.0, places=6)
        e.t = 7.0                                                         # half of the 14 s charge
        e.damage(a, b, 120, "spirit", "big", is_ability=True)
        self.assertAlmostEqual(a.dmg_out["Mystic Burst"], 60.0, places=6)
        e.t = 7.0                                                         # nothing charged since
        e.damage(a, b, 120, "spirit", "big", is_ability=True)
        self.assertAlmostEqual(a.dmg_out["Mystic Burst"], 60.0, places=6)
        e.t = 40.0                                                        # capped at a full charge
        e.damage(a, b, 120, "spirit", "big", is_ability=True)
        self.assertAlmostEqual(a.dmg_out["Mystic Burst"], 100.0, places=6)

    def test_tankbuster_release_scales_current_health_and_ignores_resist(self):
        e = Engine()
        a, b = pair(e, "Infernus", ["Tankbuster"], souls=9000)
        b.st.spirit_resist = [0.5]
        hp = b.hp
        e.damage(a, b, 400, "spirit", "big", is_ability=True)
        full = a.dmg_out["Tankbuster"]
        hp_at_release = hp - a.dmg_out["big"]
        self.assertAlmostEqual(full, 40.0 + hp_at_release * 0.075, places=4)   # no 50% resist taken off
        e.t = 3.5                                                         # a quarter of the 14 s charge
        before, big_before = a.dmg_out["Tankbuster"], a.dmg_out["big"]
        hp = b.hp
        e.damage(a, b, 400, "spirit", "big", is_ability=True)
        hp_at_release = hp - (a.dmg_out["big"] - big_before)
        self.assertAlmostEqual(a.dmg_out["Tankbuster"] - before, 0.25 * (40.0 + hp_at_release * 0.075), places=4)


class Booking(unittest.TestCase):
    def test_express_shot_proc_booked_under_item(self):
        aim = Skill(accuracy=1.0, headshot=0.0, use_abilities=False, use_actives=False)
        r = duel(Loadout("Haze", ["Express Shot"], souls=9000, skill=aim),
                 Loadout("Abrams", [], souls=9000, skill=Skill(accuracy=0.0, use_abilities=False)),
                 distance=10.0, max_time=10.0, mechanics=Mechanics(range_drift=False))
        self.assertGreater(r.a_dmg.get("Express Shot", 0), 0, dict(r.a_dmg))
        self.assertGreater(r.a_dmg.get("gun", 0), r.a_dmg["Express Shot"], dict(r.a_dmg))

    def test_escalating_exposure_amp_booked_under_item(self):
        e = Engine()
        a, b = pair(e, "Infernus", ["Escalating Exposure"], souls=9000)
        b.st.spirit_resist = []
        e.damage(a, b, 100, "spirit", "first", is_ability=True)          # adds the first stack after the hit
        amp = b.stat("spirit_amp_taken")
        self.assertGreater(amp, 0)
        e.damage(a, b, 100, "spirit", "second", is_ability=True)
        total = a.dmg_out["second"] + a.dmg_out["Escalating Exposure"]
        self.assertAlmostEqual(a.dmg_out["Escalating Exposure"] / total, amp / (1 + amp), places=6)

    def test_escalating_exposure_amp_gets_its_item_factor_in_realistic_mode(self):
        """Realistic mode scales the booked amp (not the hit) by the item's factor, like an item's own damage."""
        def second_hit(factor):
            e = Engine()
            a, b = pair(e, "Infernus", ["Escalating Exposure"], souls=9000)
            if factor is not None:
                a.skill.item_landing = {"Escalating Exposure": factor}
            b.st.spirit_resist = []
            e.damage(a, b, 100, "spirit", "first", is_ability=True)
            e.damage(a, b, 100, "spirit", "second", is_ability=True)
            return a.dmg_out["second"], a.dmg_out["Escalating Exposure"]
        hit, amp = second_hit(None)
        hit_half, amp_half = second_hit(0.5)
        self.assertAlmostEqual(hit_half, hit, places=6)
        self.assertAlmostEqual(amp_half, amp * 0.5, places=6)


class KineticCarbine(unittest.TestCase):
    def carbine_hit(self, souls):
        aim = Skill(accuracy=0.0, headshot=0.0, spirit_accuracy=1.0, use_abilities=True, use_actives=False)
        r = duel(Loadout("Paradox", [], souls=souls, skill=aim, unlocked=[False, False, True, False]),
                 Loadout("Abrams", [], souls=souls, skill=Skill(accuracy=0.0, use_abilities=False)),
                 distance=10.0, max_time=4.0, mechanics=Mechanics(range_drift=False))
        return r.a_dmg.get("Kinetic Carbine", 0)

    def test_hit_grows_with_level_bullet_damage(self):
        """Replays: a Carbine hit stays 10-17x a gun hit all match (96 at 0-5 min, ~470 at 20-30 min)."""
        early, late = self.carbine_hit(1000), self.carbine_hit(30000)
        self.assertGreater(early, 0)
        self.assertGreater(late / early, 1.4)


if __name__ == "__main__":
    unittest.main()
