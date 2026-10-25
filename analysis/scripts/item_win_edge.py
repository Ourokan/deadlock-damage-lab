"""Matched win edge of every shop item (tier 1-4, all slots) from current-patch ranked builds.

Generalises counters/scripts/analyze.py (events2) + report.py (edge) from 14 vitality items to every item:

  event   = a player's FIRST purchase of an item of tier 1-4
  stratum = (own hero, 5-min purchase bin, team item-souls lead bucket, own-souls-vs-team bucket)
            lead = round((own team held item souls - enemy team held item souls) / 2500), clipped to +-6
            rel  = round((own held item souls - own team held / 6) / 1500), clipped to +-4
            (holdings measured at the start of the 5-min bin, exactly as analyze.py)
  edge    = sum_s n_item,s * (wr_item,s - wr_others,s) / sum_s n_item,s
            others = buyers of OTHER items of the same slot AND tier in the same stratum (cells with <5 others
            dropped), SE = sqrt(sum n_c^2 p(1-p)(1/n_c + 1/n_o)) / sum n_c (report.py's formula).
  bracket = badge//10 <= 6 "low", 7-9 "mid", >= 10 "high"; per-bracket edges stratify on bracket too.

Per-file partial counts are cached in analysis/work/item_win_edge/ (resumable).

    python3 scripts/item_win_edge.py [--workers 2] [--limit N] [--aggregate-only]
"""
from __future__ import annotations

import argparse
import glob
import gzip
import json
import math
import os
import sys
import time
from collections import defaultdict
from multiprocessing import Pool

ROOT = "/mnt/project-files"
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = f"{ROOT}/data/builds/player_builds"
WORK = f"{ROOT}/analysis/work/item_win_edge"
OUT = f"{ROOT}/analysis/out"
# the repo's game data is the current patch's (the patch rerun pulls it before reading new builds)
ITEMS = {x["id"]: x for x in json.load(open(f"{REPO}/data/game/shop_items.json"))}
COST = {i: x["cost"] for i, x in ITEMS.items()}
TIER = {i: x["tier"] for i, x in ITEMS.items()}
SLOT = {i: x["slot"] for i, x in ITEMS.items()}
TARGET = {i for i, t in TIER.items() if 1 <= t <= 4}
BIN = 300
BRACKETS = ("low", "mid", "high")


def bracket(badge):
    t = (badge or 0) // 10
    return 0 if t <= 6 else 1 if t <= 9 else 2


