class JuryState:
    def __init__(self, field, winner=None, line=-1):
        '''
        field - List of cells ('.', 'X', 'O')
        winner - Winner of the game (type is Player).
                  It is equal to None is game is not finished
        line - line of winner
        '''
        self.field = field
        self.winner = winner
        self.line = line