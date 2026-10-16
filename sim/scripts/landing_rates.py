"""Fit per-ability effective landing rates and compare simulated vs real damage shares.

For each player-match in validation/matches_sample.jsonl.gz, duel the player's real build (items owned and net
worth at three points of the match, real gun accuracy and headshot rate) against a real enemy build from the same
match at the same moment, with every ability landing 100%. Then, per hero, compare the ratio
(ability damage / gun damage) in the sim with the same ratio in the real damage matrix:

    landing(ability) = (real ability dmg / real gun dmg) / (sim ability dmg / sim gun dmg)

The gun is calibrated by real accuracy, so this factor absorbs everything about the ability the sim can't see:
missed skillshots, partial AoE/DoT uptime, casts on creeps or not at all, fights shorter than a cooldown.
Values above 1 mean real players get more from the ability than the 1v1 sim gives it (multi-target hits, model
gaps). Output: data/landing_rates.json (used by Skill.ability_landing) and validation/damage_shares.json.

Melee: each fighter melees at its hero's rate from data/melee_rates.json. With --fit-melee the rates are refitted
(rate x real melee/gun ratio / sim melee/gun ratio) and written back; run it 2-3 times to converge.

usage: python3 scripts/landing_rates.py [max_players] [workers] [--fit-melee] [--hero NAME ...]
With --hero it runs only those heroes and prints real vs sim damage shares without writing any files.
"""
import collections
import gzip
import json
import os
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from deadsim import Loadout, Skill, duel, game  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
from deadsim.accuracy import HEADS, HITS, SHOTS, default_distance  # noqa: E402

CATEGORY = {"Bullet", "Ability", "Melee", "Misc"}   # per-damage-type totals in the matrix, not sources
MIN_HITS = 150
FIGHT_TIME = 20.0
FRACS = (0.3, 0.6, 0.9)


def real_key(name, classes):
    """Normalize a damage-matrix source name: gun -> GUN, melee -> MELEE, ability sub-sources
    (e.g. citadel_ability_shiv_dagger_dot) -> their ability class."""
    if name.startswith("citadel_weapon") or "_primary_weapon" in name:
        return "GUN"
    if "ability_melee_" in name:
        return "MELEE"
    best = max((c for c in classes if name == c or name.startswith(c + "_")), key=len, default=None)
    return best or name


def sim_key(name, names, G):
    """Normalize a sim damage source: ability names (or labels starting with one) -> ability class."""
    if name == "gun":
        return "GUN"
    if name.lower().startswith("melee"):
        return "MELEE"
    if name in names:
        return names[name]
    if name.lower() in G.items_by_name:
        return G.items_by_name[name.lower()].class_name
    best = max((n for n in names if name.startswith(n)), key=len, default=None)
    return names[best] if best else name


MELEE_FILE = os.path.join(ROOT, "data", "melee_rates.json")
try:
    MELEE = {int(k): v["rate"] for k, v in json.load(open(MELEE_FILE))["heroes"].items()}
except (OSError, ValueError, KeyError):
    MELEE = {}
MELEE_START = 0.1   # melee hits/s used for a hero not yet fitted


def skill_of(p):
    c = p["custom"]
    shots, hits = c.get(SHOTS, 0), c.get(HITS, 0)
    rate = MELEE.get(p["hero_id"], MELEE_START)
    if shots < 300:
        return Skill(melee_rate=rate)
    return Skill(accuracy=hits / shots, headshot=c.get(HEADS, 0) / max(1, hits), melee_rate=rate)


def build_at(p, t):
    G = game()
    items = [i for i, bt, st, _ in p["items"] if i in G.items and bt <= t and (st == 0 or st > t) and G.items[i].cost > 0]
    snaps = [s for s in p["stats"] if s["time_stamp_s"] <= t] or p["stats"][:1]
    return items, snaps[-1]["net_worth"]


def sim_player(job):
    m, slot = job
    G = game()
    load_heroes()
    me = next(p for p in m["players"] if p["slot"] == slot)
    foes = [p for p in m["players"] if p["team"] != me["team"] and p["hero_id"] in G.heroes]
    h = G.hero(me["hero_id"])
    names = {ab.name: ab.class_name for ab in h.abilities}
    rnd = random.Random(m["match_id"] * 31 + slot)
    out = collections.Counter()
    fights = 0
    for frac in FRACS:
        t = m["duration_s"] * frac
        items, souls = build_at(me, t)
        foe = rnd.choice(foes)
        fitems, fsouls = build_at(foe, t)
        a = Loadout(h.name, items, souls=souls, skill=skill_of(me))
        b = Loadout(foe["hero_id"], fitems, souls=fsouls, skill=skill_of(foe))
        try:
            r = duel(a, b, distance=default_distance(h.name), max_time=FIGHT_TIME)
        except Exception as e:  # noqa: BLE001 - a broken hero file shouldn't kill the run
            out["_errors"] += 1
            out["_err:" + type(e).__name__ + ":" + str(e)[:80]] += 1
            continue
        fights += 1
        for k, v in r.a_dmg.items():
            out[sim_key(k, names, G)] += v
    return me["hero_id"], dict(out), fights


