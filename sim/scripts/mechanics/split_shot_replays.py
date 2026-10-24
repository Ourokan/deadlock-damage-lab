"""Split Shot and Mercurial Magnum in Phantom+ replays (Deadlock API demo queries): the numbers behind
mechanics.SPLIT_PRIMARY_HIT / SPLIT_SECONDARY_COVER and Mercurial Magnum's bullet bonus lasting its buff.

usage: python3 -I split_shot_replays.py fetch <work dir> <sample.jsonl.gz> [n_vyper_matches=45] [n_other=40]
       python3 -I split_shot_replays.py report <work dir> [out.json]

fetch picks matches of the sample with replay salts where someone holds Vyper, Mercurial Magnum or Split Shot, and
saves every hero-vs-hero DamageEvent (one demo query per match) to <work>/raw/<match>.ndjson. Gun hits carry the
hero's weapon id (data/game/weapons.json); Split Shot pellets and Mercurial procs carry the item id.
report, per hero:
- Mercurial Magnum: share of gun hits after the holder's first proc that carry a proc (same victim, +-1 tick). A Vyper
  clip lasts 1.7 s, so a bonus that ended at reload would cover far less than it does.
- Split Shot: activations = runs of its hits with gaps under 6 s. In the 5 s after each activation's first hit:
  share of the holder's gun damage (after his first use) inside windows, Split Shot hits on the main target (most
  gun damage) per landed gun bullet, damage on other heroes / on the main target.
"""
import bisect
import collections
import concurrent.futures as cf
import glob
import gzip
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fight_patterns"))
ROOT = os.path.join(HERE, "..", "..", "..")
MM, SS, VYPER = 3919289022, 3647584222, 58
T = 64.0   # ticks per second
API = "https://api.deadlock-api.com/v1"
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}
SQL = """SELECT 'dmg' AS k, CAST(entindex_attacker AS BIGINT) * 100000 + CAST(entindex_victim AS BIGINT) AS a, CAST(ability_id AS VARCHAR) AS s, CAST(damage AS DOUBLE) AS v, tick FROM DamageEvent WHERE attacker_class = 1 AND victim_class = 1 AND damage > 0"""


def has_salt(m):
    try:
        req = urllib.request.Request(f"{API}/matches/{m}/salts", headers=UA)
        return m if json.load(urllib.request.urlopen(req, timeout=30)).get("replay_salt") else None
    except Exception:  # noqa: BLE001
        return None


def fetch(work, sample, n_vyper=45, n_other=40):
    from demo_query import run
    vy, other = set(), set()
    for line in gzip.open(sample):
        m = json.loads(line)
        for p in m["players"]:
            ids = {i[0] for i in p["items"]}
            if p["hero_id"] == VYPER:
                vy.add(m["match_id"])
            elif MM in ids or SS in ids:
                other.add(m["match_id"])
    with cf.ThreadPoolExecutor(8) as ex:
        vy = [m for m in ex.map(has_salt, sorted(vy, reverse=True)) if m][:n_vyper]
        other = [m for m in ex.map(has_salt, sorted(other - set(vy), reverse=True)) if m][:n_other]
    os.makedirs(os.path.join(work, "raw"), exist_ok=True)

    def one(m):
        out = os.path.join(work, "raw", f"{m}.ndjson")
        if not os.path.exists(out):
            try:
                run(m, SQL, out)
            except BaseException as e:  # noqa: BLE001
                print(m, e, flush=True)
        return m
    with cf.ThreadPoolExecutor(4) as ex:
        for i, m in enumerate(ex.map(one, vy + other)):
            print(i, m, flush=True)


