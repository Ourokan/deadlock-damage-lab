"""When Victor's Pain Battery first lands in real Phantom+ fights, from replays: data/battery_timing.json.

Pain Battery charges from any damage Victor takes (his own aura and Jumpstart included) and keeps the charge between
fights, so real Victors often walk into a fight with it full: its first hit lands by 1 / 3 / 6 s of a pair fight in
0.12 / 0.27 / 0.43 of them (opener_timing.py). The sim's duels start with the battery empty and fill it from the
duel's own damage (40% of max health), so the first bolt came late (0.01 / 0.05 / 0.27, mean 8.3 s against real
5.0) and the ability read under while the aura, which fills it, read over.

Fights: pair fights as aura_timing.py (two enemy heroes trading, gaps < GAP_S s, >= MIN_HITS hits both ways), counted
once he has hit with the battery earlier in the match (skilled). First use = his first Pain Battery hit on any enemy
hero in the fight, seconds after its start (Kaplan-Meier, the fight end censors).

Output per phase (lane before LANE_MIN, late from LATE_MIN minutes, as aura_timing.py): holds = QBINS
equal-probability first-hit times (s; None = not by HORIZON). Read by deadsim/heroes/frank.py (PainBattery.draw_plan,
Mechanics.execute_timing): the first bolt of a fight goes out at the drawn time whatever the duel's charge (the real
time already holds the charge carried in and the fight's own), later ones need a full battery from the duel.

usage: python3 -I battery_timing.py [--write]
"""
import collections
import glob
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
import aura_timing as A  # noqa: E402

OUT = os.path.join(ROOT, "data", "battery_timing.json")
VICTOR = A.VICTOR
BATTERY = 2043074967   # ability_frank_shocktarget2
QBINS = A.QBINS
HORIZON = A.HORIZON


def holds(rows):
    """rows (first hit s or None, fight length s): QBINS equal-probability values to HORIZON, None past it."""
    grid, curve = W.km_fine(rows, HORIZON)
    out = []
    for b in range(QBINS):
        p = (b + 0.5) / QBINS
        k = next((k for k, v in enumerate(curve) if v >= p), None)
        if k is None:
            out.append(None)
        elif k == 0:
            out.append(0.0)
        else:
            lo = curve[k - 1]
            out.append(round(grid[k] - W.STEP * (curve[k] - p) / max(1e-9, curve[k] - lo), 2))
    return out, curve


def main():
    files = sorted(glob.glob(W.FIGHTS + "*.ndjson.gz"))
    sample = FL.load_sample(W.SAMPLE, {os.path.basename(f).split(".")[0] for f in files})
    per = collections.defaultdict(list)
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
            team = by_hero[VICTOR]["team"]
            hits = sorted(e[0] for e in ev if e[1] == pawn and e[6] == BATTERY and e[2] != pawn
                          and by_hero.get(hero.get(e[2]), {}).get("team", team) != team)
            if not hits:
                continue
            for t0, t1 in W.pair_fights(ev, pawn, hero, by_hero):
                if t0 <= hits[0]:
                    continue   # not skilled / not used yet in the match
                minute = t0 / 60
                ph = "lane" if minute < A.LANE_MIN else "late" if minute >= A.LATE_MIN else "mid"
                first = next((t for t in hits if t0 <= t <= t1), None)
                per[ph].append((None if first is None else first - t0, t1 - t0))
    out = {"source": f"{players} Victor players in Phantom+ replays, pair fights after his first Pain Battery hit "
                     "(sim/scripts/mechanics/battery_timing.py)",
           "note": "per phase: holds = equal-probability seconds from a fight's start to his first Pain Battery hit "
                   "(Kaplan-Meier, null = not by 20 s)",
           "phases": {}}
    for ph in ("lane", "mid", "late"):
        rows = per[ph]
        if not rows:
            continue
        q, curve = holds(rows)
        out["phases"][ph] = {"fights": len(rows), "holds": q}
        by = [round(curve[int(t / W.STEP)], 3) for t in (1, 3, 6, 20)]
        print(f"{ph}: {len(rows)} fights, first hit by 1/3/6/20 s {by}")
        print("  holds", q)
    if "--write" in sys.argv:
        with open(OUT, "w") as fh:
            json.dump(out, fh, indent=1)
            fh.write("\n")
        print("wrote", OUT)


if __name__ == "__main__":
    main()
