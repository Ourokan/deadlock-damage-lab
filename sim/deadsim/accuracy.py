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

import functools
import json
import os
import time
import urllib.request

from .data import game, gun_calibration
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
    hid = game().hero(hero).id if hero is not None else None
    if hid is not None and gun_calibrated(hid):   # no per-player gun stats exist: the replay-fitted population aim
        row = gun_calibration()[str(hid)]
        sk = Skill(accuracy=row["accuracy"]["p50"], headshot=row["headshot"]["p50"], melee_rate=melee_rate(hero))
        if rank_spirit_accuracy is not None:
            sk.spirit_accuracy = rank_spirit_accuracy
        return sk, {"matches": 0, "shots": 0, "hits": 0, "headshots": 0, "median_distance_m": default_distance(hero),
                    "distance_share": {}, "note": "this hero's gun records no hero accuracy; replay-fitted median"}
    hist = _get(f"{API}/v1/players/{account_id}/match-history")
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


_melee_items_cache = {}


def _melee_items():
    if MELEE_ITEMS_FILE not in _melee_items_cache:
        try:
            with open(MELEE_ITEMS_FILE) as fh:
                _melee_items_cache[MELEE_ITEMS_FILE] = json.load(fh)
        except (OSError, ValueError):
            _melee_items_cache[MELEE_ITEMS_FILE] = None
    return _melee_items_cache[MELEE_ITEMS_FILE]


def melee_item_mults(hero):
    """(multiplier on the hero's average melee rate with 0, 1, 2+ melee items): the fitted multiplier for the build
    (data/melee_items.json, scripts/melee_items_fit.py; its 90% lower bound, since holders partly melee more because
    melee players buy these items), scaled so the hero's real mix of builds still averages to 1. None when the data
    is missing or the hero was not in the fit (it keeps the flat rate)."""
    d = _melee_items()
    row = (d or {}).get("heroes", {}).get(str(game().hero(hero).id))
    if not row or not row.get("mix"):
        return None
    cls = d["classes"][row["class"]]
    mult = [cls[g].get("used", cls[g]["mult"]) for g in ("0", "1", "2+")]
    norm = sum(row["mix"].get(g, 0.0) * m for g, m in zip(("0", "1", "2+"), mult)) or 1.0
    return tuple(round(m / norm, 4) for m in mult)


def melee_rates_by_items(hero):
    """(landed melees per second with 0, 1, 2+ melee items): melee_rate x melee_item_mults. None without data."""
    mult = melee_item_mults(hero)
    return None if mult is None else tuple(round(melee_rate(hero) * m, 4) for m in mult)


LENGTH_CORR = True   # False: no fight-length corrections (scripts/fight_length/length_factors.py fits without them)


def ability_landing(hero, mech=False):
    """{ability name: effective landing factor} fitted from real damage shares (data/landing_rates.json; with
    mech=True the refit with deadsim.mechanics on, data/landing_rates_mech.json)."""
    try:
        d = json.load(open(LANDING_MECH if mech else LANDING))["heroes"]
    except (OSError, KeyError, ValueError):
        return {}
    rows = d.get(game().hero(hero).name, {})
    return {name: min(1.5, max(0.05, r["landing"])) for name, r in rows.items()}


def ability_length_corr(hero):
    """{ability name: length_corr} for fights that book damage over real fight lengths (Mechanics.fight_length): the
    mech factors were fitted with every hit of a 20 s duel in full, and x this give the same real/sim ratio under
    the new booking (data/landing_rates_mech.json, scripts/fight_length/length_factors.py)."""
    if not LENGTH_CORR:
        return {}
    try:
        rows = json.load(open(LANDING_MECH))["heroes"].get(game().hero(hero).name, {})
    except (OSError, KeyError, ValueError):
        return {}
    return {name: r["length_corr"] for name, r in rows.items() if "length_corr" in r}


def dot_cleanse_delay(badge=None):
    """Reaction time: seconds a DoT (Decay etc.) runs before a Dispel Magic holder who means to cleanse it does, by
    match badge (tier*10+subrank). Eternus (111+): 1.5 s, a tick or two (Tyler, an Eternus player). Below: 3 s.
    How often they mean to at all is dot_cleanse_share."""
    return 1.5 if badge is not None and badge >= 111 else 3.0


DISPEL_FIT = os.path.join(HERE, "..", "validation", "dispel")


def dot_cleanse_share(badge=None):
    """Share of enemy DoTs a Dispel Magic holder spends it on, fitted to real Decay damage (sim/scripts/fit_dispel.py,
    validation/dispel/fit_<min badge>.json): Dispel holders still take 85% of their teammates' Decay damage at Phantom+
    (1500 matches), 87% at all ranks, 91% at Eternus+ (175 matches, noisy): Dispel is often on cooldown, saved for a
    stun or not noticed. Phantom+ (91+) uses the Phantom+ fit, lower badges and None the all-ranks fit. Eternus+
    (fit_111.json, 0.13, 90% CI 0.00-0.34) is too thin to differ from Phantom+ (0.26, CI 0.19-0.33), so it uses that."""
    return _dispel_fit(91 if badge is not None and badge >= 91 else 0)


@functools.lru_cache(maxsize=None)
def dot_cleanse_share_buildup(badge=None):
    """Share of build-up DoT episodes (Afterburn, Toxic Bullets: re-applied by the enemy's gun) a Dispel Magic holder
    spends it on, fitted to real Afterburn damage (sim/scripts/fit_dispel_buildup.py, validation/dispel/
    buildup_fit_91.json): at Phantom+ Dispel holders take 0.63 of their teammates' Afterburn (relative to Napalm, same
    Infernus, 2200 matches), Toxic Bullets similar (0.68 of it relative to gun damage), and die 21% less to Infernus,
    while Decay is barely cleansed (dot_cleanse_share). The fit sits at its ceiling, 1.0: even then the sim removes
    only 25% of Afterburn (45 s cooldown in one 30 s fight; real windows hold several short fights). Only the
    Phantom+ fit exists, so every badge uses it."""
    with open(os.path.join(DISPEL_FIT, "buildup_fit_91.json")) as f:
        return float(json.load(f)["fitted_share"])


