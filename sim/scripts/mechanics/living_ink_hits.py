"""Violet's Living Ink in Phantom+ replays (fight-length raw damage events + cast_timing raw cooldown rows): how many
heroes' hits a cast lands, and how its hits cut her other cooldowns (deadsim/heroes/artist.py INK_HOMING).

- Hits per cast: each real Living Ink cast (fit_cast_timing.real_casts) in a fight (one of her other hits on a hero
  within 3 s) owns the Living Ink hero hits until it runs out (10 s) or the next cast; "sustained": at least 3 of her
  other hits on heroes in that window.
- Cuts: a cooldown row that moves an ability's start back is a cut; how many hero hits have a cut row within 0.2 s,
  and the size of the cuts.

usage: python3 scripts/mechanics/living_ink_hits.py [fight_length raw dir] [cast_timing raw dir]
"""
import collections
import gzip
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cast_timing"))
import fit_cast_timing as F  # noqa: E402

FL = "/mnt/project-files/analysis/work/fight_length/raw"
CT = "/mnt/project-files/analysis/work/cast_timing/raw"
VIOLET, INK = 86, 836615329
T = 64
WINDOW_S = 10.0


def read(fn):
    hero, ev = {}, []
    for line in gzip.open(fn, "rt"):
        r = json.loads(line)
        if r["k"] == "ctl":
            hero[r["a"]] = int(r["s"])
        elif r["k"] == "dmg" and r.get("s"):
            ev.append((r["tick"] / T, r["a"] // 100000, r["a"] % 100000, int(r["s"].split("|")[0])))
    return hero, ev


def main(fl, ct):
    n = collections.Counter()
    cut_size = collections.Counter()
    for fn in sorted(set(os.listdir(fl)) & set(os.listdir(ct))):
        hero, ev = read(os.path.join(fl, fn))
        pawns = [p for p, h in hero.items() if h == VIOLET]
        if not pawns:
            continue
        rows = sorted((json.loads(line) for line in gzip.open(os.path.join(ct, fn), "rt")), key=lambda r: r["tick"])
        casts = F.real_casts(rows)
        for p in pawns:
            mine = [e for e in ev if e[1] == p and e[2] in hero and e[2] != p]
            ink = sorted({round(e[0], 3) for e in mine if e[3] == INK})
            other = [e[0] for e in mine if e[3] != INK]
            ts = sorted(r["tick"] / T for r in casts if r["a"] == p and int(r["s"]) == INK)
            for i, t in enumerate(ts):
                end = min(t + WINDOW_S, ts[i + 1] if i + 1 < len(ts) else 1e9)
                if not any(t - 3 <= x <= t + 3 for x in other):
                    continue
                hits = sum(1 for x in ink if t <= x < end)
                n["casts"] += 1
                n["hits"] += hits
                if sum(1 for x in other if t <= x <= end) >= 3:
                    n["sustained_casts"] += 1
                    n["sustained_hits"] += hits
            last, cut_t = {}, []
            for r in rows:
                if r["a"] != p:
                    continue
                s = int(r["s"])
                if s in last and r["v"] < last[s] - 0.05:
                    cut_size[round(last[s] - r["v"], 1)] += 1
                    cut_t.append(r["tick"] / T)
                last[s] = r["v"]
            for x in ink:
                n["hero_hits"] += 1
                n["hero_hits_cut"] += any(abs(x - c) < 0.2 for c in cut_t)
    print(f"Living Ink casts in fights {n['casts']}: hero hits per cast {n['hits'] / max(1, n['casts']):.2f}; "
          f"sustained {n['sustained_casts']}: {n['sustained_hits'] / max(1, n['sustained_casts']):.2f}")
    print(f"hero hits with a cooldown cut within 0.2 s: {n['hero_hits_cut'] / max(1, n['hero_hits']):.3f} "
          f"of {n['hero_hits']}; commonest cut sizes {cut_size.most_common(4)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else FL, sys.argv[2] if len(sys.argv) > 2 else CT)
