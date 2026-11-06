"""What a real Healing Nova cast gives teammates, from Phantom+ replays (fetch_nova.py), against the 3v3 team_value.py
fits. Run from the repo root:

    python3 sim/scripts/team/nova_heal.py /mnt/project-files/analysis/work/nova_heal/raw [--sim] [--half 0|1]

Per cast (holder pawn, tick T), for the holder and each living teammate: health and max health at T, health
received over the heal (T .. T + HEAL_S: health change + health lost to damage events) minus the mean of the same
over the HEAL_S before and after (control windows: lifesteal, regen and other heals in the fight), distance to the holder, whether the teammate dies within DIE_S after the
cast, and whether the cast is in a fight (hero damage to or from the holder's team within FIGHT_S of the cast).
Teammates within RADIUS_M of the holder are "in reach"; the heal a teammate with a large deficit receives is the
cast's full heal, so 1 - received / (full x teammates in reach) is the overheal.

The 3v3 (team_value.py fights at SOULS, each lineup's A heroes holding Nova in turn) is instrumented the same way:
every ally heal (time, teammate, amount) and whether that teammate dies within DIE_S.

Output: per cast, real vs 3v3, ally heal received, the share of it on teammates who die anyway, the share in
fights; the real ally heal per fight relative to the holder's hero damage (fight_rate_post timelines of the same
matches) against the 3v3's, which is the absolute anchor ally_heal.py's median lacks.
"""
import collections
import dataclasses
import glob
import gzip
import json
import math
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.abspath(os.path.join(HERE, "..", ".."))
ROOT = os.path.dirname(SIM)
TICK = 64.0
HEAL_S = 2.75          # 0.25 s cast delay + 2 s heal + slack
DIE_S = 10.0
FIGHT_S = 4.0
RADIUS_M = 18.0
UNITS_PER_M = 1 / 0.0254 / 1.0   # Source units are inches
FULL_DEFICIT = 0.35    # teammates this far below max health show the full heal
SOULS = 27000
LINEUPS = 15


def load(fn):
    rows = collections.defaultdict(list)
    with gzip.open(fn, "rt") as f:
        for line in f:
            if line.strip():
                d = json.loads(line)
                rows[d["k"]].append(d)
    return rows


def pos(s):
    c = s.split("|")
    if len(c) < 6 or "None" in c or "" in c:
        return None
    return (int(c[0]) * 512 + float(c[2]), int(c[1]) * 512 + float(c[3]), int(c[4]) * 512 + float(c[5]))


def health_at(series, tick):
    """(health, max health, life state) of the last change at or before tick."""
    last = None
    for t, h, mh, ls in series:
        if t > tick:
            break
        last = (h, mh, ls)
    return last


def lost_between(dmg, t0, t1):
    return sum(x for t, x in dmg if t0 < t <= t1)


def gain(series, lost, t0, t1):
    """Health received from t0 to t1 (health change + health lost to damage), None if dead at either end."""
    a, b = health_at(series, t0), health_at(series, t1)
    if not a or not b or a[2] != 0 or b[2] != 0 or a[0] <= 0 or b[0] <= 0:
        return None
    return b[0] - a[0] + lost_between(lost, t0, t1)


