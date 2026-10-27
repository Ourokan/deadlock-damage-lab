"""Violet's Still Life draws in Phantom+ replays (fight-length raw damage events): how long a draw lasts, how many
complete (end in the big Damage hit, i.e. the stun), the Kaplan-Meier curve of breaking (deadsim/heroes/artist.py
SKETCH_BREAK) and Violet's gun hits per second while drawing vs when engaged.

A draw: the attacker's Still Life ticks on one victim with gaps < 0.6 s. Complete: its last hit is its biggest and
more than twice its median tick. Kills (victim at 0 hp) censor the break curve.

usage: python3 -I still_life_draws.py [raw dir]   (default: project folder analysis/work/fight_length/raw)
"""
import collections
import gzip
import json
import os
import statistics
import sys

RAW = "/mnt/project-files/analysis/work/fight_length/raw"
VIOLET = 86
STILL_LIFE, GUN = 3612874202, 2482363834
GAP_S = 0.6
GRID = [0.25 * k for k in range(11)]   # 0..2.5 s


def read(fn):
    hero, ev = {}, []
    for line in gzip.open(fn, "rt"):
        r = json.loads(line)
        if r["k"] == "ctl":
            hero[r["a"]] = int(r["s"])
        elif r["k"] == "dmg" and r.get("s"):
            ab, hp, _ = r["s"].split("|")
            ev.append((r["tick"] / 64, r["a"] // 100000, r["a"] % 100000, int(ab), r["v"], float(hp)))
    ev.sort()
    return hero, ev


def main(raw):
    draws, gun = [], collections.Counter()
    for fn in sorted(os.listdir(raw)):
        hero, ev = read(os.path.join(raw, fn))
        for pawn in [p for p, h in hero.items() if h == VIOLET]:
            mine = [e for e in ev if e[1] == pawn and e[2] in hero and e[2] != pawn]
            cur, own = {}, []
            for t, _, v, ab, x, hp in mine:
                if ab != STILL_LIFE:
                    continue
                if v in cur and t - cur[v][-1][0] < GAP_S:
                    cur[v].append((t, x, hp))
                else:
                    if v in cur:
                        own.append(cur[v])
                    cur[v] = [(t, x, hp)]
            own += cur.values()
            draws += own
            wins = [(d[0][0], d[-1][0]) for d in own if d[-1][0] - d[0][0] > 1.0]
            for e in mine:
                if e[3] == GUN:
                    gun["in" if any(a <= e[0] <= b for a, b in wins) else "out"] += 1
            gun["draw_s"] += sum(b - a for a, b in wins)
            gun["engaged_s"] += len({int(e[0]) for e in mine})
    rows = []
    for d in draws:
        med = statistics.median(x for _, x, _ in d)
        done = d[-1][1] == max(x for _, x, _ in d) and d[-1][1] > 2 * med
        rows.append((d[-1][0] - d[0][0], done, d[-1][2] <= 0))
    n = len(rows)
    dur = sorted(r[0] for r in rows)
    print(f"{n} draws; duration p25/50/75/90 {[round(dur[int(q * (n - 1))], 2) for q in (.25, .5, .75, .9)]}; "
          f"complete {sum(r[1] for r in rows) / n:.3f}; end in a kill {sum(r[2] for r in rows) / n:.3f}")
    cd = sorted(r[0] for r in rows if r[1])
    print("complete draws' duration p05/25/50:", [round(cd[int(q * (len(cd) - 1))], 3) for q in (.05, .25, .5)])
    ev = sorted((t, not done and not kill) for t, done, kill in rows)
    s, i, out = 1.0, 0, []
    for g in GRID:
        while i < n and ev[i][0] <= g:
            if ev[i][1]:
                s *= 1 - 1 / (n - i)
            i += 1
        out.append(round(1 - s, 3))
    print("P(broken by t), t = 0, 0.25, ..., 2.5 s:", out)
    print(f"gun hits/s while drawing {gun['in'] / max(1e-9, gun['draw_s']):.2f}, "
          f"engaged {(gun['in'] + gun['out']) / max(1, gun['engaged_s']):.2f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else RAW)
