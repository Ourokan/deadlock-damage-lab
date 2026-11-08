"""Mystic Burst / Tankbuster releases per victim of Mo & Krill's area abilities in real replays (2026-11-08).

Reads DamageEvent dumps of scripts/mechanics/ally_target.py (one <match_id>.ndjson.gz per replay; used: the
fight_length/raw, kelvin_reverb and ally_target/* dirs under /mnt/project-files/analysis/work, 129 matches with Mo &
Krill). A cast = one Mo & Krill's hits of the ability (env AB, default Scorn) on enemy heroes within 8 ticks; for each,
the heroes it hit and how many of them got an item release (env ITEM, default Mystic Burst) within -2..+12 ticks.
Result: Scorn casts hitting 1 / 2 / 3 / 4+ heroes: 4,481 / 891 / 150 / 26, Mystic Burst on 0.71 / 1.35 / 1.82 / 2.04 of
them, median size 34 / 30 / 24 / 24 (each victim gets a near-full release); Tankbuster 0.15 / 0.30 / 0.53 / 1.15; Sand
Blast (AB=1914797280) Mystic Burst 0.34 / 0.51 / 0.97 / 1.50. Heroes per cast: Scorn 1.22, Sand Blast 1.20
(items_fx.AREA_RELEASES).

usage: [AB=<ability id>] [ITEM=<item id>] python3 -I mk_area_releases.py <raw dir> [...]
"""
import gzip, json, glob, os, sys, collections, statistics
SC = os.environ.get("AB", "1454278799"); MB = os.environ.get("ITEM", "1998374645")
files = {}
for d in sys.argv[1:]:
    for f in glob.glob(d.rstrip('/') + '/*.ndjson.gz'):
        files.setdefault(f.split('/')[-1], f)
bykv = collections.Counter(); procs_by_k = collections.defaultdict(list); sz_by_k = collections.defaultdict(list)
for f in files.values():
    ctl = {}; dm = []
    for l in gzip.open(f):
        r = json.loads(l)
        if r['k'] == 'ctl': ctl[r['a']] = int((r.get('s') or '0|0').split('|')[0])
        elif r['k'] == 'dmg': dm.append((r['tick'], r['a'] // 100000, r['a'] % 100000, (r.get('s') or '').split('|')[0], r['v']))
    mk = {e for e, h in ctl.items() if h == 18}
    if not mk: continue
    ev = sorted(x for x in dm if x[1] in mk and x[2] in ctl and x[2] not in mk)
    mbs = [x for x in ev if x[3] == MB]
    scs = [x for x in ev if x[3] == SC]
    # group scorn hits into casts: same attacker, within 8 ticks
    casts = []
    for x in scs:
        if casts and x[1] == casts[-1][-1][1] and x[0] - casts[-1][0][0] <= 8: casts[-1].append(x)
        else: casts.append([x])
    for c in casts:
        t0 = c[0][0]; vic = {x[2] for x in c}; k = len(vic)
        m = [x for x in mbs if x[1] == c[0][1] and t0 - 2 <= x[0] <= t0 + 12 and x[2] in vic]
        procs_by_k[min(k, 4)].append(len({x[2] for x in m}))
        sz_by_k[min(k, 4)] += [x[4] for x in m]
for k in sorted(procs_by_k):
    p = procs_by_k[k]
    print(f"casts hitting {k}{'+' if k == 4 else ''} heroes: n {len(p)}, MB-proc victims per cast {statistics.mean(p):.2f}, "
          f"median MB size {statistics.median(sz_by_k[k]) if sz_by_k[k] else 0:.0f}")
