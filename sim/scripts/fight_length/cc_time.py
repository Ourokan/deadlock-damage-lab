"""Real Phantom+ crowd-control time per fight from replays, against the sim duel's.

Real (default): fetch_cc.py extracts (each pawn's modifier state mask and slow ring) beside fetch_fights.py's (hero
damage events, pawn -> hero) for the same matches. A player is in combat during each of their pair fights (fit_length:
a run of damage between them and one enemy hero, both ways, no gap over GAP_S, MIN_HITS hits); their combat time is the
union of those. CC time is the time a state bit is on inside their combat time. The bits were matched to the replays'
AbilityNotifyEvent status bits (1 stun, 4 sleep, 8 silence, 16 disarm, 32 immobilize) by which pawn bit goes on with
each status within 8 ticks (lift over the bit's base rate, 18 matches):
stun 12 (97% of stun notifies, Knockdown 98%, Petrifying Bola 98%; 20 twins it), sleep 144 (Sleep Dagger 100%),
silence 17 (Silence Wave 98%, 3.0 s), immobilize 18 (79%; it also goes on without any notify, so it reads high).
Disarm is unsure: no bit goes on with Sand Blast's disarm notifies; 21 is the best of weak candidates (25%).
Fear (Nurse's Terrors), Hotel Guest and Telekinesis send no notify; their bits are not mapped (not counted).
The pawn's slow ring (last four slows, game-clock start / end) holds 0.6 s 50% slows only, not ability slows: the
"slow" row is printed but is not comparable with the sim's move slows.
Each CC run is credited to the enemy whose status notify on the player came last before it (within NOTIFY_S), and
counted as "from the duel foe" when that enemy is one of the player's pair-fight partners at the time (the sim duel
only has its foe's CC). The per-hero table (--compare) uses credited CC only, so heroes whose CC sends no notify read
low there.

Sim (--sim <sample> [max players] [workers]): damage_audit's duels (each player's real build and a real foe of the
same match at five points of the match, mechanics as the searches) with every CC debuff put on the player logged
(keys stun, silence, disarm, immobilize; Haze's sleep is a stun; slow = move_slow), time on / duel time. CC_LANDING=0
/ 1 overrides Mechanics.cc_landing.

Result (2026-10-28, 260 matches / 3,000 sim players): real stun 2.46% + sleep 0.28%, silence 2.20% of combat time
(match-id halves 2.72 / 2.77%, 2.16 / 2.24%); sim duel's one foe 4.24% stun, 3.07% silence before cc_landing, 3.27%
/ 2.97% with it. Write-up: validation/cc_time.md.

usage: python3 -I cc_time.py <cc raw dir> <fights raw dir> [--sample validation/phantom_sample.jsonl.gz] [--json out]
                                [--compare sim.json]
       python3 cc_time.py --sim <sample> [max_players] [workers] [--json sim.json]
"""
import bisect
import collections
import glob
import gzip
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from fit_length import GAP_S, MIN_HITS, T, read  # noqa: E402

BITS = {"stun": (12,), "sleep": (144,), "silence": (17,), "immobilize": (18,), "disarm": (21,)}
STATUS = {1: "stun", 4: "sleep", 8: "silence", 16: "disarm", 32: "immobilize"}
NOTIFY_S = 0.25
KEYS = ("stun", "sleep", "silence", "disarm", "immobilize", "slow")


