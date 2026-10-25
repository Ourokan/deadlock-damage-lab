"""How often real Phantom+ players use their non-damage active items in a fight, against how often the sim does.

The sim casts every active the moment its condition is met (on sight for Rusted Barrel / Disarming Hex / Knockdown,
below half health for Metal Skin...), with every cooldown under 60 s ready at the fight start. Damage actives have a
real-data factor for that (item_landing.json: real item damage / sim item damage holds misses, late casts and
cooldowns spent in the fight before), but items whose effect is a debuff, a buff or a shield have nothing to fit
it on, so the overall score took their full effect in every fight. The build win check found the largest
sim-vs-real gaps among them (Disarming Hex -6.4 win points, Metal Skin -5.8, Rusted Barrel -4.1 while the sim
ranked them average or better in their tier).

real: in the fight-length replays (sim/scripts/fight_length/fetch_fights.py: two enemy heroes trading, gaps < 5 s,
>= 4 hits both ways; a fighter's pair fights that overlap or follow within 5 s are one engagement, since one cast
of a single-target item serves a whole team fight, like the sim's one duel) and their item casts
(fetch_item_casts.py: cooldown starts per owner pawn), for each fighter holding the item at the engagement's start (validation sample buy / sell times, components gone once their upgrade is
bought): did the fighter cast it from PRE_S before the first hit to POST_S after the last? Items whose effect
outlasts fights (Cultist Sacrifice's 160 s buff) count as used when the buff is up at any time of the fight.
sim: the overall search's fight (damage/scripts/overall_search.fight: counterplay skill, real fight-length booking)
of each real holder hero at the fight's net worth, the hero's popular Phantom+ build + the item vs the screening
enemy pool; use = P(the fight is still going at the first cast | nobody died) (Engine.length_w; a cast at t <= 0 or
an effect up at the start counts 1, never cast 0), the same expectation the score books damage with.

Factor = real / sim use share, shrunk toward 1 by its holder-match bootstrap variance (method-of-moments spread),
capped at 1 (a real player can't use an item more often than the sim does by casting it the moment it can).
deadsim realistic mode (accuracy.hero_default_skill counterplay=True, Skill.item_use) then leaves the item unused
in 1 - factor of the fights that have a fight_phase (the overall score's spread enemy pool), see engine.unused_items.

usage: python3 sim/scripts/item_use/fit_item_use.py [--fights DIR] [--casts DIR] [--workers 4] [--real-only]
Writes sim/data/item_use.json and sim/validation/item_use.md. Static snapshot (the replays live in the shared folder):
refit after a patch that changes these items.
"""
import argparse
import bisect
import collections
import dataclasses
import gzip
import json
import math
import os
import random
import statistics
import sys
import zlib
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "sim"))
sys.path.insert(0, os.path.join(ROOT, "sim", "scripts", "fight_length"))
sys.path.insert(0, os.path.join(ROOT, "damage", "scripts"))
sys.path.insert(0, os.path.join(ROOT, "search", "scripts"))

import fit_length as FL  # noqa: E402

FIGHTS = "/mnt/project-files/analysis/work/fight_length/raw/"
CASTS = "/mnt/project-files/analysis/work/item_use/raw/"
SAMPLE = os.path.join(ROOT, "sim", "validation", "phantom_sample.jsonl.gz")
OUT = os.path.join(ROOT, "sim", "data", "item_use.json")
REPORT = os.path.join(ROOT, "sim", "validation", "item_use.md")
T = 64
PRE_S = 2.0     # a cast this long before the first hit of the fight counts (opening casts, pre-fight buffs)
POST_S = 1.0
LONG_BUFF_S = 60.0   # items whose buff lasts longer: used when the buff is up during the fight
MIN_HOLDERS = 15     # holder-matches
BOOT = 300
MERGE = True         # a fighter's pair fights that overlap or follow within GAP_S are one engagement
SIM_ENEMIES = "S"    # screening pool (16 enemies)
BUDGETS = (10000, 18000, 27000, 37000, 50000)


