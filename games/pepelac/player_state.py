def serialize_field_side(field_side, stream):
    stream.write(str(field_size) + '\n')
    stream.flush()


class PlayerState:
    explosion_time = None
    current_player = None
    players = []
    bullets = []


def list_to_str(lst):
    return ' '.join(lst)


def serialize_pstate(ps, stream):
    stream.write('\n'.join([
        list_to_str([len(ps.players) + 1, len(ps.bullets), ps.explosion_time]),
        list_to_str(ps.current_player),
        [list_to_str(player) for player in ps.players],
        [list_to_str(bullet) for bullet in ps.bullets]
    ]))
    stream.flush()
