import gzip, json, sys
sys.path.insert(0, sys.argv[1])
from deadsim.data import game
G = game()
rows = []
for line in gzip.open('/mnt/project-files/sim/validation/matches_sample.jsonl.gz', 'rt'):
    m = json.loads(line)
    teams = {}
    for p in m['players']:
        h = G.heroes[p['hero_id']] if p['hero_id'] in G.heroes else None
        if h is None: continue
        lvl_boons = max(0, (p.get('level') or 20) - 1)
        light = h.base.get('light_melee_damage', 50) + lvl_boons * h.per_boon.get('MODIFIER_VALUE_BASE_MELEE_DAMAGE_FROM_LEVEL', 0)
        heavy = (h.base.get('heavy_melee_damage') or 2.32 * h.base.get('light_melee_damage', 50)) * light / h.base.get('light_melee_damage', 50)
        per = 0.7 * light + 0.3 * heavy
        melee = (p['damage_sources'] or {}).get('Melee', 0)
        c = p.get('custom') or {}
        t = teams.setdefault(p['team'], {'hits': 0, 'ps': 0, 'pm': 0, 'n': 0})
        t['hits'] += melee / per
        t['ps'] += c.get('Parry Success', 0); t['pm'] += c.get('Parry Miss', 0); t['n'] += 1
    if len(teams) != 2: continue
    (a, ta), (b, tb) = teams.items()
    rows.append((tb['hits'], ta['ps'], ta['pm'], m['duration_s']))
    rows.append((ta['hits'], tb['ps'], tb['pm'], m['duration_s']))
# OLS ps = a + b*hits (per match)
n = len(rows)
xs = [r[0] for r in rows]; ys = [r[1] for r in rows]
mx, my = sum(xs)/n, sum(ys)/n
b = sum((x-mx)*(y-my) for x, y in zip(xs, ys)) / sum((x-mx)**2 for x in xs)
a = my - b*mx
print('teams', n, 'mean enemy melee hits landed', round(mx,1), 'mean team parry success', round(my,1), 'miss', round(sum(r[2] for r in rows)/n,1))
print('fit: parries = %.2f + %.3f * enemy landed melee hits' % (a, b))
# bootstrap
import random
random.seed(1); bs=[]
for _ in range(300):
    s=[random.choice(rows) for _ in range(n)]
    xs=[r[0] for r in s]; ys=[r[1] for r in s]; mx,my=sum(xs)/n,sum(ys)/n
    bs.append(sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs))
bs.sort(); print('b 90%% CI %.3f-%.3f' % (bs[15], bs[285]))
print('share of hero melee attempts parried = b/(1+b) = %.3f' % (b/(1+b)))
# quartiles
rows.sort()
q=n//4
for i in range(4):
    s=rows[i*q:(i+1)*q]; print('quartile', i, 'hits %.0f parries %.1f' % (sum(r[0] for r in s)/len(s), sum(r[1] for r in s)/len(s)))
