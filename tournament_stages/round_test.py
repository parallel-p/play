import unittest
from unittest.mock import patch, Mock
from log import logger
with patch.dict('sys.modules', {'config': Mock(), 'series': Mock()}):
    import config
    import tournament_stages.series as series
    from tournament_stages.round import Round


class RoundTest(unittest.TestCase):
    def test_round(self):
        with patch('config.Generator') as Generator:
            test_round = Round(players_list=[[1, 2]],
                               game_info=None)
        self.assertEqual(test_round._players_list, [[1, 2]])
        self.assertEqual(test_round._game_info, None)

    def test_generate_series(self):
        with patch('config.Generator') as Generator:
            Generator().generate_start_positions.return_value = [42]
            test_round = Round(players_list=[[1, 2]],
                               game_info=Mock())
            test_round._generate_series()
            self.assertEqual(test_round._jurystates_list[0], 42)

    def test_run(self):
        with patch('config.Generator') as Generator:
            series.Series = Mock()
            series.Series().get_results.return_value = {'aba': 'caba'}
            test_round = Round(players_list=[[1, 2]],
                               game_info=Mock())
            test_round._jurystates_list = [Mock()]
            logger.setLevel(10050000)
            # logger = Mock()
            test_round.run()
            self.assertEqual(test_round.games_results, {'aba': 'caba'})

if __name__ == '__main__':
    unittest.main()
