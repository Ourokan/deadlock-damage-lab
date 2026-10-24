"""Hand-calculated checks of the combat model. Run: python3 -m unittest discover -s tests -v (from sim/)."""
import heapq
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim import Loadout, Skill, compute_stats, game, time_to_kill  # noqa: E402
from deadsim.build import combine_resist  # noqa: E402
from deadsim.engine import Accum, Engine  # noqa: E402
from deadsim.fight import make_fighter  # noqa: E402

G = game()


# hand-calculated at one fixed distance: range spread (mechanics range_drift) off, see tests/test_range_items.py
def setUpModule():
    global _DEFAULT
    import deadsim.mechanics as M
    _DEFAULT, M.DEFAULT = M.DEFAULT, M.Mechanics(range_drift=False)


def tearDownModule():
    import deadsim.mechanics as M
    M.DEFAULT = _DEFAULT


PERFECT = Skill(accuracy=1.0, headshot=0.0, use_abilities=False, use_actives=False)


def gun_damage_after(attacker, defender, seconds, distance=10.0):
    r = time_to_kill(attacker, defender, distance=distance, max_time=seconds)
    return r.a_dmg.get("gun", 0.0), r


class Resists(unittest.TestCase):
    def test_wiki_stacking_example(self):
        # deadlock.wiki: 60% and 40% bullet resist -> 76%
        self.assertAlmostEqual(combine_resist([0.6, 0.4]), 0.76)

    def test_reduction_subtracts_after_stacking(self):
        # 30% and 18% -> 1 - .7*.82 = 42.6%; a 10% shred then subtracts -> 32.6%
        self.assertAlmostEqual(combine_resist([0.3, 0.18], [0.10]), 0.326, places=6)

    def test_negative_resist_amplifies(self):
        self.assertAlmostEqual(combine_resist([], [0.12]), -0.12)


class Stats(unittest.TestCase):
    def test_level_and_boons(self):
        h = G.hero("Infernus")
        self.assertEqual(G.level_for_souls(h, 800), 3)   # thresholds 0/200/500/900
        st = compute_stats("Infernus", ["Extra Health"], souls=800)
        self.assertEqual(st.boons, 1)

    def test_health_formula(self):
        # (830 base + 1 boon * 39) * (1 + 9% vitality invest at 800) + 210 Extra Health
        st = compute_stats("Infernus", ["Extra Health"], souls=800)
        self.assertAlmostEqual(st.max_health, (830 + 39) * 1.09 + 210, places=6)

    def test_spirit_formula(self):
        # 1 boon * 1.1 + 7 spirit invest (800 in spirit) + 10 Extra Spirit
        st = compute_stats("Infernus", ["Extra Spirit"], souls=800)
        self.assertAlmostEqual(st.spirit_power, 1.1 + 7 + 10, places=6)

    def test_weapon_pct_is_additive(self):
        # High-Velocity Rounds 8% + Extended Magazine 8% + weapon invest at 1600 (12%) = 28%
        st = compute_stats("Infernus", ["High-Velocity Rounds", "Extended Magazine"], souls=1600)
        self.assertAlmostEqual(st.weapon_pct, 0.28, places=6)
        self.assertEqual(st.clip, round(27 * 1.30))

    def test_falloff_and_crit(self):
        st = compute_stats("Infernus", [], souls=0)
        self.assertAlmostEqual(st.falloff(10), 1.0)       # inside 18 m start
        self.assertAlmostEqual(st.falloff(60), 0.1)       # past 55 m end
        mid = (18.0 + 55.0) / 2
        self.assertAlmostEqual(st.falloff(mid), 0.55, places=2)   # bias 0.5 = linear
        self.assertAlmostEqual(st.crit_mult(10), 1.65)


