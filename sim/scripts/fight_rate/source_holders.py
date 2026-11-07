"""Holders vs non-holders of an item, damage to enemy heroes by SOURCE (gun, abilities, the item itself, other items,
melee), real and sim, on the same player intervals.

Unit = one player's damage-matrix interval (fetch_validation.py samples, ~180 s) whose start net worth is in NW.
Held = bought by the interval's start, not sold before its end (bought/sold inside: left out). Matched like
real_rates.py: stratum (hero, net worth // 2500, start time // 300 s), per stratum holders' mean vs non-holders' mean,
holder-weighted; reported as holders / non-holders ratios per source. Real = damage-matrix damage per minute in the
interval. Sim (--sim) = one audit duel (damage_audit.sim_player's model: the player's real build, aim and a real foe
at the interval's midpoint, expected over real fight lengths, area extra hits) per interval: the sim's damage by
source for the same builds, so real ratio / sim ratio says which source the sim under-produces for holders.
Split-half by match id parity.

usage: python3 scripts/fight_rate/source_holders.py SAMPLE.jsonl.gz [--item "Mystic Reverb"] [--sim] [--workers 8]
       [--nw 20250 49950] [--out FILE.json]
"""
import argparse
import collections
import dataclasses
import gzip
import json
import math
import os
import random
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, ".."))
from deadsim import Loadout, duel, game  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
import landing_rates as L  # noqa: E402
import damage_audit as A  # noqa: E402
from deadsim.mechanics import DEFAULT as MECH, RICOCHET_RADIUS, real_length, real_nearby  # noqa: E402
from deadsim.accuracy import default_distance  # noqa: E402
from deadsim.heroes import nurse  # noqa: E402

NW_BIN, T_BIN = 2500, 300
CATS = ("gun", "ability", "self", "item", "melee", "total")


def real_cat(name, classes, item_cls):
    if name in L.CATEGORY:
        return None
    k = L.real_key(name, classes)
    if k == "GUN":
        return "gun"
    if k == "MELEE":
        return "melee"
    if k == item_cls:
        return "self"
    if k.startswith("upgrade_"):
        return "item"
    return "ability" if k in classes or "ability" in k else "item"


def sim_cat(k, G, classes, item_cls):
    if k == item_cls:
        return "self"
    c = A.kind(k, G, classes)
    return {"other": "ability"}.get(c, c)


def held_state(p, item_id, t0, t1):
    """1 held all interval, 0 not at all, None bought/sold inside."""
    st = 0
    for i, bt, sold, _ in p["items"]:
        if i != item_id:
            continue
        if bt <= t0 and (sold == 0 or sold >= t1):
            return 1
        if bt < t1 and (sold == 0 or sold > t0):
            st = None
    return st


def nw_at(p, t):
    snaps = [s for s in p["stats"] if s["time_stamp_s"] <= t] or p["stats"][:1]
    return snaps[-1]["net_worth"]


def units(m, item_id, item_cls, nw, heroes):
    G = game()
    times = m.get("damage_times") or []
    for p in m["players"]:
        if p["hero_id"] not in G.heroes or (heroes and p["hero_id"] not in heroes):
            continue
        classes = [ab.class_name for ab in G.hero(p["hero_id"]).abilities]
        ser = p.get("damage_series") or {}
        for i in range(1, len(times)):
            t0, t1 = times[i - 1], times[i]
            mins = (t1 - t0) / 60
            if mins < 2.0:
                continue
            w0 = nw_at(p, t0)
            if not nw[0] <= w0 < nw[1]:
                continue
            h = held_state(p, item_id, t0, t1)
            if h is None:
                continue
            d = collections.Counter()
            for k, arr in ser.items():
                c = real_cat(k, classes, item_cls)
                if c:
                    d[c] += (arr[i] - arr[i - 1]) / mins
            d["total"] = sum(d[c] for c in CATS if c != "total")
            yield p["slot"], p["hero_id"], w0, t0, t1, h, dict(d)


