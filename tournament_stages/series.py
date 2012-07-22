from tournament_stages.exceptions import NoResultsException
from tournament_stages.game import Game
from copy import copy
from log import logger


class Series:
    '''
    Series - a collection games of one round of involving the same members.
    '''

    def __init__(self, initial_jurystates, signature, players_list):
        '''
        initial_jurystates_list - list of initial juristates.
        '''
        self._initial_jurystates = initial_jurystates
        self._signature = signature
        self._players_list = players_list
        self._results = None

    def run(self):
        '''
        Starts all games in series.
        '''
        logger.info('running series #%d', self._signature.series_id)
        self._results = {}
        for game_id, initial_jurystate in enumerate(self._initial_jurystates):
            self._signature.game_id = game_id
            _game = Game(initial_jurystate, self._signature,
                         self._players_list)
            _game.run_engine()
            points = _game.get_results()
            self._results[copy(self._signature)] = copy(points)

    def get_results(self):
        '''
        Returns results of the all games in series.
        '''
        if self._results is not None:
            return self._results
        else:
            raise NoResultsException('Series does not have the results yet.')
