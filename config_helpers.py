import sys
import os

def initialize_game_environment(path):
    '''
    This function modify `sys.path` to import configuration file
    from specified path.
    Argument `path` may be a configuration file name or directory
    where this file is located.
    '''
    path = os.path.abspath(path)
    if os.path.isdir(path):
        dirname = path
    else:
        dirname = os.path.dirname(path)
    sys.path.insert(0, dirname)
