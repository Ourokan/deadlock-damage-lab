# Deadlock data (step 1)

Pulled 2026-10-14 from the Deadlock API (api.deadlock-api.com). Current patch: **09-29-2026**, treated as starting 2026-09-30 00:00 UTC (match volume jumps from ~45k to ~70k/day that day).

## Which build source is most accurate

| Source | Reachable here | Freshness | Sample size, current patch | Verdict |
|---|---|---|---|---|
| **Deadlock API** | Yes, free, no key, 200 req/min | Matches up to the last hour (newest ingested match 2026-10-14 14:40 UTC, ~163k matches fetched per day) | ~1.29M matches / 15.4M player rows since 09-30; 3.2M ranked player rows | **Primary source.** Raw per-player final items, purchase times, ability order, win/loss, rank, net worth. |
| Statlocker | Site yes, but almost every data endpoint needs an API key (Steam login + application) | Its own health endpoint reports its Deadlock API feed as "down"; the one free hero stats call returned ~13k Infernus matches (its filter parameters are undocumented, so not a clean comparison) | Much smaller | Secondary. Builds on Deadlock API data (it links the deadlock-api ingest tool). Worth an API key later only for its derived metrics. |
| Mobalytics | Site sits behind a Cloudflare bot challenge; GraphQL API answers but has introspection disabled | Editorial guides, not match data | n/a | Not used. Guides are opinions, not measured builds. |
| deadlock.wiki | Cloudflare challenge (403) | n/a | n/a | Not needed; game files via Deadlock API carry the same numbers. |

**Rate-limit claim:** the article said Valve's tighter limits stopped match tracking after 2 Sept. That is not true for the Deadlock API: daily ranked+unranked match counts are steady at 40-55k/day through September and 60-90k/day since the patch (see `builds/aggregates/hero_stats.json` and the daily counts in the step 1 thread).

## Files

### `game/` — hero, item and ability stats (from the game's files)
- `heroes.json` — 41 released heroes: base stats, per-level gains (`level_up_per_boon`, e.g. bullet damage and spirit power per boon), soul thresholds per level, souls-invested bonuses per item slot (`souls_invested_bonuses`), primary weapon and the 4 signature abilities.
- `weapons.json` — every hero gun: `weapon_info` has bullet damage, cycle time, clip, reload, falloff start/end range and scale, crit (headshot) multiplier, pellets, burst, spread.
- `abilities.json` — 164 hero abilities with every non-default property. Each property's `scale` says what scales it: `scale_function_tech_damage` with `stat_scale` = spirit scaling (damage = base + stat_scale x spirit power), `ETechCooldown`/`ETechDuration`/`ETechRange` = item cooldown/duration/range multipliers. `upgrades` lists the T1/T2/T3 ability-point upgrades.
- `shop_items.json` — 173 shop items: slot, tier, cost, components, active/passive, properties (with `provided_property_type` naming the stat it grants) and enhanced-item upgrades. Tier 5 at 9999 souls are the special legendary items.
- `raw/` — untouched API dumps (heroes, items incl. non-shop and unreleased, modifiers, generic-data, ranks, patches, client versions) in case the normalized files drop something.

### `builds/player_builds/` — real player builds, current patch, ranked only
One gzipped JSONL file per UTC day since 2026-09-30. One line per player per match:
`match_id, account_id, hero_id, won, net_worth, badge (avg match rank, tier*10+subrank), duration_s, level, final_items (item ids held at end), purchases ([item_id, buy_time_s, sold_time_s]), ability_points ([ability_id, time_s])`.
Item and ability ids match `game/*.json` `id`.
Totals: 3.22M player rows from ~233k ranked matches (2026-09-30 to 2026-10-14). `2026-10-14.jsonl.gz` is partial (up to ~15:30 UTC); delete it and re-run `fetch_builds.py` to refresh. The SQL endpoint caps each query at 100k rows, so the script queries 3-hour windows.

**New heroes:** Solomon (released 2026-10-09) and Deadman Danny (id 78, released 2026-10-13) are in all files, including stats, abilities and gun. Danny has only ~13k ranked player rows so far, so his item win rates are noisy. Re-pull his builds after a week.

### `builds/aggregates/` — Deadlock API's own stats, current patch
- `hero_stats.json` — per-hero wins, matches, damage, shots hit/missed, etc. Keys `all` and `oracle_plus` (avg badge >= 81).
- `per_hero/<id>_<class>.json` — for each rank filter: `item_stats` (win rate, pick count, avg buy time per item), `item_stats_by_networth` (same, bucketed per 1000 souls of net worth), `ability_order_stats` (ability point orders with win rates). Plus `published_builds`: the 50 most-favorited in-game builds (guides, not patch-filtered).

### `scripts/`
`normalize_game.py`, `fetch_builds.py`, `fetch_analytics.py` reproduce everything above.

## Notes for step 2 (combat model)
- Player gun stats don't need Statlocker: Deadlock API `match_player` has per-player `stats.shots_hit`, `stats.shots_missed`, `stats.hero_bullets_hit`, `stats.hero_bullets_hit_crit` (headshots) over time, queryable by `account_id`.
- `/v1/sql` on the Deadlock API is marked deprecated in favour of the data lake at data.deadlock-api.com, which this environment cannot reach yet. If SQL is removed, add `data.deadlock-api.com` to the allowed domains.
- `assets.deadlock-api.com` fails through the proxy (502), but the same assets are served at `api.deadlock-api.com/v1/assets/*`, so it isn't needed.
- No Python packages could be installed (pip finds no versions), so the scripts are stdlib only.
