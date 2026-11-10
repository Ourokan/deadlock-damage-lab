"""Which ability real players imbue, per hero, from every replay DamageEvent dump on the project share (2026-11-10).

Three imbue items leave their own damage events tied to the imbued ability's hit (scripts/fight_patterns/replay_imbues.py
reads the same markers from fetch_replays.py extracts):
- Quicksilver Reload: its bonus lands on the imbued ability's hit tick (+-2 ticks);
- Mercurial Magnum: its charge hit (40+ damage) lands on that tick too;
- Mystic Reverb: its echo lands DelayDuration (3 s +- 0.6) after a hit on the same victim.
Each proc votes for the hero's own ability that dealt the most damage to the same victim in that window. Prints per
hero and item: the sim's slot, the votes, and each holder's majority. Run 2026-11-10 over 1,830 matches (ally_target,
fight_length, kelvin/sinclair_reverb, nurse_leech, ... dumps; vindicta_snipe's format is skipped):

- Quicksilver: Holliday Powder Keg 19 of 20 holders (sim: Crackshot), Mirage Fire Scarabs 9 / Djinn's Mark 5 of 14
  (sim: Dust Devil), Rat King Rat Swarm 4 of 4 (sim: Scrap Grenade), Violet Living Ink 3 of 3 (sim: Still Life),
  Victor split Aura of Suffering 14 / Pain Battery 9 (left on Pain Battery); every fight_patterns "imbue" row agrees.
- Mercurial Magnum: Holliday Powder Keg 8 of 8, Rat King Rat Swarm 3 of 3, Violet Living Ink 3 of 3, Mirage Djinn's Mark 3.
- Mystic Reverb: Lash Ground Strike 19 of 25 (Quicksilver on Flog), Graves Borrowed Decree 4 of 4, Kelvin Frost Grenade
  51 of 65 (override held out worse, 2026-11-08), Sinclair Vexing Bolt 48 of 51 (fight.IMBUE_OVERRIDE since #285);
  the rest match the sim.
fight.IMBUE_OVERRIDE / IMBUE_SLOT carry Lash, Holliday and Mirage (2026-11-10, with their refits: held-out audit flat or better,
sim_vs_win raw up); Rat King, Violet and Graves lowered sim_vs_win and stay on the usual slot.

usage: python3 -I imbue_slots.py [dump root]   (~7 min over the share)
"""
import collections
import glob
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from deadsim.data import game  # noqa: E402
from deadsim import fight, patterns  # noqa: E402

ROOT = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project-files/analysis/work"
T = 64
G = game()
AB = {ab.id: (h.id, ab.name) for h in G.heroes.values() for ab in h.abilities}
ID = {i.class_name: i.id for i in G.items.values()}
QS, MM, RV = ID["upgrade_quick_silver"], ID["upgrade_ethereal_bullets"], ID["upgrade_mystic_reverb"]
WINDOW = {QS: (-2, 2), MM: (-2, 2), RV: (-3.6 * T, -2.4 * T)}
NAME = {QS: "Quicksilver Reload", MM: "Mercurial Magnum", RV: "Mystic Reverb"}


def read(fn):
    ctl, dm = {}, []
    for line in (gzip.open if fn.endswith(".gz") else open)(fn, "rt"):
        r = json.loads(line)
        if r["k"] == "ctl":
            ctl[r["a"]] = int(str(r.get("s") or "0").split("|")[0])
        elif r["k"] == "dmg" and r.get("s"):
            dm.append((r["tick"], r["a"] // 100000, r["a"] % 100000, int(float(r["s"].split("|")[0])), r["v"]))
    return ctl, sorted(dm)


def main():
    files = {}
    for f in glob.glob(os.path.join(ROOT, "**", "*.ndjson*"), recursive=True):
        mid = os.path.basename(f).split(".")[0]
        if mid.isdigit() and not f.endswith((".tmp", ".part")):
            files.setdefault(mid, []).append(f)
    votes = collections.defaultdict(collections.Counter)                       # (hero, item) -> ability -> procs
    holders = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for mid, fs in sorted(files.items()):
        try:
            ctl, dm = read(max(fs, key=os.path.getsize))
        except (ValueError, KeyError, OSError):
            continue
        seen = collections.defaultdict(collections.Counter)
        for t, a, v, ab, d in dm:
            if ab in AB:
                seen[a][AB[ab][0]] += 1
        hero = {a: ctl.get(a) or c.most_common(1)[0][0] for a, c in seen.items()}
        by = collections.defaultdict(list)
        for x in dm:
            if x[1] != x[2]:
                by[x[1]].append(x)
        for a, ev in by.items():
            h = hero.get(a)
            own = [x for x in ev if x[3] in AB and AB[x[3]][0] == h]
            for t, _, v, ab, d in ev:
                if ab not in WINDOW or (ab == MM and d < 40):
                    continue
                lo, hi = WINDOW[ab]
                c = collections.Counter()
                for t2, _, v2, ab2, d2 in own:
                    if t + lo <= t2 <= t + hi and v2 == v:
                        c[AB[ab2][1]] += d2
                if c:
                    k = c.most_common(1)[0][0]
                    votes[(h, ab)][k] += 1
                    holders[(h, ab)][mid][k] += 1
    for (h, it), c in sorted(votes.items(), key=lambda x: (NAME[x[0][1]], G.heroes[x[0][0]].name)):
        hero = G.heroes[h]
        unl = [True] * len(hero.abilities)
        over = fight.IMBUE_OVERRIDE.get((hero.class_name, next(k for k, v in ID.items() if v == it)))
        idx = next((i for i, ab in enumerate(hero.abilities) if ab.class_name == over), None) if over else None
        if idx is None:
            idx = patterns.imbue_target(hero, unl)
        if idx is None and hero.class_name in fight.IMBUE_SLOT:
            idx = next(i for i, ab in enumerate(hero.abilities) if ab.class_name == fight.IMBUE_SLOT[hero.class_name])
        if idx is None:
            idx = fight._default_imbue_target(hero, unl)
        maj = collections.Counter(m.most_common(1)[0][0] for m in holders[(h, it)].values())
        print(f"{NAME[it]:19s} {hero.name:15s} sim {hero.abilities[idx].name:22s} procs {dict(c.most_common(3))} "
              f"holders {dict(maj.most_common(3))}")


if __name__ == "__main__":
    main()
