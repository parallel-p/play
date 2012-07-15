import unittest
from unittest.mock import Mock, patch
from tournament_stages.game_signature import GameSignature
with patch.dict('sys.modules', {'game': Mock()}):
    import game
    from tournament_stages.series import Series


class SeriesTest(unittest.TestCase):

    def test_series_init(self):
        signature = GameSignature(1, 1, 1, 1)
        series1 = Series([1], signature, 'ololo', [1, 2])
        self.assertEqual(series1._initial_jurystates, [1])
        self.assertEqual(series1._signature, signature)

    def test_run(self):
        inst = Mock()
        inst.get_results.return_value = {
            '1': 123,
        }
        signature = GameSignature(1, 1, 1, 1)
        game.Game.return_value = inst
        series1 = Series([1], signature, 'ololo', [1, 2])
        series1.run()
        result = {signature: {'1': 123}}
        self.assertEqual(series1._results, result)

    def test_get_results(self):
        signature = GameSignature(1, 1, 1, 1)
        series1 = Series([1], signature, 'ololo', [1, 2])
        self.assertRaises(Exception, series1.get_results)
        series1._results = '123'
        self.assertEqual('123', series1.get_results())


if __name__ == '__main__':
    unittest.main()
