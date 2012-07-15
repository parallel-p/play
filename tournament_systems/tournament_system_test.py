from tournament_systems.tournament_system import TournamentSystem
import unittest
import sys
import os
from copy import copy

PROJECT_ROOT = os.path.normpath(os.path.join(
                                os.path.dirname(__file__), '..'))
if not PROJECT_ROOT in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tournament_stages.game_signature import GameSignature


class TournamentSystemTest(unittest.TestCase):
    def setUp(self):
        self.ts = TournamentSystem(
            ['player1', 'player2'],
        )

    def test_add_round_results(self):
        round_results = {'1': 'OLOLO'}
        self.ts.add_round_results(round_results)
        self.assertEqual(self.ts._results, round_results)
        self.assertEqual(self.ts._current_round_id, 1)

    def test_get_all_results(self):
        signature = GameSignature(1, 1, 1, 1)
        game_results = {'player1': 1, 'player2': 2}
        round_results = {signature: game_results}
        self.ts.add_round_results(round_results)
        self.ts.add_round_results(round_results)
        round_results.update(round_results)
        self.assertEqual(self.ts.get_all_results(),
                         round_results)

    def test_get_round_results(self):
        signature = GameSignature(1, 1, 1, 1)
        game_results = {'player1': 1, 'player2': 2}
        round_results1 = {signature: game_results}
        self.ts.add_round_results(round_results1)
        signature = copy(signature)
        signature.round_id = 2
        game_results = {'player1': 3, 'player2': 4}
        round_results2 = {signature: game_results}
        self.ts.add_round_results(round_results2)
        self.assertEqual(self.ts.get_round_results(2), round_results2)
        self.assertEqual(self.ts.get_round_results(1), round_results1)

    def test_get_current_round_results(self):
        signature = GameSignature(1, 1, 1, 1)
        game_results = {'player1': 1, 'player2': 2}
        round_results1 = {signature: game_results}
        self.ts.add_round_results(round_results1)
        signature = copy(signature)
        signature.round_id = 2
        game_results = {'player1': 3, 'player2': 4}
        round_results2 = {signature: game_results}
        self.ts.add_round_results(round_results2)
        self.assertEqual(self.ts.get_current_round_results(), round_results2)


if __name__ == "__main__":
    unittest.main()
