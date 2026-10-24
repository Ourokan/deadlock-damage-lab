"""Check: the sim's gun damage per hit on heroes vs the real one, per hero, from the same replays as fit_guns.py.

Real: gun damage on enemy heroes / gun hits on them (validation/gun_calib/gun_stats.json.gz, replay DamageEvents,
pooled over each hero's players, whole match). Sim: the damage audit's duels (scripts/damage_audit.py: real builds
at 30/60/90% of the match, real enemy) for the same heroes in the Phantom+ sample, gun damage / gun hits. Only
one-bullet guns (a shotgun volley is one replay damage event but several sim hits). The sim's later sampling points
make every ratio a little high.

A hit that deals too little leaves too many hits for the same gun damage, and every on-hit item (Tesla Bullets,
Capacitor, Mystic Shot, Siphon Bullets) procs on hits: that is how Graves' items came out ~2x real in the audit.
With the data's falloff (start 7.6 m, 50% by 17 m), and shots beyond the 20 m tether counted as 0-damage hits, the
sim's Graves hit dealt 0.60x the real one while the other one-bullet guns sat at 0.8-1.6x (median 1.07). Now the tether
has no falloff (gun_calibration.json "falloff": false) and out-of-range shots miss (Engine.gun_reach): 0.92x.

usage: python3 hit_damage.py [sample.jsonl.gz] [players per hero=40]
Output: validation/gun_calib/hit_damage.json
"""
import collections
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import damage_audit as A  # noqa: E402
from deadsim import engine, game  # noqa: E402

MIN_PLAYERS = 5


def real_per_hit():
    rows = json.load(gzip.open(os.path.join(ROOT, "validation", "gun_calib", "gun_stats.json.gz"), "rt"))
    by = collections.defaultdict(lambda: [0.0, 0, 0])
    for r in rows:
        if r["hits"] >= 50 and r["pellets"] == r["hits"]:
            b = by[r["hero_id"]]
            b[0] += r["gun_damage"]
            b[1] += r["hits"]
            b[2] += 1
    return {h: (d / n, c) for h, (d, n, c) in by.items() if c >= MIN_PLAYERS}


def sim_per_hit(sample, heroes, per_hero):
    cur = [0.0, 0.0]
    orig = engine.Engine.damage

    def counted(self, src, dst, raw, kind, source, *a, **k):
        r = orig(self, src, dst, raw, kind, source, *a, **k)
        if r and source == "gun" and src.name.endswith("(A)"):
            cur[0] += r
            cur[1] += k.get("hits", 0) or 0
        return r

    engine.Engine.damage = counted
    try:
        ms = [json.loads(line) for line in gzip.open(sample, "rt")]
        out = {}
        for h in heroes:
            cur[:] = [0.0, 0.0]
            for job in [(m, p["slot"]) for m in ms for p in m["players"] if p["hero_id"] == h][:per_hero]:
                A.sim_player(job)
            if cur[1]:
                out[h] = cur[0] / cur[1]
        return out
    finally:
        engine.Engine.damage = orig


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sample = args[0] if args else os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
    per_hero = int(args[1]) if len(args) > 1 else 40
    G = game()
    # one replay damage event per pellet volley vs one sim hit per pellet: shotguns can't be compared this way
    real = {h: v for h, v in real_per_hit().items() if h in G.heroes and G.heroes[h].weapon.get("bullets", 1) == 1}
    sim = sim_per_hit(sample, sorted(real), per_hero)
    rows = []
    for h, (r, n) in real.items():
        if h in sim:
            rows.append({"hero_id": h, "name": G.heroes[h].name, "replay_players": n, "real": round(r, 2),
                         "sim": round(sim[h], 2), "sim_over_real": round(sim[h] / r, 3)})
    rows.sort(key=lambda x: x["sim_over_real"])
    for x in rows:
        print(f"{x['name']:16s} real {x['real']:6.2f} sim {x['sim']:6.2f} sim/real {x['sim_over_real']:.2f}")
    dst = os.path.join(ROOT, "validation", "gun_calib", "hit_damage.json")
    json.dump({"source": "validation/gun_calib/gun_stats.json.gz vs damage_audit duels on " + os.path.basename(sample),
               "players_per_hero": per_hero, "heroes": rows}, open(dst, "w"), indent=1)
    print("->", dst)


if __name__ == "__main__":
    main()
