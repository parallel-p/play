import random
import copy
from jury_state import JuryState
from math import sqrt
from math import ceil

_field_size = random.randint(20, 30)


class Generator:
    def _collect_around(self, field, x, y):
        val = 0
        if x > 1:
            val += bool(field[x - 1][y])
        if y > 1:
            val += bool(field[x][y - 1])
        if x < _field_size - 1:
            val += bool(field[x + 1][y])
        if y < _field_size - 1:
            val += bool(field[x][y + 1])

        return bool(val)

    def generate_players(self, field, players_count):
        new_field = copy.deepcopy(field)
        sells_side = int(ceil(sqrt(players_count)))
        sell_size = _field_size / sells_side

        for ind, sell in enumerate(random.sample(range(sells_side ** 2),
                                  players_count)):
            sell_x, sell_y = sell // sells_side, sell % sells_side
            player_x = int(sell_x * sell_size + random.random() * sell_size)
            player_y = int(sell_y * sell_size + random.random() * sell_size)
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
            field = [[0 for i in range(_field_size)]
                     for j in range(_field_size)]
            field = self.generate_players(field, self.players_count)
            self.bullets = [0] * self.players_count
            field = self.generate_bullets(field, self.bullets_count)
            yield JuryState(_field_size, field, self.bullets, self.time)
