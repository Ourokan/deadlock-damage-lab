"""Audit: how the sim's damage mix compares with real Phantom+ matches, per hero and per item, with the model as the
build searches use it (ability landing factors, real-data item factors, counterplay, mechanics, melee by build).

For each player-match in the sample, duel the player's real build (items and net worth at 30/60/90% of the match,
the player's real hero accuracy and headshot rate) against a real enemy from the same match at the same moment,
with the real mean count of other enemies near the target (Mechanics.extra_targets = mechanics.real_nearby, as the
searches fight; Ricochet and Split Shot hits on them count, and area items' replay-measured extra hits on other
heroes (mechanics.area_extra), since the real damage matrix has every enemy hero),
then compare where the damage comes from with the match's real damage matrix (damage to enemy heroes):

- per hero: share of gun / abilities / items / melee, real vs sim, and the total distance between the two mixes
  (half the sum of absolute share differences: 0 = same mix, 1 = nothing in common);
- per hero and source (each ability, each item): real / sim ratio of (source damage / gun damage);
- per item, item holders only, pooled over heroes: real vs sim (item damage / gun damage while the item was owned:
  real gun damage between buy and sell time from the damage matrix samples, sim gun damage of the duels whose
  build had the item). Needs a sample with damage_series (fetch_validation.py since 2026-10-24).

Unlike landing_rates.py and item_landing.py this fits nothing and writes no model data; it says where the model
is furthest from real games now. Output: validation/damage_audit.json and validation/damage_audit.md.

usage: python3 scripts/damage_audit.py <sample.jsonl.gz> [max_players] [workers] [--badge N]
The sample comes from scripts/fetch_validation.py (e.g. --api 91 5 for Phantom+ of the last 5 days).
"""
import collections
import dataclasses
import gzip
import json
import math
import os
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deadsim import Loadout, duel, game  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
from deadsim.mechanics import DEFAULT as MECH, RICOCHET_RADIUS, area_extra, real_length, real_nearby  # noqa: E402
from deadsim.accuracy import HEADS, HITS, SHOTS, default_distance, gun_calibrated, hero_default_skill  # noqa: E402
import landing_rates as L  # noqa: E402

BADGE = 91
HERO_ITEM_MIN = 20   # holders for a per-hero item row
COUNTERPLAY = True   # item_landing.py fits with this off (items uncut) and everything else as the searches fight
PROFILE = False      # scripts/fight_length/profile_check.py: also "_by2s:k" / "_alive:k" (damage, duels going)
LENGTH = True        # damage expected over real fight lengths (mechanics.real_length); --no-length: in full to 20 s
_sk = {}


def sim_sources(r, key, exp=True):
    """The duel's damage to enemy heroes by source (key maps a sim source to the audit's name): the main target's,
    Ricochet / Split Shot hits on the other enemies near it, and area items' real extra hits on other heroes
    (x mechanics.area_extra, area_hits.json). exp: expected over real fight lengths (= in full when the duel's
    mechanics have no fight_length), else every hit in full."""
    d = collections.Counter()
    for k, v in (r.a_exp if exp else r.a_dmg).items():
        d[key(k)] += v * (1.0 + (area_extra(k) or 0.0))
    for k, v in (r.a_splash_exp if exp else r.a_splash).items():
        d[key(k)] += v
    return d


def skill_of(p):
    """The search's skill for the hero (landing factors, counterplay, melee by build), with the player's real aim."""
    hid = p["hero_id"]
    if hid not in _sk:
        _sk[hid] = hero_default_skill(game().hero(hid).name, badge=BADGE, counterplay=COUNTERPLAY)
    sk = _sk[hid]
    c = p["custom"]
    shots, hits = c.get(SHOTS, 0), c.get(HITS, 0)
    if shots >= 300 and not gun_calibrated(hid):   # Danny's API shots are a partial count: keep the replay fit
        sk = dataclasses.replace(sk, accuracy=hits / shots, headshot=c.get(HEADS, 0) / max(1, hits))
    return sk


def kind(key, G, classes):
    if key == "GUN":
        return "gun"
    if key == "MELEE":
        return "melee"
    if key.startswith("upgrade_") or key.lower() in G.items_by_name:
        return "item"
    if key in classes or (key in L.ALIASES.values() and key not in L.ENEMY_BOOKED):
        return "ability"
    return "other"


