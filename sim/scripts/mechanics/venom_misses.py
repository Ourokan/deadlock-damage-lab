"""Vyper's Lethal Venom in replays: what becomes of each cast (heroes/viper.py VENOM_MISS).

For every Lethal Venom cast: landed (venom damage on a hero within 3.3 s), no fight (no hero damage by Vyper within
2 s of the cast), or a miss: target likely dead (it deals and takes no damage from 3 to 20 / 6 s after the cast),
still in the fight (it takes damage 3-6 s after) or left. Also venom hits with no cast in the 3.2 s before (T3 gun
build-up) by fifth of the match.
First run 2026-11-08 on 47 Phantom+ Vyper matches: 772 casts, landed 491, no fight 100, dead 79, left 54, still in
the fight 48 -> VENOM_MISS = (54 + 48) / 672 in-fight casts = 0.152; 36.5% of venom hits are build-up ones.

usage: python3 -I venom_misses.py <work dir>      (/mnt/project-files/analysis/work)
"""
import bisect, collections, glob, gzip, json, os, sys
B = sys.argv[1].rstrip("/") + "/"
VYPER, VENOM = 58, "3428732129"
dmgd, castd = {}, {}
for d in ["fight_length/raw", "gun_phase/raw", "dynamo_replays/raw", "viscous_replays/raw", "victor_battery/raw",
          "ivy_kudzu/raw", "kelvin_reverb", "ally_target/paige", "ally_target/solomon"]:
    for f in glob.glob(B + d + "/*.ndjson.gz"): dmgd.setdefault(os.path.basename(f), f)
for d in ["cast_timing/raw", "item_use/raw", "dynamo_replays/casts"]:
    for f in glob.glob(B + d + "/*.ndjson.gz"): castd.setdefault(os.path.basename(f), f)
res = collections.Counter(); hits = orph = 0
for fn, path in dmgd.items():
    if fn not in castd: continue
    ctl, alld = {}, []
    for line in gzip.open(path, "rt"):
        r = json.loads(line)
        if r["k"] == "ctl": ctl[r["a"]] = int(str(r.get("s") or "0").split("|")[0])
        elif r["k"] == "dmg": alld.append((r["tick"], r["a"] // 100000, r["a"] % 100000, (r.get("s") or "").split("|")[0], r["v"]))
    me = {a for a, h in ctl.items() if h == VYPER}
    if not me: continue
    alld.sort(); ticks = [e[0] for e in alld]   # events are not time-sorted in the dumps
    def win(t0, t1): return alld[bisect.bisect_left(ticks, t0):bisect.bisect_right(ticks, t1)]
    cs = sorted((r["tick"], r["a"]) for r in map(json.loads, gzip.open(castd[fn], "rt"))
                if r["k"] == "cast" and str(r["s"]).split("|")[0] == VENOM and r["a"] in me)
    for e in alld:
        if e[1] in me and e[3] == VENOM and e[2] in ctl:
            hits += 1
            orph += not any(0 <= e[0] - t <= 3.2 * 64 + 8 for t, a in cs if a == e[1])
    for t, a in cs:
        w3 = win(t, t + int(3.3 * 64))
        hit = [e for e in w3 if e[1] == a and e[3] == VENOM and e[2] in ctl]
        if hit: res["landed"] += 1; continue
        near = [e for e in win(t - 128, t + 128) if e[1] == a and e[2] in ctl]
        if not near: res["no fight"] += 1; continue
        m = collections.Counter(e[2] for e in near).most_common(1)[0][0]
        if any(e[2] == m for e in win(t + 3 * 64, t + 6 * 64)): res["miss: still in the fight"] += 1
        elif any(e[1] == m for e in win(t + 3 * 64, t + 20 * 64)): res["miss: left"] += 1
        else: res["miss: target likely dead"] += 1
fight = sum(res.values()) - res["no fight"]
print(dict(res), "casts", sum(res.values()))
print("miss on a living target per in-fight cast", round((res["miss: left"] + res["miss: still in the fight"]) / max(1, fight), 3),
      "dead", round(res["miss: target likely dead"] / max(1, fight), 3))
print("venom hits", hits, "build-up (no cast before)", round(orph / max(1, hits), 3))
