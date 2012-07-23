from config_helpers import initialize_game_environment, players_parse
from visualizer import VideoVisualizer
import sys
from time import clock
from tournament_systems.tournament_system_factory import create
import os

if len(sys.argv) < 5:
    print('Usage: create_video.py <path to game env> <folder with game logs> '
          '<filemask of logs (regular expression)> <resw_name> '
          '[-f <framerate>] [--silent]')
    exit()

if __name__ == '__main__':
    game_path, log_path, log_mask, res_name = sys.argv[1:5]
    framerate = 3 if '-f' not in sys.argv else int(sys.argv[sys.argv.index('-f') + 1])
    silent = '--silent' in sys.argv
    initialize_game_environment(game_path)
    import config
    beg = clock()
    ts = create()(players_parse(os.path.join(game_path, config.players_config)))
    visualizer = VideoVisualizer(framerate, config.Painter, log_mask,
                                 log_path, silent, ts.draw_table if hasattr(ts, 'draw_table') else None)
    visualizer.compile(res_name)
    if not silent:
        print('Compiled in', clock() - beg, 'sec.')
