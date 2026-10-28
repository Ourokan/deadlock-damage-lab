"""Imbue item effects checked against replay measurements. Run from sim/:
    python3 -m unittest discover -s tests
"""
import heapq
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

    def test_bullet_bonus_outlasts_the_clip(self):
        """Replays: 82% of a Vyper holder's gun hits after the first proc carry the bonus; it lasts the 12 s buff,
        not one clip (his clip lasts 1.7 s)."""
        e, f, g = pair(["Mercurial Magnum"], hero="Vyper")
        fx = next(x for x in f.items_fx if x.name == "Mercurial Magnum")
        ab = next(s for s in f.abilities if any(i.name == "Mercurial Magnum" for i in s.imbues))
        fx.on_cast(f, ab)
        for x in f.items_fx:
            if hasattr(x, "on_reload"):
                x.on_reload(f)
        self.assertTrue(f.mods.active("mercurial"))
        e.t = 11.0
        self.assertTrue(f.mods.active("mercurial"))
        n0 = f.dmg_out.get("Mercurial Magnum", 0.0)
        e.damage(f, g, f.st.bullet_damage, "bullet", "gun", hits=1)
        self.assertGreater(f.dmg_out.get("Mercurial Magnum", 0.0), n0)     # a bullet after the reload still gets it
        e.t = 12.5
        self.assertFalse(f.mods.active("mercurial"))


class TestMysticReverb(unittest.TestCase):
    def test_imbued_lifesteal_heals_on_the_hit(self):
        e, f, g = pair(["Mystic Reverb"], hero="Paradox")
        ab = next(s for s in f.abilities if any(i.name == "Mystic Reverb" for i in s.imbues))
        f.hp = f.max_hp * 0.5
        before = f.hp
        amt = e.damage(f, g, 200, "spirit", ab.ab.name, is_ability=True, ability=ab)
        ls = f.st.spirit_lifesteal + 0.22
        self.assertAlmostEqual(f.hp - before, amt * ls, delta=amt * 0.02)

    def _echo(self, hits, target_hp=None):
        e, f, g = pair(["Mystic Reverb"], hero="Paradox")
        if target_hp is not None:
            g.hp = target_hp
        ab = next(s for s in f.abilities if any(i.name == "Mystic Reverb" for i in s.imbues))
        for raw in hits:
            e.damage(f, g, raw, "spirit", ab.ab.name, is_ability=True, ability=ab)
        hp = g.hp
        e.t = 0.0
        while e.q and e.t < 3.5:
            t, _, fn, args = heapq.heappop(e.q)
            e.t = t
            if getattr(fn, "__name__", "") == "echo":
                fn(*args)
        return f.dmg_out.get("Mystic Reverb", 0.0), hp

    def test_echo_adds_current_health_bonus(self):
        """MaxHealthDamage is the tooltip's "Current Health Bonus Damage": the echo is 50% of the hit + 10% of the
        target's current health (it used to be read as a cap). CURRENT_HEALTH_BONUS False leaves it out (real
        Phantom+ echoes don't scale with the target's health)."""
        from deadsim.items_fx import MysticReverb
        full, hp_full = self._echo([200])
        low, hp_low = self._echo([200], target_hp=1000.0)
        # the 200-damage hit lands the same way on both; only the echo's 10% of current health differs (after resist)
        d = hp_full - hp_low
        self.assertGreater(full - low, 0.05 * d)
        self.assertLessEqual(full - low, 0.1 * d + 1)
        MysticReverb.CURRENT_HEALTH_BONUS = False
        try:
            full, _ = self._echo([200])
            low, _ = self._echo([200], target_hp=1000.0)
        finally:
            MysticReverb.CURRENT_HEALTH_BONUS = True
        self.assertAlmostEqual(full, low)

    def test_small_hits_build_up_to_the_minimum(self):
        """Ticks under MinimumDamage (100) add up until they reach it, so DoT and multi-hit imbues trigger too."""
        self.assertGreater(self._echo([40, 40, 40])[0], 0.0)
        self.assertEqual(self._echo([40])[0], 0.0)

    def test_build_up_expires(self):
        e, f, g = pair(["Mystic Reverb"], hero="Paradox")
        ab = next(s for s in f.abilities if any(i.name == "Mystic Reverb" for i in s.imbues))
        e.damage(f, g, 60, "spirit", ab.ab.name, is_ability=True, ability=ab)
        e.t = 10.0   # past DelayDuration: the next 60 starts a new build-up
        e.damage(f, g, 60, "spirit", ab.ab.name, is_ability=True, ability=ab)
        self.assertTrue(f.items_fx[[type(x).__name__ for x in f.items_fx].index("MysticReverb")].ready())


if __name__ == "__main__":
    unittest.main()


class TestBallisticEnchantment(unittest.TestCase):
    """Mechanics.ballistic_stacks: a stack per unique hero the imbued ability tagged in the last 20 s; a duel has one
    enemy, so an area ability's stack counts as its real heroes tagged (data/ballistic_stacks.json)."""

    def buff(self, hero, flag=True):
        import dataclasses
        from types import SimpleNamespace
        from deadsim import mechanics
        e, f, g = pair(["Ballistic Enchantment"], hero=hero)
        e.mech = dataclasses.replace(e.mech or mechanics.DEFAULT, ballistic_stacks=flag)
        fx = next(x for x in f.items_fx if x.name == "Ballistic Enchantment")
        ab = next(s for s in f.abilities if any(i.name == "Ballistic Enchantment" for i in s.imbues))
        fx.on_damage_dealt(f, g, SimpleNamespace(ability=ab))
        return sum(f.mods.values("weapon_pct")), mechanics.ballistic_stacks(ab.ab.class_name), fx.item

    def test_area_ability_carries_its_real_stacks(self):
        got, stacks, it = self.buff("Lady Geist")
        per = it.p("WeaponPowerPerStack") / 100
        self.assertGreater(stacks, 1.2)
        self.assertAlmostEqual(got, stacks * per, places=6)
        off, _, _ = self.buff("Lady Geist", flag=False)
        self.assertAlmostEqual(off, per, places=6)

    def test_unknown_ability_is_one_stack(self):
        from deadsim import mechanics
        self.assertEqual(mechanics.ballistic_stacks("no_such_ability"), 1.0)
