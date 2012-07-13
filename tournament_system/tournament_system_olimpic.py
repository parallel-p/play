import tournament_system
from math import log

class TournamentSystemOlimpic(tournament_system.TournamentSystem):
    def get_rounds(self):
        count_of_players = len(self._players_list)
        count_of_rounds = log(count_of_players)
        for game in range(count_of_rounds):
            get_game()

    def get_game(self):
        for player in range(1, count_of_players, 2):
            yield [self._players_list[player - 1], self._players_list[player]]
