"""Sim escape share (escaped / (escaped + died) within 10 s of dropping below 25%) for fighter A with item X added to
his real build vs without; and with X added to B (enemy-side items). Same duels as sim_escapes.py.
usage: sim_item_escape.py SIM "Item" side(A|B)"""
import gzip, json, random, sys, os, collections
SIM = sys.argv[1]; sys.path.insert(0, SIM); sys.path.insert(0, os.path.join(SIM, "scripts"))
from deadsim import Loadout, game
from deadsim.engine import Engine
from deadsim.fight import make_fighter
from deadsim.accuracy import default_distance, hero_default_skill
import deadsim.mechanics as M
import landing_rates as L
G = game(); ITEM = sys.argv[2]; SIDE = sys.argv[3]
mech = M.Mechanics()
def run(ia, sa, ha, ib, sb, hb):
    e = Engine(distance=(default_distance(ha) + default_distance(hb)) / 2, max_time=45, mech=mech)
    fa = make_fighter(e, Loadout(ha, ia, souls=sa, skill=hero_default_skill(ha)), "A")
    fb = make_fighter(e, Loadout(hb, ib, souls=sb, skill=hero_default_skill(hb)), "B")
    mark = {}
    def mon():
        if "A" not in mark and fa.alive and fb.alive and fa.hp_frac < 0.25: mark["A"] = e.t
        e.after(0.25, mon)
    e.at(0.25, mon)
    r = e.run(fa, fb)
    if "A" not in mark: return None
    t0 = mark["A"]
    if not fa.alive and fa.death_time <= t0 + 10: return 0
    if r.escaped == "A" and r.time <= t0 + 10: return 1
    return None
acc = {"with": [0, 0], "without": [0, 0]}
for line in gzip.open(os.path.join(SIM, "validation", "matches_sample.jsonl.gz")):
    m = json.loads(line)
    for p in m["players"]:
        if p["hero_id"] not in G.heroes: continue
        foes = [q for q in m["players"] if q["team"] != p["team"] and q["hero_id"] in G.heroes]
        rnd = random.Random(m["match_id"] * 7 + p["slot"])
        t = m["duration_s"] * rnd.choice(L.FRACS); q = rnd.choice(foes)
        ia, sa = L.build_at(p, t); ib, sb = L.build_at(q, t)
        if sa < 9000: continue
        ha, hb = G.hero(p["hero_id"]).name, G.hero(q["hero_id"]).name
        iid = G.item(ITEM).id
        ia0 = [i for i in ia if i != iid]; ib0 = [i for i in ib if i != iid]
        for key, (x, y) in (("without", (ia0, ib0)), ("with", ((ia0 + [iid], ib0) if SIDE == "A" else (ia0, ib0 + [iid])))):
            o = run(x, sa, ha, y, sb, hb)
            if o is not None:
                acc[key][0] += o; acc[key][1] += 1
w, wo = acc["with"], acc["without"]
print(f"{ITEM:18s} side {SIDE}  escape share with {w[0]/max(1,w[1]):.3f} (n={w[1]})  without {wo[0]/max(1,wo[1]):.3f} (n={wo[1]})  diff {w[0]/max(1,w[1]) - wo[0]/max(1,wo[1]):+.3f}")
