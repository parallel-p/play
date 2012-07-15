import tournament_systems.ascii_draw_tree as ascii_draw_tree
from tournament_systems.tournament_system import TournamentSystem
from math import log


class TournamentSystemOlympic(TournamentSystem):
    '''
    This class spends a game based on the Olympic tournament
    system, generating a list of players for each round based
    on the results of the previous one.
    '''
    def __init__(self, players_list):
        self._players_list = players_list
        self._results = {}
        self._all_rounds = [players_list]
        self._current_round_id = -1
        self._list_of_rounds = []
        self._data = []

    def add_round_results(self, round_results):
        '''
        Add round_results to all results of tournament
        '''
        self._results.update(round_results)
        self._current_round_id += 1
        results_list = []
        for _, game in sorted(round_results.items()):
            games_results = []
            for player, score in game.items():
                games_results.append((player, score))
            results_list.append(games_results)
        self._data.append(results_list)

    def get_rounds(self):
        '''
        Yields lists of players for each round.
        '''
        list_of_players = self._players_list
        count_of_players = len(list_of_players)
        count_of_all_rounds = round(log(count_of_players, 2))
        if count_of_players == 0:
            raise Exception("No players found. Can not create Olympic system.")
        for game_round in range(count_of_all_rounds):
            count_of_players = len(list_of_players)
            yield self.get_round(count_of_players, list_of_players)
            list_of_players = self.update_list_of_players(count_of_players)

    def get_round(self, count_of_players, list_of_players):
        '''
        Yields list of players for current round.
        '''
        print(list_of_players)
        list_of_round = []
        for player in range(0, count_of_players - 1, 2):
            list_of_round.append([list_of_players[player],
                                  list_of_players[player + 1]])
        return list_of_round

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

    def get_table(self):
        '''
        Draw a table with results.
        '''
        tree_drawer = ascii_draw_tree.ASCIIDrawTree()
        return tree_drawer.draw_tree(self._data)
