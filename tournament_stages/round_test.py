import unittest
from unittest.mock import patch, Mock, MagicMock
with patch.dict('sys.modules', {'generator': Mock(), 'series': Mock()}):
    import generator
    import series
    import round


class RoundTest(unittest.TestCase):
    def test_round(self):
        test_round = round.Round(players_list=[[1, 2]],
                              game_info=None, config=None)
        self.assertEqual(test_round._players_list, [[1, 2]])
        self.assertEqual(test_round._game_info, None)

    def test_generate_series(self):
        generator.Generator = Mock()
        generator.Generator().generate_start_positions.return_value = [42]
        test_round = round.Round(players_list=[[1, 2]],
                              game_info=Mock(), config=None)
        test_round.generate_series()
        self.assertEqual(test_round._jurystates_list[0], 42)

    def test_run(self):
        series.Series = Mock()
        series.Series().get_results.return_value = {'aba': 'caba'}
        test_round = round.Round(players_list=[[1, 2]],
                              game_info=Mock(), config=None)
        test_round._jurystates_list = [Mock()]
        test_round.run()
        self.assertEqual(test_round.games_results, {'aba': 'caba'})

if __name__ == '__main__':
    unittest.main()
