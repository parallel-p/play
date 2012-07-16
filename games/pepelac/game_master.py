from player_state import *
from move import *

EMPTY = 0
BULLET = -1
EXPLODED = -2
MOVES = [(0, -1), (1, 0), (0, 1), (-1, 0)]


class NumberOfPlayersException(Exception):
    pass


class IncorrectMoveException(Exception):
    pass


class GameMaster:
    def __init__(self, simulator, start_state):
        self._simulator = simulator
        self._players = simulator.get_players()
        if len(self._players) != 2:
            raise NumberOfPlayersException(
                'Number of players should be equal to 2')
        side = start_state.field_side
        self._number_of_correct_cells = side ** 2
        self._last_exploded_cell = (-1, -1)
        self._direction = 0
        self._turn = 0
        self._scores = {}
        for player in self._players:
            move = self._simulator.get_move(
                player, start_state.field_side,
                serialize_field_side, deserialize_start
            )
            self._scores[player] = 0
        self._state = start_state
        self._simulator.report_state(self._state)

    def tick(self, state):
        self._state = state
        if(self._number_of_correct_cells == 0 or
           set(self._state.dead_players) == set(self._players)):
            self._simulator.finish_game(self._scores)
            return

        turn = self._turn
        self._turn = (turn + 1) % len(self._players)
        player = self._players[turn]
        if player in self._state.dead_players:
            return

        ps = PlayerState()
        ps.explosion_time = self._state.explosion_time
        for i, row in enumerate(self._state.field):
            for j, cell in enumerate(row):
                if cell == BULLET:
                    ps.bullets.append((i, j))
                elif cell > 0:
                    player_id = cell - 1  # players numering from the 1
                    if player_id == turn:
                        ps.current_player = (
                            i, j, self._state.bullets[cell - 1]
                        )
                    else:
                        ps.players.append(
                            (i, j, self._state.bullets[cell - 1])
                        )

        old_row, old_col = old_pos = ps.current_player[:2]
        try:
            move = self._simulator.get_move(
                player, ps, serialize_pstate, deserialize_move
            )

            if not self._is_correct_cell(old_pos, move):
                raise IncorrectMoveException()
            new_row, new_col = new_pos = self._make_move(old_pos, move)
            cell = self._state.field[new_row][new_col]
            if cell > 0 and turn != cell - 1:
                raise IncorrectMoveException()
        except(OSError, DeserializeMoveException, IncorrectMoveException) as e:
            self._state.dead_players.append(player)
            self._state.field[old_row][old_col] = EMPTY
            self._simulator.report_state(self._state)
            return
        if cell == BULLET:
            self._state.bullets[turn] += 1

        self._state.field[old_row][old_col] = EMPTY
        self._state.field[new_row][new_col] = turn + 1

        for move in MOVES:
            if self._is_correct_cell(new_pos, move):
                col, row = pos = self._make_move(new_pos, move)
                if(self._state.field[col][row] > 0 and
                   self._fight(new_pos, pos)):
                    self._simulator.report_state(state)
                    return

        for player in self._players:
            if not player in self._state.dead_players:
                self._scores[player] += 1

        self._state.explosion_time -= 1
        if self._state.explosion_time < 0:
            self._explode_cell()

        self._simulator.report_state(state)

    def _make_move(self, position, move):
        return tuple(x + dx for x, dx in zip(position, move))

    def _is_correct_cell(self, position, move):
        new_row, new_col = new_pos = self._make_move(position, move)
        for x in new_pos:
            if not (0 <= x < self._state.field_side):
                return False
        if self._state.field[new_row][new_col] == EXPLODED:
            return False
        return True

    def _explode_cell(self):
        last_cell = self._last_exploded_cell
        direction = self._direction
        if last_cell[0] == -1:
            new_pos = (0, 0)
            direction = 1
        else:
            while not self._is_correct_cell(last_cell, MOVES[direction]):
                direction = (direction + 1) % len(MOVES)
            new_pos = self._make_move(last_cell, MOVES[direction])

        cell = self._state.field[new_pos[0]][new_pos[1]]
        if cell > 0:
            self._state.dead_players.append(self._players[cell - 1])

        self._state.field[new_pos[0]][new_pos[1]] = EXPLODED
        self._last_exploded_cell = new_pos
        self._direction = direction
        self._number_of_correct_cells -= 1

    def _fight(self, pos1, pos2):
        row1, col1 = pos1
        row2, col2 = pos2
        p1 = self._state.field[row1][col1] - 1
        p2 = self._state.field[row2][col2] - 1
        delta = min(self._state.bullets[p1], self._state.bullets[p2])
        self._state.bullets[p1] -= delta
        self._state.bullets[p2] -= delta
        if(self._state.bullets[p1] == 0 and
           self._state.bullets[p2] > 0):
            self._state.dead_players.append(self._players[p1])
            self._state.field[row1][col1] = EMPTY
            return True
        elif(self._state.bullets[p1] > 0 and
             self._state.bullets[p2] == 0):
            self._state.dead_players.append(self._players[p2])
            self._state.field[row2][col2] = EMPTY
        return False