def targets(g):
    """Non-damage active items: actives without a real damage factor (item_landing.json), movement items (their
    value is the real chase / escape effect, movement_value.json) and Dispel Magic (fitted cleanse timing,
    fit_dispel.py) excepted. Refresher's long cooldown is already in the fight phases."""
    with open(os.path.join(ROOT, "sim", "data", "item_landing.json")) as f:
        landing = set(json.load(f)["items"])
    with open(os.path.join(ROOT, "sim", "data", "movement_value.json")) as f:
        mv = json.load(f)
    moving = set(mv.get("movement_items", mv["items"]))
    skip = {"Dispel Magic", "Refresher", "Golden Goose Egg", "Blood Tribute"}
    return {i: it for i, it in g.items.items()
            if it.activation != "passive" and it.cost < 9000 and it.class_name not in landing
            and it.name not in moving and it.name not in skip}


def buff_len(it):
    """Seconds the item's effect lasts when longer than LONG_BUFF_S (else 0)."""
    d = max((v for k, v in it.props.items() if k.endswith("Duration")), default=0.0)
    return d if d > LONG_BUFF_S else 0.0


def held_at(player, item, g0, g):
    """Item held by the player at game time g0: bought by then, not sold, its upgrade not bought yet."""
    bought = sold = None
    for iid, t, s, *_ in player["items"]:
        if iid == item and t <= g0:
            bought, sold = t, s
    if bought is None or (sold and sold <= g0):
        return False
    for iid, t, *_ in player["items"]:
        up = g.items.get(iid)
        if up is not None and item in up.components and t <= g0:
            return False
    return True


def real_rows(args):
    """[(item id, hero id, net worth, used 0/1, match)] for every fighter x held target item x fight of one match."""
    fn, cast_fn, m, tids, buffs = args
    import search as S
    g = S.G()
    hero, ev = FL.read(fn)
    off = FL.clock_offset(ev, hero, m)
    if off is None:
        return []
    casts = collections.defaultdict(list)
    for line in gzip.open(cast_fn, "rt"):
        r = json.loads(line)
        casts[(r["a"], int(r["s"]))].append(r["tick"] / T)
    for v in casts.values():
        v.sort()
    by_hero = {p["hero_id"]: p for p in m["players"]}
    pairs = collections.defaultdict(list)
    for e in ev:
        _, a, v = e[:3]
        pa, pv = by_hero.get(hero.get(a)), by_hero.get(hero.get(v))
        if pa is None or pv is None or pa["team"] == pv["team"]:
            continue
        pairs[min(a, v), max(a, v)].append(e)
    out = []
    spans = collections.defaultdict(list)   # pawn -> [(t0, t1)] of its pair fights
    for (x, y), es in pairs.items():
        runs = []
        for e in es:
            if not runs or e[0] - runs[-1][-1][0] > FL.GAP_S:
                runs.append([])
            runs[-1].append(e)
        for f in runs:
            death = next((k for k, e in enumerate(f) if e[3] <= 0), None)
            if death is not None:
                f = f[:death + 1]
            if len(f) < FL.MIN_HITS or len({(e[1], e[2]) for e in f}) < 2:
                continue
            for pawn in (x, y):
                spans[pawn].append((f[0][0], f[-1][0]))
    for pawn, sp in spans.items():
        # a fighter in a team fight trades with several enemies at once: its overlapping pair fights are one
        # engagement (one cast of a single-target item serves all of them), like the sim's one duel
        sp.sort()
        merged = []
        for t0, t1 in sp:
            if MERGE and merged and t0 <= merged[-1][1] + FL.GAP_S:
                merged[-1][1] = max(merged[-1][1], t1)
            else:
                merged.append([t0, t1])
        p = by_hero[hero[pawn]]
        for t0, t1 in merged:
            g0 = t0 - off(t0)
            nw = FL.nw_at(p["stats"], g0)
            if nw is None:
                continue
            for iid in {it[0] for it in p["items"]}:
                if iid not in tids or not held_at(p, iid, g0, g):
                    continue
                cs = casts.get((pawn, iid), [])
                lo = t0 - (buffs.get(iid) or PRE_S)
                k = bisect.bisect_left(cs, lo)
                used = int(k < len(cs) and cs[k] <= t1 + POST_S)
                out.append((iid, p["hero_id"], nw, used, m["match_id"]))
    return out


