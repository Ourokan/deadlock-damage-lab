"""Quick end-to-end check that the searches still run on the current sim: python3 pipeline/smoke_test.py

One duel from the duel search, one dummy damage test and one tank survival fight, plus a check that every hero's fight
pattern (sim/data/fight_patterns.json) names abilities it still has, the overall score's movement weights and that the counter items are still in the shop. Fails if any of them raises or returns nothing. Runs in CI on every pull request (.github/workflows/pr-tests.yml).
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

# every hero both ways in the survival fight the overall, counter and survival searches run (its immortal refill sits
# in items_fx without an item; Violet crashed on it and rerun 73 lost every overall job, 2026-10-25), bare and with
# every lifesteal item on both sides: lifesteal heals pass engine.heal's origin=, and Nurse Harrow's Wretched Vapors
# heal hook didn't take it, which failed rerun 78's publish (2026-10-25)
_LS = ["Spirit Lifesteal", "Bullet Lifesteal", "Melee Lifesteal"]
for hid in G.heroes:
    _n = G.hero(hid).name
    for _a, _b in ((_n, "Abrams"), ("Abrams", _n)):
        for _it in ([], _LS):
            assert survive(_a, _it, 20000, _b, _it, max_time=10.0)["time_alive"] > 0, (_a, _b, _it)
print("every hero in a survival fight ok")

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
m = ev._map(pop[2:])   # fewer items, less max health: more heal trips (map_time values: sim/tests/test_lane.py)
assert ev._map(pop) == 1.0 and 0.7 < m < 1.0, m
assert ev._map(pop + [ids["Radiant Regeneration"]]) > 1.0
want = m / O.movement_value(pop)   # same damage: only movement and heal trips differ
assert abs(ev.run(pop) - 1.0) < 1e-9 and abs(ev.run(pop[2:]) - want) < 1e-9, ev.run(pop)


class _Ev4(_Ev):   # 4x the damage with one more item
    def _rows(self, items, pool):
        return [(1, 1.0, 900.0 * (4 if len(items) > 3 else 1), 12.0, False)]


# damage elasticity: the score counts the damage ratio ^ DAMAGE_ELASTICITY, the other factors in full
more = pop + [ids["Extra Health"]]
_e = O.DAMAGE_ELASTICITY
try:
    O.DAMAGE_ELASTICITY = 1.0
    full = _Ev4(1, 18000, {}).run(more)
    O.DAMAGE_ELASTICITY = 0.5
    assert abs(_Ev4(1, 18000, {}).run(more) - full / 2) < 1e-9, (full, _Ev4(1, 18000, {}).run(more))
finally:
    O.DAMAGE_ELASTICITY = _e


class _EvNeg(_Ev):   # damage net of the enemy's healing below 0: a real score of 0, not a complex number
    def _rows(self, items, pool):
        return [(1, 1.0, 900.0 if len(items) <= 3 else -50.0, 12.0, False)]


assert _EvNeg(1, 18000, {}).run(more) == 0.0
S.popular_build = _popular
# real win-edge blend (overall_search.win_value): neutral without items, movement items left out, capped per item
haze = G.hero("Haze").id
assert O.win_value([], haze) == 1.0 and O.win_value([ids["Stalker"]], haze) == 1.0
assert O.win_value([ids["Decay"]], haze) < 1.0, O.win_value([ids["Decay"]], haze)
assert all(abs(v) <= O.WIN_CAP for row in O._win.values() for v in row.values())
# real death rate (overall_search.death_rate_value): the static fit's item names must still exist in the game
_fr = O.fight_rate_data()
missing = sorted({n for t in _fr["items"].values() for n in t["items"] if n not in ids})
assert not missing, f"fight_rate.json names items the game no longer has (refit sim/scripts/fight_rate): {missing}"
assert O.death_rate_value([ids["Cheat Death"]], haze, 27000) > 1.0
print("movement weights ok: Stalker", round(st, 4), "four top items", round(O.movement_value(top), 4))

# what changed between reruns (pipeline/changes.py): items in/out per hero and net worth, small moves dropped
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import changes as C  # noqa: E402
_b = lambda items, dbd, d15: {"best": {"items": items, "damage_before_death": dbd}, "damage_best": {"items": items, "dummy_15s": d15}}
_old = {"heroes": {"13": {"name": "Haze", "brackets": {"phantom": {"18000": _b([1, 2, 3], 1000, 2000), "27000": _b([4, 5], 1000, 2000)}}}}}
_new = {"heroes": {"13": {"name": "Haze", "brackets": {"phantom": {"18000": _b([1, 2, 6], 1100, 2010), "27000": _b([4, 5], 1020, 2400)}}}}}
rows, total = C.build_rows(_old, _new, "phantom")
assert total == 4, total
got = {(r["souls"], r["kind"]): r for r in rows}
assert set(got) == {(18000, "overall"), (18000, "damage"), (27000, "damage")}, got   # 27k overall moved only 2%
assert got[(18000, "overall")]["in"] == [6] and got[(18000, "overall")]["out"] == [3] and got[(18000, "overall")]["kept"] == [1, 2]
assert got[(27000, "damage")]["in"] == [] and got[(27000, "damage")]["new"] == 2400
assert C.build_rows(_old, _new, "ascendant") == ([], 0)
# model causes come from the commits the results were built from, not the rerun commits: the 05:38 rerun of
# 2026-10-27 was built from #145's code, so #146/#147/#149 (merged while it ran) are pending, not causes
if C.built("648862c") and C.built("71eae46"):
    _e = C.entry("71eae46", "648862c", "71eae46", "648862c", "phantom", "forced")
    assert [c["pr"] for c in _e["causes"] if c["kind"] == "model"] == [145], _e["causes"]
    assert [m["pr"] for m in _e["pending"]] == [146, 147, 149], _e.get("pending")
print("changes ok")

# real win edge refresh after a patch (pipeline/refresh_win_edge.py): counts the patch window's day files, rebuilds the
# edges with enough Ritualist+ matches and keeps the last snapshot otherwise
import gzip  # noqa: E402
import math  # noqa: E402
import shutil  # noqa: E402
import tempfile  # noqa: E402
import refresh_win_edge as RW  # noqa: E402

_tmp = tempfile.mkdtemp()
_items = sorted(i for i in RW.W.TARGET if RW.W.TIER[i] == 1 and RW.W.SLOT[i] == "weapon")[:2]
_day = RW.P.build_days()[0]
with gzip.open(os.path.join(_tmp, f"{_day}.jsonl.gz"), "wt") as _f:
    for m, badge in ((1, 85), (2, 85), (3, 40)):   # two Ritualist+ matches, one below
        for p in range(12):
            _f.write(json.dumps({"match_id": m, "account_id": p, "hero_id": 1 + p % 6, "won": p < 6, "badge": badge,
                                 "purchases": [[_items[p % 2], 300, 0]]}) + "\n")
_paths = RW.partials(_tmp, os.path.join(_tmp, "work"), RW.P.build_days(), 1)
assert len(_paths) == 1 and RW.ritualist_matches(_paths) == 2, RW.ritualist_matches(_paths)
RW.B.EDGE_PATH = os.path.join(_tmp, "edge.json")
with open(RW.B.EDGE_PATH, "w") as _f:
    json.dump({"meta": {"patch": "old"}, "heroes": {}}, _f)
_argv = sys.argv
sys.argv = ["refresh_win_edge.py", _tmp, "--work", os.path.join(_tmp, "work"), "--min-matches", "3"]
RW.main()
assert json.load(open(RW.B.EDGE_PATH))["meta"]["patch"] == "old"   # too few matches: snapshot kept
sys.argv[-1] = "2"
RW.main()
_m = json.load(open(RW.B.EDGE_PATH))
assert _m["meta"]["patch"] == RW.P.load()["patch"] and _m["meta"]["matches"] == 2, _m["meta"]
sys.argv = _argv
shutil.rmtree(_tmp)
assert "rare_pick" in _m["meta"], _m["meta"]   # hero_edges -> write_edges carries the fit
# rare-pick prior (build_win_check.rarity_fit): items seldom bought that lose more give a negative slope per decade,
# and a spread that grows with rarity
_cells = [{"raw": -0.01 * r + 0.01 * r * (k % 3 - 1), "raw_se": 0.005, "prior0": 0.0, "rare": r}
          for k in range(60) for r in (0.0, 0.5, 1.0, 2.0)]
_fit = RW.B.rarity_fit(_cells)
assert abs(_fit["beta"] + 0.01) < 1e-3 and _fit["tau2_rare"] > 0, _fit
assert RW.B.rarity_fit([]) == {"beta": 0.0, "tau2": RW.B.TAU ** 2, "tau2_rare": 0.0}
# hero_edges end to end on a tiny ev: two same-slot same-tier items on one hero, 90% / 10% of the buys
_a, _b = _items
_ev = {(_a, 1, 300, 0, 0): [900, 450], (_b, 1, 300, 0, 0): [100, 60]}
_h, _f = RW.B.hero_edges(_ev, {"beta": -0.01, "tau2": RW.B.TAU ** 2, "tau2_rare": 0.0})
assert abs(_h[1][_a]["share"] - 0.9) < 1e-9 and abs(_h[1][_b]["share"] - 0.1) < 1e-9, _h
_tmp = tempfile.mkdtemp()
RW.B.write_edges(_h, os.path.join(_tmp, "e.json"), fit=RW.B.rarity_fit([]))
assert json.load(open(os.path.join(_tmp, "e.json")))["meta"]["rare_pick"]["knee_share"] == RW.B.SHARE_KNEE
# the blend's bands (overall_search.win_value): a loss at 1.5 se counts, a gain at 1.5 se does not
_hz = str(G.hero("Haze").id)
with open(os.path.join(_tmp, "w.json"), "w") as _f:
    json.dump({"meta": {"patch": RW.P.load()["patch"]},
               "heroes": {_hz: {str(ids["Decay"]): [-1.5, 1.0, 100, -1.5], str(ids["Mystic Shot"]): [1.5, 1.0, 100, 1.5]}}}, _f)
_we, O.WIN_EDGE, O._win = O.WIN_EDGE, os.path.join(_tmp, "w.json"), None
assert abs(O.win_value([ids["Decay"]], int(_hz)) - math.exp(-1.5 * O.WIN_K)) < 1e-9
assert O.win_value([ids["Mystic Shot"]], int(_hz)) == 1.0
O.WIN_EDGE, O._win = _we, None
shutil.rmtree(_tmp)
print("win edge refresh ok")

# the counter items the Phantom+ rerun scores (counters/scripts/sim_counters.py) are all still in the shop
sys.path.insert(0, os.path.join(ROOT, "counters", "scripts"))
import sim_counters  # noqa: E402
missing = [n for n in sim_counters.OPTIONS if n not in {it.name for it in G.items.values()}]
assert not missing, f"counter items no longer in the shop: {missing}"
print("counter items ok:", len(sim_counters.OPTIONS))

# the rerun's job split (pipeline/run_shard.py): every job on exactly one machine, a job and the jobs it reads on the
# same one, and every step's per-job command takes the hero and budget it was planned for
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import run_shard as RS  # noqa: E402
import unit_costs as UC  # noqa: E402
_ids = sorted(G.heroes)
_tanks = set(_ids[:10])
_groups = RS.plan(RS.PRIMARY, _ids, RS.BUDGETS, UC.Costs(RS.PRIMARY), _tanks)
_shards, _est = RS.split(_groups, 16, 4)
_where = {id(u): i for i, s in enumerate(_shards) for u in s}
_all = [u for g in _groups for u in g]
assert len(_where) == len(_all) == sum(len(s) for s in _shards), (len(_where), len(_all))
assert all(_where[id(d)] == _where[id(u)] for u in _all for d in u.deps)
_n = {s: sum(u.step == s for u in _all) for s in UC.STEPS}
_nb = len(RS.BUDGETS)
assert _n == {"damage": len(_ids) * _nb, "buy_order": len(_ids), "skill_order": len(_ids), "duel": len(_ids) * _nb,
              "survival": 10 * _nb, "overall": len(_ids) * _nb, "counters": len(_ids) * len(RS.COUNTER_BUDGETS),
              "path": len(_ids)}, _n
assert all(str(u.hero) in u.cmd and (u.budget is None or str(u.budget) in u.cmd) for u in _all)
print(f"rerun split ok: {len(_all)} jobs on 16 machines, slowest about {max(_est) / 60:.0f} min")

# the shard scheduler: a job starts only after the jobs it reads, a failing job gets one retry, and a job that still
# fails is reported without holding back the jobs waiting on it
_tmp = tempfile.mkdtemp()
_log = os.path.join(_tmp, "log")


def _u(name, code):
    u = RS.Unit(name, name, 1, None, [sys.executable, "-c", f"open({_log!r}, 'a').write({name!r} + '\\n'); {code}"], 1)
    return u


_a, _b, _c = _u("a", "pass"), _u("b", "raise SystemExit(1)"), _u("c", "pass")
_c.deps = [_a, _b]
for _x in (_a, _b, _c):
    _x.after = [_c] if _x is not _c else []
    RS.chain(_x)
_secs, _failed = RS.run([_c, _b, _a], 2)
_order = open(_log).read().split()
assert _failed == [_b] and _order.count("b") == 2 and _order[-1] == "c" and set(_secs) == {_a, _b, _c}, (_order, _failed)
shutil.rmtree(_tmp)
print("rerun scheduler ok")

# check_patch.pending_request: a rerun request newer than the results reruns once, for 2 days, and never crashes
import datetime  # noqa: E402
import check_patch as CP  # noqa: E402
_tmp = tempfile.mkdtemp()
CP.REQUEST, _req = os.path.join(_tmp, "rerun_request.json"), CP.REQUEST
_now = datetime.datetime(2026, 10, 24, 19, 0, tzinfo=datetime.timezone.utc)
_st = {"results_built": "2026-10-24T15:00:00Z"}
assert CP.pending_request(_st, _now) is None   # no file
open(CP.REQUEST, "w").write("{not json")
assert CP.pending_request(_st, _now) is None   # malformed
json.dump({"requested_at": "2026-10-24T18:30:00Z", "reason": "fix"}, open(CP.REQUEST, "w"))
assert CP.pending_request(_st, _now) == "fix"   # newer than the results
assert CP.pending_request({"results_built": "2026-10-24T18:45:00Z"}, _now) is None   # already rerun
assert CP.pending_request({}, _now) is None   # results never built
assert CP.pending_request(_st, _now + datetime.timedelta(days=2, hours=1)) is None   # over 2 days old
_state = {"patch": "09-29-2026", "patch_start": "2026-09-30", "builds_through": "2026-10-23", "game_hash": "h",
          "standard": RS.PRIMARY}
_today = datetime.date(2026, 10, 24)
assert CP.decide(_state, "h", [], _today, request="fix")[:2] == ("rerun", "rerun requested: fix")
assert CP.decide(_state, "h", [], _today)[0] == "none"
assert CP.decide(_state, "h", [{"title": "10-23-2026 Update"}], _today, request="fix")[0] == "wait"   # new patch waits
CP.REQUEST = _req
shutil.rmtree(_tmp)
print("rerun request ok")

# the patch rerun's team value refit: one machine per ally item, and the merged parts write the file one full run writes
sys.path.insert(0, os.path.join(ROOT, "sim", "scripts", "team"))
import team_value as TV  # noqa: E402
import re  # noqa: E402
with open(os.path.join(ROOT, ".github", "workflows", "patch-rerun.yml")) as _f:
    _wf = _f.read()
_parts = json.loads(re.search(r"^\s+part: (\[[\d, ]*\])", _wf, re.M).group(1))   # the team job's matrix
assert _parts == list(range(len(TV.ALLY_ITEMS))), (_parts, len(TV.ALLY_ITEMS))
assert re.findall(r"--part [^\n]*? --of (\d+)", _wf) == [str(len(TV.ALLY_ITEMS))], "team job --of != ALLY_ITEMS"
_tmp = tempfile.mkdtemp()
_out, TV.OUT = TV.OUT, os.path.join(_tmp, "team_value.json")
_res = {i: {"10000": {"value": k / 10, "se": 0.01, "swing_on": 1.0, "swing_off": 0.5, "holder_damage": 9.0,
                      "fights": 8}} for k, i in enumerate(TV.ALLY_ITEMS)}
shutil.copy(_out, TV.OUT)
TV.write(_res)
_full = open(TV.OUT).read()
shutil.copy(_out, TV.OUT)
os.makedirs(os.path.join(_tmp, "parts"))
_items = list(TV.ALLY_ITEMS)
for _k in range(3):
    json.dump({i: _res[i] for i in _items[_k::3]}, open(os.path.join(_tmp, "parts", f"part_{_k}.json"), "w"))
open(os.path.join(_tmp, "parts", "notes.txt"), "w").write("not a part")
TV.merge(os.path.join(_tmp, "parts"))
assert open(TV.OUT).read() == _full, "merged team values differ from one full run's"
os.remove(os.path.join(_tmp, "parts", "part_0.json"))
shutil.copy(_out, TV.OUT)
for _missing in (os.path.join(_tmp, "parts"), os.path.join(_tmp, "none")):
    try:
        TV.merge(_missing)
        raise AssertionError("merge with a missing part wrote the file")
    except SystemExit:
        pass
assert open(TV.OUT).read() == open(_out).read()   # a missing part keeps the last fit
TV.OUT = _out
shutil.rmtree(_tmp)
print("team value parts ok:", len(_parts))

# a rerun's publish lays files built by the run's (older) code over main: the committed game data must be what main's
# normalize_game.py makes of its own raw dump (run 67 put back a data/game without Violet and Baba on 2026-10-25)
import subprocess  # noqa: E402
import publish_guard as PG  # noqa: E402
_tmp = tempfile.mkdtemp()
shutil.copytree(os.path.join(ROOT, "data", "game"), os.path.join(_tmp, "data", "game"))
shutil.copytree(os.path.join(ROOT, "data", "scripts"), os.path.join(_tmp, "data", "scripts"))
shutil.copytree(os.path.join(ROOT, "sim", "deadsim", "heroes"), os.path.join(_tmp, "sim", "deadsim", "heroes"))
PG.rebuild_game(_tmp)
for _f in ("heroes.json", "abilities.json", "weapons.json", "shop_items.json"):
    assert open(os.path.join(_tmp, "data", "game", _f)).read() == open(os.path.join(ROOT, "data", "game", _f)).read(), \
        f"data/game/{_f} isn't what normalize_game.py makes of data/game/raw: rebuild it (pipeline/publish_guard.py)"
shutil.rmtree(_tmp)
print("game data matches the normalizer ok")


# publish_guard.keep_newer and check_patch.request_in on a scratch repo: main refit a fit while the run ran, and a
# rerun request merged after the run took its code
def _git(*a):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=_tmp, check=True,
                          capture_output=True, text=True).stdout.strip()


def _put(path, text):
    os.makedirs(os.path.dirname(os.path.join(_tmp, path)), exist_ok=True)
    open(os.path.join(_tmp, path), "w").write(text)


_tmp = tempfile.mkdtemp()
_git("init", "-q")
for _p in ("fit.json", "code/fit.py", "other.json", "agg/a.json", "pipeline/rerun_request.json"):
    _put(_p, "v1")
_git("add", "-A")
_git("commit", "-qm", "start")
_built = _git("rev-parse", "HEAD")
_put("fit.json", "main refit")
_put("agg/a.json", "v1 ")   # its producer didn't change, but the file did
_put("pipeline/rerun_request.json", "v2")
_git("commit", "-qam", "main moves on")
_put("other.json", "last run")
_git("commit", "-qam", "Rerun searches (phantom): forced")   # a rerun's own results don't count as main's refit
_guard = {"fit.json": ["code"], "other.json": ["code"], "agg": ["code"]}
for _p, _t in (("fit.json", "run"), ("other.json", "run"), ("agg/a.json", "run"), ("agg/new.json", "run")):
    _put(_p, _t)   # the run's artifact laid over main
_kept = PG.keep_newer(_built, _tmp, _guard)
assert set(_kept) == {"fit.json", "agg"}, _kept
assert open(os.path.join(_tmp, "fit.json")).read() == "main refit" and open(os.path.join(_tmp, "agg/a.json")).read() == "v1 "
assert not os.path.exists(os.path.join(_tmp, "agg/new.json"))
assert open(os.path.join(_tmp, "other.json")).read() == "run"   # unchanged on main: the run's copy is published
assert set(PG.keep_newer("0" * 40, _tmp, {"other.json": []})) == {"other.json"}   # unknown commit: keep main's
assert PG.changed_since(_git("rev-parse", "HEAD"), ["fit.json"], _tmp) == []
_req = CP.REQUEST
CP.REQUEST = os.path.join(_tmp, "pipeline", "rerun_request.json")
assert CP.request_in(_built, _tmp) is False and CP.request_in(_git("rev-parse", "HEAD"), _tmp) is True
assert CP.request_in("0" * 40, _tmp) is None
CP.REQUEST = _req
shutil.rmtree(_tmp)
print("publish guard ok")

# the item sheet's swaps (search.item_swaps): same slot first, then closest cost; an alternative that doesn't fit
# the budget or would drop another item is skipped, and an item with no fitting alternative gets no swap
class _Ev:
    def run(self, items, pool, detail=False):
        return {"score": len(items), "matchups": {}}


_n = {it.name: i for i, it in G.items.items()}
_lim = S.BRACKET, S.caps_for_limit
S.caps_for_limit = lambda *a: {}
_best = [_n["Spirit Lifesteal"], _n["Headhunter"]]
_pop = [_n["Enduring Speed"], _n["Extra Health"], _n["Boundless Spirit"]]
_sw = S.item_swaps(_Ev(), _best, _pop, S.cost(_best))
assert G.items[_sw[str(_n["Spirit Lifesteal"])]["alt"]].slot == G.items[_n["Spirit Lifesteal"]].slot, _sw
assert "matchups" not in _sw[str(_n["Spirit Lifesteal"])]["F"], _sw
assert all(S.valid([x for x in _best if str(x) != k] + [v["alt"]], S.cost(_best)) for k, v in _sw.items()), _sw
assert S.item_swaps(_Ev(), _best, [_n["Boundless Spirit"]], S.cost(_best)) == {}   # too dear for either slot
S.caps_for_limit = _lim[1]
print("item swaps ok:", len(_sw))

# items.json stats_only (export.item_meta): stat-only passives are, items with effect code or actives are not
import export as EX  # noqa: E402
_m = {v["name"]: v for v in EX.item_meta(G).values()}
assert _m["Spirit Lifesteal"]["stats_only"] and _m["Extra Health"]["stats_only"], (_m["Spirit Lifesteal"], _m["Extra Health"])
assert not _m["Slowing Hex"]["stats_only"] and not _m["Headhunter"]["stats_only"]
print("item meta ok")
