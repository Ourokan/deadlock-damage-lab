"""Real kill stacks of Glass Cannon and Trophy Collector holders by net worth (validation/kill_stacks.md,
build.KILL_STACKS_BY_NW).

Stat timelines (fetch_rates.py, every ~180-300 s: net worth, hero damage, kills, deaths, assists) and item buys with
sell times. From the buy to the sale (or match end), stacks follow the timeline: Glass Cannon +1 per kill, -1 per
death, 0..8; Trophy Collector +1 per kill or assist, kept through death, 0..16. Kills and deaths inside one snapshot
interval are netted. Prints the mean stacks over each interval's midpoint, weighted by the holder's hero damage in it,
per 10k net worth bin, for both match-id halves and pooled.

usage: python3 -I kill_stacks.py [timeline dir]   (default: project folder analysis/work/fight_rate_post)
"""
import collections
import glob
import gzip
import json
import os
import sys

ITEMS = {"Glass Cannon": (365620721, 8, False), "Trophy Collector": (3074274290, 16, True)}   # id, cap, assists count


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project-files/analysis/work/fight_rate_post"
    acc = {n: collections.defaultdict(lambda: [0.0] * 4) for n in ITEMS}
    holders = collections.Counter()
    for path in sorted(glob.glob(os.path.join(d, "*.jsonl.gz"))):
        for line in gzip.open(path, "rt"):
            m = json.loads(line)
            half = m["match_id"] % 2
            for p in m["players"]:
                for name, (iid, cap, assists) in ITEMS.items():
                    buys = [it for it in p["items"] if it[0] == iid]
                    if not buys:
                        continue
                    holders[name] += 1
                    t0, t1 = buys[0][1], buys[0][2] or m["duration_s"]
                    stacks, prev = 0.0, None
                    for s in p["stats"]:
                        if prev is not None and s[0] > t0 and prev[0] < t1:
                            a, b = max(prev[0], t0), min(s[0], t1)
                            frac = (b - a) / max(1, s[0] - prev[0])
                            gain = (s[4] - prev[4]) + ((s[6] - prev[6]) if assists else 0)
                            loss = 0 if assists else (s[5] - prev[5])
                            start = stacks
                            stacks = min(cap, max(0.0, stacks + (gain - loss) * frac))
                            w = (s[2] - prev[2]) * frac
                            row = acc[name][min(60000, s[1] // 10000 * 10000)]
                            row[2 * half] += w * (start + stacks) / 2
                            row[2 * half + 1] += w
                        prev = s
    for name in ITEMS:
        print(f"{name}: {holders[name]} holders\n  net worth  pooled  half A  half B")
        for nb, r in sorted(acc[name].items()):
            pooled = (r[0] + r[2]) / max(1, r[1] + r[3])
            print(f"  {nb:>6}+  {pooled:6.2f}  {r[0] / max(1, r[1]):6.2f}  {r[2] / max(1, r[3]):6.2f}")


if __name__ == "__main__":
    main()
