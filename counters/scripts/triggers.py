"""What on the enemy team triggers a counter-item purchase: specific enemy items (Decay -> Dispel Magic?) and enemy
heroes (their abilities).

Every 5 minutes (5-40 min) each player who doesn't own counter C yet is "at risk"; the outcome is buying C in the next
5 minutes. Exposure = an enemy holds item X at that moment (or hero H is on the enemy team). The rate ratio is
Mantel-Haenszel pooled over strata of (buyer's own hero, checkpoint): who buys a counter depends mostly on the
buyer's hero, and late-game enemy items would otherwise look like triggers just because everyone buys more later.

    python3 scripts/triggers.py --workers 3 && python3 scripts/triggers.py --report
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
sys.path.insert(0, os.path.dirname(__file__))
from analyze import COUNTER_IDS, ITEMS  # noqa: E402

HEROES = {h["id"]: h["name"] for h in json.load(open(f"{ROOT}/data/game/heroes.json"))}
CPS = range(300, 2401, 300)
DEBUFFS = ("Decay", "Toxic Bullets", "Slowing Hex", "Disarming Hex", "Silence Wave", "Knockdown", "Cursed Relic",
           "Spirit Burn", "Alchemical Fire", "Mystic Slow", "Silencer", "Inhibitor", "Arctic Blast", "Vortex Web",
           "Scourge", "Healbane", "Crippling Headshot", "Slowing Bullets")
GUN = ("Toxic Bullets", "Tesla Bullets", "Mystic Shot", "Silencer", "Inhibitor", "Siphon Bullets", "Burst Fire",
       "Lucky Shot", "Armor Piercer", "Headhunter", "Glass Cannon", "Crippling Headshot", "Spiritual Overflow",
       "Escalating Exposure", "Swift Striker", "Hollow Point", "Express Shot")
NAMED = {"Dispel Magic": DEBUFFS, "Debuff Reducer": DEBUFFS, "Unstoppable": DEBUFFS,
         "Metal Skin": GUN, "Return Fire": GUN, "Plated Armor": GUN, "Bullet Resilience": GUN,
         "Counterspell": ("Tankbuster", "Spirit Burn", "Boundless Spirit", "Mystic Reverb", "Echo Shard",
                          "Refresher", "Lightning Scroll", "Decay", "Cursed Relic", "Knockdown")}
WINDOW = 300


def process(path):
    matches = defaultdict(dict)
    with gzip.open(path, "rt") as fh:
        for line in fh:
            r = json.loads(line)
            matches[r["match_id"]][r["account_id"]] = r
    base = defaultdict(lambda: [0, 0])   # (counter, own_hero) -> [at risk, bought]
    exp = defaultdict(lambda: [0, 0])    # (counter, own_hero, "i"+item | "h"+hero) -> [at risk, bought]
    for rows in matches.values():
        rows = list(rows.values())
        if len(rows) != 12 or sum(r["won"] for r in rows) != 6:
            continue
        for r in rows:
            enemies = [e for e in rows if e["won"] != r["won"]]
            first = {}
            for it, b, _ in r["purchases"]:
                first.setdefault(it, b)
            for cp in CPS:
                if r["duration_s"] < cp + WINDOW:
                    break
                held = {"i%d" % it for e in enemies for it, b, s in e["purchases"]
                        if b <= cp and (s == 0 or s > cp) and it in ITEMS}
                held |= {"h%d" % e["hero_id"] for e in enemies}
                for c in COUNTER_IDS:
                    if c in first and first[c] <= cp:
                        continue
                    y = 1 if c in first and first[c] <= cp + WINDOW else 0
                    k = (c, r["hero_id"] * 10000 + cp)
                    base[k][0] += 1
                    base[k][1] += y
                    for x in held:
                        e = exp[k + (x,)]
                        e[0] += 1
                        e[1] += y
    return os.path.basename(path), [[list(k), v] for k, v in base.items()], [[list(k), v] for k, v in exp.items()]


def report():
    base = defaultdict(lambda: [0, 0])
    exp = defaultdict(lambda: [0, 0])
    for f in glob.glob(f"{ROOT}/counters/work/triggers/*.json"):
        d = json.load(open(f))
        for k, v in d["base"]:
            b = base[tuple(k)]
            b[0] += v[0]
            b[1] += v[1]
        for k, v in d["exp"]:
            b = exp[tuple(k)]
            b[0] += v[0]
            b[1] += v[1]
    out = {}
    by_c = defaultdict(lambda: defaultdict(list))
    for (c, h, x), v in exp.items():
        by_c[c][x].append((h, v))
    for c, xs in by_c.items():
        res = []
        for x, strata in xs.items():
            num = den = 0.0
            n_exp = buys_exp = 0
            for h, (n1, a) in strata:
                n_all, y_all = base[(c, h)]
                n0, b = n_all - n1, y_all - a
                N = n_all
                if N == 0:
                    continue
                num += a * n0 / N
                den += b * n1 / N
                n_exp += n1
                buys_exp += a
            if n_exp < 3000 or den == 0:
                continue
            name = ITEMS[int(x[1:])]["name"] if x[0] == "i" else HEROES.get(int(x[1:]), x)
            res.append({"kind": "item" if x[0] == "i" else "hero", "name": name, "rate_ratio": num / den,
                        "buy_rate_exposed": buys_exp / n_exp, "n_exposed": n_exp})
        out[COUNTER_IDS[c]] = sorted(res, key=lambda r: -r["rate_ratio"])
    json.dump(out, open(f"{ROOT}/counters/out/triggers.json", "w"), indent=1)
    L = ["# What triggers counter-item buys\n",
         "Rate ratio = how much more likely a player is to buy the counter in the next 5 minutes when an enemy holds "
         "that item (or that hero is on the enemy team), versus when not, at the same moment. Pooled over the buyer's own hero "
         "and the checkpoint (Mantel-Haenszel). Checkpoints every 5 min from 5 to 40 min; exposures with 3,000+ player-checkpoints.\n"]
    for c in COUNTER_IDS.values():
        rows = out.get(c, [])
        items = [r for r in rows if r["kind"] == "item"]
        heroes = [r for r in rows if r["kind"] == "hero"]
        L.append(f"## {c}\n")
        L.append("Strongest enemy-item triggers: " + ", ".join(f"{r['name']} ×{r['rate_ratio']:.2f}" for r in items[:10]))
        named = [r for r in items if r["name"] in NAMED.get(c, ())]
        if named:
            L.append("\nNamed threats: " + ", ".join(f"{r['name']} ×{r['rate_ratio']:.2f}" for r in named))
        L.append("\nEnemy heroes: " + ", ".join(f"{r['name']} ×{r['rate_ratio']:.2f}" for r in heroes[:8])
                 + "; least: " + ", ".join(f"{r['name']} ×{r['rate_ratio']:.2f}" for r in heroes[-3:][::-1]) + "\n")
    open(f"{ROOT}/counters/out/triggers.md", "w").write("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if a.report:
        return report()
    d = f"{ROOT}/counters/work/triggers"
    os.makedirs(d, exist_ok=True)
    files = [f for f in sorted(glob.glob(f"{ROOT}/data/builds/player_builds/*.jsonl.gz"))
             if not os.path.exists(f"{d}/{os.path.basename(f)}.json")]
    with Pool(a.workers) as p:
        for name, base, exp in p.imap_unordered(process, files):
            json.dump({"base": base, "exp": exp}, open(f"{d}/{name}.json", "w"))
            print(name, file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
