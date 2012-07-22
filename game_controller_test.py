GAME_PATH = 'games/pepelac'
import config_helpers
config_helpers.initialize_game_environment(GAME_PATH)
import config
import unittest
import copy
import bot
from unittest.mock import Mock
import game_controller
from game_controller import GameNotFinishedException

class GameControllerTest(unittest.TestCase):
    def setUp(self):
        self.players = [4, 5]
        self.signature = ''
        self.jury_state = ''
        self._simulator = Mock()
        self.game = game_controller.GameController(self.players,\
                    self.signature, self.jury_state, self._simulator)
        self.game.is_finished = False
        self.game._scores = {'5'}
    
    def test_finish_game(self):
        self.is_finished = False
        with self.assertRaises(GameNotFinishedException):
            self.game.get_scores()
        self.game.finish_game(self.game._scores)
        self.assertTrue(self.game.is_finished)

    def test_get_scores(self):
        self.game.is_finished = True
        self.assertEqual(self.game._scores, self.game.get_scores())

    def test_get_players(self):
        self.assertEqual(self.players, self.game.get_players())

if __name__ == '__main__':
    unittest.main()
