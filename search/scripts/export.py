"""Turn work/jobs/*.json into the files the step 4 web page reads (search/out/).

out/index.json          heroes x budgets summary (best build vs most popular real build)
out/items.json          item id -> name, slot, tier, cost, whether its effect is modeled
out/opponents.json      per budget: the real opponent builds every build was tested against, with weights
out/heroes/<id>.json    per hero, rank bracket and budget: top builds with stats and the best build's matchups
out/summary.csv         one row per hero x budget, for spreadsheets
out/usage.json          per bracket and budget: how often each hero's players hold each item (>= 3%), the tier
                        caps and the item budget; the site's build maker builds enemy builds at any souls from it

Brackets with no local jobs keep what out/ already has (patch reruns run the brackets one tier at a time and can
switch tiers off: pipeline/tiers.json); each bracket in index.json says which patch and run it was built for.

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
from deadsim.items_fx import MODELED  # noqa: E402
from build_pool import BUDGETS, BRACKETS, item_budget, suffix, tier_caps  # noqa: E402
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


USAGE_MIN = 0.03


def export_usage(G):
    """out/usage.json: item hold rates per bracket, budget and hero, from work/item_usage*.json (build_pool.py).
    Brackets without a local usage file keep what out/usage.json already has."""
    path = os.path.join(OUT, "usage.json")
    out = json.load(open(path)) if os.path.exists(path) else {}
    for br in BRACKETS:
        fn = os.path.join(ROOT, "work", f"item_usage{suffix(br)}.json")
        if not os.path.exists(fn):
            continue
        usage, prev = json.load(open(fn)), out.get(br, {})
        # without the bracket's own work/tier_caps file, keep the caps it last published (tier_caps() would fall
        # back to another bracket's or the hard-coded caps)
        own = os.path.exists(os.path.join(ROOT, "work", f"tier_caps{suffix(br)}.json"))
        caps = tier_caps(br) if own else {}
        cell = dict(prev)   # a budget missing from this run keeps its last published rates
        for b in BUDGETS:
            u = usage.get(str(b))
            if not u:
                continue
            heroes = {}
            for h, row in u.items():
                n = row.get("_n", 0)
                if int(h) not in G.heroes or n <= 0:
                    continue
                heroes[h] = {"n": n, "items": {i: round(c / n, 3) for i, c in sorted(row.items(), key=lambda x: -x[1] if x[0] != "_n" else 0)
                                               if i != "_n" and int(i) in G.items and c / n >= USAGE_MIN}}
            c = {str(t): n for t, n in caps.get(b, {}).items()} if own else prev.get(str(b), {}).get("caps")
            if c is None:
                c = {str(t): n for t, n in tier_caps(br).get(b, {}).items()}
            cell[str(b)] = {"item_budget": item_budget(b), "caps": c, "heroes": heroes}
        out[br] = cell
    if out:
        json.dump(out, open(path, "w"), separators=(",", ":"))
    return list(out)


# properties of an item outside its always-on stats that change nothing in a fight
NO_EFFECT_PROPS = {"AbilityUnitTargetLimit"}


def item_meta(G):
    """out/items.json. effect_modeled: the item has its own effect code (deadsim.items_fx); stats_only: a passive item
    whose only properties are always-on stats, so the stats are the whole item and nothing is missing without
    effect code (Spirit Lifesteal, Extra Health)."""
    def stats_only(i):
        extra = {k for k, v in i.props.items() if v and k not in i.innate}
        return i.activation == "passive" and all(k in NO_EFFECT_PROPS or k.endswith("TooltipOnly") for k in extra)
    return {str(i.id): {"name": i.name, "class_name": i.class_name, "slot": i.slot, "tier": i.tier, "cost": i.cost,
                        "active": i.activation != "passive", "effect_modeled": i.class_name in MODELED,
                        "stats_only": i.class_name not in MODELED and stats_only(i)}
            for i in G.items.values() if i.cost > 0}


def main():
    G = game()
    os.makedirs(os.path.join(OUT, "heroes"), exist_ok=True)
    jobs = {b: bracket_jobs(b) for b in BRACKETS}
    jobs = {b: j for b, j in jobs.items() if j}
    now, patch = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), patch_state.load()["patch"]
    old = {}
    if os.path.exists(os.path.join(OUT, "index.json")):
        old = json.load(open(os.path.join(OUT, "index.json")))
    old_meta = {x["id"]: x for x in old.get("brackets", [])}
    carry = [b for b in BRACKETS if b in old_meta and b not in jobs]
    old_patch = old.get("patch")

    json.dump(item_meta(G), open(os.path.join(OUT, "items.json"), "w"), indent=0)

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
    if carry and os.path.exists(os.path.join(OUT, "opponents.json")):
        prev = json.load(open(os.path.join(OUT, "opponents.json")))
        opp.update({br: prev[br] for br in carry if br in prev})
    json.dump(opp, open(os.path.join(OUT, "opponents.json"), "w"))
    old_summary = {h["id"]: h["brackets"] for h in old.get("heroes", [])}

    index_heroes, rows = [], []
    for hid in sorted(G.heroes):
        h = G.hero(hid)
        per, summary = {}, {}
        for br, bj in jobs.items():
            for b in BUDGETS:
                r = bj.get((hid, b))
                if not r:
                    continue
                e = budget_entry(r) | {"patch": patch}
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
        hero_fn = os.path.join(OUT, "heroes", f"{hid}.json")
        if os.path.exists(hero_fn):
            # brackets not rerun, and cells a rerun didn't finish (check_results.py allows 5% missing), keep their
            # last result, marked with the patch it was built for
            prev = json.load(open(hero_fn))["brackets"]
            for br, cells in prev.items():
                if br not in carry and br not in jobs:
                    continue
                for b, cell in cells.items():
                    if b in per.get(br, {}):
                        continue
                    cell.setdefault("patch", old_meta.get(br, {}).get("patch", old_patch))
                    per.setdefault(br, {})[b] = cell
                    if b in old_summary.get(hid, {}).get(br, {}):
                        summary.setdefault(br, {})[b] = old_summary[hid][br][b]
        if not per:
            continue
        json.dump({"hero_id": hid, "hero": h.name, "brackets": per},
                  open(os.path.join(OUT, "heroes", f"{hid}.json"), "w"))
        index_heroes.append({"id": hid, "name": h.name, "brackets": summary})

    index = {
        "generated": now,
        "patch": patch,
        "budgets": [{"souls": b, "item_budget": item_budget(b)} for b in BUDGETS],
        "brackets": [{"id": br, "min_badge": BRACKETS[br][0], "max_badge": BRACKETS[br][1], "aim_percentile": BRACKETS[br][2],
                      "label": BRACKET_LABELS[br],
                      "patch": patch if br in jobs else old_meta[br].get("patch", old_patch),
                      "generated": now if br in jobs else old_meta[br].get("generated", old.get("generated"))}
                     for br in BRACKETS if br in jobs or br in carry],
        "fight": {"type": "1v1 duel", "max_time_s": search.MAX_TIME,
                  "score": "win 1 / timeout 0.5 / loss 0, + 0.3 x HP margin, + 0.2 x speed on wins"},
        "heroes": index_heroes,
    }
    json.dump(index, open(os.path.join(OUT, "index.json"), "w"), indent=1)
    if carry and os.path.exists(os.path.join(OUT, "summary.csv")):
        with open(os.path.join(OUT, "summary.csv"), newline="") as f:
            rows += [r for r in csv.DictReader(f) if r.get("bracket") in carry]
    if rows:
        with open(os.path.join(OUT, "summary.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    print({b: len(j) for b, j in jobs.items()}, "jobs ->", len(index_heroes), "heroes in", OUT,
          "| usage:", export_usage(G))


if __name__ == "__main__":
    main()
