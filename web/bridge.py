"""Browser entry point for the custom damage test (runs in Pyodide; also works in plain CPython).

run(json_str) takes the page's form as JSON and returns damage_test()'s result plus the settings actually used:
    {"hero": "Haze", "items": [ids or names], "souls": 27000, "aim": "p50", "accuracy": null, "headshot": null,
     "distance": null, "melee_rate": null, "ability_order": null, "dummy": {"hero": "Abrams", "items": [...], "souls": null, "hp": null,
     "bullet_resist": null, "spirit_resist": null, "melee_resist": null, "immortal": true}}
"""
import json

from deadsim.accuracy import default_distance, hero_default_skill
from deadsim.data import game
from deadsim.fight import melee_build_mult
from dummy import Dummy, damage_test


def _item(G, x):
    return G.item(int(x) if isinstance(x, (int, float)) or str(x).isdigit() else x)


def _setup(q):
    """The page's JSON -> (hero name, item names, damage_test kwargs)."""
    G = game()
    hero = G.hero(q["hero"])
    items = [_item(G, x) for x in q.get("items", [])]
    skill = hero_default_skill(hero.name, q.get("aim") or "p50")
    if q.get("accuracy") is not None:
        skill.accuracy = float(q["accuracy"])
    if q.get("headshot") is not None:
        skill.headshot = float(q["headshot"])
    if q.get("melee_rate") is not None:   # own landed melees per second; else the rate follows the build
        skill.melee_rate = max(0.0, float(q["melee_rate"]))
        skill.melee_item_mult = None
    dq = q.get("dummy") or {}
    dummy = Dummy(
        hero=G.hero(dq.get("hero") or "Haze").name,
        items=[_item(G, x).name for x in dq.get("items", [])],
        souls=dq.get("souls"), hp=dq.get("hp"),
        bullet_resist=dq.get("bullet_resist"), spirit_resist=dq.get("spirit_resist"),
        melee_resist=dq.get("melee_resist"), immortal=bool(dq.get("immortal", True)),
        zone_exit_s=dq.get("zone_exit_s"))
    kw = dict(souls=q.get("souls"), dummy=dummy, skill=skill, distance=q.get("distance"),
              ability_order=[int(x) for x in q.get("ability_order") or []] or None)
    return hero, items, kw


def _melee_rate(skill, items):
    """Landed melees per second the fight used (scaled by the build's melee items, fight.melee_build_mult)."""
    return round(skill.melee_rate * melee_build_mult(skill, items), 4)


def run(req_json):
    q = json.loads(req_json)
    hero, items, kw = _setup(q)
    r = damage_test(hero.name, [i.name for i in items], **kw)
    r["used"] = {
        "hero": hero.name, "items": [i.name for i in items], "item_cost": sum(i.cost for i in items),
        "accuracy": round(kw["skill"].accuracy, 4), "headshot": round(kw["skill"].headshot, 4),
        "distance": kw["distance"] if kw["distance"] is not None else default_distance(hero.name),
        "melee_rate": _melee_rate(kw["skill"], items),
    }
    return json.dumps(r)


