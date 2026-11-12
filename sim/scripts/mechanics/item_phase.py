"""Item damage by game phase from the damage audit's fifths (2026-11-12).

An item's landing factor (data/item_landing.json, item_landing_heroes rows) is one number over the match, but some
items' real share of their holders' damage grows differently over the match than the sim's: in the fresh audit
(4,000 post-hotfix Phantom+ matches) Tankbuster read 0.72x real in the second fifth and 1.03x in the last, Toxic
Bullets 0.76 -> 1.04, Headhunter 0.91 -> 1.11, Mystic Shot 0.93 -> 1.15, Quicksilver 0.93 -> 1.20; Split Shot and
Ricochet the other way. Like melee_phase, this fits a per-item phase curve to the audit's own fifths:
rel(fifth) = real share / sim share pooled over heroes (players-weighted), over its real-damage-weighted mean (so the
whole-match level, item_landing, stays), shrunk toward 1 by the fifth's weight (players x real share, K), placed at
the fifth's mean net worth in the sample (log mean of every player's net worth at the fifth's middle).
Mechanics.item_phase multiplies the item's landing factor by rel at the holder's net worth (linear in ln net worth,
flat outside). Only items in ITEMS (held the split-half audit) get rows.

usage: python3 -I item_phase.py <audit.json with AUDIT_FIFTH_SOURCES=1 AUDIT_FIFTH_MIN=0.0005> <sample.jsonl.gz>
       [--all] [--write]
"""
import bisect
import collections
import gzip
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
OUT = os.path.join(ROOT, "data", "item_phase.json")
K = 60.0          # players x share of shrinkage per fifth
MIN_W = 200.0     # items below this summed weight are left out
# kept: better held-out per-fifth error on both match_id halves (fit on one half's audit, audit the other; 2026-11-12)
ITEMS = ("upgrade_crackshot", "upgrade_quick_silver", "upgrade_headhunter", "upgrade_magic_shock", "upgrade_express_shot",
         "upgrade_melee_charge", "upgrade_cold_front", "upgrade_toxic_bullets", "upgrade_mystic_reverb",
         "upgrade_chain_lightning", "upgrade_weapon_backstabber", "upgrade_magic_burst")
# --all fits every item above MIN_W


def fifth_net_worth(sample, half=None):
    acc = [[0.0, 0] for _ in range(5)]
    for line in gzip.open(sample):
        m = json.loads(line)
        if half is not None and m["match_id"] % 2 != half:
            continue
        T = m["duration_s"]
        for p in m["players"]:
            st = p.get("stats") or []
            ts = [s["time_stamp_s"] for s in st]
            for b in range(5):
                i = bisect.bisect_right(ts, (b + 0.5) / 5 * T) - 1
                if i >= 0 and st[i].get("net_worth"):
                    acc[b][0] += math.log(st[i]["net_worth"])
                    acc[b][1] += 1
    return [math.exp(s / n) for s, n in acc]


def fit(audit, nws, only=None):
    acc = collections.defaultdict(lambda: [[0.0, 0.0] for _ in range(5)])
    for v in audit["heroes"].values():
        w = v["players"]
        for f, fs in enumerate(v.get("fifth_sources") or []):
            for k, (r, s) in (fs or {}).items():
                if k.startswith("upgrade_"):
                    acc[k][f][0] += w * r
                    acc[k][f][1] += w * s
    out = {}
    for k, a in acc.items():
        if (only is not None and k not in only) or sum(x[0] for x in a) < MIN_W:
            continue
        pts = [(f, r / s, r) for f, (r, s) in enumerate(a) if r > 0 and s > 0]
        mean = sum(q * w for _, q, w in pts) / sum(w for _, _, w in pts)
        bins = []
        for f, q, w in pts:
            rel = 1.0 + (q / mean - 1.0) * w / (w + K)
            bins.append({"net_worth": round(nws[f]), "fifth": f, "real_over_sim": round(q, 3), "weight": round(w, 1),
                         "rel": round(rel, 4)})
        out[k] = {"bins": bins}
    return out


def main():
    args = sys.argv[1:]
    from deadsim import game
    G = game()
    audit = json.load(open(args[0]))
    nws = fifth_net_worth(args[1])
    rows = fit(audit, nws, None if "--all" in args or not ITEMS else set(ITEMS))
    names = {it.class_name: it.name for it in G.items.values()}
    for k, v in sorted(rows.items(), key=lambda x: -sum(b["weight"] for b in x[1]["bins"])):
        v["name"] = names.get(k, k)
        print(f"{v['name']:24s}", " ".join(f"{b['net_worth']}:{b['rel']:.2f}" for b in v["bins"]))
    if "--write" in args:
        json.dump({"source": f"scripts/mechanics/item_phase.py ({os.path.basename(args[0])}, {os.path.basename(args[1])})",
                   "note": "item damage x rel(nw) at the holder's net worth, linear in ln nw between bins, flat outside "
                           "(Mechanics.item_phase)", "items": rows}, open(OUT, "w"), indent=1)
        print("->", OUT)


if __name__ == "__main__":
    main()
