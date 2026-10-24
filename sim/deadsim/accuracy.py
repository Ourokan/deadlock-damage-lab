"""Player aim inputs for the fight model.

Real numbers come from the Deadlock API match metadata. Each match stores, per player, custom stats
"Enemy Hero Accuracy##Shots / Hits / Headshots" (bullets fired while aiming at heroes, hero hits, hero
headshots) and "Outgoing Bullet Dist##<m>" (bullet hits by distance bucket). Those are hero-only numbers;
the plain shots_hit / shots_missed stats include creeps and run about twice as high.

    from deadsim.accuracy import player_skill, hero_default_skill
    sk, info = player_skill(34500250, hero="Bebop")      # Skill(...), details
    sk = hero_default_skill("Haze", "p50")               # population default for a hero

Manual input is just Skill(accuracy=..., headshot=...).
"""
from __future__ import annotations

import json
import os
import time
import urllib.request

from .data import game
from .engine import Skill

API = "https://api.deadlock-api.com"
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}
HERE = os.path.dirname(__file__)
CACHE = os.path.join(HERE, "..", "cache")
DEFAULTS = os.path.join(HERE, "..", "data", "skill_defaults.json")

SHOTS, HITS, HEADS = "Enemy Hero Accuracy##Shots", "Enemy Hero Accuracy##Hits", "Enemy Hero Accuracy##Headshots"
DIST_PREFIX = "Outgoing Bullet Dist##"
DIST_EDGES = {"10": 10, "20": 20, "30": 30, "40": 40, "50": 50, "75": 75, "100": 100, "Infinite": 150}


def _get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return json.load(r)
        except Exception:  # noqa: BLE001
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def _cached(name, url):
    os.makedirs(CACHE, exist_ok=True)
    fn = os.path.join(CACHE, name)
    if os.path.exists(fn):
        return json.load(open(fn))
    d = _get(url)
    json.dump(d, open(fn, "w"))
    return d


def match_custom_stats(match_id):
    """{account_id: {stat name: value}} at the end of the match (cached on disk)."""
    m = _cached(f"meta_{match_id}.json", f"{API}/v1/matches/{match_id}/metadata")
    mi = m.get("match_info", m)
    names = {c["id"]: c["name"] for c in mi.get("custom_user_stats") or []}
    out = {}
    for p in mi["players"]:
        last = p["stats"][-1] if p.get("stats") else {}
        out[p["account_id"]] = {names.get(c["id"], str(c["id"])): c["value"] for c in last.get("custom_user_stats") or []}
        out[p["account_id"]]["_hero_id"] = p["hero_id"]
    return out


def distance_profile(custom):
    """Share of bullet hits per distance bucket -> (median meters, {bucket upper edge: share})."""
    buckets = {DIST_EDGES[k[len(DIST_PREFIX):]]: v for k, v in custom.items()
               if k.startswith(DIST_PREFIX) and k[len(DIST_PREFIX):] in DIST_EDGES}
    tot = sum(buckets.values())
    if not tot:
        return None, {}
    share = {k: v / tot for k, v in sorted(buckets.items())}
    acc, prev = 0.0, 0
    for edge, s in share.items():
        if acc + s >= 0.5:
            return prev + (edge - prev) * (0.5 - acc) / s, share
        acc += s
        prev = edge
    return prev, share


def player_skill(account_id, hero=None, n_matches=20, rank_spirit_accuracy=None):
    """Aim from a player's recent matches (optionally on one hero). Returns (Skill, info dict)."""
    hist = _get(f"{API}/v1/players/{account_id}/match-history")
    hid = game().hero(hero).id if hero is not None else None
    ms = [m for m in hist if hid is None or m["hero_id"] == hid][:n_matches]
    shots = hits = heads = 0
    dist = {}
    used = 0
    for m in ms:
        try:
            cs = match_custom_stats(m["match_id"]).get(account_id)
        except Exception:  # noqa: BLE001 - match not ingested yet
            continue
        if not cs or not cs.get(SHOTS):
            continue
        used += 1
        shots += cs.get(SHOTS, 0)
        hits += cs.get(HITS, 0)
        heads += cs.get(HEADS, 0)
        for k, v in cs.items():
            if k.startswith(DIST_PREFIX):
                dist[k] = dist.get(k, 0) + v
    if not shots:
        raise ValueError(f"no hero-accuracy data for account {account_id}" + (f" on {hero}" if hero else ""))
    acc, hs = hits / shots, heads / max(1, hits)
    med, share = distance_profile(dist)
    sk = Skill(accuracy=acc, headshot=hs, melee_rate=melee_rate(hero) if hero is not None else 0.0)
    if rank_spirit_accuracy is not None:
        sk.spirit_accuracy = rank_spirit_accuracy
    return sk, {"matches": used, "shots": shots, "hits": hits, "headshots": heads, "median_distance_m": med,
                "distance_share": share}


LANDING = os.path.join(HERE, "..", "data", "landing_rates.json")
LANDING_MECH = os.path.join(HERE, "..", "data", "landing_rates_mech.json")
MELEE = os.path.join(HERE, "..", "data", "melee_rates.json")
MELEE_ITEMS_FILE = os.path.join(HERE, "..", "data", "melee_items.json")


def melee_rate(hero):
    """Landed basic melee hits per second for this hero, fitted from real damage (data/melee_rates.json)."""
    try:
        d = json.load(open(MELEE))["heroes"]
    except (OSError, KeyError, ValueError):
        return 0.0
    row = d.get(str(game().hero(hero).id))
    return row["rate"] if row else 0.0


