"""Run one rank tier's searches for one slice of the jobs:
python3 pipeline/run_shard.py --tier phantom --shard I --of N [--workers 4]

Every tier runs the duel search, the overall search (damage before dying, counterplay on) and the full game build
path in its rank bracket. The standard tier (build_pool.PRIMARY, Phantom and up) also runs the dummy damage search,
the item buy order, the ability upgrade order, the counter-item values (counters/scripts/sim_counters.py) and, for the
tank heroes, the survival search. Tiers and their order: pipeline/tiers.json. Inputs: search/work/snapshots_*.json and
item_usage*.json from search/scripts/build_pool.py. Results land in each search's work/jobs*/ folder as usual.

The work is split by job (hero x budget), not by hero, so N machines finish together: every shard builds the same
plan from pipeline/unit_costs.json (each job's time in the last rerun) and takes its share, longest first. Jobs that
need others stay on one machine: a hero's damage searches with its buy and ability orders (they read them), and its
overall searches with its game path (it reads them). On a machine, --workers jobs run side by side, each its own
search process (--workers 1), next job picked by the longest chain of work it holds up, so no core sits idle while
work is left. A job runs exactly as the search scripts run it for that hero and budget, so the results don't depend on
the split. A failed job is retried once; the heroes still failing are listed in pipeline/work/shard_<tier>_<I>.json
and the publish step decides. That file also records each job's time for the next plan (pipeline/unit_costs.py).
"""
import argparse
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "search", "scripts"))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from build_pool import BRACKETS, BUDGETS, PRIMARY  # noqa: E402
import unit_costs  # noqa: E402

COUNTER_BUDGETS = [18000, 27000, 37000, 50000]   # counters/scripts/sim_counters.py BUDGETS


class Unit:
    def __init__(self, step, name, hero, budget, cmd, cost):
        self.step, self.name, self.hero, self.budget, self.cmd, self.cost = step, name, hero, budget, cmd, cost
        self.deps, self.after = [], []   # units this one waits for / units waiting for it
        self.chain = None                # cost of this job and the longest chain of jobs waiting on it

    @property
    def key(self):
        return f"{self.hero}_{self.budget}" if self.budget else str(self.hero)


def tanks():
    """The tank heroes the survival search runs (survival_search.tank_heroes on the standard bracket's usage)."""
    sys.path.insert(0, os.path.join(ROOT, "survival", "scripts"))
    import survival_search as SV  # noqa: E402
    with open(os.path.join(ROOT, "search", "work", f"item_usage_{PRIMARY}.json")) as f:
        order, _ = SV.tank_heroes(json.load(f))
    return set(order[:SV.N_TANKS])


def plan(tier, heroes, budgets, cost, tank_ids):
    """Groups of units (each group runs on one machine), in the order the steps used to run."""
    py, one = sys.executable, ["--workers", "1"]
    limited = ["--budgets", ",".join(map(str, budgets))] if budgets != BUDGETS else []
    groups = []

    def unit(step, name, script, hero, budget=None, extra=()):
        b = ["--budgets", str(budget)] if budget else limited
        cmd = [py, script, *extra, "--heroes", str(hero), *b, *one]
        return Unit(step, name, hero, budget, cmd, cost(step, hero, budget))

    for h in heroes:
        if tier == PRIMARY:
            dmg = [unit("damage", "damage", "damage/scripts/dummy_search.py", h, b) for b in budgets]
            order = unit("buy_order", "buy_order", "damage/scripts/buy_order.py", h)        # needs the 50k damage job
            skill = unit("skill_order", "skill_order", "damage/scripts/skill_order.py", h)  # needs every budget's
            for u in (order, skill):
                u.deps = list(dmg)
            groups.append(dmg + [order, skill])
        groups += [[unit("duel", f"duel_{tier}", "search/scripts/search.py", h, b, ["--bracket", tier])]
                   for b in budgets]
        if tier == PRIMARY and h in tank_ids:
            groups += [[unit("survival", "survival", "survival/scripts/survival_search.py", h, b, ["--only-tanks"])]
                       for b in budgets]
        ov = [unit("overall", f"overall_{tier}", "damage/scripts/overall_search.py", h, b, ["--bracket", tier])
              for b in budgets]
        path = unit("path", f"path_{tier}", "damage/scripts/game_path.py", h, None, ["--bracket", tier])
        path.deps = list(ov)   # reads the overall jobs
        groups.append(ov + [path])
        if tier == PRIMARY:
            groups += [[unit("counters", "counters", "counters/scripts/sim_counters.py", h, b)]
                       for b in budgets if b in COUNTER_BUDGETS]
    for g in groups:
        for u in g:
            for d in u.deps:
                d.after.append(u)
    for g in groups:
        for u in g:
            chain(u)
    return groups


