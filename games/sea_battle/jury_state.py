class JuryState:
    def __init__(self, field_side, fields, start_fields, ships, winner=None):
        '''
        field_side - The side of field

        fields - fields of players:
        field:
            -1 - exploded
            0 - empty
            1-4 - ships

        start_fields - start fields of players

        ships - all ships:
            ships[0] - ships of first player
            ships[1] - ships of second player
        ships of player - the list of ships
        ship - the list of cells (tuples)

        winner - Winner of the game (type is Player).
                 It is equal to None is game is not finished
        '''
        self.field_side = field_side
        self.fields = fields
        self.start_fields = start_fields
        self.ships = ships
        self.winner = winner
