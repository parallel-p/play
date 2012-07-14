import tournament_system
import ascii_draw_table


class TournamentSystemEach(tournament_system.TournamentSystem):
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
        return play_list

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
        scores = {}
        table = []
        row = []
        #Used to sort rows and then add to table
        rows = []
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
        #Header
        row.append('')
        for player in self._players_list:
            row.append(str(player))
        row.append('Sum')
        table.append(row)

        #Main data
        for first_player in self._players_list:
            row = [(str(first_player))]
            current_sum = 0
            for second_player in self._players_list:
                if first_player == second_player:
                    row.append('')
                else:
                    score = scores[(first_player, second_player)]
                    current_sum += score[0]
                    score = self._convert_score(score)
                    row.append(score)
            #Score cell
            row.append(str(current_sum))
            rows.append((current_sum, row))
        rows.sort(reverse=True)
        for row in rows:
            table.append(row[1])
        ascii_drawer = ascii_draw_table.ASCIIDrawTable()
        return ascii_drawer.draw_table(table)