def main():
    args = sys.argv[1:]
    fit_melee = "--fit-melee" in args
    args = [a for a in args if a != "--fit-melee"]
    only = set()
    if "--hero" in args:
        i = args.index("--hero")
        only = {game().hero(" ".join(args[i + 1:])).id} if args[i + 1:] else set()
        args = args[:i]
    max_players = int(args[0]) if len(args) > 0 else 10 ** 9
    workers = int(args[1]) if len(args) > 1 else os.cpu_count()
    G = game()
    load_heroes()
    real = collections.defaultdict(collections.Counter)
    jobs = []
    for line in gzip.open(os.path.join(ROOT, "validation", "matches_sample.jsonl.gz")):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] not in G.heroes or p["custom"].get(HITS, 0) < MIN_HITS or (only and p["hero_id"] not in only):
                continue
            classes = [ab.class_name for ab in G.hero(p["hero_id"]).abilities]
            for k, v in p["damage_sources"].items():
                if k not in CATEGORY:
                    real[p["hero_id"]][real_key(k, classes)] += v
            jobs.append((m, p["slot"]))
    random.Random(1).shuffle(jobs)
    jobs = jobs[:max_players]
    sim = collections.defaultdict(collections.Counter)
    errs = collections.Counter()
    t0 = time.time()
    with ProcessPoolExecutor(workers) as ex:
        for i, (hid, d, n) in enumerate(ex.map(sim_player, jobs, chunksize=8)):
            for k, v in d.items():
                (errs if k.startswith("_") else sim[hid])[k] += v
            if i % 500 == 0 and not only:
                print(f"{i}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    print("errors:", errs.most_common(10))

    landing, shares = {}, {}
    for hid in sorted(sim):
        h = G.hero(hid)
        r, s = real[hid], sim[hid]
        rt, st = sum(r.values()), sum(s.values())
        shares[h.name] = {
            "real": {k: round(v / rt, 4) for k, v in r.most_common(12)},
            "sim": {k: round(v / st, 4) for k, v in s.most_common(12)},
        }
        rows = {}
        for ab in h.abilities:
            ra, sa = r.get(ab.class_name, 0), s.get(ab.class_name, 0)
            if sa <= 0 or r["GUN"] <= 0 or s["GUN"] <= 0:
                continue
            lr = (ra / r["GUN"]) / (sa / s["GUN"])
            rows[ab.name] = {"class": ab.class_name, "landing": round(lr, 3),
                             "real_share": round(ra / rt, 4), "sim_share": round(sa / st, 4)}
        landing[h.name] = rows
    if fit_melee:
        out = {}
        if only:  # refit some heroes, keep the rest
            try:
                out = json.load(open(MELEE_FILE))["heroes"]
            except (OSError, KeyError, ValueError):
                out = {}
        for hid in sorted(sim):
            r, s_ = real[hid], sim[hid]
            rate = MELEE.get(hid, MELEE_START)
            if r["GUN"] > 0 and s_["GUN"] > 0 and s_.get("MELEE", 0) > 0:
                new = rate * (r.get("MELEE", 0) / r["GUN"]) / (s_["MELEE"] / s_["GUN"])
                out[str(hid)] = {"name": G.hero(hid).name, "rate": round(min(1.0, new), 4),
                                 "real_melee_share": round(r.get("MELEE", 0) / sum(r.values()), 4)}
        json.dump({"meta": {"what": "landed basic melee hits per second of fight, fitted so sim melee/gun damage "
                                    "matches real damage matrix (scripts/landing_rates.py --fit-melee)"},
                   "heroes": out}, open(MELEE_FILE, "w"), indent=1)
        print("melee rates:", {v["name"]: v["rate"] for v in out.values()})
    if only:
        for hn in shares:
            print(f"\n{hn}  real vs sim share of hero damage (GUN = gun, MELEE = melee):")
            keys = list(dict.fromkeys(list(shares[hn]["real"]) + list(shares[hn]["sim"])))
            for k in keys:
                print(f"   {k:45s} real {shares[hn]['real'].get(k, 0):6.3f}   sim {shares[hn]['sim'].get(k, 0):6.3f}")
            for a, v in landing[hn].items():
                print(f"   landing {a:30s} {v['landing']:.2f}")
        return
    meta = {"source": f"{len(jobs)} player-matches x {len(FRACS)} duels, {FIGHT_TIME:.0f} s max, real builds both sides",
            "formula": "(real ability dmg / real gun dmg) / (sim ability dmg / sim gun dmg)"}
    # items: share of all hero damage, summed over every hero (needs per-item handlers in items_fx.py)
    rt_all = sum(sum(c.values()) for c in real.values() if c)
    st_all = sum(sum(c.values()) for c in sim.values())
    items = {}
    for k in set().union(*[set(c) for c in real.values()], *[set(c) for c in sim.values()]):
        if k.startswith("upgrade_"):
            r_ = sum(c.get(k, 0) for h, c in real.items() if h in sim) / rt_all
            s_ = sum(c.get(k, 0) for c in sim.values()) / st_all
            if r_ > 0.0005 or s_ > 0.0005:
                items[k] = {"name": G.items_by_class[k].name if k in G.items_by_class else k,
                            "real": round(r_, 5), "sim": round(s_, 5)}
    json.dump({"meta": meta, "items": dict(sorted(items.items(), key=lambda x: -x[1]["real"]))},
              open(os.path.join(ROOT, "validation", "item_shares.json"), "w"), indent=1)
    json.dump({"meta": meta, "heroes": landing}, open(os.path.join(ROOT, "data", "landing_rates.json"), "w"), indent=1)
    json.dump({"meta": meta, "heroes": shares}, open(os.path.join(ROOT, "validation", "damage_shares.json"), "w"), indent=1)
    for hn, rows in landing.items():
        print(hn + ": " + ", ".join(f"{a} {v['landing']:.2f}" for a, v in rows.items()))


if __name__ == "__main__":
    main()
