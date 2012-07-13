import sys
from unittest.mock import Mock, MagicMock
import config_helpers
import config

tournament_id = 1


class Main:

    def __init__(self):
        self.players_list = None

    def load_config(self):
        '''
        Run something which allow import config and import config
        '''
        config_helpers.initialize_game_environment()

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
        tournament = Tournament(self.players_list, tournament_id)
        tournament.run()
        self.tournament_results = tournament.get_results()

    def show_result(self):
        return tournament_results

    def main(self, game_path):
        main = Main()
        main.load_config()
        main.load_players()
        main.run_tournament()

if (__name__ == '__main__'):
    if len(sys.argv) > 1:
        game_path = sys.argv[1]
    else:
        game_path = "C:\\Users\\Admin\\smth\\play"
    main = Main()
    main.main(game_path)
