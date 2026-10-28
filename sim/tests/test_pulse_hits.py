"""Paradox's Pulse Grenade pulses (Mechanics.pulse_hits, data/pulse_hits.json): with it a landed throw deals and stacks
fewer pulses and the amp on his other hits is booked under Pulse Grenade. Run: python3 -m unittest discover -s tests -v
(from sim/)."""
import dataclasses
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.mechanics import DEFAULT, pulse_survival  # noqa: E402

AIM = Skill(accuracy=0.4, headshot=0.0, spirit_accuracy=1.0, use_abilities=True, use_actives=False)
FOE = Loadout("Abrams", [], souls=20000, skill=Skill(accuracy=0.3, use_abilities=False))


def pulse(on):
    m = dataclasses.replace(DEFAULT, pulse_hits=on)
    r = duel(Loadout("Paradox", [], souls=20000, skill=AIM), FOE, max_time=8.0, mechanics=m)
    return r.a_dmg


class TestPulseHits(unittest.TestCase):
    def test_survival_falls(self):
        class F:
            pass
        f = F()
        f.e = F()
        f.e.mech = dataclasses.replace(DEFAULT, pulse_hits=True)
        f.st = F()
        f.st.souls = 15000
        s = pulse_survival(f)
        self.assertEqual(s[0], 1.0)
        self.assertTrue(all(a >= b for a, b in zip(s, s[1:])))
        self.assertLess(sum(s[:5]), 3.0)   # ~2 of 5 pulses on the main victim (replays)
        f.e.mech = dataclasses.replace(DEFAULT, pulse_hits=False)
        self.assertIsNone(pulse_survival(f))

    def test_fewer_pulses_and_booked_amp(self):
        off, on = pulse(False), pulse(True)
        self.assertGreater(off["Pulse Grenade"], 0)
        self.assertLess(on["Pulse Grenade"], off["Pulse Grenade"])   # amp booked under it, but fewer pulses
        self.assertLess(on["gun"], off["gun"])   # fewer stacks, and their amp on the gun booked under Pulse Grenade


if __name__ == "__main__":
    unittest.main()
