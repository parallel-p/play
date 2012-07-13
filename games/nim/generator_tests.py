from jury_state import JuryState
from generator import Generator
import random
import unittest
from unittest.mock import Mock


class GeneratorTests(unittest.TestCase):
    def test_generator(self):
        tests_count = 1000
        for test in range(tests_count):
            players = []
            max_stones_count = random.randint(1, 10)
            games_count = 2
            generator_state = Generator(
                max_stones_count,
                games_count
            )

            players_count = random.randint(1, 10)
            game_signature = None
            positions = Generator.generate_start_positions(
                generator_state,
                game_signature,
                players_count
            )
            self.assertEqual(len(list(positions)), games_count)
            for position in positions:
                self.assertEqual(len(position.heaps_sizes), players_count)
                for heap_size in position.heaps_sizes:
                    self.assertTrue(1 <= heap_size <= max_stones_sizes)

if __name__ == '__main__':
    unittest.main()