class Gun(unittest.TestCase):
    def test_raw_gun_damage_two_seconds(self):
        # Infernus, 0 souls: 5.5 per bullet, a shot every 0.105 s from t=0 -> 20 shots in [0, 2.0]
        dmg, _ = gun_damage_after(Loadout("Infernus", [], souls=0, skill=PERFECT),
                                  Loadout("Abrams", [], souls=0), 2.0)
        self.assertAlmostEqual(dmg, 20 * 5.5, places=6)

    def test_reload_gap(self):
        # 27-round clip: 27 shots by t=2.73, reload 2.25 s, next shot at 2.73+0.105+2.25 = 5.085
        dmg, _ = gun_damage_after(Loadout("Infernus", [], souls=0, skill=PERFECT),
                                  Loadout("Abrams", [], souls=0), 5.0)
        self.assertAlmostEqual(dmg, 27 * 5.5, places=6)

    def test_headshots_and_bullet_resist(self):
        sk = Skill(accuracy=1.0, headshot=0.5, use_abilities=False, use_actives=False)
        # 20 shots, 10 headshots at 1.65x; target has Bullet Resilience 30% -> * 0.7
        dmg, _ = gun_damage_after(Loadout("Infernus", [], souls=0, skill=sk),
                                  Loadout("Abrams", ["Bullet Resilience"], souls=0), 2.0)
        self.assertAlmostEqual(dmg, (10 * 5.5 + 10 * 5.5 * 1.65) * 0.7, places=6)

    def test_accuracy_accumulator(self):
        a = Accum()
        self.assertEqual(sum(a.take(0.57) for _ in range(100)), 57)


class Abilities(unittest.TestCase):
    def test_spirit_scaling(self):
        e = Engine()
        f = make_fighter(e, Loadout("Infernus", ["Extra Spirit"], souls=800, tiers=[0, 0, 0, 0]))
        napalm = f.abilities[0]
        self.assertAlmostEqual(napalm.ctx.val("Damage"), 40 + 0.6 * f.st.spirit_power, places=6)

    def test_cooldown_reduction_multiplies(self):
        e = Engine()
        f = make_fighter(e, Loadout("Infernus", ["Superior Cooldown"], souls=3200, tiers=[0, 0, 0, 0]))
        # Napalm 25 s * (1 - 20%)
        self.assertAlmostEqual(f.abilities[0].cooldown(), 25 * 0.8, places=6)


