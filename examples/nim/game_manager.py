from jury_state import JuryState
from player_state import PlayerState


class IncorrectMoveException(Exception):
    pass


class GameManager:
    def play(self, js):
        '''Manages the game.
        "js" is the jury state, "ps" is the player state.
        yields jury state.'''

        sum_sizes = sum(js.heap_sizes)
        while sum_sizes > 0:
            for i, player in enumerate(js.players):
                js.turn = i
                player.get_move(PlayerState(js), move)
                self._check_move(i, move, js)
                js.heap_sizes[move.heap_number] -= move.removed_stones
                sum_sizes -= move.removed_stones
                if sum_sizes == 0:
                    player.points = 1
                    return js
                yield js

        #If sum_sizes==0 from the beginning of the game
        js.players[0].points = 1
        return js

    def _check_move(idx, move, js):
        '''Checks that move is correct.
        "idx" is index of the player,
        "move" is move of the player,
        "js" is the jury state.
        If move is incorrect, raises the exception.'''

        if not(
            0 <= move.heap_number < len(js.heap_sizes) and
            1 <= move.removed_stones <= js.heap_sizes[move.heap_number]
        ):
            raise IncorrectMoveException(
                'Player #{0} made an incorrect move'.format(idx)
            )
