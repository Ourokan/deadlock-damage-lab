"""Victor's Shocking Reanimation carried over from earlier fights, from Phantom+ replays: data/victor_revive.json.

The ult triggers on lethal damage and then has a 240 s cooldown (145 s at T3), so in real games it is often still on
cooldown when the next fight starts: no revive in that fight, and the T1 bonus (+fire rate, spirit damage per
bullet "while on cooldown") is on from the first shot. A sim duel used to start with it ready every time.

Input: the fight-length replays (every hero-vs-hero DamageEvent, fight_length/fetch_fights.py) and the cast-timing
replays (ability cooldown starts per pawn, cast_timing/fetch_ability_casts.py) of the same matches. A cast is a
cooldown start equal to the game time (fit_cast_timing.real_casts: tick/64 - start = the offset of that stretch of the
replay; a pause moves it, other starts are cooldown cuts). Until 2026-10-27 this used the replay's one most common
offset, which dropped every cast after a pause (~40% of revives): since-last-cast came out too long, and the duel
started on cooldown in 29% of late fights where real Victors are in ~45%.
A Victor fight starts at a hit between him and an enemy hero after more than GAP_S s without one (his aura's
self-damage doesn't count: until 2026-10-27 its ticks out of combat made ~40% of the mid "fights"). The rest of a
fight he revives in counts as one more fight, started REVIVE_S after the cast: real fights with a revive in them last
~25 s vs 6-9 s and go on a mean 9-11 s after it (a fresh fight, half the fight's bullets, with the T1 bonus on), but in
a sim duel the reanimation blast mostly finishes its one foe.
For each fight start: seconds since his last cast (None = not cast yet in the match), by game phase: his net worth at
the fight start (the sample's stats snapshots, replay clock lined up by fit_length.clock_offset) under 10k / up to 27k
/ more, as frank.souls_phase reads it (a match the clock can't line up: lane before LANE_MIN, late from LATE_MIN
minutes; until 2026-10-27 every match was split by minutes, which put many 10k+ fights of the 30% duels in lane).

Output: QBINS equal-probability values per phase (None = not cast before; the sim then starts with it ready), read
by deadsim/heroes/frank.py: the duel starts with it on cooldown for (cooldown - since) s when since < cooldown.
Also prints the ult's real damage split (small per-bullet T1 hits vs the revive blast).

usage: python3 -I victor_revive.py [--parity even|odd] [--write [PATH]]   (--parity: only even / odd match ids)
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
sys.path.insert(0, os.path.join(HERE, "..", "cast_timing"))
import fit_length as FL  # noqa: E402
from fit_cast_timing import real_casts  # noqa: E402

FIGHTS = "/mnt/project-files/analysis/work/fight_length/raw/"
CASTS = "/mnt/project-files/analysis/work/cast_timing/raw/"
OUT = os.path.join(ROOT, "data", "victor_revive.json")
VICTOR, REVIVE = 66, 3493884851
GAP_S = FL.GAP_S
LANE_MIN, LATE_MIN = 9.0, 25.0
QBINS = 20
READY_CD = {"lane": 240.0, "mid": 145.0, "late": 145.0}   # its cooldown by phase (T3 -95 s from mid on in the sim)
REVIVE_S = 3.0       # RespawnDelay: the reanimation, where the rest of the fight starts
BLAST_MIN = 100.0    # a revive hit this big is the blast, smaller ones are the T1 per-bullet damage


SAMPLE = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")


def phase(t, stats=None, off=None):
    if stats and off is not None:
        nw = FL.nw_at(stats, t - off(t))
        return "lane" if nw < 10000 else "mid" if nw <= 27000 else "late"
    m = t / 60
    return "lane" if m < LANE_MIN else "late" if m >= LATE_MIN else "mid"


def main():
    since = collections.defaultdict(list)
    ready = collections.defaultdict(list)
    small = blast = total = 0.0
    n_vic = n_cast = n_nw = n_in = 0
    files = sorted(glob.glob(FIGHTS + "*.ndjson.gz"))
    if "--parity" in sys.argv:
        par = 0 if sys.argv[sys.argv.index("--parity") + 1] == "even" else 1
        files = [f for f in files if int(os.path.basename(f).split(".")[0]) % 2 == par]
    sample = FL.load_sample(SAMPLE, {os.path.basename(f).split(".")[0] for f in files})
    for fn in files:
        cf = CASTS + os.path.basename(fn)
        if not os.path.exists(cf):
            continue
        hero, ev = FL.read(fn)
        vic = [p for p, h in hero.items() if h == VICTOR]
        if not vic:
            continue
        m = sample.get(os.path.basename(fn).split(".")[0])
        off = FL.clock_offset(ev, hero, m) if m else None
        n_nw += off is not None
        rows = real_casts([json.loads(line) for line in gzip.open(cf, "rt")])
        for line in gzip.open(fn, "rt"):
            r = json.loads(line)
            if (r["k"] == "dmg" and r.get("s") and r["a"] // 100000 in vic and hero.get(r["a"] % 100000)
                    and r["a"] % 100000 not in vic):   # not his own self-damage
                total += r["v"]
                if int(r["s"].split("|")[0]) == REVIVE:
                    if r["v"] >= BLAST_MIN:
                        blast += r["v"]
                    else:
                        small += r["v"]
        for p in vic:
            n_vic += 1
            stats = next((q["stats"] for q in m["players"] if q["hero_id"] == VICTOR), None) if m else None
            cs = sorted(r["tick"] / 64 for r in rows if r["a"] == p and int(r["s"]) == REVIVE)
            n_cast += len(cs)
            last, fights = -1e9, []
            for t, a, v, *_ in ev:
                if p not in (a, v) or not hero.get(a) or not hero.get(v) or a == v:   # not his self-damage
                    continue
                if t - last > GAP_S:
                    k = bisect.bisect_left(cs, t)
                    since[phase(t, stats, off)].append(t - cs[k - 1] if k > 0 else None)
                    fights.append([t, t])
                fights[-1][1] = last = t
            # the rest of a fight he revives in counts as a fight of its own, started on cooldown
            for t in cs:
                if any(t0 <= t <= t1 for t0, t1 in fights):
                    since[phase(t, stats, off)].append(REVIVE_S)
                    n_in += 1
            # fights he starts with it ready: does he revive in it, how far in
            for t0, t1 in fights:
                ph = phase(t0, stats, off)
                k = bisect.bisect_left(cs, t0)
                if k > 0 and t0 - cs[k - 1] < READY_CD[ph]:
                    continue
                at = next((t - t0 for t in cs[k:k + 1] if t <= t1), None)
                ready[ph].append(at)
    print(f"{n_nw} matches phased by net worth")
    print(f"{n_vic} Victors, {n_cast} revives ({n_cast / max(1, n_vic):.1f} a match), {n_in} inside a fight")
    print(f"ult damage {small + blast:.0f} = {(small + blast) / total:.3f} of his hero damage: "
          f"T1 per-bullet {small / max(1, small + blast):.2f}, blast {blast / max(1, small + blast):.2f}")
    out = {"source": "Phantom+ replays (sim/scripts/mechanics/victor_revive.py): seconds since Victor's last Shocking "
                     "Reanimation at the start of his fights, equal-probability bins, null = not cast yet; in_fight: fights he "
                     "starts with it ready, share with a revive in them (p) and its time from the fight start (at)",
           "phases": {}, "in_fight": {}}
    for ph in ("lane", "mid", "late"):
        v = since[ph]
        key = sorted(v, key=lambda x: (x is None, x or 0.0))
        qs = [key[min(len(key) - 1, int((i + 0.5) / QBINS * len(key)))] for i in range(QBINS)]
        out["phases"][ph] = [None if x is None else round(x, 1) for x in qs]
        on = {cd: sum(1 for x in v if x is not None and x < cd) / len(v) for cd in (145, 240)}
        r = ready[ph]
        at = sorted(x for x in r if x is not None)
        out["in_fight"][ph] = {"p": round(len(at) / len(r), 4),
                               "at": [round(at[min(len(at) - 1, int((i + 0.5) / QBINS * len(at)))], 1) for i in range(QBINS)]}
        print(f"{ph:5s} ready fights {len(r)}: revives in {out['in_fight'][ph]['p']:.3f}, "
              f"median {at[len(at) // 2]:.1f} s in")
        print(f"{ph:5s} fights {len(v):5d}  on cooldown at start if cd 145 s: {on[145]:.2f}, 240 s: {on[240]:.2f}")
    if "--write" in sys.argv:
        i = sys.argv.index("--write") + 1
        path = sys.argv[i] if i < len(sys.argv) and not sys.argv[i].startswith("--") else OUT
        json.dump(out, open(path, "w"), indent=1)
        print("wrote", path)


if __name__ == "__main__":
    main()
