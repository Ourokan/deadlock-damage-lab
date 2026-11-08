"""Lash's Flog in Phantom+ replays: is its landing factor above 1 more heroes per cast or more casts (Quicksilver Reload,
imbued on Flog, spends one charge per cast; items_fx.LANDING_PROCS).

Per Lash holding Quicksilver (procs seen) in the hero-on-hero DamageEvents: Flog casts (hits within 0.5 s), heroes per
cast, per-hero hit size, Quicksilver procs and how many land with a Flog, procs per cast, Quicksilver / Flog damage.
Result (2026-11-08, 260 replays in analysis/work/fight_length/raw, 73 holders): 1.17 heroes per cast, hit median 138,
0.95 procs per cast, Quicksilver / Flog damage 0.235.

usage: python3 -I lash_quicksilver.py <raw dir>
"""
import collections, glob, os, statistics, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fight_length"))
from opener_timing import read
LASH, FLOG, QSR, GS = 31, 519124136, 84321454, 3561817145
casts = procs = 0; vic = []; per_hit = []; qdmg = []; flogd = 0.0; qtot = 0.0; same = collections.Counter(); n = 0
proc_cast = []
for fn in sorted(glob.glob(os.path.join(sys.argv[1], "*.ndjson.gz"))):
    hero, ev = read(fn)
    for me in (e for e, h in hero.items() if h == LASH):
        fl = [(t, v, d) for t, a, v, hp, mx, d, ab in ev if a == me and ab == FLOG and v in hero]
        q = [(t, v, d) for t, a, v, hp, mx, d, ab in ev if a == me and ab == QSR and v in hero]
        if not q: continue
        n += 1
        cs = []
        for t, v, d in fl:
            if cs and t - cs[-1][0] < 0.5: cs[-1][1].add(v); cs[-1][2] += d
            else: cs.append([t, {v}, d])
            per_hit.append(d)
        casts += len(cs); vic += [len(c[1]) for c in cs]; flogd += sum(c[2] for c in cs)
        procs += len(q); qtot += sum(d for _, _, d in q); qdmg += [d for _, _, d in q]
        ft = [c[0] for c in cs]
        for t, v, d in q:
            same["flog" if any(abs(t - x) < 0.6 for x in ft) else "other"] += 1
print(f"Lash QSR holders {n}; Flog casts {casts}, victims/cast {statistics.mean(vic):.2f}, per-victim hit median {statistics.median(per_hit):.0f}")
print(f"QSR procs {procs} ({dict(same)}), per proc median {statistics.median(qdmg):.0f}; procs per Flog cast {procs/casts:.2f}; QSR/Flog damage {qtot/flogd:.3f}")
