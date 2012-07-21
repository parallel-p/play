# -*- coding: utf-8 -*-
def Generator(*args, **kwargs):
    import generator
    return generator.Generator(*args, **kwargs)


def GameMaster(*args, **kwargs):
    import game_master
    return game_master.GameMaster(*args, **kwargs)


def Painter(*args, **kwargs):
    import painter
    return painter.Painter(*args, **kwargs)


def AsciiPainter(*args, **kwargs):
    import ascii_painter
    return ascii_painter.Painter(*args, **kwargs)


def default_pchars(player_num):
    return 'P{0:1x}'.format(player_num)

def alpha_pchars(num):
    if num < 10:
        c = chr(ord('0') + num)
    elif num <= 36:
        c = chr(ord('a') - 10 + num)
    else:
        c = chr(num)
    return 'P' + c


players_config = 'players_config'
apainter_chars = ('@@', '[]', '**', alpha_pchars)
apainter_colors = ((5, 8, 0), (3, 2, 2), (8, 0, 2), (4, 7, 0))

real_time_limit_seconds = 5.0
cpu_time_limit_seconds = 10.0
memory_limit_mb = 15.0

tournament_system = 'round-robin'
