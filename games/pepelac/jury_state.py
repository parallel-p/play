class JuryState:
    def __init__(self, field_side, field, explosion_time):
        '''
        field_side is side of field
        field is the current field:

        if field[i][j] = -1 then there is a bullet in cell (i, j)
        if field[i][j] = 0 then cell (i, j) is empty
        if field[i][j] > 1 then there is player in cell (i, j)

        explosion_time is time before the explosion of the field
        '''
        self.field_side = field_side
        self.table = table
        self.time_before_explosion = explosion_time
