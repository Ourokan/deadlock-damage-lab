"""Which Kelvin ability real Mystic Reverb holders imbue (2026-11-08).

Reads DamageEvent dumps of scripts/mechanics/ally_target.py (fetch with any ability table, e.g. CCitadel_Ability_Slide;
raw: /mnt/project-files/analysis/work/kelvin_reverb, 52 post-hotfix Phantom+ Reverb holders). For each Reverb echo,
the Kelvin ability that hit the same victim DelayDuration (3 s +- 0.6) earlier: Frost Grenade 381, Arctic Beam 69,
none 336. Echo / that damage median 0.67. The sim imbues Arctic Beam (highest listed damage); a Frost Grenade
override made Reverb read further over (the echo's current-health bonus) and failed split-half, so it is not used.

usage: python3 -I kelvin_reverb.py [raw dir]
"""
import sys
import gzip,json,collections,glob,statistics
D=(sys.argv[1] if len(sys.argv) > 1 else '/mnt/project-files/analysis/work/kelvin_reverb').rstrip('/')+'/'
RV='3577481646'; BEAM='2351041382'; GR='18921423'
nm={BEAM:'beam',GR:'grenade','1963397252':'path','3826390464':'dome'}
tot=collections.Counter(); prev=collections.Counter(); echoes=[]; ratio=[]; n=0
for f in sorted(glob.glob(D+'*.ndjson.gz')):
    ctl={};dm=[]
    for l in gzip.open(f):
        r=json.loads(l)
        if r['k']=='ctl':
            h,t=(r.get('s') or '0|0').split('|'); ctl[r['a']]=int(h)
        elif r['k']=='dmg':
            s=(r.get('s') or 'none||').split('|')
            dm.append((r['tick'],r['a']//100000,r['a']%100000,s[0],r['v']))
    kel=set(e for e,h in ctl.items() if h==12)
    if not kel: continue
    n+=1
    mine=[x for x in sorted(dm) if x[1] in kel and x[2] not in kel]
    for t,a,v,ab,d in mine: tot[nm.get(ab,'gun/other' if ab!=RV else 'reverb')]+=d
    for i,(t,a,v,ab,d) in enumerate(mine):
        if ab!=RV: continue
        echoes.append(d)
        back=[(ab2,d2) for t2,a2,v2,ab2,d2 in mine if v2==v and t-3.6*64<=t2<=t-2.4*64 and ab2 in nm]
        c=collections.Counter()
        for ab2,d2 in back: c[nm[ab2]]+=d2
        k=c.most_common(1)[0][0] if c else 'none'
        prev[k]+=1
        if c: ratio.append(d/sum(c.values()))
print('kelvins',n,'echoes',len(echoes),'per match',round(len(echoes)/n,1),'median echo',statistics.median(echoes))
print('damage totals',{k:round(v) for k,v in tot.items()})
print('reverb / (beam+grenade)', round(tot['reverb']/(tot['beam']+tot['grenade']),3), 'reverb share of all', round(tot['reverb']/sum(tot.values()),3))
print('what hit the victim 2.4-3.6 s before the echo:',prev)
ratio.sort(); print('echo / that damage quartiles',[round(ratio[int(q*len(ratio))],2) for q in (.25,.5,.75)])
