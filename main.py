import sys
import os

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from unittest.mock import Mock, MagicMock
import config_helpers
from tournament_stages.tournament import Tournament

tournament_id = 1


class Main:

    def __init__(self, game_path, tournament_id):
        self.players_list = None
        self.tournament_id = tournament_id

    def load_config(self):
        '''
        Run something which allow import config and import config
        '''
        config_helpers.initialize_game_environment()
        import config

    def load_players(self):
        '''
        Load players_list with players_parse(it parses
        file containing player's information), filename is there in config
        '''
        self.players_list = config_helpers.players_parse(config.players_config)
        if self.players_list is None:
            raise Exception("Players list doesn't exist")

    def run_tournament(self):
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
        self.load_config()
        self.load_players()
        self.run_tournament()

if (__name__ == '__main__'):
    main = Main(game_path, 1)
    if len(sys.argv) > 1:
        game_path = sys.argv[1]
    else:
        game_path = "C:\\Users\\Admin\\smth\\play"
    main = Main(game_path, tournament_id)
    main.main()
