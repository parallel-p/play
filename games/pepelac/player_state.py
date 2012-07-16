def serialize_field_side(field_side, stream):
    representation = str(field_side) + '\n'
    stream.write(representation.encode())
    stream.flush()


class PlayerState:
    def __init__(self):
        self.explosion_time = None
        self.current_player = None
        self.players = []
        self.bullets = []


def list_to_str(lst):
    return ' '.join(map(str, lst))


def serialize_pstate(ps, stream):
    representation = '\n'.join(
        [
            list_to_str(
                [len(ps.players) + 1, len(ps.bullets), ps.explosion_time]
            ), list_to_str(ps.current_player)
        ] +
        [list_to_str(player) for player in ps.players] +
        [list_to_str(bullet) for bullet in ps.bullets]
    ) + '\n'
    stream.write(representation.encode())
    stream.flush()
