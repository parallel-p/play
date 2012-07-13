import random
from jury_state import JuryState

_field_size_x = 50
_field_size_y = 50


class Generator:
    def generate_start_postion(self, game_signature, players_count):
        '''Generates a list of start positions'''
        bullets_count = players_count * 5
        for game in range(players_count):
            field = [[0 for i in range(_field_size_x)]
                for j in range(_field_size_y)]
            for player in range(players_count):
                player_x = randint(0, _field_size_x)
                player_y = randint(0, _field_size_y)
                while(field[player_x][player_y] != 0):
                    player_x = randint(0, _field_size_x)
                    player_y = randint(0, _field_size_y)
                field[player_x][player_y] = player + 1
            for bullet in range(bullets_count):
                bullet_x = randint(0, _field_size_x)
                bullet_y = randint(0, _field_size_y)
                while(field[bullet_x][bullet_y] != 0):
                    bullet_x = randint(0, _field_size_x)
                    bullet_y = randint(0, _field_size_y)
                field[bullet_x][bullet_y] = -1
            yield JuryState(field)