def breakdown(req_json):
    """What each item adds to the build's damage, from one run without each item (same request as run()).

    loss: damage lost by each mark when the item is removed. share: the build's damage above the no-item hero split
    across items in proportion to their positive loss, so base + shares = total. sources: change in each damage
    source (30 s) the item causes; direct: damage booked under the item's own name (its procs)."""
    q = json.loads(req_json)
    hero, items, kw = _setup(q)
    names = [i.name for i in items]
    full = damage_test(hero.name, names, **kw)
    base = damage_test(hero.name, [], **kw)
    marks = list(full["damage"])
    out = {"total": full["damage"], "base": base["damage"], "sources": full["sources"], "items": []}
    for it in items:
        r = damage_test(hero.name, [n for n in names if n != it.name], **kw)
        delta = {k: round(v - r["sources"].get(k, 0.0), 1) for k, v in full["sources"].items()}
        for k, v in r["sources"].items():
            if k not in full["sources"]:
                delta[k] = round(-v, 1)
        out["items"].append({
            "id": it.id, "name": it.name, "cost": it.cost,
            "loss": {m: round(full["damage"][m] - r["damage"][m], 1) for m in marks},
            "direct": round(sum(v for k, v in full["sources"].items() if k == it.name or k.startswith(it.name + " ")), 1),
            "sources": {k: v for k, v in sorted(delta.items(), key=lambda x: -abs(x[1])) if abs(v) >= 1},
        })
    for m in marks:
        extra = full["damage"][m] - base["damage"][m]
        pos = sum(max(0.0, x["loss"][m]) for x in out["items"])
        for x in out["items"]:
            x.setdefault("share", {})[m] = round(extra * max(0.0, x["loss"][m]) / pos, 1) if pos > 0 else 0.0
    return json.dumps(out)


def team(req_json):
    """Team fight (2v2, 3v3). {"a": [{"hero", "items", "souls"?, "aim"?}], "b": [...], "souls": 27000,
    "focus": "focus" | "spread", "distance": null, "max_time": 40} -> deadsim.team.TeamResult.to_dict()."""
    from deadsim import Loadout
    from deadsim.team import team_fight
    q = json.loads(req_json)
    G = game()
    souls = q.get("souls")
    sides = []
    for side in ("a", "b"):
        team = []
        for m in q.get(side, [])[:6]:
            hero = G.hero(m["hero"])
            items = [_item(G, x).name for x in m.get("items", [])]
            team.append(Loadout(hero.name, items, souls=m.get("souls") or souls,
                                skill=hero_default_skill(hero.name, m.get("aim") or q.get("aim") or "p50")))
        sides.append(team)
    r = team_fight(sides[0], sides[1], distance=q.get("distance") or 15.0, max_time=q.get("max_time") or 40.0,
                   focus=q.get("focus") or "focus")
    return json.dumps(r.to_dict())


def _real_abilities(hero, events):
    """(tiers, unlocked) from a real match's ability purchases so far: the first time an ability id appears unlocks
    it, each later time buys its next upgrade (the match metadata lists ability buys among the items)."""
    ids = [a.id for a in hero.abilities]
    n = [sum(1 for e in events if int(e) == i) for i in ids]
    return [max(0, min(3, k - 1)) for k in n], [k > 0 for k in n]


def replay(req_json):
    """A real fight replayed in the team sim (web/replay.js). {"a": [member], "b": [member], "distance": m,
    "max_time": s, "focus": "focus"}; member = {"hero", "items", "souls", "accuracy"?, "headshot"?, "hp"? (share of
    max health at the fight's start), "abilities"? (ability ids bought so far, in order)}.
    Returns deadsim.team.TeamResult.to_dict() plus each hero's start health in "start_hp"."""
    from deadsim import Loadout
    from deadsim.team import team_fight
    q = json.loads(req_json)
    G = game()
    sides, start = [], []
    for side in ("a", "b"):
        team = []
        for m in q.get(side, [])[:6]:
            hero = G.hero(m["hero"])
            skill = hero_default_skill(hero.name, m.get("aim") or "p50")
            if m.get("accuracy") is not None:
                skill.accuracy = float(m["accuracy"])
            if m.get("headshot") is not None:
                skill.headshot = float(m["headshot"])
            tiers = unlocked = None
            if m.get("abilities"):
                tiers, unlocked = _real_abilities(hero, m["abilities"])
                if not any(unlocked):
                    tiers = unlocked = None
            team.append(Loadout(hero.name, [_item(G, x).name for x in m.get("items", [])], souls=m.get("souls"),
                                skill=skill, tiers=tiers, unlocked=unlocked))
            start.append(m.get("hp"))
        sides.append(team)
    r = team_fight(sides[0], sides[1], distance=float(q.get("distance") or 15.0),
                   max_time=float(q.get("max_time") or 20.0), focus=q.get("focus") or "focus", start_hp=start)
    out = r.to_dict()
    for row, frac in zip(out["fighters"], start):
        row["start_hp"] = round(row["max_hp"] * (1.0 if frac is None else max(0.0, min(1.0, float(frac)))), 1)
    return json.dumps(out)


