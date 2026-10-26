"""Melee hits gain MELEE_WEAPON_SCALE of the weapon damage bonus; Uppercut procs Mystic Burst / Tankbuster (Tankbuster on a flat share of hits); ability
melee hits proc on-melee items (validation/README.md, 2026-10-26). Run from sim/: python3 -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from deadsim import Loadout  # noqa: E402
from deadsim.engine import MELEE_WEAPON_SCALE, Engine, Hit  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def pair(items, foe_items=()):
    e = Engine(distance=3)
    a = make_fighter(e, Loadout("Bebop", list(items), souls=20000))
    b = make_fighter(e, Loadout("Abrams", list(foe_items), souls=20000))
    a.enemy, b.enemy = b, a
    return e, a, b


def slot(f, cls):
    return next(s for s in f.abilities if s.ab.class_name == cls)


def fx(f, cls):
    return next(x for x in f.items_fx if x.item.class_name == cls)


def melee_hit(f, cls, size=200.0, landing=1.0):
    s = slot(f, cls)
    return Hit("melee", s.ab.name, size, size, is_ability=True, ability=s, landing=landing, pre_mit=size)


class MeleeScaling(unittest.TestCase):
    def test_melee_mult_takes_half_the_weapon_bonus(self):
        _, a, _ = pair(["Headshot Booster", "High-Velocity Rounds", "Melee Charge"])
        st = a.st
        self.assertGreater(st.weapon_pct, 0.0)
        self.assertAlmostEqual(a.melee_mult(), 1.0 + st.melee_pct + MELEE_WEAPON_SCALE * st.weapon_pct)

    def test_uppercut_procs_mystic_burst_and_tankbuster_hook_does_not(self):
        for item in ("Mystic Burst", "Tankbuster"):
            for cls, procs in (("citadel_ability_uppercut", True), ("citadel_ability_hook", False)):
                e, a, b = pair([item])
                x = fx(a, "upgrade_magic_burst" if item == "Mystic Burst" else "upgrade_magic_shock")
                hp = b.hp
                for _ in range(10):   # Tankbuster releases on a share of Uppercut hits (bebop.TANKBUSTER_CHANCE)
                    e.t += 14.0
                    x.on_damage_dealt(a, b, melee_hit(a, cls))
                self.assertEqual(b.hp < hp, procs, (item, cls))

    def test_uppercut_releases_tankbuster_on_a_flat_share_of_hits_any_size(self):
        from deadsim.heroes.bebop import TANKBUSTER_CHANCE
        for size in (100.0, 300.0):   # below and above the 165 minimum
            e, a, b = pair(["Tankbuster"])
            x = fx(a, "upgrade_magic_shock")
            n = 0
            for _ in range(200):
                e.t += 14.0
                before = a.dmg_out.get("Tankbuster", 0.0)
                x.on_damage_dealt(a, b, melee_hit(a, "citadel_ability_uppercut", size=size))
                n += a.dmg_out.get("Tankbuster", 0.0) > before
                b.hp = b.max_hp
            self.assertAlmostEqual(n / 200, TANKBUSTER_CHANCE, delta=0.02, msg=size)

    def test_ability_melee_procs_spirit_snatch(self):
        _, a, b = pair(["Spirit Snatch"])
        hp = b.hp
        x = fx(a, "upgrade_spirit_snatch")
        x.on_damage_dealt(a, b, melee_hit(a, "citadel_ability_hook"))
        self.assertLess(b.hp, hp)
        self.assertFalse(x.ready())   # on cooldown after the proc

    def test_heavy_melee_items_ignore_ability_melee(self):
        _, a, b = pair(["Melee Charge"])
        a.counters["melee_heavy"] = True
        hp = b.hp
        fx(a, "upgrade_melee_charge").on_damage_dealt(a, b, melee_hit(a, "citadel_ability_uppercut"))
        self.assertEqual(b.hp, hp)


if __name__ == "__main__":
    unittest.main()
