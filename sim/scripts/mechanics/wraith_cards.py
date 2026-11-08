"""Wraith Card Trick in replays: per engagement (Wraith vs a hero, gap >= 10 s before), card hits in the first 3 / 6 s,
cards per engagement, gap from first Wraith damage to first card, cards within 1 / 3 s of the first one, card size,
and the histogram of the opening burst (heroes/wraith.py ENTRY_HAND).

usage: python3 -I wraith_cards.py <raw dir> [raw dir ...]
"""
import collections, glob, gzip, json, os, sys, statistics
CARD = 1999680326; WRAITH = 7
WEAP = {w["id"] for w in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..",
                                                      "data", "game", "weapons.json")))}
seen = {}
for d in sys.argv[1:]:
    for f in glob.glob(os.path.join(d, "*.ndjson.gz")): seen.setdefault(os.path.basename(f), f)
A1=[];A3=[];DUR=[]
first3 = []; first6 = []; per = []; delay = []; size = []; nofirst = 0; eng = 0
for fn in sorted(seen.values()):
    ctl = {}; ev = []
    for line in gzip.open(fn, "rt"):
        r = json.loads(line)
        if r["k"] == "ctl": ctl[r["a"]] = int(str(r.get("s") or "0").split("|")[0])
        elif r["k"] == "dmg" and r.get("s"): ev.append((r["tick"], r["a"] // 100000, r["a"] % 100000, int(r["s"].split("|")[0]), r["v"]))
    ev.sort()
    heroes = set(ctl)
    for me, hid in ctl.items():
        if hid != WRAITH: continue
        mine = [e for e in ev if e[1] == me and e[2] in heroes]
        if not any(e[3] == CARD for e in mine): continue
        # engagements: clusters of Wraith's hero damage with gaps >= 10 s
        cl = []
        for e in mine:
            if cl and e[0] - cl[-1][-1][0] < 640: cl[-1].append(e)
            else: cl.append([e])
        for c in cl:
            if c[-1][0] - c[0][0] < 3 * 64: continue   # skip pokes
            eng += 1
            t0 = c[0][0]
            cards = [e for e in c if e[3] == CARD]
            size += [e[4] for e in cards]
            first3.append(sum(1 for e in cards if e[0] - t0 <= 192)); first6.append(sum(1 for e in cards if e[0] - t0 <= 384))
            per.append(len(cards))
            if cards:
                delay.append((cards[0][0] - t0) / 64); A1.append(sum(1 for e in cards if e[0]-cards[0][0] <= 64)); A3.append(sum(1 for e in cards if e[0]-cards[0][0] <= 192)); DUR.append((c[-1][0]-t0)/64)
            else: nofirst += 1
print(f"{len(seen)} replays, {eng} engagements (>=3 s)")
print("cards per engagement mean", round(statistics.mean(per), 2), "first 3 s", round(statistics.mean(first3), 2), "first 6 s", round(statistics.mean(first6), 2))
print("share with no card", round(nofirst / eng, 3), "first-card delay median", statistics.median(delay), "quartiles", sorted(delay)[len(delay)//4], sorted(delay)[3*len(delay)//4])
print("dist first 3 s", collections.Counter(first3).most_common(8))
print("card size median", statistics.median(size))
print("after first card within 1s", round(statistics.mean(A1),2), "within 3s", round(statistics.mean(A3),2), "engagement length median", statistics.median(DUR))
print("A3 hist with zeros", sorted(collections.Counter(A3 + [0]*nofirst).items()))
