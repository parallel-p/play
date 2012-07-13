import game_simulator
import unittest
import game_controller
from unittest.mock import Mock


class GameSimulatorTest(unittest.TestCase):
    def test_game(self):
        def game_side_effect(game_controller):
            game_controller.is_finished = 1
        game_master = Mock()
        game_master.tick.side_effect = game_side_effect
        config = Mock()
        config.game_master_constructor.return_value = game_master
        eng = game_simulator.GameSimulator(config, [], [], [])
        result = eng.play()
        game_master.tick.assert_called_once()

        answer = game_controller.GameController(config, [], [], [])
        answer.is_finished = 1
        self.assertEqual(answer.is_finished, result.is_finished)


if __name__ == '__main__':
    unittest.main()
