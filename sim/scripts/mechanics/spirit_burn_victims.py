"""Spirit Burn's immunity per victim in real replays (2026-11-08).

Reads DamageEvent dumps of scripts/mechanics/ally_target.py (one <match_id>.ndjson.gz per replay; used: the
fight_length/raw, kelvin_reverb and ally_target/* dirs under /mnt/project-files/analysis/work). An episode = one
holder's Spirit Burn damage on one hero after 9+ s without any (explosion + 8 s DoT); gaps between a holder's episode
starts, on the same victim or on another one.
Result: 897 holder-matches, 7,795 episodes; same victim: 574 gaps, median 72 s, 7% under the 20 s ImmunityDuration;
another victim: 6,324 gaps, median 19.5 s, 51% under 20 s; 1.21 victims start within 1 s of an episode. So the
immunity is per victim: team fights burn more heroes than the duel's one (per-hero rows in item_landing.json absorb it).

usage: python3 -I spirit_burn_victims.py <raw dir> [...]
"""
import gzip, json, glob, sys, collections, statistics
SB = "343572757"
files = {}
for d in sys.argv[1:]:
    for f in glob.glob(d.rstrip('/') + '/*.ndjson.gz'):
        files.setdefault(f.split('/')[-1], f)
gaps_same = []; gaps_other = []; nep = 0; holders = 0; vic_per_window = []
for f in files.values():
    ctl = {}; dm = []
    for l in gzip.open(f):
        r = json.loads(l)
        if r['k'] == 'ctl': ctl[r['a']] = int((r.get('s') or '0|0').split('|')[0])
        elif r['k'] == 'dmg':
            s=(r.get('s') or '').split('|')
            if s[0] == SB: dm.append((r['tick'], r['a'] // 100000, r['a'] % 100000, r['v']))
    by = collections.defaultdict(list)
    for t, a, v, d in sorted(dm):
        if v in ctl: by[(a, v)].append(t)
    # episodes: per (attacker, victim) a new episode when gap > 9 s
    starts = collections.defaultdict(list)
    for (a, v), ts in by.items():
        last = -1e9
        for t in ts:
            if t - last > 9 * 64: starts[a].append((t, v))
            last = t
    for a, st in starts.items():
        holders += 1; st.sort(); nep += len(st)
        for i in range(1, len(st)):
            g = (st[i][0] - st[i-1][0]) / 64
            (gaps_same if st[i][1] == st[i-1][1] else gaps_other).append(g)
        # victims starting within 1 s of an episode start
        for t, v in st:
            vic_per_window.append(len({w for x, w in st if abs(x - t) <= 64}))
print('attacker-matches', holders, 'episodes', nep)
for n, g in (('same victim', gaps_same), ('other victim', gaps_other)):
    if g: print(n, len(g), 'median gap', round(statistics.median(g), 1), 'share < 20 s', round(sum(x < 20 for x in g) / len(g), 2))
print('victims starting within 1 s of an episode', round(statistics.mean(vic_per_window), 2))
