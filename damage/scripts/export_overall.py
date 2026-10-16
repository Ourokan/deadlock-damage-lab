"""Export the overall search (work/jobs_overall) to out/overall/ for the web page, and compare with the dummy damage
builds and the popular builds.

out/overall/index.json        per hero x budget: best vs popular (damage before death, time alive) + the dummy
                              damage search's best 15 s build scored the same way
out/overall/heroes/<id>.json  the job files as written by overall_search.py (top 10 builds, item removal loss...)
out/overall/summary.csv       one row per hero x budget with item names
out/overall/items.md          how often each item is in best overall / best damage / popular builds
"""
import collections
import csv
import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import overall_search as O  # noqa: E402
S = O.S

OUT = os.path.join(ROOT, "out", "overall")


def score_damage_best(args):
    hero, budget = args
    O._phases()
    d = json.load(open(os.path.join(ROOT, "work", "jobs", f"{hero}_{budget}.json")))
    items = d["objectives"]["fight_15s"]["builds"][0]["items"]
    ev = O.Evaluator(hero, budget, S.load_pools(budget))
    r = ev.run(items, "F", detail=True)
    r.pop("matchups")
    return hero, budget, items, r, d["objectives"]["fight_15s"]["builds"][0]["damage"]["fight_15s"], \
        d["popular"]["damage"]["fight_15s"]


def main():
    g = S.G()
    os.makedirs(os.path.join(OUT, "heroes"), exist_ok=True)
    jobs = {}
    for f in os.listdir(O.JOBS):
        if f.endswith(".json"):
            r = json.load(open(os.path.join(O.JOBS, f)))
            jobs[(r["hero_id"], r["budget"])] = r
    with Pool(4) as p:
        dmg = {(h, b): (it, r, d15, p15) for h, b, it, r, d15, p15 in p.map(score_damage_best, sorted(jobs))}
    # dummy 15 s damage of the best overall build
    sys.path.insert(0, HERE)
    import dummy_search as D
    hp_cache = {}
    index, rows = {}, []
    cnt = {k: collections.Counter() for k in ("overall", "damage", "popular")}
    slot = {k: collections.Counter() for k in cnt}
    n_b = collections.Counter()
    for (h, b), r in sorted(jobs.items()):
        best, pop = r["builds"][0], r["popular"]
        if b not in hp_cache:
            hp_cache[b] = D.dummy_hp_for(S.load_pools(b), b)
        best_d15 = D.run_dummy(h, tuple(best["items"]), b, hp_cache[b])[0]["fight_15s"]
        dit, dr, d15, p15 = dmg[(h, b)]
        e = {"best": {k: v for k, v in best["F"].items() if k != "matchups"} | {"items": best["items"],
                                                                               "dummy_15s": round(best_d15, 1)},
             "popular": {k: v for k, v in pop["F"].items() if k != "matchups"} | {"items": pop["items"],
                                                                                 "dummy_15s": p15},
             "damage_best": dr | {"items": dit, "dummy_15s": d15}}
        index.setdefault(str(h), {"name": r["hero"], "budgets": {}})["budgets"][str(b)] = e
        json.dump(r, open(os.path.join(OUT, "heroes", f"{h}_{b}.json"), "w"))
        nm = lambda its: " | ".join(g.items[i].name for i in its)
        rows.append([r["hero"], h, b, e["best"]["damage_before_death"], e["popular"]["damage_before_death"],
                     e["damage_best"]["damage_before_death"], e["best"]["time_alive_s"], e["popular"]["time_alive_s"],
                     e["damage_best"]["time_alive_s"], e["best"]["dummy_15s"], p15, d15,
                     nm(best["items"]), nm(pop["items"]), nm(dit)])
        n_b[b] += 1
        for k, its in (("overall", best["items"]), ("damage", dit), ("popular", pop["items"])):
            for i in its:
                cnt[k][(b, i)] += 1
                slot[k][(b, g.items[i].slot)] += g.items[i].cost
    json.dump({"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "objective":
               "damage dealt before dying vs the 41 typical real builds (enemy fights back, damage x2, never dies), "
               "30 s cap, counterplay on", "heroes": index}, open(os.path.join(OUT, "index.json"), "w"))
    with open(os.path.join(OUT, "summary.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["hero", "hero_id", "souls", "overall_best_dmg_before_death", "popular_dmg_before_death",
                    "damage_best_dmg_before_death", "overall_best_alive_s", "popular_alive_s", "damage_best_alive_s",
                    "overall_best_dummy15", "popular_dummy15", "damage_best_dummy15",
                    "overall_best_build", "popular_build", "damage_best_build"])
        w.writerows(rows)
    lines = ["# Items in best overall vs best damage vs popular builds", "",
             "Count of the 41 heroes whose build holds the item, per budget. Slot spend = mean souls per build.", ""]
    for b in sorted(n_b):
        lines += [f"## {b} net worth", "", "| Item | Overall | Damage (dummy 15 s) | Popular |", "|---|---:|---:|---:|"]
        keys = {i for k in cnt for (bb, i) in cnt[k] if bb == b}
        for i in sorted(keys, key=lambda i: -(cnt["overall"][(b, i)] * 3 + cnt["damage"][(b, i)] + cnt["popular"][(b, i)]))[:25]:
            lines.append(f"| {g.items[i].name} | {cnt['overall'][(b, i)]} | {cnt['damage'][(b, i)]} | {cnt['popular'][(b, i)]} |")
        lines += ["", "| Slot spend | Overall | Damage | Popular |", "|---|---:|---:|---:|"]
        for s_ in ("weapon", "spirit", "vitality"):
            lines.append(f"| {s_} | {slot['overall'][(b, s_)] / n_b[b]:.0f} | {slot['damage'][(b, s_)] / n_b[b]:.0f} | "
                         f"{slot['popular'][(b, s_)] / n_b[b]:.0f} |")
        lines.append("")
    open(os.path.join(OUT, "items.md"), "w").write("\n".join(lines))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
