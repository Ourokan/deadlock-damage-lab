# Return Fire, Arctic Blast and the landing cap (2026-10-27)

## The cap

`accuracy.item_landing` leaves items real players get more from (pooled landing >= 1) uncut, but `fight.py` still
multiplies their `length_corr`. For front-loaded actives the correction is well under 1 (the sim books their damage
later in a fight than real players deal it), so they landed only `length_corr` of their fitted level: damage audit
per holder (total norm) Arctic Blast real/sim 1.42, Lightning Scroll 1.46, Quicksilver Reload 1.25, Headshot Booster
1.16, Phantom Strike 1.14.

`accuracy.CAP_AFTER_LENGTH` (on): for an uncut item with `length_corr < 1`, the factor is `min(1, landing x
length_corr)`. Corrections above 1 (Spirit Burn 1.53, Rebuttal 1.31, Tankbuster 1.05) are kept as they were; the
first try of this fix (thread "Fix the next hero damage gap") also cut those to 1, which is part of why it lost
sim_vs_win. Then the lifted items' pooled landing refit to the audit (`item_landing_heroes.py --item X --pooled`,
which now fits lifted rows on `min(1, landing x length_corr)` and lets the landing sit above 1):

| | main | lift | lift + refit |
|---|---|---|---|
| Arctic Blast real/sim (172 holders) | 1.42 | 1.00 | 1.00 |
| Phantom Strike (125) | 1.14 | 0.79 | 0.96 |
| Lightning Scroll (49) | 1.46 | 1.22 | 1.18 |
| Quicksilver Reload (1114) | 1.25 | 1.13 | 1.07 |
| Headshot Booster (375) | 1.16 | 1.07 | 1.03 |
| items, holder-weighted mean abs log real/sim | 0.0966 | 0.0828 | 0.0769 |
| hero mix distance (player-weighted) | 0.0182 | 0.0186 | 0.0186 |

Per-hero rows (`item_landing.json` "heroes") multiply the same corrected factor, so the lifted items' hero rows were
refit too (`item_landing_heroes.py --item X`, from the audit after the pooled refit): six Quicksilver rows had been
fit on the old 0.855 and read ~15% over (Wraith 0.86, Mina 0.90); holder-weighted |log real/sim| over the lifted
items' hero rows 0.210 (main) -> 0.171 (pooled refit) -> 0.116, pooled item gap 0.080, mix 0.0186.

Split-half (match id parity; refit from one half's audit, audit the other): those five items' held-out gap
0.143 -> 0.099 (odd half) and 0.086 -> 0.044 (even half); mix flat both halves. The hero mix moves +0.0004, mostly
Calico (0.035 -> 0.042): her whole-match mix already has items over (0.33 vs 0.31, mid-game bias of the 30/60/90%
duels), while her Arctic Blast holders-only row is now on (1.50 -> ~1.0).

## Return Fire

Not lifted (`accuracy.LENGTH_CAP_SKIP`). What the data says:

- 260 Phantom+ replays (fight_length raw), 338 Return Fire activations: 278 reflected damage per activation, onto
  1.9 heroes (72% on the top one), from 2.2 attackers who dealt 1144 to the holder in the 6.5 s. Reflected damage to
  an attacker = 0.81 x (65% of their bullet + 25% of their spirit damage): it lands without aim. The sim multiplies
  it by the holder's gun accuracy (`items_fx.ReturnFire`), which is most of the audit's 3.1x.
- The overall score gives Return Fire ~2% of a holder's fight damage (Abrams, Rat King, Seven, Yamato at 27k) vs
  real holders' 9.4%; lifted it would be ~3%. Its damage is not over-valued: under.
- Real holders vs matched non-holders (holder_rates.py on fight_rate_ext, 27k band, 10.8k holder-minutes): damage
  dealt 1.058, taken 1.034, deaths 1.076, kills + assists 0.995, souls 0.980. Same at 37k. They deal the reflected
  damage, die more and get nothing for it; the real win edge is -5.5 pt on every hero (Rat King -2.5, its main buyer:
  41 of 96 audit holders).
- The score already counts the deaths (death_rate_value: Abrams 1.017 -> 0.991 with it) and a 0.54 kill weight.

Lifting it doubles its score; sim_vs_win (27k, blend off, all heroes): main all 0.219 / within slot and tier 0.258 /
damage items 0.114 / per item 0.307; lift on every item 0.211 / 0.248 / 0.077 / 0.297; this change (lift without
Return Fire, lifted items refit pooled and per hero) 0.217 / 0.258 / 0.109 / 0.308. So the conflict the first try found is
Return Fire's alone: real damage that comes with being focused and doesn't win. Fixing the accuracy term would make
its damage truer and the score worse in the same way; both wait for a score that can price damage taken to deal it.
Script for the replay numbers: `sim/scripts/mechanics/return_fire_replays.py`.
