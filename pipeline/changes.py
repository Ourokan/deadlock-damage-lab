"""What changed in the recommended builds after each rerun, and why: data/changes.json for the site's "What changed" tab.

    python3 pipeline/changes.py update --tier phantom --reason "forced"   # CI publish step, after the exports
    python3 pipeline/changes.py backfill                                  # rebuild every entry from git history

update compares the results committed at HEAD (the previous run) with the freshly exported ones in the working tree
and puts a new entry at the top. backfill walks the "Rerun searches (<tier>): <reason>" commits on main and diffs
each against the one before it (needs full history: git fetch --unshallow).

An entry holds, for the rerun tier's bracket of damage/out/overall/index.json, every hero and net worth whose best
overall or best raw damage build changed items, or whose number moved 5% or more: items in and out, damage before
dying (overall) or dummy damage by 15 s (raw damage), old and new. Causes come from data/patch.json (new game
patch, hotfix = game values changed, newer player builds), the model changes merged since the last rerun
(first-parent commits touching the sim or the search scripts) and pipeline/rerun_request.json.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data/changes.json")
OVERALL = "damage/out/overall/index.json"
KEEP = 25          # entries kept in data/changes.json
MOVE = 0.05        # a build whose items stayed the same is listed when its number moved this much
RERUN = re.compile(r"Rerun searches \((\w+)\): (.*)")
MODEL_PATHS = ["sim", "damage", "search", "survival", "data/sim", ":!damage/out", ":!search/out", ":!survival/out",
               ":!sim/validation", ":!*.md", ":!sim/tests", ":!*/tests/*"]
CHANGELOG = "https://forums.playdeadlock.com/forums/changelog.10/"


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, check=True).stdout


def at(ref, path):
    """JSON of path at a commit, or in the working tree when ref is None; None when missing."""
    try:
        if ref is None:
            with open(os.path.join(ROOT, path)) as fh:
                return json.load(fh)
        return json.loads(git("show", f"{ref}:{path}"))
    except (OSError, ValueError, subprocess.CalledProcessError):
        return None


def build_rows(old, new, tier):
    """Per hero and net worth: best overall and best raw damage builds that changed between two overall indexes."""
    rows, total = [], 0
    if not old or not new:
        return rows, total
    for hid, h in new.get("heroes", {}).items():
        nb = h.get("brackets", {}).get(tier) or {}
        ob = (old.get("heroes", {}).get(hid) or {}).get("brackets", {}).get(tier) or {}
        for souls, b in nb.items():
            a = ob.get(souls)
            if not a:
                continue
            for kind, key, metric in (("overall", "best", "damage_before_death"), ("damage", "damage_best", "dummy_15s")):
                x, y = a.get(key), b.get(key)
                if not x or not y:
                    continue
                total += 1
                xi, yi = set(x["items"]), set(y["items"])
                o, n = x.get(metric) or 0, y.get(metric) or 0
                moved = o > 0 and abs(n / o - 1) >= MOVE
                if xi == yi and not moved:
                    continue
                rows.append({"hero": int(hid), "name": h.get("name"), "souls": int(souls), "kind": kind,
                             "in": sorted(yi - xi), "out": sorted(xi - yi), "kept": sorted(xi & yi),
                             "old": round(o, 1), "new": round(n, 1)})
    rows.sort(key=lambda r: (r["name"] or "", r["souls"], r["kind"]))
    return rows, total


def patch_link(ref, title):
    for p in at(ref, "data/game/raw/patches.json") or []:
        if p.get("title") == title:
            return p.get("link")
    return CHANGELOG


def model_changes(prev, head):
    """Merged changes to the sim or the searches between two commits: [{"pr", "title"}] (pr None for direct pushes)."""
    if not prev:
        return []
    log = git("log", "--first-parent", "--format=%H%x1f%s%x1f%b%x1e", f"{prev}..{head}", "--", *MODEL_PATHS)
    out = []
    for c in log.split("\x1e"):
        if not c.strip():
            continue
        sha, subject, body = (c.strip("\n").split("\x1f") + ["", ""])[:3]
        if RERUN.match(subject):
            continue
        m = re.match(r"Merge pull request #(\d+)", subject)
        if m:
            title = body.strip().splitlines()[0] if body.strip() else subject
            out.append({"pr": int(m.group(1)), "title": title})
            continue
        if subject.startswith("Merge "):
            continue
        m = re.match(r"(.*) \(#(\d+)\)$", subject)
        out.append({"pr": int(m.group(2)), "title": m.group(1)} if m else {"pr": None, "title": subject, "sha": sha[:7]})
    out.reverse()
    return out


def causes(prev, head, new_ref):
    """Why the results moved, oldest cause first. prev/head are commits; new_ref is the new results (None = tree)."""
    a = (at(prev, "data/patch.json") or {}) if prev else {}
    b = at(new_ref, "data/patch.json") or {}
    out = []
    if b.get("patch") and a.get("patch") != b.get("patch"):
        out.append({"kind": "patch", "text": f"New game patch {b['patch']}", "link": patch_link(new_ref, b["patch"])})
    elif a.get("game_hash") and b.get("game_hash") and a["game_hash"] != b["game_hash"]:
        out.append({"kind": "hotfix", "text": f"Hotfix: game values changed on patch {b.get('patch', '?')}",
                    "link": patch_link(new_ref, b.get("patch"))})
    if b.get("standard") and a.get("standard") and a["standard"] != b["standard"]:
        out.append({"kind": "standard", "text": f"Standard rank changed to {b['standard']}"})
    for m in model_changes(prev, head):
        out.append({"kind": "model", **m})
    if prev:
        ra, rb = at(prev, "pipeline/rerun_request.json") or {}, at(head, "pipeline/rerun_request.json") or {}
        if rb.get("requested_at") and ra.get("requested_at") != rb.get("requested_at") and rb.get("reason"):
            out.append({"kind": "request", "text": rb["reason"]})
    if b.get("builds_through") and a.get("builds_through") and a["builds_through"] != b["builds_through"]:
        out.append({"kind": "builds", "text": f"Real player builds through {b['builds_through']} "
                                              f"(was {a['builds_through']})"})
    return out


def entry(old_ref, new_ref, prev, head, tier, reason, sha=None, date=None):
    """old_ref/new_ref: the results compared (new_ref None = working tree); prev..head: where to look for causes."""
    rows, total = build_rows(at(old_ref, OVERALL) if old_ref else None, at(new_ref, OVERALL), tier)
    p = at(new_ref, "data/patch.json") or {}
    changed = [r for r in rows if r["in"] or r["out"]]
    e = {"date": date or p.get("results_built") or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
         "tier": tier, "reason": reason, "patch": p.get("patch"), "builds_through": p.get("builds_through"),
         "causes": causes(prev, head, new_ref),
         "summary": {"builds": total, "changed": len(changed), "moved": len(rows) - len(changed),
                     "heroes": len({r["hero"] for r in changed})},
         "rows": rows}
    if sha:
        e["sha"] = sha
    return e


def reruns(ref="HEAD"):
    """[(sha, date, tier, reason)] of rerun commits on the first-parent history, oldest first."""
    log = git("log", "--first-parent", "--format=%H%x1f%cI%x1f%s", ref)
    out = []
    for line in log.splitlines():
        sha, date, subject = line.split("\x1f", 2)
        m = RERUN.match(subject)
        if m:
            out.append((sha, date, m.group(1), m.group(2)))
    out.reverse()
    return out


def save(entries):
    with open(OUT, "w") as fh:
        json.dump({"generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                   "entries": entries[:KEEP]}, fh, separators=(",", ":"))
        fh.write("\n")


def update(tier, reason):
    """CI publish step: diff HEAD's committed results (the last run) against the exported ones in the tree."""
    # results: HEAD (what the site shows now) against the tree; causes: everything since the tier's last rerun
    prev = next((r[0] for r in reversed(reruns()) if r[2] == tier), None)
    e = entry("HEAD", None, prev, "HEAD", tier, reason)
    old = at(None, "data/changes.json") or {}
    save([e] + old.get("entries", []))
    s = e["summary"]
    print(f"changes: {s['changed']} of {s['builds']} best builds changed items across {s['heroes']} heroes, "
          f"{s['moved']} more moved {MOVE:.0%}+; {len(e['causes'])} causes")


def backfill():
    runs = reruns()
    entries = []
    for i, (sha, date, tier, reason) in enumerate(runs):
        prev = next((r[0] for r in reversed(runs[:i]) if r[2] == tier), None)
        if prev is None:
            continue   # first run of a tier: nothing to compare with
        built = (at(sha, "data/patch.json") or {}).get("results_built")
        entries.append(entry(prev, sha, prev, sha, tier, reason, sha=sha[:7], date=built or date))
    entries.reverse()
    save(entries)
    print(f"changes: {len(entries)} reruns written to {os.path.relpath(OUT, ROOT)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["update", "backfill"])
    ap.add_argument("--tier", default="phantom")
    ap.add_argument("--reason", default="")
    a = ap.parse_args()
    if a.mode == "update":
        update(a.tier, a.reason)
    else:
        backfill()


if __name__ == "__main__":
    sys.exit(main())
