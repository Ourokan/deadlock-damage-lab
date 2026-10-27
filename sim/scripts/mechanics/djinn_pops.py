"""Mirage's Djinn's Mark pops in real fights vs the sim's audit duels (2026-10-27, mirage.MARKS_OUTLAST).

real: the fight-length replays (fights as in fit_length.py, two enemy heroes trading). In each Mirage fight his
Djinn's Mark damage events on that enemy are the pops; marks are replayed on his real gun hits (base ProcCooldown,
cleared after VictimStackDuration without a mark). Per fight second: pops and marks; per pop: the marks it popped and
whether it came within VictimStackDuration - 0.5 s of the last mark (a cast) or later (an expiry pop; marks last 8 s
at T2, so some casts read as expiry).

sim: the damage audit's duels of the sample's Mirage players (4 draws), every pop and mark weighted as the audit books
it (P(the real fight still goes on) at the pop, or at the last mark with MARKS_OUTLAST), per fight second over the
same weights.

Found: real 0.72 pops / 10 s, 64% expiry, popped marks 1/2/3/4 = 58/23/16/2% (of pops with a replayed mark); the sim
popped 0.43 / 10 s (34% expiry): marks still on the target when a fight ended (a disengage) never popped, though in
game they pop on expiry anyway. With MARKS_OUTLAST 0.78 / 10 s, 53% expiry, 54/30/10/6%.

usage: python3 scripts/mechanics/djinn_pops.py real | sim [--off]   (from sim/; --off: MARKS_OUTLAST off)
"""
import collections
import glob
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(HERE, "..", "fight_length"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, ROOT)

RAW = "/mnt/project-files/analysis/work/fight_length/raw"
SAMPLE = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")


def report(pops, secs, marks, stacks, kinds):
    print(f"pops / 10 s {10 * pops / secs:.3f}  marks / 10 s {10 * marks / secs:.3f}")
    print("marks popped", {k: round(v / sum(stacks.values()), 3) for k, v in sorted(stacks.items())})
    print("cast / expiry", {k: round(v / pops, 3) for k, v in sorted(kinds.items())})


def real():
    import fit_length as FL
    import opener_timing as OT
    from deadsim import game
    G = game()
    weap = {w["id"] for w in json.load(open(os.path.join(ROOT, "..", "data", "game", "weapons.json")))}
    dm = next(s for s, v in OT.sources(G).items() if v[2] == "mirage_sand_phantom")
    mir = next(h for h in G.heroes.values() if h.name == "Mirage")
    ab = next(a for a in mir.abilities if a.class_name == "mirage_sand_phantom")
    cd, dur = float(ab.props["ProcCooldown"]), float(ab.props["VictimStackDuration"])
    files = sorted(glob.glob(os.path.join(RAW, "*.ndjson.gz")))
    sample = FL.load_sample(SAMPLE, {os.path.basename(f).split(".")[0] for f in files})
    fights, secs, pops, marks = 0, 0.0, 0, 0
    stacks, kinds = collections.Counter(), collections.Counter()
    for fn in files:
        m = sample.get(os.path.basename(fn).split(".")[0])
        if m is None:
            continue
        hero, ev = OT.read(fn)
        pawn = next((a for a, h in hero.items() if h == mir.id), None)
        if pawn is None:
            continue
        by_hero = {p["hero_id"]: p for p in m["players"]}
        pairs = collections.defaultdict(list)
        for e in ev:
            a, v = e[1], e[2]
            if pawn not in (a, v):
                continue
            pa, pv = by_hero.get(hero.get(a)), by_hero.get(hero.get(v))
            if pa is None or pv is None or pa["team"] == pv["team"]:
                continue
            pairs[v if a == pawn else a].append(e)
        for es in pairs.values():
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
                fights += 1
                secs += f[-1][0] - f[0][0] + 0.5
                n, last, ready = 0, -99.0, -1.0
                for e in f:
                    if e[1] != pawn:
                        continue
                    if e[6] == dm:
                        pops += 1
                        if n:
                            stacks[min(4, n)] += 1
                        kinds["cast" if e[0] - last < dur - 0.5 else "expiry"] += 1
                        n = 0
                    elif e[6] in weap and e[0] >= ready:
                        if e[0] - last > dur:
                            n = 0
                        n, last, ready, marks = n + 1, e[0], e[0] + cd, marks + 1
    print(f"{len(files)} replays, {fights} Mirage fights, {secs:.0f} fight s")
    report(pops, secs, marks, stacks, kinds)


def sim(off):
    os.environ.setdefault("AUDIT_NORM", "total")
    import damage_audit as A
    from deadsim import game
    from deadsim.heroes import mirage as M
    from deadsim.mechanics import LENGTH_STEP
    if off:
        M.MARKS_OUTLAST = False
    w = collections.Counter()
    stacks, kinds = collections.Counter(), collections.Counter()
    now = {"k": "cast"}
    pop0, cast0, expire0, dealt0 = M.DjinnsMark.pop, M.DjinnsMark.cast, M.DjinnsMark.expire, M.DjinnsMark.on_damage_dealt

    def pop(self, c):
        x = c.engine.length_w(t=c.state["last"]) if M.MARKS_OUTLAST else c.engine.length_w()
        w["pops"] += x
        stacks[min(4, c.state["stacks"])] += x
        kinds[now["k"]] += x
        return pop0(self, c)

    def expire(self, c, gen):
        now["k"] = "expiry"
        try:
            return expire0(self, c, gen)
        finally:
            now["k"] = "cast"

    def dealt(self, c, target, hit):
        g = c.state["gen"]
        r = dealt0(self, c, target, hit)
        if c.state["gen"] != g:
            w["marks"] += c.engine.length_w()
        return r

    M.DjinnsMark.pop, M.DjinnsMark.expire, M.DjinnsMark.on_damage_dealt = pop, expire, dealt
    duel0 = A.duel

    def duel(*a, **k):
        r = duel0(*a, **k)
        c, t = k["mechanics"].fight_length, 0.0
        while t < r.time:
            x = t / LENGTH_STEP
            i = int(x)
            w["secs"] += 0.05 * (c[-1] if i >= len(c) - 1 else c[i] + (c[i + 1] - c[i]) * (x - i))
            t += 0.05
        return r

    A.duel = duel
    mir = next(h for h in game().heroes.values() if h.name == "Mirage").id
    for seed in range(4):
        A.SEED = seed
        for line in gzip.open(SAMPLE):
            m = json.loads(line)
            for p in m["players"]:
                if p["hero_id"] == mir:
                    A.sim_player((m, p["slot"]))
    print("MARKS_OUTLAST", M.MARKS_OUTLAST)
    report(w["pops"], w["secs"], w["marks"], stacks, kinds)


if __name__ == "__main__":
    if sys.argv[1:2] == ["real"]:
        real()
    else:
        sim("--off" in sys.argv)
