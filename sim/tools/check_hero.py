"""Smoke-test a hero's ability models: runs a one-way TTK and a duel at a few soul levels, prints damage by
source and which abilities still use the generic fallback.
usage: python3 tools/check_hero.py <hero name> [--log]"""
import sys
sys.path.insert(0, __file__.rsplit("/tools/", 1)[0])
from deadsim import Loadout, duel, time_to_kill, game
from deadsim.abilities import REGISTRY, load_heroes

load_heroes()
args = [a for a in sys.argv[1:] if not a.startswith("--")]
G = game()
h = G.hero(" ".join(args))
print(f"{h.name}:")
for ab in h.abilities:
    print(f"  {ab.slot} {ab.name:28s} {'modeled: ' + REGISTRY[ab.class_name].__name__ if ab.class_name in REGISTRY else 'GENERIC FALLBACK'}")
dummy_items = ["Extra Health", "Extra Regen", "Bullet Armor" if "bullet armor" in G.items_by_name else "Extra Stamina"]
for souls, items in [(4000, ["Extra Spirit", "Rapid Rounds", "Extra Health"]),
                     (15000, ["Extra Spirit", "Rapid Rounds", "Extra Health", "Mystic Burst", "Swift Striker", "Improved Spirit", "Enduring Speed"]),
                     (35000, ["Boundless Spirit", "Swift Striker", "Fortitude", "Superior Cooldown", "Tesla Bullets", "Spirit Resilience", "Mystic Burst", "Opening Rounds"])]:
    me = Loadout(h.name, items, souls=souls)
    foe = Loadout("Abrams", ["Extra Health", "Extra Regen", "Enduring Speed"][: max(1, souls // 5000)], souls=souls)
    r = time_to_kill(me, foe, distance=12, log="--log" in sys.argv)
    tot = sum(r.a_dmg.values())
    print(f"\n souls {souls}: TTK vs Abrams = {r.time:.2f}s  total {tot:.0f}")
    for k, v in sorted(r.a_dmg.items(), key=lambda x: -x[1]):
        print(f"   {k:30s} {v:7.0f}")
    if "--log" in sys.argv:
        print("\n".join(r.log[:60]))
    d = duel(me, Loadout("Haze", ["Rapid Rounds", "Swift Striker", "Extra Health"], souls=souls), distance=12)
    print("  duel vs Haze:", d.summary())
