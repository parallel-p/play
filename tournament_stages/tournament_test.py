import unittest
import sys
from unittest.mock import MagicMock, Mock, patch

if 'C:\\Users\\Admin\\smth\\play' not in sys.path:
    sys.path.insert(0, 'C:\\Users\\Admin\\smth\\play')
with patch.dict('sys.modules',
                {'tournament_systems.tournament_system': MagicMock(),
                 'TournamentSystem': MagicMock(),
                 'tournament_stages.round': MagicMock(),
                 'Round': MagicMock()}):
    from tournament_systems.tournament_system import TournamentSystem
    from tournament_stages.round import Round
    import tournament as tournament_file


class TournamentTest(unittest.TestCase):
    def test_tournament(self):
        TournamentSystem = MagicMock()
        TournamentSystem().get_results = 5
        TournamentSystem().get_rounds.return_value = [{1: {1: 0, 2: 1}},
                                                      {2: {2: 0, 3: 1}}]
        TournamentSystem().get_all_results.return_value = 'First player won'
        tournament = tournament_file.Tournament([1, 2, 3], 1)
        tournament.run()
        result = tournament.get_results()
        if result != 'First player won':
            raise Exception("tournament.py or 'patch.dict' doesn't work")

if __name__ == '__main__':
    unittest.main()
