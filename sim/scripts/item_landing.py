"""Fit per-item effective landing factors from real damage.

Replays the sample (real builds both sides, each player's real gun accuracy, abilities at their fitted landing
factors, counterplay as the searches use it but with no item factors) and compares, per damaging item,
(real item dmg / real gun dmg) with (sim item dmg / sim gun dmg), pooled over the players who had the item at a
sampled point, with gun damage counted only while the item was owned:

    item_landing = (real item dmg / real gun dmg while owned) / (sim item dmg / sim gun dmg in duels holding it)

Below 1: real players get less from the item than the 1v1 sim gives it (procs spent on creeps, charges used
outside fights, effects the target walks out of or cleanses). Above 1: real players get more, mostly from
hitting several heroes in team fights, which a 1v1 should not count. deadsim uses only factors below 1
(Skill.item_landing, `realistic` mode) and leaves the rest at 1.

2026-10-24: the first fit (2026-10-14) divided by match-total gun damage and fought with abilities always landing.
Gun damage before an item is bought diluted the real ratio of late items, and on-ability procs (Mystic Burst,
Tankbuster, Spirit Burn) fired more often in the sim than in the searches; both pushed factors down.

Writes data/item_landing.json. Does not touch landing_rates.json or the validation files.
usage: python3 scripts/item_landing.py [workers] [--sample PATH]
"""
import collections
import gzip
import json
import os
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deadsim import game  # noqa: E402
import damage_audit as A  # noqa: E402
import landing_rates as L  # noqa: E402

A.COUNTERPLAY = False
MIN_HOLDERS = 25


def job(j):
    m, slot = j
    hid, d, held = A.sim_player(j)
    return m["match_id"], slot, d, held


def main():
    args = sys.argv[1:]
    sample = os.path.join(ROOT, "validation", "matches_sample.jsonl.gz")
    if "--sample" in args:
        i = args.index("--sample")
        sample = args[i + 1]
        args = args[:i] + args[i + 2:]
    workers = int(args[0]) if args else os.cpu_count()
    G = game()
    real_gun, real_item = collections.Counter(), collections.Counter()
    sim_gun, sim_item = collections.Counter(), collections.Counter()
    holders = collections.Counter()
    jobs, realrows = [], {}
    windowed = True
    for line in gzip.open(sample):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] not in G.heroes or not L.gun_known(p):
                continue
            classes = [ab.class_name for ab in G.hero(p["hero_id"]).abilities]
            r = collections.Counter()
            for k, v in p["damage_sources"].items():
                if k not in L.CATEGORY:
                    r[L.real_key(k, classes)] += v
            hg = L.held_gun(m, p)
            windowed = windowed and hg is not None
            realrows[(m["match_id"], p["slot"])] = (r, hg)
            jobs.append((m, p["slot"]))
    t0 = time.time()
    with ProcessPoolExecutor(workers) as ex:
        for i, (mid, slot, d, held) in enumerate(ex.map(job, jobs, chunksize=8)):
            r, hg = realrows[(mid, slot)]
            if r["GUN"] <= 0:
                continue
            # holders at a sampled point; gun damage only while the item was owned (real: between buy and sell
            # from the damage matrix samples; sim: the duels whose build had it). A sample without damage_series
            # falls back to match-total real gun damage, which undercounts items bought late.
            for c, (si, sg) in held.items():
                if not c.startswith("upgrade_") or sg <= 0:
                    continue
                rg = hg.get(c, 0.0) if hg is not None else r["GUN"]
                if rg <= 0:
                    continue
                holders[c] += 1
                real_gun[c] += rg
                sim_gun[c] += sg
                real_item[c] += r.get(c, 0)
                sim_item[c] += si
            if i % 1000 == 0:
                print(f"{i}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    out = {}
    for c in holders:
        if holders[c] < MIN_HOLDERS or sim_item[c] <= 0 or real_gun[c] <= 0:
            continue
        rr, sr = real_item[c] / real_gun[c], sim_item[c] / sim_gun[c]
        if rr <= 0 and sr <= 0:
            continue
        out[c] = {"name": G.items_by_class[c].name if c in G.items_by_class else c, "holders": holders[c],
                  "real_per_gun": round(rr, 4), "sim_per_gun": round(sr, 4), "landing": round(rr / sr, 3)}
    meta = {"source": f"{len(jobs)} player-matches x {len(L.FRACS)} duels ({L.FIGHT_TIME:.0f} s), real builds both sides",
            "formula": "(real item dmg / real gun dmg) / (sim item dmg / sim gun dmg), item holders only"
                       + (", gun damage while the item was owned" if windowed else ", match-total real gun damage"),
            "sample": os.path.basename(sample),
            "use": "deadsim realistic mode scales an item's own damage by min(1, landing)"}
    try:   # keep the fight-length corrections (scripts/fight_length/length_factors.py; rerun it after this)
        prev = json.load(open(os.path.join(ROOT, "data", "item_landing.json")))
        for c, r in prev["items"].items():
            if c in out and "length_corr" in r:
                out[c]["length_corr"] = r["length_corr"]
        if "length" in prev.get("meta", {}):
            meta["length"] = prev["meta"]["length"]
        heroes = prev.get("heroes")   # per-hero factors (scripts/item_landing_heroes.py; rerun it after this)
        hero_meta = prev.get("meta", {}).get("heroes")
    except (OSError, ValueError, KeyError):
        heroes = hero_meta = None
    if hero_meta:
        meta["heroes"] = hero_meta
    res = {"meta": meta, "items": dict(sorted(out.items(), key=lambda x: x[1]["landing"]))}
    if heroes:
        res["heroes"] = heroes
    json.dump(res, open(os.path.join(ROOT, "data", "item_landing.json"), "w"), indent=1)
    for c, v in sorted(out.items(), key=lambda x: x[1]["landing"]):
        print(f"{v['name']:28s} n={v['holders']:5d} real {v['real_per_gun']:.4f} sim {v['sim_per_gun']:.4f} landing {v['landing']:.2f}")


if __name__ == "__main__":
    main()
