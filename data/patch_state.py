"""The patch the committed results were built for (data/patch.json) and helpers shared by the data scripts,
the searches' exports and the patch rerun pipeline (pipeline/).

patch.json fields:
  patch           changelog title of the patch, e.g. "09-29-2026"
  patch_start     first UTC day of player builds counted for it (the day after the patch date)
  meta_start      optional: first UTC day after the patch's last big hotfix (pipeline/check_patch.BIG_HOTFIX_ITEMS).
                  Once it has META_MIN_DAYS full days, the builds window starts there instead of at patch_start
  builds_through  last full UTC day of player builds the results use
  game_hash       fingerprint of data/game (gameplay values only), to spot hotfixes without a changelog
  results_built   when the searches last ran
  results_commit  the commit whose code built them (the rerun's github.sha; main has moved on by the time it publishes)
"""
import datetime
import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "patch.json")
GAME_FILES = ["heroes.json", "abilities.json", "weapons.json", "shop_items.json", "raw/items.json"]
# text and art change without changing the fight; street brawl values belong to another game mode
IGNORED_KEY = re.compile(r"description|desc$|image|icon|street_brawl|lore|localiz|_webp|_png|_svg", re.I)


def load():
    with open(PATH) as f:
        return json.load(f)


def save(state):
    with open(PATH, "w") as f:
        json.dump(state, f, indent=1)
        f.write("\n")


def day(s):
    return datetime.date.fromisoformat(s)


def patch_date(title):
    """'09-29-2026' or '09-16-2026 Update' -> date(2026, 9, 29); None if the title has no date."""
    m = re.match(r"\s*(\d{2})-(\d{2})-(\d{4})", title or "")
    return datetime.date(int(m.group(3)), int(m.group(1)), int(m.group(2))) if m else None


# A big hotfix moves the meta inside a patch: the 10-30 hotfix (heal nerfs, Decay -55%) took Yamato from 28% to
# 77% spirit builds, and edges pooled over the whole patch (10-02..11-04) hid it (heal items' real edge flipped on
# post-hotfix days alone). The window waits for this many full days of post-hotfix games, as a new patch does
# (check_patch.MIN_DAYS), so a hotfix doesn't leave the searches a day of builds.
META_MIN_DAYS = 3


def window_start(state=None):
    """First UTC day of player builds the results use: meta_start once it has META_MIN_DAYS full days, else
    patch_start."""
    s = state or load()
    a, b = day(s["patch_start"]), day(s["builds_through"])
    m = s.get("meta_start")
    if m and day(m) > a and (b - day(m)).days + 1 >= META_MIN_DAYS:
        return day(m)
    return a


def build_days(state=None):
    """The UTC days of player builds the current results use, oldest first."""
    s = state or load()
    a, b = window_start(s), day(s["builds_through"])
    return [a + datetime.timedelta(days=i) for i in range((b - a).days + 1)]


def _strip(x):
    if isinstance(x, dict):
        return {k: _strip(v) for k, v in sorted(x.items()) if not IGNORED_KEY.search(k)}
    if isinstance(x, list):
        return [_strip(v) for v in x]
    return x


def game_hash(game_dir=os.path.join(HERE, "game")):
    h = hashlib.sha256()
    for name in GAME_FILES:
        with open(os.path.join(game_dir, name)) as f:
            h.update(json.dumps(_strip(json.load(f)), sort_keys=True, separators=(",", ":")).encode())
    return h.hexdigest()[:16]


def changed_entries(old_dir, new_dir=os.path.join(HERE, "game")):
    """Names of the heroes, abilities, weapons and shop items whose gameplay values differ between two game data
    folders (normalize_game.py output), for telling a big hotfix from a one-value fix."""
    out = []
    for name in GAME_FILES:
        if name.startswith("raw/"):
            continue
        try:
            with open(os.path.join(old_dir, name)) as f:
                old = json.load(f)
            with open(os.path.join(new_dir, name)) as f:
                new = json.load(f)
        except (OSError, ValueError):
            continue
        entries = old if isinstance(old, list) else list(old.values())
        o = {_key(e): _strip(e) for e in entries if isinstance(e, dict)}
        entries = new if isinstance(new, list) else list(new.values())
        n = {_key(e): _strip(e) for e in entries if isinstance(e, dict)}
        out += [k for k in sorted(set(o) | set(n)) if o.get(k) != n.get(k)]
    return out


def _key(e):
    return str(e.get("class_name") or e.get("id") or e.get("name"))
