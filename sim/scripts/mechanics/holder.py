"""Sim item damage / gun damage for real holders of an item (validation sample builds), with mechanics on.
usage: holder.py SIM "Item Name" [k=v skill/mechanics overrides]"""
import gzip, json, random, sys, os
SIM = sys.argv[1]; sys.path.insert(0, SIM); sys.path.insert(0, os.path.join(SIM, "scripts"))
from deadsim import Loadout, duel, game
from deadsim.accuracy import default_distance
import deadsim.mechanics as M
import landing_rates as L
G = game(); item = G.item(sys.argv[2])
mk, sk = {}, {}
for o in sys.argv[3:]:
    k, v = o.split("=")
    if k.startswith("M."):
        setattr(M, k[2:], float(v)); continue
    (mk if k in M.Mechanics.__dataclass_fields__ else sk)[k] = (v == "1") if k in ("parry", "summons", "movement") else float(v)
mech = M.Mechanics(**mk)
tot = {"item": 0.0, "gun": 0.0, "n": 0}
rows = [json.loads(l) for l in gzip.open(os.path.join(SIM, "validation", "matches_sample.jsonl.gz"))]
for m in rows:
    for p in m["players"]:
        if p["hero_id"] not in G.heroes: continue
        foes = [q for q in m["players"] if q["team"] != p["team"] and q["hero_id"] in G.heroes]
        rnd = random.Random(m["match_id"] + p["slot"])
        for frac in L.FRACS:
            t = m["duration_s"] * frac
            items, souls = L.build_at(p, t)
            if item.id not in items: continue
            q = rnd.choice(foes); fi, fs = L.build_at(q, t)
            s1, s2 = L.skill_of(p), L.skill_of(q)
            for s in (s1, s2):
                for k, v in sk.items(): setattr(s, k, v)
            h = G.hero(p["hero_id"]).name
            r = duel(Loadout(h, items, souls=souls, skill=s1), Loadout(q["hero_id"], fi, souls=fs, skill=s2),
                     distance=default_distance(h), max_time=L.FIGHT_TIME, mechanics=mech)
            tot["item"] += r.a_dmg.get(item.name, 0) + r.a_splash.get(item.name, 0)
            tot["gun"] += r.a_dmg.get("gun", 0); tot["n"] += 1
print(item.name, mech, sk, "fights", tot["n"], "item/gun", round(tot["item"] / max(1, tot["gun"]), 4))
