"""Counter-item buying analysis over the current-patch ranked builds (data/builds/player_builds).

Teams come from the `won` flag (6 winners vs 6 losers per match). For every player, the enemy team's items held at
any moment are rebuilt from `purchases` ([item, buy_s, sold_s], sold_s 0 = kept).

Outputs counters/out/raw_counts.json (aggregated counts); report.py turns them into tables.

    python3 scripts/analyze.py [--workers 3]
"""
from __future__ import annotations

import argparse
import glob
import gzip
import json
import os
import sys
from collections import defaultdict
from multiprocessing import Pool

ROOT = "/mnt/project-files"
ITEMS = {x["id"]: x for x in json.load(open(f"{ROOT}/data/game/shop_items.json"))}
BY_NAME = {x["name"]: x["id"] for x in ITEMS.values()}

COUNTERS = ["Dispel Magic", "Counterspell", "Metal Skin", "Return Fire", "Plated Armor",
            # comparison defensive items
            "Debuff Reducer", "Bullet Resilience", "Spirit Resilience", "Unstoppable", "Spellbreaker",
            "Witchmail", "Reactive Barrier", "Indomitable", "Divine Barrier"]
COUNTER_IDS = {BY_NAME[n]: n for n in COUNTERS}

# Enemy items a cleanse or debuff resistance answers (DoTs, slows, silences, disarms, stuns, roots, curses).
DEBUFF_ITEMS = {BY_NAME[n] for n in [
    "Toxic Bullets", "Decay", "Slowing Hex", "Disarming Hex", "Silence Wave", "Knockdown", "Cursed Relic",
    "Mystic Slow", "Silencer", "Inhibitor", "Arctic Blast", "Vortex Web", "Cold Front", "Scourge",
    "Alchemical Fire", "Spirit Sap", "Slowing Bullets", "Crippling Headshot", "Rusted Barrel", "Healbane",
    "Frostbite Charm", "Shrink Ray"]}
# On-hit bullet procs Plated Armor deflects at 50% (BulletProcDeflectionPercent).
PROC_ITEMS = {BY_NAME[n] for n in [
    "Toxic Bullets", "Tesla Bullets", "Mystic Shot", "Silencer", "Inhibitor", "Siphon Bullets", "Slowing Bullets",
    "Spirit Shredder", "Escalating Exposure", "Spiritual Overflow", "Crippling Headshot", "Headhunter",
    "Ballistic Enchantment", "Weakening Headshot", "Spirit Rend", "Bullet Resist Shredder", "Haunting Shot"]}

SLOT = {i: x["slot"] for i, x in ITEMS.items()}
COST = {i: x["cost"] for i, x in ITEMS.items()}
TIER = {i: x["tier"] for i, x in ITEMS.items()}
VIT_T = {t: {i for i, x in ITEMS.items() if x["slot"] == "vitality" and x["tier"] == t} for t in (2, 3, 4)}
BIN = 300  # 5-minute purchase-time bins


def bracket(badge):
    t = badge // 10
    return "1-3 Initiate-Seeker" if t <= 3 else "4-6 Alchemist-Arcanist" if t <= 6 else "7-9 Ritualist-Phantom" \
        if t <= 9 else "10-11 Ascendant-Eternus"


def team_state(team_rows, t):
    """A team at time t: weapon share, spirit share, debuff-item count, proc-item count, total item souls held."""
    w = s = v = 0
    deb = proc = 0
    for r in team_rows:
        for it, b, sold in r["purchases"]:
            if b <= t and (sold == 0 or sold > t) and it in SLOT:
                c = COST[it]
                sl = SLOT[it]
                if sl == "weapon":
                    w += c
                elif sl == "spirit":
                    s += c
                else:
                    v += c
                if it in DEBUFF_ITEMS:
                    deb += 1
                if it in PROC_ITEMS:
                    proc += 1
    tot = w + s + v
    return (w / tot if tot else 0.0, s / tot if tot else 0.0, deb, proc, tot)


def q(x, step=0.05):
    return round(int(x / step) * step, 2)


