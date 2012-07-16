# -*- coding: utf-8 -*-
from ascii_painter import Painter
import ascii_painter_test_data
import unittest
from unittest.mock import Mock


class ascii_painter_test(unittest.TestCase):
    def test_output(self):
        test_subject = Painter()
        mock_js = Mock()
        for test in ascii_painter_test_data.tests:
            mock_js.field = test[0]
            picture = test_subject.ascii_paint(mock_js)
            self.assertEqual(test[1], picture)

if __name__ == '__main__':
    unittest.main()
