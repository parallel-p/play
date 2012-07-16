import sys
import os
import subprocess

if len(sys.argv) < 4:
    print('''visualize_jstate.py takes 4 arguments:
             game's path, framerate of video,
             directory with GameController files,
             file mask of GameController files (regular expression)''')
    exit()

from visualizer import VideoVisualizer
import config_helpers
config_helpers.initialize_game_environment(sys.argv[1])
import config

output_name = 'output.mpg'
framerate = int(sys.argv[2])
log_dir_name = sys.argv[3]
log_files_mask = sys.argv[4]


'''
Run Visualizer
'''
vjs = VideoVisualizer(framerate, config.Painter(), log_files_mask, log_dir_name)
#vjs = VideoVisualizer(25, config.Painter(), '0-0-0\.jstate', 'logs/tournament1')
vjs.compile(output_name)

output_name = output_name[:output_name.rfind('.')] + '1.mpg'
output_place = os.path.join(os.path.dirname(__file__), log_dir_name, output_name)

'''
Play results
'''
subprocess.call('ffplay -x 640 -y 480 ' + output_place)
os.remove(output_place)
