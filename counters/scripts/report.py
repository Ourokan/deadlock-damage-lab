"""Turn counters/work/*.json (analyze.py) into out/report.json + out/tables.md (real-match tables only; the sim values
are counters/out/sim.json and sim.md from sim_counters.py + export_sim.py)."""
from __future__ import annotations

import glob
import json
import math
from collections import defaultdict

ROOT = "/mnt/project-files"
ITEMS = {x["id"]: x for x in json.load(open(f"{ROOT}/data/game/shop_items.json"))}
HEROES = {h["id"]: h["name"] for h in json.load(open(f"{ROOT}/data/game/heroes.json"))}
NAME = {i: x["name"] for i, x in ITEMS.items()}
ID = {v: k for k, v in NAME.items()}
MAIN = ["Dispel Magic", "Counterspell", "Metal Skin", "Return Fire", "Plated Armor"]
EXTRA = ["Debuff Reducer", "Bullet Resilience", "Spirit Resilience", "Unstoppable", "Spellbreaker", "Witchmail",
         "Reactive Barrier", "Indomitable", "Divine Barrier"]
# Which enemy-team measure each counter answers. Event/hazard key fields: wsh=enemy weapon-souls share,
# ssh=spirit share, deb=enemy debuff items held, proc=enemy bullet-proc items held.
THREAT = {"Dispel Magic": "deb", "Counterspell": "ssh", "Metal Skin": "wsh", "Return Fire": "wsh",
          "Plated Armor": "proc", "Debuff Reducer": "deb", "Bullet Resilience": "wsh", "Spirit Resilience": "ssh",
          "Unstoppable": "deb", "Spellbreaker": "ssh", "Witchmail": "ssh", "Reactive Barrier": "deb",
          "Indomitable": "deb", "Divine Barrier": "wsh"}
THREAT_LABEL = {"wsh": "enemy team's share of item souls in weapon items",
                "ssh": "enemy team's share of item souls in spirit items",
                "deb": "debuff items the enemy team holds (Toxic Bullets, Decay, Slowing Hex, Silence Wave, ...)",
                "proc": "bullet-proc items the enemy team holds (Toxic Bullets, Tesla Bullets, Mystic Shot, ...)"}
FIELD = {"wsh": 0, "ssh": 1, "deb": 2, "proc": 3}


def load():
    agg = {k: defaultdict(lambda: [0, 0, 0]) for k in ("totals", "bought", "vs_hero", "vs_hero_tot", "events", "events2", "hazard")}
    buy_times = defaultdict(lambda: defaultdict(int))
    matches = 0
    for f in sorted(glob.glob(f"{ROOT}/counters/work/*.json")):
        d = json.load(open(f))
        matches += d["matches"]
        for k in agg:
            for key, v in d[k]:
                key = tuple(key) if isinstance(key, list) else key
                v = v if isinstance(v, list) else [v]
                acc = agg[k][key]
                for i, x in enumerate(v):
                    acc[i] += x
        for it, m in d["buy_times"]:
            for minute, n in m.items():
                buy_times[it][int(minute)] += n
    return matches, agg, buy_times


def wq(pairs, p):
    """Weighted quantile of [(value, weight)]."""
    pairs = sorted(pairs)
    tot = sum(w for _, w in pairs)
    acc = 0
    for v, w in pairs:
        acc += w
        if acc >= p * tot:
            return v
    return pairs[-1][0]


def tercile_fn(pairs):
    lo, hi = wq(pairs, 1 / 3), wq(pairs, 2 / 3)
    if lo == hi:  # heavy ties: split at the tied value
        return lambda v: "low" if v < lo else ("high" if v > hi else "mid")
    return lambda v: "low" if v <= lo else ("high" if v > hi else "mid")


