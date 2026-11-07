"""Who real players put their ally-targeted abilities on: themselves or a teammate (2026-11-07).

The duel has no teammates, so abilities that "grant an ally" something are self-cast there (Paige's Plot Armor,
Solomon's Kingside Knight). Replays carry no modifier target (ModifierAppliedEvent is empty; victim_shield_* is null),
but a DamageEvent's damage_absorbed is what a barrier soaked: after each cast, the hero whose absorbed hits appear
(none in the 3 s before, some within the buff) got it. A cast is "self" when the caster's barrier appears, "ally" when only a
teammate's does, "unseen" when nobody with the barrier took damage meanwhile.

fetch: python3 -I ally_target.py fetch <work dir> <ids file> <ability table> [n=160] [workers=6]
report: python3 -I ally_target.py report <work dir> <hero id> [dur=6]
Post-hotfix demos (match id > 132.0M) decode hero ability entities normally (re-checked 2026-11-07,
fight_patterns/demo_check.py); a broken decode seen right after the 11-05 hotfix did not reproduce.
"""
import collections
import concurrent.futures as cf
import gzip
import json
import os
import sys
import bisect

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fight_patterns"))

SQL = """SELECT 'dmg' AS k, CAST(entindex_attacker AS BIGINT) * 100000 + CAST(entindex_victim AS BIGINT) AS a, CAST(ability_id AS VARCHAR) || '|' || CAST(victim_health_new AS VARCHAR) || '|' || CAST(COALESCE(damage_absorbed, 0) AS VARCHAR) AS s, CAST(damage AS DOUBLE) AS v, tick FROM DamageEvent WHERE victim_class = 1 AND damage > 0
UNION ALL
SELECT 'ctl' AS k, CAST(max("m_hHeroPawn") AS BIGINT) % 16384 AS a, CAST(max("m_PlayerDataGlobal__m_nHeroID") AS VARCHAR) || '|' || CAST(max("m_iTeamNum") AS VARCHAR) AS s, 0.0 AS v, min(tick) AS tick FROM CCitadelPlayerController GROUP BY entity_index
UNION ALL
SELECT 'pos' AS k, CAST(entity_index AS BIGINT) AS a, CAST("CBodyComponent__m_cellX" AS VARCHAR) || '|' || CAST("CBodyComponent__m_cellY" AS VARCHAR) || '|' || CAST("CBodyComponent__m_cellZ" AS VARCHAR) || '|' || CAST("CBodyComponent__m_vecX" AS VARCHAR) || '|' || CAST("CBodyComponent__m_vecY" AS VARCHAR) || '|' || CAST("CBodyComponent__m_vecZ" AS VARCHAR) || '|' || CAST("m_iHealth" AS VARCHAR) AS s, 0.0 AS v, tick FROM CCitadelPlayerPawn WHERE tick % 64 = 0
UNION ALL
SELECT 'cast' AS k, CAST(o AS BIGINT) AS a, s, 0.0 AS v, tick FROM (SELECT tick, CAST("m_hOwnerEntity" AS BIGINT) % 16384 AS o, COALESCE(CAST("m_flCooldownStart" AS VARCHAR),'') || '|' || COALESCE(CAST("m_nUpgradeInfo" AS VARCHAR),'') AS s, LAG(COALESCE(CAST("m_flCooldownStart" AS VARCHAR),'') || '|' || COALESCE(CAST("m_nUpgradeInfo" AS VARCHAR),'')) OVER (PARTITION BY entity_index ORDER BY tick) AS ps FROM {table}) t WHERE ps IS NULL OR s <> ps
"""


def fetch(work, ids_file, table, n=160, workers=6):
    from demo_query import run
    os.makedirs(work, exist_ok=True)
    ids = [line.strip() for line in open(ids_file) if line.strip()][:n]
    sql = SQL.replace("{table}", table)

    def one(mid):
        out = os.path.join(work, f"{mid}.ndjson.gz")
        if os.path.exists(out):
            return "cached"
        tmp = out + ".tmp"
        try:
            run(mid, sql, tmp)
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


