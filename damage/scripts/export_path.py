"""Export the full game build paths (work/jobs_path_<bracket>) to out/path/ for the web page.

out/path/index.json                 per rank bracket and hero: path score, stage scores vs popular, start
out/path/heroes/<id>_<bracket>.json the job files as written by game_path.py

Brackets with no local jobs keep what out/path already has (patch reruns run one tier at a time), each with the
patch it was built for; heroes a run didn't finish keep their last result.
"""
import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "..", "data"))
sys.path.insert(0, os.path.join(ROOT, "..", "search", "scripts"))
import patch_state  # noqa: E402
from build_pool import BRACKETS, PRIMARY  # noqa: E402
from game_path import jobs_dir  # noqa: E402
from export_overall import LABELS  # noqa: E402

OUT = os.path.join(ROOT, "out", "path")


def main():
    os.makedirs(os.path.join(OUT, "heroes"), exist_ok=True)
    old = {}
    if os.path.exists(os.path.join(OUT, "index.json")):
        with open(os.path.join(OUT, "index.json")) as f:
            old = json.load(f)
    brackets = {x["id"]: x for x in old.get("brackets", []) if x["id"] in BRACKETS}
    heroes = old.get("heroes", {})
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    patch = patch_state.load()["patch"]
    n = {}
    for br in BRACKETS:
        files = glob.glob(os.path.join(jobs_dir(br), "*.json"))
        if not files:
            continue
        prev_patch = brackets.get(br, {}).get("patch")
        for h in heroes.values():
            if br in h["brackets"]:
                h["brackets"][br].setdefault("patch", prev_patch)
        brackets[br] = {"id": br, "label": LABELS[br], "patch": patch, "generated": now}
        for fn in files:
            with open(fn) as f:
                r = json.load(f)
            e = {"path_score": r["path_score"], "stage_scores": r["stage_scores"], "start": r["start"],
                 "patch": patch}
            heroes.setdefault(str(r["hero_id"]), {"name": r["hero"], "brackets": {}})["brackets"][br] = e
            with open(os.path.join(OUT, "heroes", f"{r['hero_id']}_{br}.json"), "w") as f:
                json.dump(r, f)
        n[br] = len(files)
    order = [b for b in BRACKETS if b in brackets]
    with open(os.path.join(OUT, "index.json"), "w") as f:
        json.dump({"generated": now, "primary": PRIMARY, "brackets": [brackets[b] for b in order], "heroes": heroes}, f)
    print(n, "new paths; brackets out:", order, "->", OUT)


if __name__ == "__main__":
    main()
