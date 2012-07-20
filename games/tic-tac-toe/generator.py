import random
from jury_state import JuryState


class Generator:
    _max_stones_count = 100
    _games_count = 1
    _heaps_count = 15

    def generate_start_positions(self, game_signature, players_count):
        '''Generates a list of start positions (Jury states)'''
        for game in range(self._games_count):
            yield JuryState(list('.') * 9)
