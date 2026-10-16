"""Pull full match metadata for a sample of current-patch ranked matches and keep only what the
combat model is validated against: per-player item timeline, stat timeline (max_health, tech_power,
shots, headshots, damage) and per-source damage dealt to enemy heroes from the damage matrix.

usage: python3 fetch_validation.py <player_builds.jsonl.gz> <out.jsonl.gz> [n_matches]
"""
import gzip, json, random, sys, time, urllib.request, concurrent.futures as cf

SRC, OUT = sys.argv[1], sys.argv[2]
N = int(sys.argv[3]) if len(sys.argv) > 3 else 300
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}

ids = set()
with gzip.open(SRC, "rt") as f:
    for line in f:
        r = json.loads(line)
        if (r["badge"] or 0) >= 60 and r["duration_s"] > 1500:
            ids.add(r["match_id"])
random.seed(7)
ids = random.sample(sorted(ids), min(N, len(ids)))

STAT_KEYS = ("time_stamp_s", "net_worth", "max_health", "tech_power", "weapon_power", "shots_hit",
             "shots_missed", "hero_bullets_hit", "hero_bullets_hit_crit", "player_damage",
             "player_damage_taken", "ability_points", "kills", "deaths")


def get(mid):
    url = f"https://api.deadlock-api.com/v1/matches/{mid}/metadata"
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return json.load(r)["match_info"]
        except Exception as e:  # noqa: BLE001 - retry anything transient
            time.sleep(3 * (i + 1))
    return None


def slim(m):
    dm = m.get("damage_matrix") or {}
    names = (dm.get("source_details") or {}).get("source_name", [])
    stypes = (dm.get("source_details") or {}).get("stat_type", [])
    # Damage matrix: stat_type 0 = damage dealt (1 mitigated?, 3 taken?, 5 healing); target slot 0 = non-heroes.
    # Source names "Bullet", "Ability", "Melee", "Misc" are per-damage-type totals of the named sources.
    team = {p["player_slot"]: p["team"] for p in m["players"]}
    dmg = {}  # player_slot -> {source_name: damage dealt to enemy heroes}
    for d in dm.get("damage_dealers", []):
        me = d["dealer_player_slot"]
        acc = dmg.setdefault(me, {})
        for s in d["damage_sources"]:
            i = s["source_details_index"]
            if i >= len(names) or (stypes[i] if i < len(stypes) else None) != 0:
                continue
            tot = sum(t["damage"][-1] for t in s["damage_to_players"]
                      if t["damage"] and t["target_player_slot"] in team and team[t["target_player_slot"]] != team.get(me))
            if tot:
                acc[names[i]] = acc.get(names[i], 0) + tot
    cus = {c["id"]: c["name"] for c in m.get("custom_user_stats") or []}
    players = []
    for p in m["players"]:
        last = p["stats"][-1] if p["stats"] else {}
        custom = {cus.get(c["id"], str(c["id"])): c["value"] for c in last.get("custom_user_stats") or []}
        players.append({
            "account_id": p["account_id"], "slot": p["player_slot"], "team": p["team"],
            "hero_id": p["hero_id"], "level": p["level"], "net_worth": p["net_worth"],
            "items": [[x["item_id"], x["game_time_s"], x["sold_time_s"], x.get("upgrade_id", 0)] for x in p["items"]],
            "stats": [{k: s.get(k) for k in STAT_KEYS} for s in p["stats"]],
            "damage_sources": dmg.get(p["player_slot"], {}),
            "custom": custom,
            "deaths": [{"t": d.get("game_time_s"), "killer": d.get("killer_player_slot"), "ttk": d.get("time_to_kill_s")}
                       for d in p.get("death_details") or []],
            "power_ups": [{"type": b.get("type"), "values": b.get("pickup_stat_values"), "times": b.get("pickup_times_s")}
                          for b in p.get("power_up_buffs") or []],
        })
    return {"match_id": m["match_id"], "duration_s": m["duration_s"],
            "badge": [m.get("average_badge_team0"), m.get("average_badge_team1")], "players": players}


n = 0
with gzip.open(OUT, "wt") as out, cf.ThreadPoolExecutor(4) as ex:
    for m in ex.map(get, ids):
        if m:
            out.write(json.dumps(slim(m), separators=(",", ":")) + "\n"); n += 1
print("wrote", n, "matches")