@functools.lru_cache(maxsize=None)
def _dispel_fit(lo):
    # no fallback: a missing fit would silently turn every DoT cleanse back on
    with open(os.path.join(DISPEL_FIT, f"fit_{lo}.json")) as f:
        return float(json.load(f)["fitted_share"])


COUNTERSPELL_FIT = os.path.join(HERE, "..", "validation", "counterspell", "fit_91.json")


@functools.lru_cache(maxsize=None)
def spell_parry_rates(badge=None):
    """(non-ultimate, ultimate) share of enemy aimed casts a Counterspell holder times a spell parry against, fitted
    by sim/scripts/fit_counterspell.py to real Phantom+ ability damage on holders vs teammates
    (validation/counterspell/fit_91.json): their ability damage moves no more than their gun damage (0.965 / 0.98
    vs 0.96), Lash's Death Slam included (1.00), so both rates are about 0. Only the Phantom+ fit exists, so every
    badge uses it."""
    with open(COUNTERSPELL_FIT) as f:
        d = json.load(f)
    return float(d["fitted_rate"]), float(d["fitted_rate_ult"])


ITEM_LANDING = os.path.join(HERE, "..", "data", "item_landing.json")
# 30 since the 2026-10-24 Phantom+ refit so Focus Lens (36 holders) keeps a cut: its factor is low-confidence (0.32 from
# 43 holders in the biased first fit, 0.59 now), but no cut at all would be further from both. 25 since the fight
# length booking (2026-10-24): Silence Wave (26 holders, 0.69; the audit has real/sim 0.35) was left uncut and, with
# its silence landing in full at a fight's opening, picked by 5 of 8 overall builds while it loses ~1.6 win-rate
# points on every hero. No other item has 25-29 holders.
ITEM_LANDING_MIN_HOLDERS = 25


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


def item_length_corr():
    """{item name: length_corr}: item_landing's factors (or 1 for an item left uncut) x this for fights that book
    damage over real fight lengths (data/item_landing.json, scripts/fight_length/length_factors.py)."""
    if not LENGTH_CORR:
        return {}
    try:
        rows = json.load(open(ITEM_LANDING))["items"]
    except (OSError, ValueError, KeyError):
        return {}
    return {r["name"]: r["length_corr"] for r in rows.values()
            if "length_corr" in r and r["holders"] >= ITEM_LANDING_MIN_HOLDERS}


def zone_exit_time(badge=None):
    """Seconds a player stays in an avoidable ground zone (Alchemical Fire, 10 m radius, 5 s) before walking out:
    reaction time plus the walk to the edge. Assumption, like dot_cleanse_delay: 2.0 s for ranked overall,
    1.5 s from Ascendant up. Not measurable from the API (no zone positions)."""
    return 1.5 if badge is not None and badge >= 101 else 2.0


def gun_calibrated(hero_id):
    """True if this hero's aim comes from the replay calibration: its match stats have no usable gun accuracy, so
    data/skill_defaults.json has no row for it (a row there, once the API records the gun, takes precedence
    everywhere: hero_default_skill, default_distance, player_skill and the fits)."""
    return str(hero_id) in gun_calibration() and str(hero_id) not in _defaults()["heroes"]


_defaults_cache = None


def _defaults():
    global _defaults_cache
    if _defaults_cache is None:
        _defaults_cache = json.load(open(DEFAULTS))
    return _defaults_cache


def _aim_row(d, h):
    return d["heroes"].get(str(h.id)) or gun_calibration().get(str(h.id)) or d["all"]


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
    row = _aim_row(d, h)
    sk = Skill(accuracy=row["accuracy"][pct], headshot=row["headshot"][pct])
    if landing:
        sk.ability_landing = ability_landing(hero)
        sk.ability_landing_mech = ability_landing(hero, mech=True)
        sk.ability_length_corr = ability_length_corr(hero)
    if melee:
        sk.melee_rate = melee_rate(hero)
        if melee_build:
            sk.melee_item_mult = melee_item_mults(hero)
    if melee_rate_override is not None:
        sk.melee_rate = max(0.0, float(melee_rate_override))
        sk.melee_item_mult = None
    if heavy_share is not None:
        sk.heavy_share = min(1.0, max(0.0, float(heavy_share)))
    sk.dot_cleanse_delay = dot_cleanse_delay(badge)
    sk.dot_cleanse_share = dot_cleanse_share(badge)
    sk.dot_cleanse_share_buildup = dot_cleanse_share_buildup(badge)
    sk.spell_parry_rate, sk.spell_parry_rate_ult = spell_parry_rates(badge)
    # players walk out of ground zones (Alchemical Fire) unless stunned, rooted or slowed (items_fx.held_share);
    # on in every mode since 2026-10-21 (Tyler: no Alchemical Fire for heroes that can't hold a target in it)
    sk.zone_exit_s = zone_exit_time(badge)
    if counterplay:   # realistic mode: item damage calibrated to real matches
        sk.item_landing = item_landing()
        sk.item_length_corr = item_length_corr()
    return sk


def default_distance(hero):
    d = json.load(open(DEFAULTS))
    h = game().hero(hero)
    return _aim_row(d, h).get("median_distance_m", 15.0)
