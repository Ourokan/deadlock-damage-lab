"""Check the site's recommended overall builds against real per-hero item win edge.

Per (hero, item) edge from the item_win_edge cache (analysis/work/item_win_edge, built by item_win_edge.py):
same matched stratum (hero, 5-min purchase bin, team lead, own souls vs team), vs buyers of other
same-slot same-tier items, brackets Ritualist+ (badge//10 >= 7). Raw per-hero edges are shrunk toward the item's all-hero edge (see TAU). Then, for every hero and budget of the
Phantom+ overall builds (damage/out/overall), lists recommended items whose real edge is clearly negative,
and strong-edge items the sim never picks.

    python3 analysis/scripts/build_win_check.py   # ~1 min
Writes analysis/out/hero_item_edge.json (per hero, used by the site) and analysis/out/build_win_check.md.
"""
from __future__ import annotations

import glob
import gzip
import json
import math
import os
from collections import defaultdict

ROOT = "/mnt/project-files"
WORK = f"{ROOT}/analysis/work/item_win_edge"
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = f"{REPO}/analysis/out"
ITEMS = {x["id"]: x for x in json.load(open(f"{REPO}/data/game/shop_items.json"))}
MIN_BR = 1          # item_win_edge.bracket(): 0 = badge//10 <= 6, 1 = 7-9 (Ritualist-Phantom), 2 = >= 10; so >= 1 is Ritualist+
Z = 1.96
# Hero-specific edges are shrunk toward the item's all-hero edge (empirical Bayes). TAU = spread of true
# per-hero edges around it: method of moments over (hero, item) cells with >= 300 matched buyers gave
# 1.2-1.8 points (rare items have a few dozen buyers per hero, raw edges of +-30 points are noise).
TAU = 0.015
STRONG = 0.015


def load():
    ev = defaultdict(lambda: [0, 0])   # (item, hero, tb, lead, rel) -> [n, w]
    for f in sorted(glob.glob(f"{WORK}/*.json.gz")):
        with gzip.open(f, "rt") as fh:
            d = json.load(fh)
        for it, hero, tb, lead, rel, br, n, w in d["events"]:
            if br < MIN_BR or it not in ITEMS:
                continue
            e = ev[(it, hero, tb, lead, rel)]
            e[0] += n
            e[1] += w
    return ev


def last_day():
    """Last match day in the cache (file names are <day>.jsonl.gz.json.gz)."""
    days = sorted(os.path.basename(f).split(".")[0] for f in glob.glob(f"{WORK}/*.json.gz"))
    return days[-1] if days else None


def hero_edges(ev):
    tot = defaultdict(lambda: [0, 0])   # (slot, tier, hero, tb, lead, rel)
    for (it, *s), (n, w) in ev.items():
        x = ITEMS[it]
        t = tot[(x["slot"], x["tier"], *s)]
        t[0] += n
        t[1] += w
    acc = defaultdict(lambda: [0.0, 0.0, 0.0, 0, 0])   # (hero, item) -> num, den, var, buyers, wins
    for (it, hero, tb, lead, rel), (nc, wc) in ev.items():
        x = ITEMS[it]
        a = acc[(hero, it)]
        a[3] += nc
        a[4] += wc
        tn, tw = tot[(x["slot"], x["tier"], hero, tb, lead, rel)]
        no, wo = tn - nc, tw - wc
        if no < 5:
            continue
        p = (wc + wo) / (nc + no)
        a[0] += nc * (wc / nc - wo / no)
        a[1] += nc
        a[2] += nc * nc * p * (1 - p) * (1 / nc + 1 / no)
    pool = defaultdict(lambda: [0.0, 0.0, 0.0])   # item -> all-hero num, den, var (prior mean and its variance)
    for (hero, it), a in acc.items():
        pool[it][0] += a[0]
        pool[it][1] += a[1]
        pool[it][2] += a[2]
    heroes = defaultdict(dict)
    for (hero, it), (num, den, var, n, w) in acc.items():
        if not den:
            continue
        raw, se = num / den, math.sqrt(var) / den
        prior, prior_var = pool[it][0] / pool[it][1], pool[it][2] / pool[it][1] ** 2
        k = TAU ** 2 / (TAU ** 2 + se ** 2)
        # posterior variance with the prior's own sampling noise (rare items: k ~ 0, so the prior's se dominates)
        heroes[hero][it] = {"edge": prior + k * (raw - prior), "se": math.sqrt(k * se ** 2 + (1 - k) ** 2 * prior_var),
                            "raw": raw, "raw_se": se, "prior": prior, "n": int(den), "buyers": n}
    return heroes


def sig(e, sign):
    return e and (e["edge"] - Z * e["se"] > 0 if sign > 0 else e["edge"] + Z * e["se"] < 0)


