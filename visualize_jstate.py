import sys
import os
import subprocess
import argparse

arg_parser = argparse.ArgumentParser(description='''
Visualize_jstate visualizate one game with jstate(GameController) file.
                                                 ''')
arg_parser.add_argument(
    'game_path',
    help='Directory containing game')
arg_parser.add_argument(
    '-f', '--framerate', type=int, default='24',
    help='Framerate of output video (default 24)')
arg_parser.add_argument(
    'game_controller_directory',
    help='Directory with GameController files')
arg_parser.add_argument(
    'game_controller_filemask',
    help='File mask of GameController files (regular expression)')
args = arg_parser.parse_args()

from visualizer import VideoVisualizer
import config_helpers
config_helpers.initialize_game_environment(args.game_path)
import config

output_name = 'output.mpg'


'''
Run Visualizer
'''
vjs = VideoVisualizer(args.framerate, config.Painter(),
                      args.game_controller_filemask,
                      args.game_controller_directory)
vjs.compile(output_name)

output_name = output_name[:output_name.rfind('.')] + '1.mpg'
output_place = os.path.join(os.path.dirname(__file__),
                            args.game_controller_directory, output_name)

'''
Play results
'''
subprocess.call('ffplay -x 640 -y 480 ' + output_place)
os.remove(output_place)
