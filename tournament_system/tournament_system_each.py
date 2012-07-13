import tournament_system


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

    def _cut_string(self, string, width):
        '''
        Makes the string len equal to width.
        If len(string) is less than width then
        method adds spaces.
        '''
        if len(string) < width:
            string += (' ' * (width - len(string)))
        string = string[:width]
        return string

    def _convert_score(self, score):
        '''
        Converts score from format (a, b) to string 'a:b'.
        '''
        return str(score[0]) + ':' + str(score[1])

    def _print_separator(self, width, columns):
        '''
        Returns the line of separators '-'.
        '''
        return str('*' + '-' * width) * columns + '*'

    def get_table(self, width):
        '''
        Yields the scores of the tournament in a table
        (string one by one), gets width of one column.
        '''
        table = {}
        rows = []
        for game in self._results.values():
            current_game = []
            for player, score in game.items():
                current_game.append((player, score))
            ((first_player, first_score), 
             (second_player, second_score)) = current_game
            table[(first_player, second_player)] =\
                  (first_score, second_score)
            table[(second_player, first_player)] =\
                  (second_score, first_score)
        #Quantity of columns
        columns = len(self._players_list) + 2
        #Print separator line
        yield self._print_separator(width, columns)
        #Header
        current_string = '|' + ' ' * width + '|'
        for player in self._players_list:
            current_string += self._cut_string(str(player), width)
            current_string += '|'
        current_string += self._cut_string('Sum', width) + '|'
        yield current_string
        #Main data
        for first_player in self._players_list:
            current_string = '|' + self._cut_string(str(first_player), width)
            current_string += '|'
            current_sum = 0
            for second_player in self._players_list:
                if first_player == second_player:
                    current_string += (' ' * width)
                else:
                    score = table[(first_player, second_player)]
                    current_sum += score[0]
                    score = self._convert_score(score)
                    current_string += self._cut_string(score, width)
                current_string += '|'
            #Score cell
            current_string += self._cut_string(str(current_sum), width)
            current_string += '|'
            rows.append((current_sum, current_string))
        rows.sort(reverse=1)
        for row in rows:
            yield self._print_separator(width, columns)
            yield row[1]
        yield self._print_separator(width, columns)
