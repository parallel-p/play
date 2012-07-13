import unittest
from unittest.mock import Mock
import game_controller
import copy


class GameControllerTest(unittest.TestCase):
    def setUp(self):
        self.num_players = 5
        self.config = ''
        player = Mock()
        player.path_to_executable.return_value = ''
        self.players = [copy.deepcopy(player) for i in range(self.num_players)]
        self.signature = ''
        self.jury_state = ''
        self.game = game_controller.GameController(self.config, self.players,
            self.signature, self.jury_state)

    def tearDown(self):
        pass

    def test_create_bots(self):
        self.game.create_bots()
        self.assertEqual(len(self.game.bots), self.num_players)

    def test_kill_bots(self):
        self.game.kill_bots()
        self.assertEqual(len(self.game.bots), 0)

    def test_get_players(self):
        self.assertEqual(self.game.get_players(), self.players)

    def test_report_state(self):
        begin = len(self.game.jury_states)
        self.game.report_state(self.jury_state)
        end = len(self.game.jury_states)
        self.assertEqual(begin + 1, end)

if __name__ == '__main__':
    unittest.main()
