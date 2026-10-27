"""Killing Blow and Soul Exchange on real fight timing, from Phantom+ replays: data/execute_timing.json.

The sim casts Killing Blow only on an execute (target below EnemyHealthPercent) and Soul Exchange only once Geist is
SWAP_MIN_GAIN lower than her target. Against the real cast curves (validation/cast_timing.md) Killing Blow came out
~3 s late (median first cast 11.2 s vs 8.5 s) and cast in 84% of duels by 20 s (real 36%); Soul Exchange ~2 s early
(6.4 s vs 8.6 s) and cast in 18% (real 42%). The replays show why:

- third parties: in a real pair fight the enemy also takes damage from the fighter's teammates. Geist takes ~1.15x as
  much from others as from her pair enemy (and enters fights at ~75% health): real Geists swap at ~25% health on a
  ~90% target, a gap the sim's duel rarely opens. "assist": damage the gate holder takes from others / from the pair
  enemy over the pair fights (Fighter.gate_assist). Shiv's target takes ~0.9x from others too ("assist_kb_target"),
  but the sim's duels already bring the target down faster than real pair fights: with it Killing Blow's executes
  came ~3 s early, without it (entry deficit only) on real timing, so Killing Blow doesn't use it.
- Soul Exchange's first cast in a fight: "soul_exchange" holds = the real first cast times (QBINS points of its
  curve, None = not cast; on hold_share of the fights, fitted on the sim duels so the cast share by 20 s matches:
  the gap gate leaves some holds uncast); the swap waits for its hold, then for its gap (Geist's gate health).
- half of the real first Killing Blows in a fight are no execute: cast on a target at ~55% health for the slash
  damage (or missed), and the ult then sits out its whole cooldown (next cast ~200 s later, vs ~10 s after an
  execute's recast). "killing_blow": competing-risk curves of the first cast in a fight (Kaplan-Meier, fight end
  censors): "spent" = cast without an execute, "exec" = an execute; the sim draws one of: spent at a real time
  (commit_holds, quantiles of the spent curve), execute when the gate opens (exec_share, fitted on the sim duels so
  the total cast curve by 20 s matches), or not this fight (ult on cooldown).

Fights as fit_length.py (two enemy heroes trading, gaps < 5 s, >= 4 hits both ways), first casts as
fit_cast_timing.py real (PRE_S before the first hit counts as 0; never cast before in the match = not unlocked: left
out). Rows "all" plus "even" / "odd" match id halves for the split-half check.

usage: python3 -I execute_timing.py [--se-only] [--write]   (real side, then the sim fits on Shiv's / Geist's audit
       duels; --se-only refits Soul Exchange's hold_share and keeps the file's Killing Blow rows)
"""
import bisect
import collections
import gzip
import json
import os
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "fight_length"))
sys.path.insert(0, os.path.join(HERE, "..", "cast_timing"))
import fit_cast_timing as CT  # noqa: E402
import fit_length as FL  # noqa: E402
import opener_timing as OT  # noqa: E402

FIGHTS = CT.FIGHTS
CASTS = CT.CASTS
OUT = os.path.join(ROOT, "data", "execute_timing.json")
SHIV, GEIST = 19, 4
KB = 1835738020
SE = 1307289689
KB_CLASS = "citadel_ability_shiv_killing_blow"
SE_CLASS = "ability_health_swap"
HIT_S = 3.0      # a Killing Blow hit this long after the cast is its slash
EXEC_FRAC = 0.95  # a lethal slash dealing this share of the target's health or more is an execute
FIT_STEPS = 6     # bisection steps of the sim fits (~6 s each per hero)


