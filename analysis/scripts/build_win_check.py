"""Check the site's recommended overall builds against real per-hero item win edge.

Per (hero, item) edge from the item_win_edge cache (analysis/work/item_win_edge, built by item_win_edge.py):
same matched stratum (hero, 5-min purchase bin, team lead, own souls vs team), vs buyers of other
same-slot same-tier items, brackets Ritualist+ (badge//10 >= 7). Raw per-hero edges are shrunk toward the item's all-hero edge,
lowered for items the hero seldom buys (see TAU and SHARE_KNEE). Then, for every hero and budget of the
Phantom+ overall builds (damage/out/overall), lists recommended items whose real edge is clearly negative,
and strong-edge items the sim never picks.

    python3 analysis/scripts/build_win_check.py   # ~1 min
Writes analysis/out/hero_item_edge.json (per hero, used by the overall search and the site) and
analysis/out/build_win_check.md. --report-only rewrites just the .md from the existing hero_item_edge.json (the
patch rerun does this after the overall search; pipeline/refresh_win_edge.py refreshes the edges from the
rerun's own player builds).
"""
from __future__ import annotations

import argparse
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
EDGE_PATH = f"{OUT}/hero_item_edge.json"
ITEMS = {x["id"]: x for x in json.load(open(f"{REPO}/data/game/shop_items.json"))}
MIN_BR = 1          # item_win_edge.bracket(): 0 = badge//10 <= 6, 1 = 7-9 (Ritualist-Phantom), 2 = >= 10; so >= 1 is Ritualist+
Z = 1.96
# Hero-specific edges are shrunk toward the item's all-hero edge (empirical Bayes). TAU = spread of true
# per-hero edges around it: method of moments over (hero, item) cells with >= 300 matched buyers gave
# 1.2-1.8 points (rare items have a few dozen buyers per hero, raw edges of +-30 points are noise).
TAU = 0.015
# Rare picks (2026-10-25): an item a hero seldom buys does worse on that hero than the item's all-hero edge says,
# and its true edge varies more. Below SHARE_KNEE of the hero's buyers of same-slot same-tier items, the prior is
# the all-hero edge + beta x decades below the knee and tau^2 grows by tau2_rare per decade (rarity_fit, refitted on
# every rebuild; written to the edge file's meta). 09-30 to 10-14 Ritualist+: beta -1.5 points per decade, tau 1.2
# points at common picks, 2.7 at 0.3% share. Checked on two disjoint halves of the players (by account): positive
# edges at < 0.5% share in one half averaged -2.4 +- 2.3 in the other (the old shrinkage made them +4.0), negative
# rare edges held (-4.2 -> -7.5); with the rare-pick prior every share bin matches the other half, error vs the other
# half 1.15/1.17 -> 1.09/1.13 points. Binomial se is honest: the halves disagree no more than it says, so a rare
# item bought by the same few players is not extra noise. Sim vs real (sim_vs_win.py, 27k): edges clear of noise
# r 0.181 -> 0.187; over all pairs 0.154 -> 0.136, since the sim rates off-meta picks higher than real games do.
SHARE_KNEE = 0.03
SHARE_FLOOR = 1e-4
STRONG = 0.015


def load(files=None):
    """Ritualist+ event counts from item_win_edge.py partials (default: every file in the shared-folder cache)."""
    ev = defaultdict(lambda: [0, 0])   # (item, hero, tb, lead, rel) -> [n, w]
    for f in files if files is not None else sorted(glob.glob(f"{WORK}/*.json.gz")):
        with gzip.open(f, "rt") as fh:
            d = json.load(fh)
        for it, hero, tb, lead, rel, br, n, w in d["events"]:
            if br < MIN_BR or it not in ITEMS:
                continue
            e = ev[(it, hero, tb, lead, rel)]
            e[0] += n
            e[1] += w
    return ev


def last_day(files=None):
    """Last match day in the cache (file names are <day>.jsonl.gz.json.gz)."""
    days = sorted(os.path.basename(f).split(".")[0] for f in (files if files is not None else glob.glob(f"{WORK}/*.json.gz")))
    return days[-1] if days else None


def hero_edges(ev, fit=None):
    """(hero -> item -> edge dict, rarity fit). fit: reuse a rarity_fit() result instead of fitting on ev."""
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
    group = defaultdict(int)   # (hero, slot, tier) -> buyers, for each item's share of its hero's slot/tier buys
    for (hero, it), a in acc.items():
        group[(hero, ITEMS[it]["slot"], ITEMS[it]["tier"])] += a[3]
    cells = []
    for (hero, it), (num, den, var, n, w) in acc.items():
        if not den:
            continue
        share = n / group[(hero, ITEMS[it]["slot"], ITEMS[it]["tier"])]
        cells.append({"hero": hero, "item": it, "raw": num / den, "raw_se": math.sqrt(var) / den,
                      "prior0": pool[it][0] / pool[it][1], "prior_var": pool[it][2] / pool[it][1] ** 2,
                      "n": int(den), "buyers": n, "share": share,
                      "rare": max(0.0, math.log10(SHARE_KNEE / max(share, SHARE_FLOOR)))})
    fit = fit or rarity_fit(cells)
    heroes = defaultdict(dict)
    for c in cells:
        raw, se = c["raw"], c["raw_se"]
        prior = c["prior0"] + fit["beta"] * c["rare"]
        tau2 = fit["tau2"] + fit["tau2_rare"] * c["rare"]
        k = tau2 / (tau2 + se ** 2)
        # posterior variance with the prior's own sampling noise (rare items: k ~ 0, so the prior's se dominates)
        heroes[c["hero"]][c["item"]] = {
            "edge": prior + k * (raw - prior), "se": math.sqrt(k * se ** 2 + (1 - k) ** 2 * c["prior_var"]),
            "raw": raw, "raw_se": se, "prior": prior, "n": c["n"], "buyers": c["buyers"], "share": c["share"]}
    return heroes, fit


