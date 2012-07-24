from jury_state import JuryState
from unittest.mock import Mock
from painter import Painter
from PIL import Image
import unittest
import random


class PainterTests(unittest.TestCase):
    def test_type(self):
        jury_state = JuryState(list(range(9)))
        current_painter = Painter(Mock())
        byte_string = current_painter.ascii_paint(jury_state)
        self.assertEqual(byte_string, '0 1 2\n3 4 5\n6 7 8')

if __name__ == '__main__':
    unittest.main()
