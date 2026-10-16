"""Decide whether the searches need a rerun for a new Deadlock patch: python3 pipeline/check_patch.py [--apply] [--force]

Pulls the current game data and changelog from the Deadlock API and compares them with data/patch.json:
  new patch    a changelog entry dated after the current patch. Waits until MIN_DAYS full UTC days of ranked
               games exist on it, then reruns with player builds from the new patch only.
  hotfix       the game data's gameplay values changed with no new changelog entry. Reruns right away on the
               same patch's builds.
  more data    same patch and game data, but the patch now has 7 or 14 full days of games while the results
               used fewer (the duel brackets read 7 or 14 days). Reruns once at each mark.
  standard     the standard rank bracket (search/scripts/build_pool.PRIMARY) differs from the one the results were
               built for (patch.json "standard"). Reruns right away on the same patch's builds.
Prints the decision and, under GitHub Actions, writes action (none|wait|rerun) and reason to $GITHUB_OUTPUT.
--apply (only acted on when the decision is rerun) writes the new game data to data/game and the new window to
data/patch.json. --force reruns even when nothing changed.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "data"))
import patch_state as P  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, "search", "scripts"))
from build_pool import PRIMARY  # noqa: E402

MIN_DAYS = 3
MILESTONES = (7, 14)


def latest_patch(patches):
    dated = [(P.patch_date(p.get("title")), p["title"]) for p in patches]
    dated = [x for x in dated if x[0]]
    return max(dated) if dated else (None, None)


def decide(state, game_hash, patches, today, force=False):
    """Returns (action, reason, new_state)."""
    yesterday = today - datetime.timedelta(days=1)
    cur_date = P.patch_date(state["patch"])
    new_date, new_title = latest_patch(patches)
    new = dict(state, builds_through=str(yesterday), game_hash=game_hash, standard=PRIMARY)
    if new_date and cur_date and new_date > cur_date:
        start = new_date + datetime.timedelta(days=1)
        have = (yesterday - start).days + 1
        new.update(patch=new_title, patch_start=str(start))
        if have >= MIN_DAYS or force:
            return "rerun", f"new patch {new_title}: {max(have, 0)} full days of games since {start}", new
        return "wait", f"new patch {new_title}: {max(have, 0)} of {MIN_DAYS} full days of games so far", state
    have = (yesterday - P.day(state["patch_start"])).days + 1
    used = len(P.build_days(state))
    if game_hash != state["game_hash"]:
        return "rerun", f"game data changed on patch {state['patch']} (hotfix)", new
    if state.get("standard") != PRIMARY:
        return "rerun", f"standard rank bracket is now {PRIMARY} (results built for {state.get('standard', 'all')})", new
    for m in MILESTONES:
        if used < m <= have:
            return "rerun", f"patch {state['patch']} now has {have} full days of games (results used {used})", new
    if force:
        return "rerun", "forced", new
    return "none", f"patch {state['patch']} unchanged, results use {used} days of games", state


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--today", default=None, help="YYYY-MM-DD, for testing (default: today UTC)")
    a = ap.parse_args()
    today = P.day(a.today) if a.today else datetime.datetime.now(datetime.timezone.utc).date()
    state = P.load()
    tmp = tempfile.mkdtemp()
    raw, game = os.path.join(tmp, "raw"), os.path.join(tmp, "game")
    subprocess.run([sys.executable, os.path.join(ROOT, "data/scripts/fetch_game.py"), raw], check=True)
    subprocess.run([sys.executable, os.path.join(ROOT, "data/scripts/normalize_game.py"), raw, game], check=True,
                   stdout=subprocess.DEVNULL)
    with open(os.path.join(raw, "patches.json")) as f:
        patches = json.load(f)
    action, reason, new = decide(state, P.game_hash(game), patches, today, a.force)
    print(f"{action}: {reason}")
    if a.apply and action == "rerun":
        dst = os.path.join(ROOT, "data", "game")
        shutil.rmtree(dst)
        shutil.copytree(game, dst)
        P.save(new)
        print("applied:", json.dumps(new))
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"action={action}\nreason={reason}\n")
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
