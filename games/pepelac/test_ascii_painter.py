# -*- coding: utf-8 -*-
from ascii_painter import Painter
import ascii_painter_test_data
import unittest
from unittest.mock import Mock


class ascii_painter_test(unittest.TestCase):
    def test_default_output(self):
        mock_js = Mock()
        for test in ascii_painter_test_data.tests:
            test_subject = Painter(test['players'])
            mock_js.bullets = test['bullets']
            mock_js.dead_players = test['dead']
            mock_js.scores = test['scores']
            mock_js.dead_reason = test['why_dead']
            mock_js.collision = test['collisions']
            mock_js.field = test['field']
            picture = test_subject.ascii_paint(mock_js)
            print(picture)
            print(repr(picture))
            self.assertEqual(test['result'], picture)

if __name__ == '__main__':
    unittest.main()