def held_by_bin(purchases, nbins):
    """Item souls held at t = k*BIN for k in 0..nbins-1 (held iff buy <= t and (sold == 0 or sold > t))."""
    diff = [0] * (nbins + 1)
    for it, b, sold in purchases:
        c = COST.get(it)
        if c is None:
            continue
        s = -(-b // BIN)  # first k with k*BIN >= b
        if s >= nbins:
            continue
        # held while t < sold: last held k has k*BIN < sold -> end (exclusive) = ceil(sold/BIN)
        e = nbins if sold == 0 else min(nbins, -(-sold // BIN))
        if e > s:
            diff[s] += c
            diff[e] -= c
    out, acc = [], 0
    for k in range(nbins):
        acc += diff[k]
        out.append(acc)
    return out


def process(path):
    matches = defaultdict(dict)
    with gzip.open(path, "rt") as fh:
        for line in fh:
            r = json.loads(line)
            matches[r["match_id"]][r["account_id"]] = r
    ev = defaultdict(lambda: [0, 0])     # (item, hero, tb, lead, rel, br) -> [n, wins]
    side = defaultdict(lambda: [0, 0, 0, 0])  # item -> [n, sum buy_s, sum lead, sum rel]
    n_match = n_players = 0
    by_br = [0] * len(BRACKETS)
    for rows in matches.values():
        rows = list(rows.values())
        if len(rows) != 12 or sum(r["won"] for r in rows) != 6:
            continue
        n_match += 1
        by_br[bracket(rows[0]["badge"])] += 1   # badge is the match's average badge, the same on every row
        n_players += 12
        maxb = max((b for r in rows for _, b, _ in r["purchases"]), default=0)
        nb = maxb // BIN + 1
        held = [held_by_bin(r["purchases"], nb) for r in rows]
        team = {True: [0] * nb, False: [0] * nb}
        for r, h in zip(rows, held):
            t = team[r["won"]]
            for k in range(nb):
                t[k] += h[k]
        for r, h in zip(rows, held):
            won = r["won"]
            hero = r["hero_id"]
            br = bracket(r["badge"])
            mine, theirs = team[won], team[not won]
            seen = set()
            for it, b, sold in r["purchases"]:
                if it in seen:
                    continue
                seen.add(it)
                if it not in TARGET:
                    continue
                k = b // BIN
                lead = max(-6, min(6, round((mine[k] - theirs[k]) / 2500)))
                rel = max(-4, min(4, round((h[k] - mine[k] / 6) / 1500)))
                e = ev[(it, hero, k * BIN, lead, rel, br)]
                e[0] += 1
                e[1] += won
                s = side[it]
                s[0] += 1
                s[1] += b
                s[2] += lead
                s[3] += rel
    return {"file": os.path.basename(path), "matches": n_match, "players": n_players, "matches_by_bracket": by_br,
            "events": [list(k) + v for k, v in ev.items()],
            "side": [[k] + v for k, v in side.items()]}


def run(workers, limit):
    files = sorted(glob.glob(f"{DATA}/*.jsonl.gz"))
    if limit:
        files = files[:limit]
    todo = [f for f in files if not os.path.exists(f"{WORK}/{os.path.basename(f)}.json.gz")]
    print(f"{len(files)} files, {len(todo)} to process", file=sys.stderr, flush=True)
    t0 = time.time()
    with Pool(workers) as p:
        for res in p.imap_unordered(process, todo):
            tmp = f"{WORK}/{res['file']}.json.gz.tmp"
            with gzip.open(tmp, "wt") as fh:
                json.dump(res, fh)
            os.replace(tmp, f"{WORK}/{res['file']}.json.gz")
            print(f"{res['file']} matches={res['matches']} events={len(res['events'])} "
                  f"t={time.time() - t0:.0f}s", file=sys.stderr, flush=True)
    return files


def edge(cells):
    """cells: iterable of (n_c, w_c, n_o, w_o). Returns [edge, se, n_used]."""
    num = den = var = 0.0
    for nc, wc, no, wo in cells:
        if nc == 0 or no < 5:
            continue
        pc, po = wc / nc, wo / no
        p = (wc + wo) / (nc + no)
        num += nc * (pc - po)
        den += nc
        var += nc * nc * p * (1 - p) * (1 / nc + 1 / no)
    if not den:
        return [None, None, 0]
    return [num / den, math.sqrt(var) / den, int(den)]


def aggregate(files):
    names = {os.path.basename(f) for f in files}
    ev = defaultdict(lambda: [0, 0])
    side = defaultdict(lambda: [0, 0, 0, 0])
    matches = players = 0
    used = 0
    for f in sorted(glob.glob(f"{WORK}/*.json.gz")):
        if os.path.basename(f)[:-len(".json.gz")] not in names:
            continue
        used += 1
        with gzip.open(f, "rt") as fh:
            d = json.load(fh)
        matches += d["matches"]
        players += d["players"]
        for it, hero, tb, lead, rel, br, n, w in d["events"]:
            e = ev[(it, hero, tb, lead, rel, br)]
            e[0] += n
            e[1] += w
        for it, *v in d["side"]:
            s = side[it]
            for i, x in enumerate(v):
                s[i] += x
    # per group (slot, tier): stratum totals, and per-item stratum counts
    tot_all = defaultdict(lambda: [0, 0])    # (grp, hero, tb, lead, rel) -> [n, w]
    tot_br = defaultdict(lambda: [0, 0])     # (grp, hero, tb, lead, rel, br)
    it_all = defaultdict(lambda: defaultdict(lambda: [0, 0]))   # item -> stratum -> [n, w]
    it_br = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for (it, hero, tb, lead, rel, br), (n, w) in ev.items():
        g = (SLOT[it], TIER[it])
        s = (hero, tb, lead, rel)
        for d_, key in ((tot_all, (g,) + s), (tot_br, (g,) + s + (br,))):
            d_[key][0] += n
            d_[key][1] += w
        for d_, key in ((it_all[it], s), (it_br[it], s + (br,))):
            d_[key][0] += n
            d_[key][1] += w

    def cells(it, sel=lambda s: True, by_br=None):
        g = (SLOT[it], TIER[it])
        if by_br is None:
            src, tot = it_all[it], tot_all
        else:
            src, tot = it_br[it], tot_br
        for s, (n, w) in src.items():
            if by_br is not None and s[4] != by_br:
                continue
            if not sel(s):
                continue
            tn, tw = tot[(g,) + s]
            yield n, w, tn - n, tw - w

    bands = [("0-10", 0, 600), ("10-20", 600, 1200), ("20-30", 1200, 1800), ("30+", 1800, 10 ** 9)]
    out = {}
    for it in sorted(side, key=lambda i: (SLOT[i], TIER[i], ITEMS[i]["name"])):
        x = ITEMS[it]
        n, sb, sl, sr = side[it]
        wins = sum(w for (n_, w) in it_all[it].values())
        e = edge(cells(it))
        r = {"name": x["name"], "slot": x["slot"], "tier": x["tier"], "cost": x["cost"],
             "n_buyers": n, "buy_rate": n / players, "buyer_win_rate": wins / n,
             "mean_buy_min": sb / n / 60, "mean_lead_bucket": sl / n, "mean_rel_bucket": sr / n,
             "edge": e[0], "se": e[1], "n_matched": e[2],
             "ci95": [e[0] - 1.96 * e[1], e[0] + 1.96 * e[1]] if e[0] is not None else None,
             "by_bracket": {}, "by_buy_time": {}}
        for bi, bn in enumerate(BRACKETS):
            eb = edge(cells(it, by_br=bi))
            r["by_bracket"][bn] = {"edge": eb[0], "se": eb[1], "n_matched": eb[2]}
        for lab, lo, hi in bands:
            et = edge(cells(it, sel=lambda s, lo=lo, hi=hi: lo <= s[1] < hi))
            r["by_buy_time"][lab] = {"edge": et[0], "se": et[1], "n_matched": et[2]}
        out[str(it)] = r
    meta = {"matches": matches, "players": players, "files": used,
            "bracket_def": "badge//10: <=6 low (Initiate-Arcanist), 7-9 mid (Ritualist-Phantom), >=10 high",
            "method": __doc__.split("Per-file")[0].strip()}
    json.dump({"meta": meta, "items": out}, open(f"{OUT}/item_win_edge.json", "w"), indent=1)
    write_md(meta, out)
    return meta, out


def f_pp(v, d=1):
    return "n/a" if v is None else f"{100 * v:+.{d}f}"


def write_md(meta, out):
    L = ["# Item win edge (all tier 1-4 items)", "",
         f"{meta['matches']:,} ranked matches ({meta['players']:,} players), current patch builds. "
         "Edge = win-rate points vs buyers of other same-slot same-tier items, matched on hero, 5-min purchase "
         "bin, team item-souls lead and own souls vs team (Mantel-Haenszel-style pooled difference, weights = "
         "buyers). CI = 95% normal approx. Bracket edges: low = Initiate-Arcanist, mid = Ritualist-Phantom, "
         "high = Ascendant-Eternus. `lead` = mean team item-souls lead bucket at purchase (1 = +2,500 souls); "
         "`min` = mean purchase minute.", "",
         "Script: `analysis/scripts/item_win_edge.py`. Data: `analysis/out/item_win_edge.json`.", ""]
    groups = defaultdict(list)
    for r in out.values():
        groups[(r["slot"], r["tier"])].append(r)
    for slot in ("weapon", "vitality", "spirit"):
        for tier in (1, 2, 3, 4):
            rs = groups.get((slot, tier))
            if not rs:
                continue
            rs.sort(key=lambda r: -(r["edge"] if r["edge"] is not None else -9))
            L += [f"## {slot.capitalize()} tier {tier} ({rs[0]['cost']:,} souls)", "",
                  "| Item | buyers | buy % | raw WR | edge | 95% CI | low | mid | high | min | lead |",
                  "|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|"]
            for r in rs:
                ci = f"{f_pp(r['ci95'][0])} to {f_pp(r['ci95'][1])}" if r["ci95"] else "n/a"
                b = r["by_bracket"]
                L.append(f"| {r['name']} | {r['n_buyers']:,} | {100 * r['buy_rate']:.1f} | "
                         f"{100 * r['buyer_win_rate']:.1f} | **{f_pp(r['edge'])}** | {ci} | "
                         f"{f_pp(b['low']['edge'])} | {f_pp(b['mid']['edge'])} | {f_pp(b['high']['edge'])} | "
                         f"{r['mean_buy_min']:.0f} | {r['mean_lead_bucket']:+.2f} |")
            L.append("")
    open(f"{OUT}/item_win_edge.md", "w").write("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--aggregate-only", action="store_true")
    a = ap.parse_args()
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    if a.aggregate_only:
        files = sorted(glob.glob(f"{DATA}/*.jsonl.gz"))[: a.limit or None]
    else:
        files = run(a.workers, a.limit)
    meta, out = aggregate(files)
    print(f"done: {meta['matches']:,} matches, {len(out)} items, {time.time() - t0:.0f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
