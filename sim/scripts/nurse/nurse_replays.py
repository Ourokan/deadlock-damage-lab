"""Nurse Harrow in Phantom+ replays: leech stacks, leech pickup delay and Wretched Vapors timing (numbers behind
deadsim/heroes/nurse.py).

usage: python3 -I nurse_replays.py fetch <work dir> <replay_damage dir> [n_matches=40]
       python3 -I nurse_replays.py report <work dir> <replay_damage dir> <sample.jsonl.gz>

<replay_damage dir> holds every hero-vs-hero DamageEvent per match (scripts/mechanics/split_shot_replays.py fetch);
matches where someone deals Leech Therapy damage are Nurse matches. fetch saves, per match, the Leech Therapy
ability entity (m_iLeechCount = collected leech stacks, m_flCooldownStart = casts) and Wretched Vapors casts.
report prints:
- leech stacks at Nurse's casts by her net worth (the sample's stats curve; replay ticks start before the clock),
- delay from a Leech Therapy cast to the next stack gain while below the cap (leech pickup),
- Wretched Vapors: hero damage Nurse took in the 3 s before / during the 4 s after each self cast.
"""
import bisect
import collections
import concurrent.futures as cf
import glob
import gzip
import json
import os
import statistics as S
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fight_patterns"))
T = 64.0
LT, WV = "267712790", "3621314027"
SQL = """SELECT 'lt' AS k, tick, CAST("m_hOwnerEntity" AS BIGINT) % 16384 AS a, CAST("m_iLeechCount" AS DOUBLE) AS v, CAST("m_flCooldownStart" AS DOUBLE) AS cd FROM CCitadel_Ability_Nurse_LeechTherapy WHERE delta_type = 'update'
UNION ALL SELECT 'wv' AS k, tick, CAST("m_hOwnerEntity" AS BIGINT) % 16384 AS a, 0.0 AS v, CAST("m_flCooldownStart" AS DOUBLE) AS cd FROM CCitadel_Ability_Nurse_AdrenalineRush WHERE delta_type = 'update'"""


def damage(fn):
    return [e for e in (json.loads(l) for l in gzip.open(fn)) if "s" in e]


def nurse_matches(dmg_dir):
    out = []
    for fn in sorted(glob.glob(os.path.join(dmg_dir, "*.ndjson.gz"))):
        with gzip.open(fn) as f:
            if LT.encode() in f.read():
                out.append(os.path.basename(fn).split(".")[0])
    return out


def fetch(work, dmg_dir, n=40):
    from demo_query import run
    os.makedirs(work, exist_ok=True)
    todo = [m for m in nurse_matches(dmg_dir)[-int(n):] if not os.path.exists(os.path.join(work, m + ".ndjson"))]

    def one(m):
        try:
            run(m, SQL, os.path.join(work, m + ".ndjson"))
            return m, "ok"
        except SystemExit as e:
            return m, str(e)[:120]
    with cf.ThreadPoolExecutor(6) as ex:
        for m, s in ex.map(one, todo):
            print(m, s, flush=True)


def casts(rows, k):
    """{pawn: sorted cast ticks} from m_flCooldownStart changes (the first update tick with a new value)."""
    seen, out = {}, collections.defaultdict(list)
    for r in rows:
        if r["k"] != k or not r["cd"]:
            continue
        if seen.get(r["a"]) != r["cd"]:
            seen[r["a"]] = r["cd"]
            out[r["a"]].append(r["tick"])
    return out


def stacks(rows):
    """{pawn: [(tick, leech count)]} at each change."""
    last, out = {}, collections.defaultdict(list)
    for r in rows:
        if r["k"] == "lt" and last.get(r["a"]) != r["v"]:
            last[r["a"]] = r["v"]
            out[r["a"]].append((r["tick"], r["v"]))
    return out


def at(series, t):
    i = bisect.bisect_right([x[0] for x in series], t)
    return series[i - 1][1] if i else 0.0


def report(work, dmg_dir, sample):
    want = {os.path.basename(f).split(".")[0] for f in glob.glob(os.path.join(work, "*.ndjson"))}
    nw = {}
    for line in gzip.open(sample):
        m = json.loads(line)
        if str(m["match_id"]) in want:
            nw[str(m["match_id"])] = m
    by_nw, delays, wv_rows, maxed = collections.defaultdict(list), [], [], collections.Counter()
    for mid in sorted(want):
        rows = [json.loads(l) for l in open(os.path.join(work, mid + ".ndjson"))]
        if not rows:
            continue
        ev = damage(os.path.join(dmg_dir, mid + ".ndjson.gz"))
        last_tick = max(e["tick"] for e in ev)
        m = nw.get(mid)
        off = max(0.0, last_tick / T - m["duration_s"]) if m else None
        lt_casts, wv_casts, st = casts(rows, "lt"), casts(rows, "wv"), stacks(rows)
        nurse_p = [p for p in (m["players"] if m else []) if p["hero_id"] == 87]
        for pawn, ticks in lt_casts.items():
            ser = st.get(pawn, [])
            curve = None
            if off is not None and len(nurse_p) == 1:
                s = nurse_p[0]["stats"]
                s = json.loads(s) if isinstance(s, str) and s.startswith("[") else s
                if isinstance(s, list):
                    curve = [(x["time_stamp_s"], x["net_worth"]) for x in s]
            for t in ticks:
                n = at(ser, t)
                maxed[n >= 10] += 1
                if curve:
                    g = t / T - off
                    i = bisect.bisect_left([c[0] for c in curve], g)
                    w = curve[min(i, len(curve) - 1)][1]
                    by_nw[min(40, int(w // 5000) * 5)].append(n)
                if n < 9:   # pickups visible below the cap
                    nxt = [x[0] for x in ser if x[0] > t and x[1] > n]
                    if nxt and nxt[0] - t < 30 * T:
                        delays.append((nxt[0] - t) / T)
        for pawn, ticks in wv_casts.items():
            inc = sorted((e["tick"], e["v"]) for e in ev if e["a"] % 100000 == pawn and e["s"] != WV)
            tt = [x[0] for x in inc]
            for t in ticks:
                pre = sum(v for x, v in inc[bisect.bisect_left(tt, t - 3 * T):bisect.bisect_left(tt, t)])
                post = sum(v for x, v in inc[bisect.bisect_left(tt, t):bisect.bisect_left(tt, t + 4 * T)])
                wv_rows.append((pre, post))
    print("leech stacks at Leech Therapy casts by Nurse net worth (k souls: n casts, mean, median):")
    for k in sorted(by_nw):
        v = by_nw[k]
        print(f"  {k:>2}k+  {len(v):4d}  {S.mean(v):5.2f}  {S.median(v):4.1f}")
    print("casts at >= 10 stacks:", dict(maxed))
    if delays:
        print(f"pickup delay after a cast (s, n={len(delays)}): quartiles {[round(q, 1) for q in S.quantiles(delays, n=4)]}")
    if wv_rows:
        pre = [r[0] for r in wv_rows]
        post = [r[1] for r in wv_rows]
        print(f"Wretched Vapors self-relevant casts n={len(wv_rows)}: no hero damage taken in the 3 s before "
              f"{sum(1 for p in pre if p == 0) / len(pre):.2f}; damage before median {S.median(pre):.0f}, "
              f"during next 4 s median {S.median(post):.0f}, mean {S.mean(post):.0f}")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "fetch":
        fetch(*args)
    else:
        report(*args)
