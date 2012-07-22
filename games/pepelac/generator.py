import random
import copy
from jury_state import JuryState
from math import sqrt
from math import ceil

_field_size = random.randint(10, 20)


class Generator:
    def generate_players(self, field, players_count):
        new_field = copy.deepcopy(field)
        cells_side = int(ceil(sqrt(players_count)))
        cell_size = _field_size / cells_side

        for ind, cell in enumerate(random.sample(range(cells_side ** 2),
                                   players_count)):
            cell_x, cell_y = cell // cells_side, cell % cells_side
            player_x = int(cell_x * cell_size + random.random() * cell_size)
            player_y = int(cell_y * cell_size + random.random() * cell_size)
            new_field[player_x][player_y] = ind + 1
        return new_field

    def generate_bullets(self, field, bullets_count):
        new_field = copy.deepcopy(field)
        for bullet in range(bullets_count):
            bullet_x = random.randint(0, _field_size - 1)
            bullet_y = random.randint(0, _field_size - 1)
            while new_field[bullet_x][bullet_y] != 0:
                bullet_x = random.randint(0, _field_size - 1)
                bullet_y = random.randint(0, _field_size - 1)
            new_field[bullet_x][bullet_y] = -1
        return new_field

    def generate_start_positions(self, game_signature, players_count):
        self.players_count = players_count
        self._games_count = 1
        '''Generates a list of start positions'''
        random.seed()
        self.time = random.randint(100, 140)
        self.bullets_count = self.players_count * 5
        for game in range(self._games_count):
            field = [[0 for i in range(_field_size)] for j in range(_field_size)]
            field = self.generate_players(field, self.players_count)
            self.bullets = [0] * self.players_count
            field = self.generate_bullets(field, self.bullets_count)
            yield JuryState(_field_size, field, self.bullets, self.time)