def main():
    heroes = hero_edges(load())
    idx = json.load(open(f"{REPO}/damage/out/overall/index.json"))
    hero_out = {str(h): {str(i): [round(100 * e["edge"], 2), round(100 * e["se"], 2), e["n"],
                                    round(100 * e["raw"], 2)]
                         for i, e in sorted(v.items())} for h, v in sorted(heroes.items())}
    patch = json.load(open(f"{REPO}/data/patch.json"))
    json.dump({"meta": {"brackets": "Ritualist+", "patch": patch["patch"], "matches_through": last_day(),
                        "note": "static snapshot: rerun this script (needs the shared-folder cache) after a patch", "unit": "win-rate points vs same-slot same-tier items",
                        "fields": ["edge (shrunk)", "se", "matched buyers", "raw edge"],
                        "tau": TAU}, "heroes": hero_out},
              open(f"{OUT}/hero_item_edge.json", "w"), separators=(",", ":"))
    bad_tot = defaultdict(list)      # item -> [(hero, budget, edge)]
    miss_tot = defaultdict(list)     # item -> [(hero, edge)]
    rows = []
    n_rec = n_bad = n_good = 0
    sum_edge = sum_pop = 0.0
    n_pop = 0
    for hid, h in sorted(idx["heroes"].items(), key=lambda kv: kv[1]["name"]):
        ph = h["brackets"].get("phantom")
        if not ph:
            continue
        he = heroes.get(int(hid), {})
        picked = set()
        hr = {"hero": h["name"], "budgets": {}}
        for bud, r in sorted(ph.items(), key=lambda kv: int(kv[0])):
            items = r["best"]["items"]
            picked |= set(items)
            bad = [(i, he[i]) for i in items if sig(he.get(i), -1)]
            for i in items:
                e = he.get(i)
                if e:
                    n_rec += 1
                    sum_edge += e["edge"]
                    n_bad += sig(e, -1)
                    n_good += sig(e, +1)
            for i in r["popular"]["items"]:
                if he.get(i):
                    sum_pop += he[i]["edge"]
                    n_pop += 1
            for i, e in bad:
                bad_tot[i].append((h["name"], bud, e["edge"]))
            hr["budgets"][bud] = bad
        miss = sorted(((i, e) for i, e in he.items() if i not in picked and e["edge"] >= STRONG and sig(e, +1)
                       and ITEMS[i]["tier"] <= 4), key=lambda x: -x[1]["edge"])
        for i, e in miss:
            miss_tot[i].append((h["name"], e["edge"]))
        hr["miss"] = miss
        rows.append(hr)
    nm = lambda i: ITEMS[i]["name"]
    pp = lambda v: f"{100 * v:+.1f}"
    L = ["# Recommended builds vs real win edge", "",
         "Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, "
         "vs other same-slot same-tier items, shrunk toward the item's all-hero edge) for every item in the Phantom+ \"Best overall\" builds. "
         f"Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.", "",
         f"- Recommended item slots with data: {n_rec}; mean edge {pp(sum_edge / max(n_rec, 1))} "
         f"(popular builds {pp(sum_pop / max(n_pop, 1))}); clearly positive {n_good}, clearly negative {n_bad}.", "",
         "Findings 2026-10-24 (one-off checks, not rerun by this script):",
         "- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) "
         "vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 "
         "damage-before-death score does not rank items the way real wins do.",
         "- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, "
         "Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, "
         "Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).",
         "- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves "
         "Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.",
         "- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 "
         "instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal "
         "lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state "
         "(deaths, enemy picks), not the item.", "",
         "## Recommended items that lose real games (hero x budget count)", "",
         "| Item | slot/tier | builds | heroes (edge) |", "|---|---|---:|---|"]
    for i, v in sorted(bad_tot.items(), key=lambda kv: -len(kv[1])):
        hs = {}
        for hn, b, e in v:
            hs[hn] = e
        L.append(f"| {nm(i)} | {ITEMS[i]['slot']} {ITEMS[i]['tier']} | {len(v)} | "
                 + ", ".join(f"{k} {pp(e)}" for k, e in sorted(hs.items(), key=lambda kv: kv[1])) + " |")
    L += ["", f"## Strong items the sim never picks (edge >= {pp(STRONG)}, lower 95% bound > 0)", "",
          "| Item | slot/tier | heroes | heroes (edge) |", "|---|---|---:|---|"]
    for i, v in sorted(miss_tot.items(), key=lambda kv: -len(kv[1])):
        L.append(f"| {nm(i)} | {ITEMS[i]['slot']} {ITEMS[i]['tier']} | {len(v)} | "
                 + ", ".join(f"{k} {pp(e)}" for k, e in sorted(v, key=lambda x: -x[1])) + " |")
    L += ["", "## Per hero", ""]
    for hr in rows:
        L.append(f"### {hr['hero']}")
        for b, bad in hr["budgets"].items():
            if bad:
                L.append(f"- {int(b) // 1000}k: " + ", ".join(f"{nm(i)} {pp(e['edge'])}" for i, e in bad))
        if hr["miss"]:
            L.append("- never picked: " + ", ".join(f"{nm(i)} {pp(e['edge'])}" for i, e in hr["miss"][:8]))
        L.append("")
    open(f"{OUT}/build_win_check.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L[:60]))


if __name__ == "__main__":
    main()
