import zipfile

ARCHIVE_NAME = 'redist.zip'

result = None
compression = None
try:
    result = zipfile.ZipFile(ARCHIVE_NAME, 'w', zipfile.ZIP_DEFLATED)
    compression = zipfile.ZIP_DEFLATED
except:
    result = zipfile.ZipFile(ARCHIVE_NAME, 'w')
    compression = zipfile.ZIP_STORED

file_list = {
    'lib/colorama/': 'lib/colorama/',
    'lib/colorama/__init__.py': 'lib/colorama/__init__.py',
    'lib/colorama/ansi.py': 'lib/colorama/ansi.py',
    'lib/colorama/initialise.py': 'lib/colorama/initialise.py',
    'lib/colorama/win32.py': 'lib/colorama/win32.py',
    'lib/colorama/winterm.py': 'lib/colorama/winterm.py',
    'lib/colorama/ansitowin32.py': 'lib/colorama/ansitowin32.py',
    'run_tools.py': 'run_tools.py',
    'config_helpers.py': 'config_helpers.py',
    'player.py': 'player.py',
    'games/pepelac/bots/stand.py': 'pepelac/bots/stand.py',
    'games/pepelac/bots/consequent_bot.py': 'pepelac/bots/consequent_bot.py',
    'games/pepelac/game_master.py': 'pepelac/game_master.py',
    'games/pepelac/player_state.py': 'pepelac/player_state.py',
    'games/pepelac/player.py': 'pepelac/player.py',
    'games/pepelac/jury_state.py': 'pepelac/jury_state.py',
    'games/pepelac/ascii_painter.py': 'pepelac/ascii_painter.py',
    'games/pepelac/move.py': 'pepelac/move.py',
    'games/pepelac/painter.py': 'pepelac/painter.py',
    'games/pepelac/generator.py': 'pepelac/generator.py',
    'games/pepelac/config.py': 'pepelac/config.py',
    'development_tools/__init__.py': 'development_tools/__init__.py',
    'development_tools/frame_visualizer.py':\
                                    'development_tools/frame_visualizer.py',
    'development_tools/ascii_visualizer.py':\
                                    'development_tools/ascii_visualizer.py',
    'game_controller.py': 'game_controller.py',
    'tournament_stages/round.py': 'tournament_stages/round.py',
    'tournament_stages/__init__.py': 'tournament_stages/__init__.py',
    'tournament_stages/exceptions.py': 'tournament_stages/exceptions.py',
    'tournament_stages/game.py': 'tournament_stages/game.py',
    'tournament_stages/series.py': 'tournament_stages/series.py',
    'tournament_stages/game_signature.py':\
                                      'tournament_stages/game_signature.py',
    'tournament_stages/tournament.py': 'tournament_stages/tournament.py',
    'README': 'README',
    'log.py': 'log.py',
    'bot.py': 'bot.py',
    'commands': 'commands',
    'lib/__init__.py': 'lib/__init__.py',
    'lib/keyboard_capture.py': 'lib/keyboard_capture.py',
    'game_simulator.py': 'game_simulator.py',
}

for name, archname in file_list.items():
    print('  {} -> {}/play/{}'.format(name, ARCHIVE_NAME, archname))
    result.write(name, 'play/' + archname, compression)

result.close()