def melee_rates_by_items(hero):
    """(rate with 0, 1, 2+ melee items) for this hero: the average rate (melee_rates.json) times the fitted multiplier
    for the build (data/melee_items.json, scripts/melee_items_fit.py; its 90% lower bound, since holders partly melee
    more because melee players buy these items), scaled so the hero's real mix of builds still
    averages to the average rate. None when the data is missing."""
    avg = melee_rate(hero)
    try:
        d = json.load(open(MELEE_ITEMS_FILE))
    except (OSError, ValueError):
        return None
    hid = str(game().hero(hero).id)
    row = d["heroes"].get(hid, {})
    cls = row.get("class") or ("melee" if avg >= d["meta"]["melee_hero_rate"] else "gun")
    mult = [d["classes"][cls][g].get("used", d["classes"][cls][g]["mult"]) for g in ("0", "1", "2+")]
    mix = row.get("mix") or {"0": 1.0}
    norm = sum(mix.get(g, 0.0) * m for g, m in zip(("0", "1", "2+"), mult)) or 1.0
    return tuple(round(avg * m / norm, 4) for m in mult)


def ability_landing(hero, mech=False):
    """{ability name: effective landing factor} fitted from real damage shares (data/landing_rates.json; with
    mech=True the refit with deadsim.mechanics on, data/landing_rates_mech.json)."""
    try:
        d = json.load(open(LANDING_MECH if mech else LANDING))["heroes"]
    except (OSError, KeyError, ValueError):
        return {}
    rows = d.get(game().hero(hero).name, {})
    return {name: min(1.5, max(0.05, r["landing"])) for name, r in rows.items()}


def dot_cleanse_delay(badge=None):
    """Seconds a DoT (Decay etc.) runs before a Dispel Magic holder cleanses it, by match badge (tier*10+subrank).
    Eternus (111+): 1.5 s, a tick or two (Tyler, an Eternus player). Ascendant/Phantom (91-110): 3 s. Lower ranks and
    badge=None: None = only below 50% health. Real data (damage/work/decay_vs_dispel_*.json) shows a smaller effect:
    Dispel holders still take 99% (all ranks), 91% (81+) and 85% (111+) of their teammates' Decay damage, likely
    because Dispel is often on cooldown or used on something else first."""
    if badge is None or badge < 91:
        return None
    return 1.5 if badge >= 111 else 3.0


ITEM_LANDING = os.path.join(HERE, "..", "data", "item_landing.json")
ITEM_LANDING_MIN_HOLDERS = 40


def item_landing():
    """{item name: real-data damage factor} for items whose own damage the 1v1 sim over-predicts (factor < 1,
    clipped at 0.25; data/item_landing.json, scripts/item_landing.py). Items real players get MORE from are left
    at 1: that excess is mostly hitting several heroes in team fights, which a 1v1 should not count."""
    try:
        rows = json.load(open(ITEM_LANDING))["items"]
    except (OSError, ValueError, KeyError):
        return {}
    return {r["name"]: max(0.25, r["landing"]) for r in rows.values()
            if r["landing"] < 1.0 and r["holders"] >= ITEM_LANDING_MIN_HOLDERS}


def zone_exit_time(badge=None):
    """Seconds a player stays in an avoidable ground zone (Alchemical Fire, 10 m radius, 5 s) before walking out:
    reaction time plus the walk to the edge. Assumption, like dot_cleanse_delay: 2.0 s for ranked overall,
    1.5 s from Ascendant up. Not measurable from the API (no zone positions)."""
    return 1.5 if badge is not None and badge >= 101 else 2.0


def hero_default_skill(hero, pct="p50", landing=True, melee=True, melee_rate_override=None, heavy_share=None,
                       badge=None, counterplay=False, melee_build=True):
    """Population aim for a hero (current-patch ranked sample, hero-only accuracy). pct: p25 | p50 | p75 | p90.
    landing=True also applies each ability's real-data landing factor (clipped to 0.05-1.5); melee=True sets the
    hero's real melee rate; with melee_build=True that rate follows the build (players with melee items melee more,
    melee_rates_by_items). melee_rate_override (landed melees per second) and heavy_share (0-1) replace the
    data defaults with the user's own numbers. badge (match rank, e.g. 111 = Eternus 1) sets rank-dependent
    habits: how fast Dispel Magic is used on a DoT (dot_cleanse_delay). Targets always walk out of ground
    zones (zone_exit_s). counterplay=True also applies real-data item damage factors (item_landing)."""
    d = json.load(open(DEFAULTS))
    h = game().hero(hero)
    row = d["heroes"].get(str(h.id)) or d["all"]
    sk = Skill(accuracy=row["accuracy"][pct], headshot=row["headshot"][pct])
    if landing:
        sk.ability_landing = ability_landing(hero)
        sk.ability_landing_mech = ability_landing(hero, mech=True)
    if melee:
        sk.melee_rate = melee_rate(hero)
        if melee_build:
            sk.melee_by_items = melee_rates_by_items(hero)
    if melee_rate_override is not None:
        sk.melee_rate = max(0.0, float(melee_rate_override))
        sk.melee_by_items = None
    if heavy_share is not None:
        sk.heavy_share = min(1.0, max(0.0, float(heavy_share)))
    sk.dot_cleanse_delay = dot_cleanse_delay(badge)
    # players walk out of ground zones (Alchemical Fire) unless stunned, rooted or slowed (items_fx.held_share);
    # on in every mode since 2026-10-21 (Tyler: no Alchemical Fire for heroes that can't hold a target in it)
    sk.zone_exit_s = zone_exit_time(badge)
    if counterplay:   # realistic mode: item damage calibrated to real matches
        sk.item_landing = item_landing()
    return sk


def default_distance(hero):
    d = json.load(open(DEFAULTS))
    h = game().hero(hero)
    row = d["heroes"].get(str(h.id)) or d["all"]
    return row.get("median_distance_m", 15.0)
