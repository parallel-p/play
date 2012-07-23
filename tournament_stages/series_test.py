import sys
sys.path.append('/home/daniel/play/play/')

import unittest
from unittest.mock import Mock, patch
from log import logger
from tournament_stages.series import Series


class SeriesTest(unittest.TestCase):

    def test_series_init(self):
        signature = Mock()
        series1 = Series([1], signature, [1, 2])
        self.assertEqual(series1._initial_jurystates, [1])
        self.assertEqual(series1._signature, signature)

    @patch('tournament_stages.series.Game')
    def test_run(self, mock_class):
        logger.setLevel(10050000)
        signature = Mock()
        mock_class().get_results.return_value = {
            '1': 123,
        }
        series1 = Series([1], signature, [1, 2])
        series1.run()
        result = {signature: {'1': 123}}
        self.assertEqual(list(series1._results.values()), list(result.values()))

    def test_get_results(self):
        signature = Mock()
        series1 = Series([1], signature, [1, 2])
        self.assertRaises(Exception, series1.get_results)
        series1._results = '123'
        self.assertEqual('123', series1.get_results())


if __name__ == '__main__':
    unittest.main()
