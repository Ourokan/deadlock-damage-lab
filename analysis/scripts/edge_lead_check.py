"""How much team lead is in the real item win edges (validation/team_lead_edges.md, 2026-10-28).

item_win_edge.py matches each purchase on the team item-souls lead at the purchase (2,500-soul buckets). This redoes
its events (Ritualist+) with more lead keys and writes build_win_check.hero_edges() files per variant:
  none         no lead stratum
  lead         the shipped one (lead at the purchase bin)
  fine         1,000-soul buckets at the purchase bin
  post5/post10 the lead one / two 5-min bins after the purchase (matched on lead the item may have built)
  lead_post10  lead at the purchase and 10 min after
Then sim_vs_win_offline.py --edges compares the sim with each.

    python3 analysis/scripts/edge_lead_check.py events [--workers 2]   # ~5 min a file, cache in WORK
    python3 analysis/scripts/edge_lead_check.py edges OUT_DIR           # ~5 min
"""
import argparse
import glob
import gzip
import json
import os
import sys
from collections import defaultdict
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_win_check as B  # noqa: E402
import item_win_edge as W  # noqa: E402

WORK = f"{W.ROOT}/analysis/work/edge_lead"
VARS = {"none": lambda l, f, p5, p10: 0, "lead": lambda l, f, p5, p10: l, "fine": lambda l, f, p5, p10: f,
        "post5": lambda l, f, p5, p10: p5, "post10": lambda l, f, p5, p10: p10,
        "lead_post10": lambda l, f, p5, p10: (l, p10)}


def process(path):
    """item_win_edge.process with key (item, hero, tb, lead, rel, br, lead_fine, lead_post5, lead_post10)."""
    matches = defaultdict(dict)
    with gzip.open(path, "rt") as fh:
        for line in fh:
            r = json.loads(line)
            matches[r["match_id"]][r["account_id"]] = r
    ev = defaultdict(lambda: [0, 0])
    for rows in matches.values():
        rows = list(rows.values())
        if len(rows) != 12 or sum(r["won"] for r in rows) != 6:
            continue
        maxb = max((b for r in rows for _, b, _ in r["purchases"]), default=0)
        nb = maxb // W.BIN + 1
        held = [W.held_by_bin(r["purchases"], nb) for r in rows]
        team = {True: [0] * nb, False: [0] * nb}
        for r, h in zip(rows, held):
            t = team[r["won"]]
            for k in range(nb):
                t[k] += h[k]
        for r, h in zip(rows, held):
            won, br = r["won"], W.bracket(r["badge"])
            if br < B.MIN_BR:
                continue
            mine, theirs = team[won], team[not won]
            seen = set()
            for it, b, sold in r["purchases"]:
                if it in seen:
                    continue
                seen.add(it)
                if it not in W.TARGET:
                    continue
                k = b // W.BIN
                d = mine[k] - theirs[k]
                k1, k2 = min(nb - 1, k + 1), min(nb - 1, k + 2)
                e = ev[(it, r["hero_id"], k * W.BIN, max(-6, min(6, round(d / 2500))),
                        max(-4, min(4, round((h[k] - mine[k] / 6) / 1500))), br, max(-15, min(15, round(d / 1000))),
                        max(-6, min(6, round((mine[k1] - theirs[k1]) / 2500))),
                        max(-6, min(6, round((mine[k2] - theirs[k2]) / 2500))))]
                e[0] += 1
                e[1] += won
    with gzip.open(f"{WORK}/{os.path.basename(path)}.json.gz", "wt") as f:
        json.dump([list(k) + v for k, v in ev.items()], f)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("events", "edges"))
    ap.add_argument("out", nargs="?", default=".")
    ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args()
    if a.mode == "events":
        os.makedirs(WORK, exist_ok=True)
        files = [f for f in sorted(glob.glob(f"{W.DATA}/*.jsonl.gz"))
                 if not os.path.exists(f"{WORK}/{os.path.basename(f)}.json.gz")]
        with Pool(a.workers) as p:
            for x in p.imap_unordered(process, files):
                print(x, flush=True)
        return
    ev = {v: defaultdict(lambda: [0, 0]) for v in VARS}
    for p in sorted(glob.glob(f"{WORK}/*.json.gz")):
        with gzip.open(p, "rt") as f:
            for it, hero, tb, lead, rel, br, fine, p5, p10, n, w in json.load(f):
                if it not in B.ITEMS:
                    continue
                for v, fn in VARS.items():
                    e = ev[v][(it, hero, tb, fn(lead, fine, p5, p10), rel)]
                    e[0] += n
                    e[1] += w
    for v in VARS:
        heroes, fit = B.hero_edges(ev[v])
        B.write_edges(heroes, path=os.path.join(a.out, f"edges_{v}.json"), fit=fit, variant=v)
        print(v, flush=True)


if __name__ == "__main__":
    main()
