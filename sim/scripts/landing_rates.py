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

With --iterate the sim runs with the current landing factors applied and each factor is updated as
old x (real ratio / sim ratio). For abilities whose damage scales linearly with the factor this gives the same
result in one pass; for the rest (Bullet Dance, whose factor shortens the channel, and Fixation, whose stacks the
channel's bullets build) it converges over 2-3 runs.

usage: python3 scripts/landing_rates.py [max_players] [workers] [--fit-melee] [--iterate] [--sample PATH] [--hero NAME ...]
With --hero it runs only those heroes and prints real vs sim damage shares without writing any files.
--sample replaces validation/matches_sample.jsonl.gz (e.g. a Phantom+ sample from fetch_validation.py --api 91 5).
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
from deadsim.accuracy import HEADS, HITS, SHOTS, ability_landing, default_distance, gun_calibrated, gun_calibration  # noqa: E402
import deadsim.mechanics as MECH  # noqa: E402

CATEGORY = {"Bullet", "Ability", "Melee", "Misc"}   # per-damage-type totals in the matrix, not sources
SAMPLE = os.path.join(ROOT, "validation", "matches_sample.jsonl.gz")
# Sim damage labels that are not an ability name of the hero, mapped to the class the damage matrix books them under.
# Silver's Lycan Curse swaps her three basic abilities for wolf ones; each wolf ability gets its own landing factor
# under its sim label (the engine looks factors up by damage source name).
ALIASES = {
    "Go For The Throat": "ability_werewolf_frenzy",
    "Mauling Leap": "ability_werewolf_maulingleap",
    "Tail Whack": "ability_werewolf_cripplingslash",
    "Bloodletting (deferred)": "citadel_ability_shiv_defer_damage",   # an enemy Shiv's deferred damage
    "Wretched Vapors (crash)": "ability_nurse_adrenaline_rush",       # an enemy Nurse's specters (her own vapors)
}
SHIV_DEFER = "citadel_ability_shiv_defer_damage"
# damage the game books under the enemy's ability (deferred damage hitting its owner): not one of this hero's sources
ENEMY_BOOKED = {SHIV_DEFER, "ability_nurse_adrenaline_rush"}
COPY_ULT = "ability_magician_copyult"   # Sinclair: the copied ultimate is booked under the enemy hero's own class
MIN_HITS = 150       # API enemy-hero hits for a player's real aim to count (gun_known)
MIN_SHOTS = 300      # shots for the player's own accuracy (else the hero default)
# Slow guns land far fewer hero hits a match: Apollo (0.38 s cycle) has a median 300 shots / 69 hits per Phantom+
# match vs 1360 / 334 over all heroes, so MIN_HITS kept 6 of 111 Apollo players and his ability timing, landing and
# audit rested on them. Per hero (min hits, min shots), about MIN_HITS / MIN_SHOTS x the hero's median shots share
# (~0.25), floored for a usable accuracy (40 hits: +-15% relative, 150 shots). The same gap (validation/README.md):
# Violet (220 shots / 67 hits, 1% of players known at 150), The Doorman (301 / 99, 5%), Kelvin (508 / 98, 14%),
# Solomon (373 / 129, 31%); all but Kelvin then got cast timing rows and an audit refit. Rem (551 / 133, 37%), Paige
# (447 / 135, 42%) and Sinclair (685 / 141, 36%) sit just under the cutoff: (60, 200) keeps 57, 135, 55 players.
SLOW_GUNS = {77: (40, 150), 86: (40, 150), 69: (40, 150), 12: (55, 150), 85: (40, 150),
             79: (60, 200), 67: (60, 200), 60: (60, 200)}
FIGHT_TIME = 20.0
FRACS = (0.3, 0.6, 0.9)


def real_key(name, classes):
    """Normalize a damage-matrix source name: gun -> GUN, melee -> MELEE, ability sub-sources
    (e.g. citadel_ability_shiv_dagger_dot) -> their ability class."""
    if name.startswith("citadel_weapon") or "_primary_weapon" in name:
        return "GUN"
    if "ability_melee_" in name or name == "ability_baba_bench_melee":   # Baba's melee while on her bench
        return "MELEE"
    best = max((c for c in classes if name == c or name.startswith(c + "_")), key=len, default=None)
    if best is None and COPY_ULT in classes and name not in ENEMY_BOOKED and "ability_" in name:
        return COPY_ULT   # another hero's ability class in Sinclair's damage: the ultimate she copied
    return best or name


def sim_key(name, names, G):
    """Normalize a sim damage source: ability names (or labels starting with one) -> ability class."""
    if name == "gun":
        return "GUN"
    if name.lower() in G.items_by_name:   # before melee: "Melee Charge" is an item
        return G.items_by_name[name.lower()].class_name
    if name.lower().startswith("melee"):
        return "MELEE"
    if name in names:
        return names[name]
    if name in ALIASES:
        return ALIASES[name]
    best = max((n for n in names if name.startswith(n)), key=len, default=None)
    return names[best] if best else name


MELEE_FILE = os.path.join(ROOT, "data", "melee_rates.json")
try:
    MELEE = {int(k): v["rate"] for k, v in json.load(open(MELEE_FILE))["heroes"].items()}
except (OSError, ValueError, KeyError):
    MELEE = {}
MELEE_START = 0.1   # melee hits/s used for a hero not yet fitted
ITERATE = False     # --iterate: fight with the current landing factors and update them multiplicatively
_landing = {}


def current_landing(hero_id):
    """The landing factors fights use now (mechanics on or off, as deadsim.mechanics.DEFAULT says)."""
    mech = MECH.DEFAULT is not None
    if (hero_id, mech) not in _landing:
        _landing[hero_id, mech] = ability_landing(game().hero(hero_id).name, mech=mech)
    return _landing[hero_id, mech]


def gun_limits(hero_id):
    """(min API hero hits, min shots) for a player's real gun data (SLOW_GUNS: fewer for a slow gun)."""
    return SLOW_GUNS.get(hero_id, (MIN_HITS, MIN_SHOTS))


def gun_known(p):
    """Enough real gun data to fit against: API hero hits, or a hero whose gun records none but has a replay-fitted
    accuracy (Graves, Deadman Danny: data/gun_calibration.json)."""
    return p["custom"].get(HITS, 0) >= gun_limits(p["hero_id"])[0] or gun_calibrated(p["hero_id"])


def own_aim(p):
    """Enough shots for the player's own accuracy and headshot rate."""
    return p["custom"].get(SHOTS, 0) >= gun_limits(p["hero_id"])[1]


def skill_of(p):
    c = p["custom"]
    shots, hits = c.get(SHOTS, 0), c.get(HITS, 0)
    rate = MELEE.get(p["hero_id"], MELEE_START)
    cal = gun_calibration().get(str(p["hero_id"])) if gun_calibrated(p["hero_id"]) else None
    if cal:   # the match stats' shots/hits for this gun are missing or partial
        sk = Skill(accuracy=cal["accuracy"]["p50"], headshot=cal["headshot"]["p50"], melee_rate=rate)
    elif not own_aim(p):
        sk = Skill(melee_rate=rate)
    else:
        sk = Skill(accuracy=hits / shots, headshot=c.get(HEADS, 0) / max(1, hits), melee_rate=rate)
    if ITERATE:
        sk.ability_landing = sk.ability_landing_mech = dict(current_landing(p["hero_id"]))
    return sk


def build_at(p, t):
    G = game()
    items = [i for i, bt, st, _ in p["items"] if i in G.items and bt <= t and (st == 0 or st > t) and G.items[i].cost > 0]
    snaps = [s for s in p["stats"] if s["time_stamp_s"] <= t] or p["stats"][:1]
    return items, snaps[-1]["net_worth"]


def real_gun_series(m, p):
    """Cumulative real gun damage to enemy heroes as a function of match time (piecewise linear between the damage
    matrix samples, 0 at 0 s), or None for a sample without damage_series."""
    times, ser = m.get("damage_times"), p.get("damage_series")
    if not times or not ser:
        return None
    classes = [ab.class_name for ab in game().hero(p["hero_id"]).abilities]
    cum = [0.0] * len(times)
    for k, arr in ser.items():
        if k not in CATEGORY and real_key(k, classes) == "GUN":
            cum = [a + b for a, b in zip(cum, arr)]
    xs, ys = [0.0] + list(times), [0.0] + cum

    def at(t):
        if t >= xs[-1]:
            return ys[-1]
        for i in range(1, len(xs)):
            if t <= xs[i]:
                f = (t - xs[i - 1]) / max(1e-9, xs[i] - xs[i - 1])
                return ys[i - 1] + f * (ys[i] - ys[i - 1])
        return ys[-1]
    return at


def held_gun(m, p):
    """{item class: real gun damage to enemy heroes while the player owned the item}: the fair denominator for an
    item's damage per gun damage (match-total gun damage dilutes items bought late). None without damage_series."""
    gun = real_gun_series(m, p)
    if gun is None:
        return None
    G = game()
    out = collections.Counter()
    for i, bt, st, _ in p["items"]:
        if i in G.items:
            end = st if st and st > bt else m["duration_s"]
            out[G.items[i].class_name] += max(0.0, gun(end) - gun(bt))
    return out


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
    held = collections.defaultdict(lambda: [0.0, 0.0])   # item class -> [item dmg, gun dmg] of the duels holding it
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
        d = collections.Counter()
        for k, v in r.a_dmg.items():
            d[sim_key(k, names, G)] += v
        out.update(d)
        for i in items:
            c = G.items[i].class_name
            held[c][0] += d.get(c, 0.0)
            held[c][1] += d.get("GUN", 0.0)
    return me["hero_id"], dict(out), fights, dict(held)


def main():
    args = sys.argv[1:]
    global ITERATE, SAMPLE
    if "--sample" in args:
        i = args.index("--sample")
        SAMPLE = args[i + 1]
        args = args[:i] + args[i + 2:]
    fit_melee = "--fit-melee" in args
    ITERATE = "--iterate" in args
    args = [a for a in args if a not in ("--fit-melee", "--iterate")]
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
    for line in gzip.open(SAMPLE):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] not in G.heroes or not gun_known(p) or (only and p["hero_id"] not in only):
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
        for i, (hid, d, n, _) in enumerate(ex.map(sim_player, jobs, chunksize=8)):
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
        srcs = [(ab.name, ab.class_name) for ab in h.abilities]
        srcs += [(lab, cls) for lab, cls in ALIASES.items() if cls not in {c for _, c in srcs} and s.get(cls, 0) > 0
                 and cls not in ENEMY_BOOKED]
        for ab_name, ab_class in srcs:
            ra, sa = r.get(ab_class, 0), s.get(ab_class, 0)
            if sa <= 0 or r["GUN"] <= 0 or s["GUN"] <= 0:
                continue
            lr = (ra / r["GUN"]) / (sa / s["GUN"])
            if ITERATE:
                lr *= current_landing(hid).get(ab_name, 1.0)
            rows[ab_name] = {"class": ab_class, "landing": round(lr, 3),
                             "real_share": round(ra / rt, 4), "sim_share": round(sa / st, 4)}
        landing[h.name] = rows
    if fit_melee:
        out = {}
        if only:  # refit some heroes, keep the rest
            try:
                out = json.load(open(MELEE_FILE))["heroes"]
            except (OSError, KeyError, ValueError):
                out = {}
        try:   # rows refit to the damage audit (scripts/melee_audit_fit.py) stay: this model is not the audit's
            kept = {k: v for k, v in json.load(open(MELEE_FILE))["heroes"].items() if v.get("audit_fit")}
        except (OSError, KeyError, ValueError):
            kept = {}
        for hid in sorted(sim):
            if str(hid) in kept:
                out[str(hid)] = kept[str(hid)]
                continue
            r, s_ = real[hid], sim[hid]
            rate = MELEE.get(hid, MELEE_START)
            if r["GUN"] > 0 and s_["GUN"] > 0 and s_.get("MELEE", 0) > 0:
                new = rate * (r.get("MELEE", 0) / r["GUN"]) / (s_["MELEE"] / s_["GUN"])
                out[str(hid)] = {"name": G.hero(hid).name, "rate": round(min(1.0, new), 4),
                                 "real_melee_share": round(r.get("MELEE", 0) / sum(r.values()), 4)}
        try:
            meta = json.load(open(MELEE_FILE))["meta"]   # keeps the audit_fit note
        except (OSError, KeyError, ValueError):
            meta = {}
        meta["what"] = ("landed basic melee hits per second of fight, fitted so sim melee/gun damage matches real "
                        "damage matrix (scripts/landing_rates.py --fit-melee)")
        json.dump({"meta": meta, "heroes": out}, open(MELEE_FILE, "w"), indent=1)
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
