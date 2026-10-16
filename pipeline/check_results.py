"""Check a rerun tier is complete enough to publish: python3 pipeline/check_results.py --tier phantom [--min-share 0.95]

Counts the tier's finished search jobs per step (pipeline/run_shard.py steps) against heroes x budgets (10 tank heroes for survival, one per hero for
the buy order), lists the heroes the shards reported as failed, writes a table to $GITHUB_STEP_SUMMARY under GitHub Actions and exits 1 when any
step has less than --min-share of its jobs, so the old results stay up rather than a site with holes.
"""
import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "search", "scripts"))
from build_pool import BRACKETS, BUDGETS, PRIMARY, suffix  # noqa: E402

N_TANKS = 10


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", default=PRIMARY, choices=list(BRACKETS))
    ap.add_argument("--min-share", type=float, default=0.95)
    a = ap.parse_args()
    with open(os.path.join(ROOT, "data", "game", "heroes.json")) as f:
        heroes = {h["id"]: h["name"] for h in json.load(f)}
    # step -> (jobs dir, expected job files): one per hero x budget, except the buy order (one per hero)
    n = len(BUDGETS)
    t = a.tier
    dirs = {}
    if t == PRIMARY:
        dirs = {"damage": ("damage/work/jobs", len(heroes) * n), "buy_order": ("damage/work/jobs_order", len(heroes))}
    dirs[f"duel_{t}"] = ("search/work/jobs" + suffix(t), len(heroes) * n)
    if t == PRIMARY:
        dirs["survival"] = ("survival/work/jobs", N_TANKS * n)
    dirs[f"overall_{t}"] = ("damage/work/jobs_overall_" + t, len(heroes) * n)
    failed = {}
    for fn in glob.glob(os.path.join(ROOT, "pipeline", "work", f"shard_{t}_*.json")):
        with open(fn) as f:
            for step, ids in json.load(f)["failed"].items():
                failed.setdefault(step, []).extend(heroes.get(h, str(h)) for h in ids)
    ok = True
    lines = ["| Step | Jobs done | Expected | Failed heroes |", "|---|---|---|---|"]
    for step, (d, want) in dirs.items():
        done = len(glob.glob(os.path.join(ROOT, d, "*.json")))
        ok &= done >= a.min_share * want
        lines.append(f"| {step} | {done} | {want} | {', '.join(sorted(failed.get(step, []))) or '-'} |")
    lines.append("")
    lines.append("Complete enough to publish." if ok else f"Below {a.min_share:.0%} on some step: not publishing.")
    text = "\n".join(lines)
    print(text)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write(f"## Search results: {t}\n\n" + text + "\n")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
