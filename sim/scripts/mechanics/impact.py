import gzip, json, random, sys, os, time, statistics
SIM = sys.argv[1]; sys.path.insert(0, SIM); sys.path.insert(0, os.path.join(SIM, "scripts"))
from deadsim import Loadout, duel, game
from deadsim.accuracy import default_distance, hero_default_skill
from deadsim.mechanics import Mechanics
import landing_rates as L
G = game(); pairs = []
for line in gzip.open(os.path.join(SIM, "validation", "matches_sample.jsonl.gz")):
    m = json.loads(line)
    for p in m["players"][:3]:
        if p["hero_id"] not in G.heroes: continue
        rnd = random.Random(m["match_id"] + p["slot"]); q = rnd.choice([x for x in m["players"] if x["team"] != p["team"] and x["hero_id"] in G.heroes])
        t = m["duration_s"] * rnd.choice(L.FRACS); ia, sa = L.build_at(p, t); ib, sb = L.build_at(q, t)
        ha, hb = G.hero(p["hero_id"]).name, G.hero(q["hero_id"]).name
        pairs.append((Loadout(ha, ia, souls=sa, skill=hero_default_skill(ha)), Loadout(hb, ib, souls=sb, skill=hero_default_skill(hb)), (default_distance(ha) + default_distance(hb)) / 2))
out = {}
for key, mech in (("old", None), ("new", Mechanics())):
    t0 = time.time(); rs = [duel(a, b, distance=d, max_time=30, mechanics=mech) for a, b, d in pairs]
    out[key] = rs
    print(key, "duels", len(rs), "ms/duel", round((time.time() - t0) / len(rs) * 1000, 1), "decided", round(sum(r.winner is not None for r in rs) / len(rs), 3),
          "escaped", round(sum(r.escaped is not None for r in rs) / len(rs), 3), "median t", round(statistics.median(r.time for r in rs), 1))
same = sum(o.winner == n.winner for o, n in zip(out["old"], out["new"]))
flip = sum(o.winner is not None and n.winner is not None and o.winner != n.winner for o, n in zip(out["old"], out["new"]))
print("same result", round(same / len(pairs), 3), "winner flipped", round(flip / len(pairs), 3))
