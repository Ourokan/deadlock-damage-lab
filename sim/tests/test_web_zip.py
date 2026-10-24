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


if __name__ == "__main__":
    unittest.main()