def casts(fn):
    """Per cast: dict(holder, tick, team, fight, allies=[dict(self, h, mh, recv, dist_m, dies)])."""
    r = load(fn)
    team = {d["a"]: d["s"] for d in r["pawn"]}
    hp = collections.defaultdict(list)
    for d in r["hp"]:
        mh, ls = d["s"].split("|")
        hp[d["a"]].append((d["tick"], d["v"], float(mh), int(ls)))
    for s in hp.values():
        s.sort()
    lost = collections.defaultdict(list)
    hits = []          # (tick, attacker, victim)
    for d in r["dmg"]:
        at, vi = divmod(d["a"], 100000)
        hl = d["s"].split("|")[0]
        lost[vi].append((d["tick"], float(hl) if hl not in ("", "None") else d["v"]))
        if at in team and d["v"] > 0:
            hits.append((d["tick"], at, vi))
    deaths = collections.defaultdict(list)
    for d in r["kill"]:
        deaths[d["a"] % 100000].append(d["tick"])
    ps = collections.defaultdict(list)
    for d in r["pos"]:
        p = pos(d["s"])
        if p:
            ps[d["a"]].append((d["tick"], p))
    out = []
    for c in sorted(r["nova"], key=lambda d: d["tick"]):
        o, T = c["a"], c["tick"]
        if o not in team:
            continue
        side = team[o]
        mates = [e for e, tm in team.items() if tm == side]
        fight = any(abs(t - T) <= FIGHT_S * TICK and (team.get(a) == side) != (team.get(v) == side)
                    for t, a, v in hits)
        po = min(ps.get(o, []), key=lambda x: abs(x[0] - T), default=None)
        allies = []
        for e in mates:
            s = hp.get(e)
            if not s:
                continue
            now = health_at(s, T)
            if not now or now[2] != 0 or now[0] <= 0:
                continue
            g = [gain(s, lost[e], T + k * HEAL_S * TICK, T + (k + 1) * HEAL_S * TICK) for k in (-1, 0, 1)]
            if g[1] is None:
                continue
            ctl = [x for x in (g[0], g[2]) if x is not None]
            base = sum(ctl) / len(ctl) if ctl else 0.0
            recv = g[1] - base
            pe = min(ps.get(e, []), key=lambda x: abs(x[0] - T), default=None)
            dist = math.dist(po[1], pe[1]) / UNITS_PER_M if po and pe else None
            dies = any(T < t <= T + DIE_S * TICK for t in deaths.get(e, []))
            allies.append({"self": e == o, "h": now[0], "mh": now[1], "recv": recv, "dist_m": dist, "dies": dies,
                           "base": base})
        out.append({"holder": o, "tick": T, "fight": fight, "allies": allies})
    return out


def summary(cs, label):
    allies = [a for c in cs for a in c["allies"] if not a["self"]]
    selfs = [a for c in cs for a in c["allies"] if a["self"]]
    # full heal: teammates far below max health (and the holder itself) show it
    deep = [a["recv"] for a in allies + selfs if a["h"] < (1 - FULL_DEFICIT) * a["mh"]
            and (a["dist_m"] is None or a["dist_m"] <= RADIUS_M)]
    full = statistics.median(deep) if deep else float("nan")
    reach = [a for a in allies if a["dist_m"] is not None and a["dist_m"] <= RADIUS_M]
    n = len(cs)
    tot = sum(a["recv"] for a in allies)
    print(f"{label}: {n} casts, {sum(c['fight'] for c in cs) / max(1, n):.2f} in fights; full heal (median of "
          f"{len(deep)} deep-deficit) {full:.0f}")
    print(f"  self heal/cast {sum(a['recv'] for a in selfs) / max(1, n):.0f}; ally heal/cast {tot / max(1, n):.0f} "
          f"(in reach {sum(a['recv'] for a in reach) / max(1, n):.0f}); teammates in reach/cast "
          f"{len(reach) / max(1, n):.2f}, at >=95% hp {sum(a['h'] >= 0.95 * a['mh'] for a in reach) / max(1, len(reach)):.2f}")
    if reach and full == full:
        print(f"  overheal in reach: 1 - received / (full x in reach) = "
              f"{1 - sum(a['recv'] for a in reach) / (full * len(reach)):.2f}")
    dies = sum(a["recv"] for a in allies if a["dies"])
    infight = sum(a["recv"] for c in cs if c["fight"] for a in c["allies"] if not a["self"])
    print(f"  ally heal on teammates dying within {DIE_S:.0f} s: {dies / max(1, tot):.2f}; in fights: "
          f"{infight / max(1, tot):.2f}")
    return {"casts": n, "fight_share": sum(c["fight"] for c in cs) / max(1, n), "full_heal": full,
            "ally_heal_per_cast": tot / max(1, n), "ally_heal_in_fight_per_cast": infight / max(1, n),
            "dying_share": dies / max(1, tot), "self_heal_per_cast": sum(a["recv"] for a in selfs) / max(1, n)}


