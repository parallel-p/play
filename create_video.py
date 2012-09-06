from config_helpers import initialize_game_environment, players_parse
from visualizer import VideoVisualizer
import sys
from time import clock
import os

if len(sys.argv) < 5:
    print('Usage: create_video.py <path to game env> <folder with game logs> '
          '<filemask of logs> <resw_name> [-f <framerate>] [--silent]')
    exit(1)

if __name__ == '__main__':
    game_path, log_path, log_mask, res_name = sys.argv[1:5]
    if '-f' not in sys.argv:
        framerate = 24
    else:
        framerate = int(sys.argv[sys.argv.index('-f') + 1])
    silent = '--silent' in sys.argv
    initialize_game_environment(game_path)
    import config
    from tournament_systems.tournament_system_factory import create
    beg = clock()
    ts = create()(players_parse(os.path.join(game_path,
                                             config.players_config)))
    visualizer = VideoVisualizer(framerate, config.Painter, log_mask,
                                 log_path, res_name, silent, ts.draw_table
                                 if hasattr(ts, 'draw_table') else None)
    visualizer.compile()
    if not silent:
        print('Compiled in', clock() - beg, 'sec.')
