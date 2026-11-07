"""Ivy's Kudzu Connection: how often a real Ivy has an ally to connect to (Mechanics.kudzu_connect, 2026-11-07).

Kudzu Connection gives Ivy its full fire rate and bullet lifesteal while connected to an ally within its 16 m cast
range, 50% with no connection; the replay's ability entity carries no tether target (m_hTarget is always empty) and no
pawn state bit turns on at the cast, so this measures the chance instead: the share of Ivy's combat seconds (seconds
she dealt or took hero damage) with a living ally within R m, from pawn positions every 0.5 s.

fetch: python3 -I ivy_kudzu.py fetch <work dir> <ids file> [n=160] [workers=6]   (Deadlock API demo queries, ~20 s
       each; recent matches only, older demos 404)
report: python3 -I ivy_kudzu.py report <work dir>
First run (75 post-hotfix Phantom+ Ivy matches from validation fresh_2026-11-06 sample): ally within 16 m 0.44 of
combat seconds (0.46 / 0.37 / 0.43 / 0.46 / 0.49 by fifth of the match), 0.51 inside a Kudzu window, 0.48 at the cast.
"""
import collections
import concurrent.futures as cf
import gzip
import json
import os
import sys
import bisect

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fight_patterns"))

SQL = """SELECT 'dmg' AS k, CAST(entindex_attacker AS BIGINT) * 100000 + CAST(entindex_victim AS BIGINT) AS a, CAST(ability_id AS VARCHAR) || '|' || CAST(victim_health_new AS VARCHAR) || '|' || CAST(victim_health_max AS VARCHAR) AS s, CAST(damage AS DOUBLE) AS v, tick FROM DamageEvent WHERE attacker_class = 1 AND victim_class = 1 AND damage > 0
UNION ALL
SELECT 'ctl' AS k, CAST(max("m_hHeroPawn") AS BIGINT) % 16384 AS a, CAST(max("m_PlayerDataGlobal__m_nHeroID") AS VARCHAR) || '|' || CAST(max("m_iTeamNum") AS VARCHAR) AS s, 0.0 AS v, min(tick) AS tick FROM CCitadelPlayerController GROUP BY entity_index
UNION ALL
SELECT 'pos' AS k, CAST(entity_index AS BIGINT) AS a, CAST("CBodyComponent__m_cellX" AS VARCHAR) || '|' || CAST("CBodyComponent__m_cellY" AS VARCHAR) || '|' || CAST("CBodyComponent__m_cellZ" AS VARCHAR) || '|' || CAST("CBodyComponent__m_vecX" AS VARCHAR) || '|' || CAST("CBodyComponent__m_vecY" AS VARCHAR) || '|' || CAST("CBodyComponent__m_vecZ" AS VARCHAR) || '|' || CAST("m_iHealth" AS VARCHAR) AS s, 0.0 AS v, tick FROM CCitadelPlayerPawn WHERE tick % 32 = 0
UNION ALL
SELECT 'tt' AS k, CAST(o AS BIGINT) AS a, s, 0.0 AS v, tick FROM (SELECT tick, CAST("m_hOwnerEntity" AS BIGINT) % 16384 AS o, COALESCE(CAST("m_flCooldownStart" AS VARCHAR),'') || '|' || COALESCE(CAST("m_flCooldownEnd" AS VARCHAR),'') || '|' || COALESCE(CAST("m_flCastCompletedTime" AS VARCHAR),'') AS s, LAG(COALESCE(CAST("m_flCooldownStart" AS VARCHAR),'') || '|' || COALESCE(CAST("m_flCooldownEnd" AS VARCHAR),'') || '|' || COALESCE(CAST("m_flCastCompletedTime" AS VARCHAR),'')) OVER (PARTITION BY entity_index ORDER BY tick) AS ps FROM CCitadel_Ability_TangoTether) t WHERE ps IS NULL OR s <> ps
"""


def fetch(work, ids_file, n=160, workers=6):
    from demo_query import run
    os.makedirs(work, exist_ok=True)
    ids = [line.strip() for line in open(ids_file) if line.strip()][:n]

    def one(mid):
        out = os.path.join(work, f"{mid}.ndjson.gz")
        if os.path.exists(out):
            return "cached"
        tmp = out + ".tmp"
        try:
            run(mid, SQL, tmp)
            with open(tmp, "rb") as s, gzip.open(out + ".part", "wb") as d:
                d.write(s.read())
            os.rename(out + ".part", out)
            os.remove(tmp)
            return "ok"
        except BaseException as e:  # noqa: BLE001
            return f"err {str(e)[:100]}"
    with cf.ThreadPoolExecutor(workers) as ex:
        for mid, r in zip(ids, ex.map(one, ids)):
            print(mid, r, flush=True)


