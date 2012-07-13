import tournament_system


class TournamentSystemEach(tournament_system.TournamentSystem):
    '''
    In this tournament system every player competes with each other
    '''
    def get_rounds(self):
        '''
        Yields lists of players who plays in this round
        '''
        for first_player in range(len(self._players_list)):
            for second_player in range(first_player + 1,
                                       len(self._players_list)):
                yield [self._players_list[first_player],
                       self._players_list[second_player]]
