import game_controller
import unittest
from unittest.mock import Mock


config = ""
players = [Mock() for i in range(5)]
signature = ""
jury_state = ""


class GameControllerTest(unittest.TestCase):
    def setUp(self):
        self.game = game_controller.GameController(config, players,
            signature, jury_state)

    def tearDown(self):
        pass

    def test_create_bots(self):
        self.game.create_bots()
        self.assertEqual(len(self.game.bots), 5)

    def test_kill_bots(self):
        self.game.kill_bots()
        self.assertEqual(len(self.game.bots), 0)

    def test_get_players(self):
        self.assertEqual(self.game.get_players(), players)

    def test_report_state(self):
        begin = len(self.game.jury_states)
        self.game.report_state(jury_state)
        end = len(self.game.jury_states)
        self.assertEqual(begin + 1, end)

if __name__ == "__main__":
    unittest.main()
