from config_helpers import initialize_game_environment
from visualizer import VideoVisualizer
import sys
from time import clock
import os

if len(sys.argv) < 4:
    print('Usage: create_video.py <path to game env> <log filename>'
          ' <output name> [-f <framerate>] [--silent]')
    print('Example: create_video.py pepelac log.gc -f 2')
    exit()

if __name__ == '__main__':
    game_path, log_name, res_name = sys.argv[1:4]
    if '-f' not in sys.argv:
        framerate = 24
    else:
        framerate = int(sys.argv[sys.argv.index('-f') + 1])
    silent = '--silent' in sys.argv
    initialize_game_environment(game_path)
    import config
    beg = clock()
    visualizer = VideoVisualizer(framerate, config.Painter, log_name,
                                 '.', silent)
    visualizer.compile(res_name)
    if not silent:
        print('Created in', clock() - beg, 'sec.')
