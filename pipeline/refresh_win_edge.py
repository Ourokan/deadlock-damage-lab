"""Refresh the real per-hero item win edge (analysis/out/hero_item_edge.json) from the patch rerun's own player builds:
python3 pipeline/refresh_win_edge.py BUILDS_DIR [--work DIR] [--workers 2] [--min-matches N]

The overall search blends these edges into its score (damage/scripts/overall_search.win_value), so after a patch
they have to come from the new patch's games. This reads the day files fetch_builds.py already downloaded for the
rerun (the window in data/patch.json, so no extra Deadlock API queries), counts them with
analysis/scripts/item_win_edge.process (per-day partials cached in --work) and rebuilds the edges with
analysis/scripts/build_win_check.hero_edges. When the window has fewer than --min-matches Ritualist+ matches
(builds not all fetched, a thin API day) the existing file is kept as it is, so the blend falls back to the last
snapshot, whose patch the overall search and the site already flag when it is older than the builds.

MIN_MATCHES: with the 09-29 patch's games, edges from the first 2 days (~11k Ritualist+ matches) agreed in sign
with an independent later week on 99% of the edges the blend uses (r 0.82; 1 day: 98%, r 0.75). The 95% band the
blend requires already drops what a short window can't measure, so fewer days mean fewer edges, not wrong ones.
A new patch waits 3 full days (check_patch.MIN_DAYS), about 17k matches.
"""
import argparse
import datetime
import glob
import gzip
import json
import os
import sys
import time
from multiprocessing import Pool

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "data"))
sys.path.insert(0, os.path.join(ROOT, "analysis", "scripts"))
import patch_state as P  # noqa: E402
import item_win_edge as W  # noqa: E402
import build_win_check as B  # noqa: E402

MIN_MATCHES = 10000


def partials(builds, work, days, workers):
    """Per-day item_win_edge partials for the window's day files in builds (cached in work). Returns their paths."""
    os.makedirs(work, exist_ok=True)
    files = [f for d in days for f in [os.path.join(builds, f"{d}.jsonl.gz")] if os.path.exists(f)]
    out = {f: os.path.join(work, os.path.basename(f) + ".json.gz") for f in files}
    todo = [f for f in files if not os.path.exists(out[f])]
    t0 = time.time()
    if todo:
        with Pool(min(workers, len(todo))) as p:
            for f, res in zip(todo, p.imap(W.process, todo)):
                with gzip.open(out[f] + ".tmp", "wt") as fh:
                    json.dump(res, fh)
                os.replace(out[f] + ".tmp", out[f])
                print(f"{res['file']}: {res['matches']} matches, {time.time() - t0:.0f} s", flush=True)
    return [out[f] for f in files]


def ritualist_matches(paths):
    n = 0
    for p in paths:
        with gzip.open(p, "rt") as fh:
            n += sum(json.load(fh)["matches_by_bracket"][B.MIN_BR:])
    return n


def summary(line):
    print(line)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write(line + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("builds", help="folder of <day>.jsonl.gz player builds (fetch_builds.py)")
    ap.add_argument("--work", default=os.path.join(ROOT, "analysis", "work", "win_edge_rerun"))
    ap.add_argument("--workers", type=int, default=2)   # ~1.8 GB of memory per worker on a busy day
    ap.add_argument("--min-matches", type=int, default=MIN_MATCHES)
    a = ap.parse_args()
    state = P.load()
    days = P.build_days(state)
    paths = partials(a.builds, a.work, days, a.workers)
    n = ritualist_matches(paths)
    try:
        with open(B.EDGE_PATH) as f:
            old = json.load(f)["meta"]
        kept = f"patch {old.get('patch')}, matches through {old.get('matches_through')}"
    except (OSError, ValueError, KeyError):
        kept = "none"
    if n < a.min_matches:
        summary(f"Win edge: kept the last snapshot ({kept}); patch {state['patch']} has {n:,} Ritualist+ matches "
                f"in {len(paths)} of {len(days)} days of builds, {a.min_matches:,} needed.")
        return
    used = [os.path.basename(p).split(".")[0] for p in paths]
    heroes, fit = B.hero_edges(B.load(paths))
    B.write_edges(heroes, B.EDGE_PATH, fit=fit, patch=state["patch"], matches_from=used[0],
                  matches_through=used[-1], matches=n, refreshed=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                  note="refreshed by the patch rerun from its player builds (pipeline/refresh_win_edge.py)")
    summary(f"Win edge: refreshed from {n:,} Ritualist+ matches, {used[0]} to {used[-1]} (patch {state['patch']}); "
            f"was {kept}.")


if __name__ == "__main__":
    main()
