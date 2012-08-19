from jury_state import JuryState
import random


class Generator:
    _games_count = 1

    def generate_start_positions(self):
        for game in range(self._games_count):
            field_side = 10
            empty_list = [0 for i in range(field_side)]
            empty_field = [empty_list for j in range(field_side)]
            yield JuryState(field_side, [empty_field, empty_field], None)
