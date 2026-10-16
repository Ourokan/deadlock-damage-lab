"""Before/after (difference-in-differences) effect of buying item X on enemy ability damage taken.
For each player who buys X (and keeps it), per 180 s window: share = (ability dmg taken by the player / max hp) over
(mean of teammates' ability dmg taken / max hp), same enemy dealers. effect = mean share after / mean share before
(windows fully before purchase vs fully after), pooled over players (ratio of sums)."""
import glob, gzip, json, random, sys
N_T = [0]
def at(s, k):
    """Damage-matrix arrays are cumulative per sample time but right-aligned: shorter arrays start later."""
    i = k - (N_T[0] - len(s))
    return s[i] if 0 <= i < len(s) else (0 if i < 0 else s[-1])
sys.path.insert(0, sys.argv[1])
from deadsim.data import game
G = game()
NAMES = sys.argv[3].split(",")
files = sorted(glob.glob(sys.argv[2] + "/*.json.gz"))
def is_ability(nm): return nm.startswith(("ability_", "citadel_ability"))
res = {n: [] for n in NAMES}
for fn in files:
    m = json.load(gzip.open(fn, "rt")); T = m["times"]; N_T[0] = len(T); P = {p["slot"]: p for p in m["players"]}
    def maxhp(p, t):
        for ts, hp, nw in p["stats"]:
            if ts >= t and hp: return hp
        return None
    # ability damage taken per target per window
    taken = {}
    for dslot, srcs in m["dmg"].items():
        for nm, tg in srcs.items():
            if not is_ability(nm): continue
            for ts, ser in tg.items():
                arr = taken.setdefault(int(ts), [0.0] * len(T))
                for k in range(1, len(T)):
                    arr[k] += at(ser, k) - at(ser, k - 1)
    for name in NAMES:
        iid = G.item(name).id
        for p in m["players"]:
            buy = [(b, s) for i, b, s in p["items"] if i == iid]
            if not buy: continue
            b, s = buy[0]
            mates = [q for q in m["players"] if q["team"] == p["team"] and q["slot"] != p["slot"]
                     and not any(i == iid for i, *_ in q["items"])]
            bef, aft = [0, 0], [0, 0]
            for k in range(1, len(T)):
                t0, t1 = T[k - 1], T[k]
                hp = maxhp(p, t1)
                mv = [taken.get(q["slot"], [0] * len(T))[k] / h for q in mates if (h := maxhp(q, t1))]
                if not hp or not mv: continue
                mine = taken.get(p["slot"], [0] * len(T))[k] / hp
                mean = sum(mv) / len(mv)
                if t1 <= b:
                    bef[0] += mine; bef[1] += mean
                elif t0 >= b and (not s or s >= t1):
                    aft[0] += mine; aft[1] += mean
            if bef[1] > 0 and aft[1] > 0:
                res[name].append((bef[0], bef[1], aft[0], aft[1]))
random.seed(2)
for name, rows in res.items():
    def eff(rs):
        b = sum(r[0] for r in rs) / sum(r[1] for r in rs); a = sum(r[2] for r in rs) / sum(r[3] for r in rs)
        return a / b
    bs = sorted(eff([random.choice(rows) for _ in rows]) for _ in range(400))
    print(name, "players", len(rows), "effect", round(eff(rows), 3), "ci90", round(bs[20], 3), round(bs[379], 3))
