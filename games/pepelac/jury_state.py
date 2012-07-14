from player import Player


class JuryState:
    def __init__(self, field_side, field, bullets, explosion_time, players):
        '''
        field_side is side of field
        field is the current field:

        if field[i][j] = -1 then there is a bullet in cell (i, j)
        if field[i][j] = 0 then cell (i, j) is empty
        if field[i][j] > 1 then there is player in cell (i, j)

        bullets is list of quantities of bullets, which players have

        explosion_time is time before the explosion of the field
        '''
        self.field_side = field_side
        self.field = field
        self.bullets = bullets
        self.explosion_time = explosion_time
        self.players = players
