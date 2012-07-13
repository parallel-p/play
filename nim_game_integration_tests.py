import unittest
import random
from tournament_stages.game_signature import GameSignature
from player import Player
from game_simulator import GameSimulator

import config_helpers
config_helpers.initialize_game_environment('games/nim')
import config


class NimGameIntegrationTests(unittest.TestCase):
    def setUp(self):
        signature = GameSignature()
        generator = config.Generator()
        start_states = list(generator.generate_start_positions(signature))
        start_state = random.choice(start_states)
        players = [Player('games/nim/bots/ideal_bot'),
                   Player('games/nim/bots/wrong_bot.py')]
        self._simulator = GameSimulator(config, players, start_state,
                                        signature)

    def test_that_game_is_finished(self):
        controller = self._simulator.play()
        self.assertTrue(controller.is_finished)

if __name__ == '__main__':
    unittest.main()
