"""Export the overall search (work/jobs_overall_<bracket>) to out/overall/ for the web page, and compare with the
dummy damage builds and the popular builds.

out/overall/index.json                  per rank bracket, hero and budget: best vs popular (damage before death, time
                                        alive) + the dummy damage search's best 15 s build scored the same way
out/overall/heroes/<id>_<bracket>_<budget>.json   the job files as written by overall_search.py (top 10 builds...)
out/overall/summary.csv                 one row per bracket x hero x budget with item names
out/overall/items.md                    standard bracket: how often each item is in best overall / damage / popular

Brackets with no local jobs keep what out/overall already has (patch reruns run the brackets one tier at a time and
can switch tiers off: pipeline/tiers.json), each with the patch it was built for.
"""
import collections
import csv
import glob
import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "..", "data"))
import overall_search as O  # noqa: E402
import patch_state  # noqa: E402
from build_pool import BRACKETS, PRIMARY  # noqa: E402
S = O.S

OUT = os.path.join(ROOT, "out", "overall")
LABELS = {"all": "All ranks", "low": "Ritualist and below", "phantom": "Phantom and up",
          "ascendant": "Ascendant and up", "eternus": "Eternus and up", "eternus5": "Eternus 5 match average"}


def load_jobs(bracket):
    jobs = {}
    for fn in glob.glob(os.path.join(O.jobs_dir(bracket), "*.json")):
        r = json.load(open(fn))
        jobs[(r["hero_id"], r["budget"])] = r
    return jobs


def score_damage_best(args):
    """The dummy damage search's best 15 s build (standard bracket) scored with the overall test in this bracket."""
    bracket, hero, budget = args
    fn = os.path.join(ROOT, "work", "jobs", f"{hero}_{budget}.json")
    if not os.path.exists(fn):
        return args, None
    O.set_bracket(bracket)
    O._phases()
    d = json.load(open(fn))
    best = d["objectives"]["fight_15s"]["builds"][0]
    r = O.Evaluator(hero, budget, S.load_pools(budget)).run(best["items"], "F", detail=True)
    r.pop("matchups")
    return args, (best["items"], r, best["damage"]["fight_15s"], d["popular"]["damage"]["fight_15s"])


def main():
    g = S.G()
    os.makedirs(os.path.join(OUT, "heroes"), exist_ok=True)
    jobs = {b: j for b in BRACKETS if (j := load_jobs(b))}
    with Pool(4) as p:
        dmg = dict(p.map(score_damage_best, [(br, h, b) for br, j in jobs.items() for h, b in sorted(j)]))
    import dummy_search as D   # dummy 15 s damage of the best overall build, standard dummy and aim
    hp_cache = {}
    S.BRACKET = PRIMARY

    old = {}
    if os.path.exists(os.path.join(OUT, "index.json")):
        old = json.load(open(os.path.join(OUT, "index.json")))
    brackets = {x["id"]: x for x in old.get("brackets", []) if x["id"] in BRACKETS}
    heroes = {hid: {"name": h["name"], "brackets": {br: v for br, v in h.get("brackets", {}).items() if br in brackets}}
              for hid, h in old.get("heroes", {}).items()}
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    patch = patch_state.load()["patch"]
    for br, bj in jobs.items():
        lo, hi, aim, _ = BRACKETS[br]
        # cells this run didn't finish (check_results.py allows 5% missing) keep their last result, marked with
        # the patch it was built for so the site can say so
        prev_patch = brackets.get(br, {}).get("patch")
        for h in heroes.values():
            for cell in h["brackets"].get(br, {}).values():
                cell.setdefault("patch", prev_patch)
        brackets[br] = {"id": br, "label": LABELS[br], "min_badge": lo, "aim_percentile": aim, "patch": patch,
                        "generated": now}
        for (h, b), r in sorted(bj.items()):
            best, pop = r["builds"][0], r["popular"]
            if b not in hp_cache:
                hp_cache[b] = D.dummy_hp_for(S.load_pools(b), b)
            best_d15 = D.run_dummy(h, tuple(best["items"]), b, hp_cache[b])[0]["fight_15s"]
            e = {"best": {k: v for k, v in best["F"].items() if k != "matchups"} | {"items": best["items"],
                                                                                   "dummy_15s": round(best_d15, 1)},
                 "popular": {k: v for k, v in pop["F"].items() if k != "matchups"} | {"items": pop["items"]},
                 "patch": patch}
            got = dmg.get((br, h, b))
            if got:
                dit, dr, d15, p15 = got
                e["damage_best"] = dr | {"items": dit, "dummy_15s": d15}
                e["popular"]["dummy_15s"] = p15
            heroes.setdefault(str(h), {"name": r["hero"], "brackets": {}})["brackets"].setdefault(br, {})[str(b)] = e
            json.dump(r, open(os.path.join(OUT, "heroes", f"{h}_{br}_{b}.json"), "w"))
    order = [b for b in BRACKETS if b in brackets]
    json.dump({"generated": now, "primary": PRIMARY,
               "objective": "damage dealt before dying vs the 41 typical real builds (enemy fights back, damage x2, "
                            "never dies), 30 s cap, counterplay on",
               "brackets": [brackets[b] for b in order], "heroes": heroes},
              open(os.path.join(OUT, "index.json"), "w"))

    nm = lambda its: " | ".join(g.items[i].name for i in its if i in g.items)
    rows = []
    cnt = {k: collections.Counter() for k in ("overall", "damage", "popular")}
    slot = {k: collections.Counter() for k in cnt}
    n_b = collections.Counter()
    for hid, hh in sorted(heroes.items(), key=lambda x: int(x[0])):
        for br in order:
            for b, e in sorted(hh["brackets"].get(br, {}).items(), key=lambda x: int(x[0])):
                db = e.get("damage_best", {})
                rows.append([br, hh["name"], hid, b, e["best"]["damage_before_death"],
                             e["popular"]["damage_before_death"], db.get("damage_before_death"),
                             e["best"]["time_alive_s"], e["popular"]["time_alive_s"], db.get("time_alive_s"),
                             e["best"]["dummy_15s"], e["popular"].get("dummy_15s"), db.get("dummy_15s"),
                             nm(e["best"]["items"]), nm(e["popular"]["items"]), nm(db.get("items", []))])
                if br != PRIMARY:
                    continue
                n_b[int(b)] += 1
                for k, its in (("overall", e["best"]["items"]), ("damage", db.get("items", [])),
                               ("popular", e["popular"]["items"])):
                    for i in its:
                        if i in g.items:
                            cnt[k][(int(b), i)] += 1
                            slot[k][(int(b), g.items[i].slot)] += g.items[i].cost
    with open(os.path.join(OUT, "summary.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["bracket", "hero", "hero_id", "souls", "overall_best_dmg_before_death", "popular_dmg_before_death",
                    "damage_best_dmg_before_death", "overall_best_alive_s", "popular_alive_s", "damage_best_alive_s",
                    "overall_best_dummy15", "popular_dummy15", "damage_best_dummy15",
                    "overall_best_build", "popular_build", "damage_best_build"])
        w.writerows(rows)
    lines = [f"# Items in best overall vs best damage vs popular builds ({LABELS[PRIMARY]})", "",
             "Count of heroes whose build holds the item, per budget. Slot spend = mean souls per build.", ""]
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
    print({b: len(j) for b, j in jobs.items()}, "new jobs; brackets out:", order, "->", OUT)


if __name__ == "__main__":
    main()
