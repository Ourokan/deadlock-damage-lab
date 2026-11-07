"""Mystic Reverb echoes in Phantom+ replays: per hero, echo count, mean echo and trigger damage, and which of the
hero's abilities hit the same target 2.4-3.6 s before (DelayDuration 3: echo lags peak at 3.0 s).

Real 260 replays (2026-11-06): median echo / trigger damage 0.52-0.70 on every hero (Grey Talon 0.62, Kelvin 0.54),
i.e. about TechDamagePercent 50% of the trigger, with no current-health term (items_fx.MysticReverb).
About 45% of echoes have no own-ability hit on the same hero 3 s before (not explained here).

usage: python3 -I scripts/mechanics/reverb_echoes.py <fetch_fights.py raw dir>
"""
import collections
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts", "fight_length"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from opener_timing import read  # noqa: E402
from deadsim import game  # noqa: E402


def main(raw):
    G = game()
    rev = G.items_by_name["mystic reverb"].id
    abname = {ab.id: (h.name, ab.name) for h in G.heroes.values() for ab in h.abilities}
    trig = collections.defaultdict(collections.Counter)
    size = collections.defaultdict(list)
    echoes = collections.Counter()
    for fn in sorted(glob.glob(os.path.join(raw, "*.ndjson.gz"))):
        hero, ev = read(fn)
        for t, a, v, hp, hmax, dmg, ab in ev:
            if ab != rev or a == v or hero.get(v) is None:
                continue
            h = G.heroes.get(hero.get(a))
            hn = h.name if h else str(hero.get(a))
            echoes[hn] += 1
            by = collections.Counter()
            for t2, a2, v2, _, _, d2, ab2 in ev:
                if a2 == a and v2 == v and t - 3.6 <= t2 <= t - 2.4 and abname.get(ab2, ("?",))[0] == hn:
                    by[abname[ab2][1]] += d2
            if by:
                trig[hn][by.most_common(1)[0][0]] += 1
                size[hn].append((dmg, sum(by.values())))
            else:
                trig[hn]["(none)"] += 1
    for hn in sorted(echoes, key=lambda k: -echoes[k]):
        s = size[hn]
        r = sorted(e / max(1.0, tr) for e, tr in s)
        med = r[len(r) // 2] if r else 0.0
        me = sum(e for e, _ in s) / max(1, len(s))
        mt = sum(tr for _, tr in s) / max(1, len(s))
        print(f"{hn:14s} echoes {echoes[hn]:4d}  mean echo {me:6.0f}  trigger {mt:6.0f}  median echo/trigger {med:.2f}  "
              "trigger: " + ", ".join(f"{k} {n}" for k, n in trig[hn].most_common(4)))


if __name__ == "__main__":
    main(sys.argv[1])
