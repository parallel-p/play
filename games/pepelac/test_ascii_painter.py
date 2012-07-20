# -*- coding: utf-8 -*-
from ascii_painter import Painter
import ascii_painter_test_data
import unittest
from unittest.mock import Mock


class ascii_painter_test(unittest.TestCase):
    def test_output(self):
        p1 = Mock()
        p1.bot_name = 'GoodBot'
        p1.author_name = 'Longcat'
        p2 = Mock()
        p2.bot_name = 'BadBot'
        p2.author_name = 'Tacgnol'
        p3 = Mock()
        p3.bot_name = 'DeadBot'
        p3.author_name = 'Tima'

        test_subject = Painter([p1, p2, p3])
        mock_js = Mock()
        mock_js.bullets = [6, 3, 0]
        mock_js.dead_players = [p3]
        for test in ascii_painter_test_data.tests:
            mock_js.field = test[0]
            picture = test_subject.ascii_paint(mock_js)
            print(picture)
            print(repr(picture))
            self.assertEqual(test[1], picture)

if __name__ == '__main__':
    unittest.main()
