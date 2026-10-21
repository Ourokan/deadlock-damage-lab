"""Full game build paths: one build that grows from 10k to 50k net worth and stays strong at every stage.

Tyler asked (2026-10-21) for optimal full game builds that flow from low to high souls, get value at every stage,
hit the investment spikes and keep agency through the whole game. The best overall build at each net worth
(overall_search.py) doesn't line up from one net worth to the next, so this search builds a path instead:

- Stages: the five search budgets (10k/18k/27k/37k/50k net worth). Each stage is scored with the overall test
  (overall_search.Evaluator: damage dealt before dying vs the 41 typical real builds of the rank bracket, enemy fights
  back, counterplay on), relative to that net worth's most popular real build (1.0 = popular).
- Each stage keeps the previous stage's items. Upgrading a held component is free (the game credits it). Selling
  refunds half the cost, so the lost half stays spent for the rest of the game, and a sale must beat the best
  keep-everything build at that stage by SELL_MARGIN per item sold ("sell only when it clearly pays").
- Path score = mean of the stage scores with the weakest stage counted twice, so a path can't buy a strong late game
  with a weak stage (agency at every point of the game).
- Search: three starts at 10k (the best 10k build, the runner-up, and one built from the late game target's items
  and components), each grown stage by stage with a constrained local search (fill the new souls, then swaps on the
  16-enemy screening pool, best few confirmed on all 41). The best complete path wins.
- Buy order inside each stage, starting from nothing: the piece (item or component) with the most fight value per
  soul at the next stage's enemies, where two pieces bought together count as a pair when only the pair crosses a slot
  investment threshold (the 4800-soul jump is the big one: weapon 18% -> 46%). Every threshold crossed is listed
  as a spike with the net worth it lands at.

Same budget rules as the other searches: item budget per net worth, at most 12 items, the bracket's tier caps
(build_pool.TIER_STEPS) at each stage.

usage: python3 scripts/game_path.py [--workers 4] [--heroes Haze] [--bracket phantom]
Reads work/jobs_overall_<bracket>/ when present (late game target, best build per stage for comparison).
Writes work/jobs_path_<bracket>/<hero_id>.json (resumes); scripts/export_path.py builds out/path/.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

import overall_search as O  # noqa: E402
from build_pool import BRACKETS, BUDGETS, PRIMARY, item_budget  # noqa: E402
from buy_order import cap_net_worth, net_worth_for  # noqa: E402

S = O.S
REFUND = 0.5            # share of an item's cost a sale gives back
SELL_MARGIN = 0.03      # a sale must add this much stage score (share of the popular build's) per item sold
ROUNDS = 3              # swap rounds per stage after the fill
PROPOSALS_S = 12
PROPOSALS_F = 3
TOP_SCAN = 30           # candidates rescanned while filling, after one full scan
SLOTS = ("weapon", "vitality", "spirit")


def jobs_dir(bracket):
    return os.path.join(ROOT, "work", "jobs_path_" + bracket)


def path_score(scores):
    return (sum(scores) + min(scores)) / (len(scores) + 1)


def comps(i):
    return S.component_ids(S.G().items[i])


def sold_items(kept, items):
    """Kept items no longer held, directly or as a component of a held upgrade."""
    up = set().union(*(comps(j) for j in items)) if items else set()
    return [i for i in kept if i not in items and i not in up]


def with_item(cur, j):
    """cur plus j; held components of j are consumed (upgrade credit)."""
    c = comps(j)
    return [i for i in cur if i not in c] + [j]


class Ctx:
    def __init__(self, hero, bracket):
        self.hero, self.bracket = hero, bracket
        self.pools, self.ev, self.cand = {}, {}, {}

    def evaluator(self, b):
        if b not in self.ev:
            self.pools[b] = S.load_pools(b)
            self.ev[b] = O.Evaluator(self.hero, b, self.pools[b])
            self.cand[b] = S.candidates(item_budget(b), self.pools[b]["usage"])
        return self.ev[b]

    def popular(self, b):
        self.evaluator(b)
        return S.popular_build(self.hero, item_budget(b), self.pools[b])

    @property
    def fights(self):
        return sum(e.fights for e in self.ev.values())


def stage_search(ctx, b, kept, waste, seed):
    """Best builds at budget b that keep `kept` (sales allowed, see SELL_MARGIN), starting from `seed`.
    Returns [(adjusted score, score, items, sold, waste)] best first."""
    g = S.G()
    ev, limit, cand = ctx.evaluator(b), item_budget(b), ctx.cand[b]
    archive = {}

    def fits(items):
        if not S.valid(list(items), limit):
            return None
        sold = sold_items(kept, items)
        w = waste + REFUND * S.cost(sold)
        return (sold, w) if S.cost(items) + w <= limit else None

    def full(items):
        key = tuple(sorted(items))
        if key not in archive:
            sold, w = fits(key)
            sc = ev.run(key, "F")
            archive[key] = (sc - SELL_MARGIN * len(sold), sc, list(key), sold, w)
        return archive[key][0]

    # fill: add the item with the most screening-pool value per soul, the price floored at the souls left per free
    # slot so cheap items don't use up the 12 slots
    cur = list(seed) if fits(seed) else list(kept)
    scan, first = list(cand), True
    while True:
        base = ev.run(cur, "S")
        slack = limit - waste - S.cost(cur)
        vals = {}
        for j in scan:
            if j in cur or any(j in comps(i) for i in cur):
                continue
            new = with_item(cur, j)
            if fits(new) is None:
                continue
            paid = S.cost(new) - S.cost(cur)
            floor = slack / max(1, S.MAX_ITEMS - len(cur))
            vals[j] = (ev.run(new, "S") - base) / max(paid, floor, 1)
        if first:
            scan, first = sorted(vals, key=lambda j: -vals[j])[:TOP_SCAN], False
        good = [j for j in vals if vals[j] > 0]
        if not good:
            break
        cur = with_item(cur, max(good, key=lambda j: vals[j]))
    cur_f = full(cur)

    # swaps, as in search.search: measured add / remove values on S, proposals confirmed on F. The first round
    # scans every candidate (the fill only saw the ones that still fit), later rounds the best of those.
    scan = cand
    for rnd in range(ROUNDS):
        base = ev.run(cur, "S")
        add_v = {}
        for j in scan:
            if j in cur:
                continue
            add_v[j] = ev.run(with_item([i for i in cur if j not in comps(i)], j), "S") - base
        if rnd == 0:
            scan = list(dict.fromkeys(sorted(add_v, key=lambda j: -add_v[j] / g.items[j].cost)[:TOP_SCAN]
                                      + sorted(add_v, key=lambda j: -add_v[j])[:15]))
        rem_v = {i: base - ev.run([x for x in cur if x != i], "S") for i in cur}
        adds = sorted(add_v, key=lambda j: -add_v[j])[:20]
        props = set()

        def propose(remove, add):
            new = [i for i in cur if i not in remove]
            for j in add:
                new = with_item([i for i in new if j not in comps(i)], j)
            key = tuple(sorted(new))
            if key not in archive and fits(key) is not None:
                n_sold = len(sold_items(kept, key))
                pred = sum(add_v.get(j, 0) for j in add) - sum(rem_v.get(i, 0) for i in remove) - SELL_MARGIN * n_sold
                props.add((pred, key))

        for j in adds:
            propose([], [j])
            for i in cur:
                propose([i], [j])
        cheap = sorted(cur, key=lambda i: rem_v[i] / g.items[i].cost)[:5]
        for a in range(len(cheap)):
            for c in range(a + 1, len(cheap)):
                for j in adds[:10]:
                    propose([cheap[a], cheap[c]], [j])
        for i in cheap[:3]:
            for a in range(min(8, len(adds))):
                for c in range(a + 1, min(8, len(adds))):
                    propose([i], [adds[a], adds[c]])
        props = sorted(props, key=lambda p: -p[0])[:PROPOSALS_S]
        if not props:
            break
        scored = sorted(((ev.run(p, "S"), p) for _, p in props), key=lambda x: -x[0])
        best_f, best_p = cur_f, None
        for _, p in scored[:PROPOSALS_F]:
            f = full(p)
            if f > best_f:
                best_f, best_p = f, p
        if best_p is None or best_f - cur_f < 0.002:
            if best_p is not None:
                cur, cur_f = list(best_p), best_f
            break
        cur, cur_f = list(best_p), best_f
    return sorted(archive.values(), key=lambda x: -x[0])


def toward(ctx, b, target):
    """A build at budget b made of the late game target's items and their components, filled greedily by
    screening-pool value per soul (no selling later needed for these pieces)."""
    ev, limit = ctx.evaluator(b), item_budget(b)
    pieces = set(target)
    for i in target:
        pieces |= comps(i) & set(S.G().items)
    cur = []
    while True:
        base = ev.run(cur, "S")
        best = None
        for p in pieces:
            if p in cur or any(p in comps(i) for i in cur):
                continue
            new = with_item(cur, p)
            if not S.valid(new, limit):
                continue
            v = (ev.run(new, "S") - base) / max(1, S.cost(new) - S.cost(cur))
            if v > 0 and (best is None or v > best[0]):
                best = (v, new)
        if best is None:
            return cur
        cur = best[1]


def overall_job(bracket, hero, b):
    fn = os.path.join(O.jobs_dir(bracket), f"{hero}_{b}.json")
    if os.path.exists(fn):
        with open(fn) as f:
            return json.load(f)
    return None


def grow(ctx, start):
    """Grow a 10k build through the later stages. Returns the stage list."""
    stages = [start]
    for b in BUDGETS[1:]:
        prev = stages[-1]
        best = stage_search(ctx, b, prev["items"], prev["waste"], prev["items"])[0]
        stages.append({"budget": b, "items": best[2], "score": best[1], "sold": best[3], "waste": best[4]})
    return stages


def invest(items):
    g = S.G()
    out = {s: 0 for s in SLOTS}
    for i in items:
        out[g.items[i].slot] = out.get(g.items[i].slot, 0) + g.items[i].cost
    return out


def crossed(hero, before, after):
    """Investment thresholds crossed between two slot spends: [{slot, at, bonus}]."""
    out = []
    for s in SLOTS:
        for th, v in hero.invest.get(s, []):
            if before[s] < th <= after[s]:
                out.append({"slot": s, "at": th, "bonus": v})
    return out


def buy_order(ctx, stages):
    """Purchase order from nothing through every stage (see the module doc)."""
    g = S.G()
    hero = g.hero(ctx.hero)
    owned, waste, last_nw, steps = [], 0.0, 0, []
    prev_items = []
    for st in stages:
        b = st["budget"]
        ev = ctx.evaluator(b)
        if st["sold"]:
            owned = [i for i in owned if i not in st["sold"]]
            refund = REFUND * S.cost(st["sold"])
            waste += refund
            steps.append({"sell": st["sold"], "refund": round(refund), "net_worth": last_nw, "stage": b,
                          "invest": invest(owned)})
        target = st["items"]
        pieces = set(i for i in target if i not in prev_items)
        for i in list(pieces):
            pieces |= comps(i) & set(g.items)
        pieces -= set(prev_items)

        def options(cur):
            out = []
            for p in pieces:
                if p in cur or any(p in comps(o) for o in cur):
                    continue
                # only components of something still to buy
                if p not in target and not any(p in comps(t) for t in target if t not in cur):
                    continue
                new = with_item(cur, p)
                if len(new) > S.MAX_ITEMS:
                    continue
                out.append((p, new, S.cost(new) - S.cost(cur)))
            return out

        while set(target) - set(owned):
            base = ev.run(owned, "S")
            spend0 = invest(owned)
            best = None
            for p, new, paid in options(owned):
                v = (ev.run(new, "S") - base) / max(1, paid)
                # spike pairs: p then q crosses a threshold that p alone doesn't
                if not crossed(hero, spend0, invest(new)):
                    for q, new2, paid2 in options(new):
                        if crossed(hero, invest(new), invest(new2)) and \
                                len(crossed(hero, spend0, invest(new2))) > len(crossed(hero, spend0, invest(new))):
                            v = max(v, (ev.run(new2, "S") - base) / max(1, paid + paid2))
                key = (v, -paid)
                if best is None or key > best[0]:
                    best = (key, p, new, paid)
            if best is None:
                raise RuntimeError(f"no buyable piece toward {sorted(set(target) - set(owned))}")
            _, p, new, paid = best
            nw = max(net_worth_for(S.cost(new) + waste), cap_net_worth(new), last_nw)
            spikes = crossed(hero, invest(owned), invest(new))
            steps.append({"item": p, "replaces": [i for i in owned if i not in new], "paid": paid,
                          "net_worth": nw, "stage": b, "invest": invest(new), "spikes": spikes})
            owned, last_nw = new, nw
        prev_items = list(target)
    return steps


def describe(ctx, b, items, waste):
    ev = ctx.evaluator(b)
    d = ev.run(items, "F", detail=True)
    d.pop("matchups")
    hero = S.G().hero(ctx.hero)
    spend = invest(items)
    inv = {}
    for s in SLOTS:
        tiers = hero.invest.get(s, [])
        nxt = next(((th, v) for th, v in tiers if th > spend[s]), None)
        inv[s] = {"spent": spend[s], "bonus": next((v for th, v in reversed(tiers) if spend[s] >= th), 0),
                  "next_at": nxt[0] if nxt else None, "next_bonus": nxt[1] if nxt else None}
    return {"budget": b, "item_budget": item_budget(b), "items": sorted(items), "cost": S.cost(items),
            "lost_to_sales": round(waste), "overall": d, "invest": inv}


def path_job(args):
    hero, bracket = args
    O.set_bracket(bracket)
    O._phases()
    fn = os.path.join(jobs_dir(bracket), f"{hero}.json")
    if os.path.exists(fn):
        return fn, "skip"
    t0 = time.time()
    g = S.G()
    ctx = Ctx(hero, bracket)
    b0 = BUDGETS[0]

    # late game target: the overall search's best 50k build, else a quick search here
    late = overall_job(bracket, hero, BUDGETS[-1])
    target = late["builds"][0]["items"] if late else \
        stage_search(ctx, BUDGETS[-1], [], 0.0, ctx.popular(BUDGETS[-1]))[0][2]

    # starts at 10k
    first = stage_search(ctx, b0, [], 0.0, ctx.popular(b0))
    starts = {"best_10k": first[0]}
    runner = next((x for x in first[1:] if x[2] != first[0][2]), None)
    if runner:
        starts["runner_up_10k"] = runner
    tw = toward(ctx, b0, target)
    tw_best = stage_search(ctx, b0, tw, 0.0, tw)
    # keep the late-game pieces: the best 10k build that still holds every piece of the seed
    keep = [x for x in tw_best if not sold_items(tw, x[2])]
    starts["toward_late_game"] = (keep or tw_best)[0]

    lineages = []
    seen = set()
    for name, x in starts.items():
        key = tuple(x[2])
        if key in seen:
            continue
        seen.add(key)
        st = grow(ctx, {"budget": b0, "items": x[2], "score": x[1], "sold": [], "waste": 0.0})
        sc = [s["score"] for s in st]
        lineages.append({"start": name, "stages": st, "stage_scores": [round(v, 4) for v in sc],
                         "path_score": round(path_score(sc), 4)})
    lineages.sort(key=lambda x: -x["path_score"])
    best = lineages[0]

    stages_out = []
    for st in best["stages"]:
        b = st["budget"]
        d = describe(ctx, b, st["items"], st["waste"])
        pop = ctx.popular(b)
        d["popular"] = {"items": sorted(pop)} | {k: v for k, v in ctx.ev[b].run(pop, "F", detail=True).items()
                                                  if k != "matchups"}
        job = overall_job(bracket, hero, b)
        if job:   # the best build for this net worth alone, rescored on the current sim
            bi = job["builds"][0]["items"]
            d["best_alone"] = {"items": bi} | {k: v for k, v in ctx.ev[b].run(bi, "F", detail=True).items()
                                                if k != "matchups"}
        d["sold"] = st["sold"]
        stages_out.append(d)
    order = buy_order(ctx, best["stages"])

    out = {"hero_id": hero, "hero": g.hero(hero).name, "bracket": bracket, "budgets": BUDGETS,
           "path_score": best["path_score"], "stage_scores": best["stage_scores"], "start": best["start"],
           "late_target": sorted(target), "stages": stages_out, "order": order,
           "lineages": [{k: v for k, v in x.items() if k != "stages"} | {"items": [s["items"] for s in x["stages"]]}
                        for x in lineages],
           "refund": REFUND, "sell_margin": SELL_MARGIN,
           "fights": ctx.fights, "seconds": round(time.time() - t0, 1)}
    os.makedirs(jobs_dir(bracket), exist_ok=True)
    with open(fn + ".tmp", "w") as f:
        json.dump(out, f)
    os.replace(fn + ".tmp", fn)
    sc = " ".join(f"{b // 1000}k {s:.2f}" for b, s in zip(BUDGETS, out["stage_scores"]))
    return fn, f"{out['hero']}: path {out['path_score']:.3f} ({best['start']}) stages vs popular {sc} " \
               f"({out['fights']} fights, {out['seconds']}s)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--heroes", default="")
    ap.add_argument("--bracket", default=PRIMARY, choices=list(BRACKETS))
    ap.add_argument("--budgets", default="", help="a path needs every budget; a run limited to some skips it")
    a = ap.parse_args()
    if a.budgets and {int(b) for b in a.budgets.split(",")} != set(BUDGETS):
        print("game path skipped: it needs every budget")
        return
    g = S.G()
    heroes = [g.hero(int(h) if h.isdigit() else h).id for h in a.heroes.split(",") if h] or sorted(g.heroes)
    os.makedirs(jobs_dir(a.bracket), exist_ok=True)
    with Pool(a.workers) as p:
        for fn, msg in p.imap_unordered(path_job, [(h, a.bracket) for h in heroes]):
            print(time.strftime("%H:%M:%S"), msg, flush=True)


if __name__ == "__main__":
    main()
