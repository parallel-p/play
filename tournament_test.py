import unittest
from unittest.mock import MagicMock, Mock, patch
with patch.dict('sys.modules', {'tournament_system': MagicMock()}):
    import tournament_system as ts
    import tournament as tournament_file


class TournamentTest(unittest.TestCase):
    def test_tournament(self):
        ts.TournamentSystem = MagicMock()
        ts.TournamentSystem().get_rounds.return_value = [{1: {1: 0, 2: 1}},
                                                         {2: {2: 0, 3: 1}}]
        tournament = tournament_file.Tournament([1, 2, 3], MagicMock())
        tournament.run()
        result = tournament.get_results()

if __name__ == '__main__':
    unittest.main()