def main():
    matches, agg, buy_times = load()
    rep = {"matches": matches, "players": 0, "items": {}}
    tot_players = sum(v[0] for v in agg["totals"].values())
    tot_wins = sum(v[1] for v in agg["totals"].values())
    rep["players"] = tot_players
    hero_n = defaultdict(int)
    br_n = defaultdict(int)
    for (h, br), v in agg["totals"].items():
        hero_n[h] += v[0]
        br_n[br] += v[0]
    for name in MAIN + EXTRA:
        it = ID[name]
        tier = ITEMS[it]["tier"]
        r = {"id": it, "tier": tier, "cost": ITEMS[it]["cost"], "threat": THREAT[name]}
        # overview
        b = [v for (i, h, br), v in agg["bought"].items() if i == it]
        n_b = sum(v[0] for v in b)
        r["buy_rate"] = n_b / tot_players
        r["buyer_win_rate"] = sum(v[1] for v in b) / max(1, n_b)
        r["sold_rate"] = sum(v[2] for v in b) / max(1, n_b)
        bt = buy_times[it]
        r["buy_minute"] = {p: wq(list(bt.items()), q) for p, q in (("p25", .25), ("median", .5), ("p75", .75))} if bt else {}
        by_br = defaultdict(int)
        by_hero = defaultdict(int)
        for (i, h, br), v in agg["bought"].items():
            if i == it:
                by_br[br] += v[0]
                by_hero[h] += v[0]
        r["buy_rate_by_rank"] = {br: by_br[br] / br_n[br] for br in sorted(br_n, key=lambda b: int(b.split("-")[0]))}
        r["top_buyers"] = sorted(([HEROES.get(h, h), by_hero[h] / hero_n[h], hero_n[h]] for h in by_hero
                                  if hero_n[h] >= 2000), key=lambda x: -x[1])[:8]
        # enemy hero lift
        lift = []
        for (i, e), v in agg["vs_hero"].items():
            if i == it and v[0] >= 2000:
                lift.append([HEROES.get(e, e), v[1] / v[0] / r["buy_rate"], v[0]])
        lift.sort(key=lambda x: -x[1])
        r["enemy_hero_lift_top"] = lift[:8]
        r["enemy_hero_lift_bottom"] = lift[-5:][::-1]
        # hazard: buy within next 10 min, by threat tercile (terciles per checkpoint)
        f = FIELD[THREAT[name]] + 2  # hazard key: (it, cp, wsh, ssh, deb, proc)
        hz = defaultdict(lambda: [0, 0])
        per_cp = defaultdict(list)
        for k, v in agg["hazard"].items():
            if k[0] == it:
                per_cp[k[1]].append((k[f], v[0], v[1]))
        for cp, rows in per_cp.items():
            tf = tercile_fn([(x, n) for x, n, _ in rows])
            for x, n, y in rows:
                g = tf(x)
                hz[g][0] += n
                hz[g][1] += y
        r["buy_next10_by_threat"] = {g: [hz[g][1] / max(1, hz[g][0]), hz[g][0]] for g in ("low", "mid", "high")}
        # choice-set win edge vs other same-tier vitality items bought by the same hero in the same 5-min bin
        f = FIELD[THREAT[name]] + 3  # event key: (it, hero, tb, wsh, ssh, deb, proc)
        same = {i for i, x in ITEMS.items() if x["slot"] == "vitality" and x["tier"] == tier}
        ev = [(k, v) for k, v in agg["events"].items() if k[0] in same]
        per_bin = defaultdict(list)
        for k, v in ev:
            per_bin[k[2]].append((k[f], v[0]))
        tfs = {tb: tercile_fn(p) for tb, p in per_bin.items()}
        cell = defaultdict(lambda: [0, 0, 0, 0])  # (hero, tb, lead, group) -> [n_c, w_c, n_o, w_o]
        for k, v in ev:
            g = tfs[k[2]](k[f])
            for key in ((k[1], k[2], k[7], g), (k[1], k[2], k[7], "all"), (k[1], k[2], k[7], "t" + str(k[2] // 600))):
                c = cell[key]
                if k[0] == it:
                    c[0] += v[0]
                    c[1] += v[1]
                else:
                    c[2] += v[0]
                    c[3] += v[1]

        cell2 = defaultdict(lambda: [0, 0, 0, 0])  # (hero, tb, lead, own-vs-team)
        for k, v in agg["events2"].items():
            if k[0] in same:
                c = cell2[k[1:]]
                if k[0] == it:
                    c[0] += v[0]
                    c[1] += v[1]
                else:
                    c[2] += v[0]
                    c[3] += v[1]

        def edge(sel, cells=cell):
            num = den = var = 0.0
            for key, (nc, wc, no, wo) in cells.items():
                if not sel(key) or nc == 0 or no < 5:
                    continue
                pc, po = wc / nc, wo / no
                p = (wc + wo) / (nc + no)
                num += nc * (pc - po)
                den += nc
                var += nc * nc * p * (1 - p) * (1 / nc + 1 / no)
            return [num / den if den else None, math.sqrt(var) / den if den else None, int(den)]
        r["win_edge"] = {"all": edge(lambda k: k[3] == "all"), "all_own_position": edge(lambda k: True, cell2)}
        r["win_edge_by_hero"] = sorted(([HEROES.get(h, h)] + edge(lambda k, h=h: k[0] == h, cell2)
                                        for h in {k[0] for k in cell2}), key=lambda x: -(x[3] or 0))
        r["win_edge_by_hero"] = [x for x in r["win_edge_by_hero"] if x[3] >= 1000]
        for g in ("low", "mid", "high"):
            r["win_edge"][g + "_threat"] = edge(lambda k, g=g: k[3] == g)
        for t in range(0, 8):
            e = edge(lambda k, t=t: k[3] == "t" + str(t))
            if e[2] >= 300:
                r["win_edge"][f"bought_{t * 10}-{t * 10 + 10}min"] = e
        rep["items"][name] = r
    json.dump(rep, open(f"{ROOT}/counters/out/report.json", "w"), indent=1)
    write_md(rep)


def pct(x, d=1):
    return "n/a" if x is None else f"{100 * x:.{d}f}%"


def pp(e):
    if not e or e[0] is None:
        return "n/a"
    return f"{100 * e[0]:+.1f} ± {196 * e[1]:.1f} (n={e[2]:,})"


def write_md(rep):
    L = [f"# Counter-item tables\n\nRanked matches since patch 09-29-2026: {rep['matches']:,} matches, "
         f"{rep['players']:,} player rows (duplicates removed). Generated by `scripts/report.py`.\n"]
    L.append("## 1. Who buys them and when\n\n| Item | Cost | Bought by | Median buy (min) | p25-p75 | Buyer win rate | Sold later |\n|---|---|---|---|---|---|---|")
    for n, r in rep["items"].items():
        m = r["buy_minute"]
        L.append(f"| {n} | {r['cost']} | {pct(r['buy_rate'])} | {m.get('median')} | {m.get('p25')}-{m.get('p75')} | "
                 f"{pct(r['buyer_win_rate'])} | {pct(r['sold_rate'])} |")
    L.append("\nBuy rate by rank:\n\n| Item | " + " | ".join(next(iter(rep["items"].values()))["buy_rate_by_rank"]) + " |\n|---|---|---|---|---|")
    for n, r in rep["items"].items():
        L.append(f"| {n} | " + " | ".join(pct(v) for v in r["buy_rate_by_rank"].values()) + " |")
    L.append("\n## 2. Heroes that buy each most\n")
    for n in MAIN:
        r = rep["items"][n]
        L.append(f"- **{n}**: " + ", ".join(f"{h} {pct(x, 0)}" for h, x, _ in r["top_buyers"]))
    L.append("\n## 3. Which enemy heroes trigger the purchase\n\nLift = buy rate when that hero is on the enemy team "
             "÷ overall buy rate.\n")
    for n in MAIN + EXTRA:
        r = rep["items"][n]
        L.append(f"- **{n}**: most vs " + ", ".join(f"{h} ×{x:.2f}" for h, x, _ in r["enemy_hero_lift_top"][:6])
                 + "; least vs " + ", ".join(f"{h} ×{x:.2f}" for h, x, _ in r["enemy_hero_lift_bottom"][:3]))
    L.append("\n## 4. Do players buy in response to the threat?\n\nPlayers alive at a checkpoint (10-35 min) who don't "
             "own the item yet: share who buy it in the next 10 minutes, by the enemy threat at the checkpoint "
             "(terciles per checkpoint).\n\n| Item | Threat measure | Low | Mid | High | High ÷ low |\n|---|---|---|---|---|---|")
    for n, r in rep["items"].items():
        h = r["buy_next10_by_threat"]
        ratio = h["high"][0] / h["low"][0] if h["low"][0] else float("nan")
        L.append(f"| {n} | {r['threat']} | {pct(h['low'][0])} | {pct(h['mid'][0])} | {pct(h['high'][0])} | ×{ratio:.2f} |")
    L.append("\nThreat measures: " + "; ".join(f"`{k}` = {v}" for k, v in THREAT_LABEL.items()) + ".")
    L.append("\n## 5. Does buying it win more than the alternatives?\n\nWin rate of players who bought the counter minus "
             "players of the same hero who bought a different vitality item of the same tier in the same 5-minute "
             "window with the same team soul lead (2,500-soul buckets), in percentage points (± 95% interval). Split by the enemy threat at the purchase.\n\n"
             "| Item | Overall | Low threat | Mid threat | High threat |\n|---|---|---|---|---|")
    for n, r in rep["items"].items():
        e = r["win_edge"]
        L.append(f"| {n} | {pp(e['all'])} | {pp(e['low_threat'])} | {pp(e['mid_threat'])} | {pp(e['high_threat'])} |")
    L.append("\nAlso holding the buyer's own position fixed (their held item souls vs their team's average, 1,500-soul "
             "buckets), on top of hero, time and team lead:\n\n| Item | Edge |\n|---|---|")
    for n, r in rep["items"].items():
        L.append(f"| {n} | {pp(r['win_edge']['all_own_position'])} |")
    L.append("\nBy buyer hero (own-position control, heroes with 1,000+ buys, most-bought first):\n")
    for n in MAIN:
        L.append(f"- **{n}**: " + ", ".join(f"{h} {100 * e:+.1f}" for h, e, se, k in rep["items"][n]["win_edge_by_hero"][:8]))
    L.append("\nBy purchase time:\n")
    for n in MAIN:
        e = rep["items"][n]["win_edge"]
        L.append(f"- **{n}**: " + ", ".join(f"{k.split('_')[1]} {pp(v).split(' (')[0]}" for k, v in e.items()
                                           if k.startswith("bought")))
    open(f"{ROOT}/counters/out/tables.md", "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
