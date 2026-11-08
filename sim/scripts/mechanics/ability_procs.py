"""Per-cast item procs off one ability in Phantom+ replays: is the ability's landing factor above 1 more casts (each
spending a Quicksilver Reload charge and releasing Mystic Burst / Tankbuster) or more heroes / hits per cast?
(items_fx.LANDING_PROCS: Viscous' Splatter, Nurse's Leech Therapy, Lash's Flog.)

Per player of the hero in the hero-on-hero DamageEvents: the ability's casts (hits less than 1 s apart), heroes per
cast, hits per hero per cast, hit size; for Quicksilver / Mystic Burst / Tankbuster: procs, the share landing in the
same tick (50 ms) as one of the ability's hits, and the item's damage per the ability's damage. Generalizes
lash_quicksilver.py; used 2026-11-08 to sweep the heroes (validation/README.md "Per-cast item procs across heroes").

usage: python3 -I ability_procs.py <raw dir> "<Hero>" "<Ability>"
"""
import bisect
import collections
import glob
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fight_length"))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from opener_timing import read, sources  # noqa: E402
from deadsim.data import game  # noqa: E402

G = game()
names = sources(G)
hero_name, ab_name = sys.argv[2], sys.argv[3]
H = G.hero(hero_name); AB = next(a for a in H.abilities if a.name == ab_name).id
items = {i: names[i][1] for i in names if names[i][1] in ("Mystic Burst", "Tankbuster", "Quicksilver Reload")}
casts = 0; vic = []; hits_per_victim = []; size = []; abd = 0.0; pr = collections.Counter(); prd = collections.Counter(); prwith = collections.Counter(); n = 0
for fn in sorted(glob.glob(os.path.join(sys.argv[1], "*.ndjson.gz"))):
    hero, ev = read(fn)
    for me in (e for e, h in hero.items() if h == H.id):
        n += 1
        mine = [(t, v, d, ab) for t, a, v, hp, mx, d, ab in ev if a == me and v in hero]
        fl = [(t, v, d) for t, v, d, ab in mine if ab == AB]
        cs = []
        for t, v, d in fl:
            if cs and t - cs[-1][1] < 1.0: cs[-1][1] = t; cs[-1][2][v] += 1; cs[-1][3] += d
            else: cs.append([t, t, collections.Counter({v: 1}), d])
            size.append(d)
        casts += len(cs); vic += [len(c[2]) for c in cs]; hits_per_victim += [x for c in cs for x in c[2].values()]; abd += sum(c[3] for c in cs)
        ft = [t for t, _, _ in fl]
        for t, v, d, ab in mine:
            if ab in items:
                nm = items[ab]; pr[nm] += 1; prd[nm] += d
                i = bisect.bisect_left(ft, t - 0.05)
                if i < len(ft) and abs(ft[i] - t) <= 0.05: prwith[nm] += 1
print(f"{hero_name} {ab_name}: players {n}, casts {casts}, heroes/cast {statistics.mean(vic):.2f}, hits/hero/cast {statistics.mean(hits_per_victim):.2f}, hit median {statistics.median(size):.0f}")
for nm in pr: print(f"  {nm}: procs {pr[nm]}, with {ab_name} {prwith[nm]/pr[nm]:.2f}, per {ab_name} damage {prd[nm]/abd:.3f}")
