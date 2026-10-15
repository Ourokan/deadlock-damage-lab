# Build search (step 3)

For each of the 41 heroes and 5 souls budgets (net worth 10k, 18k, 27k, 37k, 50k), search item builds in the
step 2 combat model (`/mnt/project-files/sim`) against the builds real ranked players have at that net worth, and
rank the builds that win 1v1 duels most often and fastest. Patch 09-29-2026, ranked games 2026-10-07 to 10-13.

## Rank brackets

| Bracket | Opponent builds from (match average rank) | Games | Aim (both sides) |
|---|---|---|---|
| `all` | every ranked game | 7 days | ranked median per hero |
| `low` | Ritualist and below (badge <= 59) | 7 days | 25th percentile |
| `phantom` | Phantom and up (>= 91) | 14 days | 75th percentile |
| `ascendant` | Ascendant and up (>= 101) | 14 days | 90th percentile |
| `eternus` | Eternus and up (>= 111) | 14 days | 90th percentile |
| `eternus5` | Eternus 5 (115, the highest match average in the data; no game averages Eternus 6) | 14 days | 90th percentile |

Rank is the match's average badge (the data has no per-player rank). Aim percentiles are across all ranked
players of the hero, not measured per rank, so they stand in for rank-specific aim; 90th is the top available.
`eternus5` is thin (some heroes have ~11 player rows in 15 days), so its opponent builds are noisy.
Dispel Magic timing against DoTs follows the bracket's lowest badge (`accuracy.dot_cleanse_delay`: Eternus 1.5 s,
Phantom/Ascendant 3 s, lower only below 50% HP), as Tyler set it; real data shows a smaller effect
(`damage/work/decay_vs_dispel_*.json`). Each bracket is a separate search (`search.py --bracket eternus`), so builds can differ by rank.

## Files for the web page (`out/`)

| File | What it holds |
|---|---|
| `index.json` | Budgets, rank brackets, fight settings, and per hero x bracket x budget: best build's win rate and score vs the most popular real build's |
| `heroes/<hero_id>.json` | `brackets.<bracket>.<budget>`: top 10 builds (item ids, cost, score, win rate, loss rate, HP margin, avg time to win, the same on the random pool), the best build's per-opponent matchups and how much score it loses without each item, and the most popular real build with the same stats |
| `items.json` | Item id -> name, slot, tier, cost, active, `effect_modeled` (false = only its always-on stats count) |
| `opponents.json` | Per bracket and budget, the real opponent builds every build was tested against, with weights |
| `summary.csv` | One row per hero x budget with build names, for a quick look in a spreadsheet |

Hero ids match `data/game/heroes.json`; item ids match `data/game/shop_items.json`. Matchup `result` is 1 win,
0.5 timeout, 0 loss; `hp_margin` is my HP% left minus the enemy's (dead = 0).

## Method

- **Opponents** (`scripts/build_pool.py`): every ranked player row of 7 days (~1.2M rows) is cut at the moment
  its held items cost reached the budget's item share (players hold 80-89% of net worth in items, fitted on the
  400 validation matches with real net worth over time). Per budget and hero: one *typical* real build (the
  snapshot made of that hero's most common items) and one *random* real build. Opponents are weighted by how often
  each hero reaches that net worth.
- **Fight**: `deadsim.duel`, 30 s cap, both sides at the hero's ranked median aim, real ability landing and
  melee rates; distance = mean of both heroes' real median engagement distances; same net worth on both sides.
- **Score** per fight: win 1 / timeout 0.5 / loss 0, plus 0.3 x HP margin, plus 0.2 x (1 - time/30) on a win.
  A build's score is the weighted mean over the 41 typical opponents. Win rate and time to win are reported apart.
- **Search** (`scripts/search.py`): start from the hero's most popular real build at that budget. Each round
  measures every candidate item's value added to the current build and every owned item's value removed (on the
  16 most played opponents), proposes 1-for-1, 2-for-1, 1-for-2 and add moves ranked by predicted gain, checks the
  best on the full pool and moves to the best improvement. Up to 8 rounds, stopping when a round gains < 0.004.
  Rules: max 12 items, total cost within the item budget, no item together with its own component.
  Candidate items: 151 tier 1-4 items with a modeled effect or always-on stats (tier 5 legendaries are never
  bought in real ranked games; Ricochet and Split Shot do nothing in a 1v1).
- **Robustness**: the top 10 builds are re-run against the random real build pool. A build that drops a lot there
  was tuned to the typical builds.

`python3 scripts/build_pool.py [bracket]`, then `python3 scripts/search.py --bracket <bracket>`, then
`python3 scripts/export.py` reproduces everything (`search.py` skips finished jobs in `work/jobs/`, so it resumes).

## Read the results with these limits

- **Duels, not matches.** Typical real builds' 1v1 win rates range from ~7% (Rem) to ~92% (Lady Geist) at 27k,
  while real match win rates sit near 50%. Supports and team-fight heroes are weak in a fixed-distance duel.
  Compare builds within a hero (best vs popular), not heroes against each other.
- **Inherited model gaps** (`sim/validation/README.md`): no movement (mobility, slows, gap closers and escape
  items are worth nothing), turrets can't be shot, multi-target items do nothing, every duel starts with all
  cooldowns ready (favours burst, ultimates and Refresher-style items), some items are under-modeled (Torment
  Pulse, Mystic Reverb, Capacitor). Items with `effect_modeled: false` count only their stats.
- **Local search.** The search starts from what players build and moves step by step, so it finds strong builds
  near the popular one, not a proof of the global optimum.
- Ability upgrade order is the most popular real order for the souls (not searched).
- Abrams lands on a melee + spirit build that wins nearly every duel in ~7 s: melee lands at a fixed
  rate with no distance to close, so treat melee-heavy picks as an upper bound.
