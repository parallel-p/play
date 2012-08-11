def list_to_str(lst):
    return ' '.join(map(str, lst))


def serialize(player_state, stream):
    representation = '\n'.join(
        [list_to_str(player_state.field[i]) for i in range(3)] +
        [list_to_str(player_state.field[i]) for i in range(3, 6)] +
        [list_to_str(player_state.field[i]) for i in range(6, 9)]
    )
    stream.write(representation.encode())
    stream.flush()


class PlayerState:
    def __init__(self, field):
        self.field = field
