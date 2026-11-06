"""Refresh fight_rate.json's item tables for the shop items a hotfix changed (2026-11-06, validation/hotfix_rates.md).

The 10-30 hotfix changed 36 shop items (heal nerfs, Decay, Toxic / Crippling, lifesteal...) mid patch. The real holder
ratios (deaths, kills + assists, damage taken, jungle souls: death_rate_value, focus_value, farm_value) were fitted on
09-30..10-24 games. Refitting every item on the 22k post-hotfix Phantom+ matches alone, or on pre + post pooled, lowers
sim_vs_win and fails the match-half check (fewer items clear |z| >= 3, more noise). Replacing only the changed items'
entries with the pooled pre + post fit holds on both match halves (ratios from one half vs edges from the other).

    python3 -I fit_fight_rate.py --src POOLED_DIR --out pooled.json        # pre (fight_rate_ext) + post timelines
    python3 -I hotfix_items.py pooled.json OLD_GAME_DIR [--base sim/data/fight_rate.json] [--out same]

OLD_GAME_DIR: data/game from before the hotfix (git archive <commit> data/game); the changed items are the shop items
patch_state.changed_entries finds between it and data/game. A changed item the pooled fit has no entry for is dropped.
"""
import argparse
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "data"))
import patch_state as P  # noqa: E402

OUT = os.path.join(ROOT, "sim", "data", "fight_rate.json")


def changed_items(old_dir):
    ch = set(P.changed_entries(old_dir))
    with open(os.path.join(ROOT, "data", "game", "shop_items.json")) as f:
        return sorted(i["name"] for i in json.load(f) if i["class_name"] in ch)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pooled")
    ap.add_argument("old_game")
    ap.add_argument("--base", default=OUT)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--label", default="10-30 hotfix")
    a = ap.parse_args()
    with open(a.base) as f:
        base = json.load(f)
    with open(a.pooled) as f:
        pooled = json.load(f)
    names = changed_items(a.old_game)
    for b, t in base["items"].items():
        new = pooled["items"][b]["items"]
        for n in names:
            if n in new:
                t["items"][n] = new[n]
            else:
                t["items"].pop(n, None)
    base["hotfix_items"] = {"hotfix": a.label, "items": names, "pooled_matches": pooled["matches"],
                            "note": "these items' entries come from the pre + post hotfix pooled fit (hotfix_items.py)"}
    with open(a.out, "w") as f:
        json.dump(base, f, indent=1)
    print(len(names), "items:", ", ".join(names))


if __name__ == "__main__":
    main()
