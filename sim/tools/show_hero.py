"""Print a hero's abilities compactly (properties, scaling, upgrades, descriptions) for writing ability models.
usage: python3 tools/show_hero.py <hero name or id>"""
import re
import sys
sys.path.insert(0, __file__.rsplit("/tools/", 1)[0])
from deadsim.data import game

G = game()
h = G.hero(int(sys.argv[1]) if sys.argv[1].isdigit() else " ".join(sys.argv[1:]))
w = h.weapon
print(f"# {h.name} (id {h.id}, {h.class_name})  hp {h.base['max_health']}  gun: {w.get('bullet_damage')} dmg x{w.get('bullets')} pellets, "
      f"cycle {w.get('cycle_time')}s, clip {w.get('clip_size')}, reload {w.get('reload_duration')}s, burst {w.get('burst_shot_count')}")
for ab in h.abilities:
    print(f"\n## [{ab.slot}] {ab.name}  class_name={ab.class_name}  ultimate={ab.ultimate}")
    for k, v in ab.description.items():
        print(f"  {k}: {re.sub(r'<[^>]+>', '', str(v))[:400]}")
    for k, v in ab.props.items():
        if v in (None, 0.0) and k not in ab.scale:
            continue
        sc = ab.scale.get(k)
        s = f"  [{sc[1] or sc[0]} x{sc[2]}]" if sc and (sc[2] or sc[1]) else ""
        print(f"  {k} = {v}{s}")
    for i, u in enumerate(ab.upgrades):
        print(f"  T{i+1} upgrade: {u}")
