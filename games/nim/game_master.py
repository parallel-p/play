from jury_state import JuryState
from player_state import serialize
from move import deserialize


class NumberOfPlayersException(Exception):
    pass


class GameMaster:
    def __init__(self, simulator, start_state):
        self._simulator = simulator
        self._players = simulator.get_players()
        if len(self._players) != 2:
            raise NumberOfPlayersException(
                'Number of players should be equal to 2')

    def tick(self, state):
        scores = dict(zip(self._players, [1, 1]))
        turn = 0
        while sum(state.heap_sizes) != 0:
            current_player = self._players[turn]
            try:
                move = self._simulator.get_move(
                    current_player, state.heap_sizes, serialize, deserialize)
            except OSError:
                break
            if not self._is_valid_move(state, move):
                break
            state.heap_sizes[move[0]] -= move[1]
            self._simulator.report_state(state)
            turn = 1 - turn
        scores[self._players[turn]] = 0
        self._simulator.finish_game(scores)

    def _is_valid_move(self, state, move):
        return (0 <= move[0] < len(state.heap_sizes) and
                1 <= move[1] <= state.heap_sizes[move[0]])
