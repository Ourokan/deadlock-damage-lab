"""Per hero: does a fight pattern (cast order + ult setup) make the sim fight like real players?

Runs the damage audit's duels (scripts/damage_audit.py: real builds both sides at 30/60/90% of the match, the
search skill with each player's real aim, real nearby enemies, damage expected over real fight lengths) for the
given heroes, once per variant of the hero's fight pattern, and compares with the Phantom+ replays
(data/fight_patterns.json 'replay' block):

- casts: per ability, the share of duels it is cast in before the real fight would likely have ended (each cast
  weighted by the real chance the fight is still going at that time, mechanics.fight_length), its share of being
  the first ability cast, and the median time of its first cast, next to the replay's cast_share / first_share /
  median_first_cast_s. ult_after: share of fights with an ult whose cast came after each setup ability.
- mix: the audit's damage mix distance (gun / abilities / items / melee) and the mean |log real/sim| of the
  hero's ability sources (source damage per gun damage), with the current landing factors.

The timing error is the mean over abilities of |sim - real| for first_share and cast_share plus
|log(sim / real median first cast)| / 4, so one is roughly a share point.

usage: python3 scripts/fight_patterns/combo_check.py <sample.jsonl.gz> <out.json> HERO [HERO ...]
       [--variant NAME=order1,order2|ult_after1,ult_after2 ...]
Variants: "off" (slot order) and "replay" (the file's replay_order / replay_ult_after) always run.
"""
import collections
import dataclasses
import gzip
import json
import math
import os
import random
import statistics
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.join(HERE, "..", "..")
sys.path.insert(0, SIM)
sys.path.insert(0, os.path.join(SIM, "scripts"))
import damage_audit as A  # noqa: E402
import landing_rates as L  # noqa: E402
from deadsim import Loadout, duel, game  # noqa: E402
from deadsim import abilities as AB  # noqa: E402
from deadsim import engine as EN  # noqa: E402
from deadsim import patterns as P  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
from deadsim.accuracy import default_distance  # noqa: E402
from deadsim.mechanics import DEFAULT as MECH, LENGTH_STEP, RICOCHET_RADIUS, real_length, real_nearby  # noqa: E402

ROW = {}            # hero id -> pattern row for this run (set before the pool forks)
CASTS = []
LAST = {}

_cast = AB.AbilityState.cast
_run = EN.Engine.run
_pattern = P.pattern


def cast(self):
    CASTS.append((self.f, self.ab.name, self.ab.ultimate, self.f.e.t))
    return _cast(self)


def run(self, fa, fb, *a, **k):
    LAST["a"] = fa
    return _run(self, fa, fb, *a, **k)


def pattern(hid):
    return ROW.get(int(hid), _pattern(hid))


AB.AbilityState.cast = cast
EN.Engine.run = run
P.pattern = pattern


def surv_fn(curve):
    """S(t) from a mechanics.real_length curve (survival at t = 0, LENGTH_STEP, ...), 1 without one."""
    if curve is None:
        return lambda t: 1.0

    def alive(t):
        x = max(0.0, t) / LENGTH_STEP   # (precasts come before t = 0: the fight is surely still on)
        i = int(x)
        if i + 1 >= len(curve):
            return max(0.0, min(1.0, curve[-1]))
        return max(0.0, min(1.0, curve[i] + (x - i) * (curve[i + 1] - curve[i])))
    return alive


