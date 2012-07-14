GAME_PATH = 'games/nim'
BOTS = ['python3 games/nim/bots/random_bot.py',
        'python3 games/nim/bots/wrong_bot.py']

import unittest
import random
from tournament_stages.game_signature import GameSignature
from player import Player
from game_simulator import GameSimulator

import config_helpers
config_helpers.initialize_game_environment(GAME_PATH)
import config


class GameModulesIntegrationTests(unittest.TestCase):
    def setUp(self):
        signature = GameSignature()
        players = [Player(command_line) for command_line in BOTS]
        generator = config.Generator()
        start_states = list(generator.generate_start_positions(signature,
                                                               len(players)))
        start_state = random.choice(start_states)
        self._simulator = GameSimulator(config, players, start_state,
                                        signature)

    def test_that_game_is_finished(self):
        controller = self._simulator.play()
        self.assertTrue(controller.is_finished)

    def test_that_scores_exists_for_each_player(self):
        controller = self._simulator.play()
        scores = controller.get_scores()
        players = controller.get_players()
        self.assertEqual(set(scores.keys()), set(players))

if __name__ == '__main__':
    unittest.main()