def sim_unit(job):
    """Sim damage by category of one duel at the interval midpoint (damage_audit.sim_player's set-up)."""
    m, slot, t, item_cls, seed, drop = job
    G = game()
    load_heroes()
    me = next(p for p in m["players"] if p["slot"] == slot)
    foes = [p for p in m["players"] if p["team"] != me["team"] and p["hero_id"] in G.heroes]
    h = G.hero(me["hero_id"])
    names = {ab.name: ab.class_name for ab in h.abilities}
    classes = set(names.values())
    rnd = random.Random(m["match_id"] * 31 + slot * 7 + int(t) + seed * 1000003)
    items, souls = L.build_at(me, t)
    if drop:   # the holder's build without the item (its souls kept): the item's own part of the holders' ratio
        items = [i for i in items if G.items[i].class_name != item_cls]
    foe = rnd.choice(foes)
    fitems, fsouls = L.build_at(foe, t)
    a = Loadout(h.name, items, souls=souls, skill=A.skill_of(me), **A.real_tiers(me, t))
    b = Loadout(foe["hero_id"], fitems, souls=fsouls, skill=A.skill_of(foe), **A.real_tiers(foe, t))
    team = lambda pl: {G.hero(x["hero_id"]).name for x in m["players"]  # noqa: E731
                       if x["team"] == pl["team"] and x["hero_id"] in G.heroes}
    vapors = (nurse.ally_vapors_share(team(me), h.name), nurse.ally_vapors_share(team(foe), G.hero(foe["hero_id"]).name))
    mech = dataclasses.replace(MECH, extra_targets=real_nearby("extra", RICOCHET_RADIUS, souls), ally_vapors=vapors,
                               fight_length=real_length(souls))
    try:
        r = duel(a, b, distance=default_distance(h.name), max_time=L.FIGHT_TIME, rng=random.Random(rnd.random()),
                 mechanics=mech)
    except Exception:  # noqa: BLE001
        return None
    d = collections.Counter()
    for k, v in A.sim_sources(r, lambda k: L.sim_key(k, names, G)).items():
        d[sim_cat(k, G, classes, item_cls)] += v
    d["total"] = sum(d[c] for c in CATS if c != "total")
    return dict(d)