def sim_player(job, both=False):
    """(hero id, sim damage by source, {item: [item dmg, gun dmg] of the duels holding it}); both=True: each of the
    two as a pair (expected over real fight lengths, in full) from the same duels (scripts/fight_length)."""
    m, slot = job
    G = game()
    load_heroes()
    me = next(p for p in m["players"] if p["slot"] == slot)
    foes = [p for p in m["players"] if p["team"] != me["team"] and p["hero_id"] in G.heroes]
    h = G.hero(me["hero_id"])
    names = {ab.name: ab.class_name for ab in h.abilities}
    rnd = random.Random(m["match_id"] * 31 + slot)
    out, out_u = collections.Counter(), collections.Counter()
    held = collections.defaultdict(lambda: [0.0, 0.0])   # item class -> [sim item dmg, sim gun dmg] in duels holding it
    held_u = collections.defaultdict(lambda: [0.0, 0.0])
    for frac in L.FRACS:
        t = m["duration_s"] * frac
        items, souls = L.build_at(me, t)
        foe = rnd.choice(foes)
        fitems, fsouls = L.build_at(foe, t)
        a = Loadout(h.name, items, souls=souls, skill=skill_of(me))
        b = Loadout(foe["hero_id"], fitems, souls=fsouls, skill=skill_of(foe))
        try:
            mech = dataclasses.replace(MECH, extra_targets=real_nearby("extra", RICOCHET_RADIUS, souls),
                                       fight_length=real_length(souls) if LENGTH else None)
            r = duel(a, b, distance=default_distance(h.name), max_time=L.FIGHT_TIME, rng=random.Random(rnd.random()),
                     mechanics=mech)
        except Exception as e:  # noqa: BLE001
            out["_err:" + type(e).__name__ + ":" + str(e)[:80]] += 1
            continue
        if PROFILE:
            for k, v in r.a_by_2s.items():
                out[f"_by2s:{k}"] += v
            for k in range(int(math.ceil(r.time / 2))):
                out[f"_alive:{k}"] += 1
            # opener timing (scripts/fight_length/opener_timing.py): first hit of each held source, 0.5 s buckets,
            # "_fu" used in the bucket, "_fc" duel over in the bucket without a use
            first = {}
            for k, v in r.a_first.items():
                key = L.sim_key(k, names, G)
                first[key] = min(v, first.get(key, v))
            have = set(names.values()) | {G.items[i].class_name for i in items} | set(first)
            for key in have:
                if key in ("GUN", "MELEE"):
                    continue
                if key in first:
                    out[f"_fu:{key}:{min(40, int(first[key] / 0.5))}"] += 1
                else:
                    out[f"_fc:{key}:{min(40, int(r.time / 0.5))}"] += 1
            for (k, b), v in r.a_src_2s.items():
                out[f"_s2:{L.sim_key(k, names, G)}:{b}"] += v
        for o, hd, exp in ((out, held, True), (out_u, held_u, False)) if both else ((out, held, True),):
            d = sim_sources(r, lambda k: L.sim_key(k, names, G), exp)
            o.update(d)
            for i in items:
                c = G.items[i].class_name
                hd[c][0] += d.get(c, 0.0)
                hd[c][1] += d.get("GUN", 0.0)
    if both:
        return me["hero_id"], (dict(out), dict(out_u)), (dict(held), dict(held_u))
    return me["hero_id"], dict(out), dict(held)


def mix(c, G, classes):
    tot = sum(c.values()) or 1.0
    k = collections.Counter()
    for s, v in c.items():
        k[kind(s, G, classes)] += v / tot
    return {x: round(k.get(x, 0.0), 4) for x in ("gun", "ability", "item", "melee", "other")}