def sim_player(job):
    m, slot, _ = job
    G = game()
    load_heroes()
    me = next(p for p in m["players"] if p["slot"] == slot)
    foes = [p for p in m["players"] if p["team"] != me["team"] and p["hero_id"] in G.heroes]
    h = G.hero(me["hero_id"])
    names = {ab.name: ab.class_name for ab in h.abilities}
    rnd = random.Random(m["match_id"] * 31 + slot)
    out = collections.Counter()
    fights = []
    for frac in L.FRACS:
        t = m["duration_s"] * frac
        items, souls = L.build_at(me, t)
        foe = rnd.choice(foes)
        fitems, fsouls = L.build_at(foe, t)
        a = Loadout(h.name, items, souls=souls, skill=A.skill_of(me))
        b = Loadout(foe["hero_id"], fitems, souls=fsouls, skill=A.skill_of(foe))
        mech = dataclasses.replace(MECH, extra_targets=real_nearby("extra", RICOCHET_RADIUS, souls),
                                   fight_length=real_length(souls))
        CASTS.clear()
        try:
            r = duel(a, b, distance=default_distance(h.name), max_time=L.FIGHT_TIME, rng=random.Random(rnd.random()),
                     mechanics=mech)
        except Exception as e:  # noqa: BLE001
            out["_err:" + type(e).__name__ + ":" + str(e)[:80]] += 1
            continue
        fa = LAST["a"]
        casts = [(n, u, tt) for f, n, u, tt in CASTS if f is fa]
        fights.append({"casts": casts, "souls": souls, "time": r.time})
        out.update(A.sim_sources(r, lambda k: L.sim_key(k, names, G), True))
    return me["hero_id"], dict(out), fights


def timing(fights, h, row):
    """Sim cast stats per ability (weighted by the real chance the fight still goes on at the cast)."""
    res = {}
    W = 0.0
    cast_w = collections.Counter()
    first_w = collections.Counter()
    first_t = collections.defaultdict(list)
    ult_w, after_w = 0.0, collections.Counter()
    for fi in fights:
        alive = surv_fn(real_length(fi["souls"]))
        W += 1.0
        seen = {}
        for n, u, t in fi["casts"]:
            seen.setdefault(n, (t, u))
        for n, (t, u) in seen.items():
            w = alive(t)
            cast_w[n] += w
            first_t[n].append((t, w))
        if seen:
            # first among casts, weighted by the chance the fight got that far
            n0, (t0, _) = min(seen.items(), key=lambda x: x[1][0])
            first_w[n0] += alive(t0)
        ult = next(((n, t) for n, (t, u) in seen.items() if u), None)
        if ult:
            wu = alive(ult[1])
            ult_w += wu
            for n, (t, u) in seen.items():
                if not u and t <= ult[1]:
                    after_w[n] += wu
    tot_first = sum(first_w.values()) or 1.0
    for ab in h.abilities:
        n = ab.name
        ts = sorted(first_t.get(n, []))
        med = None
        if ts:
            half, acc = sum(w for _, w in ts) / 2, 0.0
            for t, w in ts:
                acc += w
                if acc >= half:
                    med = t
                    break
        res[n] = {"cast_share": round(cast_w[n] / W, 3) if W else 0.0,
                  "first_share": round(first_w[n] / tot_first, 3),
                  "median_first_cast_s": None if med is None else round(med, 2),
                  "ult_after_share": round(after_w[n] / ult_w, 3) if ult_w and not ab.ultimate else None}
    return res


def timing_error(sim, real):
    errs = []
    for n, rr in real.items():
        if rr.get("cast_share", 0) < 0.05 or n not in sim:   # passives (Fixation) carry no casts
            continue
        s = sim[n]
        e = abs(s["first_share"] - rr["first_share"]) + abs(s["cast_share"] - rr["cast_share"])
        if rr.get("median_first_cast_s") and s["median_first_cast_s"]:
            e += abs(math.log(max(0.2, s["median_first_cast_s"]) / max(0.2, rr["median_first_cast_s"]))) / 4
        else:
            e += 0.5
        errs.append(e)
    return round(sum(errs) / max(1, len(errs)), 3)


