"""Do Siphon Bullets holders keep max health per kill? (validation/kill_heals.md)

The item data still carries StealPerKill 1 / StackLostPerDeath 2 / MaxStacks 9999 (an old permanent steal per kill),
while the in-game text says the steal is temporary. If kills still gave permanent stacks, a holder's max health
would rise ~2.5% of a victim's max health (~90 HP) per kill since the buy and fall 2 stacks per death.

Stat timelines of post-hotfix Phantom+ matches (fight_rate_post): every player's second-to-last snapshot, max health
regressed on hero (fixed effects), net worth, ability points, the bonus health of the items held, kills / deaths /
assists, and for Siphon holders kills / deaths / assists since the buy. Both match-id halves and pooled.

usage: python3 -I siphon_kill_stacks.py [timeline dir]
"""
import glob
import gzip
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = json.load(open(os.path.join(HERE, "..", "..", "..", "data", "game", "shop_items.json")))
HP = {it["id"]: (it["properties"].get("BonusHealth") or {}).get("value") or 0 for it in ITEMS}
SIPHON = 1282141666
# fetch_rates.py STAT_KEYS: 0 time, 1 net worth, 4 kills, 5 deaths, 6 assists, 7 max health, 20 ability points


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project-files/analysis/work/fight_rate_post"
    rows = []
    for path in sorted(glob.glob(os.path.join(d, "*.jsonl.gz"))):
        for line in gzip.open(path, "rt"):
            m = json.loads(line)
            for p in m["players"]:
                st = p["stats"]
                if len(st) < 4:
                    continue
                s = st[-2]
                held = [it for it in p["items"] if it[1] <= s[0] and (not it[2] or it[2] > s[0])]
                sb = [it for it in held if it[0] == SIPHON]
                k = dd = a = 0
                if sb:
                    s0 = max([x for x in st if x[0] <= sb[0][1]] or [st[0]], key=lambda x: x[0])
                    k, dd, a = s[4] - s0[4], s[5] - s0[5], s[6] - s0[6]
                rows.append((s[7], p["hero_id"], bool(sb), k, dd, a, s[1] / 1000, s[20],
                             sum(HP.get(i, 0) for i in {it[0] for it in held}), s[4], s[5], s[6], m["match_id"] % 2))
    r = np.array(rows, float)
    heroes = sorted(set(r[:, 1]))
    H = np.column_stack([(r[:, 1] == h).astype(float) for h in heroes])
    names = ("held", "kills since buy", "deaths since buy", "assists since buy", "net worth k", "ability points",
             "item bonus health", "kills", "deaths", "assists")
    for half in (None, 0, 1):
        sel = np.ones(len(r), bool) if half is None else r[:, 12] == half
        X = np.column_stack([H, r[:, 2:12]])[sel]
        y = r[sel, 0]
        c, *_ = np.linalg.lstsq(X, y, rcond=None)
        se = np.sqrt(np.diag(np.linalg.pinv(X.T @ X)) * (y - X @ c).var())
        n = len(heroes)
        print(f"{'pooled' if half is None else 'half ' + 'AB'[half]}: {int(r[sel, 2].sum())} holders")
        for i, nm in enumerate(names):
            print(f"  {nm:20s} {c[n + i]:+7.1f} +- {se[n + i]:.1f} HP")


if __name__ == "__main__":
    main()
