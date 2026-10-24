# Counter-item buying

How ranked players buy Dispel Magic, Counterspell, Metal Skin, Return Fire and Plated Armor (plus nine other
defensive items for comparison): who buys them, what on the enemy team sets them off, whether buying them wins
more than the alternatives, and what they are worth in the current sim (rerun after every patch with the Phantom+
searches; site tab **Counter items**).

Data: 227,561 ranked matches, 2,730,732 player rows, patch 09-29-2026 (2026-09-30 to 2026-10-14). Teams come
from the `won` flag; the enemy team's items at any moment are rebuilt from purchase and sell times.

## Findings

### Dispel Magic: the counter people buy most, and Decay does trigger it
- 16.9% of players buy it (12.5% at Initiate-Seeker, 22.4% at Ascendant-Eternus), at a median 19 minutes.
  Mina (75% of her players), Shiv, Wraith and Mirage buy it most.
- Enemy items that make a Dispel buy in the next 5 minutes more likely: **Toxic Bullets ×1.40, Slowing Hex
  ×1.30, Decay ×1.22**, Healbane ×1.22, Disarming Hex ×1.14, Silence Wave ×1.12, Knockdown ×1.11. Spirit Burn
  (×1.00) and Mystic Slow (×0.90) don't.
- Enemy heroes (their abilities): **Infernus ×1.52, Shiv ×1.36, Mirage ×1.35, Bebop ×1.25**, the DoT and
  hook/bleed kits. Lady Geist, Victor and Dynamo make it less likely.
- Win edge: +0.7 points over players of the same hero buying a different 3,200-soul vitality item at the same
  time, team lead and own souls position. Small and the same whether the enemy holds many debuffs or few.
- But in real fights Dispel holders still take 85% of their teammates' Decay damage at Phantom+
  (`damage/scripts/decay_vs_dispel.py`, 1500 matches, 2026-10-24 rerun with the right-aligned damage read; the
  first run said 100%): players buy it because of Decay but mostly don't spend it on Decay. Its value comes from cleansing silences and stuns, the heal and the spirit resist.
- Against Infernus it works (2026-10-24, `scripts/cleanse_real.py`): holders take 0.63 of their teammates'
  Afterburn and about 0.6 of their Toxic Bullets (both against the gun damage they take), and die 21% less to
  Infernus. The sim could not purge Afterburn until then; now it does, and Dispel is worth +0.27 extra against
  Infernus at 27k (was -0.03; counter sim of 2026-10-24 after the merge).

### Counterspell: a Vindicta item, set off by Lash
- 8.4% buy it, at a median 22 minutes, and two thirds of Vindicta players do.
- Strongest hero trigger of any counter: **Lash ×2.14** (Death Slam), then Pocket, Grey Talon and Apollo
  (×1.1-1.2). It does not respond to how spirit-heavy the enemy team is (×0.89 high vs low) or to big spirit
  items (Tankbuster ×1.15, Mystic Reverb ×1.07).
- Win edge −0.8 points. In real fights it blocks about nothing (2026-10-24, `scripts/cleanse_real.py`,
  2200 Phantom+ matches): holders take as much Death Slam damage as their teammates (1.00, CI 0.95-1.06) and die
  to Lash as often (1.03); over all enemies their ability damage moves no more than their gun damage (0.97 vs 0.96).
  The sim's spell parry is fitted to that (`sim/validation/counterspell/`), so its low value is real.

### Metal Skin: the most threat-driven buy, and the worst result
- 3.8% buy it, at a median 27 minutes. Hero 88, Silver, Shiv and Billy buy it most.
- Strongest response of any counter: **Haze ×4.2** (Bullet Dance) and Vyper ×1.7; enemy Burst Fire ×2.8,
  Swift Striker ×2.7, Lucky Shot ×2.4, Armor Piercer ×2.1. Buy rate is 2.7× higher against the most gun-heavy
  enemy teams than the least.
- Win edge **−5.7 points**, and negative for almost every buyer hero (Rat King −7.5, Seven −7.0, Drifter −6.2,
  Bebop −5.9), at every purchase time and threat level.
- The sim alone (2026-10-24) rates it well (+0.26 mean matchup gain at 27k) and, like players, most against
  Wraith (+0.70 extra), Haze (+0.43) and Infernus (+0.29). Its overall score is only +0.035 because the overall
  score also multiplies in the real win edge (`overall_search.py` win_value). So players buy it against the right heroes and the sim says it should
  pay; either they use it badly in real fights (it slows you and lasts 5 s), or buyers are being focused in ways a
  team-souls control can't see. The data can't tell these apart.

### Return Fire: rare, and worse the later it's bought
- 1.7% buy it, at a median 17 minutes; Rat King (15%) and Mo & Krill (6%) are most of the buyers.
- Set off by Vyper ×1.7 and Haze ×1.6, and by crit and burst gun items (Lucky Shot, Armor Piercer, Burst Fire,
  each ×1.6-1.7).
