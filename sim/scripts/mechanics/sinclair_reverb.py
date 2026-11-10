"""Which Sinclair ability real Mystic Reverb holders imbue (2026-11-10).

Reads DamageEvent dumps of scripts/mechanics/ally_target.py (fetch with any ability table, e.g. CCitadel_Ability_Slide;
raw: /mnt/project-files/analysis/work/sinclair_reverb, 51 post-hotfix Phantom+ Sinclair Reverb holders from the
2026-11-06..11-10 samples, about half the ids have no demo). For each Reverb echo, the Sinclair ability that dealt the
most damage to the same victim DelayDuration (3 s +- 0.6) earlier: Vexing Bolt 274, Spectral Assistant 46, Rabbit Hex 4,
none 328 (echoes splash other heroes). Echo / that Vexing Bolt damage median 0.57. The sim imbued the Assistant (highest
listed damage: Vexing Bolt lists only MinDamage/MaxDamage), so fight.IMBUE_OVERRIDE puts Reverb on Vexing Bolt.

usage: python3 -I sinclair_reverb.py [raw dir]
"""
import collections
import glob
import gzip
import json
import statistics
import sys

D = (sys.argv[1] if len(sys.argv) > 1 else '/mnt/project-files/analysis/work/sinclair_reverb').rstrip('/') + '/'
SINCLAIR = 60
RV = '3577481646'   # upgrade_mystic_reverb (ability ids are MurmurHash2 of the class name, seed 0x31415926)
NM = {'3156905386': 'Vexing Bolt', '12456023': 'Spectral Assistant', '2142213586': 'Rabbit Hex',
      '191022746': 'Audience Participation'}
prev = collections.Counter()
ratio = collections.defaultdict(list)
n = echoes = 0
for f in sorted(glob.glob(D + '*.ndjson.gz')):
    ctl, dm = {}, []
    for line in gzip.open(f):
        r = json.loads(line)
        if r['k'] == 'ctl':
            ctl[r['a']] = int((r.get('s') or '0|0').split('|')[0])
        elif r['k'] == 'dmg':
            s = (r.get('s') or 'none||').split('|')
            dm.append((r['tick'], r['a'] // 100000, r['a'] % 100000, s[0], r['v']))
    me = {e for e, h in ctl.items() if h == SINCLAIR}
    if not me:
        continue
    n += 1
    mine = [x for x in sorted(dm) if x[1] in me and x[2] not in me]
    for t, a, v, ab, d in mine:
        if ab != RV:
            continue
        echoes += 1
        c = collections.Counter()
        for t2, a2, v2, ab2, d2 in mine:
            if v2 == v and t - 3.6 * 64 <= t2 <= t - 2.4 * 64 and ab2 in NM:
                c[NM[ab2]] += d2
        k = c.most_common(1)[0][0] if c else 'none'
        prev[k] += 1
        if c:
            ratio[k].append(d / c[k])
print('sinclairs', n, 'echoes', echoes)
for k, m in prev.most_common():
    print(f'{k:24s} {m:5d}', f'echo/dmg median {statistics.median(ratio[k]):.2f}' if ratio[k] else '')
