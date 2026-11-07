"""Ivy's Kudzu Connection with an ally (2026-11-07, Mechanics.kudzu_connect): the duel's Kudzu fire rate bonus is
0.5 + 0.5 x kudzu_connect of the full value (an ally in range 0.45 of real Ivy combat time)."""
import dataclasses
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from deadsim.heroes import tengu  # noqa: E402
from deadsim.mechanics import DEFAULT  # noqa: E402


class FakeC:
    def __init__(self, share):
        self.engine = type("E", (), {"mech": dataclasses.replace(DEFAULT, kudzu_connect=share)})()
        self.buffs = {}

    def val(self, k):
        return {"BonusFireRate": 20.0, "BulletLifestealPercent": 10.0}[k]

    def buff(self, kind, v, dur, tag=None):
        self.buffs[kind] = v


class KudzuConnect(unittest.TestCase):
    def test_default(self):
        self.assertAlmostEqual(DEFAULT.kudzu_connect, 0.45)

    def test_share_scales_bonus(self):
        for share, f in ((0.0, 0.5), (0.45, 0.725), (1.0, 1.0)):
            c = FakeC(share)
            tengu.KudzuConnection._apply(None, c, 12.0)
            self.assertAlmostEqual(c.buffs["fire_rate"], 0.20 * f)
            self.assertAlmostEqual(c.buffs["bullet_lifesteal"], 0.10 * f)


if __name__ == "__main__":
    unittest.main()
