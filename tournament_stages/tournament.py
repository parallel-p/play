from tournament_stages.round import Round
from tournament_stages.game_signature import GameSignature
from tournament_systems.tournament_system_factory import create
from tournament_stages.exceptions import NoResultsException
from log import logger


class Tournament:
    def __init__(self, players_list, tournament_id):
        self.players_list = players_list
        self.tournament_id = tournament_id
        self.results = None
        self.tournament_system = None

    def run(self):
        '''
        Getting results of tournament.
        '''
        logger.info('running tournament #%d', self.tournament_id)

        game_signature = GameSignature(self.tournament_id)

        self.tournament_system = create()(self.players_list)
        for round_id, players in enumerate(self.tournament_system.get_rounds()):
            game_signature.round_id = round_id
            # If our tournament can give names to rounds, e.g. olympic,
            # we should also assign a name to the round. But it is also
            # possible, that get_round_name returns None.
            game_signature.round_name = self.tournament_system.get_round_name(
                round_id, len(list(self.tournament_system.get_rounds())))
            _round = Round(list(players), game_signature)
            _round.run()
            _round_results = _round.games_results
            self.tournament_system.add_round_results(_round_results)
        self.results = self.tournament_system.get_all_results()
        logger.info('tournament #%d finished', self.tournament_id)

    def get_results(self):
        if self.results is None:
            raise NoResultsException(
              'Results of the tournament haven\'t exist yet.')
        return self.results
