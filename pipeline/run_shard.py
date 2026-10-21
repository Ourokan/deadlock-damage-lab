"""Run one rank tier's searches for one slice of the heroes:
python3 pipeline/run_shard.py --tier phantom --shard I --of N [--workers 4]

Heroes are dealt round-robin into N shards, so N machines can run a tier side by side. Every tier runs the duel
search, the overall search (damage before dying, counterplay on) and the full game build path in its rank bracket. The standard tier
(build_pool.PRIMARY, Phantom and up) also runs the dummy damage search, the item buy order, the ability upgrade order and, for the tank heroes,
the survival search. Tiers and their order: pipeline/tiers.json. Inputs: search/work/snapshots_*.json and item_usage*.json from search/scripts/build_pool.py. Results land
in each search's work/jobs*/ folder as usual. A step that fails is retried hero by hero, so one broken hero
doesn't sink the shard; failures are listed in pipeline/work/shard_<I>.json and the publish step decides.
"""
import argparse
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "search", "scripts"))
from build_pool import BRACKETS, PRIMARY  # noqa: E402


def steps(tier, workers):
    py, w = sys.executable, ["--workers", str(workers)]
    if tier == PRIMARY:
        yield "damage", [py, "damage/scripts/dummy_search.py"] + w
        yield "buy_order", [py, "damage/scripts/buy_order.py"] + w   # needs the 50k damage jobs
        yield "skill_order", [py, "damage/scripts/skill_order.py"] + w   # needs every budget's damage jobs
    yield f"duel_{tier}", [py, "search/scripts/search.py", "--bracket", tier] + w
    if tier == PRIMARY:
        yield "survival", [py, "survival/scripts/survival_search.py", "--only-tanks"] + w
    yield f"overall_{tier}", [py, "damage/scripts/overall_search.py", "--bracket", tier] + w   # needs the damage jobs to export
    yield f"path_{tier}", [py, "damage/scripts/game_path.py", "--bracket", tier] + w   # reads the overall jobs


def run(cmd, heroes, budgets=""):
    extra = ["--budgets", budgets] if budgets else []
    return subprocess.run(cmd + ["--heroes", ",".join(map(str, heroes))] + extra, cwd=ROOT).returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", default=PRIMARY, choices=list(BRACKETS))
    ap.add_argument("--shard", type=int, required=True)
    ap.add_argument("--of", type=int, required=True)
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 4)
    ap.add_argument("--budgets", default="", help="e.g. 10000 for a quick test; default every budget")
    a = ap.parse_args()
    with open(os.path.join(ROOT, "data", "game", "heroes.json")) as f:
        ids = sorted(h["id"] for h in json.load(f))
    mine = ids[a.shard::a.of]
    report = {"tier": a.tier, "shard": a.shard, "heroes": mine, "steps": {}, "failed": {}}
    for name, cmd in steps(a.tier, a.workers):
        t0 = time.time()
        if not run(cmd, mine, a.budgets):
            print(f"{name} failed, retrying hero by hero", flush=True)
            bad = [h for h in mine if not run(cmd, [h], a.budgets)]   # finished jobs are skipped, so only the rest rerun
            if bad:
                report["failed"][name] = bad
        report["steps"][name] = round(time.time() - t0)
        print(f"== {name} done in {report['steps'][name]} s", flush=True)
    os.makedirs(os.path.join(ROOT, "pipeline", "work"), exist_ok=True)
    with open(os.path.join(ROOT, "pipeline", "work", f"shard_{a.tier}_{a.shard}.json"), "w") as f:
        json.dump(report, f, indent=1)
    print(json.dumps(report))


if __name__ == "__main__":
    main()