- Win edge −3.2 points overall: −2.0 bought at 10-20 min, −7.1 at 30-40, −13.5 at 40-50.
- The sim alone likes it for 1,600 souls (+0.17 mean matchup gain at 27k), most against Wraith, Venator and Rat
  King; with its real win edge blended in, its overall score is +0.02, near the bottom. The reflect is still scaled
  by the holder's own gun accuracy (`items_fx.py` ReturnFire).

### Plated Armor: good in the sim, slightly behind in real games
- 6.4% buy it, at a median 32 minutes; Shiv, Abrams, Rat King and Billy (14-18%).
- Set off by Haze ×1.9, Vyper ×1.6, Wraith ×1.4 and Venator ×1.3; enemy Swift Striker ×2.1, Burst Fire ×1.8,
  Silencer ×1.6, Armor Piercer ×1.6, Siphon Bullets ×1.5.
- Win edge −2.1 points against other 6,400-soul vitality items (that pool includes Witchmail at +1.9 and
  Unstoppable). Smallest gap (−1.1) when the enemy holds the most bullet procs, which is when it should matter.
- Sim (2026-10-24): +0.22 overall at 27k (+0.33 sim alone), and the single biggest counter in the table: +0.76
  extra against Haze and +0.69 against Holliday; per soul it ranks lower because it costs 6,400.

### Across all counters
- Players answer gun threats much more than spirit threats: Metal Skin, Bullet Resilience and Spellbreaker
  respond 2.3-2.8× to their threat, Counterspell not at all.
- Higher ranks buy cleanses more (Dispel 12.5% → 22.4%, Counterspell 6.2% → 9.8%); Bullet Resilience,
  Spellbreaker, Witchmail and Indomitable go the other way.
- The defensive items with a positive real win edge are Witchmail (+1.9), Spirit Resilience (+1.5), Debuff
  Reducer (+1.1), Dispel Magic (+0.7) and Divine Barrier (+0.7). Spirit Resilience is also the best per soul
  in the overall score at 27k (+12.9% per 1k souls), and the sim's best counter to Mina and Grey Talon.
- Sim and players agree on the gun counters: across enemy heroes, the sim's extra value and the real buy trigger
  correlate +0.68 for Plated Armor, +0.61 Bullet Resilience, +0.43 Metal Skin (27k). Since the Dispel fix (#50)
  Dispel agrees too (+0.35; Infernus is a top-3 Dispel target in both). Counterspell (−0.04) and Witchmail (+0.08)
  don't: players buy them against Lash and Victor, and neither real fights nor the sim show a block there.

## Read these with care
- Win edges are observational. They compare players of the same hero who bought a same-tier vitality item in the
  same 5-minute window with the same team item-souls lead and the same souls relative to their own team; being
  focused or out-played isn't captured. Trust the direction more than the size.
- Trigger ratios are pooled over the buyer's hero and the time in the match, so late-game items don't look like
  triggers just because everyone buys more late. Enemy items still travel with enemy heroes (Swift Striker mostly
  on gun heroes), so an item trigger can partly be its owner's kit.
- Sim values (`scripts/sim_counters.py`, since 2026-10-24) add the counter for free on top of each hero's most
  popular Phantom+ build at 18k, 27k, 37k and 50k, scored with the overall test (`damage/scripts/overall_search.py`:
  net damage before dying against every hero's typical build, sustain, movement, parries, range spread,
  targetable summons). Free means every item looks good on a fragile hero: compare items with each other and use
  the *extra vs this enemy* number for counters. Per-enemy numbers are the sim alone; the overall gain also
  multiplies in the item's real per-hero win edge, like the overall build search. The real-match half (triggers, win edges) is from patch 09-29-2026
  and all ranks, and is not rerun automatically (it needs a ~30 min scan of raw player builds).
- About 15% of the rows in `data/builds/player_builds` are exact duplicates (3.22M rows, 2.73M unique); these
  scripts drop them. Win rates elsewhere are unaffected, but row counts are inflated.

## Files
- `out/tables.md`: every table (buy rates, timing, rank, buyer heroes, enemy hero lift, threat response, win
  edges by threat, time and buyer hero). `out/report.json` has the same as data.
- `out/triggers.md` / `triggers.json`: enemy items and heroes that set off each counter, with rate ratios.
- `out/sim.md` / `sim.json`: sim values per item, per enemy hero and per buyer hero at each net worth
  (`scripts/sim_counters.py` → `scripts/export_sim.py`; run by the Phantom+ rerun in `pipeline/run_shard.py`).
- `scripts/analyze.py` → `scripts/report.py`; `scripts/triggers.py` (then `--report`);
  `scripts/sim_counters.py [--heroes Haze --budgets 27000]` then `scripts/export_sim.py`.
