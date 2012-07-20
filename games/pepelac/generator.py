import random
import copy
from jury_state import JuryState

_field_size = 15


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
        for player in range(players_count):
            player_x = random.randint(0, _field_size - 1)
            player_y = random.randint(0, _field_size - 1)
            while (new_field[player_x][player_y] != 0 or
                   self._collect_around(field, player_x, player_y)):
                player_x = random.randint(0, _field_size - 1)
                player_y = random.randint(0, _field_size - 1)
            new_field[player_x][player_y] = player + 1
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
        _field_size = random.randint(10, 50)
        self.bullets_count = self.players_count * 5
        for game in range(self._games_count):
            field = [[0 for i in range(_field_size)]
                     for j in range(_field_size)]
            field = self.generate_players(field, self.players_count)
            self.bullets = [0] * self.players_count
            field = self.generate_bullets(field, self.bullets_count)
            yield JuryState(_field_size, field, self.bullets, self.time, [], [])