def mix_stats(real, sim, h, G):
    classes = {ab.class_name for ab in h.abilities}
    rm, sm = A.mix(real, G, classes), A.mix(sim, G, classes)
    dist = 0.5 * sum(abs(rm[k] - sm[k]) for k in rm)
    logs = {}
    for ab in h.abilities:
        k = ab.class_name
        if real.get(k, 0) > 0 and sim.get(k, 0) > 0 and real["GUN"] > 0 and sim["GUN"] > 0:
            logs[ab.name] = round((real[k] / real["GUN"]) / (sim[k] / sim["GUN"]), 3)
    err = sum(abs(math.log(v)) for v in logs.values()) / max(1, len(logs))
    return {"mix_distance": round(dist, 3), "ability_real_over_sim": logs, "ability_log_err": round(err, 3),
            "real_mix": rm, "sim_mix": sm}


def main():
    args = sys.argv[1:]
    variants = {}
    while "--variant" in args:
        i = args.index("--variant")
        name, spec = args[i + 1].split("=", 1)
        order, _, after = spec.partition("|")
        variants[name] = ([x for x in order.split(",") if x], [x for x in after.split(",") if x])
        args = args[:i] + args[i + 2:]
    sample, out_path, heroes = args[0], args[1], args[2:]
    G = game()
    load_heroes()
    hids = [G.hero(n).id for n in heroes]
    real = collections.defaultdict(collections.Counter)
    jobs = []
    for line in gzip.open(sample):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] not in hids:
                continue
            known = L.gun_known(p)   # the damage mix needs real gun data; cast timing takes every player
            if known:
                classes = [ab.class_name for ab in G.hero(p["hero_id"]).abilities]
                for k, v in p["damage_sources"].items():
                    if k not in L.CATEGORY:
                        real[p["hero_id"]][L.real_key(k, classes)] += v
            jobs.append((m, p["slot"], known))
    print("player-matches", len(jobs), flush=True)
    rows = {hid: _pattern(hid) for hid in hids}
    result = {}
    names = ["off", "replay"] + list(variants)
    for vn in names:
        ROW.clear()
        for hid in hids:
            base = dict(rows[hid])
            if vn == "off":
                base.update(order=[], ult_after=[], prefight=None)
            elif vn == "replay":
                base.update(order=base.get("replay_order", []), ult_after=base.get("replay_ult_after", []))
            else:
                base.update(order=variants[vn][0], ult_after=variants[vn][1])
            ROW[hid] = base
        sim = collections.defaultdict(collections.Counter)
        fights = collections.defaultdict(list)
        with ProcessPoolExecutor(os.cpu_count()) as ex:
            for (_, _, known), (hid, d, fs) in zip(jobs, ex.map(sim_player, jobs, chunksize=4)):
                if known:
                    sim[hid].update({k: v for k, v in d.items() if not k.startswith("_")})
                fights[hid].extend(fs)
        for hid in hids:
            h = G.hero(hid)
            rr = rows[hid]["replay"]["abilities"]
            t = timing(fights[hid], h, ROW[hid])
            ms = mix_stats(real[hid], sim[hid], h, G)
            r = result.setdefault(h.name, {"real": rr, "players": sum(1 for m, s, _ in jobs if next(
                p for p in m["players"] if p["slot"] == s)["hero_id"] == hid),
                "mix_players": sum(1 for m, s, k in jobs if k and next(
                    p for p in m["players"] if p["slot"] == s)["hero_id"] == hid)})
            r[vn] = {"order": ROW[hid]["order"], "ult_after": ROW[hid]["ult_after"], "timing": t,
                     "timing_error": timing_error(t, rr), **ms}
            print(f"{h.name:10} {vn:8} timing err {r[vn]['timing_error']:.3f}  mix {ms['mix_distance']:.3f}  "
                  f"abil log err {ms['ability_log_err']:.3f}  {ms['ability_real_over_sim']}", flush=True)
            for n, s in t.items():
                rv = rr.get(n, {})
                print(f"    {n:24} cast {s['cast_share']:.2f}/{rv.get('cast_share', 0):.2f}  first "
                      f"{s['first_share']:.2f}/{rv.get('first_share', 0):.2f}  t1 {s['median_first_cast_s']}/"
                      f"{rv.get('median_first_cast_s')}  ult_after {s['ult_after_share']}/{rv.get('ult_after_share')}")
    json.dump(result, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