def real(fights_dir, casts_dir, workers):
    import search as S
    g = S.G()
    tg = targets(g)
    buffs = {i: buff_len(it) for i, it in tg.items() if buff_len(it)}
    mids = {f.split(".")[0] for f in os.listdir(casts_dir) if f.endswith(".ndjson.gz")}
    mids &= {f.split(".")[0] for f in os.listdir(fights_dir) if f.endswith(".ndjson.gz")}
    sample = FL.load_sample(SAMPLE, mids)
    jobs = [(os.path.join(fights_dir, f"{mid}.ndjson.gz"), os.path.join(casts_dir, f"{mid}.ndjson.gz"), sample[mid],
             set(tg), buffs) for mid in sorted(mids) if mid in sample]
    rows = []
    with Pool(workers) as p:
        for r in p.imap_unordered(real_rows, jobs):
            rows += r
    return rows, len(jobs), tg


# ---- sim side ------------------------------------------------------------------------------------------------
def sim_job(args):
    """Expected use share of item i on hero h at budget b vs the screening pool: P(fight still going at the first
    cast), 1 for an effect up at the start."""
    h, b, i = args
    from deadsim import accuracy, items_fx
    accuracy.ITEM_USE = False   # the sim's own use share, every item used whenever it can be
    import overall_search as O
    import game_path as GP
    O._phases()
    S = O.S
    pools = S.load_pools(b)
    pop = S.popular_build(h, GP.item_budget(b), pools)
    items = GP.with_item(pop, i) if i not in pop else list(pop)
    name = S.G().items[i].name
    log = []
    orig_use = items_fx.FX.use
    orig_buff = items_fx.FX.buff

    def use(self, *a, **k):
        if self.name == name and self.f.name == "me":
            log.append(self.f.e.t)
        return orig_use(self, *a, **k)

    def buff(self, *a, **k):   # long buffs put up at the start (Cultist Sacrifice) without a cast
        if self.name == name and self.f.name == "me" and self.f.e.t <= 0:
            log.append(0.0)
        return orig_buff(self, *a, **k)
    items_fx.FX.use, items_fx.FX.buff = use, buff
    lw = []
    try:
        from deadsim.engine import Engine
        orig_run = Engine.run

        def run(self, a, b_, one_way=False):
            log.clear()
            r = orig_run(self, a, b_, one_way)
            lw.append(self.length_w(max(0.0, log[0])) if log else 0.0)
            return r
        Engine.run = run
        try:
            for oh, oitems, w in pools[SIM_ENEMIES]:
                O.fight(h, items, oh, oitems, b, phase=O.PHASES[oh])
        finally:
            Engine.run = orig_run
    finally:
        items_fx.FX.use, items_fx.FX.buff = orig_use, orig_buff
    ws = [w for _, _, w in pools[SIM_ENEMIES]]
    return h, b, i, sum(x * w for x, w in zip(lw, ws)) / sum(ws)


