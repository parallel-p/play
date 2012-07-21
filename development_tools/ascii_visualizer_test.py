import unittest as ut
from unittest.mock import Mock
import config_helpers
config_helpers.initialize_game_environment('games/nim')
from development_tools.ascii_visualizer import AsciiVisualizer


class AsciiVisualizerTestCase(ut.TestCase):
    @ut.mock.patch('print')
    def test_with_nim_ascii_painter(self):
        ''' Test with nim painter (we added it to nim). '''
        game_controller = Mock()
        game_controller.jury_states = []
        for i in range(100):
            sample_jury_state = Mock()
            sample_jury_state.heap_sizes = [i, i + 1, i + 2]
            game_controller.jury_states.append(sample_jury_state)
        vis = AsciiVisualizer(game_controller)
        vis.activate()

    def test_dump(self):
        game_controller = Mock()
        game_controller.jury_states = []
        for i in range(100):
            sample_jury_state = Mock()
            sample_jury_state.heap_sizes = [i, i + 1, i + 2]
            game_controller.jury_states.append(sample_jury_state)
        vis = AsciiVisualizer(game_controller)
        file = open('development_tools/testing/gamedump.txt', mode='wt')
        vis.dump(file)
        file.close()

if __name__ == "__main__":
    ut.main()