def match_rows(fn):
    """(match id, [(kind, value...)]) for one match: ("assist", hero id, from enemy, from others) per pair fight of
    Shiv / Geist; ("kb", first cast s or None, "exec" / "spent" / None, fight length s) per Shiv fight; ("se", first
    cast s or None, "cast" / None, fight length s) per Geist fight."""
    mid = os.path.basename(fn).split(".")[0]
    hero, ev = OT.read(fn)
    byv = collections.defaultdict(list)
    for e in ev:
        byv[e[2]].append(e)
    pairs = collections.defaultdict(list)
    for e in ev:
        if e[1] != e[2] and (hero.get(e[1]) in (SHIV, GEIST) or hero.get(e[2]) in (SHIV, GEIST)):
            pairs[min(e[1], e[2]), max(e[1], e[2])].append(e)
    casts = []
    cfn = os.path.join(CASTS, os.path.basename(fn))
    if os.path.exists(cfn):
        casts = CT.real_casts([json.loads(line) for line in gzip.open(cfn, "rt")])
    ult_casts = collections.defaultdict(list)
    for r in casts:
        if int(r["s"]) in (KB, SE):
            ult_casts[r["a"]].append(r["tick"] / CT.T)
    for v in ult_casts.values():
        v.sort()
    kb_hits = collections.defaultdict(list)
    for e in ev:
        if e[6] == KB:
            kb_hits[e[1]].append(e)
    out = []
    for (x, y), es in pairs.items():
        runs = []
        for e in es:
            if not runs or e[0] - runs[-1][-1][0] > FL.GAP_S:
                runs.append([])
            runs[-1].append(e)
        for f in runs:
            death = next((k for k, e in enumerate(f) if e[3] <= 0), None)
            if death is not None:
                f = f[:death + 1]
            if len(f) < FL.MIN_HITS or len({(e[1], e[2]) for e in f}) < 2:
                continue
            t0, t1 = f[0][0], f[-1][0]
            for me, foe in ((x, y), (y, x)):
                h = hero.get(me)
                if h == hero.get(foe) or h not in (SHIV, GEIST):
                    continue
                # the gate holder: Shiv's target (its health opens Killing Blow), Geist herself (Soul Exchange)
                v, pair = (foe, me) if h == SHIV else (me, foe)
                taken = [e for e in byv[v] if t0 <= e[0] <= t1]
                out.append(("assist", h, sum(e[5] for e in taken if e[1] == pair),
                            sum(e[5] for e in taken if e[1] != pair)))
                if me not in ult_casts:
                    continue
                cs = ult_casts[me]
                k = bisect.bisect_left(cs, t0 - CT.PRE_S)
                first = cs[k] if k < len(cs) and cs[k] <= t1 else None
                if first is None and k == 0:
                    continue   # never cast before in the match: not unlocked yet
                kind = None
                if first is not None and h == GEIST:
                    kind = "cast"
                elif first is not None:
                    hs = [e for e in kb_hits.get(me, []) if 0 <= e[0] - first <= HIT_S]
                    ex = hs and hs[0][3] <= 0 and hs[0][5] >= EXEC_FRAC * (hs[0][3] + hs[0][5])
                    kind = "exec" if ex else "spent"
                out.append(("kb" if h == SHIV else "se", None if first is None else max(0.0, first - t0), kind,
                            t1 - t0))
    return mid, out


def cif(rows):
    """rows (time or None, kind, fight length): cumulative incidence of each first-cast kind on CT.GRID (Kaplan-Meier,
    the fight's end censors)."""
    ev = sorted(((t if t is not None else d, (kind if t is not None else None) or "") for t, kind, d in rows))
    n, i, surv = len(ev), 0, 1.0
    acc = collections.Counter()
    out = {"exec": [], "spent": [], "cast": []}
    for t in CT.GRID:
        while i < n and ev[i][0] <= t:
            j, c = i, collections.Counter()
            while j < n and ev[j][0] == ev[i][0]:
                if ev[j][1]:
                    c[ev[j][1]] += 1
                j += 1
            at_risk = n - i
            for k, m in c.items():
                acc[k] += surv * m / at_risk
            surv *= 1.0 - sum(c.values()) / at_risk
            i = j
        for k in out:
            out[k].append(round(acc[k], 4))
    return out


def commit_holds(spent):
    """CT.QBINS equal-probability points u of the spent curve: the time it reaches u (None past its share by the
    horizon)."""
    out = []
    for b in range(CT.QBINS):
        p = (b + 0.5) / CT.QBINS
        q = CT.quantile(spent, p)
        out.append(None if q is None or p > spent[-1] else round(q, 3))
    return out


