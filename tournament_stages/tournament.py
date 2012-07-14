from tournament_stages.round import Round
from tournament_stages.game_signature import GameSignature
from tournament_system.tournament_system_factory import create
from tournament_system.tournament_system import TournamentSystem


class Tournament:
    def __init__(self, players_list, tournament_id):
        self.players_list = players_list
        self.tournament_id = tournament_id
        self.results = None

    def run(self):
        '''
        Getting results of tournament.
        '''
        game_signature = GameSignature(self.tournament_id)

        tournament_system = create()(self.players_list)
        for round_id, round_info in enumerate(tournament_system.get_rounds()):
            game_signature.round_id = round_id
            _round = Round(game_series_list=round_info,
                           game_info=game_signature)
            _round.run()
            _round_results = _round.games_results
            tournament_system.give_round_results(_round_results)
        self.results = tournament_system.get_all_results()

    def get_results(self):
        if self.results is None:
            raise Exception("Results of the tournament haven't exist yet.")
        return self.results
