"""Do bullet speed items make real players hit heroes more often? Holders vs non-holders of every item, per-minute
gun rates from the stat timelines: hero bullets hit, shots fired (hit + missed, every target), crits, damage dealt.
Same matching and bands as holder_rates.py; hero hits per shot = hhit ratio / shots ratio
(sim/validation/melee_lifesteal_heal.md: High-Velocity Rounds 0.98-1.00x, no accuracy gain).

usage: python3 -I gun_hit_rates.py fetch [OUT_DIR]       (14 days of Phantom+ matches, ~50 min; bulk metadata, no SQL)
       python3 -I gun_hit_rates.py rates SRC_DIR OUT.json (~10 min)
"""
import glob
import gzip
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import real_rates as R  # noqa: E402

KEYS = ("time_stamp_s", "net_worth", "player_damage", "player_damage_taken", "kills", "deaths", "assists",
        "shots_hit", "shots_missed", "hero_bullets_hit", "hero_bullets_hit_crit", "weapon_power", "creep_damage",
        "neutral_damage", "boss_damage")
M = {"dealt": 2, "hhit": 9, "shit": 7, "smiss": 8, "crit": 10, "creep": 12, "neutral": 13}
BANDS = {10000: (6000, 15000), 18000: (13500, 24300), 27000: (20250, 36450), 37000: (27750, 49950)}


def fetch(out):
    import fetch_rates as F
    F.STAT_KEYS = KEYS
    sys.argv = [sys.argv[0], "--start", "2026-10-11", "--end", "2026-10-25", "--out", out]
    F.main()


def rates(src, dst):
    R.METRICS = tuple(M) + ("shots",)
    items = R.shop_items()
    st = {(b, h): R.Strata() for b in BANDS for h in (0, 1, 2)}
    for p in sorted(glob.glob(os.path.join(src, "*.jsonl.gz"))):
        for line in gzip.open(p, "rt"):
            m = json.loads(line)
            if m.get("mode") not in (None, "Normal", 1):
                continue
            half = m["match_id"] % 2
            for pl in m["players"]:
                ab = pl.get("abandon_s") or 0
                buys = [b for b in pl["items"] if b[0] in items]
                s = pl["stats"]
                for a, b in zip(s, s[1:]):
                    mins = (b[0] - a[0]) / 60
                    if mins < R.MIN_MIN or (ab and ab < b[0]):
                        continue
                    for bb, (lo, hi) in BANDS.items():
                        if lo <= a[1] < hi:
                            held, part = R.held_sets(buys, items, a[0], b[0])
                            v = {k: (b[j] - a[j]) / mins for k, j in M.items()}
                            v["shots"] = v["shit"] + v["smiss"]
                            r = (pl["hero_id"], a[1], a[0], mins, v, held, part)
                            st[(bb, 2)].add(r)
                            st[(bb, half)].add(r)
    out = {}
    for (bb, h), s in st.items():
        t = {}
        for i, c in s.count.items():
            if c < 200:
                continue
            e = s.compare(i)
            if e:
                t[items[i]["name"]] = {"n": e["n"], **{k: [e[k]["ratio"], e[k]["z"], e[k]["base"]] for k in R.METRICS}}
        out[f"{bb}_{h}"] = t
    with open(dst, "w") as fh:
        json.dump(out, fh)


if __name__ == "__main__":
    if sys.argv[1] == "fetch":
        fetch(sys.argv[2] if len(sys.argv) > 2 else "/mnt/project-files/analysis/work/gun_stats")
    else:
        rates(sys.argv[2], sys.argv[3])
