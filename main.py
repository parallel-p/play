import sys
import os
from exceptions import MainArgumentException, PlayersException

'''
These strings add project_root to sys.path
'''
project_root = os.path.normpath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

'''
This horrible code import config and config_helpers,
with function initialize_game_environment it add game_path to sys.path
'''
import config_helpers
if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise MainArgumentException('Many or little arguments for main.py')
    game_path = sys.argv[1]
    config_helpers.initialize_game_environment(game_path)
import config

from tournament_stages.tournament import Tournament


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

    def main(self):
        self._load_players()
        self._run_tournament()

if __name__ == '__main__':
    main = Main(game_path, 1)
    main.main()
