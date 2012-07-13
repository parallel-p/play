import unittest
import copy
import bot
from unittest.mock import Mock
import game_controller


class GameControllerTest(unittest.TestCase):
    def setUp(self):
        self.num_players = 5
        self.config = 'cfg'
        player = Mock()
        player.command_line = 'bash'
        self.players = [copy.deepcopy(player) for i in range(self.num_players)]
        self.signature = ''
        self.jury_state = ''
        self.game = game_controller.GameController(self.config, self.players,
            self.signature, self.jury_state)

    def test_create_bots(self):
        bot.Bot = Mock()
        bot.Bot.return_value = True
        self.game.create_bots()
        self.assertEqual(self.game.bots, dict(zip(self.players,
            [True] * self.num_players)))
        self.assertEqual(bot.Bot.call_args_list,
            [(("bash", "cfg"),)] * self.num_players)

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