def sim(souls=SOULS, lineups=LINEUPS):
    """The 3v3's Nova casts, instrumented like the real ones (team_value.py fights, every A hero holding it in turn)."""
    sys.path.insert(0, SIM)
    sys.path.insert(0, HERE)
    import team_value as TV
    from deadsim import Loadout
    import deadsim.team as T
    item = "Healing Nova"
    log = []
    orig = T.heal_ally

    def rec(src, dst, amount, source):
        got = orig(src, dst, amount, source)
        if source == item:
            log.append((id(src), id(dst), src.e.t if hasattr(src.e, "t") else 0.0, amount, got, dst))
        return got
    T.heal_ally = rec
    casts = ally = ally_dies = ask = dmg = selfh = 0.0
    n_f = 0
    try:
        for six in TV.lineups()[:lineups]:
            a = [Loadout(h, TV.popular(h, souls), souls=souls, skill=TV.skill(h)) for h in six[:3]]
            b = [Loadout(h, TV.popular(h, souls), souls=souls, skill=TV.skill(h)) for h in six[3:]]
            for k in range(3):
                base = [dataclasses.replace(x, items=[i for i in x.items if i != item]) for x in a]
                w = list(base)
                w[k] = dataclasses.replace(base[k], items=base[k].items + [item])
                for focus in ("focus", "spread"):
                    for dist in (12.0, 20.0):
                        log.clear()
                        r = T.team_fight(w, b, focus=focus, distance=dist, max_time=TV.MAX_TIME, huddle=1.0,
                                         aoe_share=0.0)
                        n_f += 1
                        dmg += r.fighters[k]["damage"]
                        ts = sorted({round(t, 1) for s_, d_, t, *_ in log if s_ == d_})
                        casts += len(ts) / 4 if ts else 0   # 4 ticks per cast
                        for s_, d_, t, am, got, dst in log:
                            if s_ == d_:
                                selfh += got
                                continue
                            ally += got
                            ask += am
                            if dst.death_time is not None and dst.death_time <= t + DIE_S:
                                ally_dies += got
    finally:
        T.heal_ally = orig
    out = {"fights": n_f, "casts_per_fight": casts / n_f, "ally_heal_per_cast": ally / max(1, casts),
           "self_heal_per_cast": selfh / max(1, casts), "overheal": 1 - ally / max(1, ask),
           "dying_share": ally_dies / max(1, ally), "ally_heal_per_damage": ally / max(1, dmg)}
    print(f"3v3 ({souls}): " + ", ".join(f"{k} {v:.3f}" for k, v in out.items()))
    return out


def per_damage(files, tl_path):
    """Real in-fight ally (and self) Nova heal per holder hero damage over the held time (bulk metadata timelines of
    the same matches: player_damage cumulative per sample), for holders alone with Nova on their team."""
    nova = 2956256701
    tl = {}
    with gzip.open(tl_path, "rt") as f:
        for line in f:
            m = json.loads(line)
            tl[m["match_id"]] = m

    def cum(stats, t):
        prev = (0, 0)
        for r in stats:
            if r[0] >= t:
                return prev[1] + (r[2] - prev[1]) * (t - prev[0]) / max(1, r[0] - prev[0])
            prev = (r[0], r[2])
        return prev[1]
    heal = selfh = dmg = mins = 0.0
    n_c = n_h = 0
    for fn in files:
        mid = int(os.path.basename(fn).split(".")[0])
        if mid not in tl:
            continue
        team = {d["a"]: {"2": "Team0", "3": "Team1"}.get(d["s"]) for d in load(fn)["pawn"]}
        by = collections.defaultdict(list)
        for c in casts(fn):
            by[c["holder"]].append(c)
        hold = [p for p in tl[mid]["players"] if any(it[0] == nova for it in p["items"])]
        for p in hold:
            if sum(q["team"] == p["team"] for q in hold) > 1:
                continue
            spans = [(t0, ts or 1e9) for iid, t0, ts in p["items"] if iid == nova and t0 > 0]
            pawns = [e for e in by if team.get(e) == p["team"]]
            if not spans or len(pawns) != 1:
                continue
            a, b = spans[0][0], min(spans[0][1], tl[mid]["duration_s"])
            mine = [c for c in by[pawns[0]] if a <= c["tick"] / TICK <= b + 5]
            heal += sum(x["recv"] for c in mine if c["fight"] for x in c["allies"] if not x["self"])
            selfh += sum(x["recv"] for c in mine if c["fight"] for x in c["allies"] if x["self"])
            dmg += cum(p["stats"], b) - cum(p["stats"], a)
            mins += (b - a) / 60
            n_c += len(mine)
            n_h += 1
    return {"holders": n_h, "casts_per_min": n_c / max(1e-9, mins), "ally_heal_per_damage": heal / max(1.0, dmg),
            "self_heal_per_damage": selfh / max(1.0, dmg)}


