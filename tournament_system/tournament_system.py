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

    def get_rounds(self):
        '''
        Yield players_list for every round
        '''
        pass

    def get_table(self):
        '''
        Return list of strings
        '''
        return ['']
