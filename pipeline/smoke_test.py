"""Quick end-to-end check that the searches still run on the current sim: python3 pipeline/smoke_test.py

One duel from the duel search, one dummy damage test and one tank survival fight, plus a check that every hero's fight
pattern (sim/data/fight_patterns.json) names abilities it still has. Fails if any of them raises or returns nothing. Runs in CI on every pull request (.github/workflows/pr-tests.yml).
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

# every hero has a fight pattern row whose abilities still exist (a patch can rename or add abilities and heroes)
from deadsim import patterns  # noqa: E402
from deadsim.data import game  # noqa: E402
G = game()
for hid in G.heroes:
    row = patterns.pattern(hid)
    assert row is not None, f"no fight_patterns.json row for {G.hero(hid).name}"
    names = {a.class_name for a in G.hero(hid).abilities}
    gone = [c for c in row["order"] + row["ult_after"] + [row["prefight"] or next(iter(names))] + [row.get("imbue") or next(iter(names))]
            if c not in names]
    assert not gone, f"fight_patterns.json: {G.hero(hid).name} lists abilities it no longer has: {gone}"
print("fight patterns ok:", len(G.heroes), "heroes")
