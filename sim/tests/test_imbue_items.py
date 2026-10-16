"""Imbue item effects checked against replay measurements. Run from sim/:
    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill  # noqa: E402
from deadsim.engine import Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402


def pair(items, hero="Wraith"):
    e = Engine(distance=10, max_time=5)
    f = make_fighter(e, Loadout(hero, items, souls=20000, skill=Skill(use_actives=False)))
    g = make_fighter(e, Loadout("Abrams", [], souls=20000))
    f.enemy, g.enemy = g, f
    for s in f.abilities + g.abilities:
        s.start()
    for x in f.items_fx:
        if hasattr(x, "on_start"):
            x.on_start(f)
    return e, f, g


class TestMercurialMagnum(unittest.TestCase):
    def test_bullet_bonus_is_percent_of_base_bullet_damage(self):
        """Replays: each proc is ~0.4-0.55 x the hero's base bullet damage (Wraith median 4), not flat 20+."""
        e, f, g = pair(["Mercurial Magnum"])
        fx = next(x for x in f.items_fx if x.name == "Mercurial Magnum")
        f.mods.add("mercurial", 1, 1e9, "test")
        e.damage(f, g, f.st.bullet_damage * 3, "bullet", "gun", hits=3)
        pct = fx.v("BulletsBonusMagicDamage") / 100
        self.assertLess(pct, 1.0)
        got = f.dmg_out["Mercurial Magnum"]
        self.assertGreater(got, 0)
        self.assertLessEqual(got, f.st.bullet_damage * pct * 3 * 1.5)
        self.assertLess(got / 3, 10)        # per bullet, Wraith: real median 4 (was ~40 with the flat value)


class TestMysticReverb(unittest.TestCase):
    def test_imbued_lifesteal_heals_on_the_hit(self):
        e, f, g = pair(["Mystic Reverb"], hero="Paradox")
        ab = next(s for s in f.abilities if any(i.name == "Mystic Reverb" for i in s.imbues))
        f.hp = f.max_hp * 0.5
        before = f.hp
        amt = e.damage(f, g, 200, "spirit", ab.ab.name, is_ability=True, ability=ab)
        ls = f.st.spirit_lifesteal + 0.22
        self.assertAlmostEqual(f.hp - before, amt * ls, delta=amt * 0.02)


if __name__ == "__main__":
    unittest.main()
