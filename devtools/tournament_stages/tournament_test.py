import unittest
import sys
import os
from unittest.mock import MagicMock, patch

project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
with patch.dict('sys.modules',
                {'tournament_systems.tournament_system': MagicMock(),
                 'TournamentSystem': MagicMock(),
                 'tournament_stages.round': MagicMock(),
                 'Round': MagicMock(),
                 'tournament_systems.tournament_system_factory': MagicMock(),
                 'create': MagicMock(),
                 'log': MagicMock(),
                 'logger': MagicMock()}):
    from tournament_systems.tournament_system import TournamentSystem
    from tournament_systems.tournament_system_factory import create
    from tournament_stages.round import Round
    from log import logger
    import tournament_stages.tournament as tournament_file


class TournamentTest(unittest.TestCase):
    def test_tournament(self):
        create()().get_results = 5
        create()().get_rounds.return_value = [{1: {1: 0, 2: 1}},
                                                      {2: {2: 0, 3: 1}}]
        create()().get_all_results.return_value = 'First player won'
        tournament = tournament_file.Tournament([1, 2, 3], 1)
        tournament.run()
        result = tournament.get_results()
        if result != 'First player won':
            raise Exception("tournament.py or 'patch.dict' doesn't work")

if __name__ == '__main__':
    unittest.main()
