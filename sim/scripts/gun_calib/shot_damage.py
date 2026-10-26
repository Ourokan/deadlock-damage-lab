"""Check: the sim's gun damage per shot vs the real one, per hero, on the SAME players as the replays.

Real: a player's gun damage on enemy heroes / the shots they fired within 4 s of hero damage (shots_fight4; the API's
hero-aimed shots are ~1.0 x that per pellet), validation/gun_calib/gun_stats.json.gz. Sim: the damage audit's duels
(scripts/damage_audit.sim_player: the player's real build, net worth and aim against a real enemy) for the same
player-matches, gun damage / trigger pulls (Engine.fire), at FRACS evenly spaced through the match.

Why not the Phantom+ sample against the replay players (what the Drifter thread first read: Abrams 2.0x real per
shot): different players and the audit's 30/60/90% sampling points. Abrams' 16 replay players aimed 0.228 per pellet
where the sample's 138 aim 0.278 (1.22x), and his hits come early (laning) while 30/60/90% sits late (1.17x). On the
same players sampled evenly Abrams reads 1.19x (95% 1.06-1.35), Haze 0.99, Wraith 1.00 (2026-10-26).

Damage the game books under an item (Express Shot's proc shot, Engine.damage book=) is not gun damage in the replays,
so it is left out here too: counting it read Deadman Danny 1.18x real per shot, 0.97x without it.

The two extra columns split the ratio: hits per shot (the sim's per-pellet hits against the replay's gun hit events;
a shotgun volley is one replay event, so only one-bullet guns read right there) and damage per hit. Across 31 guns
the per-shot ratios spread ~9% (sd) around 1.01 beyond sampling noise, with no shared cause in the ~1.2x group
(2026-10-26): Kelvin/Holliday/Apollo land more hits per shot (the API accuracy the sim aims with vs the replay's fight
shots, a known ~13% per-hero spread, gun_calibration memory), Billy/Paige deal more per hit (their weapon buffs: Close
Quarters, Plot Armor, Opening Rounds), Abrams/Silver are shotguns. Item weapon buffs check out within each hero.

usage: python3 shot_damage.py <replay matches.jsonl.gz> [hero,hero|all] [workers]
The matches file holds gun_stats' matches in fetch_validation.py format; when it does not exist it is fetched from the
API first (70 matches, ~1.3 MB, a minute). Output: per hero, geometric mean of the per-player sim/real ratios with a
95% range (heroes with 3+ players).
"""
import collections
import gzip
import json
import math
import os
import statistics
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import damage_audit as A  # noqa: E402
import landing_rates as L  # noqa: E402
from deadsim import engine, game  # noqa: E402

FRACS = tuple(round(0.05 * i, 2) for i in range(1, 20))
MIN_PLAYERS = 3
_acc = collections.Counter()
_damage, _run = engine.Engine.damage, engine.Engine.run


def _counted_damage(self, src, dst, raw, kind, source, *a, **k):
    amt = _damage(self, src, dst, raw, kind, source, *a, **k)
    if source == "gun" and k.get("book") is None and self.fighters and src is self.fighters[0]:
        _acc["dmg"] += amt or 0.0
        if amt:
            _acc["hits"] += k.get("hits", 0) or 0
    return amt


def _counted_run(self, a, b, one_way=False):
    r = _run(self, a, b, one_way)
    _acc["shots"] += a.shots_fired
    return r


def sim_job(job):
    _acc.clear()
    engine.Engine.damage, engine.Engine.run, L.FRACS = _counted_damage, _counted_run, FRACS
    try:
        A.sim_player(job)
    finally:
        engine.Engine.damage, engine.Engine.run = _damage, _run
    return dict(_acc)


def fetch(dst, rows):
    import concurrent.futures as cf
    import fetch_validation as F
    ids = sorted({r["match_id"] for r in rows})
    with cf.ThreadPoolExecutor(6) as ex:
        ms = [m for m in ex.map(F.get, ids) if m]
    with gzip.open(dst, "wt") as out:
        for m in ms:
            out.write(json.dumps(F.slim(m)) + "\n")
    print(f"{len(ms)}/{len(ids)} replay matches -> {dst}", flush=True)


def main():
    sample = sys.argv[1]
    which = sys.argv[2] if len(sys.argv) > 2 else "all"
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else os.cpu_count()
    G = game()
    heroes = set(G.heroes) if which == "all" else {G.hero(x.strip()).id for x in which.split(",")}
    rows = json.load(gzip.open(os.path.join(ROOT, "validation", "gun_calib", "gun_stats.json.gz"), "rt"))
    if not os.path.exists(sample):
        fetch(sample, rows)
    real = {(r["match_id"], r["hero_id"]): r for r in rows if r["shots_fight4"] and r["gun_damage"]}
    jobs = []
    for line in gzip.open(sample, "rt"):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] in heroes and (m["match_id"], p["hero_id"]) in real and L.gun_known(p):
                jobs.append((m, p["slot"]))
    ratios, splits = collections.defaultdict(list), collections.defaultdict(list)
    with ProcessPoolExecutor(workers) as ex:
        for (m, slot), s in zip(jobs, ex.map(sim_job, jobs, chunksize=2)):
            hid = next(p["hero_id"] for p in m["players"] if p["slot"] == slot)
            r = real[m["match_id"], hid]
            if s.get("shots") and s.get("dmg"):
                ratios[hid].append((s["dmg"] / s["shots"]) / (r["gun_damage"] / r["shots_fight4"]))
                if s.get("hits") and r["pellets"]:
                    splits[hid].append(((s["hits"] / s["shots"]) / (r["pellets"] / r["shots_fight4"]),
                                        (s["dmg"] / s["hits"]) / (r["gun_damage"] / r["pellets"])))
    rows = []
    for hid, rs in ratios.items():
        if len(rs) < MIN_PLAYERS:
            continue
        lg = [math.log(x) for x in rs]
        mu, se = statistics.mean(lg), statistics.stdev(lg) / math.sqrt(len(lg))
        hit, per = (math.exp(statistics.mean(math.log(x[i]) for x in splits[hid])) if splits[hid] else math.nan for i in (0, 1))
        rows.append((math.exp(mu), math.exp(mu - 2 * se), math.exp(mu + 2 * se), len(rs), G.heroes[hid].name, hit, per))
    for g, lo, hi, n, name, hit, per in sorted(rows):
        print(f"{name:16s} sim/real per shot {g:5.2f}  95% {lo:.2f}-{hi:.2f}  players {n:3d}  hits/shot {hit:5.2f}  per hit {per:5.2f}")


if __name__ == "__main__":
    main()
