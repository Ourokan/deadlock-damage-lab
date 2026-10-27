"""Heavy melee share of Melee Charge / Crushing Fists holders from Phantom+ replays: Mechanics.heavy_holders,
data/melee_heavy.json.

Both items proc on a heavy melee off a 5 s cooldown (Melee Charge +25% of the hit: real procs are 0.25x the melee hit
on the same tick, every one). So a holder's basic melee hits that carry a proc on the same victim within 2 ticks are
heavies the item paid for. The sim's melee rotation is 30% heavy (engine.HEAVY_SHARE) for every player; real holders
throw heavies far more: Abrams 0.55 of their basic melee hits proc, Apollo 0.70, Yamato 0.50, Venator 0.72 (and of the
hits off the item's cooldown, 0.6-0.9 are heavies), pooled ~0.5.

Input: the fight-length replays (every hero-vs-hero DamageEvent with the ability id, fight_length/fetch_fights.py)
and the validation sample (each player's items over time: a hit counts while the player owns either item).
Per hero: procced hits / basic melee hits, shrunk toward the pooled share with PRIOR hits.

usage: python3 -I melee_heavy.py [--write]
"""
import collections
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(HERE, ".."))
from deadsim import game  # noqa: E402
import landing_rates as L  # noqa: E402

RAW = "/mnt/project-files/analysis/work/fight_length/raw/"
SAMPLE = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
OUT = os.path.join(ROOT, "data", "melee_heavy.json")
ITEMS = ("upgrade_melee_charge", "upgrade_crushing_fists")
PRIOR = 100   # hits
MIN_HITS = 30


def main():
    G = game()
    raw = json.load(open(os.path.join(ROOT, "..", "data", "game", "raw", "items.json")))
    name = {str(x.get("id")): x.get("class_name") or "" for x in raw}
    ids = {G.items[i].class_name: i for i in G.items}
    hold = {ids[c] for c in ITEMS if c in ids}
    sample = {}
    for line in gzip.open(SAMPLE):
        m = json.loads(line)
        sample[str(m["match_id"])] = m
    acc = collections.defaultdict(lambda: [0, 0])   # hero id -> [procced basic melee hits, basic melee hits]
    n_matches = 0
    for f in sorted(os.listdir(RAW)):
        mid = f.split(".")[0]
        if mid not in sample:
            continue
        n_matches += 1
        ev = [json.loads(x) for x in gzip.open(RAW + f)]
        hero = {r["a"]: r["s"] for r in ev if r["k"] == "ctl"}
        t0 = min(r["tick"] for r in ev)
        players = {str(p["hero_id"]): p for p in sample[mid]["players"]}
        procs, hits = collections.defaultdict(list), []
        for r in ev:
            if r["k"] != "dmg" or "s" not in r:
                continue
            a, v = divmod(r["a"], 100000)
            if a not in hero or v not in hero:
                continue
            src = name.get(r["s"].split("|")[0], r["s"].split("|")[0])
            if src in ITEMS:
                procs[(a, v)].append(r["tick"])
            elif src.startswith("citadel_ability_melee") or src.startswith("ability_melee"):
                hits.append((r["tick"], a, v))
        for t, a, v in hits:
            p = players.get(hero[a])
            if not p or p["hero_id"] not in G.heroes:
                continue
            items, _ = L.build_at(p, (t - t0) / 64)
            if not hold & set(items):
                continue
            c = acc[p["hero_id"]]
            c[0] += any(abs(t2 - t) <= 2 for t2 in procs[(a, v)])
            c[1] += 1
    k = sum(c[0] for c in acc.values())
    n = sum(c[1] for c in acc.values())
    pooled = k / max(1, n)
    heroes = {}
    for hid, (kk, nn) in sorted(acc.items(), key=lambda x: -x[1][1]):
        if nn < MIN_HITS:
            continue
        share = (kk + PRIOR * pooled) / (nn + PRIOR)
        heroes[str(hid)] = {"name": G.heroes[hid].name, "hits": nn, "procced": kk, "real": round(kk / nn, 3),
                            "share": round(share, 3)}
        print(f"{G.heroes[hid].name:14s} hits {nn:5d} procced {kk / nn:.2f} -> share {share:.3f}")
    print(f"pooled {k}/{n} = {pooled:.3f} ({n_matches} replays)")
    if "--write" in sys.argv:
        out = {"source": f"{n_matches} Phantom+ replays (fight_length raw), basic melee hits by Melee Charge / Crushing "
                         f"Fists holders with the item's proc on the same victim within 2 ticks "
                         f"(scripts/mechanics/melee_heavy.py)",
               "note": f"share = heavy share of a holder's melee rotation (Mechanics.heavy_holders), per hero shrunk "
                       f"toward pooled with {PRIOR} hits",
               "pooled": round(pooled, 3), "heroes": heroes}
        json.dump(out, open(OUT, "w"), indent=1)
        print("wrote", OUT)


if __name__ == "__main__":
    main()
