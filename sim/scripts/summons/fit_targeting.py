"""Fit how much the enemy shoots each summon kind (data/summon_targeting.json "focus") to Phantom+ replays.

Real (summon_stats.py output): gun_focus_share = enemy gun damage to summons of a kind / (that + enemy gun damage to
the owner), while at least one summon of that kind is alive. Gun only, because in the sim only bullets hit summons
(real enemies also hit them with area abilities). That other damage is fitted as "splash": the share of the owner's
non-gun damage taken that also lands on a summon (real: non-gun damage to summons / non-gun damage to the owner).
The gravestone takes no gun damage in the replays (only abilities and melee), so its focus is 0; besides splash the
enemy breaks it (melee) with probability break_p at break_s s: the real share of those that took hero damage that a
hero destroyed, and the real median time to break one. Sim: the same ratio from duels of every sample player
of the owner hero (validation/matches_sample.jsonl.gz, real builds at 30/60/90% of the match, real gun accuracy,
current landing factors) against a random real enemy build from the same match. Each round scales a kind's share
of trigger pulls by real odds / sim odds; acc_mult stays as written (an assumption: stationary turret and gravestone
2.5x hero accuracy, walking zombies 2x, small flying Deadheads 1x).

usage: python3 scripts/summons/fit_targeting.py <summon_stats.json> [rounds=4] [workers]
Writes data/summon_targeting.json (focus, plus real and sim numbers per kind).
"""
import collections
import gzip
import json
import os
import random
import sys
from concurrent.futures import ProcessPoolExecutor

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from deadsim import Loadout, duel, game  # noqa: E402
from deadsim.abilities import load_heroes  # noqa: E402
from deadsim.accuracy import default_distance  # noqa: E402
import deadsim.mechanics as M  # noqa: E402
import landing_rates as L  # noqa: E402

OWNERS = {"mcginnis_turret": 8, "graves_zombie": 76, "graves_skull": 76, "graves_stone": 76}
PATH = os.path.join(ROOT, "data", "summon_targeting.json")


def sim_player(job):
    m, slot, kinds = job
    M._TARGETING = kinds
    L.ITERATE = True
    G = game()
    load_heroes()
    me = next(p for p in m["players"] if p["slot"] == slot)
    foes = [p for p in m["players"] if p["team"] != me["team"] and p["hero_id"] in G.heroes]
    rnd = random.Random(m["match_id"] * 31 + slot)
    # kind -> [gun to summons, other to summons, gun on owner, other on owner, spawned, killed]
    out = collections.defaultdict(lambda: [0.0] * 6)
    for frac in L.FRACS:
        t = m["duration_s"] * frac
        items, souls = L.build_at(me, t)
        foe = rnd.choice(foes)
        fitems, fsouls = L.build_at(foe, t)
        a = Loadout(me["hero_id"], items, souls=souls, skill=L.skill_of(me))
        b = Loadout(foe["hero_id"], fitems, souls=fsouls, skill=L.skill_of(foe))
        r = duel(a, b, distance=default_distance(G.hero(me["hero_id"]).name), max_time=L.FIGHT_TIME)
        for k, v in r.b_summon_kind.items():
            out[k][0] += v[0]
            out[k][1] += v[1]
        for k, v in r.a_hit_while_summon.items():
            out[k][2] += v[0]
            out[k][3] += v[1]
        for k, (n, dead) in r.a_summons_out.items():
            out[k][4] += n
            out[k][5] += dead
    return dict(out)


def run(jobs, kinds, workers):
    tot = collections.defaultdict(lambda: [0.0] * 6)
    with ProcessPoolExecutor(workers) as ex:
        for d in ex.map(sim_player, [(m, s, kinds) for m, s in jobs], chunksize=2):
            for k, v in d.items():
                for i in range(6):
                    tot[k][i] += v[i]
    return tot


def main():
    real = json.load(open(sys.argv[1]))["kinds"]
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else os.cpu_count()
    cur = json.load(open(PATH))
    kinds = cur["kinds"]
    for k in OWNERS:
        kinds[k]["life_other_s"] = real[k]["life_s_not_hero_killed"]
    kinds["graves_stone"]["focus"] = 0.0
    # bullets can't hurt it: enemies break it (melee) as often and as late as real ones that took hero damage
    kinds["graves_stone"]["break_s"] = real["graves_stone"]["life_s_hero_killed"]
    kinds["graves_stone"]["break_p"] = real["graves_stone"]["hero_killed_engaged"]
    G = game()
    jobs = []
    for line in gzip.open(os.path.join(ROOT, "validation", "matches_sample.jsonl.gz")):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] in set(OWNERS.values()):   # all of them: Graves' gun records no hits in the data
                jobs.append((m, p["slot"]))
    print(len(jobs), "sample players", flush=True)
    for rnd in range(rounds + 1):
        tot = run(jobs, kinds, workers)
        for k in OWNERS:
            gun_s, oth_s, gun_o, oth_o, n, dead = tot[k]
            share = gun_s / (gun_s + gun_o) if gun_s + gun_o else 0.0
            splash = oth_s / oth_o if oth_o else 0.0
            want, want_sp = real[k]["gun_focus_share"], real[k]["splash_ratio"]
            kinds[k]["sim"] = {"gun_focus_share": round(share, 3), "splash_ratio": round(splash, 3),
                               "killed": round(dead / n, 3) if n else None, "n": int(n)}
            print(f"round {rnd} {k}: focus {kinds[k]['focus']:.3f} splash {kinds[k].get('splash', 0):.3f} | gun share "
                  f"sim {share:.3f} real {want:.3f} | splash ratio sim {splash:.3f} real {want_sp:.3f} | "
                  f"killed by hero sim {kinds[k]['sim']['killed']} real {real[k]['hero_killed_engaged']} (of those hit by "
                  f"a hero; all: {real[k]['hero_killed']})", flush=True)
            if rnd < rounds:
                if 0 < share < 1 and want > 0:
                    odds = (want / (1 - want)) / (share / (1 - share))
                    kinds[k]["focus"] = round(min(0.95, max(0.005, kinds[k]["focus"] * odds ** 0.5)), 3)
                sp = kinds[k].get("splash", 0.0)
                kinds[k]["splash"] = round(want_sp if sp <= 0 or splash <= 0 else sp * want_sp / splash, 3)
    for k in OWNERS:
        r = real[k]
        kinds[k]["real"] = {x: r[x] for x in ("gun_focus_share", "splash_ratio", "focus_share", "gun_part", "hero_killed",
                                              "hero_killed_engaged", "life_s_hero_killed", "killed", "hp",
                                              "life_s", "life_s_not_hero_killed", "n", "matches")}
        kinds[k]["life_other_s"] = r["life_s_not_hero_killed"]
    cur["note"] = ("focus = share of the enemy's trigger pulls spent on a living summon of this kind, fitted so the "
                   "sim's share of enemy gun damage on summons (vs the owner) matches Phantom+ replays "
                   "(scripts/summons/fit_targeting.py); splash = share of the owner's non-gun damage taken that also "
                   "hits it (fitted the same way); acc_mult = accuracy on it vs on a hero (assumption); "
                   "life_other_s = real median life of summons no enemy hero killed (caps the sim life)")
    json.dump(cur, open(PATH, "w"), indent=1)
    open(PATH, "a").write("\n")


if __name__ == "__main__":
    main()
