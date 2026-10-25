"""Keep a rerun's publish from putting files built by older code onto main: python3 pipeline/publish_guard.py --built-at SHA

A rerun takes ~2 hours, and main moves on while it runs: the detect, data and fits jobs run the code of the commit
that started the run (SHA), but the publish step checks out main as it is at the end and lays the run's files over
it. On 2026-10-25 run 67 started before Violet and Baba were added (PRs #79, #81) and its publish put back the
data/game its old normalize_game.py had built, without them. So, run on the publish checkout right after the run's
files are downloaded, this:

  rebuilds data/game from the run's fresh API dump (data/game/raw) with main's data/scripts/normalize_game.py, so
    the game data is the new patch's as main's code reads it (same files when the code didn't change);
  keeps main's copy of each fit or input in GUARDED whose file or producing code main changed since SHA (a PR that
    refit it, or changed the script that writes it, wins over the run's older copy; the waiting rerun the PR
    requested rebuilds it);
  notes in the run summary when model code changed since SHA: the run's results then come from the older model
    until the next rerun.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from changes import MODEL_PATHS  # noqa: E402

GAME = "data/game"
# file or folder the publish commits from a run's artifact -> the code that writes it
GUARDED = {
    "data/builds/aggregates": ["data/scripts/fetch_analytics.py"],
    "analysis/out/hero_item_edge.json": ["pipeline/refresh_win_edge.py", "analysis/scripts/item_win_edge.py",
                                         "analysis/scripts/build_win_check.py"],
    "sim/data/team_value.json": ["sim/scripts/team"],
}


def git(*args, root=ROOT, check=True):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=check)


def rebuild_game(root=ROOT):
    """Rebuild root/data/game from its raw/ dump with root's normalize_game.py. raw/ holds the API files under
    normalize_game.py's output names (assets_ prefix dropped), so they go back under their input names first."""
    raw = os.path.join(root, GAME, "raw")
    tmp = tempfile.mkdtemp()
    try:
        src, out = os.path.join(tmp, "src"), os.path.join(tmp, "game")
        os.makedirs(src)
        for f in os.listdir(raw):
            shutil.copy(os.path.join(raw, f), os.path.join(src, f if f in ("patches.json", "info.json") else "assets_" + f))
        subprocess.run([sys.executable, os.path.join(root, "data/scripts/normalize_game.py"), src, out], check=True,
                       stdout=subprocess.DEVNULL)
        shutil.rmtree(os.path.join(root, GAME))
        shutil.copytree(out, os.path.join(root, GAME))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def changed_since(sha, paths, root=ROOT):
    """Files under paths that commits after sha on HEAD changed, leaving out the reruns' own result commits (an
    earlier tier of this run, or the run before it publishing after this one took its code); None when sha isn't
    in the history (treated as changed)."""
    r = git("log", "--format=", "--name-only", "--invert-grep", "--grep=^Rerun searches (", f"{sha}..HEAD", "--",
            *paths, root=root, check=False)
    return sorted(set(r.stdout.split())) if r.returncode == 0 else None


def keep_newer(sha, root=ROOT, guarded=GUARDED):
    """Put back HEAD's copy of every guarded path whose file or producing code changed since sha. Returns
    {path: reason} for the paths kept."""
    kept = {}
    for path, code in guarded.items():
        ch = changed_since(sha, [path, *code], root)
        if ch == []:
            continue
        if git("cat-file", "-e", f"HEAD:{path}", root=root, check=False).returncode == 0:
            git("checkout", "HEAD", "--", path, root=root)
            git("clean", "-fdq", "--", path, root=root)
        kept[path] = "run's commit not in the history" if ch is None else ", ".join(ch[:3]) + (" ..." if len(ch) > 3 else "")
    return kept


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--built-at", required=True, help="commit the run's code came from (github.sha)")
    a = ap.parse_args()
    head = git("rev-parse", "HEAD").stdout.strip()
    lines = []
    rebuild_game()
    lines.append("- data/game rebuilt from the run's API dump with main's normalize_game.py")
    if head != a.built_at:
        for path, why in keep_newer(a.built_at).items():
            lines.append(f"- kept main's {path}: changed on main since the run started ({why})")
        model = changed_since(a.built_at, MODEL_PATHS)
        if model:
            lines.append(f"- the model changed on main since the run started ({len(model)} files): these results use "
                         f"the model at {a.built_at[:7]} until the next rerun")
    msg = "\n".join(lines)
    print(msg)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write(f"### Publish onto main {head[:7]} (run built at {a.built_at[:7]})\n{msg}\n")


if __name__ == "__main__":
    main()