def attackers(fn):
    ev = collections.defaultdict(list)
    for line in open(fn):
        r = json.loads(line)
        if r.get("k") == "dmg" and r.get("s"):
            ev[r["a"] // 100000].append((r["tick"], r["a"] % 100000, int(r["s"]), r["v"]))
    for es in ev.values():
        es.sort()
        yield es


def report(work, out=None):
    weap = {w["id"]: w["hero"] for w in json.load(open(os.path.join(ROOT, "data", "game", "weapons.json")))}
    mm = collections.defaultdict(lambda: [0, 0])
    ss = collections.defaultdict(collections.Counter)
    for fn in glob.glob(os.path.join(work, "raw", "*.ndjson")):
        for es in attackers(fn):
            hero = collections.Counter(weap[i] for _, _, i, _ in es if i in weap).most_common(1)
            if not hero:
                continue
            hero = hero[0][0]
            gun = [(t, v, d) for t, v, i, d in es if i in weap]
            procs = {(t + k, v) for t, v, i, _ in es if i == MM for k in (-1, 0, 1)}
            first = next((t for t, v, _ in gun if (t, v) in procs), None)
            if first is not None:
                for t, v, _ in gun:
                    if t >= first:
                        mm[hero][0] += 1
                        mm[hero][1] += (t, v) in procs
            hits = [e for e in es if e[2] == SS]
            if not hits:
                continue
            c = ss[hero]
            starts = [e[0] for k, e in enumerate(hits) if k == 0 or e[0] - hits[k - 1][0] > 6 * T]
            ticks = [e[0] for e in es]
            for s0 in starts:
                g, gh, sd, sh = (collections.Counter() for _ in range(4))
                for t, v, i, d in es[bisect.bisect_left(ticks, s0):bisect.bisect_right(ticks, s0 + 5 * T)]:
                    if i in weap:
                        g[v] += d
                        gh[v] += 1
                    elif i == SS:
                        sd[v] += d
                        sh[v] += 1
                if not g:
                    continue
                main = g.most_common(1)[0][0]
                c["acts"] += 1
                c["gun_window"] += sum(g.values())
                c["gun_main"] += g[main]
                c["gun_hits"] += sum(gh.values())
                c["ss_main"] += sd[main]
                c["ss_hits_main"] += sh[main]
                c["ss_side"] += sum(sd.values()) - sd[main]
            c["gun_after_first"] += sum(d for t, _, d in gun if t >= hits[0][0])
            c["ss_total"] += sum(e[3] for e in hits)
    res = {"mercurial": {}, "split_shot": {}}
    print("Mercurial Magnum: share of gun hits after the first proc that carry one")
    for h, (n, k) in sorted(mm.items(), key=lambda x: -x[1][0]):
        res["mercurial"][h] = {"hits": n, "share": round(k / n, 3)}
        print(f"  {h:14s} {k / n:.2f} of {n} hits")
    print("Split Shot (5 s after each activation)")
    for h, c in sorted(ss.items(), key=lambda x: -x[1]["acts"]):
        if c["acts"] < 5:
            continue
        row = {"activations": c["acts"],
               "ss_per_gun_after_first_use": round(c["ss_total"] / c["gun_after_first"], 3),
               "gun_share_in_windows": round(c["gun_window"] / c["gun_after_first"], 3),
               "main_hits_per_gun_hit": round(c["ss_hits_main"] / c["gun_hits"], 3),
               "main_dmg_per_gun_main": round(c["ss_main"] / c["gun_main"], 3),
               "side_per_main": round(c["ss_side"] / c["ss_main"], 3)}
        res["split_shot"][h] = row
        print(f"  {h:14s} " + ", ".join(f"{k} {v}" for k, v in row.items()))
    acts = sum(r["activations"] for r in res["split_shot"].values())
    main = sum(r["main_hits_per_gun_hit"] * r["activations"] for r in res["split_shot"].values()) / acts
    side = sum(r["side_per_main"] * r["activations"] for r in res["split_shot"].values()) / acts
    res["split_shot_pooled"] = {"main_hits_per_gun_hit": round(main, 3), "side_per_main": round(side, 3)}
    print(f"  pooled by activations: main hits per gun hit {main:.2f}, side / main {side:.2f}")
    if out:
        with open(out, "w") as fh:
            json.dump(res, fh, indent=1)


if __name__ == "__main__":
    if sys.argv[1] == "fetch":
        fetch(sys.argv[2], sys.argv[3], *(int(x) for x in sys.argv[4:6]))
    else:
        report(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
