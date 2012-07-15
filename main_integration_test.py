import config_helpers
import os
import unittest
from visualizer import VideoVisualizer

game_path = 'games/nim/'
file_mask = '0-0-0\.jstate'
log_file = 'logs/tournament1/0-0-0.jstate'
config_helpers.initialize_game_environment(game_path)
from main import Main
import config


class MainTest(unittest.TestCase):
    def test_integration(self):
        main = Main(game_path, 1)
        main._load_players()
        main._run_tournament()
        self.assertTrue(os.path.exists(log_file))
        video_visualizer = VideoVisualizer(24, config.Painter(), file_mask,
                                           'logs/tournament1')
        video_visualizer.compile('test_video.mpg')
        self.assertTrue(os.path.exists('logs/tournament1/test_video.mpg'))


if __name__ == '__main__':
    unittest.main()
