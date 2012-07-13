from unittest.mock import Mock, patch
import tournament_system as ts
from game_supporting_classes import GameSignature


tournament_id = 1


class Tournament:

    def __init__(self, players_list, config_data):
        self.players_list = players_list
        self.config_data = config_data
        self.results = None

    def run(self):
        '''
        Getting results of tournament.
        '''
        game_signature = GameSignature(tournament_id)
        tournament_system = ts.TournamentSystem(self.players_list,
                                                self.config_data)
        for round_id, round_info in enumerate(tournament_system.get_rounds()):
            game_signature.round_id = round_id
            _round = ts.Round(game_series_list=round_info,
                              game_info=game_signature,
                              config=self.config_data)
            _round.run()
            _round_results = _round.get_results
            tournament_system.give_round_results(_round_results)
        self.results = tournament_system.get_all_results()

    def get_results(self):
        if self.results is None:
            raise Exception("Results of the tournament haven't exist yet.")
        return self.results
