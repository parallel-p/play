# -*- coding: utf-8 -*-
from player_state import *
from move import *

EMPTY = 0
BULLET = -1
EXPLODED = -2
MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class IncorrectMoveException(Exception):
    pass


class GameMaster:
    def __init__(self, simulator, start_state):
        self._simulator = simulator
        self._players = simulator.get_players()
        side = start_state.field_side
        self._number_of_correct_cells = side ** 2
        self._last_exploded_cell = (-1, -1)
        self._direction = 0
        self._scores = {}
        self._players_poses = {}
        for player in self._players:
            self._scores[player] = 0
            try:
                move = self._simulator.get_move(
                    player, start_state.field_side,
                    serialize_field_side, deserialize_start
                )
            except OSError:
                self._kill_player(cur_player, 'made wrong init move')
        self._state = start_state
        self._simulator.report_state(self._state)

    def tick(self, state):
        self._state = state
        for turn, cur_player in enumerate(self._players):
            if(self._number_of_correct_cells == 0 or
               set(self._state.dead_players) == set(self._players)):
                self._simulator.finish_game(self._scores)
                return

            if cur_player in self._state.dead_players:
                continue

            ps = PlayerState()
            ps.explosion_time = self._state.explosion_time
            for i, row in enumerate(self._state.field):
                for j, cell in enumerate(row):
                    if cell == BULLET:
                        ps.bullets.append((i + 1, j + 1))
                    elif cell > 0:
                        player_id = cell - 1
                        self._players_poses[self._players[player_id]] = (i, j)
                        player = (i + 1, j + 1, self._state.bullets[player_id])
                        if player_id == turn:
                            ps.current_player = player
                        else:
                            ps.players.append(player)

            old_row, old_col = old_pos = self._players_poses[cur_player]
            try:
                move = self._simulator.get_move(
                    cur_player, ps, serialize_pstate, deserialize_move
                )

                if not self._is_correct_cell(old_pos, move):
                    raise IncorrectMoveException()
                new_row, new_col = new_pos = self._make_move(old_pos, move)
                cell = self._state.field[new_row][new_col]
                if cell > 0 and turn != cell - 1:
                    raise IncorrectMoveException()
            except (OSError, DeserializeMoveException, IncorrectMoveException):
                self._kill_player(cur_player, 'made wrong move')
                continue

            if cell == BULLET:
                self._state.bullets[turn] += 1

            self._state.field[old_row][old_col] = EMPTY
            self._state.field[new_row][new_col] = turn + 1
            self._players_poses[cur_player] = new_pos

            for move in MOVES:
                if self._is_correct_cell(new_pos, move):
                    col, row = pos = self._make_move(new_pos, move)
                    if self._state.field[col][row] > 0:
                        self._fight([new_pos, pos])
                        if cur_player in self._state.dead_players:
                            break

            self._simulator.report_state(self._state)

        for player in self._players:
            if not player in self._state.dead_players:
                self._scores[player] += 1

        self._state.scores = self._scores
        self._state.explosion_time -= 1
        if self._state.explosion_time < 0:
            self._explode_cell()

        self._simulator.report_state(self._state)

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
            self._kill_player(self._players[cell - 1],
                              'destroyed by Armageddon')

        self._state.field[new_pos[0]][new_pos[1]] = EXPLODED
        self._last_exploded_cell = new_pos
        self._direction = direction
        self._number_of_correct_cells -= 1

    def _fight(self, poses):
        players = []
        for pos in poses:
            players.append(self._state.field[pos[0]][pos[1]] - 1)

        bullets = [self._state.bullets[player_id] for player_id in players]
        if max(bullets) == 0:
            return
        delta = min(bullets)

        self._state.collision = [
            self._players[player_id] for player_id in players
        ]
        self._simulator.report_state(self._state)
        self._state.collision = None

        kill = 0
        for player_id in players:
            self._state.bullets[player_id] -= delta
            if self._state.bullets[player_id] == 0:
                kill ^= 1
                kill_player_id = player_id

        if kill == 1:
            self._kill_player(self._players[kill_player_id],
                              'killed with bullet')

    def _kill_player(self, player, reason):
        self._state.dead_players.append(player)
        self._state.dead_reason[player] = reason
        pos = self._players_poses[player]
        self._state.field[pos[0]][pos[1]] = EMPTY