def real():
    files = sorted(os.path.join(FIGHTS, f) for f in os.listdir(FIGHTS) if f.endswith(".ndjson.gz"))
    by = {"all": [], "even": [], "odd": []}
    with Pool(4) as p:
        for mid, rs in p.imap_unordered(match_rows, files):
            by["all"] += rs
            by["even" if int(mid) % 2 == 0 else "odd"] += rs
    res = {}
    for half, rs in by.items():
        assist = {}
        for h, cls in ((SHIV, KB_CLASS), (GEIST, SE_CLASS)):
            a = [r for r in rs if r[0] == "assist" and r[1] == h]
            assist[cls] = round(sum(r[3] for r in a) / max(1.0, sum(r[2] for r in a)), 3)
        kb = [r[1:] for r in rs if r[0] == "kb"]
        c = cif(kb)
        se = [r[1:] for r in rs if r[0] == "se"]
        cs = cif(se)["cast"]
        res[half] = {"assist": {SE_CLASS: assist[SE_CLASS]}, "assist_kb_target": assist[KB_CLASS],
                     "killing_blow": {"fights": len(kb), "exec_by": c["exec"], "spent_by": c["spent"],
                                      "commit_share": c["spent"][-1], "commit_holds": commit_holds(c["spent"])},
                     "soul_exchange": {"fights": len(se), "cast_by": cs, "holds": commit_holds(cs)}}
    return res


def sim_top(row, hid, cls):
    """The sim's P(first cast by 20 s) of hid's ability cls in the audit duels with this row (the duels run in forked
    workers, which inherit it)."""
    from deadsim import mechanics
    mechanics._EXEC = {mechanics.EXEC_ROW: row}
    return CT.sim_curves(10 ** 6, os.cpu_count(), True, hero=hid)[f"{hid}:{cls}"]["cast_by"][-1]


def bisect_fit(set_x, target, steps=FIT_STEPS):
    """x in [0, 1] with sim_top(set_x(x)) ~ target (it rises with x; a Kaplan-Meier share is not linear in it)."""
    lo, hi = 0.0, 1.0
    for _ in range(steps):
        mid = (lo + hi) / 2
        if set_x(mid) < target:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 3)


def main():
    write = "--write" in sys.argv
    se_only = "--se-only" in sys.argv
    res = real()
    if se_only:
        old = json.load(open(OUT))
        for half, r in res.items():
            r["killing_blow"] = old[half]["killing_blow"]
    for half, r in res.items():
        k = r["killing_blow"]
        print(half, "assist", r["assist"], "KB target", r["assist_kb_target"], "KB fights", k["fights"],
              "spent by 20 s", k["commit_share"], "exec by 20 s", k["exec_by"][-1], "SE fights",
              r["soul_exchange"]["fights"], "cast by 20 s", r["soul_exchange"]["cast_by"][-1])
    # fitted on the sim duels so the first cast share by 20 s matches: Killing Blow's exec_share; Soul Exchange's
    # share of fights with a hold (its gap gate leaves some of them uncast)
    for half, r in res.items():
        k, se = r["killing_blow"], r["soul_exchange"]
        real_se = list(se["cast_by"])

        def kb_at(x):
            k["exec_share"] = x
            return sim_top(r, SHIV, KB_CLASS)

        def se_at(x):
            top = real_se[-1] or 1.0
            se["holds"] = commit_holds([v / top * x for v in real_se])
            return sim_top(r, GEIST, SE_CLASS)
        target = k["exec_by"][-1] + k["spent_by"][-1]
        if not se_only:
            k["exec_share"] = bisect_fit(kb_at, target)
        se["hold_share"] = bisect_fit(se_at, real_se[-1])
        se_at(se["hold_share"])
        print(half, f"Killing Blow by 20 s target {target:.3f}: exec_share {k['exec_share']} -> "
              f"{kb_at(k['exec_share']):.3f}; Soul Exchange target {real_se[-1]:.3f}: hold_share "
              f"{se['hold_share']} -> {sim_top(r, GEIST, SE_CLASS):.3f}")
    out = {"source": f"{len(os.listdir(FIGHTS))} Phantom+ replays, pair fights (scripts/mechanics/execute_timing.py)",
           "note": ("assist: damage the gate holder (Geist; assist_kb_target: Shiv's target, not used) takes from "
                    "others per damage from the pair enemy in real pair fights. Killing Blow first cast in a fight: "
                    "commit_holds = real times of a first cast without an execute (spent, None = no such cast), "
                    "exec_share = share of fights whose Killing Blow waits for the execute gate (fitted on the sim "
                    "duels), the rest not cast (cooldown). Soul Exchange: holds = real first cast times (None = not "
                    "cast; hold_share = share of fights with a hold, fitted on the sim duels), then the gap gate"),
           "grid_s": CT.GRID, **res}
    if write:
        with open(OUT, "w") as fh:
            json.dump(out, fh, indent=1)
            fh.write("\n")
        print("wrote", OUT)


if __name__ == "__main__":
    main()
