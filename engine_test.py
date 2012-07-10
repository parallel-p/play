import engine
import unittest
import game_controller
from unittest.mock import Mock


class CoreTest(unittest.TestCase):
    def test_game(self):
        def game_side_effect(game_controller):
            game_controller.isfinished = 1
        game_master = Mock()
        game_master.tick.side_effect = game_side_effect
        GameMaster = Mock(return_value=game_master)
        eng = engine.Engine(GameMaster)
        result = eng.play()
        game_master.tick.assert_called_once()

        answer = game_controller.GameController()
        answer.isfinished = 1
        self.assertEqual(answer.isfinished, result.isfinished)


if __name__ == '__main__':
    unittest.main()
