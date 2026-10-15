"""Turn work/jobs/*.json into the files the step 4 web page reads (search/out/).

out/index.json          heroes x budgets summary (best build vs most popular real build)
out/items.json          item id -> name, slot, tier, cost, whether its effect is modeled
out/opponents.json      per budget: the real opponent builds every build was tested against, with weights
out/heroes/<id>.json    per hero, rank bracket and budget: top builds with stats and the best build's matchups
out/summary.csv         one row per hero x budget, for spreadsheets

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
from deadsim import game  # noqa: E402
from deadsim.items_fx import MODELED  # noqa: E402
from build_pool import BUDGETS, BRACKETS, item_budget, suffix  # noqa: E402
import search  # noqa: E402

OUT = os.path.join(ROOT, "out")
BRACKET_LABELS = {"all": "All ranks", "low": "Ritualist and below", "phantom": "Phantom and up",
                  "ascendant": "Ascendant and up", "eternus": "Eternus and up", "eternus5": "Eternus 5 match average"}


def stats(d):
    keep = ("score", "win_rate", "loss_rate", "hp_margin", "avg_win_time_s")
    return {k: d.get(k) for k in keep}


def bracket_jobs(bracket):
    jobs = {}
    for fn in glob.glob(os.path.join(ROOT, "work", "jobs" + suffix(bracket), "*.json")):
        r = json.load(open(fn))
        jobs[(r["hero_id"], r["budget"])] = r
    return jobs


def matchups(d):
    return {oh: {"result": v[0], "hp_margin": v[1], "time_s": v[2]} for oh, v in d["matchups"].items()}


def budget_entry(r):
    builds = []
    for k, x in enumerate(r["builds"]):
        e = {"rank": k + 1, "items": x["items"], "cost": x["cost"], **stats(x["F"]), "random_pool": stats(x["F2"])}
        if k == 0:
            e["matchups"] = matchups(x["F"])
            e["item_removal_loss"] = r["best_item_removal_loss"]
        builds.append(e)
    pop = r["popular"]
    return {
        "item_budget": r["item_budget"], "builds": builds,
        "popular": {"items": pop["items"], "cost": pop["cost"], **stats(pop["F"]), "random_pool": stats(pop["F2"]),
                    "matchups": matchups(pop["F"])},
        "search": {"fights": r["fights"], "seconds": r["seconds"], "candidate_items": r["candidates"]},
    }


def main():
    G = game()
    os.makedirs(os.path.join(OUT, "heroes"), exist_ok=True)
    jobs = {b: bracket_jobs(b) for b in BRACKETS}
    jobs = {b: j for b, j in jobs.items() if j}

    items = {str(i.id): {"name": i.name, "class_name": i.class_name, "slot": i.slot, "tier": i.tier, "cost": i.cost,
                         "active": i.activation != "passive", "effect_modeled": i.class_name in MODELED}
             for i in G.items.values() if i.cost > 0}
    json.dump(items, open(os.path.join(OUT, "items.json"), "w"), indent=0)

    opp = {}
    for br in jobs:
        search.BRACKET = br
        opp[br] = {}
        for b in BUDGETS:
            if not os.path.exists(os.path.join(ROOT, "work", f"snapshots_{b}{suffix(br)}.json")):
                continue
            p = search.load_pools(b)
            opp[br][str(b)] = {
                "typical": [{"hero_id": h, "items": list(it), "weight": round(w, 5)} for h, it, w in p["F"]],
                "random": [{"hero_id": h, "items": list(it), "weight": round(w, 5)} for h, it, w in p["F2"]],
            }
    json.dump(opp, open(os.path.join(OUT, "opponents.json"), "w"))

    index_heroes, rows = [], []
    for hid in sorted(G.heroes):
        h = G.hero(hid)
        per, summary = {}, {}
        for br, bj in jobs.items():
            for b in BUDGETS:
                r = bj.get((hid, b))
                if not r:
                    continue
                e = budget_entry(r)
                per.setdefault(br, {})[str(b)] = e
                best, pop = e["builds"][0], e["popular"]
                summary.setdefault(br, {})[str(b)] = {
                    "best_win_rate": best["win_rate"], "best_score": best["score"],
                    "popular_win_rate": pop["win_rate"], "popular_score": pop["score"]}
                rows.append({"bracket": br, "hero": h.name, "hero_id": hid, "souls": b, "item_budget": r["item_budget"],
                             "best_win_rate": best["win_rate"], "best_avg_win_time_s": best["avg_win_time_s"],
                             "best_random_pool_win_rate": best["random_pool"]["win_rate"],
                             "popular_win_rate": pop["win_rate"],
                             "best_build": " | ".join(G.items[i].name for i in best["items"]),
                             "popular_build": " | ".join(G.items[i].name for i in pop["items"])})
        if not per:
            continue
        json.dump({"hero_id": hid, "hero": h.name, "brackets": per},
                  open(os.path.join(OUT, "heroes", f"{hid}.json"), "w"))
        index_heroes.append({"id": hid, "name": h.name, "brackets": summary})

    index = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "patch": "09-29-2026",
        "budgets": [{"souls": b, "item_budget": item_budget(b)} for b in BUDGETS],
        "brackets": [{"id": br, "min_badge": BRACKETS[br][0], "max_badge": BRACKETS[br][1], "aim_percentile": BRACKETS[br][2],
                      "label": BRACKET_LABELS[br]} for br in jobs],
        "fight": {"type": "1v1 duel", "max_time_s": search.MAX_TIME,
                  "score": "win 1 / timeout 0.5 / loss 0, + 0.3 x HP margin, + 0.2 x speed on wins"},
        "heroes": index_heroes,
    }
    json.dump(index, open(os.path.join(OUT, "index.json"), "w"), indent=1)
    if rows:
        with open(os.path.join(OUT, "summary.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    print({b: len(j) for b, j in jobs.items()}, "jobs ->", len(index_heroes), "heroes in", OUT)


if __name__ == "__main__":
    main()
