"""Real fight openers per hero from replay extracts (fetch_replays.py output).

A fight is a run of hero-vs-hero damage to or from the hero with gaps under GAP s and at least MIN_DMG damage; casts
from PRE s before its first hit count as its opener. Per hero: cast order (pairwise: which ability usually comes first),
share of fights each ability is cast / cast first / cast before the first hit, abilities cast before the ultimate, and
for Mo & Krill the share of fights that start with Mo underground.

usage: python3 -I replay_openers.py <work dir> <out.json>
"""
import json, glob, os, sys, collections, statistics as st, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from deadsim.data import game
G = game()
AB = {}
for hid in G.heroes:
    h = G.hero(hid)
    for i, a in enumerate(h.abilities):
        AB[a.id] = (hid, i, a.class_name, a.name, a.ultimate)
TICK = 64.0


def burrowed(states, lo, hi):
    """Was Mo underground at any moment in [lo, hi]? states: [(time, in_ground)] at each entity update."""
    cur = False
    for t, g in sorted(states):
        if t > hi:
            break
        if t >= lo and g:
            return True
        cur = g
    return cur
GAP = 8.0          # s without hero damage that ends a fight
PRE = 4.0          # s before the first damage that still count as the fight's opener
MIN_DMG = 300
agg = collections.defaultdict(lambda: {"fights": 0, "matches": 0, "first": collections.Counter(), "cast": collections.Counter(),
                                       "t": collections.defaultdict(list), "pre": collections.Counter(),
                                       "before": collections.Counter(), "ground": 0, "ult_after": collections.Counter(), "ult_fights": 0,
                                       "seq": collections.Counter()})
files = glob.glob(os.path.join(sys.argv[1], "raw", "*.ndjson"))
for fn in files:
    rows = [json.loads(l) for l in open(fn)]
    # hero per pawn: the hero whose abilities that pawn owns (m_nHeroID is empty in the extracts)
    pawns = {r["a"] for r in rows if r["k"] == "pawn"}
    votes = collections.defaultdict(collections.Counter)
    for r in rows:
        if r["k"] == "cast" and (r["a"] & 0x3FFF) in pawns:
            aid = struct.unpack("<I", bytes.fromhex(r["s"][:8]))[0]
            if aid in AB:
                votes[r["a"] & 0x3FFF][AB[aid][0]] += 1
    pawn = {e: c.most_common(1)[0][0] for e, c in votes.items()}
    # a cast sets the cooldown start to the current game time (a fixed offset from tick / TICK in each replay);
    # cooldown cuts (Violet's Living Ink hits, Witchmail) move the start back, which is no cast
    off = collections.Counter(round(r["tick"] / TICK - r["v"], 2) for r in rows if r["k"] == "cast").most_common(1)
    off = off[0][0] if off else None
    casts = collections.defaultdict(list); dmg = collections.defaultdict(list); ground = collections.defaultdict(list)
    for r in rows:
        if r["k"] == "cast":
            e = r["a"] & 0x3FFF
            if e not in pawn or abs(r["tick"] / TICK - r["v"] - off) > 0.05: continue
            aid = struct.unpack("<I", bytes.fromhex(r["s"][:8]))[0]
            if aid in AB and AB[aid][0] == pawn[e]:
                casts[e].append((r["tick"] / TICK, aid))
        elif r["k"] == "dmg":
            at, vi = divmod(r["a"], 100000)
            if at in pawn and vi in pawn and at != vi:
                dmg[at].append((r["tick"] / TICK, r["v"])); dmg[vi].append((r["tick"] / TICK, r["v"]))
        elif r["k"] == "ground":
            ground[r["a"] & 0x3FFF].append((r["tick"] / TICK, r["s"] == "true"))
    for e, hid in pawn.items():
        if hid not in G.heroes: continue
        A = agg[hid]; A["matches"] += 1
        ev = sorted(dmg[e]); fights = []; cur = None
        for t, v in ev:
            if cur and t - cur[1] <= GAP: cur[1] = t; cur[2] += v
            else:
                if cur: fights.append(cur)
                cur = [t, t, v]
        if cur: fights.append(cur)
        cs = sorted(casts[e])
        prev_end = -1e9
        for s, end, tot in fights:
            lo = max(s - PRE, prev_end + 1.0); prev_end = end
            if tot < MIN_DMG: continue
            inside = [(t, a) for t, a in cs if lo <= t <= end]
            A["fights"] += 1
            if burrowed(ground[e], s - 3.0, s + 0.5): A["ground"] += 1
            seen = []
            for t, a in inside:
                if a not in seen:
                    seen.append(a); A["t"][a].append(t - s)
            for a in seen: A["cast"][a] += 1
            if seen:
                A["first"][seen[0]] += 1
                if inside[0][0] < s: A["pre"][seen[0]] += 1
                A["seq"][tuple(AB[a][1] for a in seen[:3])] += 1
            for i, a in enumerate(seen):
                for b in seen[i + 1:]:
                    A["before"][(a, b)] += 1
            ult = [a for a in seen if AB[a][4]]
            if ult:
                A["ult_fights"] += 1
                for a in seen[:seen.index(ult[0])]: A["ult_after"][a] += 1
out = {}
for hid, A in sorted(agg.items(), key=lambda kv: G.hero(kv[0]).name):
    h = G.hero(hid); n = A["fights"]
    if not n: continue
    abil = {}
    for i, a in enumerate(h.abilities):
        ts = A["t"].get(a.id, [])
        abil[a.class_name] = {"name": a.name, "slot": i + 1, "cast_share": round(A["cast"][a.id] / n, 3),
                              "first_share": round(A["first"][a.id] / n, 3), "pre_share": round(A["pre"][a.id] / n, 3),
                              "median_first_cast_s": round(st.median(ts), 2) if ts else None,
                              "ult_after_share": round(A["ult_after"][a.id] / A["ult_fights"], 3) if A["ult_fights"] and not a.ultimate else None}
    # order: pairwise precedence (Copeland), among abilities cast in >= 10% of fights
    ids = [a.id for a in h.abilities if A["cast"][a.id] / n >= 0.10]
    score = {a: sum(A["before"][(a, b)] > A["before"][(b, a)] for b in ids if b != a) for a in ids}
    order = sorted(ids, key=lambda a: (-score[a], st.median(A["t"][a])))
    out[str(hid)] = {"name": h.name, "matches": A["matches"], "fights": n, "burrowed_at_start": round(A["ground"] / n, 3) if hid == 18 else None,
                     "order": [AB[a][2] for a in order], "abilities": abil,
                     "top_sequences": [[[h.abilities[i].name for i in k], round(v / n, 3)] for k, v in A["seq"].most_common(3)]}
json.dump(out, open(sys.argv[2], "w"), indent=1)
for r in out.values():
    print(f"{r['name']:15} m{r['matches']:3} f{r['fights']:4} order: {' > '.join(r['abilities'][c]['name'] for c in r['order'])}"
          + (f"  burrowed {r['burrowed_at_start']}" if r['burrowed_at_start'] is not None else ""))
