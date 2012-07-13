class TournamentSystem:

    def __init__(self, players_list, config_data):
        self._players_list = players_list
        self._config_data = config_data
        self._results = []

    def give_round_results(self, round_results):
        self._results.append(round_results)

    def get_all_results(self):
        return self._results

    def get_rounds(self):
        pass