def process(path):
    # The SQL pull returns most players twice (identical rows), so keep one row per (match, account).
    matches = defaultdict(dict)
    with gzip.open(path, "rt") as fh:
        for line in fh:
            r = json.loads(line)
            matches[r["match_id"]][r["account_id"]] = r
    matches = {m: list(v.values()) for m, v in matches.items()}
    # aggregates
    totals = defaultdict(lambda: [0, 0])          # (hero, bracket) -> [players, wins]
    bought = defaultdict(lambda: [0, 0, 0])       # (item, hero, bracket) -> [buyers, wins, sold]
    buy_times = defaultdict(lambda: defaultdict(int))   # item -> minute -> n
    vs_hero = defaultdict(lambda: [0, 0])         # (item, enemy_hero) -> [players facing, buyers]
    vs_hero_tot = defaultdict(int)
    # choice-set events: tier-T vitality item purchases. key -> [n, wins]
    events = defaultdict(lambda: [0, 0])          # (item, own_hero, bin, wsh, ssh, deb, proc, lead)
    events2 = defaultdict(lambda: [0, 0])         # (item, own_hero, bin, lead, own-vs-team bucket)
    # hazard: at checkpoints, players not yet owning item -> did they buy it in the next 10 min, by enemy threat
    hazard = defaultdict(lambda: [0, 0])          # (item, checkpoint, wsh, ssh, deb, proc) -> [at risk, bought]
    n_match = 0
    for mid, rows in matches.items():
        if len(rows) != 12 or sum(r["won"] for r in rows) != 6:
            continue
        n_match += 1
        teams = {True: [r for r in rows if r["won"]], False: [r for r in rows if not r["won"]]}
        cache = {}

        def enemy(won, t):
            k = (won, t)
            if k not in cache:
                cache[k] = team_state(teams[not won], t)
            return cache[k]

        for r in rows:
            br = bracket(r["badge"])
            hero = r["hero_id"]
            won = r["won"]
            totals[(hero, br)][0] += 1
            totals[(hero, br)][1] += won
            first = {}
            for it, b, sold in r["purchases"]:
                if it not in first:
                    first[it] = (b, sold)
            enemies = [e["hero_id"] for e in teams[not won]]
            for e in enemies:
                vs_hero_tot[e] += 1
            for it, name in COUNTER_IDS.items():
                if it in first:
                    b, sold = first[it]
                    x = bought[(it, hero, br)]
                    x[0] += 1
                    x[1] += won
                    x[2] += 1 if sold else 0
                    buy_times[it][b // 60] += 1
                for e in enemies:
                    vs_hero[(it, e)][0] += 1
                    if it in first:
                        vs_hero[(it, e)][1] += 1
            # choice-set events (first purchase of each T2-T4 vitality item)
            for it, (b, sold) in first.items():
                if TIER.get(it) in (2, 3, 4) and SLOT.get(it) == "vitality":
                    tb = (b // BIN) * BIN
                    w, s, deb, proc, etot = enemy(won, tb)
                    # team item-souls lead at the purchase, in 2500-soul buckets clipped to +-6
                    lead = max(-6, min(6, round((enemy(not won, tb)[4] - etot) / 2500)))
                    e = events[(it, hero, tb, q(w, 0.1), q(s, 0.1), min(deb, 6), min(proc, 6), lead)]
                    e[0] += 1
                    e[1] += won
                    # same event with the player's own position: held item souls vs own team's average
                    own = sum(COST[i] for i, bb, ss in r["purchases"] if bb <= tb and (ss == 0 or ss > tb) and i in COST)
                    rel = max(-4, min(4, round((own - enemy(not won, tb)[4] / 6) / 1500)))
                    e2 = events2[(it, hero, tb, lead, rel)]
                    e2[0] += 1
                    e2[1] += won
            # hazard
            for cp in (600, 900, 1200, 1500, 1800, 2100):
                if r["duration_s"] < cp + 600:
                    break
                w, s, deb, proc, _ = enemy(won, cp)
                for it in COUNTER_IDS:
                    if it in first and first[it][0] <= cp:
                        continue
                    h = hazard[(it, cp, q(w, 0.1), q(s, 0.1), min(deb, 6), min(proc, 6))]
                    h[0] += 1
                    if it in first and first[it][0] <= cp + 600:
                        h[1] += 1
    def ser(d):
        return [[list(k) if isinstance(k, tuple) else k, v] for k, v in d.items()]
    return {
        "file": os.path.basename(path), "matches": n_match,
        "totals": ser(totals), "bought": ser(bought),
        "buy_times": [[k, dict(v)] for k, v in buy_times.items()],
        "vs_hero": ser(vs_hero), "vs_hero_tot": ser(vs_hero_tot),
        "events": ser(events), "events2": ser(events2), "hazard": ser(hazard),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    files = sorted(glob.glob(f"{ROOT}/data/builds/player_builds/*.jsonl.gz"))
    if a.limit:
        files = files[:a.limit]
    os.makedirs(f"{ROOT}/counters/work", exist_ok=True)
    todo = [f for f in files if not os.path.exists(f"{ROOT}/counters/work/{os.path.basename(f)}.json")]
    with Pool(a.workers) as p:
        for res in p.imap_unordered(process, todo):
            json.dump(res, open(f"{ROOT}/counters/work/{res['file']}.json", "w"))
            print(res["file"], res["matches"], file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
