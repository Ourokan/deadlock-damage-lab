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

- items: for the items that deal damage from the target's current health (CURRENT_HEALTH_ITEMS), the target's
  health share before each of the item's hits on an enemy hero, real (every hit in the replays) and sim (the damage
  audit's duels, the main fighter's item hits x P(fight still going)); real also gives the item's damage per hit / the
  target's current health and / its max health by health share, to tell which one it scales with.

usage: python3 -I target_health.py real <raw dir> [--sample PATH]
       python3 -I target_health.py sim [max_players=1500] [workers]
       python3 -I target_health.py items real <raw dir> | items sim [max_players=3000] [workers]
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


# items dealing damage from the target's current health: class -> game item name (sim source)
CURRENT_HEALTH_ITEMS = {"upgrade_magic_shock": "Tankbuster", "upgrade_mystic_reverb": "Mystic Reverb",
                        "upgrade_rupture": "Decay", "upgrade_eldritch_shot": "Haunting Shot",
                        "upgrade_toxic_bullets": "Toxic Bullets"}   # Toxic: max health (control)


def show_items(rows):
    for name, (n, s_hp, hist) in sorted(rows.items()):
        tot = sum(hist.values()) or 1.0
        deciles = " ".join(f"{hist.get(k, 0.0) / tot:.2f}" for k in range(BINS))
        print(f"{name:16s} hits {n:8.0f}  mean health share {s_hp / max(1e-9, n):.3f}  by decile {deciles}")


def items_real(raw):
    from deadsim import game
    G = game()
    ids = {it.id: it.name for it in G.items.values() if it.class_name in CURRENT_HEALTH_ITEMS}
    rows = {n: [0, 0.0, collections.Counter()] for n in ids.values()}
    ratio = collections.defaultdict(lambda: [0.0, 0.0, 0.0, 0])   # (item, decile) -> [dmg/cur, dmg/max, -, n]
    for fn in sorted(glob.glob(os.path.join(raw, "*.ndjson.gz"))):
        mid = int(os.path.basename(fn).split(".")[0])
        if HALF is not None and mid % 2 != HALF:
            continue
        hero, ev = read(fn)
        for t, a, v, hp, hmax, dmg, ab in ev:
            name = ids.get(ab)
            if name is None or hmax <= 0 or a == v or hero.get(v) is None:
                continue
            before = min(hmax, hp + dmg)
            if before <= 0:
                continue
            frac = before / hmax
            b = min(BINS - 1, int(frac * BINS))
            r = rows[name]
            r[0] += 1
            r[1] += frac
            r[2][b] += 1
            q = ratio[name, b]
            q[0] += dmg / before
            q[1] += dmg / hmax
            q[3] += 1
    show_items(rows)
    print("damage per hit / current health and / max health, by health share decile (scales with the flat one):")
    for name in sorted(rows):
        cur = " ".join(f"{ratio[name, b][0] / max(1, ratio[name, b][3]):.3f}" for b in range(BINS))
        mx = " ".join(f"{ratio[name, b][1] / max(1, ratio[name, b][3]):.3f}" for b in range(BINS))
        print(f"{name:16s} /cur {cur}\n{'':16s} /max {mx}")


def items_sim_player(job):
    import damage_audit as A
    from deadsim import engine
    names = set(CURRENT_HEALTH_ITEMS.values())
    out = {}
    orig = engine.Engine.damage

    def hooked(self, src, dst, raw, kind, source, *a, **k):
        before = (dst.hp_frac, dst.item_hp / dst.max_hp) if dst.alive else None
        w = self.length_w()
        amt = orig(self, src, dst, raw, kind, source, *a, **k)
        if source in names and before and self.fighters and src is self.fighters[0] and amt:
            r = out.setdefault(source, [0.0, 0.0, 0.0, [0.0] * BINS])
            r[0] += w
            r[1] += w * before[0]
            r[2] += w * before[1]
            r[3][min(BINS - 1, int(min(1.0, before[1]) * BINS))] += w
        return amt
    engine.Engine.damage = hooked
    try:
        A.sim_player(job)
    finally:
        engine.Engine.damage = orig
    return out


def items_sim(max_players, workers):
    import gzip
    from concurrent.futures import ProcessPoolExecutor
    import landing_rates as L
    from deadsim import game
    G = game()
    cls = set(CURRENT_HEALTH_ITEMS)
    jobs = []
    for line in gzip.open(os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")):
        m = json.loads(line)
        if HALF is not None and m["match_id"] % 2 != HALF:
            continue
        for p in m["players"]:
            its = {G.items[i[0]].class_name for i in p.get("items", []) if i[0] in G.items}
            if p["hero_id"] in G.heroes and its & cls:
                jobs.append((m, p["slot"]))
    random.Random(1).shuffle(jobs)
    jobs = jobs[:max_players]
    tot = {}
    with ProcessPoolExecutor(workers) as ex:
        for r in ex.map(items_sim_player, jobs, chunksize=4):
            for k, v in r.items():
                t = tot.setdefault(k, [0.0, 0.0, 0.0, [0.0] * BINS])
                for i in range(3):
                    t[i] += v[i]
                t[3] = [x + y for x, y in zip(t[3], v[3])]
    print(f"sim duels ({len(jobs)} holders)")
    for name, (n, h, s, hist) in sorted(tot.items()):
        deciles = " ".join(f"{x / max(1e-9, n):.2f}" for x in hist)
        print(f"{name:16s} hits {n:8.1f}  mean health share {h / n:.3f}, as the item sees it {s / n:.3f}  "
              f"by decile (seen) {deciles}")


def main():
    args = sys.argv[1:]
    sample_path = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
    if "--sample" in args:
        sample_path = args.pop(args.index("--sample") + 1)
        args.remove("--sample")
    if args[0] == "items":
        if args[1] == "real":
            items_real(args[2])
        else:
            items_sim(int(args[2]) if len(args) > 2 else 3000, int(args[3]) if len(args) > 3 else os.cpu_count())
        return
    if args[0] == "real":
        real(args[1], sample_path)
    else:
        sim(int(args[1]) if len(args) > 1 else 1500, int(args[2]) if len(args) > 2 else os.cpu_count())


if __name__ == "__main__":
    main()