# ---------- build maker (web/maker.js) ----------
class _Refill:
    """Both sides refill on lethal damage, so a fight always runs its full length; the first lethal moment is the
    time to kill, and refills x max HP + HP missing at the end is the HP really lost (after heals and barriers)."""
    item = None
    name = "refill"

    def __init__(self):
        self.first, self.n = None, 0

    def on_lethal(self, f, attacker):
        if self.first is None:
            self.first = f.e.t
        self.n += 1
        f.hp = f.max_hp
        return True


_maker_skill = {}


def _maker_sk(name, aim):
    """Phantom+ habits (lowest badge 91) with counterplay on, the overall search's setting."""
    k = (name, aim)
    if k not in _maker_skill:
        _maker_skill[k] = hero_default_skill(name, aim, badge=91, counterplay=True)
    return _maker_skill[k]


def _skirmish(G, me, foe, T, aim):
    import dataclasses
    from deadsim import Loadout, mechanics
    from deadsim.engine import Engine
    from deadsim.fight import make_fighter
    hn, en = G.hero(me["hero"]).name, G.hero(foe["hero"]).name
    # movement off, as in the survival and overall searches: running away isn't damage dealt or taken
    mech = dataclasses.replace(mechanics.DEFAULT, movement=False) if mechanics.DEFAULT else None
    e = Engine(distance=(default_distance(hn) + default_distance(en)) / 2, max_time=T, mech=mech)
    a = make_fighter(e, Loadout(hn, [_item(G, x).name for x in me["items"]], souls=me.get("souls") or None,
                                skill=_maker_sk(hn, aim)), "you")
    b = make_fighter(e, Loadout(en, [_item(G, x).name for x in foe["items"]], souls=foe.get("souls") or None,
                                skill=_maker_sk(en, aim)), "enemy")
    ra, rb = _Refill(), _Refill()
    a.items_fx.append(ra)
    b.items_fx.append(rb)
    hp_a, hp_b = a.max_hp, b.max_hp
    e.run(a, b)

    def kill_time(r, f, hp0):
        if r.first is not None:
            return r.first
        lost = r.n * f.max_hp + max(0.0, f.max_hp - f.hp)
        return T * hp0 / lost if lost > 1 else 999.0

    top = lambda d: [[k, round(v)] for k, v in sorted(d.items(), key=lambda x: -x[1])[:3] if v >= 1]
    return {
        "dealt": round(sum(a.dmg_out.values()), 1), "taken": round(sum(a.dmg_in.values()), 1),
        "ttk": round(min(999.0, kill_time(rb, b, hp_b)), 2), "ttd": round(min(999.0, kill_time(ra, a, hp_a)), 2),
        "hp": round(hp_a), "enemy_hp": round(hp_b),
        "enemy_heal": round(getattr(b, "healed", 0.0) or 0.0, 1),
        "top_dealt": top(a.dmg_out), "top_taken": top(a.dmg_in),
    }


def maker(req_json):
    """Your build against each enemy build, both fighting back for T seconds (default 15) and refilling instead of
    dying. {"hero", "items", "souls", "aim", "T", "enemies": [{"hero", "items", "souls"}],
    "variants": [[items], ...]} -> {"variants": [[per-enemy result, ...], ...]} (variants default to [items])."""
    q = json.loads(req_json)
    G = game()
    T, aim = float(q.get("T") or 15.0), q.get("aim") or "p75"
    out = []
    for items in q.get("variants") or [q.get("items", [])]:
        me = {"hero": q["hero"], "items": items, "souls": q.get("souls")}
        out.append([_skirmish(G, me, foe, T, aim) for foe in q.get("enemies", [])])
    return json.dumps({"variants": out})
