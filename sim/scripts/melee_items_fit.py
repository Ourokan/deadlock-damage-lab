"""How much more players melee when they build melee items, fitted from real damage.

data/melee_rates.json holds each hero's average landed melee rate over all players. Players who buy melee items
(Melee Charge, Lifestrike, Spirit Snatch ...) melee more than that average and players who buy none melee less, so
a single rate per hero undervalues melee items in build search. This script measures the difference.

For each player-match in validation/matches_sample.jsonl.gz, duel the player's real build at 30/60/90% of the match
(like scripts/landing_rates.py) with the hero's average melee rate, then compare the player's real melee/gun damage
ratio with the sim's. The sim already gives melee items their per-hit damage (Melee Charge bonus, melee damage %),
so real/sim left over is the change in how often the player lands melees. Players are grouped by how many melee
items they held, averaged over the three sample points; the multiplier for each group is

    mult(n) = (sum real melee / sum real gun) / (sum sim melee / sum sim gun)   over that group,

normalized by the same ratio over all of the hero's players, then pooled over heroes (weighted by sim melee).

Output: data/melee_items.json (used by accuracy.hero_default_skill / melee_rate(hero, items)).

With --check the duels use the fitted build rates (melee_rates_by_items) instead and nothing is written: every
group's real/sim ratio should then come out near 1.

usage: python3 scripts/melee_items_fit.py [max_players] [workers] [--check]
"""
import collections
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
from deadsim import Loadout, Skill, duel, game  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
from deadsim.accuracy import HEADS, HITS, SHOTS, default_distance, melee_rate, melee_rates_by_items  # noqa: E402
from deadsim.engine import MELEE_ITEMS  # noqa: E402

MIN_HITS = 150
FIGHT_TIME = 20.0
FRACS = (0.3, 0.6, 0.9)
GROUPS = ("0", "1", "2+")
CHECK = "--check" in sys.argv
# heroes whose average melee is a real part of their damage; they are fitted separately from gun heroes
MELEE_HERO_RATE = 0.08


def build_at(G, p, t):
    items = [i for i, bt, st, _ in p["items"] if i in G.items and bt <= t and (st == 0 or st > t) and G.items[i].cost > 0]
    snaps = [s for s in p["stats"] if s["time_stamp_s"] <= t] or p["stats"][:1]
    return items, snaps[-1]["net_worth"]


def skill_of(p, rate):
    c = p["custom"]
    shots, hits = c.get(SHOTS, 0), c.get(HITS, 0)
    if shots < 300:
        return Skill(melee_rate=rate)
    return Skill(accuracy=hits / shots, headshot=c.get(HEADS, 0) / max(1, hits), melee_rate=rate)


def n_melee(G, items):
    return sum(1 for i in items if G.items[i].class_name in MELEE_ITEMS)


def sim_player(job):
    m, slot = job
    G = game()
    load_heroes()
    me = next(p for p in m["players"] if p["slot"] == slot)
    foes = [p for p in m["players"] if p["team"] != me["team"] and p["hero_id"] in G.heroes]
    h = G.hero(me["hero_id"])
    rnd = random.Random(m["match_id"] * 31 + slot)
    gun = mel = 0.0
    held = []
    for frac in FRACS:
        t = m["duration_s"] * frac
        items, souls = build_at(G, me, t)
        held.append(n_melee(G, items))
        foe = rnd.choice(foes)
        fitems, fsouls = build_at(G, foe, t)
        rate = melee_rate(h.name)
        if CHECK:
            by = melee_rates_by_items(h.name) or (rate,)
            rate = by[min(held[-1], len(by) - 1)]
        a = Loadout(h.name, items, souls=souls, skill=skill_of(me, rate))
        b = Loadout(foe["hero_id"], fitems, souls=fsouls, skill=skill_of(foe, melee_rate(foe["hero_id"])))
        try:
            r = duel(a, b, distance=default_distance(h.name), max_time=FIGHT_TIME)
        except Exception:  # noqa: BLE001 - a broken hero file shouldn't kill the run
            continue
        for k, v in r.a_dmg.items():
            if k == "gun":
                gun += v
            elif k.lower().startswith("melee") and k.lower() not in G.items_by_name:
                mel += v    # basic and ability melees; item bonuses (Melee Charge) are booked under the item, as in game
    real_gun = sum(v for k, v in me["damage_sources"].items() if k.startswith("citadel_weapon") or "_primary_weapon" in k)
    real_mel = sum(v for k, v in me["damage_sources"].items() if "ability_melee_" in k)
    return me["hero_id"], sum(held) / len(held), gun, mel, real_gun, real_mel


def group(n):
    return "0" if n < 0.5 else "1" if n < 1.5 else "2+"