def read_cc(fn):
    """({pawn: [(tick, frozenset(bits))]}, {pawn: [(start s, end s, speed)]}, [(tick, attacker, victim, status)],
    clock offset ticks/T - game clock)."""
    st, slows, nt, offs = collections.defaultdict(list), collections.defaultdict(set), [], []
    for line in gzip.open(fn, "rt"):
        r = json.loads(line)
        if r["k"] == "st":
            m, sl = r["s"].split("#")
            w = [int(x) for x in m.split(",")] if m else []
            st[r["a"]].append((r["tick"], frozenset(i * 64 + b for i, x in enumerate(w) for b in range(64) if x >> b & 1)))
            parts = sl.split(";")
            if len(parts) == 3 and parts[0]:
                ss, se, sp = ([float(x) for x in p.split(",")] for p in parts)
                for a, b, c in zip(ss, se, sp):
                    if b > a > 0:
                        if (a, b, c) not in slows[r["a"]]:
                            offs.append(r["tick"] / T - a)
                        slows[r["a"]].add((a, b, c))
        elif r["k"] == "nt" and r["v"] == 0:
            ab, si = r["s"].split("|")
            nt.append((r["tick"], r["a"] // 100000, r["a"] % 100000, int(si) if si else 0))
    for v in st.values():
        v.sort(key=lambda x: x[0])
    nt.sort()
    # a new slow shows up on the tick it starts (or a few later): the most common offset is the clock's
    off = collections.Counter(round(x, 1) for x in offs).most_common(1)[0][0] if offs else None
    return st, {k: sorted(v) for k, v in slows.items()}, nt, off


def runs_of(seq, bits):
    """[(t0 s, t1 s)] while any of bits is on."""
    out, on = [], None
    for t, b in seq:
        a = not b.isdisjoint(bits)
        if a and on is None:
            on = t / T
        elif not a and on is not None:
            out.append((on, t / T))
            on = None
    if on is not None:
        out.append((on, seq[-1][0] / T))
    return out


def union(iv):
    out = []
    for a, b in sorted(iv):
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def overlap(iv, win):
    """Seconds of iv (sorted, disjoint) inside win (sorted, disjoint)."""
    s, j = 0.0, 0
    for a, b in iv:
        while j < len(win) and win[j][1] <= a:
            j += 1
        k = j
        while k < len(win) and win[k][0] < b:
            s += max(0.0, min(b, win[k][1]) - max(a, win[k][0]))
            k += 1
    return s


def pair_fights(hero, ev, team):
    """{pawn: [(t0, t1, foe pawn)]}: fit_length's fights, seen from both sides."""
    pairs = collections.defaultdict(list)
    for e in ev:
        _, a, v = e[:3]
        if a in team and v in team and team[a] != team[v]:
            pairs[min(a, v), max(a, v)].append(e)
    out = collections.defaultdict(list)
    for (x, y), es in pairs.items():
        runs = []
        for e in es:
            if not runs or e[0] - runs[-1][-1][0] > GAP_S:
                runs.append([])
            runs[-1].append(e)
        for f in runs:
            death = next((k for k, e in enumerate(f) if e[3] <= 0), None)
            if death is not None:
                f = f[:death + 1]
            if len(f) < MIN_HITS or len({(e[1], e[2]) for e in f}) < 2:
                continue
            out[x].append((f[0][0], f[-1][0], y))
            out[y].append((f[0][0], f[-1][0], x))
    return out


def match_cc(cc_fn, fights_fn, teams):
    """Per player: hero, combat s, {key: CC s in combat}, {key: of which from a pair-fight foe}, {key: runs started}."""
    hero, ev = read(fights_fn)
    st, slows, nt, off = read_cc(cc_fn)
    team = {p: teams.get(h) for p, h in hero.items() if teams.get(h) is not None}
    fights = pair_fights(hero, ev, team)
    by_victim = collections.defaultdict(list)
    for t, a, v, si in nt:
        if si and a in team and v in team and team[a] != team[v]:
            by_victim[v].append((t / T, a, si))
    out = []
    applied = collections.defaultdict(collections.Counter)
    comb = {}
    for p, fl in fights.items():
        win = union((a, b) for a, b, _ in fl)
        combat = sum(b - a for a, b in win)
        if combat <= 0:
            continue
        cc, duel_cc, n = collections.Counter(), collections.Counter(), collections.Counter()
        notes = by_victim.get(p, [])
        nts = [x[0] for x in notes]
        for k, bits in BITS.items():
            for a, b in runs_of(st.get(p, []), set(bits)):
                s = overlap([(a, b)], win)
                if s <= 0:
                    continue
                cc[k] += s
                n[k] += 1
                i = bisect.bisect_right(nts, a + 0.05) - 1
                src = notes[i][1] if i >= 0 and a - nts[i] <= NOTIFY_S else None
                if src is not None and any(f0 - 1 <= a <= f1 + 1 and foe == src for f0, f1, foe in fl):
                    duel_cc[k] += s
                if src is not None:
                    applied[src][k] += s
        if off is not None:
            iv = union((a + off, b + off) for a, b, _ in slows.get(p, []))
            s = overlap(iv, win)
            cc["slow"] += s
            n["slow"] += sum(1 for a, b in iv if overlap([(a, b)], win) > 0)
        comb[p] = combat
        out.append([hero[p], combat, dict(cc), dict(duel_cc), dict(n)])
    by_p = {p: i for i, p in enumerate(p for p in fights if comb.get(p))}
    for p, i in by_p.items():
        out[i].append(dict(applied.get(p, {})))
    return [tuple(r) for r in out]


def real(args):
    cc_dir, f_dir = args[0], args[1]
    sample = args[args.index("--sample") + 1] if "--sample" in args else os.path.join(HERE, "..", "..", "validation", "phantom_sample.jsonl.gz")
    mids = {os.path.basename(f).split(".")[0] for f in glob.glob(os.path.join(cc_dir, "*.ndjson.gz"))}
    teams = {}
    for line in gzip.open(sample):
        m = json.loads(line)
        if str(m["match_id"]) in mids:
            teams[str(m["match_id"])] = {p["hero_id"]: p["team"] for p in m["players"]}
    rows = []
    for mid in sorted(mids & set(teams)):
        ff = os.path.join(f_dir, f"{mid}.ndjson.gz")
        if os.path.exists(ff):
            rows += [(mid,) + r for r in match_cc(os.path.join(cc_dir, f"{mid}.ndjson.gz"), ff, teams[mid])]
    return rows


def by_hero_applied(rows, sim_rows=None):
    """CC each hero puts on enemies per second of its own combat (real: credited by notify; sim: on the duel's
    player from the foe)."""
    from deadsim import game
    G = game()
    real_h = collections.defaultdict(lambda: [0.0, collections.Counter()])
    for r in rows:
        real_h[r[1]][0] += r[2]
        real_h[r[1]][1].update(r[6])
    sim_h = collections.defaultdict(lambda: [0.0, collections.Counter()])
    for r in sim_rows or []:
        for h, (t, c) in r[6].items():
            sim_h[int(h)][0] += t
            sim_h[int(h)][1].update(c)
    hard = ("stun", "sleep", "silence", "disarm", "immobilize")
    out = {}
    for h in sorted(set(real_h) | set(sim_h), key=lambda h: G.hero(h).name if h in G.heroes else str(h)):
        rt, rc = real_h.get(h, (0, {}))
        st, sc = sim_h.get(h, (0, {}))
        re_ = sum(rc.get(k, 0) for k in hard) / rt * 100 if rt else None
        si = sum(sc.get(k, 0) for k in ("stun", "silence", "disarm", "immobilize")) / st * 100 if st else None
        name = G.hero(h).name if h in G.heroes else str(h)
        out[name] = {"real_pct": re_, "sim_pct": si, "real_min": rt / 60, "sim_min": st / 60}
        print(f"  {name:16s} real {re_ if re_ is not None else float('nan'):5.2f}%  sim {si if si is not None else float('nan'):5.2f}%"
              f"  ({rt / 60:.0f} / {st / 60:.0f} combat min)")
    return out


def summarize(rows, label):
    comb = sum(r[2] for r in rows)
    print(f"{label}: {len({r[0] for r in rows})} matches, {len(rows)} player-matches, {comb / 60:.0f} combat min")
    for k in KEYS:
        s = sum(r[3].get(k, 0) for r in rows)
        d = sum(r[4].get(k, 0) for r in rows)
        n = sum(r[5].get(k, 0) for r in rows)
        if n:
            print(f"  {k:10s} {100 * s / comb:5.2f}% of combat time  ({n / comb * 60:.2f} runs/min, "
                  f"mean {s / n:.2f} s; from a pair-fight foe {100 * d / max(1e-9, s):.0f}%)")
        else:
            print(f"  {k:10s} {100 * s / comb:5.2f}% of combat time")


SIM_KEYS = {"stun": "stun", "silence": "silence", "disarm": "disarm", "immobilize": "immobilize", "move_slow": "slow"}
_log, _ids, _acc = [], [], {}


def _sim_job(job):
    """damage_audit.sim_player's duels for one player-match, with the CC put on the player logged: (hero id, duel s,
    {key: s})."""
    import damage_audit as DA
    from deadsim import engine, fight
    if not getattr(engine.Mods, "_cc_wrapped", False):
        add, mk, rm = engine.Mods.add, fight.make_fighter, engine.Mods.remove

        def rm_w(self, key, tag):
            # a CC removed early (Haze's sleep broken by damage, a cleanse) ends now
            k = SIM_KEYS.get(key)
            if k and _ids and id(self) == _ids[0] and tag in self.d.get(key, {}):
                for i in range(len(_log) - 1, -1, -1):
                    if _log[i][0] == k and _log[i][4] == tag:
                        _log[i] = _log[i][:2] + (min(_log[i][2], self.engine.t),) + _log[i][3:]
                        break
            return rm(self, key, tag)

        def add_w(self, key, value, duration, tag=None):
            k = SIM_KEYS.get(key)
            if k and duration > 0 and tag != "ethereal" and _ids and id(self) == _ids[0]:
                _log.append((k, self.engine.t, self.engine.t + duration, self.engine.max_time, tag))
            return add(self, key, value, duration, tag)

        def mk_w(e, lo, name, *a, **kw):
            f = mk(e, lo, name, *a, **kw)
            _ids.append(id(f.mods))
            return f
        engine.Mods.add, fight.make_fighter, engine.Mods.remove = add_w, mk_w, rm_w
        engine.Mods._cc_wrapped = True
        duel = DA.duel

        def duel_w(*a, **kw):
            _ids.clear()
            r = duel(*a, **kw)
            _acc["t"] += r.time
            fh = a[1].hero
            by = _acc["by"].setdefault(fh, [0.0, collections.Counter()])
            by[0] += r.time
            ends = collections.defaultdict(list)
            for k, t0, t1, _, _ in _log:
                ends[k].append((t0, min(t1, r.time)))
            for k, iv in ends.items():
                v = sum(b - a_ for a_, b in union(iv) if b > a_)
                _acc["cc"][k] += v
                by[1][k] += v
            _log.clear()
            return r
        DA.duel = duel_w
        if os.environ.get("CC_LANDING"):
            import dataclasses
            DA.MECH = dataclasses.replace(DA.MECH, cc_landing=os.environ["CC_LANDING"] == "1")
    _acc["t"], _acc["cc"], _acc["by"] = 0.0, collections.Counter(), {}
    hid, _, _ = DA.sim_player(job)
    return hid, _acc["t"], dict(_acc["cc"]), {h: [t, dict(c)] for h, (t, c) in _acc["by"].items()}


def sim(args):
    """Sim CC time on players in damage_audit's whole-match duels."""
    sys.path.insert(0, os.path.join(HERE, ".."))
    os.environ.setdefault("AUDIT_COVER", "1")
    import damage_audit as DA
    import landing_rates as L
    from concurrent.futures import ProcessPoolExecutor
    from deadsim import game
    sample = args[0]
    max_players = int(args[1]) if len(args) > 1 else 10 ** 9
    workers = int(args[2]) if len(args) > 2 else os.cpu_count()
    G = game()
    jobs = []
    for line in gzip.open(sample):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] in G.heroes and L.gun_known(p):
                jobs.append((m, p["slot"]))
    random.Random(1).shuffle(jobs)
    jobs = jobs[:max_players]
    rows = []
    with ProcessPoolExecutor(workers) as ex:
        for (m, slot), (hid, t, c, by) in zip(jobs, ex.map(_sim_job, jobs, chunksize=4)):
            rows.append((str(m["match_id"]), hid, t, c, {}, {}, by))
    return rows


def main():
    args = sys.argv[1:]
    if args and args[0] == "--sim":
        rows = sim(args[1:])
        summarize(rows, "sim")
        if "--json" in args:
            json.dump({"rows": rows}, open(args[args.index("--json") + 1], "w"))
        return
    out = None
    if "--json" in args:
        out = args[args.index("--json") + 1]
    rows = real(args)
    summarize(rows, "real")
    halves = collections.defaultdict(list)
    for r in rows:
        halves[int(r[0]) % 2].append(r)
    for h, rr in sorted(halves.items()):
        summarize(rr, f"half {h}")
    if "--compare" in args:
        sim_rows = json.load(open(args[args.index("--compare") + 1]))["rows"]
        summarize(sim_rows, "sim")
        print("CC put on enemies per second of the hero's own combat (stun, sleep, silence, disarm, immobilize):")
        by_hero_applied(rows, sim_rows)
    if out:
        json.dump({"rows": [[r[0], r[1], round(r[2], 2), r[3], r[4], r[5]] for r in rows]}, open(out, "w"))


if __name__ == "__main__":
    random.seed(0)
    main()
