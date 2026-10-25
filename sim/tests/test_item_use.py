"""Checks of the real use share of non-damage active items (deadsim engine.unused_items, Skill.item_use,
sim/data/item_use.json): in realistic fights with a fight_phase an item is left unused in 1 - share of the fights.
Run from sim/: python3 -m unittest discover -s tests"""
import dataclasses
import json
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "survival")]

from deadsim import accuracy, items_fx  # noqa: E402
from deadsim.engine import Skill, unused_items  # noqa: E402

with open(os.path.join(ROOT, "sim", "data", "item_use.json")) as _fh:
    USE = json.load(_fh)["items"]


class _Item:
    def __init__(self, name):
        self.name = name


class _FX:
    def __init__(self, name):
        self.item = _Item(name)
        self.ready_at = 0.0


class _F:
    def __init__(self, names, use, phase):
        self.items_fx = [_FX(n) for n in names]
        self.skill = Skill(item_use=use, fight_phase=phase)


class ItemUse(unittest.TestCase):
    def test_file_is_sane(self):
        self.assertIn("Knockdown", USE)
        for n, r in USE.items():
            self.assertTrue(0.0 < r["factor"] <= 1.0, n)
            self.assertGreater(r["holders"], 0, n)
            self.assertLessEqual(abs(r["factor"] - 1), abs(min(1.0, r["raw"]) - 1) + 1e-9, n)

    def test_share_of_spread_fights(self):
        # over spread fight phases the item is used in about its share of the fights
        n = 400
        used = 0
        for k in range(n):
            f = _F(["Knockdown", "Extra Health"], {"Knockdown": 0.4}, ((k + 1) * 0.6180339887) % 1.0)
            unused_items(f)
            used += f.items_fx[0].ready_at == 0.0
            self.assertEqual(f.items_fx[1].ready_at, 0.0)   # items without a share are untouched
        self.assertAlmostEqual(used / n, 0.4, delta=0.02)

    def test_no_phase_or_no_share_keeps_items(self):
        f = _F(["Knockdown"], {}, 0.3)
        unused_items(f)
        self.assertEqual(f.items_fx[0].ready_at, 0.0)

    def test_realistic_skill_loads_shares(self):
        sk = accuracy.hero_default_skill("Haze", counterplay=True)
        self.assertEqual(sk.item_use, {n: r["factor"] for n, r in USE.items() if r["factor"] < 1.0})
        self.assertEqual(accuracy.hero_default_skill("Haze").item_use, {})
        was = accuracy.ITEM_USE
        accuracy.ITEM_USE = False
        try:
            self.assertEqual(accuracy.hero_default_skill("Haze", counterplay=True).item_use, {})
        finally:
            accuracy.ITEM_USE = was

    def test_unused_item_is_never_cast(self):
        import overall_search as O
        import search as S
        O._phases()
        g = S.G()
        h, oh = g.hero("Haze").id, g.hero("Abrams").id
        kd = next(i for i, it in g.items.items() if it.name == "Knockdown")
        casts = []
        orig = items_fx.FX.use

        def use(self, *a, **k):
            if self.name == "Knockdown" and self.f.name == "me":
                casts.append(self.f.e.t)
            return orig(self, *a, **k)
        items_fx.FX.use = use
        sk = O.skill(h)
        try:
            for share in (1.0, 0.0):
                O._sk[h] = dataclasses.replace(sk, item_use={"Knockdown": share})
                casts.clear()
                O.fight(h, [kd], oh, [], 27000, phase=0.3)
                (self.assertTrue if share else self.assertFalse)(casts, share)
        finally:
            items_fx.FX.use = orig
            O._sk[h] = sk


if __name__ == "__main__":
    unittest.main()
