"""The site's Pyodide bundle (web/build.py build_zip) must hold every data file hero_default_skill reads.
Run from sim/: python3 -m unittest discover -s tests"""
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.join(ROOT, "web"))


class WebZip(unittest.TestCase):
    def test_default_skill_loads_from_bundle(self):
        import build
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "sim.zip")
            build.build_zip(path)
            zipfile.ZipFile(path).extractall(d)
            code = ("import sys; sys.path.insert(0, 'sim'); from deadsim.accuracy import hero_default_skill; "
                    "s = hero_default_skill('Infernus', badge=91, counterplay=True); "
                    "print(s.dot_cleanse_share, s.dot_cleanse_share_buildup, s.spell_parry_rate_ult)")
            r = subprocess.run([sys.executable, "-I", "-c", code], cwd=d, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr[-800:])

    def test_slim_bundle_reads_the_same_game_data(self):
        """build.py drops UI-only keys from raw/items.json and re-serializes the JSON: the sim must read exactly the
        same game data (items, abilities, heroes, raw item properties) from the bundle as from data/game."""
        import build
        code = ("import sys; sys.path.insert(0, 'sim'); from deadsim.data import game; "
                "from deadsim.mechanics import raw_props; from deadsim.heroes.werewolf import _raw, raw_ability; g = game(); "
                "print(repr(sorted(g.items.items()))); print(repr(sorted(g.abilities_by_class.items()))); "
                "print(repr(sorted(g.heroes.items()))); print(repr({c: raw_props(c) for c in sorted(_raw())})); "
                "print(repr({c: raw_ability(c) for c in sorted(_raw()) if c.startswith(('ability', 'citadel_ability'))}))")
        full = subprocess.run([sys.executable, "-I", "-c", code], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(full.returncode, 0, full.stderr[-800:])
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "sim.zip")
            build.build_zip(path)
            zipfile.ZipFile(path).extractall(d)
            slim = subprocess.run([sys.executable, "-I", "-c", code], cwd=d, capture_output=True, text=True)
            self.assertEqual(slim.returncode, 0, slim.stderr[-800:])
        self.assertTrue(full.stdout == slim.stdout, "the bundle's game data differs from data/game")


if __name__ == "__main__":
    unittest.main()