U = 39.37  # source units per metre
R = (8, 12, 16, 20, 25)


def report(raw):
    agg = collections.defaultdict(lambda: [0, collections.Counter()])   # fifth -> [combat s, Counter(R -> s near)]
    cast_agg = [0, collections.Counter()]
    act_agg = [0, collections.Counter()]   # combat seconds inside a Kudzu buff window (12 s after a cast)
    nm = 0
    for f in sorted(os.listdir(raw)):
        if not f.endswith(".ndjson.gz"): continue
        ctl, pos, dmg, tt = {}, collections.defaultdict(list), [], []
        for l in gzip.open(os.path.join(raw, f)):
            r = json.loads(l); k = r["k"]
            if k == "pos":
                c = (r.get("s") or "").split("|")
                if len(c) < 7 or "" in c: continue
                cx, cy, cz, vx, vy, vz, hp = map(float, c)
                pos[r["a"]].append((r["tick"], cx * 512 + vx, cy * 512 + vy, cz * 512 + vz, hp))
            elif k == "ctl":
                h, t = (r.get("s") or "0|0").split("|"); ctl[r["a"]] = (int(h), int(t))
            elif k == "dmg":
                dmg.append((r["tick"], r["a"] // 100000, r["a"] % 100000, r.get("s", "")))
            elif k == "tt":
                tt.append((r["tick"], r["a"], r.get("s", "")))
        ivys = [e for e, (h, t) in ctl.items() if h == 20 and e in pos]
        if not ivys: continue
        nm += 1
        end = max(t for t, *_ in dmg) if dmg else 1
        for ivy in ivys:
            team = ctl[ivy][1]
            allies = [e for e, (h, t) in ctl.items() if t == team and e != ivy and e in pos]
            P = {e: sorted(pos[e]) for e in allies + [ivy]}
            T = {e: [x[0] for x in P[e]] for e in P}
            def at(e, tick):
                i = bisect.bisect_right(T[e], tick) - 1
                return P[e][i] if i >= 0 else None
            def near(tick):
                me = at(ivy, tick)
                if me is None or me[4] <= 0: return None
                best = 1e9
                for a in allies:
                    p = at(a, tick)
                    if p is None or p[4] <= 0: continue
                    d = ((p[1] - me[1]) ** 2 + (p[2] - me[2]) ** 2 + (p[3] - me[3]) ** 2) ** 0.5 / U
                    best = min(best, d)
                return best
            secs = sorted({t // 64 for t, a, v, s in dmg if a == ivy or v == ivy})
            casts = sorted({t for t, o, s in tt if o == ivy and t > 1 and not s.startswith("0.0|")})
            cs = [c // 64 for c in casts]
            for s in secs:
                d = near(s * 64 + 32)
                if d is None: continue
                fifth = min(4, int(5 * s * 64 / end))
                a = agg[fifth]; a[0] += 1
                inbuff = any(0 <= s - c < 12 for c in cs)
                if inbuff: act_agg[0] += 1
                for r_ in R:
                    if d <= r_:
                        a[1][r_] += 1
                        if inbuff: act_agg[1][r_] += 1
            for c in casts:
                d = near(c)
                if d is None: continue
                cast_agg[0] += 1
                for r_ in R:
                    if d <= r_: cast_agg[1][r_] += 1
    print("matches", nm)
    print("combat s with living ally within R m, by fifth of match")
    for fi in sorted(agg):
        n, c = agg[fi]
        print(fi, n, " ".join(f"{r_}m {c[r_]/n:.2f}" for r_ in R))
    n = sum(a[0] for a in agg.values()); c = sum((a[1] for a in agg.values()), collections.Counter())
    print("all", n, " ".join(f"{r_}m {c[r_]/n:.2f}" for r_ in R))
    n, c = act_agg; print("in Kudzu buff (12 s after cast)", n, " ".join(f"{r_}m {c[r_]/max(n,1):.2f}" for r_ in R))
    n, c = cast_agg; print("at Kudzu cast", n, " ".join(f"{r_}m {c[r_]/max(n,1):.2f}" for r_ in R))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "fetch":
        fetch(a[1], a[2], *(int(x) for x in a[3:5]))
    else:
        report(a[1])
