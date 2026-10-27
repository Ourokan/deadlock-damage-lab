"""Fit nurse.ALLY_VAPORS: the share of a duel fighter's incoming damage an allied Nurse's Wretched Vapors defers
(Mechanics.ally_vapors), so the crash credit the damage audit books matches real Phantom+ matches.

Real Nurses mostly vapor their allies (nurse.SELF_CAST 0.2); the game credits the crash to whoever hit the vapored
ally, under ability_nurse_adrenaline_rush. Real: that source's share of all hero damage of the players whose enemy
team has a Nurse (validation sample damage_sources), split by whether the duel foe is the Nurse herself (her
self-cast, already modeled) or not. Sim: the damage audit's duels (scripts/damage_audit.sim_player, AUDIT_SEED
draws) of the same players for each share in a grid; the crash scales about linearly with it.

Found (2026-10-27, 600 matches): real crash 1.50% of the damage of players facing a Nurse (0.00% of those who
don't), the duels 0.08% with her self-cast only; ALLY_VAPORS 0.018 gives 1.48% (0.04: 3.2%).

usage: python3 scripts/nurse/fit_ally_vapors.py [sample.jsonl.gz] [workers]   (from sim/)
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
os.environ.setdefault("AUDIT_NORM", "total")
import damage_audit as DA  # noqa: E402
import landing_rates as L  # noqa: E402
from deadsim import game  # noqa: E402

CRASH = "ability_nurse_adrenaline_rush"
GRID = (0.0, 0.018, 0.04)


def run(job):
    m, slot, w = job
    import deadsim.heroes.nurse as N
    N.ALLY_VAPORS = w
    hid, d, _ = DA.sim_player((m, slot))
    return w, d.get(CRASH, 0.0), sum(v for k, v in d.items() if not k.startswith("_"))


def main():
    sample = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
    G = game()
    nurse_id = next(h.id for h in G.heroes.values() if h.name == "Nurse Harrow")
    jobs, real = [], collections.defaultdict(lambda: [0.0, 0.0])
    for line in gzip.open(sample):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] not in G.heroes or not L.gun_known(p):
                continue
            facing = any(x["hero_id"] == nurse_id for x in m["players"] if x["team"] != p["team"])
            d = {k: v for k, v in p["damage_sources"].items() if k not in L.CATEGORY}
            r = real["facing" if facing else "not"]
            r[0] += d.get(CRASH, 0.0)
            r[1] += sum(d.values())
            if facing and p["hero_id"] != nurse_id:
                jobs.append((m, p["slot"]))
    for k, (c, t) in real.items():
        print(f"real crash share, players {k} a Nurse: {c / max(1.0, t):.4f}")
    tot = {w: [0.0, 0.0] for w in GRID}
    with ProcessPoolExecutor(workers) as ex:
        for w, c, t in ex.map(run, [(m, s, w) for w in GRID for m, s in jobs], chunksize=8):
            tot[w][0] += c
            tot[w][1] += t
    print(f"{len(jobs)} players facing a Nurse (not Nurse)")
    for w in GRID:
        print(f"  ALLY_VAPORS {w:5.3f}: sim crash share {tot[w][0] / max(1.0, tot[w][1]):.4f}")


if __name__ == "__main__":
    main()
