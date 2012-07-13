import tournament_system


class TournamentSystemOlimpic(tournament_system.TournamentSystem):
    def get_rounds(self):
        count_of_players = len(self._players_list)
        for player in range(1, count_of_players, 2):
            yield [self._players_list[player - 1], self._players_list[player]]
