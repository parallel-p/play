from tournament_systems.tournament_system import TournamentSystem
import tournament_systems.ascii_draw_table


class TournamentSystemEach(TournamentSystem):
    '''
    In this tournament system every player competes with each other.
    '''
    def get_rounds(self):
        '''
        Returns list of lists of players who plays in this round
        (play_list).
        '''
        play_list = []
        for first_player in range(len(self._players_list)):
            for second_player in range(first_player + 1,
                                       len(self._players_list)):
                play_list.append([self._players_list[first_player],
                       self._players_list[second_player]])
        yield play_list

    def _convert_score(self, score):
        '''
        Converts score from format (a, b) to string 'a:b'.
        '''
        return str(score[0]) + ':' + str(score[1])

    def get_table(self):
        '''
        Retuns the scores of the tournament in a table
        (list of strings).
        '''
        # List of list of cells
        table = []
        # Gets tuple of score using tuple of players
        scores = {}
        # Used to sort players in correct order, tuple (player, score)
        players = []
        # Current row
        row = []

        # Fills scores dict
        for game in self._results.values():
            current_game = []
            for player, score in game.items():
                current_game.append((player, score))
            ((first_player, first_score),
             (second_player, second_score)) = current_game
            scores[(first_player, second_player)] =\
                  (first_score, second_score)
            scores[(second_player, first_player)] =\
                   (second_score, first_score)

        # Fills players list
        for player in self._players_list:
            sum = 0
            for second_player in self._players_list:
                if player != second_player:
                    sum += scores[(player, second_player)][0]
            players.append((player, sum))
        # Sort players by score
        players.sort(reverse=True, key=lambda player: player[1])

        # Fills the header
        row.append('')
        for player in players:
            row.append(str(player[0]))
        row.append('Sum')
        table.append(row)

        # Fills the main data
        for first_player in players:
            # Player's name
            row = [str(first_player[0])]
            for second_player in players:
                if first_player == second_player:
                    row.append('')
                else:
                    row.append(self._convert_score(scores[(first_player,
                                                           second_player)]))
            # Fills the score cell
            row.append(str(first_player[1]))
            table.append(row)
        ascii_drawer = tournament_systems.ascii_draw_table.ASCIIDrawTable()
        return ascii_drawer.draw_table(table)
