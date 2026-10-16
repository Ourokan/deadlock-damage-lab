"""Sim version of escapes_real.py: duels between real builds (validation sample) with movement on; for each fighter
whose health first drops below 25% while both live: died / won / escaped / still fighting within 10 s.
usage: sim_escapes.py SIM [k=v ...]  (Mechanics fields, Skill fields, M.CONST)"""
import gzip, json, random, sys, os, collections
SIM = sys.argv[1]; sys.path.insert(0, SIM); sys.path.insert(0, os.path.join(SIM, "scripts"))
from deadsim import Loadout, game
from deadsim.engine import Engine
from deadsim.fight import make_fighter
from deadsim.accuracy import default_distance, hero_default_skill
import deadsim.mechanics as M
import landing_rates as L
G = game()
mk, sk = {}, {}
for o in sys.argv[2:]:
    k, v = o.split("=")
    if k.startswith("M."): setattr(M, k[2:], float(v)); continue
    (mk if k in M.Mechanics.__dataclass_fields__ else sk)[k] = (v == "1") if k in ("parry", "summons", "movement") else float(v)
mech = M.Mechanics(**mk)
LOW, HOR = 0.25, 10.0
res = collections.Counter(); mob_res = collections.defaultdict(collections.Counter)
MOB = {G.item(n).id for n in ("Majestic Leap", "Warp Stone", "Ethereal Shift", "Fleetfoot", "Enduring Speed", "Magic Carpet",
                               "Extra Stamina", "Stamina Mastery", "Kinetic Dash", "Dispel Magic")}
N = 0
for line in gzip.open(os.path.join(SIM, "validation", "matches_sample.jsonl.gz")):
    m = json.loads(line)
    for p in m["players"][:6]:
        if p["hero_id"] not in G.heroes: continue
        foes = [q for q in m["players"] if q["team"] != p["team"] and q["hero_id"] in G.heroes]
        rnd = random.Random(m["match_id"] * 7 + p["slot"])
        t = m["duration_s"] * rnd.choice(L.FRACS)
        q = rnd.choice(foes)
        ia, sa = L.build_at(p, t); ib, sb = L.build_at(q, t)
        ha, hb = G.hero(p["hero_id"]).name, G.hero(q["hero_id"]).name
        s1, s2 = hero_default_skill(ha), hero_default_skill(hb)
        for s in (s1, s2):
            for k, v in sk.items(): setattr(s, k, v)
        e = Engine(distance=(default_distance(ha) + default_distance(hb)) / 2, max_time=45, mech=mech)
        fa = make_fighter(e, Loadout(ha, ia, souls=sa, skill=s1), "A"); fb = make_fighter(e, Loadout(hb, ib, souls=sb, skill=s2), "B")
        mark = {}
        def mon():
            for f in (fa, fb):
                if f.name not in mark and f.alive and f.enemy.alive and f.hp_frac < LOW:
                    mark[f.name] = e.t
            e.after(0.25, mon)
        e.at(0.25, mon)
        r = e.run(fa, fb)
        N += 1
        for f in (fa, fb):
            if f.name not in mark: continue
            t0 = mark[f.name]
            if not f.alive and f.death_time <= t0 + HOR: o = "died"
            elif not f.enemy.alive and f.enemy.death_time <= t0 + HOR: o = "won"
            elif r.escaped == f.name and r.time <= t0 + HOR: o = "escaped"
            elif r.time < t0 + HOR and r.escaped is None and f.alive and f.enemy.alive: o = "timeout"
            else: o = "still_fighting"
            res[o] += 1
            mob_res[bool(set(ia if f is fa else ib) & MOB)][o] += 1
def show(c):
    tot = sum(c.values()); return {k: f"{v} ({v / max(1, tot):.0%})" for k, v in sorted(c.items())} | {"n": tot}
print(mech, sk, {k: getattr(M, k) for k in ("CHASE_PROB", "WARP_AWAY")})
print("duels", N, "all", show(res)); print("  mobility", show(mob_res[True])); print("  none", show(mob_res[False]))
