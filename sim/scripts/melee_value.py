"""What melee is worth: (1) how much each hero's real melee rate changes its 1v1 results, and (2) the marginal value
of each melee item vs a non-melee item of the same cost, on real builds.

For each hero, take real mid/late-game snapshots of that hero from validation/matches_sample.jsonl.gz (items and
net worth at a random moment) against a real enemy from the same match at the same moment. Skills are the hero
defaults (ranked median aim, ability landing rates, real melee rate). Metrics: win rate in 30 s duels (a timeout
counts as half) and mean HP margin (my HP left - enemy HP left, as a fraction of max HP; dead = 0).

usage: python3 scripts/melee_value.py [samples_per_hero] [workers]
"""
import gzip
import json
import os
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from deadsim import Loadout, duel, game  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
from deadsim.accuracy import default_distance, hero_default_skill  # noqa: E402

HEROES = ["Abrams", "Billy", "Apollo", "Yamato", "Drifter", "Venator", "Shiv", "Calico", "Silver", "Infernus", "Haze"]
# melee item -> a same-cost non-melee comparison item
ITEMS = {"Melee Lifesteal": "Extra Health", "Spirit Strike": "Extra Spirit",
         "Melee Charge": "Swift Striker", "Spirit Snatch": "Bullet Resilience", "Lifestrike": "Bullet Resilience",
         "Crushing Fists": "Leech"}
MAX_TIME = 30.0


def build_at(G, p, t):
    items = [i for i, bt, st, _ in p["items"] if i in G.items and bt <= t and (st == 0 or st > t) and G.items[i].cost > 0]
    snaps = [s for s in p["stats"] if s["time_stamp_s"] <= t] or p["stats"][:1]
    return items, snaps[-1]["net_worth"]


def score(r, a_max, b_max):
    win = 1.0 if r.winner and "(A)" in r.winner else 0.0 if r.winner else 0.5
    return win, max(0.0, r.a_hp) / a_max - max(0.0, r.b_hp) / b_max


def run(job):
    hero, cases = job
    G = game()
    load_heroes()
    out = {}
    sk = hero_default_skill(hero)
    variants = {"no melee": (replace(sk, melee_rate=0.0, melee_by_items=None, combo_melee=False), None, None), "real melee": (sk, None, None)}
    for it, alt in ITEMS.items():   # paired: only cases owning neither item
        variants["+" + it] = (sk, it, alt)
        variants["+" + alt + " (vs " + it + ")"] = (sk, alt, it)
    dist = default_distance(hero)
    for name, (skill, extra, other) in variants.items():
        w = m = n = 0
        for items, souls, fid, fitems, fsouls in cases:
            its = list(items)
            if extra:
                x = G.item(extra)
                if x.id in its or G.item(other).id in its:
                    continue
                its.append(x.id)
            a = Loadout(hero, its, souls=souls + (G.item(extra).cost if extra else 0), skill=skill)
            b = Loadout(fid, fitems, souls=fsouls, skill=hero_default_skill(fid))
            from deadsim.fight import make_fighter  # noqa: F401
            r = duel(a, b, distance=dist, max_time=MAX_TIME)
            from deadsim.build import compute_stats
            am = compute_stats(hero, its, souls=a.souls).max_health
            bm = compute_stats(fid, fitems, souls=fsouls).max_health
            s1, s2 = score(r, am, bm)
            w += s1
            m += s2
            n += 1
        out[name] = (w / n if n else None, m / n if n else None, n)
    return hero, out


def main():
    per = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
    G = game()
    rnd = random.Random(5)
    ms = [json.loads(line) for line in gzip.open(os.path.join(ROOT, "validation", "matches_sample.jsonl.gz"))]
    jobs = []
    for hero in HEROES:
        hid = G.hero(hero).id
        cases = []
        pool = [(m, p) for m in ms for p in m["players"] if p["hero_id"] == hid]
        rnd.shuffle(pool)
        for m, p in pool:
            foes = [q for q in m["players"] if q["team"] != p["team"] and q["hero_id"] in G.heroes]
            for _ in range(2):
                t = m["duration_s"] * rnd.uniform(0.35, 0.9)
                f = rnd.choice(foes)
                items, souls = build_at(G, p, t)
                fitems, fsouls = build_at(G, f, t)
                cases.append((items, souls, f["hero_id"], fitems, fsouls))
            if len(cases) >= per:
                break
        jobs.append((hero, cases))
    res = {}
    with ProcessPoolExecutor(workers) as ex:
        for hero, out in ex.map(run, jobs):
            res[hero] = out
            print(f"\n{hero} (n={len(dict(jobs)[hero])})")
            for k, (w, m, n) in out.items():
                if w is not None:
                    print(f"   {k:42s} win {w:5.1%}  HP margin {m:+.3f}  (n={n})")
    json.dump(res, open(os.path.join(ROOT, "validation", "melee_value.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
