from game_signature import GameSignature
from exceptions import NoResultsException
from game import Game


class Series:
    '''
    Series - a collection games of one round of involving the same members.
    '''

    def __init__(self, initial_jurystates_list, signature, config,
                 players_list):
        '''
        initial_jurystates_list - list of initial juristates.
        '''
        self._initial_jurystates_list = initial_jurystates_list
        self._signature = signature
        self._config = config
        self._players_list = players_list
        self._results = None

    def run(self):
        '''
        Starts all games in series.
        '''
        self._results = {}
        for game_id, initial_jurystate in enumerate(
                self._initial_jurystates_list):
            self._signature.game_id = game_id
            game = Game(initial_jurystate, self._signature, self._config,
                        self._players_list)
            game.run_engine()
            points = game.get_results()
            self._results[self._signature] = points

    def get_results(self):
        '''
        Returns results of the all games in series.
        '''
        if self._results is not None:
            return self._results
        else:
            raise NoResultsException('Series does not have the results yet.')
