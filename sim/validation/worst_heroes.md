# Heroes with the worst win check (2026-11-07)

Question: per hero, how well does the sim's item ranking (sim_vs_win, within slot and tier, post-hotfix pools
10-31..11-05 and shipped edges 10-31..11-05) follow real win edges, which heroes are worst, and why?

Rows: `sim_vs_win.py --budgets 27000,37000 --out` on main after #229 (HEAL_SURVIVAL). Overall within slot and tier
0.392 (27k) / 0.371 (37k).

## Ranking

Lowest (27k / 37k Pearson within slot and tier, ~120 items each):

| Hero | 27k | 37k |
|---|---|---|
| McGinnis | 0.243 | 0.189 |
| Rat King | 0.239 | 0.232 |
| Haze | 0.213 | 0.295 |
| Venator | 0.278 | 0.273 |
| Warden | 0.334 | 0.261 |
| Abrams | 0.298 | 0.305 |

Best: Violet 0.57 / 0.54, Solomon 0.53 / 0.54, Doorman, Nurse, Billy, Viscous ~0.45-0.52. The ranking is not noise:
the same per-hero numbers from edges built on alternate days (independent matches) agree r 0.81.

## What is wrong for the worst heroes

Splitting each row's log score gain into the damage term and the rest: for McGinnis, Haze and Rat King the damage
term doesn't follow the real edges at all (r 0.015 / -0.023 / 0.050 at 27k; other heroes 0.19). Their worst rows
are a few rare items with a large sim damage gain and a negative real edge:

- Haze: Split Shot +4.8 z (real -5.6 pt, se 4.1), Rusted Barrel +2.0 z (real -3.5), Mystic Regeneration, Decay.
- McGinnis: Mystic Shot +2.6 / +3.0 z (real -3.1, se 3.9), Spirit Shielding +2.7 z, Spirit Sap, Cold Front.
- Rat King: Spirit Strike +2.9 / +3.4 z (real -2.5, se 3.3), Healing Rite, Split Shot.

These items are almost never bought on these heroes (Haze or Infernus with Split Shot: about 10 players across
every replay sample we hold), so the replays can't confirm or refute the sim's proc model for them (Split Shot copies
proc Fixation / on-hit items; unverified). Setting all three rows to their tier's mean would move the overall check
only +0.004 / +0.004.

## Tried, not kept

1. **Per-hero damage response.** `sim/scripts/fight_rate/holder_rates_hero.py` (new): holders vs non-holders per hero
   x item (dealt, taken, deaths, kills + assists per minute; same matching as holder_rates.py). Real holders'
   log damage ratio vs the sim's log damage-before-death ratio, within hero: pooled 0.48 (27k) / 0.43 (37k), as
   DAMAGE_ELASTICITY 0.5, but per hero from 0.07 (Haze), ~0.1-0.2 (Vyper, Seven, Victor, Shiv) to 1.5-1.8 (Doorman,
   Nurse, Dynamo), and stable across match-id halves (per-hero slopes r 0.95 / 0.92). Using each hero's slope
   (shrunk) as its elasticity lowers the check at any useful strength (full: -0.036 / -0.045 Pearson; light
   shrinkage only +0.003 Pearson with Spearman down at 37k), on post-hotfix and on independent pre-hotfix
   (09-30..10-24) holder data alike. Real per-hero damage response is real but is not what decides wins.
2. **Per-hero real death ratios** (deaths / kills + assists per hero x item, shrunk to the all-hero ratio in
   death_rate_value): lower at every strength, both data sets (tau 0.03: -0.02 / -0.02).
3. **Shrinking the sim's hero-specific item gains toward the item's mean over heroes.** The hero-specific part of
   the sim gain correlates only 0.15 with the hero-specific part of the edges (raw, unshrunk edges: the sim gain
   shrunk halfway is as good as or better than the full one). Shrinking the log score gain halfway toward the item
   mean: Pearson +0.006 / +0.006 (both day halves up), but Spearman -0.006 / -0.000 at 27k (day half B -0.005). Not
   robust on ranks and not a mechanism; not shipped.

## Spirit Shielding

The second most over-ranked item overall (+2.47 z sim vs +0.37 real, 77 hero x budget rows) and top of McGinnis and
Venator. Its duel barrier is a small part (McGinnis +11.2% score, +10.3% without the barrier; Weapon Shielding +5.3%)
and real holders get the same extra barrier as Weapon Shielding holders (+180 vs +193 per minute). The difference
is the real-holder factors: Spirit Shielding holders die 0.914x per kill + assist (Weapon Shielding 0.954x) and take
0.958x damage, so death_rate_value (^1.5) and focus_value lift it while its win edge is modest. A selection effect in
the all-hero ratios (DEATH_RATE_GAMMA / focus have been tuned on the whole check before), not a hero issue; left as is.

## Conclusion

No change shipped. The worst heroes' gaps are a handful of rare hero x item pairs each, with real edges too noisy
to fit and no replay holders to check the mechanics, plus item-wide gaps (Spirit Shielding, Arctic Blast, Capacitor)
that hit them like every hero. Hero-specific real data (damage response, death ratios) makes the check worse.
