def list_to_str(lst):
    return ''.join(map(str, lst))


def serialize(player_state, stream):
    print(player_state.field)
    field = player_state.field
    representation = '\n'.join([list_to_str([field[0], field[1], field[2]]),
                               list_to_str([field[3], field[4], field[5]]),
                               list_to_str([field[6], field[7], field[8]])])
    print('representation:', representation)
    print('representation.encode():', representation.encode())
    stream.write(representation.encode())
    print('HERE')
    stream.flush()


class PlayerState:
    def __init__(self, field):
        self.field = field
