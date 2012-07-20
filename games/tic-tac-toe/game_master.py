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

    def tick(self, js):
        scores = dict(zip(self._players, [0, 0]))
        turn = 0
        for i in range(9):
            current_player = self._players[turn]
            try:
                move = self._simulator.get_move(
                    current_player, js.field, serialize, deserialize)
            except OSError:
                turn ^= 1
                break
            if not self._is_valid_move(js, move):
                turn ^= 1
                break
            if i % 2 == 0:
                js.field[move[0] * 3 + move[1] - 4] = 'X'
            else:
                js.field[move[0] * 3 + move[1] - 4] = 'O'
            self._simulator.report_state(js)
            if self._eq3(((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)), js.field):
                break
            turn ^= 1
        scores[self._players[turn]] = 1
        self._simulator.finish_game(scores)

    def _is_valid_move(self, js, move):
        return (1 <= move[0] <= 3 and
                1 <= move[1] <= 3 and
                js.field[move[0] * 3 + move[1] - 4] == '.')

    def _eq3(self, lst, field):
        for row in lst:
            if field[row[0]] == field[row[1]] == field[row[2]] != '.':
                return True
            else:
                return False
