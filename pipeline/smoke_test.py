"""Quick end-to-end check that the searches still run on the current sim: python3 pipeline/smoke_test.py

One duel from the duel search, one dummy damage test and one tank survival fight, plus a check that every hero's fight
pattern (sim/data/fight_patterns.json) names abilities it still has, and the overall score's movement weights. Fails if any of them raises or returns nothing. Runs in CI on every pull request (.github/workflows/pr-tests.yml).
"""
import json
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

# overall score movement weights (sim/data/movement_value.json): none = 1, duplicates count once, stacks are capped,
# and the popular build still scores exactly 1.0 when it holds movement items
import overall_search as O  # noqa: E402
ids = {it.name: i for i, it in G.items.items()}
with open(O.MOVE_PATH) as f:
    _mv = json.load(f)
missing = [n for n in list(_mv["items"]) + _mv["movement_items"] if n not in ids]
assert not missing, f"movement_value.json names items the game no longer has: {missing}"
assert {"2", "3"} <= set(_mv["stack_cap"]), _mv.get("stack_cap")
assert O.movement_value([]) == 1.0 and O.movement_value([ids["Extra Health"]]) == 1.0
st = O.movement_value([ids["Stalker"]])
assert st > 1.0 and O.movement_value([ids["Stalker"], ids["Stalker"]]) == st, st
top = [ids[n] for n in ("Stalker", "Majestic Leap", "Arcane Surge", "Warp Stone")]
caps = O._move[1]
assert O.movement_value(top) <= caps[max(caps)] and O.movement_value(top[:2]) <= caps[2], O.movement_value(top)
# an unweighted movement item still counts toward the stack: Stalker + Sprint Boots is a 2-item stack
assert O.movement_value([ids["Stalker"], ids["Warp Stone"], ids["Sprint Boots"]]) <= caps[max(caps)]
# hero-only movement items count only for that hero (Mina's Mystic Expansion on Sanguine Retreat)
missing = [n for row in _mv.get("hero_items", {}).values() for n in row if n not in ids]
assert not missing, f"movement_value.json hero_items names items the game no longer has: {missing}"
me = ids["Mystic Expansion"]
assert O.movement_value([me]) == 1.0 and O.movement_value([me], G.hero("Mina").id) > 1.0
assert O.movement_value([ids["Stalker"], ids["Sprint Boots"]]) <= caps[2]
pop = [ids["Stalker"], ids["Warp Stone"], ids["Extra Health"]]
_popular = S.popular_build
S.popular_build = lambda *a: pop


class _Ev(O.Evaluator):
    def _rows(self, items, pool):
        return [(1, 1.0, 900.0, 12.0, False)]


ev = _Ev(1, 18000, {})
assert abs(ev.run(pop) - 1.0) < 1e-9 and abs(ev.run(pop[2:]) - 1.0 / O.movement_value(pop)) < 1e-9, ev.run(pop)
S.popular_build = _popular
print("movement weights ok: Stalker", round(st, 4), "four top items", round(O.movement_value(top), 4))
