"""When Victor's Aura of Suffering is on in real Phantom+ fights, from replays: data/aura_timing.json.

The aura is a toggle whose damage ramps from MinDPS to MaxDPS over AbilityDuration while it stays on. Real Victors
keep it on between fights: in about half their fights it is already on (and partly ramped) at the fight's first hit,
which is why real aura damage lands from the first second (P(first aura hit by 1 s) 0.46) while the sim's, held to
the cast-timing curve, came late (0.11, mean damage time 9.0 s against real 5.2).

The cast-timing curve was the wrong event for it: the ability's cooldown starts when the aura is toggled OFF (every
cooldown start sits at the end of a run of aura ticks, none at a run's start), so fit_cast_timing.py's "first cast"
of the aura was its first toggle-off in the fight. Read the aura from its hits instead.

Input: the fight-length replays (every hero-vs-hero DamageEvent, fight_length/fetch_fights.py). Aura runs: Victor's
aura ticks (every TickRate s on each enemy in the radius) with gaps up to RUN_GAP_S. Fights: pair fights as
wolf_timing.py (two enemy heroes trading, gaps < GAP_S s, >= MIN_HITS hits both ways), counted only once he has the
aura (his first aura hit of the match came earlier). The aura is on at a fight's start when a run spans it.

Output per phase (lane before LANE_MIN, late from LATE_MIN minutes):
- carried: the share of fights that start with the aura on;
- on_for: QBINS equal-probability values of how long it had been on then (s; the ramp has run that long);
- holds: QBINS equal-probability times of the toggle-on in the other fights (the first run starting in the fight,
  one TickRate before its first tick; Kaplan-Meier, the fight end censors; None = not by HORIZON).
Read by deadsim/heroes/frank.py (AuraOfSuffering.draw_plan, Mechanics.execute_timing).

usage: python3 -I aura_timing.py [--write]
"""
import collections
import glob
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "fight_length"))
sys.path.insert(0, os.path.join(HERE, "..", "cast_timing"))
import fit_length as FL  # noqa: E402
import opener_timing as OT  # noqa: E402
import wolf_timing as W  # noqa: E402

FIGHTS = W.FIGHTS
SAMPLE = W.SAMPLE
OUT = os.path.join(ROOT, "data", "aura_timing.json")
VICTOR = 66
AURA = 1472593493     # ability_frank_painaura (MurmurHash2 of the class name, seed 0x31415926)
TICK = 0.25           # the aura's TickRate
RUN_GAP_S = 1.0       # longer without a tick ends a run (toggled off, or no enemy in the radius)
LANE_MIN, LATE_MIN = 9.0, 25.0
QBINS = 20
HORIZON = 20.0


def quantiles(xs):
    xs = sorted(xs)
    return [round(xs[min(len(xs) - 1, int((b + 0.5) / QBINS * len(xs)))], 2) for b in range(QBINS)]


def holds(rows):
    """rows (toggle-on s or None, fight length s): QBINS equal-probability values, None past the share on by
    HORIZON (wolf_timing's fine-grid Kaplan-Meier)."""
    out = W.km_holds(rows)
    grid, curve = W.km_fine(rows, HORIZON)
    return [None if v is None or (b + 0.5) / QBINS > curve[-1] else v for b, v in enumerate(out)]


def runs_of(ticks):
    runs = []
    for t in ticks:
        if runs and t - runs[-1][1] <= RUN_GAP_S + 1e-6:
            runs[-1][1] = t
        else:
            runs.append([t, t])
    return runs


def main():
    files = sorted(glob.glob(FIGHTS + "*.ndjson.gz"))
    sample = FL.load_sample(SAMPLE, {os.path.basename(f).split(".")[0] for f in files})
    per = collections.defaultdict(lambda: {"n": 0, "carried": [], "rows": []})
    players = 0
    for fn in files:
        mid = os.path.basename(fn).split(".")[0]
        if mid not in sample:
            continue
        hero, ev = OT.read(fn)
        by_hero = {p["hero_id"]: p for p in sample[mid]["players"]}
        if VICTOR not in by_hero:
            continue
        for pawn in [p for p, h in hero.items() if h == VICTOR]:
            players += 1
            ticks = sorted({e[0] for e in ev if e[1] == pawn and e[6] == AURA})
            if not ticks:
                continue
            runs = runs_of(ticks)
            for t0, t1 in W.pair_fights(ev, pawn, hero, by_hero):
                if t0 <= ticks[0]:
                    continue   # aura not used yet in the match (not skilled)
                minute = t0 / 60   # replay clock, as victor_revive.py
                ph = "lane" if minute < LANE_MIN else "late" if minute >= LATE_MIN else "mid"
                d = per[ph]
                d["n"] += 1
                on = next((r for r in runs if r[0] < t0 <= r[1] + RUN_GAP_S), None)
                if on is not None:
                    d["carried"].append(t0 - on[0] + TICK)
                    continue
                first = next((r[0] for r in runs if t0 <= r[0] <= t1), None)
                d["rows"].append((None if first is None else max(0.0, first - t0 - TICK), t1 - t0))
    out = {"source": f"{players} Victor players in Phantom+ replays, pair fights after his first aura hit "
                     "(sim/scripts/mechanics/aura_timing.py)",
           "note": "per phase: carried = share of fights starting with the aura on; on_for = equal-probability "
                   "seconds it had been on at the start (the ramp's progress); holds = equal-probability toggle-on "
                   "times (s) in the other fights (null = not by 20 s)",
           "phases": {}}
    for ph in ("lane", "mid", "late"):
        d = per[ph]
        if not d["n"]:
            continue
        rows = d["rows"]
        grid, curve = W.km_fine(rows, HORIZON)
        row = {"fights": d["n"], "carried": round(len(d["carried"]) / d["n"], 3),
               "on_for": quantiles(d["carried"]), "holds": holds(rows)}
        out["phases"][ph] = row
        by = [round(curve[int(t / W.STEP)], 3) for t in (1, 3, 6, 20)]
        print(f"{ph}: {d['n']} fights, carried {row['carried']}, on for (median) {row['on_for'][QBINS // 2]} s; "
              f"other fights toggled on by 1/3/6/20 s {by}")
        print("  on_for", row["on_for"])
        print("  holds ", row["holds"])
    if "--write" in sys.argv:
        with open(OUT, "w") as fh:
            json.dump(out, fh, indent=1)
            fh.write("\n")
        print("wrote", OUT)


if __name__ == "__main__":
    main()
