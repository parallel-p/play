import random
import copy
from jury_state import JuryState

_field_size_x = 50
_field_size_y = 50


class Generator:
    def generate_players(field):
        new_field = copy.deepcopy(field)
        for player in range(self.players_count):
            player_x = randint(0, _field_size_x)
            player_y = randint(0, _field_size_y)
            while(new_field[player_x][player_y] != 0):
                player_x = randint(0, _field_size_x)
                player_y = randint(0, _field_size_y)
            new_field[player_x][player_y] = player + 1
        return new_field

    def generate_bullets(field):
        new_field = copy.deepcopy(field)
        for bullet in range(bullets_count):
            bullet_x = randint(0, _field_size_x)
            bullet_y = randint(0, _field_size_y)
            while(new_field[bullet_x][bullet_y] != 0):
                bullet_x = randint(0, _field_size_x)
                bullet_y = randint(0, _field_size_y)
            new_field[bullet_x][bullet_y] = -1
        return new_field

    def generate_start_postion(self, game_signature, players_count):
        self.players_count = players_count
        '''Generates a list of start positions'''
        random.seed()
        self.bullets_count = self.players_count * 5
        for game in range(players_count):
            field = [[0 for i in range(_field_size_x)]
                for j in range(_field_size_y)]
            field = generate_players(field)
            field = generate_bullets(field)
            yield JuryState(field)
