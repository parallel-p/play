import unittest as ut
from unittest.mock import Mock
import config_helpers
config_helpers.initialize_game_environment('games/nim')
from development_tools.ascii_visualizer import AsciiVisualizer
import config


class AsciiVisualizerTestCase(ut.TestCase):
    def test_with_nim_ascii_painter(self):
        ''' Test with nim painter (we added it to nim). '''
        game_controller = Mock()
        game_controller.jury_states = []
        for i in range(10):
            game_controller.jury_states.append(
                config.JuryState([i, i + 1, i + 2]))
        vis = AsciiVisualizer(game_controller)
        vis.activate()


if __name__ == "__main__":
    ut.main()
