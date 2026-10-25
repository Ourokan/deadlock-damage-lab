# deadsim: Deadlock 1v1 fight simulator (step 2)

```python
import sys; sys.path.insert(0, "/mnt/project-files/sim")
from deadsim import Loadout, Skill, duel, time_to_kill, compute_stats
from deadsim.accuracy import hero_default_skill, player_skill, default_distance

me  = Loadout("Haze", ["Rapid Rounds", "Swift Striker", "Toxic Bullets"], souls=15000,
              skill=hero_default_skill("Haze", "p50"))          # ranked median aim + ability landing rates
foe = Loadout("Abrams", ["Extra Health", "Bullet Resilience"], souls=15000)
r = duel(me, foe, distance=default_distance("Haze"), max_time=30)
print(r.summary())                     # winner, time, HP left, damage by source

sk, info = player_skill(<steam account id>, hero="Haze")      # a real player's aim from their recent matches
Skill(accuracy=0.3, headshot=0.2)                               # or manual
hero_default_skill("Abrams", melee_rate_override=0.5, heavy_share=0.4)  # own melee frequency (landed hits/s)
# by default the melee rate follows the build: more melee items -> more melees (data/melee_items.json)
compute_stats("Haze", items, souls=15000)                       # static stats only
from deadsim.mechanics import Mechanics                         # parry, shootable turrets, escape/chase, nearby enemies
r = duel(me, foe, mechanics=Mechanics(extra_targets=0.25))     # on by default (mechanics=None for the old model); r.escaped, r.a_splash, r.b_summon
```

- Team fights (2v2, 3v3): `deadsim/team.py`. `team_fight([Loadout...], [Loadout...], focus="focus"|"spread")` returns
  per-hero damage, damage taken, heals and barriers given to teammates, kills; `team_item_value(a, b, i, item)` is
  what one item on hero i is worth to the whole team. Heals, barriers and auras reach teammates (`HUDDLE` = share in
  range), area abilities also hit other enemies (`AOE_SHARE`), Ricochet/Split Shot bounce to real enemies, movement
  is off. Both shares are assumptions. CLI: `scripts/team_fight.py` (`--support 27000` ranks support items).
- Souls are net worth. Ability unlock order and upgrades default to the most popular real order for that
  soul count (`Loadout(tiers=..., unlocked=...)` to override).
- Code: `deadsim/engine.py` (event loop, damage pipeline), `build.py` (stats), `items_fx.py` (item effects),
  `abilities.py` + `heroes/*.py` (abilities; guide in `docs/ABILITY_GUIDE.md`), `fight.py` (Loadout, duel).
- Trust and known gaps: `validation/README.md`. Tests: `cd sim && python3 -m unittest discover -s tests`.
- Tools: `tools/check_hero.py <hero>`, `tools/show_hero.py <hero>`,
  `scripts/landing_rates.py 100000 1 --hero <hero>` (sim vs real damage mix).
