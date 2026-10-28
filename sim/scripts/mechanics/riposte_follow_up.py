"""How often real Apollos land Riposte's follow-up melee: fencer.FOLLOW_UP_RATE and FOLLOW_UP_DELAY.

A countered Riposte stuns the attacker: in the cc_time replays that is a status notification (k "nt", v 0) from
Apollo's pawn on the victim with Riposte's ability id. The follow-up is Apollo's own basic melee (the game books it
as ability_melee_fencer, Riposte itself deals no damage), so a counter is followed up when one of Apollo's basic melee
hits lands on the stunned hero within WINDOW s (fight_length replays, every hero-vs-hero DamageEvent).
Phantom+ 2026-10-28: 691 counters in 43 replays with Apollo, 53% followed up within 1.2 s (55% within 2 s, 56% within
4 s), median 0.75 s after the stun; the victim died within 1.5 s after 5%. The follow-ups are 40% of Apollo's basic
melee hits and 52% of their damage.

usage: python3 -I riposte_follow_up.py
"""
import bisect
import collections
import gzip
import json
import os

CC = "/mnt/project-files/analysis/work/cc_time/raw/"
RAW = "/mnt/project-files/analysis/work/fight_length/raw/"
T = 64
APOLLO = 77
RIPOSTE = "2006773718"      # ability_fencer_riposte
MELEE = "1224118768"        # ability_melee_fencer
WINDOW = 1.2
DEDUP = 2.0                 # one counter per victim within this many s (the notification repeats)


def main():
    st = collections.Counter()
    lags, dmg = [], collections.Counter()
    for f in sorted(os.listdir(CC)):
        if not os.path.exists(RAW + f):
            continue
        hero, ev = {}, []
        for line in gzip.open(RAW + f, "rt"):
            r = json.loads(line)
            if r["k"] == "ctl":
                hero[r["a"]] = int(r["s"])
            elif r["k"] == "dmg" and r.get("s", "").split("|")[0] == MELEE:
                ev.append(r)
        mel = []
        for r in ev:   # the pawn -> hero rows can come after the damage
            a, v = divmod(r["a"], 100000)
            if hero.get(a) == APOLLO and v in hero and hero[v] != APOLLO:
                mel.append((r["tick"] / T, v, r["v"]))
        ap = {e for e, h in hero.items() if h == APOLLO}
        if not ap:
            continue
        st["replays"] += 1
        stuns, last = [], {}
        for line in gzip.open(CC + f, "rt"):
            r = json.loads(line)
            if r["k"] != "nt" or r["v"] != 0 or not r["s"].startswith(RIPOSTE + "|"):
                continue
            a, v = divmod(r["a"], 100000)
            if a in ap and v in hero and hero[v] != APOLLO:
                t = r["tick"] / T
                if t - last.get(v, -1e9) > DEDUP:
                    stuns.append((t, v))
                last[v] = t
        mel.sort()
        mt = [m[0] for m in mel]
        for t, v in stuns:
            st["counters"] += 1
            nxt = [m for m in mel[bisect.bisect_right(mt, t):bisect.bisect_right(mt, t + 4)] if m[1] == v]
            if nxt:
                lag = nxt[0][0] - t
                st["within 4 s"] += 1
                st["within 2 s"] += lag < 2
                if lag < WINDOW:
                    st["followed"] += 1
                    lags.append(lag)
        for t, v, x in mel:
            fol = any(vv == v and 0 < t - ts < WINDOW for ts, vv in stuns)
            dmg["hits"] += 1
            dmg["damage"] += x
            dmg["follow-up hits"] += fol
            dmg["follow-up damage"] += x * fol
    lags.sort()
    print(dict(st))
    print(f"followed up within {WINDOW} s: {st['followed'] / st['counters']:.3f}, median lag "
          f"{lags[len(lags) // 2]:.2f} s")
    print(f"follow-ups: {dmg['follow-up hits'] / dmg['hits']:.2f} of Apollo's basic melee hits, "
          f"{dmg['follow-up damage'] / dmg['damage']:.2f} of their damage")


if __name__ == "__main__":
    main()