def compare(rows, key):
    """Holder-weighted matched ratios per category: {cat: [ratio, z]} plus n holders."""
    strata = collections.defaultdict(lambda: ([], []))
    for r in rows:
        if r.get(key) is None:
            continue
        s = strata[(r["hero"], r["nw"] // NW_BIN, r["t0"] // T_BIN)]
        s[0 if r["held"] else 1].append(r[key])
    out, nh = {}, 0
    for c in CATS:
        num = den = var = 0.0
        n = 0
        for hs, ns in strata.values():
            if not hs or not ns:
                continue
            a = [x.get(c, 0.0) for x in hs]
            b = [x.get(c, 0.0) for x in ns]
            ma, mb = sum(a) / len(a), sum(b) / len(b)
            w = len(a)
            num += w * ma
            den += w * mb
            va = sum((x - ma) ** 2 for x in a) / max(1, len(a) - 1)
            vb = sum((x - mb) ** 2 for x in b) / max(1, len(b) - 1)
            var += w * w * (va / len(a) + vb / len(b))
            n += w
        if n:   # [holders / non-holders, z, non-holders' mean, holders' mean] per minute (real) or per duel (sim)
            out[c] = [round(num / den, 3) if den > 0 else None,
                      round((num - den) / math.sqrt(var), 1) if var > 0 else 0.0,
                      round(den / n, 1), round(num / n, 1)]
        nh = max(nh, n)
    out["n"] = nh
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sample")
    ap.add_argument("--item", default="Mystic Reverb")
    ap.add_argument("--sim", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--seeds", type=int, default=1)
    ap.add_argument("--nw", type=int, nargs=2, default=(20250, 49950))
    ap.add_argument("--out")
    ap.add_argument("--no-health-term", action="store_true", help="Mystic Reverb without its current-health echo term")
    a = ap.parse_args()
    if a.no_health_term:
        from deadsim import items_fx
        items_fx.MysticReverb.CURRENT_HEALTH_BONUS = False
    G = game()
    it = G.items_by_name[a.item.lower()]
    ms = [json.loads(line) for line in gzip.open(a.sample, "rt")]
    # heroes with at least 10 holder intervals: the others have no matched holders
    cnt = collections.Counter()
    for m in ms:
        for u in units(m, it.id, it.class_name, a.nw, None):
            if u[5]:
                cnt[u[1]] += 1
    heroes = {h for h, c in cnt.items() if c >= 10}
    rows, jobs = [], []
    for m in ms:
        for slot, hid, w0, t0, t1, held, d in units(m, it.id, it.class_name, a.nw, heroes):
            rows.append({"match": m["match_id"], "hero": hid, "nw": w0, "t0": t0, "held": held, "real": d})
            jobs.append((m, slot, 0.5 * (t0 + t1), it.class_name))
    # only strata with both holders and non-holders are compared: simulate only those
    have = collections.defaultdict(set)
    for r in rows:
        have[(r["hero"], r["nw"] // NW_BIN, r["t0"] // T_BIN)].add(r["held"])
    keep = [i for i, r in enumerate(rows) if len(have[(r["hero"], r["nw"] // NW_BIN, r["t0"] // T_BIN)]) == 2]
    rows = [rows[i] for i in keep]
    jobs = [jobs[i] for i in keep]
    print(len(ms), "matches,", len(heroes), "heroes,", len(rows), "matched intervals,",
          sum(r["held"] for r in rows), "held", flush=True)
    if a.sim:
        for s in range(a.seeds):
            with ProcessPoolExecutor(a.workers) as ex:
                res = list(ex.map(sim_unit, [j + (s, False) for j in jobs], chunksize=16))
                drop = list(ex.map(sim_unit, [j + (s, True) for j, r in zip(jobs, rows) if r["held"]], chunksize=16))
            for r, d in zip(rows, res):
                if d is not None:
                    acc = r.setdefault("sim", collections.Counter())
                    for k, v in d.items():
                        acc[k] += v / a.seeds
            for r, d in zip([r for r in rows if r["held"]], drop):
                if d is not None:
                    acc = r.setdefault("sim_drop", collections.Counter())
                    for k, v in d.items():
                        acc[k] += v / a.seeds
    out = {}
    for name, sel in (("all", lambda r: True), ("even", lambda r: r["match"] % 2 == 0), ("odd", lambda r: r["match"] % 2 == 1)):
        rs = [r for r in rows if sel(r)]
        out[name] = {"real": compare(rs, "real")}
        if a.sim:
            out[name]["sim"] = compare(rs, "sim")
            # holders' sim damage with / without the item, same duels (the item's own gain on holders' builds)
            hs = [r for r in rs if r["held"] and r.get("sim") and r.get("sim_drop")]
            out[name]["sim_own"] = {c: round(sum(r["sim"].get(c, 0) for r in hs) / max(1e-9, sum(r["sim_drop"].get(c, 0) for r in hs)), 3)
                                    for c in CATS}
    per_hero = {}
    for hid in sorted(heroes):
        rs = [r for r in rows if r["hero"] == hid]
        if sum(r["held"] for r in rs) >= 15:
            per_hero[G.hero(hid).name] = {"real": compare(rs, "real"), **({"sim": compare(rs, "sim")} if a.sim else {})}
    out["heroes"] = per_hero
    for name in ("all", "even", "odd"):
        print(name, "n", out[name]["real"]["n"])
        for c in CATS:
            rr = out[name]["real"].get(c)
            ss = out[name].get("sim", {}).get(c)
            print(f"  {c:8s} real {rr}  sim {ss}  own {out[name].get('sim_own', {}).get(c)}")
    if a.out:
        json.dump({"item": a.item, "nw": a.nw, **out}, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
