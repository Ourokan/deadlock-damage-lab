"""Haze's Lucky Shot procs in real replays (2026-11-08): does Fixation's bonus damage roll Lucky Shot too?

Reads DamageEvent dumps of scripts/mechanics/ally_target.py (any post-hotfix replays; used: the kelvin_reverb, solomon
and paige raw dirs under /mnt/project-files/analysis/work, 41 Haze Lucky Shot holders). From each holder's first
proc on: hits on heroes of her gun, Bullet Dance and Fixation, Lucky Shot procs, and what shares a proc's tick.
Result: 7,625 procs vs 0.25 x (14,610 gun + Bullet Dance hits + 15,020 Fixation hits) = 7,400; Lucky Shot damage
0.23 of gun + Bullet Dance + Fixation (0.35 of gun + Bullet Dance alone): Fixation's bonus rolls on its own.

usage: python3 -I haze_lucky.py [raw dir ...]
"""
import sys
import gzip,json,collections,glob,statistics
import os
W=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'data', 'game', 'weapons.json')))
wid={str(w['id']) for w in W if w['hero_id']==13}
LUCK='1396247347'; FIX='1080948381'; BD='731943444'
DIRS=sys.argv[1:] or ['/mnt/project-files/analysis/work/kelvin_reverb', '/mnt/project-files/analysis/work/ally_target/solomon',
                     '/mnt/project-files/analysis/work/ally_target/paige']
files=[f for d in DIRS for f in glob.glob(d.rstrip('/')+'/*.ndjson.gz')]
c=collections.Counter(); szw=[]; szf=[]; tot=collections.Counter()
for f in files:
    ctl={};dm=[]
    for l in gzip.open(f):
        r=json.loads(l)
        if r['k']=='ctl':
            h,t=(r.get('s') or '0|0').split('|'); ctl[r['a']]=int(h)
        elif r['k']=='dmg':
            s=(r.get('s') or 'none||').split('|')
            dm.append((r['tick'],r['a']//100000,r['a']%100000,s[0],r['v']))
    hz=[e for e,h in ctl.items() if h==13]
    for a in hz:
        mine=[x for x in dm if x[1]==a]
        if not any(x[3]==LUCK for x in mine): continue
        t0=min(x[0] for x in mine if x[3]==LUCK); c["holders"]+=1
        by=collections.defaultdict(list)
        for t,_,v,ab,d in mine:
            if t<t0: continue
            k='gun' if ab in wid else {LUCK:'luck',FIX:'fix',BD:'bd'}.get(ab)
            if k: by[(t,v)].append((k,d)); tot[k]+=d; c[k+'_n']+=1
        for key,L in by.items():
            ks=[k for k,_ in L]
            if 'luck' in ks:
                c['luck_with '+'+'.join(sorted(set(k for k in ks if k!='luck')))]+=1
                lk=sum(d for k,d in L if k=='luck'); g=sum(d for k,d in L if k in('gun','bd')); fx=sum(d for k,d in L if k=='fix')
                if g: szw.append(lk/g); szf.append(lk/(g+fx))
print(c); print({k:round(v) for k,v in tot.items()})
for nm,s in (('luck/(gun or bd hit)',szw),('luck/(hit+fixation)',szf)):
    s.sort(); print(nm,[round(s[int(q*len(s))],2) for q in (.1,.25,.5,.75,.9)])
