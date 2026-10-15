"""Build data/skill_defaults.json (population aim per hero) from validation/matches_sample.jsonl.gz.

Per hero: hero-only accuracy (Enemy Hero Accuracy Hits/Shots) and headshot rate (Headshots/Hits) percentiles
across player-matches with >= MIN_SHOTS shots, plus the median fight distance from the bullet-hit histogram
("Outgoing Bullet Dist" counts all bullet hits, creeps included, so it is only a proxy for duel range)."""
import gzip
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from deadsim.accuracy import DIST_PREFIX, HEADS, HITS, SHOTS, distance_profile  # noqa: E402
from deadsim.data import game  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
MIN_SHOTS = 300


def pct(xs, q):
    xs = sorted(xs)
    i = (len(xs) - 1) * q
    lo = int(i)
    return xs[lo] + (xs[min(lo + 1, len(xs) - 1)] - xs[lo]) * (i - lo)


def summarize(rows):
    acc = [r[0] for r in rows]
    hs = [r[1] for r in rows]
    dist = [r[2] for r in rows if r[2] is not None]
    q = {"p25": .25, "p50": .5, "p75": .75, "p90": .9}
    return {"n": len(rows),
            "accuracy": {k: round(pct(acc, v), 4) for k, v in q.items()},
            "headshot": {k: round(pct(hs, v), 4) for k, v in q.items()},
            "median_distance_m": round(statistics.median(dist), 1) if dist else 15.0}


def main():
    src = os.path.join(ROOT, "validation", "matches_sample.jsonl.gz")
    by_hero, allrows, badges = {}, [], []
    for line in gzip.open(src):
        m = json.loads(line)
        badges.append(m.get("badge"))
        for p in m["players"]:
            c = p.get("custom") or {}
            if c.get(SHOTS, 0) < MIN_SHOTS:
                continue
            med, _ = distance_profile({k: v for k, v in c.items() if k.startswith(DIST_PREFIX)})
            row = (c[HITS] / c[SHOTS], c.get(HEADS, 0) / max(1, c[HITS]), med)
            by_hero.setdefault(p["hero_id"], []).append(row)
            allrows.append(row)
    G = game()
    names = {h.id: h.name for h in G.heroes.values()} if isinstance(G.heroes, dict) else {h.id: h.name for h in G.heroes}
    out = {"source": f"{len(badges)} matches, badge >= {min(badges)}, players with >= {MIN_SHOTS} hero-aimed shots",
           "all": summarize(allrows),
           "heroes": {str(h): dict(name=names.get(h, str(h)), **summarize(rows))
                      for h, rows in sorted(by_hero.items()) if len(rows) >= 15}}
    dst = os.path.join(ROOT, "data", "skill_defaults.json")
    json.dump(out, open(dst, "w"), indent=1)
    print(json.dumps(out["all"]))
    for h, r in sorted(out["heroes"].items(), key=lambda x: -x[1]["accuracy"]["p50"]):
        print(f"{r['name']:16s} n={r['n']:4d} acc p50 {r['accuracy']['p50']:.3f} hs {r['headshot']['p50']:.3f} dist {r['median_distance_m']}")


if __name__ == "__main__":
    main()
