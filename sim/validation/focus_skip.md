# Colossus and Lifestrike leave the focus cost (2026-11-10)

Items ranked furthest from real wins on main after #288 (all heroes, 27k + 37k, `sim_vs_win.py --movement keep`,
12,188 hero x item pairs). Per-item gap = the item's raw real edge (post-hotfix day files 10-31..11-05, both halves)
minus what its sim gain predicts, sim gain centred within hero, budget, slot and tier.

| Biggest gaps | real raw edge | gap (z) |
|---|---|---|
| Metal Skin, Disarming Hex, Knockdown (sim already low) | -5 to -6 pt | -13 to -19 |
| Spirit Shielding (sim high in tier) | -0.4 | -6.4 |
| Ethereal Shift (sim low in tier) | +1.9 | +7.0 |
| Colossus (sim low in tier) | +2.3 | +6.4 |
| Mystic Reverb, Spirit Burn, Spirit Lifesteal, Cheat Death | +2 to +3.4 | +6 to +9 |

## Fix: Colossus and Lifestrike in FOCUS_SKIP

`focus_value` multiplies the score by the held items' real damage-taken ratios ^ -0.4 (drawing more of the enemy
team's damage loses games). Colossus (1.10x at 27k and 37k, z 20-24) and Lifestrike (1.10x, z 33-46) take the most
of any non-healing item, so both paid ~4%, yet Colossus wins +2.3 pt within vitality T4 and Lifestrike is neutral.
Colossus's active is a resist for standing in and soaking; Lifestrike heals heavy melee back (same handler as Melee
Lifesteal, a healing item). The duel already counts both, as it does for Cheat Death (already skipped).

`sim_vs_win_raw.py` (raw day-half edges, no rare-pick prior):

| split | base | FOCUS_SKIP | (Lifestrike as HEAL_ITEMS instead) |
|---|---|---|---|
| 27k day half A | 0.1534 | 0.1552 (+0.0018; hero halves +0.0013 / +0.0023) | +0.0011 |
| 37k day half A | 0.1463 | 0.1479 (+0.0016; +0.0015 / +0.0018) | +0.0010 |
| 27k day half B | 0.1732 | 0.1745 (+0.0013; +0.0001 / +0.0027) | +0.0006 |
| 37k day half B | 0.1773 | 0.1787 (+0.0014; +0.0002 / +0.0028) | +0.0008 |

Shipped edges (`sim_vs_win_compare.py`): within slot and tier 27k 0.3919 -> 0.3936, 37k 0.3738 -> 0.3754, both
hero halves up. HEAL_ITEMS also halves the duel survival gain (HEAL_SURVIVAL), which costs Lifestrike more than it
gains, so it stays a FOCUS_SKIP item. Taking only the focus cost off other items that take more (Vampiric Burst,
Escalating Resilience, Frenzy) is flat or worse.

## Tried, not kept

- Ethereal Shift out of the movement items (its real deaths / ka ratio 0.95 at 37k counts in death_rate_value
  instead of its 1.007 movement value): -0.0003 .. +0.0004, flat.
- Real damage-dealt factor (score x (holders' real dealt ratio / sim damage ratio ^ 0.5) ^ g; Knockdown holders deal
  0.86x, Disarming Hex 0.88x): g 0.25 -0.003 .. +0.0002, g 0.5 -0.012 .. -0.016.
- Barrier items (Spirit Shielding, Enchanter's Emblem, Divine Barrier, Kevlar) have no shared death / taken pattern
  versus their edges (Kevlar dies less and wins, Divine Barrier dies less and doesn't).

New: `sim_vs_win.py --items NAME,...` scores only those items, for screening a change to a few items (merge into a
full run's rows; rerun the heroes whose popular build holds one of them in full: Lifestrike is in 6 popular builds).
