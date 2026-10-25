"""Take the fight-length effect out of the landing factors when the sim books damage over real fight lengths.

The ability landing factors (data/landing_rates_mech.json, landing_rates.py) and item factors (data/item_landing.json,
item_landing.py) were fitted with every hit of a 20 s duel counting in full, so they absorbed the part of real
fights being shorter (an opener counts for more of a short fight than of a 20 s one). With Mechanics.fight_length
(mechanics.real_length, data/fight_length.json) that part is modeled, so each factor is scaled by

    length_corr = (sim source dmg / sim gun dmg, every hit in full) / (the same, expected over real fight lengths)

from the same duels (the damage audit's: Phantom+ sample, real builds both sides, the searches' skills): a fight
length booking leaves the fight itself unchanged, so one run gives both. That keeps every earlier fit and choice
(heroes refit on Phantom+, refits that were kept out) and changes only what the fight length explains: the factor
x length_corr gives the same pooled real/sim ratio under the new booking as the old factor gave under the old one.
Abilities: per hero; items: holders only, gun damage of the duels holding the item, pooled over heroes (as fitted).

Each row keeps its fitted factor (landing) and gets length_corr; deadsim.accuracy applies landing x length_corr
(after the usual clips) only to fights with Mechanics.fight_length, so the dummy page and other full-booking fights
keep the fit as it is. After a refit (landing_rates.py, refit_landing_heroes.py, item_landing.py: they fit with
every hit in full and keep the old length_corr) rerun this.

usage: python3 length_factors.py [workers] [--sample PATH] [--rounds 3] [--write] [--hero NAME ...]
(--hero: only those heroes' ability rows, from their own players' duels; item rows stay as they are)   (~1 min a round on 4 cores)
"""
import collections
import gzip
import json
import os
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from deadsim import game  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
import deadsim.accuracy as ACC  # noqa: E402
import damage_audit as A  # noqa: E402
import landing_rates as L  # noqa: E402

ABILITY_FILE = os.path.join(ROOT, "data", "landing_rates_mech.json")
ITEM_FILE = os.path.join(ROOT, "data", "item_landing.json")
MIN_HOLDERS = 25
CORR_RANGE = (0.2, 5.0)   # clip: a correction outside it would be noise in a thinly sampled source


def job(j):
    return A.sim_player(j, both=True)


def clip(c):
    return max(CORR_RANGE[0], min(CORR_RANGE[1], c))


def corr(w, u, key):
    """(source / gun in full) / (source / gun over real lengths) for two Counters, or None."""
    if w.get(key, 0) <= 0 or u.get(key, 0) <= 0 or w.get("GUN", 0) <= 0 or u.get("GUN", 0) <= 0:
        return None
    return (u[key] / u["GUN"]) / (w[key] / w["GUN"])


def run(jobs, workers):
    """The duels' damage by hero and source and by held item, expected over real lengths (w) and in full (u)."""
    sim_w, sim_u = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    held_w, held_u = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    holders = collections.Counter()
    t0 = time.time()
    with ProcessPoolExecutor(workers) as ex:
        for i, (hid, (dw, du), (hw, hu)) in enumerate(ex.map(job, jobs, chunksize=8)):
            sim_w[hid].update({k: v for k, v in dw.items() if not k.startswith("_")})
            sim_u[hid].update({k: v for k, v in du.items() if not k.startswith("_")})
            for c in hw:
                holders[c] += 1
                held_w[c].update({c: hw[c][0], "GUN": hw[c][1]})
                held_u[c].update({c: hu[c][0], "GUN": hu[c][1]})
            if i % 2000 == 0:
                print(f"{i}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    return sim_w, sim_u, held_w, held_u, holders


def main():
    args = sys.argv[1:]
    sample = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
    if "--sample" in args:
        i = args.index("--sample")
        sample = args[i + 1]
        args = args[:i] + args[i + 2:]
    write = "--write" in args
    args = [a for a in args if a != "--write"]
    only = set()
    while "--hero" in args:   # refit only these heroes' ability rows (after a hero file change); items stay
        i = args.index("--hero")
        only.add(game().hero(args[i + 1]).id)
        args = args[:i] + args[i + 2:]
    rounds = 3
    if "--rounds" in args:
        i = args.index("--rounds")
        rounds = int(args[i + 1])
        args = args[:i] + args[i + 2:]
    workers = int(args[0]) if args else os.cpu_count()
    G = game()
    load_heroes()
    jobs = []
    for line in gzip.open(sample):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] in G.heroes and L.gun_known(p) and (not only or p["hero_id"] in only):
                jobs.append((m, p["slot"]))
    random.Random(1).shuffle(jobs)
    # round 0 on the fitted factors alone: the in-full ratios are the target, the expected ones give the first
    # correction; later rounds (with --write, the duels read the files) fight with the corrections, which moves
    # fight lengths and procs a little, and scale each correction by target / what they now give
    ACC.LENGTH_CORR = False   # forked workers inherit it
    target_ab = target_it = None
    abil, items = json.load(open(ABILITY_FILE)), json.load(open(ITEM_FILE))
    for rnd in range(rounds if write else 1):
        sim_w, sim_u, held_w, held_u, holders = run(jobs, workers)
        if target_ab is None:
            target_ab, target_it = sim_u, held_u
        n_ab = n_it = 0
        for hn, rows in abil["heroes"].items():
            try:
                hid = G.hero(hn).id
            except Exception:  # noqa: BLE001
                continue
            if only and hid not in only:
                continue
            for name, r in rows.items():
                cls = r.get("class") or L.ALIASES.get(name)
                c = corr(sim_w[hid], target_ab[hid], cls) if cls else None
                if c is None:
                    continue
                c = clip(c * (r.get("length_corr", 1.0) if rnd else 1.0))
                r["length_corr"] = round(c, 3)
                n_ab += 1
                print(f"  {hn:14s} {name:28s} {r['landing']} x{c:.2f}")
        for cls, r in items["items"].items():
            if only or holders[cls] < MIN_HOLDERS:   # (accuracy.item_landing uses 30+)
                continue
            c = corr(held_w[cls], target_it[cls], cls)
            if c is None:
                continue
            c = clip(c * (r.get("length_corr", 1.0) if rnd else 1.0))
            r["length_corr"] = round(c, 3)
            n_it += 1
            print(f"  item {r['name']:24s} {r['landing']} x{c:.2f}")
        print(f"round {rnd + 1}: {n_ab} ability factors, {n_it} item factors corrected", flush=True)
        if write:
            for fn, d in ((ABILITY_FILE, abil), (ITEM_FILE, items)):
                with open(fn, "w") as fh:
                    json.dump(d, fh, indent=1)
                    fh.write("\n")
            ACC.LENGTH_CORR = True
    note = ("fights with Mechanics.fight_length use landing (fit with every hit of a 20 s duel in full) x "
            "length_corr (the sim's source/gun in full / the same expected over real fight lengths, "
            f"scripts/fight_length/length_factors.py, {os.path.basename(sample)}, {rounds} rounds)")
    abil["meta"]["length"] = note
    items["meta"]["length"] = note
    if write:
        for fn, d in ((ABILITY_FILE, abil), (ITEM_FILE, items)):
            with open(fn, "w") as fh:
                json.dump(d, fh, indent=1)
                fh.write("\n")


if __name__ == "__main__":
    main()
