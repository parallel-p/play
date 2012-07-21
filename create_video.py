from config_helpers import initialize_game_environment
from visualizer import VideoVisualizer
import sys
from time import clock
import os

if len(sys.argv) < 5:
    print('Usage: create_video.py <path to game env> <folder with game logs> '
          '<filemask of logs (regular expression)> <resw_name> '
          '[-f <framerate>] [--silent]')
    exit()

if __name__ == '__main__':
    game_path, log_path, log_mask, res_name = sys.argv[1:5]
    if '-f' not in sys.argv:
        framerate = 3
    else:
        mfpos = 5
        while sys.argv[mfpos] != '-f':
            mfpos += 1
        framerate = int(sys.argv[mfpos + 1])
    silent = '--silent' in sys.argv
    initialize_game_environment(game_path)
    import config
    beg = clock()
    visualizer = VideoVisualizer(framerate, config.Painter, log_mask,
                                 log_path, silent)
    visualizer.compile(res_name)
    if not silent:
        print('Compiled in', clock() - beg, 'sec.')
