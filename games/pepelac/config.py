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


players_config = 'players_config'

real_time_limit_seconds = 5.0
cpu_time_limit_seconds = 10.0
memory_limit_mb = 15.0

tournament_system = 'round-robin'