def rarity_fit(cells):
    """Rare-pick prior: beta (edge per decade of share below SHARE_KNEE, weighted least squares of raw - all-hero
    edge) and tau^2 = tau2 + tau2_rare x decades (method of moments on the squared residuals beyond the binomial
    variance), iterated with each other's weights."""
    tau2, tau2_rare, beta = TAU ** 2, 0.0, 0.0
    for _ in range(4):
        w = [1 / (c["raw_se"] ** 2 + tau2 + tau2_rare * c["rare"]) for c in cells]
        sxx = sum(wi * c["rare"] ** 2 for wi, c in zip(w, cells))
        beta = sum(wi * c["rare"] * (c["raw"] - c["prior0"]) for wi, c in zip(w, cells)) / sxx if sxx else 0.0
        y = [(c["raw"] - c["prior0"] - beta * c["rare"]) ** 2 - c["raw_se"] ** 2 for c in cells]
        w2 = [wi * wi for wi in w]
        s0 = sum(w2)
        s1 = sum(wi * c["rare"] for wi, c in zip(w2, cells))
        s2 = sum(wi * c["rare"] ** 2 for wi, c in zip(w2, cells))
        t0 = sum(wi * yi for wi, yi in zip(w2, y))
        t1 = sum(wi * c["rare"] * yi for wi, c, yi in zip(w2, cells, y))
        det = s0 * s2 - s1 * s1
        if det <= 0:
            break
        tau2 = max((0.5 * TAU) ** 2, (s2 * t0 - s1 * t1) / det)
        tau2_rare = max(0.0, (s0 * t1 - s1 * t0) / det)
    return {"beta": beta, "tau2": tau2, "tau2_rare": tau2_rare}


def sig(e, sign):
    return e and (e["edge"] - Z * e["se"] > 0 if sign > 0 else e["edge"] + Z * e["se"] < 0)


def write_edges(heroes, path=EDGE_PATH, fit=None, **meta):
    """hero_item_edge.json: hero id -> item id -> [edge, se, matched buyers, raw edge], in win-rate points."""
    hero_out = {str(h): {str(i): [round(100 * e["edge"], 2), round(100 * e["se"], 2), e["n"],
                                    round(100 * e["raw"], 2)]
                         for i, e in sorted(v.items())} for h, v in sorted(heroes.items())}
    m = {"brackets": "Ritualist+", "unit": "win-rate points vs same-slot same-tier items",
         "fields": ["edge (shrunk)", "se", "matched buyers", "raw edge"], "tau": TAU}
    if fit:
        m["rare_pick"] = {"knee_share": SHARE_KNEE, "beta_per_decade": round(100 * fit["beta"], 3),
                          "tau": round(100 * math.sqrt(fit["tau2"]), 3),
                          "tau2_per_decade": round(1e4 * fit["tau2_rare"], 3)}
        m["tau"] = round(math.sqrt(fit["tau2"]), 5)
    m.update(meta)
    with open(path + ".tmp", "w") as f:
        json.dump({"meta": m, "heroes": hero_out}, f, separators=(",", ":"))
    os.replace(path + ".tmp", path)


def read_edges(path=EDGE_PATH):
    """hero_item_edge.json back into hero_edges() form (fractions; only edge and se are kept)."""
    with open(path) as f:
        d = json.load(f)
    return {int(h): {int(i): {"edge": v[0] / 100, "se": v[1] / 100} for i, v in row.items()}
            for h, row in d["heroes"].items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-only", action="store_true",
                    help="rewrite build_win_check.md from the existing hero_item_edge.json")
    a = ap.parse_args()
    if a.report_only:
        heroes = read_edges()
    else:
        heroes, fit = hero_edges(load())
        patch = json.load(open(f"{REPO}/data/patch.json"))
        write_edges(heroes, fit=fit, patch=patch["patch"], matches_through=last_day(),
                    note="from the shared-folder cache; patch reruns refresh it from their own builds")
    report(heroes)


def report(heroes):
    idx = json.load(open(f"{REPO}/damage/out/overall/index.json"))
    with open(EDGE_PATH) as f:
        em = json.load(f)["meta"]
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
         "vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ \"Best overall\" builds. "
         f"Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.", "",
         f"Edges: patch {em.get('patch')}, matches {em.get('matches_from', '?')} to {em.get('matches_through')}"
         + (f", {em['matches']:,} Ritualist+ matches" if em.get("matches") else "")
         + (f" (refreshed {em['refreshed']})" if em.get("refreshed") else "") + ".", "",
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
