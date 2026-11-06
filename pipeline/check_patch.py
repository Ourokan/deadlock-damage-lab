"""Decide whether the searches need a rerun for a new Deadlock patch: python3 pipeline/check_patch.py [--apply] [--force]

Pulls the current game data and changelog from the Deadlock API and compares them with data/patch.json:
  new patch    a changelog entry dated after the current patch. Waits until MIN_DAYS full UTC days of ranked
               games exist on it, then reruns with player builds from the new patch only.
  hotfix       the game data's gameplay values changed with no new changelog entry. Reruns right away on the
               same patch's builds. A big hotfix (BIG_HOTFIX_ITEMS shop items changed) also sets patch.json
               meta_start to the next day: once that has 3 full days, builds come from after the hotfix only
               (patch_state.window_start), and the 7 and 14 day marks count from it.
  more data    same patch and game data, but the patch now has 7 or 14 full days of games while the results
               used fewer (the duel brackets read 7 or 14 days). Reruns once at each mark.
  standard     the standard rank bracket (search/scripts/build_pool.PRIMARY) differs from the one the results were
               built for (patch.json "standard"). Reruns right away on the same patch's builds.
  requested    pipeline/rerun_request.json is newer than the results (patch.json results_built) and under 2 days
               old: a forced rerun whose waiting run a scheduled check replaced. Reruns on the same patch's builds.
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

REQUEST = os.path.join(ROOT, "pipeline", "rerun_request.json")
MIN_DAYS = 3
MILESTONES = (7, 14)
# A hotfix that changes this many shop items starts a new builds window (patch_state.meta_start). The 10-30 hotfix
# changed 36 (heal nerfs, Decay, Toxic Bullets...) and moved the meta; the 11-05 one changed 1 item and 19 abilities.
BIG_HOTFIX_ITEMS = 10


def latest_patch(patches):
    dated = [(P.patch_date(p.get("title")), p["title"]) for p in patches]
    dated = [x for x in dated if x[0]]
    return max(dated) if dated else (None, None)


def request_in(commit, root=ROOT):
    """Whether the last change to pipeline/rerun_request.json is in commit's history; None when git can't tell
    (shallow checkout, unknown commit)."""
    git = lambda *a: subprocess.run(["git", *a], cwd=root, capture_output=True, text=True)  # noqa: E731
    last = git("log", "-1", "--format=%H", "--", os.path.relpath(REQUEST, root)).stdout.strip()
    if not last or git("cat-file", "-e", f"{commit}^{{commit}}").returncode:
        return None
    r = git("merge-base", "--is-ancestor", last, commit)
    return {0: True, 1: False}.get(r.returncode)


def pending_request(state, now):
    """The reason of a rerun requested (pipeline/rerun_request.json) after the results were built, or None. Under 2
    days old only, so a request whose rerun keeps failing doesn't rerun every 6 hours for good. "After" means not in
    the commit the results were built with (patch.json results_commit): a run publishes ~2 hours after it took its
    code, so a request merged meanwhile is older than results_built but not in the results. Without that commit
    in the history, results_built against requested_at decides."""
    try:
        with open(REQUEST) as f:
            req = json.load(f)
        at = datetime.datetime.fromisoformat(req["requested_at"].replace("Z", "+00:00"))
        built = datetime.datetime.fromisoformat(state["results_built"].replace("Z", "+00:00"))
    except (OSError, ValueError, KeyError):
        return None
    included = request_in(state["results_commit"]) if state.get("results_commit") else None
    if (built < at if included is None else not included) and now - at < datetime.timedelta(days=2):
        return req.get("reason") or "requested"
    return None


def decide(state, game_hash, patches, today, force=False, request=None, changed_items=0):
    """Returns (action, reason, new_state). request: the reason of a rerun requested since the results were built.
    changed_items: how many shop items the new game data changes (patch_state.changed_entries)."""
    yesterday = today - datetime.timedelta(days=1)
    cur_date = P.patch_date(state["patch"])
    new_date, new_title = latest_patch(patches)
    new = dict(state, builds_through=str(yesterday), game_hash=game_hash, standard=PRIMARY)
    if new_date and cur_date and new_date > cur_date:
        start = new_date + datetime.timedelta(days=1)
        have = (yesterday - start).days + 1
        new.update(patch=new_title, patch_start=str(start))
        new.pop("meta_start", None)
        if have >= MIN_DAYS or force:
            return "rerun", f"new patch {new_title}: {max(have, 0)} full days of games since {start}", new
        return "wait", f"new patch {new_title}: {max(have, 0)} of {MIN_DAYS} full days of games so far", state
    used = len(P.build_days(state))
    if game_hash != state["game_hash"]:
        if changed_items >= BIG_HOTFIX_ITEMS:
            new["meta_start"] = str(today + datetime.timedelta(days=1))
            return "rerun", (f"game data changed on patch {state['patch']} (hotfix, {changed_items} items: builds from "
                             f"{new['meta_start']} on once it has {P.META_MIN_DAYS} full days)"), new
        return "rerun", f"game data changed on patch {state['patch']} (hotfix)", new
    start = P.window_start(new)
    if start != P.window_start(state):
        return "rerun", f"builds window now starts {start}, after the hotfix ({(yesterday - start).days + 1} full days)", new
    have = (yesterday - start).days + 1
    if state.get("standard") != PRIMARY:
        return "rerun", f"standard rank bracket is now {PRIMARY} (results built for {state.get('standard', 'all')})", new
    for m in MILESTONES:
        if used < m <= have:
            return "rerun", f"patch {state['patch']} now has {have} full days of games (results used {used})", new
    if force:
        return "rerun", "forced", new
    if request:   # a forced rerun whose waiting run a scheduled check replaced (patch-rerun.yml concurrency)
        return "rerun", f"rerun requested: {request}", new
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
    request = pending_request(state, datetime.datetime.now(datetime.timezone.utc))
    shop = os.path.join(game, "shop_items.json")
    with open(shop) as f:
        items = {P._key(e) for e in json.load(f) if isinstance(e, dict)}
    changed = len([k for k in P.changed_entries(os.path.join(ROOT, "data", "game"), game) if k in items])
    action, reason, new = decide(state, P.game_hash(game), patches, today, a.force, request, changed)
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
