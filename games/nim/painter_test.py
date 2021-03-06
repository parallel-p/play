from jury_state import JuryState
from painter import Painter
from PIL import Image
import unittest
import random


class PainterTests(unittest.TestCase):
    def test_type(self):
        jury_state = JuryState(list(range(20)))
        current_painter = Painter(['John Smith'])
        byte_string = current_painter.paint(jury_state)
        self.assertTrue(isinstance(byte_string, bytes))

if __name__ == '__main__':
    unittest.main()
