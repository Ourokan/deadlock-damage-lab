"""Quick end-to-end check that the searches still run on the current sim: python3 pipeline/smoke_test.py

One duel from the duel search, one dummy damage test and one tank survival fight. Fails if any of them raises or
returns nothing. Runs in CI on every pull request (.github/workflows/pr-tests.yml).
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, p) for p in ("sim", "search/scripts", "damage/scripts", "survival")]

import search as S  # noqa: E402
import dummy_search as D  # noqa: E402
from survival import survive  # noqa: E402

win, margin, t = S.fight(1, (), 2, (), 15000)
assert 0.0 <= win <= 1.0 and t > 0, (win, margin, t)
print("duel ok:", win, round(margin, 3), round(t, 1))

totals, by_source = D.run_dummy(1, (), 15000, 3000)
assert totals["sustained_30s"] > 0 and by_source, totals
print("dummy ok:", totals)

r = survive("Abrams", [], 20000, "Haze", [])
assert r["time_alive"] > 0 and r["damage_taken"] > 0, r
print("survival ok:", r["time_alive"], r["damage_taken"])
