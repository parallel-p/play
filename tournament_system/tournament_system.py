class TournamentSystem:

    def __init__(self, players_list, config_data):
        self._players_list = players_list
        self._config_data = config_data
        self._results = {}
        self._all_rounds = [players_list]
        self._current_round_id = 0

    def add_round_results(self, round_results):
        self._results.update(round_results)
        self._current_round_id += 1

    def get_all_results(self):
        return self._results

    def get_round_results(self, round_id):
        for game in self.get_all_results():
            if game.round_id == round_id:
                yield game

    def get_current_round_results(self):
        return self.get_round_results(self._current_round_id)

    def get_rounds(self):
        pass

    def print_table(self):
        pass
