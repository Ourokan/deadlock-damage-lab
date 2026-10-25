"""Victor's Shocking Reanimation carried over from earlier fights, from Phantom+ replays: data/victor_revive.json.

The ult triggers on lethal damage and then has a 240 s cooldown (145 s at T3), so in real games it is often still on
cooldown when the next fight starts: no revive in that fight, and the T1 bonus (+fire rate, spirit damage per
bullet "while on cooldown") is on from the first shot. A sim duel used to start with it ready every time.

Input: the fight-length replays (every hero-vs-hero DamageEvent, fight_length/fetch_fights.py) and the cast-timing
replays (ability cooldown starts per pawn, cast_timing/fetch_ability_casts.py) of the same matches. A cast is a
cooldown start equal to the game time (tick/64 - start = the replay's most common offset; other starts are cooldown
cuts). A Victor fight starts at a hit between him and an enemy hero after more than GAP_S s without one.
For each fight start: seconds since his last cast (None = not cast yet in the match), by game phase (lane before
LANE_MIN, late from LATE_MIN minutes, the overall search's 10k / 27k net worth).

Output: QBINS equal-probability values per phase (None = not cast before; the sim then starts with it ready), read
by deadsim/heroes/frank.py: the duel starts with it on cooldown for (cooldown - since) s when since < cooldown.
Also prints the ult's real damage split (small per-bullet T1 hits vs the revive blast).

usage: python3 -I victor_revive.py [--write]
"""
import bisect
import collections
import glob
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(HERE, "..", "fight_length"))
import fit_length as FL  # noqa: E402

FIGHTS = "/mnt/project-files/analysis/work/fight_length/raw/"
CASTS = "/mnt/project-files/analysis/work/cast_timing/raw/"
OUT = os.path.join(ROOT, "data", "victor_revive.json")
VICTOR, REVIVE = 66, 3493884851
GAP_S = FL.GAP_S
LANE_MIN, LATE_MIN = 9.0, 25.0
QBINS = 20
BLAST_MIN = 100.0    # a revive hit this big is the blast, smaller ones are the T1 per-bullet damage


def phase(t):
    m = t / 60
    return "lane" if m < LANE_MIN else "late" if m >= LATE_MIN else "mid"


def main():
    since = collections.defaultdict(list)
    small = blast = total = 0.0
    n_vic = n_cast = 0
    for fn in sorted(glob.glob(FIGHTS + "*.ndjson.gz")):
        cf = CASTS + os.path.basename(fn)
        if not os.path.exists(cf):
            continue
        hero, ev = FL.read(fn)
        vic = [p for p, h in hero.items() if h == VICTOR]
        if not vic:
            continue
        rows = [json.loads(line) for line in gzip.open(cf, "rt")]
        mode = collections.Counter(round(r["tick"] / 64 - r["v"], 1) for r in rows).most_common(1)[0][0]
        for line in gzip.open(fn, "rt"):
            r = json.loads(line)
            if r["k"] == "dmg" and r.get("s") and r["a"] // 100000 in vic and hero.get(r["a"] % 100000):
                total += r["v"]
                if int(r["s"].split("|")[0]) == REVIVE:
                    if r["v"] >= BLAST_MIN:
                        blast += r["v"]
                    else:
                        small += r["v"]
        for p in vic:
            n_vic += 1
            cs = sorted(r["tick"] / 64 for r in rows if r["a"] == p and int(r["s"]) == REVIVE
                        and abs(r["tick"] / 64 - r["v"] - mode) < 0.3)
            n_cast += len(cs)
            last = -1e9
            for t, a, v, *_ in ev:
                if p not in (a, v) or not hero.get(a) or not hero.get(v):
                    continue
                if t - last > GAP_S:
                    k = bisect.bisect_left(cs, t)
                    since[phase(t)].append(t - cs[k - 1] if k > 0 else None)
                last = t
    print(f"{n_vic} Victors, {n_cast} revives ({n_cast / max(1, n_vic):.1f} a match)")
    print(f"ult damage {small + blast:.0f} = {(small + blast) / total:.3f} of his hero damage: "
          f"T1 per-bullet {small / max(1, small + blast):.2f}, blast {blast / max(1, small + blast):.2f}")
    out = {"source": "Phantom+ replays (sim/scripts/mechanics/victor_revive.py): seconds since Victor's last Shocking "
                     "Reanimation at the start of his fights, equal-probability bins, null = not cast yet", "phases": {}}
    for ph in ("lane", "mid", "late"):
        v = since[ph]
        key = sorted(v, key=lambda x: (x is None, x or 0.0))
        qs = [key[min(len(key) - 1, int((i + 0.5) / QBINS * len(key)))] for i in range(QBINS)]
        out["phases"][ph] = [None if x is None else round(x, 1) for x in qs]
        on = {cd: sum(1 for x in v if x is not None and x < cd) / len(v) for cd in (145, 240)}
        print(f"{ph:5s} fights {len(v):5d}  on cooldown at start if cd 145 s: {on[145]:.2f}, 240 s: {on[240]:.2f}")
    if "--write" in sys.argv:
        json.dump(out, open(OUT, "w"), indent=1)
        print("wrote", OUT)


if __name__ == "__main__":
    main()