def main():
    args = [a for a in sys.argv[1:] if a != "--check"]
    max_players = int(args[0]) if args else 10 ** 9
    workers = int(args[1]) if len(args) > 1 else os.cpu_count()
    G = game()
    load_heroes()
    jobs = []
    for line in gzip.open(os.path.join(ROOT, "validation", "matches_sample.jsonl.gz")):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] in G.heroes and p["custom"].get(HITS, 0) >= MIN_HITS:
                jobs.append((m, p["slot"]))
    random.Random(1).shuffle(jobs)
    jobs = jobs[:max_players]
    rows = []
    t0 = time.time()
    with ProcessPoolExecutor(workers) as ex:
        for i, r in enumerate(ex.map(sim_player, jobs, chunksize=8)):
            rows.append(r)
            if i % 500 == 0:
                print(f"{i}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    by_hero = collections.defaultdict(list)
    for r in rows:
        if r[2] > 0 and r[4] > 0:
            by_hero[r[0]].append(r)

    def ratio(rs):
        sg, sm = sum(r[2] for r in rs), sum(r[3] for r in rs)
        rg, rm = sum(r[4] for r in rs), sum(r[5] for r in rs)
        return (rm / rg) / (sm / sg) if sg and sm and rg else None

    out, heroes = pool(by_hero, ratio, G)
    if CHECK:   # real/sim by group with the build rates, relative to the hero's overall real/sim
        for cls in ("melee", "gun"):
            print(cls, {g: round(math.exp(sum(math.log(heroes[h][g]["mult_vs_hero_avg"]) * heroes[h][g]["players"]
                                              for h in heroes if heroes[h]["class"] == cls and g in heroes[h]) /
                                          max(1, sum(heroes[h][g]["players"] for h in heroes
                                                     if heroes[h]["class"] == cls and g in heroes[h]))), 3)
                        for g in GROUPS})
        return
    # 90% interval from resampling players within each hero
    rnd = random.Random(5)
    boots = [pool({h: [rnd.choice(rs) for _ in rs] for h, rs in by_hero.items()}, ratio, G)[0] for _ in range(200)]
    for cls in out:
        for g in GROUPS:
            xs = sorted(b[cls][g]["mult"] for b in boots)
            out[cls][g]["ci90"] = [xs[10], xs[189]]
    print(json.dumps(out, indent=1))
    json.dump({"meta": {"what": "melee rate multiplier by melee items held (vs players with none), fitted "
                                "from real melee/gun damage vs sim on real builds (scripts/melee_items_fit.py)",
                        "melee_items": sorted(MELEE_ITEMS), "melee_hero_rate": MELEE_HERO_RATE,
                        "source": f"{len(rows)} player-matches x {len(FRACS)} duels"},
               "classes": out, "heroes": heroes},
              open(os.path.join(ROOT, "data", "melee_items.json"), "w"), indent=1)


def pool(by_hero, ratio, G):
    """Per class (melee heroes / gun heroes), fit log(group ratio / hero ratio) = a_hero + b_group (b_0 = 0),
    weighted by each group's sim melee damage, so heroes everyone builds the same way don't dilute the effect.
    Returns mult(group) = exp(b_group) relative to players with no melee items, and each hero's group mix."""
    cells = {c: [] for c in ("melee", "gun")}   # (hero, group, log ratio, weight)
    heroes = {}
    for hid, rs in by_hero.items():
        base = ratio(rs)
        if not base:
            continue
        cls = "melee" if melee_rate(hid) >= MELEE_HERO_RATE else "gun"
        hrow = {"name": G.hero(hid).name, "class": cls, "players": len(rs),
                "mix": {g: round(sum(1 for r in rs if group(r[1]) == g) / len(rs), 3) for g in GROUPS}}
        for g in GROUPS:
            gr = [r for r in rs if group(r[1]) == g]
            x = ratio(gr) if len(gr) >= 3 else None
            if x:
                cells[cls].append((hid, g, math.log(x / base), sum(r[3] for r in gr)))
                hrow[g] = {"players": len(gr), "mult_vs_hero_avg": round(x / base, 3)}
        heroes[str(hid)] = hrow
    out = {}
    for cls, cs in cells.items():
        b = {g: 0.0 for g in GROUPS}
        a = {}
        for _ in range(50):   # alternating weighted least squares
            for h in {c[0] for c in cs}:
                hc = [c for c in cs if c[0] == h]
                a[h] = sum(w * (y - b[g]) for _, g, y, w in hc) / sum(w for *_, w in hc)
            for g in GROUPS[1:]:
                gc = [c for c in cs if c[1] == g]
                if gc:
                    b[g] = sum(w * (y - a[h]) for h, _, y, w in gc) / sum(w for *_, w in gc)
        n = {g: sum(heroes[str(h)][g]["players"] for h, gg, *_ in cs if gg == g) for g in GROUPS}  # in fitted cells
        out[cls] = {g: {"mult": round(math.exp(b[g]), 3), "players": n[g]} for g in GROUPS}
    return out, heroes


if __name__ == "__main__":
    main()
