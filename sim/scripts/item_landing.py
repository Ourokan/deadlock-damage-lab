"""Fit per-item effective landing factors from real damage, the same way landing_rates.py fits abilities.

Replays the validation sample (real builds both sides, real gun accuracy, abilities landing 100%) and compares,
per damaging item, (real item dmg / real gun dmg) with (sim item dmg / sim gun dmg), pooled over every holder:

    item_landing = (real item dmg / real gun dmg) / (sim item dmg / sim gun dmg)     (holders only)

Below 1: real players get less from the item than the 1v1 sim gives it (procs spent on creeps, charges used
outside fights, effects the target walks out of or cleanses). Above 1: real players get more, mostly from
hitting several heroes in team fights, which a 1v1 should not count. deadsim uses only factors below 1
(Skill.item_landing, `realistic` mode) and leaves the rest at 1.

Writes data/item_landing.json. Does not touch landing_rates.json or the validation files.
usage: python3 scripts/item_landing.py [workers]
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
from deadsim.accuracy import HITS  # noqa: E402
import landing_rates as L  # noqa: E402

MIN_HOLDERS = 25


def job(j):
    m, slot = j
    hid, d, n = L.sim_player(j)
    return m["match_id"], slot, d


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else os.cpu_count()
    G = game()
    real_gun, real_item = collections.Counter(), collections.Counter()
    sim_gun, sim_item = collections.Counter(), collections.Counter()
    holders = collections.Counter()
    jobs, realrows = [], {}
    for line in gzip.open(os.path.join(ROOT, "validation", "matches_sample.jsonl.gz")):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] not in G.heroes or p["custom"].get(HITS, 0) < L.MIN_HITS:
                continue
            classes = [ab.class_name for ab in G.hero(p["hero_id"]).abilities]
            r = collections.Counter()
            for k, v in p["damage_sources"].items():
                if k not in L.CATEGORY:
                    r[L.real_key(k, classes)] += v
            held = {G.items[i].class_name for i, *_ in p["items"] if i in G.items}
            realrows[(m["match_id"], p["slot"])] = (r, held)
            jobs.append((m, p["slot"]))
    t0 = time.time()
    with ProcessPoolExecutor(workers) as ex:
        for i, (mid, slot, d) in enumerate(ex.map(job, jobs, chunksize=8)):
            r, held = realrows[(mid, slot)]
            s = collections.Counter({k: v for k, v in d.items() if not k.startswith("_")})
            if r["GUN"] <= 0 or s["GUN"] <= 0:
                continue
            for c in held:
                if c.startswith("upgrade_"):
                    holders[c] += 1
                    real_gun[c] += r["GUN"]
                    sim_gun[c] += s["GUN"]
                    real_item[c] += r.get(c, 0)
                    sim_item[c] += s.get(c, 0)
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
            "formula": "(real item dmg / real gun dmg) / (sim item dmg / sim gun dmg), item holders only",
            "use": "deadsim realistic mode scales an item's own damage by min(1, landing)"}
    json.dump({"meta": meta, "items": dict(sorted(out.items(), key=lambda x: x[1]["landing"]))},
              open(os.path.join(ROOT, "data", "item_landing.json"), "w"), indent=1)
    for c, v in sorted(out.items(), key=lambda x: x[1]["landing"]):
        print(f"{v['name']:28s} n={v['holders']:5d} real {v['real_per_gun']:.4f} sim {v['sim_per_gun']:.4f} landing {v['landing']:.2f}")


if __name__ == "__main__":
    main()
