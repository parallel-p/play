import sys
import os
import player


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


def _return_player(string):
    quotes = 0
    current_string = ''
    word_list = list()
    valid_char = 1
    for ch in string:
        valid_char = 1
        if (ch == '\'' or ch == '\"'):
            quotes += 1
            valid_char = 0
        if (ch == ' ' and quotes == 0):
            if (len(current_string) > 0):
                word_list.append(current_string)
            current_string = ''
            valid_char = 0
        if (quotes == 2):
            word_list.append(current_string)
            current_string = ''
            quotes = 0
        if (valid_char):
            current_string += ch
    if (len(current_string) > 1):
        if (current_string[-1] == '\n' or current_string[-1] == '\0'):
            current_string = current_string[0:-1]
        word_list.append(current_string)
    if (len(word_list) > 2):
        #word_list[0] - author's name
        #word_list[1] - bot's name
        #word_list[2] - bot path
        return player.Player(word_list[2], word_list[0], word_list[1])


def players_parse(path):
    """This function parses config file and returns list of Players"""
    config_file = open(path, 'r')
    lines = config_file.readlines()
    config_file.close()
    players_list = list()
    for line in lines:
        players_list.append(_return_player(line))
    return players_list
