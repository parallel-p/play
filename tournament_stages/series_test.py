import unittest
from unittest.mock import MagicMock, Mock, patch
from game_signature import GameSignature
with patch.dict('sys.modules', {'game': Mock(), 'log': Mock()}):
    import game
    import series


class SeriesTest(unittest.TestCase):

    def test_series_init(self):
        signature = GameSignature(1, 1, 1, 1)
        series1 = series.Series([1], signature, [1, 2])
        self.assertEqual(series1._initial_jurystates, [1])
        self.assertEqual(series1._signature, signature)

    def test_run(self):
        inst = Mock()
        results = {
            '1': 123,
        }
        inst.get_results.return_value = results
        signature = GameSignature(1, 1, 1, 1)
        game.Game.return_value = inst
        series1 = series.Series([1], signature, [1, 2])
        series1.run()
        results1 = series1._results
        results2 = {signature: results}
        signature1 = list(results1.keys())[0]
        signature2 = list(results2.keys())[0]
        self.assertEqual(signature1.tournament_id, signature2.tournament_id)
        self.assertEqual(signature1.round_id, signature2.round_id)
        self.assertEqual(signature1.series_id, signature2.series_id)
        self.assertEqual(signature1.game_id, signature2.game_id)
        self.assertEqual(list(results1.values())[0], list(results2.values())[0])
        
    def test_get_results(self):
        signature = GameSignature(1, 1, 1, 1)
        series1 = series.Series([1], signature, [1, 2])
        self.assertRaises(Exception, series1.get_results)
        series1._results = '123'
        self.assertEqual('123', series1.get_results())


if __name__ == '__main__':
    unittest.main()
