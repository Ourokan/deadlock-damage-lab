"""Paige's lane terms: Bookwyrm burn from replays (Mechanics.bookwyrm_burn) and landed share by phase
(Mechanics.landing_phase, data/landing_phase.json)."""
import dataclasses
import json
import math
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from deadsim import Loadout, Skill, duel  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
from deadsim.mechanics import DEFAULT as MECH, landing_phase_mult  # noqa: E402

load_heroes()
from deadsim.heroes.bookworm import burn_uptime  # noqa: E402

LAND = json.load(open(os.path.join(ROOT, "data", "landing_phase.json")))
BURN = json.load(open(os.path.join(ROOT, "data", "bookwyrm_burn.json")))
CR = "ability_bookworm_aoemagic"


def bookwyrm_dmg(souls, **mech):
    sk = Skill(accuracy=0.0, ability_landing={"Bookwyrm": 1.0})
    foe = Loadout("Abrams", [], souls=souls, skill=Skill(accuracy=0.0, use_abilities=False))
    r = duel(Loadout("Paige", [], souls=souls, skill=sk, unlocked=[True, False, False, False]), foe, max_time=6.0,
             mechanics=dataclasses.replace(MECH, cast_timing=False, ability_area_phase=False, **mech))
    return r.a_dmg.get("Bookwyrm", 0.0)


class PaigeLaneTest(unittest.TestCase):
    def test_landing_mult_follows_the_bins(self):
        b = LAND["abilities"][CR]["bins"]
        self.assertAlmostEqual(landing_phase_mult(CR, b[2]["net_worth"]), b[2]["rel"], places=6)
        nw = math.sqrt(b[0]["net_worth"] * b[1]["net_worth"])
        self.assertAlmostEqual(landing_phase_mult(CR, nw), (b[0]["rel"] + b[1]["rel"]) / 2, places=6)
        self.assertAlmostEqual(landing_phase_mult(CR, 10), b[0]["rel"], places=6)
        self.assertEqual(landing_phase_mult("ability_not_there", 5000), 1.0)
        self.assertEqual(landing_phase_mult(CR, None), 1.0)
        self.assertLess(landing_phase_mult(CR, 2000), 1.0)   # lane casts land less than the match average

    def test_burn_uptime_from_file_and_lane_shortest(self):
        b = BURN["bins"]
        self.assertAlmostEqual(burn_uptime(b[1]["net_worth"]), b[1]["uptime"], places=6)
        self.assertLess(burn_uptime(2000), burn_uptime(40000))
        self.assertLess(burn_uptime(40000), 0.5)   # well under the old 0.5 of the flame + linger

    def test_burn_cuts_lane_bookwyrm_more_than_late(self):
        lane = bookwyrm_dmg(3000, landing_phase=False, bookwyrm_burn=True) / bookwyrm_dmg(3000, landing_phase=False,
                                                                                          bookwyrm_burn=False)
        late = bookwyrm_dmg(40000, landing_phase=False, bookwyrm_burn=True) / bookwyrm_dmg(40000, landing_phase=False,
                                                                                           bookwyrm_burn=False)
        self.assertLess(lane, 1.0)
        self.assertLess(lane, late)

    def test_landing_phase_scales_bookwyrm(self):
        souls = 3000
        on = bookwyrm_dmg(souls, landing_phase=True, bookwyrm_burn=False)
        off = bookwyrm_dmg(souls, landing_phase=False, bookwyrm_burn=False)
        self.assertGreater(off, 0.0)
        self.assertAlmostEqual(on / off, landing_phase_mult("ability_bookworm_dragonfire", souls), places=3)

    def test_poke_rows_phase_curve(self):
        from deadsim import mechanics as M, game
        h = game().hero("Paige")
        old = M._POKES
        try:
            M._POKES = {h.id: {CR: (0.4, [(math.log(2500), 0.1), (math.log(37000), 0.9)], False)}}
            self.assertAlmostEqual(M.poke_rows(h, 2500)[CR], 0.1)
            self.assertAlmostEqual(M.poke_rows(h, math.sqrt(2500 * 37000))[CR], 0.5)
            self.assertAlmostEqual(M.poke_rows(h, None)[CR], 0.4)   # pooled without souls
            self.assertFalse(M.poke_procs(h, CR))
            self.assertTrue(M.poke_procs(h, "ability_not_there"))
        finally:
            M._POKES = old

    def test_paradox_carbine_pokes_lower_in_lane_only(self):
        from deadsim import mechanics as M, game
        h = game().hero("Paradox")
        cb = "citadel_ability_chrono_kinetic_carbine"
        old = M._POKES
        try:
            M._POKES = None
            lane, mid, late = (M.poke_rows(h, s)[cb] for s in (2600, 12405, 37000))
            self.assertLess(lane, 0.6 * mid)
            self.assertAlmostEqual(mid, late)          # flat pooled row after lane
            self.assertTrue(M.poke_procs(h, cb))
        finally:
            M._POKES = old

    def test_add_pokes_own_damage_only(self):
        from deadsim import fight, mechanics as M, game
        h = game().hero("Paige")
        me = Loadout("Paige", ["Mystic Burst"], souls=30000)
        foe = Loadout("Abrams", [], souls=30000)
        old = M._POKES
        got = {}
        try:
            for procs in (True, False):
                M._POKES = {h.id: {CR: (1.0, [], procs)}}
                d = {}
                fight.add_pokes(d, {}, me, foe, 15.0, None, MECH)
                got[procs] = d
        finally:
            M._POKES = old
        self.assertGreater(got[True].get("Mystic Burst", 0.0), 0.0)   # the proc rides the poke
        self.assertEqual(set(got[False]), {"Captivating Read"})       # procs false: own damage only
        self.assertAlmostEqual(got[False]["Captivating Read"], got[True]["Captivating Read"], places=6)


if __name__ == "__main__":
    unittest.main()