def load(path):
    ctl, pos, dmg, casts = {}, collections.defaultdict(list), [], []
    for line in gzip.open(path):
        r = json.loads(line); k = r["k"]
        if k == "pos":
            c = (r.get("s") or "").split("|")
            if len(c) < 7 or "" in c: continue
            cx, cy, cz, vx, vy, vz, hp = map(float, c)
            pos[r["a"]].append((r["tick"], cx * 512 + vx, cy * 512 + vy, cz * 512 + vz, hp))
        elif k == "ctl":
            h, t = (r.get("s") or "0|0").split("|"); ctl[r["a"]] = (int(h), int(t))
        elif k == "dmg":
            s = (r.get("s") or "").split("|")
            if len(s) < 3 or s[2] == "": continue
            dmg.append((r["tick"], r["a"] // 100000, r["a"] % 100000, float(s[2])))
        elif k == "cast":
            cd, up = ((r.get("s") or "") + "|").split("|")[:2]
            casts.append((r["tick"], r["a"], cd, up))
    return ctl, pos, sorted(dmg), sorted(casts)


def cast_ticks(casts, owner):
    """Ticks where the owner's ability cooldown start moved to a new positive value (a cast)."""
    out, last = [], None
    for t, o, cd, up in casts:
        if o != owner: continue
        if cd and cd != last and float(cd) > 0 and last is not None:
            out.append((t, up))
        last = cd
    return out


def report(raw, hero, dur=6.0):
    agg = collections.Counter()
    by_phase = collections.defaultdict(collections.Counter)
    near_n = collections.Counter()
    both = [0, 0, 0, 0]   # casts where caster and a teammate were both hit: n, caster shielded, teammate shielded, any
    nm = 0
    for f in sorted(os.listdir(raw)):
        if not f.endswith(".ndjson.gz"): continue
        ctl, pos, dmg, casts = load(os.path.join(raw, f))
        me_list = [e for e, (h, t) in ctl.items() if h == hero]
        if not me_list or not casts or not dmg: continue
        nm += 1
        end = dmg[-1][0]
        ticks = [d[0] for d in dmg]
        for me in me_list:
            team = ctl[me][1]
            allies = [e for e, (h, t) in ctl.items() if t == team and e != me]
            P = {e: sorted(pos[e]) for e in allies + [me] if e in pos}
            T = {e: [x[0] for x in P[e]] for e in P}

            def at(e, tick):
                if e not in T: return None
                i = bisect.bisect_right(T[e], tick) - 1
                return P[e][i] if i >= 0 else None
            for t, up in cast_ticks(casts, me):
                lo = bisect.bisect_left(ticks, t - 3 * 64); mid = bisect.bisect_left(ticks, t); hi = bisect.bisect_right(ticks, t + dur * 64)
                before = {d[2] for d in dmg[lo:mid] if d[3] > 0}
                got = {d[2] for d in dmg[mid:hi] if d[3] > 0 and d[2] not in before}
                seen = {d[2] for d in dmg[mid:hi]}
                pm = at(me, t)
                n_near = 0
                if pm is not None:
                    for a in allies:
                        p = at(a, t)
                        if p is None or p[4] <= 0: continue
                        if ((p[1] - pm[1]) ** 2 + (p[2] - pm[2]) ** 2 + (p[3] - pm[3]) ** 2) ** 0.5 / U <= 20: n_near += 1
                if me in got and got & set(allies): kind = "self+ally"
                elif me in got: kind = "self"
                elif got & set(allies): kind = "ally"
                elif me in seen: kind = "self unshielded"
                else: kind = "unseen"
                fifth = min(4, int(5 * t / end))
                if me in seen and seen & set(allies):   # both the caster and a teammate took hits: no "who was hit" bias
                    both[0] += 1; both[1] += me in got; both[2] += bool(got & set(allies)); both[3] += bool(got)
                agg[kind] += 1; by_phase[fifth][kind] += 1
                near_n[(kind, min(n_near, 3))] += 1
    print("matches", nm)
    tot = sum(agg.values())
    print("all", tot, {k: f"{v / tot:.2f}" for k, v in sorted(agg.items())})
    for fi in sorted(by_phase):
        c = by_phase[fi]; n = sum(c.values())
        print("fifth", fi, n, {k: f"{v / n:.2f}" for k, v in sorted(c.items())})
    print("allies within 20 m at the cast (kind, n):", sorted(near_n.items()))
    n, a_, b_, c_ = both
    if n:
        print(f"caster and a teammate both hit ({n} casts, any barrier {c_ / n:.2f}): caster shielded {a_ / n:.2f}, "
              f"teammate shielded {b_ / n:.2f}; caster share of shielded casts {a_ / max(c_, 1):.2f}")
    seen = agg["self"] + agg["ally"] + agg["self+ally"]
    if seen:
        print(f"of casts with a barrier seen: self {(agg['self'] + agg['self+ally']) / seen:.2f}, ally only {agg['ally'] / seen:.2f}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "fetch":
        fetch(a[1], a[2], a[3], *(int(x) for x in a[4:6]))
    else:
        report(a[1], int(a[2]), *(float(x) for x in a[3:4]))