def chain(u):
    if u.chain is None:
        u.chain = u.cost + max((chain(a) for a in u.after), default=0)
    return u.chain


def split(groups, n, workers):
    """Longest group first onto the machine that would finish it soonest (load / workers, or the group's own chain)."""
    load = [0.0] * n
    span = [0.0] * n
    shards = [[] for _ in range(n)]
    for g in sorted(groups, key=lambda g: (-sum(u.cost for u in g), g[0].step, g[0].key)):
        c = sum(u.cost for u in g)
        crit = max(u.chain for u in g)
        i = min(range(n), key=lambda i: (max((load[i] + c) / workers, span[i], crit), i))
        load[i] += c
        span[i] = max(span[i], crit)
        shards[i] += g
    return shards, [max(load[i] / workers, span[i]) for i in range(n)]


def setup(tier, budgets_arg, n, workers, heroes_arg=""):
    with open(os.path.join(ROOT, "data", "game", "heroes.json")) as f:
        heroes = sorted(h["id"] for h in json.load(f))
    heroes = [h for h in heroes if str(h) in heroes_arg.split(",")] if heroes_arg else heroes
    budgets = [int(b) for b in budgets_arg.split(",") if b] or BUDGETS
    tank_ids = tanks() if tier == PRIMARY else set()
    groups = plan(tier, heroes, budgets, unit_costs.Costs(tier), tank_ids)
    return split(groups, n, workers)


def show(tier, n, workers=4):
    shards, est = setup(tier, "", n, workers)
    for i, (units, t) in enumerate(zip(shards, est)):
        print(f"shard {i:2}: {len(units):3} jobs, about {t / 60:5.1f} min")
    print(f"slowest about {max(est) / 60:.1f} min")


def run(units, workers):
    """Run the units, `workers` at a time, longest chain first once its inputs are done. Returns (seconds, failed)."""
    waiting = sorted(units, key=lambda u: (-u.chain, u.step, u.key))
    done, running, seconds, failed = set(), {}, {}, []
    tries = {}
    while waiting or running:
        for u in [u for u in waiting if all(d in done for d in u.deps)]:
            if len(running) >= workers:
                break
            waiting.remove(u)
            tries[u] = tries.get(u, 0) + 1
            running[u] = (subprocess.Popen(u.cmd, cwd=ROOT), time.time())
        time.sleep(0.2)
        for u, (p, t0) in list(running.items()):
            if p.poll() is None:
                continue
            del running[u]
            seconds[u] = seconds.get(u, 0) + time.time() - t0
            if p.returncode != 0 and tries[u] < 2:
                print(f"{u.name} {u.key} failed, retrying", flush=True)
                waiting.insert(0, u)   # finished jobs are skipped, so only the rest reruns
                continue
            if p.returncode != 0:
                failed.append(u)
            done.add(u)   # a failed job doesn't hold back the rest, as before
    return seconds, failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", default=PRIMARY, choices=list(BRACKETS))
    ap.add_argument("--shard", type=int, required=True)
    ap.add_argument("--of", type=int, required=True)
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 4)
    ap.add_argument("--budgets", default="", help="e.g. 10000 for a quick test; default every budget")
    ap.add_argument("--heroes", default="", help="hero ids, e.g. 1,19 for a quick test; default every hero")
    a = ap.parse_args()
    shards, est = setup(a.tier, a.budgets, a.of, a.workers, a.heroes)
    mine = shards[a.shard]
    print(f"shard {a.shard} of {a.of}: {len(mine)} jobs, planned about {est[a.shard] / 60:.0f} min "
          f"(slowest shard {max(est) / 60:.0f} min)", flush=True)
    t0 = time.time()
    seconds, failed = run(mine, a.workers)
    report = {"tier": a.tier, "shard": a.shard, "heroes": sorted({u.hero for u in mine}), "steps": {}, "failed": {},
              "units": {}, "planned_s": round(est[a.shard]), "wall_s": round(time.time() - t0)}
    for u in mine:
        report["steps"][u.name] = report["steps"].get(u.name, 0) + round(seconds.get(u, 0))
        if not a.budgets and not a.heroes:   # a quick test's times aren't a full rerun's
            report["units"].setdefault(u.step, {})[u.key] = round(seconds.get(u, 0), 1)
    for u in failed:
        if u.hero not in report["failed"].setdefault(u.name, []):
            report["failed"][u.name].append(u.hero)
    os.makedirs(os.path.join(ROOT, "pipeline", "work"), exist_ok=True)
    with open(os.path.join(ROOT, "pipeline", "work", f"shard_{a.tier}_{a.shard}.json"), "w") as f:
        json.dump(report, f, indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != "units"}))


if __name__ == "__main__":
    main()
