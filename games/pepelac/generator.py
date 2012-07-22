import random
import copy
from jury_state import JuryState
from math import sqrt, ceil

_field_size = random.randint(10, 20)


class Generator:
    def generate_players(self, field, players_count):
        new_field = copy.deepcopy(field)
        field_size_in_cells = int(ceil(sqrt(players_count)))
        cell_size = _field_size / field_size_in_cells

        for ind, cell in enumerate(random.sample(
                                   range(field_size_in_cells ** 2),
                                   players_count)):

            cell_x = cell // field_size_in_cells
            cell_y = cell % field_size_in_cells
            x = int(cell_x * cell_size + random.random() * cell_size)
            y = int(cell_y * cell_size + random.random() * cell_size)
            player_x = min(_field_size - 1, x)
            player_y = min(_field_size, y)

            assert(0 <= player_x < _field_size)
            assert(0 <= player_y < _field_size)
            assert(new_field[player_x][player_y] == 0)
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
            assert(0 <= bullet_x < _field_size)
            assert(0 <= bullet_y < _field_size)
            assert(new_field[bullet_x][bullet_y] == 0)
            new_field[bullet_x][bullet_y] = -1
        return new_field

    def generate_start_positions(self, game_signature, players_count):
        self.players_count = players_count
        self._games_count = 2
        '''Generates a list of start positions'''
        random.seed()
        self.time = random.randint(100, 140)
        self.bullets_count = min(_field_size ** 2 - players_count,
                                 self.players_count * 5
                                 )
        field = [[0 for i in range(_field_size)] for j in range(_field_size)]
        field = self.generate_players(field, self.players_count)
        field = self.generate_bullets(field, self.bullets_count)
        for game in range(self._games_count):
            players = []
            for i, row in enumerate(field):
                for j, cell in enumerate(row):
                    if (cell > 0):
                        players.append((i, j, cell))
            assert(len(players) == 2)
            field[players[0][0]][players[0][1]] = players[1][2]
            field[players[1][0]][players[1][1]] = players[0][2]

            self.bullets = [0] * players_count
            yield JuryState(_field_size, field, self.bullets, self.time)
