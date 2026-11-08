"""Dynamo's Singularity and Kinetic Pulse in real replays (2026-11-08): heroes hit per cast by match phase.

Reads DamageEvent dumps of scripts/mechanics/ally_target.py (one <match_id>.ndjson.gz per replay; used:
/mnt/project-files/analysis/work/fight_length/raw, kelvin_reverb, ally_target/solomon, ally_target/paige: 69 matches
with a Dynamo). A cast = a run of one Dynamo's hits of the ability on enemy heroes with gaps under 6 s (Singularity) /
2 s (Kinetic Pulse); phase = the cast's time over the replay's damage span.
Result: Singularity 393 casts, 1.60 / 1.98 / 2.05 heroes per cast (total / main 1.46 / 1.68 / 1.70) before 45%, 45-75%,
after 75%. Against the gun's own spread (other / main 0.21 lane -> 0.40 late, ability_area_phase.py) that is flat
(rel 1.21 / 1.20 / 1.21), so no area-phase row. Kinetic Pulse 1.14 / 1.22 / 1.30 (already in ability_area_phase.json).

usage: python3 -I dynamo_singularity.py <raw dir> [...]
"""
import gzip, json, glob, sys, collections, statistics
SING, KP = "249410288", "3760705623"
dirs = sys.argv[1:]
files = {}
for d in dirs:
    for f in glob.glob(d.rstrip('/') + '/*.ndjson.gz'):
        files.setdefault(f.split('/')[-1], f)
casts = []  # (frac, nvictims, dmg, dur)
kp = []
nm = 0
for f in files.values():
    ctl = {}; dm = []
    for l in gzip.open(f):
        r = json.loads(l)
        if r['k'] == 'ctl':
            ctl[r['a']] = int((r.get('s') or '0|0').split('|')[0])
        elif r['k'] == 'dmg':
            dm.append((r['tick'], r['a'] // 100000, r['a'] % 100000, (r.get('s') or '').split('|')[0], r['v']))
    dyn = {e for e, h in ctl.items() if h == 11}
    if not dyn or not dm: continue
    heroes = set(ctl)
    t0 = min(x[0] for x in dm); t1 = max(x[0] for x in dm)
    nm += 1
    for ab, out, gap in ((SING, casts, 6 * 64), (KP, kp, 2 * 64)):
        ev = sorted(x for x in dm if x[1] in dyn and x[3] == ab and x[2] in heroes and x[2] not in dyn)
        cur = None
        for t, a, v, _, d in ev:
            if cur is None or t - cur['last'] > gap:
                if cur: out.append(cur)
                cur = {'t': t, 'last': t, 'v': collections.Counter(), 'frac': (t - t0) / max(1, t1 - t0)}
            cur['last'] = t; cur['v'][v] += d
        if cur: out.append(cur)
print('matches with Dynamo', nm)
for name, out in (('Singularity', casts), ('Kinetic Pulse', kp)):
    print(name, 'casts', len(out))
    for lo, hi in ((0, .45), (.45, .75), (.75, 1.01)):
        b = [c for c in out if lo <= c['frac'] < hi]
        if not b: continue
        nv = [len(c['v']) for c in b]
        main = [max(c['v'].values()) for c in b]; tot = [sum(c['v'].values()) for c in b]
        print(f"  frac {lo:.2f}-{hi:.2f}: n {len(b)}  heroes/cast {statistics.mean(nv):.2f}  total/main {sum(tot)/sum(main):.2f}  "
              f"mean total {statistics.mean(tot):.0f}  dur {statistics.mean([(c['last']-c['t'])/64 for c in b]):.1f}s")
