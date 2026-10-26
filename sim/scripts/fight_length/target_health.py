"""Target health under gun fire: real Phantom+ replays against the sim's duels.

Health-conditional effects (Opening Rounds: +weapon damage on targets above 50% health; Tankbuster, Mystic Reverb,
Rupture: damage from the target's current health) depend on how full the target is when it gets hit. This measures,
for gun damage to enemy heroes, how it spreads over the target's health share at the hit (before it):

- real: every gun hit of a hero on an enemy hero in the replays (fetch_fights.py extracts, weapon id from
  data/game/weapons.json; health before = health after + damage, capped at max), and the same inside the fights of
  fit_length.py (two enemy heroes trading, gaps < 5 s, >= 4 hits both ways). Also, per fight: the target's health
  share at its first hit (entry) and the damage the target takes from other enemies during the fight per damage from
  its pair enemy (third parties);
- sim: the damage audit's duels (real builds both sides, the searches' skills, real fight length), the main
  fighter's gun damage to its target, each hit x P(fight still going) as the audit books it.

usage: python3 -I target_health.py real <raw dir> [--sample PATH]
       python3 -I target_health.py sim [max_players=1500] [workers]
"""
import collections
import glob
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import fit_length as FL  # noqa: E402
from opener_timing import read  # noqa: E402

BINS = 10   # health share deciles
HALF = int(os.environ["TH_HALF"]) if os.environ.get("TH_HALF") else None   # match id parity (split-half check)


