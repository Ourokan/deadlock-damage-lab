"""Turn work/jobs/*.json into the files the web page reads (damage/out/).

out/index.json        budgets, objectives, and per hero x budget: best damage vs the popular build's
out/heroes/<id>.json  per budget: dummy HP, popular build, and per objective the top builds (damage at 5/15/30 s,
                      DPS, damage by source), each item's loss when removed from the best build, and every
                      candidate item's damage gain per 1000 souls when added to the popular build
out/summary.csv       one row per hero x budget x objective
out/order/<id>.json   per objective: the order to buy the best 50k build in, with milestones (scripts/buy_order.py)
Item names and costs: search/out/items.json (same ids).

usage: python3 scripts/export.py
"""
import csv
import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "..", "sim"))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "..", "data"))
from deadsim import game  # noqa: E402
import patch_state  # noqa: E402
import dummy_search as D  # noqa: E402

OUT = os.path.join(ROOT, "out")


def main():
    G = game()
    os.makedirs(os.path.join(OUT, "heroes"), exist_ok=True)
    jobs = {}
    for fn in glob.glob(os.path.join(ROOT, "work", "jobs", "*.json")):
        r = json.load(open(fn))
        jobs.setdefault(r["hero_id"], {})[r["budget"]] = r
    index, rows = [], []
    for hid in sorted(jobs):
        per, summ = {}, {}
        for b, r in sorted(jobs[hid].items()):
            per[str(b)] = {k: r[k] for k in ("item_budget", "dummy_hp", "aim", "popular", "objectives")}
            summ[str(b)] = {}
            for obj, o in r["objectives"].items():
                best = o["builds"][0]
                summ[str(b)][obj] = {"best": best["damage"][obj], "popular": r["popular"]["damage"][obj]}
                rows.append({"hero": r["hero"], "hero_id": hid, "souls": b, "objective": obj,
                             "best_damage": best["damage"][obj], "popular_damage": r["popular"]["damage"][obj],
                             "best_build": " | ".join(G.items[i].name for i in best["items"]),
                             "popular_build": " | ".join(G.items[i].name for i in r["popular"]["items"])})
        name = G.hero(hid).name
        json.dump({"hero_id": hid, "hero": name, "budgets": per}, open(os.path.join(OUT, "heroes", f"{hid}.json"), "w"))
        index.append({"id": hid, "name": name, "budgets": summ})
    json.dump({
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "patch": patch_state.load()["patch"],
        "objectives": {k: f"damage dealt to the dummy in the first {v:g} s" for k, v in D.WINDOWS.items()},
        "dummy": "never acts, no resists, refills instead of dying, HP = weighted median of real builds at the budget",
        "aim": "ranked median hero accuracy and headshot rate, real ability landing and melee rates",
        "heroes": index,
    }, open(os.path.join(OUT, "index.json"), "w"), indent=1)
    orders = glob.glob(os.path.join(ROOT, "work", "jobs_order", "*.json"))
    if orders:   # replace the whole set, so a hero whose order failed this run doesn't keep the old patch's
        os.makedirs(os.path.join(OUT, "order"), exist_ok=True)
        for fn in glob.glob(os.path.join(OUT, "order", "*.json")):
            os.remove(fn)
    for fn in orders:
        r = json.load(open(fn))
        keep = {k: r[k] for k in ("hero_id", "hero", "target_budget", "objectives")}
        json.dump(keep, open(os.path.join(OUT, "order", f"{r['hero_id']}.json"), "w"))
    if rows:
        with open(os.path.join(OUT, "summary.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    print(len(rows), "rows,", len(index), "heroes,", len(orders), "buy orders ->", OUT)


if __name__ == "__main__":
    main()
