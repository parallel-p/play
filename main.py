import sys
import os
import argparse
from exceptions import PlayersException

'''
These strings add project_root to sys.path
'''
project_root = os.path.normpath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def get_free_dirname(path, filename_begin):
    for i in range(1, 1024):
        name = os.path.normpath(os.path.join(path, filename_begin + str(i)))
        if not os.path.exists(name):
            return i


'''
This horrible code parse arguments and import config and config_helpers,
with function initialize_game_environment it add game_path to sys.path
'''
import config_helpers
if __name__ == '__main__':
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
    game_path = args.game_path
    '''
    If tournament id isn't setted it will be least non-used one
    '''
    if not args.tournament_id:
        args.tournament_id = get_free_dirname(path='logs/',
                                              filename_begin='tournament')
    config_helpers.initialize_game_environment(game_path)
import config

from tournament_stages.tournament import Tournament
from utils import print_tournament_system_results


class Main:

    def __init__(self, game_path, tournament_id):
        self._game_path = game_path
        self.players_list = None
        self.tournament_id = tournament_id

    def _load_players(self):
        '''
        Load players_list with players_parse(it parses
        file containing player's information), filename is there in config
        '''
        players_config_path = os.path.join(self._game_path,
                                           config.players_config)
        self.players_list = config_helpers.players_parse(players_config_path)
        if self.players_list is None:
            raise PlayersException('Players list doesn\'t exist')

    def _run_tournament(self):
        '''
        Run tournament and get it's results
        '''
        self.tournament = Tournament(self.players_list,
                                     self.tournament_id)
        self.tournament.run()
        self.tournament_results = self.tournament.get_results()

    def show_result(self):
        return self.tournament_results

    def _print_tournament_results(self, ts):
            print_tournament_system_results(ts)

    def main(self):
        self._load_players()
        self._run_tournament()
        self._print_tournament_results(self.tournament.tournament_system)

if __name__ == '__main__':
    main = Main(game_path, args.tournament_id)
    main.main()
