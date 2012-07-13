import tournament_system
import unittest
from unittest.mock import Mock
import sys
import os
from tournament_stages.game_signature import GameSignature


class TournamentSystemTest(unittest.TestCase):
    def setUp(self):
        self.ts = tournament_system.TournamentSystem(
            [1, 2, 3],
            'OLolo'
        )

    def test_add_round_results(self):
        round_results = {'1': 'OLOLO'}
        self.ts.add_round_results(round_results)
        self.assertEqual(self.ts._results, round_results)
        self.assertEqual(self.ts._current_round_id, 1)

    def test_get_all_results(self):
        round_results = {'1': 'OLOLO'}
        self.ts.add_round_results(round_results)
        self.ts.add_round_results(round_results)
        round_results.update(round_results)
        self.assertEqual(self.ts.get_all_results(),
                         round_results)


if __name__ == "__main__":
    unittest.main()
