"""How long each search job takes, so pipeline/run_shard.py can spread a tier's jobs evenly over the machines.

python3 pipeline/unit_costs.py update --tier phantom   (publish step: merge the shards' measured job times)
python3 pipeline/unit_costs.py bootstrap               (first table, estimated from the published results)
python3 pipeline/unit_costs.py show [--tier phantom] [--of 16]   (the planned load per machine)

pipeline/unit_costs.json: {tier: {step: {"<hero>_<budget>" or "<hero>": seconds}}}, step one of STEPS. Each rerun's
publish step replaces the times of the jobs it ran and commits the table with the results. A job missing from the
table is estimated from the same step in the standard tier, else the step's median, else DEFAULT. The times only
decide which machine runs which job; they never change a result.
"""
import argparse
import glob
import json
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "pipeline", "unit_costs.json")
sys.path.insert(0, os.path.join(ROOT, "search", "scripts"))
from build_pool import BUDGETS, PRIMARY  # noqa: E402

STEPS = ("damage", "buy_order", "skill_order", "duel", "survival", "overall", "counters", "path")
DEFAULT = {"damage": 120, "buy_order": 15, "skill_order": 60, "duel": 180, "survival": 600, "overall": 200,
           "counters": 100, "path": 900}


def load():
    try:
        with open(PATH) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save(table):
    with open(PATH, "w") as f:
        json.dump(table, f, indent=1, sort_keys=True)
        f.write("\n")


class Costs:
    def __init__(self, tier, table=None):
        self.table = load() if table is None else table
        self.tier = tier
        self._median = {}

    def median(self, step):
        if step not in self._median:
            vals = [v for t in (self.tier, PRIMARY) for v in self.table.get(t, {}).get(step, {}).values()]
            self._median[step] = statistics.median(vals) if vals else DEFAULT[step]
        return self._median[step]

    def __call__(self, step, hero, budget=None):
        key = f"{hero}_{budget}" if budget else str(hero)
        for t in (self.tier, PRIMARY):
            v = self.table.get(t, {}).get(step, {}).get(key)
            if v is not None:
                return v
        return self.median(step)


def update(tier):
    """Merge the job times the tier's shards measured (pipeline/work/shard_<tier>_*.json "units")."""
    table = load()
    row = table.setdefault(tier, {})
    n = 0
    for fn in sorted(glob.glob(os.path.join(ROOT, "pipeline", "work", f"shard_{tier}_*.json"))):
        with open(fn) as f:
            for step, jobs in json.load(f).get("units", {}).items():
                row.setdefault(step, {}).update(jobs)
                n += len(jobs)
    save(table)
    print(f"unit costs: {n} job times for {tier}")


def bootstrap():
    """A first table from what the published results record: the overall and survival searches' job seconds, the
    duel search's fight counts; the other steps scaled from the overall search (ratios from the 2026-10-24 rerun)."""
    ov, sv, du = {}, {}, {}
    for fn in glob.glob(os.path.join(ROOT, "damage", "out", "overall", "heroes", f"*_{PRIMARY}_*.json")):
        with open(fn) as f:
            d = json.load(f)
        if d.get("seconds"):
            ov[f"{d['hero_id']}_{d['budget']}"] = d["seconds"]
    for fn in glob.glob(os.path.join(ROOT, "survival", "out", "heroes", "*.json")):
        with open(fn) as f:
            d = json.load(f)
        h = os.path.basename(fn)[:-5]
        for b, r in d.get("budgets", {}).items():
            if r.get("seconds"):
                sv[f"{h}_{b}"] = r["seconds"]
    for fn in glob.glob(os.path.join(ROOT, "search", "out", "heroes", "*.json")):
        with open(fn) as f:
            d = json.load(f)
        h = os.path.basename(fn)[:-5]
        for b, r in d.get("brackets", {}).get(PRIMARY, {}).items():
            fights = (r.get("search") or {}).get("fights")
            if fights:
                du[f"{h}_{b}"] = round(fights * 0.027, 1)   # ~0.027 s a fight in the 2026-10-24 rerun's logs
    heroes = sorted({k.split("_")[0] for k in ov})
    row = {"overall": ov, "survival": sv, "duel": du,
           "damage": {k: round(0.45 * v, 1) for k, v in ov.items()},
           "counters": {k: round(0.5 * v, 1) for k, v in ov.items() if int(k.split("_")[1]) >= 18000},
           "path": {h: round(0.9 * sum(ov.get(f"{h}_{b}", 0) for b in BUDGETS), 1) for h in heroes},
           "buy_order": {h: 10 for h in heroes}, "skill_order": {h: 60 for h in heroes}}
    save({PRIMARY: row})
    print("unit costs bootstrapped:", {s: len(v) for s, v in row.items()})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["update", "bootstrap", "show"])
    ap.add_argument("--tier", default=PRIMARY)
    ap.add_argument("--of", type=int, default=16)
    a = ap.parse_args()
    if a.cmd == "update":
        update(a.tier)
    elif a.cmd == "bootstrap":
        bootstrap()
    else:
        import run_shard  # noqa: E402  (pipeline/ is on the path when run as a script)
        run_shard.show(a.tier, a.of)


if __name__ == "__main__":
    main()
