"""Venator's Ira Domini stakes (2026-10-27): the game books them under their own weapon (citadel_weapon_priest_crossbow),
not the gun, so the sim books them as "Ira Domini (stakes)" with a landing factor of their own and the audit counts
the real crossbow damage as that source; the ult starts fights on cooldown past its real ready share (GATE_READY).
Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from deadsim import Loadout, duel  # noqa: E402
from deadsim import mechanics as M  # noqa: E402
import landing_rates as L  # noqa: E402


class VenatorStakes(unittest.TestCase):
    def test_stakes_not_gun(self):
        r = duel(Loadout("Venator", [], souls=20000), Loadout("Haze", [], souls=20000), max_time=20.0)
        self.assertGreater(r.a_dmg.get("Ira Domini (stakes)", 0), 0)
        self.assertGreater(r.a_dmg.get("gun", 0), 0)

    def test_real_crossbow_is_the_stakes_source(self):
        for name in ("citadel_weapon_priest_crossbow", "citadel_weapon_priest_crossbow_crit"):
            self.assertEqual(L.real_key(name, ["ability_priest_weaponswap"]), "citadel_weapon_priest_crossbow")
        self.assertEqual(L.real_key("citadel_weapon_priest_set_crit", []), "GUN")
        self.assertEqual(L.ALIASES["Ira Domini (stakes)"], "citadel_weapon_priest_crossbow")

    def test_ult_gated_on_readiness(self):
        self.assertIn("65:ability_priest_weaponswap", M.GATE_READY)


if __name__ == "__main__":
    unittest.main()
