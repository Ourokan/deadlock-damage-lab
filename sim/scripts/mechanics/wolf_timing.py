"""When Silver is in her wolf form in real Phantom+ fights, from replays: data/wolf_timing.json.

The sim's Lycan Curse starts every duel at 0 rage and fills it from her damage (and 1% a second), so she transforms
about 7-12 s into nearly every duel and never starts one in wolf form. In real fights she carries rage and the
cooldown from fights before: 12% of her fights start with her already in wolf form, she transforms in only ~1 in 3
of the rest, and when she does it is spread from the first second on. The wolf form came late, when the real fight is
mostly over (fight length booking), so its claws and abilities needed landing x length_corr fudges of 1.3-1.6.

Input: the fight-length replays (every hero-vs-hero DamageEvent, fight_length/fetch_fights.py). The wolf form is read
from her hits, not her casts (Lycan Curse's cooldown starts when the form ends, so a cooldown start is not the cast):
a run of wolf hits (Lycan Claws, Go For The Throat, Mauling Leap, Tail Whack) broken by a human-form hit (rifle,
Slam Fire, Boot Kick, Entangling Bola) or a WOLF_GAP_S gap, from 0.5 s before its first hit to 0.5 s after its last.
Fights: pair fights as fit_cast_timing.py (two enemy heroes trading, gaps < GAP_S s, >= MIN_HITS hits both ways).

Output: start_wolf, the share of fights that start inside a wolf run; holds, QBINS equal-probability times of the
first wolf run's start in the other fights (Kaplan-Meier, the fight end censors; None = not by HORIZON). Read by
deadsim/heroes/werewolf.py (LycanCurse.draw_plan, Mechanics.execute_timing). Also prints the wolf form's share of
fight time and of her damage, against which the sim is checked (validation/README.md "Silver's wolf form").

usage: python3 -I wolf_timing.py [--write]
"""
import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(HERE, "..", "fight_length"))
sys.path.insert(0, os.path.join(HERE, "..", "cast_timing"))
import fit_length as FL  # noqa: E402
import opener_timing as OT  # noqa: E402
import fit_cast_timing as CT  # noqa: E402

FIGHTS = "/mnt/project-files/analysis/work/fight_length/raw/"
SAMPLE = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
OUT = os.path.join(ROOT, "data", "wolf_timing.json")
SILVER = 80
# ability ids (MurmurHash2 of the class name, seed 0x31415926)
WOLF = {3995444919: "citadel_weapon_werewolf_claws", 2565763509: "ability_werewolf_frenzy",
        4009459244: "ability_werewolf_maulingleap", 3117047651: "ability_werewolf_cripplingslash"}
HUMAN = {3922245490: "citadel_weapon_werewolf_rifle", 1385849824: "ability_werewolf_unloadgun",
         2717130900: "ability_werewolf_kickflip", 3983754897: "ability_werewolf_netshot"}
WOLF_GAP_S = 6.0
EDGE_S = 0.5
QBINS = 20
HORIZON = CT.HORIZON


def wolf_runs(mine):
    runs = []
    for e in mine:
        if e[6] in HUMAN:
            if runs:
                runs[-1][2] = False
            continue
        if e[6] not in WOLF:
            continue
        if runs and runs[-1][2] and e[0] - runs[-1][1] <= WOLF_GAP_S + EDGE_S:
            runs[-1][1] = e[0] + EDGE_S
        else:
            runs.append([e[0] - EDGE_S, e[0] + EDGE_S, True])
    return [(a, b) for a, b, _ in runs]


def pair_fights(ev, pawn, hero, by_hero):
    pairs = collections.defaultdict(list)
    for e in ev:
        a, v = e[1], e[2]
        if pawn not in (a, v):
            continue
        pa, pv = by_hero.get(hero.get(a)), by_hero.get(hero.get(v))
        if pa is None or pv is None or pa["team"] == pv["team"]:
            continue
        pairs[min(a, v), max(a, v)].append(e)
    out = []
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
            out.append((f[0][0], f[-1][0] + EDGE_S))
    return out


def main():
    files = sorted(glob.glob(FIGHTS + "*.ndjson.gz"))
    sample = FL.load_sample(SAMPLE, {os.path.basename(f).split(".")[0] for f in files})
    rows, n_start = [], 0
    t_fight = t_wolf = 0.0
    dmg = collections.Counter()
    players = 0
    for fn in files:
        mid = os.path.basename(fn).split(".")[0]
        if mid not in sample:
            continue
        hero, ev = OT.read(fn)
        by_hero = {p["hero_id"]: p for p in sample[mid]["players"]}
        if SILVER not in by_hero:
            continue
        team = by_hero[SILVER]["team"]
        for pawn in [p for p, h in hero.items() if h == SILVER]:
            players += 1
            mine = [e for e in ev if e[1] == pawn]
            wins = wolf_runs(mine)

            def inw(t):
                return any(a <= t <= b for a, b in wins)
            for t0, t1 in pair_fights(ev, pawn, hero, by_hero):
                t_fight += t1 - t0
                t_wolf += sum(max(0.0, min(b, t1) - max(a, t0)) for a, b in wins)
                if inw(t0):
                    n_start += 1
                    rows.append(None)
                else:
                    first = next((a for a, b in wins if t0 <= a <= t1), None)
                    rows.append((None if first is None else first - t0, t1 - t0))
                for e in mine:
                    p = by_hero.get(hero.get(e[2]))
                    if t0 <= e[0] <= t1 and p is not None and p["team"] != team:
                        k = "wolf" if e[6] in WOLF else "human" if e[6] in HUMAN else "other"
                        dmg[k] += e[5]
                        if inw(e[0]):
                            dmg[k + "_in"] += e[5]
    km_rows = [r for r in rows if r is not None]
    curve = CT.km(km_rows)
    h = int(HORIZON / 0.5)
    holds = []
    for b in range(QBINS):
        p = (b + 0.5) / QBINS
        holds.append(None if p > curve[h] else round(CT.quantile(curve, p), 2))
    tot = sum(dmg[k] for k in ("wolf", "human", "other"))
    print(f"{players} Silver players, {len(rows)} fights, {t_fight:.0f} s")
    print(f"start in wolf form {n_start / len(rows):.3f}; wolf form up {t_wolf / t_fight:.3f} of fight time")
    print(f"wolf hits {dmg['wolf'] / tot:.3f} of her damage, human-form hits {dmg['human'] / tot:.3f}, "
          f"other {dmg['other'] / tot:.3f} ({dmg['other_in'] / max(1, dmg['other']):.2f} of it in wolf form)")
    print("first wolf run, fights not starting in it: by 2/5/10/20 s",
          [round(curve[int(t / 0.5)], 3) for t in (2, 5, 10, 20)])
    print("holds", holds)
    out = {"source": f"{players} Silver players in Phantom+ replays, {len(rows)} pair fights "
                     "(sim/scripts/mechanics/wolf_timing.py)",
           "note": "start_wolf: share of fights starting in wolf form; holds: equal-probability times (s) of the first "
                   "transform in the other fights (null = not by 20 s: on cooldown or held)",
           "start_wolf": round(n_start / len(rows), 3), "holds": holds,
           "real": {"wolf_uptime": round(t_wolf / t_fight, 3), "wolf_damage_share": round(dmg["wolf"] / tot, 3),
                    "human_damage_share": round(dmg["human"] / tot, 3)}}
    if "--write" in sys.argv:
        with open(OUT, "w") as fh:
            json.dump(out, fh, indent=1)
            fh.write("\n")
        print("wrote", OUT)


if __name__ == "__main__":
    main()
