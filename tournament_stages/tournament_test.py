import unittest
import sys
import os
from unittest.mock import MagicMock, patch, Mock


with patch.dict('sys.modules',
                {'tournament_stages.round': MagicMock(),
                 'tournament_systems.tournament_system_factory': MagicMock(),
                 'log': MagicMock()}):
    import tournament_systems.tournament_system_factory as factory
    from tournament_stages.round import Round
    from log import logger
    import tournament_stages.tournament as tournament_file


class TournamentTest(unittest.TestCase):
    def test_tournament(self):
        tournament_file.Round = Mock()
        tournament_file.create = Mock()
        tournament_file.tournament_system = Mock()
        tournament_file.create()().get_results = 5
        tournament_file.create()().get_rounds.return_value = [{1: {1: 0, 2: 1}},
                                                      {2: {2: 0, 3: 1}}]
        tournament_file.create()().get_all_results.return_value = 'First player won'
        tournament = tournament_file.Tournament([1, 2, 3], 1)
        tournament.run()
        self.assertEqual(tournament.get_results(), 'First player won')

if __name__ == '__main__':
    unittest.main()
