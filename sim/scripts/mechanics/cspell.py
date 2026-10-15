"""Enemy ability damage taken per second by real Counterspell holders, with vs without the spell parry (sim)."""
import gzip, json, random, sys, os
SIM = sys.argv[1]; sys.path.insert(0, SIM); sys.path.insert(0, os.path.join(SIM, "scripts"))
from deadsim import Loadout, duel, game
from deadsim.accuracy import default_distance
import deadsim.mechanics as M
import landing_rates as L
G = game(); CS = G.item("Counterspell")
rate = float(sys.argv[2])
mech = M.Mechanics(movement=False)
acc = {"on": [0, 0], "off": [0, 0], "blocks": 0}
for line in gzip.open(os.path.join(SIM, "validation", "matches_sample.jsonl.gz")):
    m = json.loads(line)
    for p in m["players"]:
        if p["hero_id"] not in G.heroes: continue
        foes = [q for q in m["players"] if q["team"] != p["team"] and q["hero_id"] in G.heroes]
        rnd = random.Random(m["match_id"] + p["slot"])
        for frac in L.FRACS:
            t = m["duration_s"] * frac
            items, souls = L.build_at(p, t)
            if CS.id not in items: continue
            q = rnd.choice(foes); fi, fs = L.build_at(q, t)
            hq = G.hero(q["hero_id"])
            abn = {a.name for a in hq.abilities}
            for key, r_ in (("on", rate), ("off", 0.0)):
                s1, s2 = L.skill_of(p), L.skill_of(q); s1.spell_parry_rate = r_
                h = G.hero(p["hero_id"]).name
                r = duel(Loadout(h, items, souls=souls, skill=s1), Loadout(hq.name, fi, souls=fs, skill=s2),
                         distance=default_distance(h), max_time=L.FIGHT_TIME, mechanics=mech)
                ab = sum(v for k, v in r.b_dmg.items() if any(k.startswith(n) for n in abn))
                acc[key][0] += ab; acc[key][1] += r.time
print("spell_parry_rate", rate, "ability dmg/s taken on/off", round((acc["on"][0] / acc["on"][1]) / (acc["off"][0] / acc["off"][1]), 3))
