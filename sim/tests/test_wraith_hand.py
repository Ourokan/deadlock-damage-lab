"""Wraith's opening hand (heroes/wraith.py ENTRY_HAND, 2026-11-08): with fight draws the hand at a fight's start
follows Phantom+ replays (1.4 cards on average, 22% none), capped at max charges; without draws it stays full.
Melee hits build cards too. Run: python3 -m unittest discover -s tests -v (from sim/)."""
import os
import random
import sys
import types
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadsim.heroes import wraith  # noqa: E402


def ctx(phase=None, rng=None, name="Wraith"):
    f = types.SimpleNamespace(skill=types.SimpleNamespace(fight_phase=phase), e=types.SimpleNamespace(rng=rng),
                              name=name)
    return types.SimpleNamespace(me=f)


class WraithHand(unittest.TestCase):
    def test_no_draws_full_hand(self):
        self.assertEqual(wraith.entry_hand(ctx(), 4), 4)

    def test_rng_draws_follow_replays(self):
        rng = random.Random(1)
        hands = [wraith.entry_hand(ctx(rng=rng), 4) for _ in range(20000)]
        mean = sum(hands) / len(hands)
        self.assertGreater(mean, 1.2)
        self.assertLess(mean, 1.6)
        self.assertAlmostEqual(hands.count(0) / len(hands), 984 / sum(wraith.ENTRY_HAND), delta=0.02)
        self.assertLessEqual(max(hands), 4)

    def test_phase_draws_are_deterministic(self):
        self.assertEqual(wraith.entry_hand(ctx(phase=0.3), 4), wraith.entry_hand(ctx(phase=0.3), 4))

    def test_switch_off_keeps_full_hand(self):
        old = wraith.ENTRY_HAND_DRAW
        try:
            wraith.ENTRY_HAND_DRAW = False
            self.assertEqual(wraith.entry_hand(ctx(rng=random.Random(1)), 4), 4)
        finally:
            wraith.ENTRY_HAND_DRAW = old


if __name__ == "__main__":
    unittest.main()
