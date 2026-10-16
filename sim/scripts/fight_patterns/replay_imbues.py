"""Which ability each hero imbues, from replay extracts (fetch_replays.py output).

Quicksilver Reload's bonus damage is its own damage event (item id as ability_id) on the same tick as the imbued
ability's hit, so every Quicksilver hit votes for the hero ability that hit the same victim within TOL ticks.
Mercurial Magnum and the other imbue items leave no such trace; their holders are assumed to pick the same ability.
Writes {hero id: {"imbue": class name, "share": float, "hits": int, "matches": int}} into the patterns file
("imbue" fields; heroes under MIN_HITS votes, MIN_MATCHES matches or a MIN_SHARE majority are left out).

usage: python3 -I replay_imbues.py <work dir> <fight_patterns.json>
"""
import collections, glob, json, os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from deadsim.data import game
G = game()
AB = {}
for hid in G.heroes:
    for a in G.hero(hid).abilities:
        AB[a.id] = (hid, a.class_name)
QR = next(i.id for i in G.items.values() if i.class_name == "upgrade_quick_silver")
TOL = 2
MIN_HITS = 20
MIN_MATCHES = 3
MIN_SHARE = 0.8      # a split pick (Victor 68%) stays on the sim's default

votes = collections.defaultdict(collections.Counter)
matches = collections.defaultdict(set)
for fn in glob.glob(os.path.join(sys.argv[1], "raw", "*.ndjson")):
    rows = [json.loads(l) for l in open(fn)]
    pawns = {r["a"] for r in rows if r["k"] == "pawn"}
    who = collections.defaultdict(collections.Counter)
    for r in rows:
        if r["k"] == "cast" and (r["a"] & 0x3FFF) in pawns:
            aid = struct.unpack("<I", bytes.fromhex(r["s"][:8]))[0]
            if aid in AB:
                who[r["a"] & 0x3FFF][AB[aid][0]] += 1
    pawn = {e: c.most_common(1)[0][0] for e, c in who.items()}
    hits = collections.defaultdict(list)     # attacker * 100000 + victim (the extract's "a") -> [(tick, ability id)]
    qr = []
    for r in rows:
        if r["k"] != "dmg" or not r.get("s"):
            continue
        aid = int(r["s"])
        if aid == QR:
            qr.append((r["a"], r["tick"]))
        elif aid in AB:
            hits[r["a"]].append((r["tick"], aid))
    for key, t in qr:
        e = key // 100000
        hid = pawn.get(e)
        if hid is None:
            continue
        near = [(abs(t2 - t), a) for t2, a in hits[key] if abs(t2 - t) <= TOL and AB[a][0] == hid]
        if near:
            d = min(near)[0]
            closest = {a for dt, a in near if dt == d}
            if len(closest) == 1:            # two of the hero's abilities on the same tick: ambiguous, no vote
                votes[hid][AB[closest.pop()][1]] += 1
                matches[hid].add(fn)

with open(sys.argv[2]) as fh:
    pats = json.load(fh)
for row in pats["heroes"].values():          # a rerun rewrites every hero; ones below the thresholds get none
    row.pop("imbue", None)
    row.pop("replay_imbue", None)
for hid, c in sorted(votes.items()):
    n = sum(c.values())
    cls, k = c.most_common(1)[0]
    row = pats["heroes"].get(str(hid))
    print(f"{G.hero(hid).name:16s} {cls:34s} {k / n:5.0%} of {n} hits, {len(matches[hid])} matches")
    if row is None or n < MIN_HITS or len(matches[hid]) < MIN_MATCHES or k / n < MIN_SHARE:
        continue
    row["imbue"] = cls
    row["replay_imbue"] = {"share": round(k / n, 3), "hits": n, "matches": len(matches[hid]),
                           "by_ability": dict(c.most_common())}
with open(sys.argv[2], "w") as fh:
    json.dump(pats, fh, indent=1)