def show(name, hist):
    tot = sum(hist.values()) or 1.0
    above = sum(v for k, v in hist.items() if k >= BINS // 2) / tot
    deciles = " ".join(f"{hist.get(k, 0.0) / tot:.2f}" for k in range(BINS))
    print(f"{name:34s} above half {above:.3f}   by decile (0-10% .. 90-100%) {deciles}")
    return above


def real(raw, sample_path):
    weap = {w["id"] for w in json.load(open(os.path.join(ROOT, "..", "data", "game", "weapons.json")))}
    files = sorted(glob.glob(os.path.join(raw, "*.ndjson.gz")))
    sample = FL.load_sample(sample_path, {os.path.basename(f).split(".")[0] for f in files})
    h_all, h_fight = collections.Counter(), collections.Counter()
    h_phase = collections.defaultdict(collections.Counter)
    entry = collections.Counter()
    pair_dmg = others_dmg = 0.0
    for fn in files:
        mid = os.path.basename(fn).split(".")[0]
        m = sample.get(mid)
        if m is None or (HALF is not None and int(mid) % 2 != HALF):
            continue
        hero, ev = read(fn)
        off = FL.clock_offset([e[:6] for e in ev], hero, m)
        by_hero = {p["hero_id"]: p for p in m["players"]}
        pairs = collections.defaultdict(list)
        taken = collections.defaultdict(list)   # victim -> [(t, attacker, dmg)] from enemy heroes
        for e in ev:
            t, a, v, hp, hmax, dmg, ab = e
            pa, pv = by_hero.get(hero.get(a)), by_hero.get(hero.get(v))
            if pa is None or pv is None or pa["team"] == pv["team"]:
                continue
            taken[v].append((t, a, dmg))
            if ab in weap and hmax > 0:
                h_all[min(BINS - 1, int(min(1.0, (hp + dmg) / hmax) * BINS))] += dmg
            pairs[min(a, v), max(a, v)].append(e)
        for (x, y), es in pairs.items():
            runs = []
            for e in es:
                if not runs or e[0] - runs[-1][-1][0] > FL.GAP_S:
                    runs.append([])
                runs[-1].append(e)
            for f in runs:
                death = next((k for k, e in enumerate(f) if e[3] <= 0), None)
                if death is not None:
                    f = f[:death + 1]
                if len(f) < FL.MIN_HITS or len({(e[1], e[2]) for e in f}) < 2:
                    continue
                t0, t1 = f[0][0], f[-1][0]
                ph = None
                if off is not None:
                    g = t0 - off(t0)
                    nw = [FL.nw_at(by_hero[hero[z]]["stats"], g) for z in (x, y)]
                    if None not in nw:
                        s = sum(nw) / 2
                        ph = next(n for n, lo, hi in FL.PHASES if lo <= s < hi)
                for vic, att in ((x, y), (y, x)):
                    first = next((e for e in f if e[2] == vic), None)
                    if first is None:
                        continue
                    entry[min(BINS - 1, int(min(1.0, (first[3] + first[5]) / first[4]) * BINS))] += 1
                    for t, a, d in taken[vic]:
                        if t0 <= t <= t1:
                            if a == att:
                                pair_dmg += d
                            else:
                                others_dmg += d
                for e in f:
                    if e[6] in weap and e[4] > 0:
                        b = min(BINS - 1, int(min(1.0, (e[3] + e[5]) / e[4]) * BINS))
                        h_fight[b] += e[5]
                        if ph:
                            h_phase[ph][b] += e[5]
    show("real, all gun hits on heroes", h_all)
    show("real, gun hits in pair fights", h_fight)
    for ph in ("lane", "mid", "late"):
        show(f"  {ph}", h_phase[ph])
    tot = sum(entry.values())
    print("real target health at its first hit in a fight, by decile:",
          " ".join(f"{entry.get(k, 0) / tot:.2f}" for k in range(BINS)), f"(fights x2 {tot})")
    print(f"real third parties: damage to the target from others / from its pair enemy in the fight: "
          f"{others_dmg / max(1.0, pair_dmg):.3f}")


_hist = None
SEEN = os.environ.get("TH_SEEN", "")


def sim_player(job):
    import damage_audit as A
    from deadsim import engine
    global _hist
    if SEEN:
        from deadsim import mechanics
        mechanics.TARGET_HEALTH_ALL = True
        if os.environ.get("TH_ASSIST"):
            mechanics.TARGET_ASSIST = float(os.environ["TH_ASSIST"])
    _hist = collections.Counter()
    orig = engine.Engine.damage

    def hooked(self, src, dst, raw, kind, source, *a, **k):
        before = dst.hp_frac if dst.alive else 0.0
        if SEEN and dst.alive:
            before = dst.item_hp_frac
        w = self.length_w()
        amt = orig(self, src, dst, raw, kind, source, *a, **k)
        if source == "gun" and k.get("book") is None and self.fighters and src is self.fighters[0] and amt:
            _hist[min(BINS - 1, int(min(1.0, before) * BINS))] += amt * w
        return amt
    engine.Engine.damage = hooked
    try:
        A.sim_player(job)
    finally:
        engine.Engine.damage = orig
    return dict(_hist)


def sim(max_players, workers):
    import gzip
    from concurrent.futures import ProcessPoolExecutor
    import landing_rates as L
    from deadsim import game
    G = game()
    path = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
    jobs = []
    for line in gzip.open(path):
        m = json.loads(line)
        if HALF is not None and m["match_id"] % 2 != HALF:
            continue
        for p in m["players"]:
            if p["hero_id"] in G.heroes and L.gun_known(p):
                jobs.append((m, p["slot"]))
    random.Random(1).shuffle(jobs)
    jobs = jobs[:max_players]
    h = collections.Counter()
    with ProcessPoolExecutor(workers) as ex:
        for r in ex.map(sim_player, jobs, chunksize=4):
            h.update(r)
    show(f"sim duels ({len(jobs)} players)", h)


def main():
    args = sys.argv[1:]
    sample_path = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
    if "--sample" in args:
        sample_path = args.pop(args.index("--sample") + 1)
        args.remove("--sample")
    if args[0] == "real":
        real(args[1], sample_path)
    else:
        sim(int(args[1]) if len(args) > 1 else 1500, int(args[2]) if len(args) > 2 else os.cpu_count())


if __name__ == "__main__":
    main()
