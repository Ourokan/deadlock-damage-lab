"""Melee hit sizes and on-hit procs from Phantom+ replays: engine.MELEE_WEAPON_SCALE, AbilityImpl.spirit_procs,
items_fx._any_melee.

Input: the fight-length replays (every hero-vs-hero DamageEvent with the ability id, fight_length/fetch_fights.py)
and the validation sample (each player's items and net worth over time, real weapon power in the stat snapshots).

1. Size: each melee hit (basic melee of every hero, and Bebop's Exploding Uppercut) over the sim's formula (light
   melee base + boon growth) x (1 + melee damage bonus) x (1 - the victim's melee resist), by the attacker's real
   weapon power. The light-melee hits are the lowest fifth (heavies are ~1.8x); with no weapon scaling the ratio
   climbs with weapon power, and k in (1 + k x weapon power) flattens it.
2. Procs: share of Bebop's Uppercut / Grapple Arm / basic melee hits by item holders (after the match's first proc)
   with the item's damage on the same victim in the same tick, counting only ticks with no other ability or item
   damage on that victim (so a Sticky Bomb or Spirit Snatch hit can't be the trigger).

usage: python3 -I melee_scaling.py [n_matches=260]
"""
import collections
import gzip
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(HERE, ".."))
from deadsim import game  # noqa: E402
from deadsim.build import combine_resist, compute_stats  # noqa: E402
import landing_rates as L  # noqa: E402

RAW = "/mnt/project-files/analysis/work/fight_length/raw/"
SAMPLE = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
UPPERCUT, HOOK = "citadel_ability_uppercut", "citadel_ability_hook"
PROC_ITEMS = ("upgrade_magic_shock", "upgrade_magic_burst", "upgrade_spirit_snatch", "upgrade_acolytes_glove")
WP_BINS = ((0, 0.1), (0.1, 0.3), (0.3, 0.6), (0.6, 1.0), (1.0, 9))


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 260
    G = game()
    raw = json.load(open(os.path.join(ROOT, "..", "data", "game", "raw", "items.json")))
    name = {str(x.get("id")): x.get("class_name") or "" for x in raw}
    sample = {}
    for line in gzip.open(SAMPLE):
        m = json.loads(line)
        sample[str(m["match_id"])] = m
    cache = {}

    def stats(p, t):
        k = (id(p), int(t // 60))
        if k not in cache:
            items, souls = L.build_at(p, t)
            cache[k] = compute_stats(G.hero(p["hero_id"]), items, souls=souls)
        return cache[k]

    size = collections.defaultdict(list)          # "melee" / "uppercut" -> [(ratio, real weapon power)]
    procs = collections.defaultdict(lambda: [0, 0])   # (item, source) -> [procs, hits]
    for f in sorted(os.listdir(RAW))[:n]:
        mid = f.split(".")[0]
        if mid not in sample:
            continue
        ev = [json.loads(x) for x in gzip.open(RAW + f)]
        ev = [r for r in ev if r["k"] == "ctl" or "s" in r]
        hero = {r["a"]: r["s"] for r in ev if r["k"] == "ctl"}
        t0 = min(r["tick"] for r in ev)
        players = {str(p["hero_id"]): p for p in sample[mid]["players"]}
        dmg = [(r["tick"], *divmod(r["a"], 100000), name.get(r["s"].split("|")[0], ""), r["v"]) for r in ev if r["k"] == "dmg"]
        tick = collections.defaultdict(set)
        first = {}
        for t, a, v, src, _ in dmg:
            tick[(t, a, v)].add(src)
            first.setdefault((a, src), t)
        for t, a, v, src, d in dmg:
            pa, pv = players.get(hero.get(a)), players.get(hero.get(v))
            if not pa or not pv or pa["hero_id"] not in G.heroes or pv["hero_id"] not in G.heroes:
                continue
            basic = src.startswith("citadel_ability_melee")
            if basic or src == UPPERCUT:
                ts = (t - t0) / 64
                sa, sv = stats(pa, ts), stats(pv, ts)
                h = sa.hero
                light = h.base.get("light_melee_damage", 0.0) + sa.boons * h.per_boon.get(
                    "MODIFIER_VALUE_BASE_MELEE_DAMAGE_FROM_LEVEL", 0.0)
                pred = light * (1 + sa.melee_pct) * (1 - combine_resist(sv.melee_resist))
                snap = [x for x in pa["stats"] if x["time_stamp_s"] <= ts] or pa["stats"][:1]
                size["melee" if basic else "uppercut"].append((d / pred, snap[-1]["weapon_power"] / 100))
            if pa["hero_id"] == 15 and (basic or src in (UPPERCUT, HOOK)):
                same = tick[(t, a, v)] - {src}
                for it in PROC_ITEMS:
                    if (a, it) in first and t >= first[(a, it)] and not (same - {it}):
                        c = procs[(it, "basic melee" if basic else src)]
                        c[0] += it in same
                        c[1] += 1
    for kind, rows in size.items():
        print(f"\n{kind}: real hit / sim formula without weapon scaling, by attacker weapon power "
              f"({'lowest fifth = light melee' if kind == 'melee' else 'median'})")
        for k in (0.0, 0.5, 1.0):
            out = []
            for lo, hi in WP_BINS:
                r = sorted(x / (1 + k * w) for x, w in rows if lo <= w < hi)
                if len(r) >= 20:
                    out.append(f"{lo:.1f}-{hi:.1f}: {r[len(r) // 5] if kind == 'melee' else statistics.median(r):.2f}")
            print(f"  k={k}: " + "  ".join(out))
    print("\nBebop hits alone on their tick that release the item (holders, after its first proc)")
    for (it, src), (k, m) in sorted(procs.items()):
        print(f"  {it:24s} {src:26s} {k:4d}/{m:5d} = {k / max(1, m):.2f}")


if __name__ == "__main__":
    main()