class Items(unittest.TestCase):
    def test_toxic_bullets_bleed(self):
        # build-up per hit = 1.28% x 5.5 base bullet damage x 1.4 = 9.9% -> 11th hit procs; bleed 1.9% max HP/s, 4 s
        sk = Skill(accuracy=1.0, headshot=0.0, use_abilities=False, use_actives=False)
        r = time_to_kill(Loadout("Infernus", ["Toxic Bullets"], souls=3200, skill=sk, unlocked=[False] * 4),
                         Loadout("Abrams", [], souls=3200), distance=10, max_time=14.0)
        self.assertGreater(r.a_dmg.get("Toxic Bullets", 0), 0)

    def test_buildup_per_hero_matches_wiki(self):
        # deadlock.wiki: Toxic Bullets build-up per shot, Wraith 10.3%, Ivy 8.2% (within the 1.4 fit's spread)
        for hero, wiki in (("Wraith", 10.3), ("Ivy", 8.2)):
            e = Engine(distance=10)
            f = make_fighter(e, Loadout(hero, ["Toxic Bullets"], souls=3200))
            tb = next(fx for fx in f.items_fx if fx.item.name == "Toxic Bullets")
            self.assertAlmostEqual(tb.per_hit(f), wiki, delta=0.05 * wiki)

    def test_melee_rotation_light_damage(self):
        # 1 melee/s, 0 souls: first at 0.5 s, then 1.5, 2.5 ... -> 5 hits by 4.6 s; with 30% heavy -> accum gives
        # heavies at hit 2 and 5 (phase 0.5): 3 x 50 light + 2 x 116 heavy = 382 melee damage
        sk = Skill(accuracy=0.0, headshot=0.0, use_abilities=False, use_actives=False, melee_rate=1.0)
        r = time_to_kill(Loadout("Infernus", [], souls=0, skill=sk), Loadout("Abrams", [], souls=0),
                         distance=10, max_time=4.6)
        self.assertAlmostEqual(r.a_dmg.get("melee", 0), 3 * 50 + 2 * 116, places=6)

    def test_melee_heavy_share_override(self):
        # same as above with every melee heavy: each 1.1 s swing delays the next -> hits at 0.5, 1.6, 2.7, 3.8
        sk = Skill(accuracy=0.0, headshot=0.0, use_abilities=False, use_actives=False, melee_rate=1.0,
                   heavy_share=1.0)
        r = time_to_kill(Loadout("Infernus", [], souls=0, skill=sk), Loadout("Abrams", [], souls=0),
                         distance=10, max_time=4.6, mechanics=None)  # no parries
        self.assertAlmostEqual(r.a_dmg.get("melee", 0), 4 * 116, places=6)

    def test_user_melee_rate_override(self):
        from deadsim.accuracy import hero_default_skill
        sk = hero_default_skill("Abrams", melee_rate_override=0.8, heavy_share=0.5)
        self.assertEqual((sk.melee_rate, sk.heavy_share), (0.8, 0.5))
        self.assertGreater(hero_default_skill("Abrams").melee_rate, 0.1)
        self.assertIsNone(sk.melee_item_mult)   # the user's own rate is not scaled by the build

    def test_melee_rate_follows_melee_items(self):
        from deadsim.accuracy import hero_default_skill, melee_rate
        from dataclasses import replace
        from deadsim.accuracy import melee_rates_by_items
        sk = hero_default_skill("Haze")
        r0, r1, r2 = melee_rates_by_items("Haze")
        self.assertLess(r0, r1)
        self.assertLess(r1, r2)
        self.assertAlmostEqual(r0, melee_rate("Haze"), delta=0.3 * melee_rate("Haze"))  # most Haze players: none
        e = Engine(distance=10)
        rates = [make_fighter(e, Loadout("Haze", its, souls=20000, skill=sk)).skill.melee_rate
                 for its in ([], ["Melee Charge"], ["Melee Charge", "Lifestrike"], ["Melee Charge", "Lifestrike",
                                                                                    "Spirit Snatch"])]
        for got, want in zip(rates, [r0, r1, r2, r2]):
            self.assertAlmostEqual(got, want, places=3)
        self.assertEqual(sk.melee_rate, melee_rate("Haze"))   # the Skill itself keeps the average
        # a caller's own melee_rate is scaled, not replaced: 0 stays 0
        f = make_fighter(e, Loadout("Haze", ["Melee Charge"], souls=20000, skill=replace(sk, melee_rate=0.0)))
        self.assertEqual(f.skill.melee_rate, 0.0)

    def test_melee_build_rates_keep_hero_average(self):
        # the hero's real mix of builds (data/melee_items.json "mix") still averages to its fitted rate
        import json
        from deadsim.accuracy import MELEE_ITEMS_FILE, melee_rate, melee_rates_by_items
        rows = json.load(open(MELEE_ITEMS_FILE))["heroes"]
        for hero in ("Abrams", "Haze", "Drifter", "Bebop"):
            mix = rows[str(G.hero(hero).id)]["mix"]
            by = melee_rates_by_items(hero)
            avg = sum(mix[g] * r for g, r in zip(("0", "1", "2+"), by))
            self.assertAlmostEqual(avg, melee_rate(hero), delta=0.002 + 0.01 * melee_rate(hero))

    def test_melee_build_rates_missing_data(self):
        import deadsim.accuracy as A
        old = A.MELEE_ITEMS_FILE
        A.MELEE_ITEMS_FILE = os.path.join(os.path.dirname(old), "no_such_file.json")
        try:
            self.assertIsNone(A.melee_rates_by_items("Haze"))
            self.assertIsNone(A.hero_default_skill("Haze").melee_item_mult)
        finally:
            A.MELEE_ITEMS_FILE = old
        # a hero missing from the fit keeps the flat rate
        rows = A._melee_items()["heroes"]
        hid = str(G.hero("Haze").id)
        row = rows.pop(hid)
        try:
            self.assertIsNone(A.melee_item_mults("Haze"))
        finally:
            rows[hid] = row

    def test_team_fight_uses_build_melee_rate(self):
        from deadsim.accuracy import hero_default_skill
        from deadsim.team import TeamEngine
        from deadsim.accuracy import melee_rates_by_items
        sk = hero_default_skill("Haze")
        f = make_fighter(TeamEngine(distance=10), Loadout("Haze", ["Melee Charge", "Lifestrike"], souls=20000, skill=sk))
        self.assertAlmostEqual(f.skill.melee_rate, melee_rates_by_items("Haze")[2], places=3)

    def test_web_melee_rate_override(self):
        import json
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "web"))
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "damage"))
        import bridge
        from deadsim.accuracy import melee_rates_by_items
        q = {"hero": "Haze", "items": ["Melee Charge"], "souls": 15000}
        hero, items, kw = bridge._setup(dict(q, melee_rate=0))
        self.assertEqual((kw["skill"].melee_rate, kw["skill"].melee_item_mult), (0.0, None))
        self.assertEqual(bridge._melee_rate(kw["skill"], items), 0.0)
        hero, items, kw = bridge._setup(q)
        self.assertAlmostEqual(bridge._melee_rate(kw["skill"], items), melee_rates_by_items("Haze")[1], places=3)
        self.assertIn("melee_rate", json.loads(bridge.run(json.dumps(dict(q, melee_rate=0.25))))["used"])

    def test_melee_charge_heavy_lunge_reach(self):
        from deadsim.mechanics import MELEE_REACH, melee_reach
        e = Engine(distance=3)
        a = make_fighter(e, Loadout("Abrams", ["Melee Charge"], souls=9000))
        b = make_fighter(e, Loadout("Abrams", [], souls=9000))
        self.assertAlmostEqual(melee_reach(a, True), MELEE_REACH * 1.5)   # MeleeDistanceScale 50%
        self.assertAlmostEqual(melee_reach(a, False), MELEE_REACH)
        self.assertAlmostEqual(melee_reach(b, True), MELEE_REACH)
        c = make_fighter(e, Loadout("Abrams", ["Melee Charge", "Runed Gauntlets"], souls=20000))
        self.assertAlmostEqual(melee_reach(c, True), MELEE_REACH * 2.5)   # Runed Gauntlets 150%, the largest held

    def test_melee_charge_heavy_lands_from_farther_in_fight(self):
        # chase gap of 8 m beyond the start distance: past light reach (6 m), inside Melee Charge heavy reach (9 m)
        from types import SimpleNamespace
        from deadsim.mechanics import melee_reach
        for items, heavy, lands in ((["Melee Charge"], 1.0, True), ([], 1.0, False), (["Melee Charge"], 0.0, False)):
            e = Engine(distance=11)
            sk = Skill(accuracy=0.0, use_abilities=False, use_actives=False, melee_rate=1.0, heavy_share=heavy)
            a = make_fighter(e, Loadout("Abrams", items, souls=9000, skill=sk))
            b = make_fighter(e, Loadout("Haze", [], souls=9000))
            a.enemy, b.enemy = b, a
            e.mover = SimpleNamespace(start=3.0, melee_reach=melee_reach)
            e.melee_tick(a)
            self.assertEqual(a.dmg_out.get("melee", 0) > 0, lands, (items, heavy))

    def test_runed_gauntlets_heavy_melee_cuts_cooldowns(self):
        e = Engine(distance=3)
        a = make_fighter(e, Loadout("Abrams", ["Runed Gauntlets"], souls=9000))
        b = make_fighter(e, Loadout("Haze", [], souls=9000))
        a.enemy, b.enemy = b, a
        a.abilities[0].ready_at = 20.0
        a.abilities[1].ready_at = 40.0
        e.melee_hit(a, heavy=True)
        self.assertAlmostEqual(a.abilities[0].ready_at, 16.0)                 # min 4 s
        self.assertAlmostEqual(a.abilities[1].ready_at, 40.0 - 40.0 * 0.16)   # 16% of remaining
        e.melee_hit(a, heavy=True)                                            # item on cooldown
        self.assertAlmostEqual(a.abilities[0].ready_at, 16.0)

    def test_unstoppable_blocks_stun(self):
        e = Engine(distance=10)
        a = make_fighter(e, Loadout("Haze", ["Unstoppable"], souls=9000))
        b = make_fighter(e, Loadout("Abrams", [], souls=9000))
        a.enemy, b.enemy = b, a
        charge = next(s for s in b.abilities if s.ab.name == "Shoulder Charge")
        for fx in a.items_fx:
            fx.on_enemy_cast(a, charge)
        self.assertGreaterEqual(a.stat("status_resist"), 1.0)

    def test_per_bullet_bonus_is_per_shot_on_shotguns(self):
        from deadsim.engine import Hit
        from deadsim.items_fx import shots_hit
        e = Engine(distance=5)
        a = make_fighter(e, Loadout("Abrams", [], souls=3000))   # 9 pellets
        self.assertEqual(a.st.pellets, 9)
        self.assertAlmostEqual(shots_hit(a, Hit("bullet", "gun", 100, 100, hits=9)), 1.0)

    def test_mystic_burst_needs_80_damage(self):
        e = Engine()
        a = make_fighter(e, Loadout("Infernus", ["Mystic Burst"], souls=800))
        b = make_fighter(e, Loadout("Abrams", [], souls=800))
        a.enemy, b.enemy = b, a
        e.damage(a, b, 50, "spirit", "small", is_ability=True)
        self.assertNotIn("Mystic Burst", a.dmg_out)
        e.damage(a, b, 120, "spirit", "big", is_ability=True)
        self.assertAlmostEqual(a.dmg_out["Mystic Burst"], 40.0, places=6)

    def test_capacitor_shock_still_procs_after_its_active(self):
        # the 40 s active cooldown used to switch the passive shock off too
        from deadsim.engine import Hit
        e = Engine(distance=10)
        a = make_fighter(e, Loadout("Wraith", ["Capacitor"], souls=9000, skill=Skill(use_actives=True)))
        b = make_fighter(e, Loadout("Abrams", [], souls=9000))
        a.enemy, b.enemy = b, a
        fx = next(x for x in a.items_fx if x.item.name == "Capacitor")
        self.assertTrue(fx.try_active(a))
        before = a.dmg_out.get("Capacitor", 0.0)
        for i in range(100):   # t = 1 .. 25.75 s: inside the active's 40 s cooldown
            e.t = 1.0 + i * 0.25
            fx.on_damage_dealt(a, b, Hit("bullet", "gun", 50, 50, hits=1))
        self.assertLess(e.t, fx.ready_at)
        self.assertGreater(a.dmg_out.get("Capacitor", 0.0) - before, 0.0)

    def test_siphon_bullets_takes_current_health(self):
        from deadsim.engine import Hit
        e = Engine(distance=10)
        a = make_fighter(e, Loadout("Wraith", ["Siphon Bullets"], souls=9000))
        b = make_fighter(e, Loadout("Abrams", [], souls=9000))
        a.enemy, b.enemy = b, a
        b.hp = b.max_hp * 0.5   # hurt: lowering the cap alone would not touch its health
        hp = b.hp
        fx = next(x for x in a.items_fx if x.item.name == "Siphon Bullets")
        fx.on_damage_dealt(a, b, Hit("bullet", "gun", 50, 50, hits=1))
        self.assertGreater(a.dmg_out.get("Siphon Bullets", 0.0), 0.0)
        self.assertAlmostEqual(hp - b.hp, a.dmg_out["Siphon Bullets"], places=6)

    def test_ability_sub_source_uses_its_ability_landing_factor(self):
        e = Engine()
        sk = Skill(ability_landing={"Setup Bishop": 0.5})
        a = make_fighter(e, Loadout("Solomon", [], souls=9000, skill=sk))
        b = make_fighter(e, Loadout("Abrams", [], souls=9000))
        a.enemy, b.enemy = b, a
        ab = next(s for s in a.abilities if s.ab.name == "Setup Bishop")
        e.damage(a, b, 100, "spirit", "Setup Bishop squares", is_ability=True, ability=ab, ignore_resist=True)
        self.assertAlmostEqual(a.dmg_out["Setup Bishop squares"], 50.0, places=6)

    def test_hunters_aura_doubles_in_1v1(self):
        e = Engine(distance=10)
        a = make_fighter(e, Loadout("Infernus", ["Hunter's Aura"], souls=3200))
        b = make_fighter(e, Loadout("Abrams", [], souls=3200))
        a.enemy, b.enemy = b, a
        for fx in a.items_fx:
            fx.on_start(a)
        self.assertAlmostEqual(sum(b.mods.values("bullet_shred")), 0.20)
        self.assertAlmostEqual(b.stat("fire_rate_slow"), 0.30)


class FocusLensExpire(unittest.TestCase):
    def test_stored_damage_is_not_amplified_twice(self):
        # Focus Lens re-deals 35% of the damage taken during the silence; that damage already had Escalating
        # Exposure's spirit amp, so the expire hit must not get the amp again
        e = Engine(distance=10.0, max_time=30.0)
        a = make_fighter(e, Loadout("Haze", ["Focus Lens"], souls=30000, skill=PERFECT), "a")
        d = make_fighter(e, Loadout("Abrams", [], souls=30000, skill=PERFECT), "d")
        d.abilities = []
        d.mods.add("spirit_amp_taken", 0.5, 30.0, "test")
        fl = next(fx for fx in a.items_fx if fx.item.name == "Focus Lens")
        fl.extra(a, d)
        e.damage(a, d, 1000.0, "spirit", "test hit", ignore_resist=True)   # lands as 1500 with the amp
        while e.q and e.t < 10.0:   # step the event queue past the silence
            t, _, fn, args = heapq.heappop(e.q)
            e.t = t
            fn(*args)
        self.assertAlmostEqual(a.dmg_out.get("Focus Lens", 0.0), 1500.0 * 0.35, delta=1.0)


if __name__ == "__main__":
    unittest.main()

