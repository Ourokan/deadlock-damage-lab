"""Ability pokes in Phantom+ replays: hits that land outside any fight, for the sim's poke hits beside the duel
(data/ability_pokes.json, mechanics.poke_rows, fight.add_pokes).

A fight is fit_length.py's: a run of damage between two enemy heroes with no gap over GAP_S s, at least MIN_HITS
hits and damage both ways. Everything else between two enemy heroes is a poke run (a lone hit, or one side hitting
a target that doesn't answer). The damage audit compares the sim's duels with whole real matches, so an ability that
lands much more in pokes than the gun does comes out short per gun damage, and so do the items that ride on its
hits (Paradox's Kinetic Carbine: 58% of its hits are pokes, against 44% of his gun damage, and Tankbuster / Mystic
Burst / Mystic Shot ride on them).

Per hero and ability (by the game's ability id): poke hits per fight of the hero (either side), the share of the
ability's hits in pokes against the share of the gun damage in pokes, the ability's hits per 1000 gun damage in
fights and in all, the share of fights the ability opens (the hero's first hit), and the median hit as a multiple of
the hero's median gun hit in fights and in pokes. The sim uses only the rows named in USE (validation/README.md
"Carbine pokes"); the rest are listed for later heroes.

usage: python3 -I ability_pokes.py <raw dir> [--write]
Raw dir: fetch_fights.py output (project folder analysis/work/fight_length/raw).
"""
import collections
import glob
import gzip
import json
import multiprocessing
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
T = 64
GAP_S = 5.0     # fit_length.GAP_S
MIN_HITS = 4    # fit_length.MIN_HITS
MIN_N = 300     # hits of the ability for a row
USE = {(10, "citadel_ability_chrono_kinetic_carbine")}   # rows the sim uses: (hero id, ability class)

WEAPONS = {w["id"] for w in json.load(open(os.path.join(ROOT, "data", "game", "weapons.json")))}


def one(fn):
    hero, ev = {}, []
    for line in gzip.open(fn, "rt"):
        r = json.loads(line)
        if r["k"] == "ctl":
            hero[r["a"]] = int(r["s"])
        elif r["k"] == "dmg" and r.get("s"):
            ev.append((r["tick"] / T, r["a"] // 100000, r["a"] % 100000, int(r["s"].split("|")[0]), r["v"]))
    ev.sort()
    agg = collections.Counter()
    sizes = collections.defaultdict(list)   # (hero, source, kind) -> hits / the player's median gun hit
    gun_med = {}
    for p in hero:
        g = [e[4] for e in ev if e[1] == p and e[3] in WEAPONS]
        if len(g) >= 30:
            gun_med[p] = statistics.median(g)
    pairs = collections.defaultdict(list)
    for e in ev:
        a, v = e[1], e[2]
        if a in hero and v in hero and a != v:
            pairs[min(a, v), max(a, v)].append(e)
    for (x, y), es in pairs.items():
        runs = []
        for e in es:
            if not runs or e[0] - runs[-1][-1][0] > GAP_S:
                runs.append([])
            runs[-1].append(e)
        for f in runs:
            fight = len(f) >= MIN_HITS and len({e[1] for e in f}) >= 2
            kind = "fight" if fight else "poke"
            for p in (x, y):
                h = hero[p]
                mine = [e for e in f if e[1] == p]
                if fight:
                    agg[h, "fights"] += 1
                    if mine:
                        agg[h, "gun" if mine[0][3] in WEAPONS else mine[0][3], "open"] += 1
                for e in mine:
                    src = "gun" if e[3] in WEAPONS else e[3]
                    agg[h, src, kind, "dmg"] += e[4]
                    agg[h, src, kind, "n"] += 1
                    if src != "gun" and p in gun_med:
                        sizes[h, src, kind].append(e[4] / gun_med[p])
    return agg, sizes


def main():
    raw = [a for a in sys.argv[1:] if not a.startswith("--")][0]
    files = sorted(glob.glob(os.path.join(raw, "*.ndjson.gz")))
    agg, sizes = collections.Counter(), collections.defaultdict(list)
    with multiprocessing.Pool() as pool:
        for a, s in pool.imap_unordered(one, files):
            agg.update(a)
            for k, v in s.items():
                sizes[k] += v
    abilities = {a["id"]: a for a in json.load(open(os.path.join(ROOT, "data", "game", "abilities.json")))}
    heroes = {h["id"]: h["name"] for h in json.load(open(os.path.join(ROOT, "data", "game", "heroes.json")))}
    rows = []
    for k in list(agg):
        if len(k) != 4 or k[1] == "gun" or k[2] != "fight" or k[3] != "n":
            continue
        h, src = k[0], k[1]
        ab = abilities.get(src)
        if ab is None or ab["hero_id"] != h:
            continue
        nf, np_ = agg[h, src, "fight", "n"], agg[h, src, "poke", "n"]
        gf, gp = agg[h, "gun", "fight", "dmg"], agg[h, "gun", "poke", "dmg"]
        if nf + np_ < MIN_N or gf <= 0:
            continue

        def med(kind):
            v = sizes[h, src, kind]
            return round(statistics.median(v), 2) if v else None
        rows.append({"hero_id": h, "hero": heroes.get(h, str(h)), "class_name": ab["class_name"], "name": ab["name"],
                     "pokes_per_fight": round(np_ / agg[h, "fights"], 3),
                     "poke_share": round(np_ / (nf + np_), 3), "gun_poke_share": round(gp / (gf + gp), 3),
                     "per_1000_gun_fights": round(1000 * nf / gf, 3),
                     "per_1000_gun_all": round(1000 * (nf + np_) / (gf + gp), 3),
                     "opens": round(agg[h, src, "open"] / agg[h, "fights"], 3),
                     "hit_x_gun_fight": med("fight"), "hit_x_gun_poke": med("poke"),
                     "use": (h, ab["class_name"]) in USE})
    rows.sort(key=lambda r: -r["per_1000_gun_all"] / max(1e-9, r["per_1000_gun_fights"]))
    print(f"{len(files)} replays; ability / gun hits per 1000 gun damage, all over fights only (top 25)")
    for r in rows[:25]:
        print(f"{r['per_1000_gun_all'] / r['per_1000_gun_fights']:.2f} {r['hero']:14s} {r['name']:24s} "
              f"pokes/fight {r['pokes_per_fight']:.2f}, poke share {r['poke_share']:.2f} (gun {r['gun_poke_share']:.2f}), "
              f"opens {r['opens']:.2f}, hit x gun fight {r['hit_x_gun_fight']} poke {r['hit_x_gun_poke']}"
              f"{'  USED' if r['use'] else ''}")
    if "--write" in sys.argv:
        out = {"source": f"{len(files)} Phantom+ replays, hero-vs-hero DamageEvents (scripts/fight_length/ability_pokes.py)",
               "note": "pokes_per_fight: hits of the ability outside fit_length.py's fights per fight of the hero; "
                       "the sim adds that many casts' damage beside each duel for rows with use (fight.add_pokes)",
               "abilities": rows}
        with open(os.path.join(HERE, "..", "..", "data", "ability_pokes.json"), "w") as fh:
            json.dump(out, fh, indent=1)
            fh.write("\n")


if __name__ == "__main__":
    main()