def main():
    args = sys.argv[1:]
    global BADGE, LENGTH
    if "--no-length" in args:
        LENGTH = False
        args.remove("--no-length")
    if "--badge" in args:
        i = args.index("--badge")
        BADGE = int(args[i + 1])
        args = args[:i] + args[i + 2:]
    sample = args[0]
    max_players = int(args[1]) if len(args) > 1 else 10 ** 9
    workers = int(args[2]) if len(args) > 2 else os.cpu_count()
    G = game()
    load_heroes()
    real = collections.defaultdict(collections.Counter)
    real_item = collections.defaultdict(lambda: [0.0, 0.0, 0])   # item -> [item dmg, gun dmg, holders]
    real_hero_item = collections.defaultdict(lambda: [0.0, 0.0, 0])   # (hero, item) -> the same, per hero
    jobs, real_of, held_of = [], {}, {}
    n_matches = 0
    for line in gzip.open(sample):
        m = json.loads(line)
        n_matches += 1
        for p in m["players"]:
            if p["hero_id"] not in G.heroes or not L.gun_known(p):
                continue
            classes = [ab.class_name for ab in G.hero(p["hero_id"]).abilities]
            d = collections.Counter()
            for k, v in p["damage_sources"].items():
                if k not in L.CATEGORY:
                    d[L.real_key(k, classes)] += v
            real_of[m["match_id"], p["slot"]] = d
            hg = L.held_gun(m, p)
            if hg is not None:
                held_of[m["match_id"], p["slot"]] = hg
            jobs.append((m, p["slot"]))
    random.Random(1).shuffle(jobs)
    jobs = jobs[:max_players]
    sim = collections.defaultdict(collections.Counter)
    sim_item = collections.defaultdict(lambda: [0.0, 0.0, 0])
    sim_hero_item = collections.defaultdict(lambda: [0.0, 0.0, 0])
    errs = collections.Counter()
    t0 = time.time()
    with ProcessPoolExecutor(workers) as ex:
        for i, ((m, slot), (hid, d, held)) in enumerate(zip(jobs, ex.map(sim_player, jobs, chunksize=8))):
            rd = real_of[m["match_id"], slot]
            real[hid].update(rd)
            for k, v in d.items():
                (errs if k.startswith("_") else sim[hid])[k] += v
            # holders only, and only gun damage while the item was owned: real = gun damage between buy and sell
            # (damage matrix samples), sim = the duels whose build had it
            hg = held_of.get((m["match_id"], slot))
            for it, (si, sg) in held.items():
                if hg is None or hg.get(it, 0) <= 0:
                    continue
                for acc, key, a, b in ((real_item, it, rd.get(it, 0.0), hg[it]), (sim_item, it, si, sg),
                                       (real_hero_item, (hid, it), rd.get(it, 0.0), hg[it]),
                                       (sim_hero_item, (hid, it), si, sg)):
                    row = acc[key]
                    row[0] += a
                    row[1] += b
                    row[2] += 1
            if i % 500 == 0:
                print(f"{i}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    print("errors:", errs.most_common(10))

    heroes = {}
    for hid in sorted(sim):
        h = G.hero(hid)
        classes = {ab.class_name for ab in h.abilities}
        r, s = real[hid], sim[hid]
        rm, sm = mix(r, G, classes), mix(s, G, classes)
        dist = 0.5 * sum(abs(rm[k] - sm[k]) for k in rm)
        rt, st = sum(r.values()) or 1.0, sum(s.values()) or 1.0
        srcs = {}
        for k in set(r) | set(s):
            rs, ss = r.get(k, 0) / rt, s.get(k, 0) / st
            if max(rs, ss) < 0.01 or k == "GUN":
                continue
            ratio = None
            if r["GUN"] > 0 and s["GUN"] > 0 and s.get(k, 0) > 0:
                ratio = round((r.get(k, 0) / r["GUN"]) / (s[k] / s["GUN"]), 3)
            name = G.items_by_class[k].name if k in G.items_by_class else next(
                (ab.name for ab in h.abilities if ab.class_name == k), k)
            srcs[k] = {"name": name, "kind": kind(k, G, classes), "real_share": round(rs, 4),
                       "sim_share": round(ss, 4), "real_over_sim": ratio}
        heroes[h.name] = {"players": 0, "real_mix": rm, "sim_mix": sm, "mix_distance": round(dist, 3),
                          "sources": dict(sorted(srcs.items(), key=lambda x: -x[1]["real_share"]))}
    counts = collections.Counter()
    for (m, slot) in jobs:
        p = next(p for p in m["players"] if p["slot"] == slot)
        counts[p["hero_id"]] += 1
    for hid in sim:
        heroes[G.hero(hid).name]["players"] = counts[hid]

    items = {}
    for it, (ri, rg, n) in real_item.items():
        si, sg, _ = sim_item[it]
        if n < 25 or it not in G.items_by_class or (ri <= 0 and si <= 0):
            continue
        rp, sp = (ri / rg if rg else 0.0), (si / sg if sg else 0.0)
        if max(rp, sp) < 0.01:
            continue
        items[it] = {"name": G.items_by_class[it].name, "holders": n, "real_per_gun": round(rp, 4),
                     "sim_per_gun": round(sp, 4), "real_over_sim": round(rp / sp, 3) if sp > 0 else None}

    # the same per hero: the hero table's shares compare the whole real match (early game without the item
    # included) with duels at 30/60/90% of it, which overweights items bought mid-game; this one doesn't
    hero_items = []
    for (hid, it), (ri, rg, n) in real_hero_item.items():
        si, sg, _ = sim_hero_item[hid, it]
        # sim 0: bookkeeping (amps booked under the hit's source) or multi-target items, see validation/README.md
        if n < HERO_ITEM_MIN or it not in G.items_by_class or rg <= 0 or sg <= 0 or si <= 0 or max(ri / rg, si / sg) < 0.02:
            continue
        rp, sp = ri / rg, si / sg
        hero_items.append({"hero": G.hero(hid).name, "item": G.items_by_class[it].name, "holders": n,
                           "real_per_gun": round(rp, 4), "sim_per_gun": round(sp, 4),
                           "real_over_sim": round(rp / sp, 3) if sp > 0 else None})
    hero_items.sort(key=lambda x: -abs(math.log(x["real_over_sim"])) if x["real_over_sim"] else -9.0)

    meta = {"sample": os.path.basename(sample), "matches": n_matches, "player_matches": len(jobs),
            "duels": f"{len(L.FRACS)} per player-match, {L.FIGHT_TIME:.0f} s max, real builds both sides, "
                     "real nearby enemies (extra_targets)",
            "model": f"hero_default_skill(badge={BADGE}, counterplay=True) with each player's real aim",
            "errors": sum(errs.values())}
    out = {"meta": meta, "heroes": dict(sorted(heroes.items(), key=lambda x: -x[1]["mix_distance"])),
           "items": dict(sorted(items.items(), key=lambda x: -x[1]["holders"])), "hero_items": hero_items}
    json.dump(out, open(os.path.join(ROOT, "validation", "damage_audit.json"), "w"), indent=1)
    write_md(out)


def fmt_ratio(x):
    return "-" if x is None else f"{x:.2f}"


def write_md(out):
    L_ = ["# Sim vs real damage mix audit", "",
          f"Sample: {out['meta']['matches']} matches, {out['meta']['player_matches']} player-matches "
          f"({out['meta']['sample']}). Model: {out['meta']['model']}. "
          f"Duels: {out['meta']['duels']}.", "",
          "## Heroes by how far the damage mix is off", "",
          "Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).", "",
          "| Hero | n | gun real / sim | abilities | items | melee | distance |", "|---|---|---|---|---|---|---|"]
    for hn, h in out["heroes"].items():
        r, s = h["real_mix"], h["sim_mix"]
        L_.append(f"| {hn} | {h['players']} | {r['gun']:.2f} / {s['gun']:.2f} | {r['ability']:.2f} / {s['ability']:.2f}"
                  f" | {r['item']:.2f} / {s['item']:.2f} | {r['melee']:.2f} / {s['melee']:.2f} | {h['mix_distance']:.2f} |")
    L_ += ["", "## Sources furthest off (share of hero damage at least 3% in real or sim)", "",
           "real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates "
           "the source against the gun.", "",
           "| Hero | Source | kind | real share | sim share | real/sim |", "|---|---|---|---|---|---|"]
    rows = []
    for hn, h in out["heroes"].items():
        for k, v in h["sources"].items():
            if max(v["real_share"], v["sim_share"]) >= 0.03:
                x = v["real_over_sim"]
                off = abs(math.log(x)) if x else 9.0
                rows.append((off * max(v["real_share"], v["sim_share"]), hn, v))
    for _, hn, v in sorted(rows, key=lambda x: -x[0])[:40]:
        L_.append(f"| {hn} | {v['name']} | {v['kind']} | {v['real_share']:.3f} | {v['sim_share']:.3f} | "
                  f"{fmt_ratio(v['real_over_sim'])} |")
    L_ += ["", "## Items (holders only, all heroes)", "",
           "Item damage per gun damage while the item was owned (players who had it at a sampled point). "
           "real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).", "",
           "| Item | holders | real per gun | sim per gun | real/sim |", "|---|---|---|---|---|"]
    for k, v in out["items"].items():
        L_.append(f"| {v['name']} | {v['holders']} | {v['real_per_gun']:.3f} | {v['sim_per_gun']:.3f} | "
                  f"{fmt_ratio(v['real_over_sim'])} |")
    L_ += ["", f"## Items by hero (holders only, at least {HERO_ITEM_MIN} holders), furthest off first", "",
           "As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, "
           "so an item bought mid-game looks overrated there; this table doesn't have that bias.", "",
           "| Hero | Item | holders | real per gun | sim per gun | real/sim |", "|---|---|---|---|---|---|"]
    for v in out.get("hero_items", [])[:40]:
        L_.append(f"| {v['hero']} | {v['item']} | {v['holders']} | {v['real_per_gun']:.3f} | {v['sim_per_gun']:.3f} | "
                  f"{fmt_ratio(v['real_over_sim'])} |")
    open(os.path.join(ROOT, "validation", "damage_audit.md"), "w").write("\n".join(L_) + "\n")


if __name__ == "__main__":
    main()
