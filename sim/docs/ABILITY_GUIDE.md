# Writing hero ability models

The combat model lives in `/mnt/project-files/sim/deadsim`. Fights are 1v1, event-driven, at a fixed
distance (default 15 m). Every hero ability needs a small Python class that says what happens when it is
cast (or, for passives, what it does on hits). Abilities without a class fall back to `GenericAbility`
(instant listed damage), which is usually wrong.

## Files to read first
- `deadsim/abilities.py`: the module docstring is the full API (CastCtx helpers, modifier keys).
- `deadsim/heroes/infernus.py`: a complete worked example (skillshot, DoT, bullet build-up passive, ult with fuse + stun).
- `deadsim/engine.py`: `Engine.damage` (damage pipeline), `Fighter` (hp, mods, stat), `Engine.dot`, `Engine.fire`.
- `deadsim/items_fx.py`: more examples of hooks (on_damage_dealt, stat dynamic modifiers, build-ups, barriers).

## Tools
- `python3 tools/show_hero.py "<Hero>"`: every ability's properties, spirit scaling, upgrades and tooltip text.
- `python3 tools/check_hero.py "<Hero>" [--log]`: runs a TTK and a duel at 3 soul levels, prints damage per source
  and which abilities are still on the generic fallback.

## Rules
- One file per hero: `deadsim/heroes/<hero_class_without_hero_prefix>.py` (e.g. `hero_gigawatt` -> `gigawatt.py`).
  Register each ability with `@register("<ability class_name>")`. Model all 4 abilities.
- Only use numbers from the data via `c.val()/c.raw()/c.dur()/c.rng()` (they apply upgrades, spirit scaling,
  duration and range items). Hard-code only what the data lacks, as a named module constant with a comment.
- Upgrades: `c.tier` is how many of T1/T2/T3 are bought; upgrade-only properties are 0 until bought, so
  `c.raw("X")` already returns the right thing. Check `t1_desc/t2_desc/t3_desc` for effects that need code.
- Damage kinds: `spirit_hit` / `dot` (spirit), `gun_volley` / `bullet_hit` (bullet, gets bullet resist and procs),
  `melee_hit`. Pass `ignore_resist=True` only if the game says so (pure damage).
- Set `kind = "skillshot"` for aimed abilities (landing rate = caster's `skill.spirit_accuracy`), "target" for
  lock-on, "aoe"/"self" for others, "passive" for abilities that are never cast. Override `range_props` /
  `in_range` / `should_cast` when the default (cast on cooldown when in range) is wrong, e.g. heals only when hurt,
  executes only below a health threshold, ults only when the target is in reach.
- Movement-only effects (dashes, slows, knockbacks, pulls) have no direct effect in this model; skip the movement
  but keep any damage, resist, stun, silence or disarm they apply. Allies, minions and multi-target bonuses do
  not exist in a 1v1 (count one target).
- Summons, turrets and channels: schedule repeated damage with `c.after(...)`; respect `c.me.alive` and
  `c.foe.alive`; use `c.lock_gun(seconds)` when the hero can't shoot meanwhile.
- Put a module docstring listing each assumption you made. Keep code short and readable.
- Do not edit files outside your hero files. If the engine lacks something you need, approximate it inside your
  file and mention the gap in your report.
- When a modeled number looks off against what you know of the game, prefer the data and note the doubt.

## Upgrades and scaling (since the real-data review)
- `c.val()` applies scale upgrades ("+0.2 spirit scaling" tiers, from `Ability.scale_upgrades`), healing spirit
  scale, boons, light melee and weapon-damage scaling. Never re-implement these in a hero file.
- Helpers: `c.scale(prop)`, `c.light_melee()`, `c.self_damage(amount, kind)`, `c.dot(..., nonlethal=, procs=)`,
  buff key `damage_amp` (caster deals X% more).
- Book damage under the ability's name (or a label starting with it) so `scripts/landing_rates.py --hero` can
  compare it with the real damage matrix. Use that command to sanity-check a hero against real matches.
