# -*- coding: utf-8 -*-


class JuryState:
    def __init__(self, field_side, field, bullets,
                 explosion_time, dead_players=[], dead_reasons={},
                 collision=None, scores={}):
        '''
        field_side is side of field
        field is the current field:

        if field[i][j] = -2 then that cell is charred
        if field[i][j] = -1 then there is a bullet in cell (i, j)
        if field[i][j] = 0 then cell (i, j) is empty
        if field[i][j] >= 1 then there is player in cell (i, j)

        bullets is list of quantities of bullets, which players have

        explosion_time is time before the explosion of the field

        dead_reasons is map from player to reason of his death

        if dead_reasons[player] == -1 then player stepped somewhere wrong
        if dead_reasons[player] == 0 then player was killed by Armageddon
        if dead_reasons[player] == 1 then player was killed with bullet
        Otherwise, an error has occurred and dead_reasons[player] is a string
        with its representation.
        '''
        self.field_side = field_side
        self.field = field
        self.bullets = bullets
        self.explosion_time = explosion_time
        self.dead_players = dead_players
        self.dead_reasons = dead_reasons
        self.collision = collision
        self.scores = scores
