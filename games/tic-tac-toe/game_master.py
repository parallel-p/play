from player_state import *
from move import *


class NumberOfPlayersException(Exception):
    pass


class IncorrectMoveException(Exception):
    pass


class GameMaster:
    def __init__(self, simulator, start_state):
        self._simulator = simulator
        self._players = simulator.get_players()
        self._state = start_state
        if len(self._players) != 2:
            raise NumberOfPlayersException(
                'Number of players should be equal to 2')

    def tick(self, js):
        scores = dict(zip(self._players, [0, 0]))
        turn = 0
        self._state.line = -1
        for i in range(9):
            turn = i % 2
            print('turn:', turn)
            current_player = self._players[turn]
            killed = True
            #try:
            ps = PlayerState(self._state.field)
            move = self._simulator.get_move(
                current_player, ps, serialize, deserialize)
            if not self._is_valid_move(self._state, move):
                turn ^= 1
                raise IncorrectMoveException('Incorrect move')

            if turn == 0:
                self._state.field[move[0] * 3 + move[1] - 4] = 'X'
            else:
                self._state.field[move[0] * 3 + move[1] - 4] = 'O'
            idx = self._eq3([[0, 1, 2], [3, 4, 5], [6, 7, 8],
                             [0, 3, 6], [1, 4, 7], [2, 5, 8],
                             [0, 4, 8], [2, 4, 6]], self._state.field)
            if idx != -1:
                self._state.line = idx
                break
            #except (IncorrectMoveException, OSError) as exception:
            #    print(exception)
            #    turn ^= 1
            #except Exception:
            #    turn ^= 1
            #else:
            #    killed = False
            if killed:
                self._simulator.report_state(self._state)
                continue

        scores[self._players[turn]] = 1

        if self._state.line != -1:
            self._simulator.report_state(self._state)
        self._state.winner = self._players[turn]
        self._simulator.report_state(self._state)

        self._simulator.finish_game(scores)

    def _is_valid_move(self, js, move):
        return (1 <= move[0] <= 3 and
                1 <= move[1] <= 3 and
                js.field[move[0] * 3 + move[1] - 4] == '.')

    def _eq3(self, lst, field):
        for idx, row in enumerate(lst):
            finish = True
            for i in range(2):
                if field[row[i]] != field[row[i + 1]]:
                    finish = False
            finish &= field[row[0]] != '.'
            if finish:
                return idx
        return -1
