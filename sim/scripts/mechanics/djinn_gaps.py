"""Mirage's Djinn's Mark gaps in real fights, from Phantom+ replays: data/djinn_gaps.json.

Each gun hit applies a mark when the per-target ProcCooldown is ready and refreshes VictimStackDuration; marks that
get no new mark in that time pop on expiry. The sim's Mirage lands gun hits at a steady rate, so marks never expire
inside a duel: they build to MaxStacks and the active pops them at ~8 s. Real Mirage often stops hitting that target
for a while (casting, reloading, out of sight, another target): most first pops in real fights are low-stack expiry
pops (opener_timing.md: real first pop 9.8 s mean vs sim 12.6 s; P(popped by 6 s) 0.23 vs 0).

Input: the fight-length replays (every hero-vs-hero DamageEvent, fight_length/fetch_fights.py), fights as in
fit_length.py (two enemy heroes trading, gaps < 5 s, >= 4 hits both ways). In each Mirage fight the mark state is
replayed on his real gun hits on that enemy (base ProcCooldown): for each mark applied while the fight still goes on
for at least D s more, did the next mark come later than D s (the marks would expire)? The fight's own end is left
to the fight-length booking (marks applied less than D s before it are censored).

Output: P(no next mark within D s) for D on a 1 s grid, pooled and per half of the sample (even / odd match ids),
read by deadsim/heroes/mirage.py (MARK_GAPS).

usage: python3 -I djinn_gaps.py [--write]
"""
import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(HERE, "..", "fight_length"))
sys.path.insert(0, ROOT)
import fit_length as FL  # noqa: E402
import opener_timing as OT  # noqa: E402

RAW = "/mnt/project-files/analysis/work/fight_length/raw"
GRID = [float(d) for d in range(3, 13)]   # s of VictimStackDuration (5 base, 8 at T2, more with duration items)


def main():
    from deadsim import game
    G = game()
    src = OT.sources(G)
    weap = {w["id"] for w in json.load(open(os.path.join(ROOT, "..", "data", "game", "weapons.json")))}
    dm = next(s for s, v in src.items() if v[2] == "mirage_sand_phantom")
    mirage = next(h for h in G.heroes.values() if h.name == "Mirage")
    cd = float(next(a for a in mirage.abilities if a.class_name == "mirage_sand_phantom").props["ProcCooldown"])
    files = sorted(glob.glob(os.path.join(RAW, "*.ndjson.gz")))
    sample = FL.load_sample(os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz"),
                            {os.path.basename(f).split(".")[0] for f in files})
    tally = {h: {d: [0, 0] for d in GRID} for h in ("all", "even", "odd")}
    fights = 0
    for fn in files:
        mid = os.path.basename(fn).split(".")[0]
        m = sample.get(mid)
        if m is None:
            continue
        hero, ev = OT.read(fn)
        pawns = [a for a, h in hero.items() if h == mirage.id]
        if not pawns:
            continue
        pawn = pawns[0]
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
        half = "even" if int(mid) % 2 == 0 else "odd"
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
                end = f[-1][0]
                marks, ready = [], -1.0
                for e in f:
                    if e[1] == pawn and e[6] in weap and e[0] >= ready:
                        marks.append(e[0])
                        ready = e[0] + cd
                for d in GRID:
                    for i, t in enumerate(marks):
                        if t + d > end:
                            break
                        gap = marks[i + 1] - t if i + 1 < len(marks) else float("inf")
                        for h in ("all", half):
                            tally[h][d][0] += 1
                            tally[h][d][1] += gap > d
    res = {"source": f"{len(files)} Phantom+ replays, {fights} Mirage fights (scripts/mechanics/djinn_gaps.py)",
           "note": "P(no next Djinn's Mark within D s of a mark | the fight goes on D s more): the marks expire and "
                   "pop. Base ProcCooldown; marks replayed on Mirage's real gun hits on that enemy",
           "proc_cooldown": cd, "duration_s": GRID}
    for h, t in tally.items():
        res[h] = [round(t[d][1] / max(1, t[d][0]), 4) for d in GRID]
        res[f"{h}_marks"] = [t[d][0] for d in GRID]
    for h in ("all", "even", "odd"):
        print(h, dict(zip(GRID, res[h])))
    if "--write" in sys.argv:
        with open(os.path.join(ROOT, "data", "djinn_gaps.json"), "w") as fh:
            json.dump(res, fh, indent=1)
            fh.write("\n")


if __name__ == "__main__":
    main()
