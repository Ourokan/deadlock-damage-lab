"""Real win edge of heal (and other) items split by how many enemies bought Healbane (0 / 1 / 2+), same hero, 5-min
purchase bin and slot+tier strata as item_win_edge (no lead buckets), Ritualist+ full matches.

    python3 sim/scripts/sustain/healbane_split.py 2026-10-31,2026-11-01 "Radiant Regeneration,Healing Nova"   # repo root,
    data/builds/player_builds -> the shared day files
"""
import gzip, json, glob, sys, math
from collections import defaultdict
items = {x["id"]: x for x in json.load(open("data/game/shop_items.json"))}
name = {i: x["name"] for i, x in items.items()}
TIER = {i: x["tier"] for i, x in items.items()}; SLOT = {i: x["slot"] for i, x in items.items()}
HB = [i for i, n in name.items() if n == "Healbane"][0]
days = sys.argv[1].split(",")
focus = sys.argv[2].split(",")
fid = {i for i, n in name.items() if n in focus}
# cells[(item, hbgroup)][(hero, bin, slot,tier)] -> [n_item, w_item]; others same key
cnt = defaultdict(lambda: [0, 0])
for d in days:
    rows = defaultdict(list)
    for l in gzip.open(f"data/builds/player_builds/{d}.jsonl.gz", "rt"):
        r = json.loads(l)
        rows[r["match_id"]].append(r)
    for mid, ps in rows.items():
        if len(ps) != 12: continue
        if (ps[0].get("badge") or 0) < 50: continue
        for p in ps:
            enemies = [q for q in ps if q["won"] != p["won"]]
            ehb = sum(any(it == HB for it, *_ in q["purchases"]) for q in enemies)
            g = min(ehb, 2)
            seen = set()
            for it, t, *_ in p["purchases"]:
                if it in seen or it not in TIER or not 1 <= TIER[it] <= 4: continue
                seen.add(it)
                key = (p["hero_id"], t // 300, SLOT[it], TIER[it], g)
                c = cnt[(it,) + key]; c[0] += 1; c[1] += p["won"]
# edge per focus item per group
agg = defaultdict(lambda: defaultdict(lambda: [0, 0]))   # key without item -> item -> [n,w]
for (it, *key), c in cnt.items():
    a = agg[tuple(key)][it]; a[0] += c[0]; a[1] += c[1]
for f in sorted(fid, key=lambda i: name[i]):
    out = []
    for g in (0, 1, 2):
        num = den = var = 0.0
        for key, by in agg.items():
            if key[-1] != g or f not in by: continue
            n, w = by[f]
            on = sum(v[0] for i, v in by.items() if i != f); ow = sum(v[1] for i, v in by.items() if i != f)
            if on < 5: continue
            p = (w + ow) / (n + on)
            num += n * (w / n - ow / on); den += n; var += n * n * p * (1 - p) * (1 / n + 1 / on)
        out.append(f"enemyHB={g}{'+' if g==2 else ''}: n {int(den):6d} edge {100*num/den:+.2f} +- {100*math.sqrt(var)/den:.2f}" if den else f"enemyHB={g}: -")
    print(f"{name[f]:24s} | " + " | ".join(out))