def nearest_budget(nw):
    return min(BUDGETS, key=lambda b: abs(math.log(max(nw, 1000) / b)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fights", default=FIGHTS)
    ap.add_argument("--casts", default=CASTS)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--real-only", action="store_true")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    rows, n_matches, tg = real(a.fights, a.casts, a.workers)
    import search as S
    heroes = set(S.G().heroes)
    by = collections.defaultdict(list)
    for r in rows:
        by[r[0]].append(r)
    # holder-matches per item, and the (hero, budget) cells real fights fall in
    est = {}
    for i, rs in by.items():
        hm = collections.defaultdict(list)
        for r in rs:
            hm[(r[4], r[1])].append(r[3])
        if len(hm) < MIN_HOLDERS:
            continue
        cells = collections.Counter((r[1], nearest_budget(r[2])) for r in rs if r[1] in heroes)   # sim heroes
        est[i] = {"fights": len(rs), "holders": len(hm), "real": sum(r[3] for r in rs) / len(rs),
                  "groups": list(hm.values()), "cells": cells}
        print(f"{tg[i].name:22s} real use {est[i]['real']:.2f} in {len(rs)} fights, {len(hm)} holder-matches",
              flush=True)
    if a.real_only:
        return
    jobs = sorted({(h, b, i) for i, e in est.items() for (h, b) in e["cells"]})
    sim = {}
    with Pool(a.workers) as p:
        for h, b, i, u in p.imap_unordered(sim_job, jobs):
            sim[(h, b, i)] = u
    rng = random.Random(1)
    fits = {}
    for i, e in est.items():
        tot = sum(e["cells"].values())
        s = sum(sim[(h, b, i)] * n for (h, b), n in e["cells"].items()) / tot
        if s <= 0:
            continue
        raw = e["real"] / s
        boots = []
        gs = e["groups"]
        for _ in range(BOOT):
            pick = [gs[rng.randrange(len(gs))] for _ in gs]
            n = sum(len(x) for x in pick)
            boots.append(sum(sum(x) for x in pick) / n / s)
        fits[i] = (raw, statistics.pstdev(boots), e, s)
    tau2 = max(0.0, statistics.mean((min(1.0, r) - 1) ** 2 for r, *_ in fits.values())
               - statistics.mean(se ** 2 for _, se, *_ in fits.values()))
    out, lines = {}, []
    for i, (raw, se, e, s) in sorted(fits.items(), key=lambda kv: kv[1][0]):
        w = 1 + (raw - 1) * tau2 / (tau2 + se ** 2) if tau2 > 0 else 1.0
        w = min(1.0, w)
        n = tg[i].name
        out[n] = {"factor": round(w, 3), "raw": round(raw, 3), "se": round(se, 3), "real_use": round(e["real"], 3),
                  "sim_use": round(s, 3), "fights": e["fights"], "holders": e["holders"]}
        lines.append(f"| {n} | {e['real']:.2f} | {s:.2f} | {raw:.2f} +- {se:.2f} | **{w:.2f}** | {e['holders']} | "
                     f"{e['fights']} |")
        print(f"{n:22s} factor {w:.2f} (real {e['real']:.2f} / sim {s:.2f} = {raw:.2f} +- {se:.2f})")
    meta = {"source": f"{n_matches} Phantom+ replays (fight_length raw + item casts, fetch_item_casts.py)",
            "pre_s": PRE_S, "post_s": POST_S, "tau": round(tau2 ** 0.5, 3),
            "formula": "real share of fights where a holder uses the item / the sim's expected use share in the "
                       "overall search's fight (P(fight still going at the first cast)); shrunk toward 1, max 1",
            "use": "deadsim realistic mode: the item is left unused in 1 - factor of the fights with a fight_phase"}
    with open(a.out, "w") as f:
        json.dump({"meta": meta, "items": out}, f, indent=1)
    with open(REPORT, "w") as f:
        f.write("# Real use of non-damage active items (Phantom+)\n\n"
                f"{meta['source']}. Use = the fighter casts the item from {PRE_S:g} s before the fight's first hit "
                f"to {POST_S:g} s after its last (engagement: a fighter's fights with enemy heroes, sim/scripts/fight_length, merged when they overlap or follow within 5 s). Sim "
                "use = the overall search's fight, P(the fight is still going at the first cast). Factor = real / "
                f"sim, shrunk toward 1 (tau {tau2 ** 0.5:.2f}), max 1.\n\n"
                "| Item | Real use | Sim use | Raw | Factor | Holder-matches | Engagements |\n|---|---|---|---|---|---|---|\n")
        f.write("\n".join(lines) + "\n")
    print(f"tau {tau2 ** 0.5:.3f}; wrote {a.out}, {REPORT}")


if __name__ == "__main__":
    main()
