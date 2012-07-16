from config_helpers import initialize_game_environment
from visualizer import VideoVisualizer
import sys
from time import clock

if len(sys.argv) < 5:
    print('Usage: game2video.py <path to game env> <folder with game logs> '
          '<filemask of logs (regular expression)> <resw_name> [<framerate>] '
          '[--silent]')
    exit()

if __name__ == '__main__':
    game_path, log_path, log_mask, res_name = sys.argv[1:5]
    framerate = 3 if len(sys.argv) < 6 else sys.argv[5]
    silent = len(sys.argv) > 6 and sys.argv[7] == '--silent'
    initialize_game_environment(game_path)
    import config
    beg = clock()
    VideoVisualizer(framerate, config.Painter(), log_mask, log_path, silent).compile(res_name)
    if not silent:
        print('Compiled in', clock() - beg, 'sec.')