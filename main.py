import sys
import os
import argparse
from exceptions import PlayersException

'''
This horrible code parse arguments and import config and config_helpers,
with function initialize_game_environment it add game_path to sys.path
'''
import config_helpers
if __name__ == '__main__':
    '''
    These strings add project_root to sys.path
    '''
    project_root = os.path.normpath(os.path.join(os.path.dirname(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    '''
    Argument parseing:
    '''
    arg_parser = argparse.ArgumentParser(description='''
Framework runs game, placed in "game_path".
Players in this tournament read from file
"players_config" file, placed in "game_path"
path. Other settings of tournament should be written
in file "config.py", placed in "game_path".''')
    arg_parser.add_argument(
        'game_path',
        help='Directory containing game'
    )
    arg_parser.add_argument(
        '-tid', '--tournament-id', type=int,
        help='''
Tournament id which is used for saving logs,
if you don't set tournament id it will be least non-used one'''
    )
    args = arg_parser.parse_args()
    '''
    If tournament id isn't setted it will be least non-used one
    '''

    config_helpers.initialize_game_environment(args.game_path)
import config

from tournament_stages.tournament import Tournament
from utils import print_tournament_system_results
import bot


class Main:

    def __init__(self, game_path, tournament_id):
        self._game_path = game_path
        self._players_list = None
        self._tournament_id = tournament_id
        self.tournament = None

    def _load_players(self):
        '''
        Load players_list with players_parse(it parses
        file containing player's information), filename is there in config
        '''
        players_config_path = os.path.join(self._game_path,
                                           config.players_config)
        self._players_list = config_helpers.players_parse(players_config_path)
        if self._players_list is None:
            raise PlayersException('Players list doesn\'t exist')

    def _run_tournament(self):
        '''
        Run tournament and get it's results
        '''
        self.tournament = Tournament(self._players_list,
                                     self._tournament_id)
        self.tournament.run()
        self.tournament_results = self.tournament.get_results()

    def show_result(self):
        return self.tournament_results

    def _print_tournament_results(self, ts):
        print_tournament_system_results(ts)

    def _get_free_dirname(self, path, dirname_begin):
        for i in range(1, 1024):
            name = os.path.normpath(os.path.join(path, dirname_begin + str(i)))
            if not os.path.exists(name):
                return i

    def _make_good_tournament_id(self):
        if not self._tournament_id:
            self._tournament_id = self._get_free_dirname(path='logs/',
                dirname_begin='tournament')

    def main(self):
        self._load_players()
        self._make_good_tournament_id()
        try:
            self._run_tournament()
            self._print_tournament_results(self.tournament.tournament_system)
        except bot.ExecuteError:
            pass

if __name__ == '__main__':
    main = Main(args.game_path, args.tournament_id)
    main.main()
