"""Stamp the item heal values the real sustain rates were measured with into sim/data/sustain.json (measured_items).

fit_sustain.py measures each heal item's real rate (farm_heal_hp_per_min, fountain_saved_hp_per_min) on replays of
one patch. overall_search.heal_change scales those rates by the item's heal value now / at that stamp, so a later
balance change (the 10-30 hotfix: Radiant Regeneration 65 -> 40 per cast) moves them without new replays. A refit
of fit_sustain.py drops the stamp (rates then count as measured on the current values): rerun this script after it
with the game data folder of the replays' patch.

usage: python3 sim/scripts/sustain/stamp_heal_values.py [GAME_DIR]   (default: data/game, the current values)
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "damage", "scripts"))
import overall_search as O  # noqa: E402
from deadsim import data as D  # noqa: E402


def main():
    game_dir = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else D.GAME
    D.GAME = game_dir
    g = D.Game()
    by_name = {it.name: it for it in g.items.values()}
    out = {n: O.item_heal_spec(by_name[n]) for n in O.HEAL_VALUE_PROPS if n in by_name}
    with open(O.SUSTAIN_PATH) as f:
        sus = json.load(f)
    sus["measured_items"] = out
    sus["measured_items_game"] = os.path.relpath(game_dir, ROOT) if game_dir.startswith(ROOT) else game_dir
    with open(O.SUSTAIN_PATH, "w") as f:
        json.dump(sus, f, indent=1)
    for n, spec in out.items():
        print(f"{n:22s} {spec}")


if __name__ == "__main__":
    main()
