from jury_state import JuryState
from generator import Generator
import random
import unittest
from unittest.mock import Mock


class GeneratorTests(unittest.TestCase):
    def test_generator(self):
        generator_state = Generator()
        game_signature = None
        positions = Generator.generate_start_positions(
            generator_state,
            game_signature,
            2
        )
        for pos in positions:
            self.assertEqual(pos.field, ['.', '.', '.'] * 3)

if __name__ == '__main__':
    unittest.main()
