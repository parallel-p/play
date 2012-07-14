from abc import abstractmethod

class TournamentSystem:
    '''
    round_results format:
    {game_signature: {player: points, ...}, ...}
    '''

    def __init__(self, players_list):
        self._players_list = players_list
        self._results = {}
        self._all_rounds = [players_list]
        self._current_round_id = 0

    def add_round_results(self, round_results):
        '''
        Add round_results to all results of tournament
        '''
        self._results.update(round_results)
        self._current_round_id += 1

    def get_all_results(self):
        '''
        Return all results of tournament
        '''
        return self._results

    def get_round_results(self, round_id):
        '''
        Return results of round
        '''
        results = {}
        for game in self._results:
            if game.round_id == round_id:
                results.update({game: self._results[game]})
        return results

    def get_current_round_results(self):
        '''
        Return results of current round
        '''
        return self.get_round_results(self._current_round_id)

    def filter_results(tournament_id=None, round_id=None, series_id=None,
                       game_id=None):
        results = {}
        for game in self._results:
            if not (tournament_id and tournament_id != game.tournament_id or
                    round_id and round_id != game.round_id or
                    series_id and series_id != game.series_id or
                    game_id and game_id != game.game_id):
                results.update({game: self._results[game]})

    @abstractmethod
    def get_rounds(self):
        '''
        Yield players_list for every round
        '''
        pass

    @abstractmethod
    def get_table(self):
        '''
        Return list of strings
        '''
        return ['']
