# -*- coding: utf-8 -*-
from ascii_painter import Painter
import ascii_painter_test_data
import unittest
from unittest.mock import Mock


class ascii_painter_test(unittest.TestCase):
    def test_output(self):
        p1=Mock()
        p1.bot_name='bot1'
        p1.author_name='author1'
        p2=Mock()
        p2.bot_name='bot2'
        p2.author_name='author2'

        test_subject = Painter([p1,p2])
        mock_js = Mock()
        mock_js.bullets=[6,4]
        for test in ascii_painter_test_data.tests:
            mock_js.field = test[0]
            picture = test_subject.ascii_paint(mock_js)
            print(picture)
            print(repr(picture))
            self.assertEqual(test[1], picture)

if __name__ == '__main__':
    unittest.main()
