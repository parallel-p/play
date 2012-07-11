# -*- coding: utf-8 -*-
from supporting_classes import GameSignature


class Series:

    """
    Series - a collection games of one round of  involving the same members.
    """

    def __init__(self, initial_jurystates_list, signature, config,
                 players_list):
        """
        initial_jurystates_list - list of initial juristates.
        """
        self.initial_jurystates_list = initial_jurystates_list
        self.signature = signature
        self.config = config
        self.players_list = players_list
        self.results = None

    def run(self):
        """
        Starts all games in series.
        """
        _results = {}
        for game_id, initial_jurystate in enumerate(
                self.initial_jurystates_list):
            self.signature.game_id = game_id
            _game = game.Game(initial_jurystate, self.signature, self.config,
                              self.players_list)
            _game.run_engine()
            points = _game.get_results()
            _results[self.signature] = points
        self.results = _results

    def get_results(self):
        """
        Returns results of the all games in series.
        """
        if self.results is not None:
            return self.results
        else:
            raise Exception('Series does not have the results yet.')
