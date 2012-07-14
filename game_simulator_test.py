import game_simulator
import unittest
import game_controller
from unittest.mock import Mock


class GameSimulatorTest(unittest.TestCase):
    def test_game(self):
        def game_master_side_effect(game_controller, jury_state):
            game_master._game_controller = game_controller
            return game_master

        def game_side_effect(jury_state):
            game_master._game_controller.is_finished = True
        game_master = Mock()
        game_master.is_finished = False
        game_master.tick.side_effect = game_side_effect
        config = Mock()
        config.GameMaster.side_effect=game_master_side_effect
        eng = game_simulator.GameSimulator(config, [], [], [])
        result = eng.play()
        game_master.tick.assert_called_once()

        answer = game_controller.GameController(config, [], [], [])
        answer.is_finished = True
        self.assertEqual(answer.is_finished, result.is_finished)


if __name__ == '__main__':
    unittest.main()
