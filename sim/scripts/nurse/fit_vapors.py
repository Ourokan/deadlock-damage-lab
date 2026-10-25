"""Fit nurse.SELF_CAST: the share of Wretched Vapors' rush Nurse gets on herself in a duel, so that the crash damage
she takes matches real play.

Real (234 Phantom+ replays, hero-vs-hero DamageEvents): crash damage on Nurse = REAL_SHARE of all hero damage she
takes. For each SELF_CAST in a grid, duel every Nurse player of the sample as scripts/landing_rates.py does and print
the sim share; the deferral scales linearly with SELF_CAST, so pick the value at REAL_SHARE.

usage: python3 scripts/nurse/fit_vapors.py <sample.jsonl.gz> [workers]
"""
import collections
import gzip
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from deadsim import Loadout, duel, game  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
from deadsim.accuracy import default_distance  # noqa: E402
import landing_rates as L  # noqa: E402

REAL_SHARE = 0.049
NURSE = 87


def run(job):
    m, slot, w = job
    load_heroes()
    import deadsim.heroes.nurse as N
    N.SELF_CAST = w
    G = game()
    me = next(p for p in m["players"] if p["slot"] == slot)
    foes = [p for p in m["players"] if p["team"] != me["team"] and p["hero_id"] in G.heroes]
    import random
    rnd = random.Random(m["match_id"] * 31 + slot)
    out = collections.Counter()
    for frac in L.FRACS:
        t = m["duration_s"] * frac
        items, souls = L.build_at(me, t)
        foe = rnd.choice(foes)
        fitems, fsouls = L.build_at(foe, t)
        r = duel(Loadout(NURSE, items, souls=souls, skill=L.skill_of(me)),
                 Loadout(foe["hero_id"], fitems, souls=fsouls, skill=L.skill_of(foe)),
                 distance=default_distance("Nurse Harrow"), max_time=L.FIGHT_TIME)
        out["crash"] += r.b_dmg.get(N.CRASH_SRC, 0.0)
        out["taken"] += sum(r.b_dmg.values())
    return w, out


def main():
    sample = sys.argv[1]
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
    jobs = []
    for line in gzip.open(sample):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] == NURSE and L.gun_known(p):
                jobs.append((m, p["slot"]))
    grid = (0.1, 0.2, 0.4, 1.0)
    tot = {w: collections.Counter() for w in grid}
    with ProcessPoolExecutor(workers) as ex:
        for w, c in ex.map(run, [(m, s, w) for w in grid for m, s in jobs], chunksize=8):
            tot[w].update(c)
    print(f"real crash share of damage taken {REAL_SHARE}; {len(jobs)} Nurse players")
    for w in grid:
        print(f"  SELF_CAST {w:4.2f}: sim crash share {tot[w]['crash'] / max(1.0, tot[w]['taken']):.4f}")


if __name__ == "__main__":
    main()
