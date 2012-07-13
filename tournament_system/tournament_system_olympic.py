import tournament_system
from math import log


class TournamentSystemOlympic(tournament_system.TournamentSystem):
    '''
    This class spends a game based on the Olympic tournament
    system, generating a list of players for each round based
    on the results of the previous one.
    '''
    def get_rounds(self):
        '''
        Yields lists of players for each round.
        '''
        list_of_players = self._players_list
        count_of_players = len(list_of_players)
        count_of_all_rounds = round(log(count_of_players))
        for game_round in range(count_of_all_rounds + 2):
            count_of_players = len(list_of_players)
            yield self.get_round(count_of_players, list_of_players)
            list_of_players = self.update_list_of_players(count_of_players)

    def get_round(self, count_of_players, list_of_players):
        '''
        Yields list of players for current round.
        '''
        for player in range(1, count_of_players, 2):
            yield [list_of_players[player - 1], list_of_players[player]]

    def update_list_of_players(self, count_of_players):
        '''
        Return list of players based on current scores of players.
        '''
        results = self.get_current_round_results()
        new_list_of_players = []
        for game in results.values():
            new_list_of_players.append(max(game.items(),
                                      key=lambda x: x[1])[0])
        return new_list_of_players
