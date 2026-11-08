"""Solomon's Setup Bishop hits and Checkmate executes in real replays (2026-11-08).

Reads the DamageEvent dumps of scripts/mechanics/ally_target.py (raw dir: one <match_id>.ndjson.gz per replay,
/mnt/project-files/analysis/work/ally_target/solomon) and each match's spirit power timeline from the API
(fetch_validation.get / slim, cached in <raw dir>/meta.json.gz).

- Bishop hit sizes: each Setup Bishop hit on a hero over the two tooltip formulas at Solomon's spirit power then.
  The hits fall in two groups: ~25% at ImpactDamage (70 + 2.0 x spirit, scale "movedamagesf": the move passing
  through) and ~75% at Damage (25 + 0.85 x spirit, "tiledamagesf": the diagonal squares), 2.95 square hits per
  move hit; no DPS-sized ticks. 92 matches: move hits 2491, square hits 7343.
- Checkmate: for each Develop Queen hit that kills, the victim's health before it (its previous DamageEvent's
  victim_health_new) minus the hit: 113 of 162 kills leave hp the hit didn't take (median 220) = an execute, yet no queen
  hit is execute-sized (kill hit / median queen hit in the cast <= 1.5 in 172 of 173). The execute books no damage.

usage: python3 -I solomon_bishop.py <raw dir>
"""
import bisect
import collections
import glob
import gzip
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

HERO = 85
BISHOP, QUEEN = "4011110259", "1389230689"
IMPACT, TILE = (70.0, 2.0), (25.0, 0.85)


def meta(raw, ids):
    path = os.path.join(raw, "meta.json.gz")
    have = json.load(gzip.open(path, "rt")) if os.path.exists(path) else {}
    miss = [i for i in ids if i not in have]
    if miss:
        import concurrent.futures as cf
        import fetch_validation as F

        def one(i):
            m = F.get(int(i))
            return i, (F.slim(m) if m and m.get("damage_matrix") else None)
        with cf.ThreadPoolExecutor(8) as ex:
            for i, s in ex.map(one, miss):
                if s:
                    have[i] = s
        json.dump(have, gzip.open(path, "wt"))
    return have


def load(path):
    ctl, dm = {}, []
    for line in gzip.open(path):
        r = json.loads(line)
        if r["k"] == "ctl":
            h, _ = (r.get("s") or "0|0").split("|")
            ctl[r["a"]] = int(h)
        elif r["k"] == "dmg":
            s = (r.get("s") or "none||").split("|")
            hp = float(s[1]) if len(s) > 1 and s[1] not in ("", "None") else None
            dm.append((r["tick"], r["a"] // 100000, r["a"] % 100000, s[0], hp, r["v"]))
    return {e for e, h in ctl.items() if h == HERO}, sorted(dm)


def spirit_at(m, g):
    p = [p for p in m["players"] if int(p["hero_id"]) == HERO][0]
    st = p["stats"]
    if isinstance(st, str):
        import ast
        st = ast.literal_eval(st)
    ts = [0] + [s["time_stamp_s"] for s in st]
    sp = [0] + [s["tech_power"] for s in st]
    i = min(bisect.bisect(ts, g), len(ts) - 1)
    return sp[i - 1] + (sp[i] - sp[i - 1]) * max(0.0, min(1.0, (g - ts[i - 1]) / max(1, ts[i] - ts[i - 1])))


def main(raw):
    files = sorted(glob.glob(os.path.join(raw, "*.ndjson.gz")))
    metas = meta(raw, [os.path.basename(f).split(".")[0] for f in files])
    n = collections.Counter()
    dmg = collections.Counter()
    left = []
    for f in files:
        m = metas.get(os.path.basename(f).split(".")[0])
        if not m:
            continue
        sol, dm = load(f)
        t0 = max(x[0] for x in dm) / 64 - m["duration_s"]
        last = {}
        for t, a, v, ab, hp, d in dm:
            if a in sol and v not in sol and ab == BISHOP:
                x = spirit_at(m, t / 64 - t0)
                k = "move" if d / (IMPACT[0] + IMPACT[1] * x) > 0.7 else "square"
                n[k] += 1
                dmg[k] += d
            if a in sol and ab == QUEEN and hp is not None and hp <= 0 and v in last and t - last[v][0] < 3 * 64:
                left.append(last[v][1] - d)
            if hp is not None:
                last[v] = (t, hp)
    print(f"bishop hits: move {n['move']} ({dmg['move']:.0f} dmg), square {n['square']} ({dmg['square']:.0f} dmg), "
          f"square hits per move hit {n['square'] / max(1, n['move']):.2f}")
    ex = [x for x in left if x > 30]
    print(f"queen kills {len(left)}: executes (target kept > 30 hp the hit didn't take) {len(ex)}, "
          f"median hp executed {statistics.median(ex) if ex else 0:.0f}")


if __name__ == "__main__":
    main(sys.argv[1])