def write(real, sm, credited, reach, n):
    """Record the measurement in data/ally_heal.json (Healing Nova: measured_*; its applied factor is unchanged)."""
    path = os.path.join(SIM, "data", "ally_heal.json")
    with open(path) as f:
        d = json.load(f)
    e = d["items"].setdefault("Healing Nova", {})
    e.update({"replay_source": f"nova_heal.py: {n} post-hotfix Phantom+ replays with Nova, {real['casts']} casts",
              "real_ally_heal_per_cast": round(real["ally_heal_per_cast"]),
              "sim_ally_heal_per_cast_at_real_reach": round(sm["ally_heal_per_cast"] * reach / 2.0),
              "real_dying_share": round(real["dying_share"], 3), "sim_dying_share": round(sm["dying_share"], 3),
              "real_ally_heal_per_damage": round(real["ally_heal_per_damage"], 4),
              "sim_ally_heal_per_damage_credited": round(credited, 4),
              "measured_factor": round(real["ally_heal_per_damage"] / credited, 2)})
    with open(path, "w") as f:
        json.dump(d, f, indent=1)


def main():
    args = sys.argv[1:]
    half = None
    if "--half" in args:
        i = args.index("--half")
        half = int(args[i + 1])
        args = args[:i] + args[i + 2:]
    files = sorted(glob.glob(os.path.join(args[0], "*.ndjson.gz")))
    if half is not None:
        files = [f for f in files if int(os.path.basename(f).split(".")[0]) % 2 == half]
    cs = []
    for fn in files:
        try:
            cs += casts(fn)
        except Exception as e:  # noqa: BLE001
            print("skip", fn, e, file=sys.stderr)
    print(f"{len(files)} replays")
    real = summary(cs, "real")
    tl = os.path.join(os.path.dirname(os.path.normpath(args[0])), "timelines.jsonl.gz")
    if os.path.exists(tl):
        real.update(per_damage(files, tl))
        print(f"  holders {real['holders']}, casts per held min {real['casts_per_min']:.3f}, in-fight ally heal per "
              f"holder hero damage {real['ally_heal_per_damage']:.3f}, self heal per damage {real['self_heal_per_damage']:.3f}")
    if "--sim" in args or "--write" in args:
        sm = sim()
        sys.path.insert(0, os.path.join(ROOT, "damage", "scripts"))
        import overall_search as O
        reach = O.near("allies", RADIUS_M, SOULS)
        credited = sm["ally_heal_per_damage"] * reach / 2.0   # team_value.json reach_sim 2, scaled by real reach
        print(f"3v3 ally heal per holder damage {sm['ally_heal_per_damage']:.3f} x real teammates within "
              f"{RADIUS_M:.0f} m {reach:.2f} / 2 = {credited:.3f} credited; real {real.get('ally_heal_per_damage', float('nan')):.3f} "
              f"-> real / credited {real.get('ally_heal_per_damage', float('nan')) / credited:.2f}")
        if "--write" in args:
            write(real, sm, credited, reach, len(files))
    if "--dist" in args:
        rows = [(a["dist_m"], a["recv"]) for c in cs for a in c["allies"]
                if not a["self"] and a["dist_m"] is not None and a["h"] < 0.65 * a["mh"]]
        for lo in range(0, 60, 4):
            v = [r for d, r in rows if lo <= d < lo + 4]
            if v:
                print(f"  {lo:2d}-{lo + 4:2d} m: n {len(v):3d} median recv {statistics.median(v):.0f}")


if __name__ == "__main__":
    main()
