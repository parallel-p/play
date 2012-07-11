import unittest
from unittest.mock import MagicMock, Mock, patch
from game_supporting_classes import GameSignature
from tournament_system import Game, Series, Tournament, Round


class SeriesTest(unittest.TestCase):

    def test_series_init(self):
        signature = GameSignature(1, 1, 1, 1)
        series = Series([1], signature)
        self.assertEqual(series.initial_jurystates_list, [1])
        self.assertEqual(series.signature, signature)

    def test_run(self):
        inst = Mock()
        inst.get_results.return_value = {
            '1': 123,
        }
        signature = GameSignature(1, 1, 1, 1)
        Game.return_value = inst
        series = Series([1], signature)
        series.run()
        result = {signature: {'1': 123}}
        self.assertEqual(series.results, result)

    def test_get_results(self):
        signature = GameSignature(1, 1, 1, 1)
        series = Series([1], signature)
        self.assertRaises(Exception, series.get_results)
        series.results = '123'
        self.assertEqual('123', series.results)


if __name__ == '__main__':
    unittest.main()
